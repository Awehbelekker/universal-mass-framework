"""MASS LangGraph orchestration pipeline.

Implements the MASS search pipeline as a LangGraph ``StateGraph``, following
the same architectural pattern as the ``deepagents`` framework (nodes → edges
→ compile → invoke).  The graph is a stateful reasoning pipeline that
processes a search query through intent classification then specialist nodes:

    receive_query → classify_intent → retrieve      → synthesize → END
                                   ↘ action_agent ↗
                                   ↘ web_search   ↗

Graph topology
--------------
::

    ┌──────────────┐     ┌──────────┐     ┌───────────┐
    │ receive_query│────▶│ retrieve │────▶│ synthesize│────▶ END
    └──────────────┘     └──────────┘     └───────────┘

State schema
------------
``MASSState`` is a TypedDict whose fields travel through every node.  The
``agent_trace`` list uses ``operator.add`` as its reducer so that each node
appends its name without replacing the accumulated list.

Retrieval (Move 1)
------------------
``retrieve_node`` performs real Supabase pgvector similarity search when
``SUPABASE_URL`` and ``SUPABASE_SERVICE_KEY`` are configured.  It falls back
to a single stub result when those env vars are absent (safe for CI / local
dev without credentials).

Flow:
  1. Embed the query with ``litellm.aembedding`` (model: ``embedding_model``).
  2. Call the ``match_documents`` RPC on Supabase via its REST API.
  3. Map each row to the ``SearchResult`` shape expected by ``synthesize_node``.

Usage
-----
::

    from mass.graph import build_graph

    graph = build_graph()
    final_state = await graph.ainvoke({
        "query": "what is MASS?",
        "context": None,
        "max_results": 10,
    })
"""

from __future__ import annotations

import logging
import operator
from typing import Annotated, Any

import httpx
import litellm
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict

from mass.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Langfuse — wire as a LiteLLM callback when credentials are present.
# LiteLLM reads LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY / LANGFUSE_HOST
# from the environment automatically; we just need to enable the handler.
# ---------------------------------------------------------------------------
if settings.langfuse_public_key and settings.langfuse_secret_key:
    litellm.success_callback = ["langfuse"]
    litellm.failure_callback = ["langfuse"]
    logger.info("Langfuse tracing enabled for LiteLLM calls.")


# ---------------------------------------------------------------------------
# State schema
# ---------------------------------------------------------------------------


class MASSState(TypedDict):
    """State that flows through every node in the MASS graph."""

    # ── Inputs ──────────────────────────────────────────────────────────────
    query: str
    """Raw search query supplied by the caller."""

    context: dict[str, Any] | None
    """Optional caller context (user_id, session_id, filters, …)."""

    max_results: int
    """Maximum number of results to retrieve."""

    # ── Intent (Move 2) ─────────────────────────────────────────────────────
    intent: str | None
    """Classified intent of the query. One of: search | product | order |
    action | web.  Set by ``classify_intent_node`` and used by conditional
    edges to route to the appropriate specialist node."""

    # ── Outputs ─────────────────────────────────────────────────────────────
    results: list[dict[str, Any]]
    """Retrieved evidence items (each maps to a ``SearchResult``)."""

    synthesis: str | None
    """LLM-synthesised answer drawn from results."""

    model: str | None
    """LLM model identifier used for synthesis."""

    # ── Observability ────────────────────────────────────────────────────────
    agent_trace: Annotated[list[str], operator.add]
    """Ordered list of node names traversed.  Uses ``operator.add`` as its
    LangGraph reducer so each node appends without replacing the list."""


# ---------------------------------------------------------------------------
# Node implementations
# ---------------------------------------------------------------------------


def receive_query_node(state: MASSState) -> dict[str, Any]:
    """Validate and pre-process the incoming query.

    Strips whitespace and initialises state fields so every downstream node
    can safely read them without KeyError.

    If ``intent`` is already set in the incoming state (e.g. the
    ``/intelligence`` endpoint pre-sets ``'competitive'``), it is preserved
    so ``classify_intent_node`` can skip classification entirely.
    """
    cleaned_query = state["query"].strip()
    # Preserve a caller-supplied intent (e.g. "competitive" from /intelligence)
    existing_intent = state.get("intent")
    return {
        "query": cleaned_query,
        "results": [],
        "synthesis": None,
        "intent": existing_intent,  # None resets; non-None is kept
        "model": settings.litellm_model,
        "agent_trace": ["receive_query"],
    }


