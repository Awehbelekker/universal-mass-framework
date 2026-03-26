"""MASS MCP Server — exposes the MASS search graph as an MCP tool.

Run via stdio (Claude Desktop / any MCP client):
    uv run python -m mass.mcp_server

Or register in .mcp.json so Claude Desktop discovers it automatically.

The server exposes one tool: ``mass_search``.

Any MCP-compatible client (Claude Desktop, Cursor, Copilot extensions, …)
can call this tool and receive fully-synthesised intelligence from the
MASS LangGraph pipeline.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from mass.graph import MASSState, mass_graph

# ---------------------------------------------------------------------------
# FastMCP server instance
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "MASS — Universal Multi-Agent System Search",
    instructions=(
        "Call mass_search with a natural-language query to retrieve "
        "synthesised intelligence from the MASS framework. "
        "The response includes retrieved evidence and an LLM-generated synthesis."
    ),
)


# ---------------------------------------------------------------------------
# Tool: mass_search
# ---------------------------------------------------------------------------


@mcp.tool()
async def mass_search(
    query: str,
    max_results: int = 10,
    context: str = "",
) -> str:
    """Search the MASS knowledge graph and return a synthesised answer.

    Args:
        query:       The natural-language question or search query.
        max_results: Maximum number of evidence items to retrieve (default 10).
        context:     Optional JSON string with caller context
                     (e.g. '{"user_id": "u_123", "session_id": "s_456"}').

    Returns:
        A JSON string containing:
        - ``query``:       The cleaned query that was processed.
        - ``synthesis``:   LLM-synthesised answer.
        - ``results``:     List of retrieved evidence items.
        - ``agent_trace``: Ordered list of graph nodes that were executed.
        - ``model``:       The LLM model used for synthesis.
    """
    # Parse optional context JSON
    parsed_context: dict[str, Any] | None = None
    if context:
        try:
            parsed_context = json.loads(context)
        except json.JSONDecodeError:
            parsed_context = {"raw": context}

    initial_state: MASSState = {
        "query": query,
        "context": parsed_context,
        "max_results": max_results,
        "results": [],
        "synthesis": None,
        "intent": None,
        "model": None,
        "agent_trace": [],
    }

    final_state: MASSState = await mass_graph.ainvoke(initial_state)

    payload = {
        "query": final_state["query"],
        "synthesis": final_state.get("synthesis"),
        "results": final_state.get("results", []),
        "agent_trace": final_state.get("agent_trace", []),
        "model": final_state.get("model"),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Entry point — stdio transport (MCP default for local clients)
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the MASS MCP server over stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

