"""Tests for the MASS FastAPI application (Move 2 — Intent Classifier + Routing).

The /search endpoint delegates to the MASS LangGraph StateGraph:
    receive_query → classify_intent → retrieve|action_stub|web_stub → synthesize

LiteLLM calls are mocked so the test suite runs without API keys.

Run with:  uv run pytest tests/ -v
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from mass.main import app


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


# ---------------------------------------------------------------------------
# Health probe
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_health_returns_200(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_payload(client: AsyncClient):
    data = (await client.get("/health")).json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "env" in data


# ---------------------------------------------------------------------------
# Search endpoint — stub behaviour
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_search_returns_200(client: AsyncClient):
    response = await client.post("/search", json={"query": "hello world"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_search_echoes_query(client: AsyncClient):
    response = await client.post("/search", json={"query": "test query"})
    data = response.json()
    assert data["query"] == "test query"


@pytest.mark.asyncio
async def test_search_returns_results(client: AsyncClient):
    response = await client.post("/search", json={"query": "any query"})
    data = response.json()
    assert isinstance(data["results"], list)
    assert len(data["results"]) >= 1


@pytest.mark.asyncio
async def test_search_includes_agent_trace(client: AsyncClient):
    response = await client.post("/search", json={"query": "trace test"})
    data = response.json()
    assert isinstance(data["agent_trace"], list)
    assert len(data["agent_trace"]) > 0


@pytest.mark.asyncio
async def test_search_max_results_validated(client: AsyncClient):
    # max_results must be >= 1
    response = await client.post("/search", json={"query": "q", "max_results": 0})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# API key authentication
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_search_no_auth_when_key_not_configured(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    """With an empty MASS_API_KEY, all requests should pass."""
    monkeypatch.setattr("mass.main.settings.mass_api_key", "")
    response = await client.post("/search", json={"query": "open access"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_search_rejects_missing_key(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr("mass.main.settings.mass_api_key", "super-secret")
    response = await client.post("/search", json={"query": "locked"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_search_accepts_correct_key(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr("mass.main.settings.mass_api_key", "super-secret")
    response = await client.post(
        "/search",
        json={"query": "authenticated"},
        headers={"X-Api-Key": "super-secret"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_search_rejects_wrong_key(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr("mass.main.settings.mass_api_key", "super-secret")
    response = await client.post(
        "/search",
        json={"query": "bad actor"},
        headers={"X-Api-Key": "wrong-key"},
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Step 2: LangGraph StateGraph — graph behaviour assertions
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_search_agent_trace_contains_all_nodes(client: AsyncClient):
    """Graph must traverse receive_query → classify_intent → retrieve → synthesize in order."""
    response = await client.post("/search", json={"query": "trace verification"})
    data = response.json()
    trace = data["agent_trace"]
    assert "receive_query" in trace
    assert "classify_intent" in trace
    assert "retrieve" in trace
    assert "synthesize" in trace
    # Order matters: each node must appear before the next
    assert trace.index("receive_query") < trace.index("classify_intent")
    assert trace.index("classify_intent") < trace.index("retrieve")
    assert trace.index("retrieve") < trace.index("synthesize")


@pytest.mark.asyncio
async def test_search_result_has_required_fields(client: AsyncClient):
    """Each result item must expose content and source."""
    response = await client.post("/search", json={"query": "field check"})
    data = response.json()
    assert len(data["results"]) >= 1
    first = data["results"][0]
    assert "content" in first
    assert "source" in first
    assert isinstance(first["content"], str)
    assert len(first["content"]) > 0


@pytest.mark.asyncio
async def test_search_synthesis_is_string(client: AsyncClient):
    """The synthesis field must be a non-empty string (graph synthesize node ran)."""
    response = await client.post("/search", json={"query": "synthesis check"})
    data = response.json()
    assert isinstance(data["synthesis"], str)
    assert len(data["synthesis"]) > 0


@pytest.mark.asyncio
async def test_search_query_is_cleaned(client: AsyncClient):
    """receive_query node must strip leading/trailing whitespace from the query."""
    response = await client.post("/search", json={"query": "  padded query  "})
    data = response.json()
    assert data["query"] == "padded query"


@pytest.mark.asyncio
async def test_search_with_context(client: AsyncClient):
    """Optional context payload must be accepted without error."""
    response = await client.post(
        "/search",
        json={
            "query": "context test",
            "context": {"user_id": "u_123", "session_id": "s_456"},
            "max_results": 5,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "context test"


@pytest.mark.asyncio
async def test_graph_builds_without_error():
    """build_graph() must compile without raising at import/call time."""
    from mass.graph import build_graph

    g = build_graph()
    assert g is not None


# ---------------------------------------------------------------------------
# Step 3: LiteLLM synthesis — mock the acompletion call
# ---------------------------------------------------------------------------

def _make_litellm_response(content: str) -> MagicMock:
    """Build a minimal mock that mirrors litellm.ModelResponse structure."""
    msg = MagicMock()
    msg.content = content
    choice = MagicMock()
    choice.message = msg
    response = MagicMock()
    response.choices = [choice]
    return response


@pytest.mark.asyncio
async def test_synthesis_uses_litellm(client: AsyncClient):
    """synthesize_node must call litellm.acompletion and return its output."""
    mock_response = _make_litellm_response("MASS synthesised answer.")
    with patch("mass.graph.litellm.acompletion", new=AsyncMock(return_value=mock_response)):
        response = await client.post("/search", json={"query": "litellm test"})
    assert response.status_code == 200
    data = response.json()
    assert data["synthesis"] == "MASS synthesised answer."


@pytest.mark.asyncio
async def test_synthesis_fallback_on_llm_error(client: AsyncClient):
    """When litellm raises, the graph must fall back gracefully (no 500)."""
    with patch("mass.graph.litellm.acompletion", new=AsyncMock(side_effect=Exception("no key"))):
        response = await client.post("/search", json={"query": "fallback test"})
    assert response.status_code == 200
    data = response.json()
    # Fallback string should mention unavailability
    assert "unavailable" in data["synthesis"].lower() or len(data["synthesis"]) > 0


@pytest.mark.asyncio
async def test_synthesis_content_contains_query(client: AsyncClient):
    """The mocked LLM answer is returned verbatim in the synthesis field."""
    mock_response = _make_litellm_response("Answer about: special query XYZ")
    with patch("mass.graph.litellm.acompletion", new=AsyncMock(return_value=mock_response)):
        response = await client.post("/search", json={"query": "special query XYZ"})
    data = response.json()
    assert "special query XYZ" in data["synthesis"]


# ---------------------------------------------------------------------------
# Step 3: MCP server — smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_mcp_server_tool_returns_json():
    """mass_search MCP tool must return valid JSON with expected keys."""
    import json

    from mass.mcp_server import mass_search

    mock_response = _make_litellm_response("MCP synthesis result.")
    with patch("mass.graph.litellm.acompletion", new=AsyncMock(return_value=mock_response)):
        result = await mass_search(query="mcp test query", max_results=3)

    parsed = json.loads(result)
    assert parsed["query"] == "mcp test query"
    assert parsed["synthesis"] == "MCP synthesis result."
    assert isinstance(parsed["results"], list)
    assert isinstance(parsed["agent_trace"], list)
    assert "receive_query" in parsed["agent_trace"]


@pytest.mark.asyncio
async def test_mcp_server_tool_accepts_context_json():
    """mass_search must parse a JSON context string without error."""
    import json

    from mass.mcp_server import mass_search

    mock_response = _make_litellm_response("Context-aware answer.")
    with patch("mass.graph.litellm.acompletion", new=AsyncMock(return_value=mock_response)):
        result = await mass_search(
            query="context test",
            context='{"user_id": "u_42"}',
        )

    parsed = json.loads(result)
    assert parsed["query"] == "context test"


@pytest.mark.asyncio
async def test_mcp_server_instance_exists():
    """The FastMCP instance must be importable and have the correct name."""
    from mass.mcp_server import mcp

    assert mcp is not None
    assert "MASS" in mcp.name


# ---------------------------------------------------------------------------
# Move 2: Intent Classifier + Conditional Routing
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_intent_classifier_in_trace(client: AsyncClient):
    """classify_intent must appear in the agent_trace after receive_query."""
    response = await client.post("/search", json={"query": "what surfboards do you sell?"})
    data = response.json()
    trace = data["agent_trace"]
    assert "classify_intent" in trace
    assert trace.index("receive_query") < trace.index("classify_intent")


@pytest.mark.asyncio
async def test_intent_field_in_response(client: AsyncClient):
    """Response must expose the intent field (set by classify_intent_node)."""
    response = await client.post("/search", json={"query": "what is MASS?"})
    data = response.json()
    assert "intent" in data
    assert data["intent"] in ("search", "product", "order", "action", "web", None)


@pytest.mark.asyncio
async def test_intent_routes_search_to_retrieve(client: AsyncClient):
    """When classify_intent returns 'search', the retrieve node must run."""
    classify_resp = _make_litellm_response("search")
    synth_resp = _make_litellm_response("Here is what I found.")
    with patch(
        "mass.graph.litellm.acompletion",
        new=AsyncMock(side_effect=[classify_resp, synth_resp]),
    ):
        response = await client.post("/search", json={"query": "what is machine learning?"})
    data = response.json()
    assert response.status_code == 200
    assert "retrieve" in data["agent_trace"]
    assert "action_stub" not in data["agent_trace"]
    assert "web_stub" not in data["agent_trace"]
    assert data["intent"] == "search"


@pytest.mark.asyncio
async def test_intent_routes_product_to_retrieve(client: AsyncClient):
    """Product intent must also route to retrieve (same path as search)."""
    classify_resp = _make_litellm_response("product")
    synth_resp = _make_litellm_response("Here are our products.")
    with patch(
        "mass.graph.litellm.acompletion",
        new=AsyncMock(side_effect=[classify_resp, synth_resp]),
    ):
        response = await client.post("/search", json={"query": "show me surfboards under R5000"})
    data = response.json()
    assert response.status_code == 200
    assert "retrieve" in data["agent_trace"]
    assert "action_stub" not in data["agent_trace"]
    assert data["intent"] == "product"


@pytest.mark.asyncio
async def test_intent_routes_action_to_action_stub(client: AsyncClient):
    """When classify_intent returns 'action', action_stub must run instead of retrieve."""
    classify_resp = _make_litellm_response("action")
    synth_resp = _make_litellm_response("Action acknowledged.")
    with patch(
        "mass.graph.litellm.acompletion",
        new=AsyncMock(side_effect=[classify_resp, synth_resp]),
    ):
        response = await client.post("/search", json={"query": "book a surf lesson for tomorrow"})
    data = response.json()
    assert response.status_code == 200
    assert "action_stub" in data["agent_trace"]
    assert "retrieve" not in data["agent_trace"]
    assert "web_stub" not in data["agent_trace"]
    assert data["intent"] == "action"


@pytest.mark.asyncio
async def test_intent_routes_web_to_web_stub(client: AsyncClient):
    """When classify_intent returns 'web', web_stub must run instead of retrieve."""
    classify_resp = _make_litellm_response("web")
    synth_resp = _make_litellm_response("Live web result.")
    with patch(
        "mass.graph.litellm.acompletion",
        new=AsyncMock(side_effect=[classify_resp, synth_resp]),
    ):
        response = await client.post("/search", json={"query": "what is today's surf forecast?"})
    data = response.json()
    assert response.status_code == 200
    assert "web_stub" in data["agent_trace"]
    assert "retrieve" not in data["agent_trace"]
    assert "action_stub" not in data["agent_trace"]
    assert data["intent"] == "web"


@pytest.mark.asyncio
async def test_intent_defaults_to_search_on_classifier_error(client: AsyncClient):
    """When the classify_intent LLM call fails, the graph must default to 'search' and continue."""
    # First acompletion call (classify) raises; second (synthesize) succeeds
    synth_resp = _make_litellm_response("Fallback search result.")
    with patch(
        "mass.graph.litellm.acompletion",
        new=AsyncMock(side_effect=[Exception("classify failed"), synth_resp]),
    ):
        response = await client.post("/search", json={"query": "anything"})
    data = response.json()
    assert response.status_code == 200
    # Graph must still complete and route to retrieve (the search fallback path)
    assert "retrieve" in data["agent_trace"]
    assert "synthesize" in data["agent_trace"]


@pytest.mark.asyncio
async def test_intent_unknown_label_defaults_to_search(client: AsyncClient):
    """An unrecognised intent label from the LLM must fall back to 'search'."""
    classify_resp = _make_litellm_response("gibberish_label")
    synth_resp = _make_litellm_response("Search result.")
    with patch(
        "mass.graph.litellm.acompletion",
        new=AsyncMock(side_effect=[classify_resp, synth_resp]),
    ):
        response = await client.post("/search", json={"query": "random query"})
    data = response.json()
    assert response.status_code == 200
    assert "retrieve" in data["agent_trace"]
    assert data["intent"] == "search"