# ---------------------------------------------------------------------------
# Intent classifier (Move 2)
# ---------------------------------------------------------------------------

_INTENT_SYSTEM_PROMPT = """\
You are an intent classifier for MASS, the AI intelligence layer powering
Awake (a surf/outdoor store) and DIGG (a content platform).

Classify the user query into EXACTLY ONE of these intents:

  search      – general knowledge, how-to, information lookup, definitions
  product     – product details, availability, pricing, sizing, specifications
  order       – order status, tracking, returns, delivery, invoices
  action      – create, update, delete, book, schedule, submit (requires an action)
  web         – needs live/real-time data only available on the internet
  competitive – owner asking about competitor pricing, market position, or cost moat

Reply with a single lowercase word — nothing else."""

_VALID_INTENTS = {"search", "product", "order", "action", "web", "competitive"}


async def classify_intent_node(state: MASSState) -> dict[str, Any]:
    """Classify the query intent using a fast LiteLLM call.

    If ``intent`` is already set (e.g. pre-set by the ``/intelligence``
    endpoint), classification is skipped and the existing value is kept.

    Uses a cheap, fast model (gpt-4o-mini by default) to keep latency low.
    Falls back to ``search`` if the LLM is unavailable or returns an
    unrecognised label — ensuring the graph always continues.
    """
    # Skip classification if the caller already pinned an intent
    if state.get("intent") in _VALID_INTENTS:
        logger.info("Intent pre-set to %r — skipping classifier.", state["intent"])
        return {"agent_trace": ["classify_intent"]}

    query = state["query"]
    try:
        response = await litellm.acompletion(
            model=settings.litellm_model,
            messages=[
                {"role": "system", "content": _INTENT_SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            max_tokens=5,
            temperature=0.0,
        )
        raw: str = (response.choices[0].message.content or "search").strip().lower()
        intent = raw if raw in _VALID_INTENTS else "search"
    except Exception as exc:
        logger.warning("Intent classification failed (%s); defaulting to 'search'.", exc)
        intent = "search"

    logger.info("Query %r classified as intent=%r", query, intent)
    return {
        "intent": intent,
        "agent_trace": ["classify_intent"],
    }


def _route_intent(state: MASSState) -> str:
    """Conditional edge function — maps intent → next node name."""
    intent = state.get("intent") or "search"
    if intent in ("search", "product", "order"):
        return "retrieve"
    if intent == "action":
        return "action_agent"
    if intent == "competitive":
        return "competitive_intel"
    # web (and any unknown fallback)
    return "web_search"


# ---------------------------------------------------------------------------
# Web Search Agent (Move 4)
# ---------------------------------------------------------------------------

_BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"
_SERPER_SEARCH_URL = "https://google.serper.dev/search"


async def web_search_node(state: MASSState) -> dict[str, Any]:
    """Live web retrieval agent — Brave Search API with Serper fallback.

    Priority order:

    1. **Brave Search** (``BRAVE_API_KEY``) — privacy-first, no tracking.
    2. **Serper** (``SERPER_API_KEY``) — Google results via REST.
    3. **Stub** — safe fallback when neither key is configured (CI / local dev).

    Results are mapped to the standard ``SearchResult`` shape so
    ``synthesize_node`` can consume them without modification.
    """
    query = state["query"]
    max_results = min(state.get("max_results", 5), 10)

    # ── Brave Search ──────────────────────────────────────────────────────────
    if settings.brave_api_key:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    _BRAVE_SEARCH_URL,
                    headers={
                        "Accept": "application/json",
                        "Accept-Encoding": "gzip",
                        "X-Subscription-Token": settings.brave_api_key,
                    },
                    params={"q": query, "count": max_results},
                )
                resp.raise_for_status()
                data = resp.json()
            results = [
                {
                    "content": item.get("description") or item.get("title", ""),
                    "source": item.get("url", "web"),
                    "score": 1.0,
                    "metadata": {
                        "title": item.get("title"),
                        "url": item.get("url"),
                        "provider": "brave",
                    },
                }
                for item in data.get("web", {}).get("results", [])
                if item.get("description") or item.get("title")
            ]
            if results:
                logger.info("Brave Search returned %d results for: %r", len(results), query)
                return {"results": results, "agent_trace": ["web_search"]}
        except Exception as exc:
            logger.warning("Brave Search failed (%s); trying Serper.", exc)

    # ── Serper ────────────────────────────────────────────────────────────────
    if settings.serper_api_key:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    _SERPER_SEARCH_URL,
                    headers={
                        "X-API-KEY": settings.serper_api_key,
                        "Content-Type": "application/json",
                    },
                    json={"q": query, "num": max_results},
                )
                resp.raise_for_status()
                data = resp.json()
            results = [
                {
                    "content": item.get("snippet", ""),
                    "source": item.get("link", "web"),
                    "score": 1.0,
                    "metadata": {
                        "title": item.get("title"),
                        "url": item.get("link"),
                        "provider": "serper",
                    },
                }
                for item in data.get("organic", [])
                if item.get("snippet")
            ]
            if results:
                logger.info("Serper returned %d results for: %r", len(results), query)
                return {"results": results, "agent_trace": ["web_search"]}
        except Exception as exc:
            logger.warning("Serper search failed (%s); using stub.", exc)

    # ── Stub fallback (no key or all requests failed) ─────────────────────────
    logger.info(
        "Web search stub for query: %r — set BRAVE_API_KEY or SERPER_API_KEY to enable.",
        query,
    )
    return {
        "results": [
            {
                "content": (
                    f"[WEB SEARCH] Live search for: {query!r}. "
                    "Set BRAVE_API_KEY or SERPER_API_KEY to enable real-time web retrieval."
                ),
                "source": "web-stub",
                "score": 1.0,
                "metadata": {"intent": "web", "mode": "stub"},
            }
        ],
        "agent_trace": ["web_search"],
    }


