"""MASS LangGraph orchestration pipeline.

Implements the MASS search pipeline as a LangGraph ``StateGraph``, following
the same architectural pattern as the ``deepagents`` framework (nodes → edges
→ compile → invoke).  The graph is a stateful reasoning pipeline that
processes a search query through three sequential nodes:

    receive_query → classify_intent → retrieve → synthesize → END
                                   ↘ action_stub ↗
                                   ↘ web_stub   ↗

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
    """
    cleaned_query = state["query"].strip()
    return {
        "query": cleaned_query,
        "results": [],
        "synthesis": None,
        "intent": None,
        "model": settings.litellm_model,
        "agent_trace": ["receive_query"],
    }


# ---------------------------------------------------------------------------
# Intent classifier (Move 2)
# ---------------------------------------------------------------------------

_INTENT_SYSTEM_PROMPT = """\
You are an intent classifier for MASS, a universal AI intelligence layer.

Classify the user query into EXACTLY ONE of these intents:

  search   – general knowledge, how-to, information lookup, definitions
  product  – product details, availability, pricing, sizing, specifications
  order    – order status, tracking, returns, delivery, invoices
  action   – create, update, delete, book, schedule, submit (requires an action)
  web      – needs live/real-time data only available on the internet

Reply with a single lowercase word — nothing else."""

_VALID_INTENTS = {"search", "product", "order", "action", "web"}


async def classify_intent_node(state: MASSState) -> dict[str, Any]:
    """Classify the query intent using a fast LiteLLM call.

    Uses a cheap, fast model (gpt-4o-mini by default) to keep latency low.
    Falls back to ``search`` if the LLM is unavailable or returns an
    unrecognised label — ensuring the graph always continues.
    """
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
        return "action_stub"
    # web (and any unknown fallback)
    return "web_stub"


# ---------------------------------------------------------------------------
# Specialist stub nodes (Move 2 — full implementations come later)
# ---------------------------------------------------------------------------


async def action_stub_node(state: MASSState) -> dict[str, Any]:
    """Placeholder for the Action Agent.

    Will be replaced with a real tool-calling agent that can create/update/
    delete records, trigger workflows, send emails, etc.
    """
    logger.info("Action agent triggered for query: %r", state["query"])
    return {
        "results": [
            {
                "content": (
                    f"[ACTION AGENT] Received action request: {state['query']!r}. "
                    "Full action execution coming in Move 4."
                ),
                "source": "action-stub",
                "score": 1.0,
                "metadata": {"intent": "action", "mode": "stub"},
            }
        ],
        "agent_trace": ["action_stub"],
    }


async def web_stub_node(state: MASSState) -> dict[str, Any]:
    """Placeholder for the Web Search Agent.

    Will be replaced with a real web retrieval agent (Brave/Serper API)
    for queries that need live internet data.
    """
    logger.info("Web agent triggered for query: %r", state["query"])
    return {
        "results": [
            {
                "content": (
                    f"[WEB AGENT] Live web search for: {state['query']!r}. "
                    "Real-time web retrieval coming in a future move."
                ),
                "source": "web-stub",
                "score": 1.0,
                "metadata": {"intent": "web", "mode": "stub"},
            }
        ],
        "agent_trace": ["web_stub"],
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

    Graph topology (Move 2)::

        receive_query
              │
        classify_intent
              │
        ┌─────┴──────────┬──────────┐
        ▼                ▼          ▼
      retrieve      action_stub  web_stub
        │                │          │
        └────────┬────────┘          │
                 ▼                   │
            synthesize  ◄────────────┘
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
    builder.add_node("action_stub", action_stub_node)
    builder.add_node("web_stub", web_stub_node)
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
            "action_stub": "action_stub",
            "web_stub": "web_stub",
        },
    )

    # All specialist nodes converge on synthesize
    builder.add_edge("retrieve", "synthesize")
    builder.add_edge("action_stub", "synthesize")
    builder.add_edge("web_stub", "synthesize")
    builder.add_edge("synthesize", END)

    return builder.compile()


# ---------------------------------------------------------------------------
# Module-level singleton (import-time compile)
# ---------------------------------------------------------------------------

#: Pre-compiled MASS graph — import and ``await mass_graph.ainvoke(state)``
mass_graph: CompiledStateGraph = build_graph()

