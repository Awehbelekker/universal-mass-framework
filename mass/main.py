"""MASS FastAPI application entry point.

Exposes:
  GET  /health  — liveness probe (used by Cloud Run + load balancers)
  POST /search  — primary intelligence endpoint

The /search handler now delegates to the LangGraph ``StateGraph`` defined
in ``mass.graph`` (Step 2).  The graph nodes are live; the retrieve and
synthesize nodes are still stubbed until Steps 3–4 wire in RAGFlow and
LiteLLM respectively.
"""

from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException, status

from mass import __version__
from mass.config import settings
from mass.graph import MASSState, mass_graph
from mass.models import SearchRequest, SearchResponse, SearchResult

app = FastAPI(
    title="MASS — Universal Multi-Agent System Search Framework",
    description="The jQuery of AI — plug-and-play intelligence for any system.",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ---------------------------------------------------------------------------
# Liveness / readiness probe
# ---------------------------------------------------------------------------


@app.get("/health", tags=["ops"])
async def health() -> dict:
    """Cloud Run liveness probe. Returns 200 when the service is ready."""
    return {
        "status": "ok",
        "version": __version__,
        "env": settings.mass_env,
    }


# ---------------------------------------------------------------------------
# Primary search endpoint
# ---------------------------------------------------------------------------


def _verify_api_key(x_api_key: str | None) -> None:
    """Raise 401 when an API key is configured and the caller omits or
    supplies an incorrect value. A blank ``settings.mass_api_key`` disables
    auth entirely (useful for local development)."""
    if settings.mass_api_key and x_api_key != settings.mass_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid X-Api-Key header.",
        )


@app.post("/search", response_model=SearchResponse, tags=["mass"])
async def search(
    request: SearchRequest,
    x_api_key: str | None = Header(default=None),
) -> SearchResponse:
    """Universal intelligence search endpoint.

    Delegates to the MASS ``StateGraph`` (``mass.graph.mass_graph``).

    The graph topology is:
        ``receive_query → retrieve → synthesize → END``

    **Step 2** — The graph is live.  The ``retrieve`` and ``synthesize``
    nodes are still stubbed; they will be replaced by RAGFlow and LiteLLM
    in Steps 3–4.
    """
    _verify_api_key(x_api_key)

    # Build the initial state from the incoming request
    initial_state: MASSState = {
        "query": request.query,
        "context": request.context,
        "max_results": request.max_results,
        # The graph nodes populate these fields; provide empty defaults so
        # the TypedDict is fully initialised before the first node runs.
        "results": [],
        "synthesis": None,
        "intent": None,
        "model": None,
        "agent_trace": [],
    }

    # Run the graph — all three nodes execute synchronously inside LangGraph's
    # async wrapper; Step 3 will add true async LLM calls inside synthesize_node.
    final_state: MASSState = await mass_graph.ainvoke(initial_state)

    # Map raw state dicts to typed Pydantic models for the API response
    results = [
        SearchResult(
            content=r.get("content", ""),
            source=r.get("source"),
            score=r.get("score"),
            metadata=r.get("metadata", {}),
        )
        for r in final_state.get("results", [])
    ]

    return SearchResponse(
        query=final_state["query"],
        results=results,
        synthesis=final_state.get("synthesis"),
        intent=final_state.get("intent"),
        agent_trace=final_state.get("agent_trace", []),
        model=final_state.get("model"),
    )

