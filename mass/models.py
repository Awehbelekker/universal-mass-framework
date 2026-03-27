"""Pydantic request/response models for the MASS API.

These are the stable public contract that all consumers (DIGG, paperclip
adapters, thinkmesh_core bridges) will program against. Shape changes
here are breaking changes — version carefully.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class SearchRequest(BaseModel):
    """Inbound search query from any MASS consumer."""

    query: str = Field(..., description="Natural-language search query")
    context: dict[str, Any] | None = Field(
        default=None,
        description="Optional caller-supplied context (user_id, session_id, filters, …)",
    )
    max_results: int = Field(default=10, ge=1, le=100)


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------


class SearchResult(BaseModel):
    """A single retrieved piece of evidence."""

    content: str
    source: str | None = None
    score: float | None = Field(default=None, ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    """Full MASS response returned to the caller."""

    query: str
    results: list[SearchResult]
    synthesis: str | None = Field(
        default=None,
        description="LLM-synthesised answer drawn from results",
    )
    intent: str | None = Field(
        default=None,
        description=(
            "Classified intent of the query "
            "(search | product | order | action | web | competitive)"
        ),
    )
    agent_trace: list[str] = Field(
        default_factory=list,
        description="Ordered list of agent node names traversed (for observability)",
    )
    model: str | None = Field(
        default=None,
        description="LLM model used for synthesis",
    )