# ---------------------------------------------------------------------------
# Competitive Intelligence Node (Move 6)
# ---------------------------------------------------------------------------

_JINA_READER_URL = "https://r.jina.ai/"

_COMPETITIVE_SYSTEM_PROMPT = """\
You are MASS Competitive Intelligence — an AI advisor for business owners.

You will receive:
1. The owner's question about their product/market.
2. Scraped content from competitor websites.

Produce a concise competitive analysis covering:
- **Price position**: how the owner's pricing compares (cheaper / parity / premium).
- **Moat factors**: what makes the owner's offering uniquely valuable.
- **Recommendation**: hold price / adjust / reframe the value proposition.

Be specific. If prices are visible in the content, quote them. Keep the report under 400 words."""


async def _scrape_url_with_jina(url: str, client: httpx.AsyncClient) -> str | None:
    """Fetch a URL via the Jina AI Reader and return plain-text markdown.

    Returns ``None`` on failure so callers can fall back to search snippets.
    """
    headers: dict[str, str] = {"Accept": "text/plain"}
    if settings.jina_api_key:
        headers["Authorization"] = f"Bearer {settings.jina_api_key}"
    try:
        resp = await client.get(
            f"{_JINA_READER_URL}{url}",
            headers=headers,
            timeout=15.0,
            follow_redirects=True,
        )
        resp.raise_for_status()
        return resp.text[:6000]  # cap at 6 k chars to keep token budget sane
    except Exception as exc:
        logger.warning("Jina scrape failed for %s (%s).", url, exc)
        return None


async def competitive_intel_node(state: MASSState) -> dict[str, Any]:
    """Owner-facing competitive intelligence node.

    Pipeline:
    1. Run a price-focused web search (Brave → Serper → stub).
    2. Scrape the top 3 competitor pages via Jina AI Reader.
    3. Send scraped markdown + owner query to the LLM for a structured diff.
    4. Return a structured competitive analysis result.

    Falls back gracefully at every step — the graph always reaches
    ``synthesize_node`` even without API keys.
    """
    query = state["query"]
    max_search = 3  # Only need a handful of competitor pages
    logger.info("Competitive intel triggered for query: %r", query)

    # ── 1. Collect competitor search results ──────────────────────────────────
    search_results: list[dict[str, Any]] = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        price_query = f"{query} price buy"

        if settings.brave_api_key:
            try:
                resp = await client.get(
                    _BRAVE_SEARCH_URL,
                    headers={
                        "Accept": "application/json",
                        "Accept-Encoding": "gzip",
                        "X-Subscription-Token": settings.brave_api_key,
                    },
                    params={"q": price_query, "count": max_search},
                )
                resp.raise_for_status()
                for item in resp.json().get("web", {}).get("results", []):
                    search_results.append({
                        "url": item.get("url", ""),
                        "snippet": item.get("description") or item.get("title", ""),
                    })
            except Exception as exc:
                logger.warning("Brave search failed for competitive intel (%s).", exc)

        if not search_results and settings.serper_api_key:
            try:
                resp = await client.post(
                    _SERPER_SEARCH_URL,
                    headers={"X-API-KEY": settings.serper_api_key, "Content-Type": "application/json"},
                    json={"q": price_query, "num": max_search},
                )
                resp.raise_for_status()
                for item in resp.json().get("organic", []):
                    search_results.append({
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                    })
            except Exception as exc:
                logger.warning("Serper search failed for competitive intel (%s).", exc)

        # ── 2. Scrape top pages with Jina ─────────────────────────────────────
        scraped_pages: list[str] = []
        for hit in search_results[:max_search]:
            url = hit.get("url", "")
            if not url:
                continue
            page_text = await _scrape_url_with_jina(url, client)
            if page_text:
                scraped_pages.append(f"### Source: {url}\n\n{page_text}")
            else:
                # Fall back to the search snippet
                scraped_pages.append(f"### Source: {url}\n\n{hit.get('snippet', '')}")

    # ── Stub when no data is available ───────────────────────────────────────
    if not scraped_pages:
        logger.info("Competitive intel stub — no web data available for: %r", query)
        return {
            "results": [
                {
                    "content": (
                        f"[COMPETITIVE INTEL STUB] Analysis for: {query!r}. "
                        "Set BRAVE_API_KEY or SERPER_API_KEY to enable real-time "
                        "competitor discovery. JINA_API_KEY improves full-page scraping."
                    ),
                    "source": "competitive-stub",
                    "score": 1.0,
                    "metadata": {"intent": "competitive", "mode": "stub"},
                }
            ],
            "agent_trace": ["competitive_intel"],
        }

    # ── 3. LLM competitive analysis ───────────────────────────────────────────
    competitor_context = "\n\n---\n\n".join(scraped_pages)
    messages = [
        {"role": "system", "content": _COMPETITIVE_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Owner question: {query}\n\n"
                f"Competitor content:\n\n{competitor_context}"
            ),
        },
    ]

    try:
        response = await litellm.acompletion(
            model=state.get("model") or settings.litellm_model,
            messages=messages,
            max_tokens=600,
        )
        analysis: str = response.choices[0].message.content or ""
    except Exception as exc:
        logger.warning("LiteLLM competitive analysis failed (%s).", exc)
        analysis = (
            f"[COMPETITIVE INTEL] Scraped {len(scraped_pages)} competitor page(s) "
            f"for '{query}'. LLM analysis unavailable — set a valid API key."
        )

    return {
        "results": [
            {
                "content": analysis,
                "source": "competitive-intel",
                "score": 1.0,
                "metadata": {
                    "intent": "competitive",
                    "sources_scraped": len(scraped_pages),
                    "competitor_urls": [h.get("url", "") for h in search_results[:max_search]],
                },
            }
        ],
        "agent_trace": ["competitive_intel"],
    }


# ---------------------------------------------------------------------------
# Action Agent (Move 5)
# ---------------------------------------------------------------------------

#: Tool registry — add entries here to extend the action agent's capabilities
#: without modifying node logic.
_ACTION_TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "create_booking",
            "description": "Create a booking or reservation for a service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "The service to book (e.g. surf lesson, consultation)",
                    },
                    "date": {
                        "type": "string",
                        "description": "Requested date/time — natural language is fine",
                    },
                    "notes": {
                        "type": "string",
                        "description": "Any additional notes or requirements",
                    },
                },
                "required": ["service", "date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email or message to a recipient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address or name"},
                    "subject": {"type": "string", "description": "Email subject line"},
                    "body": {"type": "string", "description": "Email body content"},
                },
                "required": ["to", "subject", "body"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_record",
            "description": "Update an existing record in the system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "record_type": {
                        "type": "string",
                        "description": "Type of record (e.g. order, customer, product)",
                    },
                    "record_id": {
                        "type": "string",
                        "description": "Identifier of the record to update",
                    },
                    "fields": {
                        "type": "object",
                        "description": "Key-value pairs of fields to update",
                        "additionalProperties": True,
                    },
                },
                "required": ["record_type", "record_id", "fields"],
            },
        },
    },
]

_ACTION_SYSTEM_PROMPT = """\
You are MASS Action Agent — an AI that identifies and structures actions to perform.

Given the user's request, call the most appropriate tool to capture action details.
If no tool matches, do NOT call any tool; instead reply with a plain-text explanation."""


async def action_agent_node(state: MASSState) -> dict[str, Any]:
    """Tool-calling action agent powered by LiteLLM function calling.

    Uses the LLM's native tool-use capability to identify the appropriate
    action and extract structured parameters from natural language.

    Tool registry (``_ACTION_TOOLS``)::

        create_booking  – book or schedule a service
        send_email      – compose and send an email
        update_record   – mutate an existing record

    Add entries to ``_ACTION_TOOLS`` to register new capabilities without
    modifying this node.

    **Graceful fallback**: if the LLM call fails or the model does not support
    function calling, returns a descriptive stub result so the graph always
    reaches ``synthesize_node``.
    """
    import json as _json

    query = state["query"]
    logger.info("Action agent triggered for query: %r", query)

    try:
        response = await litellm.acompletion(
            model=state.get("model") or settings.litellm_model,
            messages=[
                {"role": "system", "content": _ACTION_SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            tools=_ACTION_TOOLS,
            tool_choice="auto",
        )
        msg = response.choices[0].message
        tool_calls = getattr(msg, "tool_calls", None) or []

        if tool_calls:
            call = tool_calls[0]
            fn_name: str = call.function.name
            try:
                fn_args: dict[str, Any] = _json.loads(call.function.arguments)
            except Exception:
                fn_args = {}

            content = (
                f"Action identified: **{fn_name}**\n\n"
                f"Parameters:\n{_json.dumps(fn_args, indent=2)}\n\n"
                "(MASS Action Agent has structured the request. "
                "Wire execution adapters to `_ACTION_TOOLS` to perform real operations.)"
            )
            logger.info("Action agent resolved tool=%r args=%r", fn_name, fn_args)
            return {
                "results": [
                    {
                        "content": content,
                        "source": "action-agent",
                        "score": 1.0,
                        "metadata": {
                            "intent": "action",
                            "tool_name": fn_name,
                            "tool_args": fn_args,
                        },
                    }
                ],
                "agent_trace": ["action_agent"],
            }

        # Model replied in plain text (no tool selected)
        fallback_content = (msg.content or "").strip() or (
            f"[ACTION AGENT] No matching action tool for: {query!r}. "
            "Register additional tools in `_ACTION_TOOLS` to expand capabilities."
        )
        return {
            "results": [
                {
                    "content": fallback_content,
                    "source": "action-agent",
                    "score": 0.5,
                    "metadata": {"intent": "action", "tool_name": None},
                }
            ],
            "agent_trace": ["action_agent"],
        }

    except Exception as exc:
        logger.warning("Action agent LiteLLM call failed (%s); using stub.", exc)
        return {
            "results": [
                {
                    "content": (
                        f"[ACTION AGENT] Could not process: {query!r}. "
                        "Ensure a valid LLM API key is configured."
                    ),
                    "source": "action-agent",
                    "score": 0.0,
                    "metadata": {"intent": "action", "error": str(exc)},
                }
            ],
            "agent_trace": ["action_agent"],
        }


async def retrieve_node(state: MASSState) -> dict[str, Any]:
    """Retrieve relevant evidence for the query via Supabase pgvector.

    When ``SUPABASE_URL`` and ``SUPABASE_SERVICE_KEY`` are configured this
    node:

    1. Embeds the query with ``litellm.aembedding`` (``embedding_model``).
    2. Calls the ``match_documents`` RPC on Supabase via its REST API.
    3. Maps each row to the ``SearchResult`` shape for ``synthesize_node``.

    Falls back to a single stub result when Supabase credentials are absent
    (safe for CI / local dev without credentials).
    """
    query = state["query"]
    max_results = state.get("max_results", 10)

    # ── Supabase credentials check ───────────────────────────────────────────
    if not settings.supabase_url or not settings.supabase_service_key:
        logger.debug("Supabase not configured — returning stub result.")
        return {
            "results": [
                {
                    "content": f"[STUB] Top result for: {query!r}",
                    "source": "mass-stub",
                    "score": 0.9,
                    "metadata": {"node": "retrieve", "mode": "stub"},
                }
            ],
            "agent_trace": ["retrieve"],
        }

    # ── 1. Embed the query ───────────────────────────────────────────────────
    try:
        embed_response = await litellm.aembedding(
            model=settings.embedding_model,
            input=[query],
        )
        query_vector: list[float] = embed_response.data[0]["embedding"]
    except Exception as exc:
        logger.warning("Embedding failed (%s); returning stub.", exc)
        return {
            "results": [
                {
                    "content": f"[STUB] Embedding unavailable for: {query!r}",
                    "source": "mass-stub",
                    "score": 0.0,
                    "metadata": {"node": "retrieve", "error": str(exc)},
                }
            ],
            "agent_trace": ["retrieve"],
        }

    # ── 2. Call match_documents RPC ──────────────────────────────────────────
    headers = {
        "apikey": settings.supabase_service_key,
        "Authorization": f"Bearer {settings.supabase_service_key}",
        "Content-Type": "application/json",
    }
    rpc_url = f"{settings.supabase_url.rstrip('/')}/rest/v1/rpc/match_documents"
    payload = {
        "query_embedding": query_vector,
        "match_count": max_results,
        "filter": {},
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(rpc_url, json=payload, headers=headers)
            resp.raise_for_status()
            rows: list[dict[str, Any]] = resp.json()
    except Exception as exc:
        logger.warning("Supabase RPC failed (%s); returning stub.", exc)
        return {
            "results": [
                {
                    "content": f"[STUB] Vector search unavailable for: {query!r}",
                    "source": "mass-stub",
                    "score": 0.0,
                    "metadata": {"node": "retrieve", "error": str(exc)},
                }
            ],
            "agent_trace": ["retrieve"],
        }

    # ── 3. Map rows → SearchResult shape ────────────────────────────────────
    results: list[dict[str, Any]] = [
        {
            "content": row.get("content", ""),
            "source": row.get("source", "supabase"),
            "score": float(row.get("score", 0.0)),
            "metadata": {
                **(row.get("metadata") or {}),
                "source_id": row.get("source_id"),
                "id": str(row.get("id", "")),
            },
        }
        for row in rows
        if row.get("content")
    ]

    if not results:
        logger.info("match_documents returned 0 rows for query: %r", query)

    return {
        "results": results,
        "agent_trace": ["retrieve"],
    }


async def synthesize_node(state: MASSState) -> dict[str, Any]:
    """Synthesise retrieved evidence into a coherent answer via LiteLLM.

    Calls ``litellm.acompletion`` so any model supported by LiteLLM
    (OpenAI, Anthropic, Gemini, Ollama, …) can be swapped in by changing
    ``settings.litellm_model`` — no code changes required.

    Langfuse tracing is activated automatically when
    ``LANGFUSE_PUBLIC_KEY`` and ``LANGFUSE_SECRET_KEY`` are set.

    **Graceful fallback**: if the LiteLLM call fails (e.g. missing API key
    in local/CI environments), the node returns a templated stub string and
    logs the error.  The graph continues to completion so callers always
    receive a valid ``SearchResponse``.
    """
    context_text = "\n\n".join(
        f"[{i + 1}] {r.get('content', '')}" for i, r in enumerate(state["results"])
    )
    messages = [
        {
            "role": "system",
            "content": (
                "You are MASS — a universal intelligence layer for AI systems. "
                "Given retrieved context, synthesise a concise, accurate answer "
                "to the user's query. Cite sources by index number where relevant."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Query: {state['query']}\n\n"
                f"Retrieved context:\n{context_text or '(no context retrieved)'}\n\n"
                "Please synthesise a helpful answer."
            ),
        },
    ]

    try:
        response = await litellm.acompletion(
            model=state.get("model") or settings.litellm_model,
            messages=messages,
            max_tokens=512,
            # Metadata forwarded to Langfuse as trace tags
            metadata={
                "mass_query": state["query"],
                "mass_results_count": len(state["results"]),
            },
        )
        synthesis: str = response.choices[0].message.content or ""
    except Exception as exc:  # noqa: BLE001
        logger.warning("LiteLLM synthesis failed (%s); using fallback.", exc)
        n = len(state["results"])
        synthesis = (
            f"Based on {n} retrieved result(s) for '{state['query']}': "
            "[LLM synthesis unavailable — set a valid API key via "
            "OPENAI_API_KEY / ANTHROPIC_API_KEY / etc.]"
        )

    return {
        "synthesis": synthesis,
        "agent_trace": ["synthesize"],
    }


# ---------------------------------------------------------------------------
# Graph factory
# ---------------------------------------------------------------------------


def build_graph() -> CompiledStateGraph:
    """Construct and compile the MASS ``StateGraph``.

    Graph topology::

        receive_query
              │
        classify_intent
              │
        ┌─────┴──────────────┬─────────────┬──────────────────┐
        ▼                    ▼             ▼                  ▼
      retrieve          action_agent   web_search   competitive_intel
        │                    │             │                  │
        └───────────┬─────────┘             └──────┬──────────┘
                    ▼                              ▼
               synthesize  ◄──────────────────────┘
                    │
                   END

    Conditional edges from ``classify_intent`` use ``_route_intent`` to
    map intent → node name.
    """
    builder: StateGraph = StateGraph(MASSState)

    # ── Register nodes ───────────────────────────────────────────────────────
    builder.add_node("receive_query", receive_query_node)
    builder.add_node("classify_intent", classify_intent_node)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("action_agent", action_agent_node)
    builder.add_node("web_search", web_search_node)
    builder.add_node("competitive_intel", competitive_intel_node)
    builder.add_node("synthesize", synthesize_node)

    # ── Wire edges ───────────────────────────────────────────────────────────
    builder.set_entry_point("receive_query")
    builder.add_edge("receive_query", "classify_intent")

    # Conditional routing based on classified intent
    builder.add_conditional_edges(
        "classify_intent",
        _route_intent,
        {
            "retrieve": "retrieve",
            "action_agent": "action_agent",
            "web_search": "web_search",
            "competitive_intel": "competitive_intel",
        },
    )

    # All specialist nodes converge on synthesize
    builder.add_edge("retrieve", "synthesize")
    builder.add_edge("action_agent", "synthesize")
    builder.add_edge("web_search", "synthesize")
    builder.add_edge("competitive_intel", "synthesize")
    builder.add_edge("synthesize", END)

    return builder.compile()


# ---------------------------------------------------------------------------
# Module-level singleton (import-time compile)
# ---------------------------------------------------------------------------

#: Pre-compiled MASS graph — import and ``await mass_graph.ainvoke(state)``
mass_graph: CompiledStateGraph = build_graph()

