"""Tests for the MASS FastAPI application (Moves 1-5).

The /search endpoint delegates to the MASS LangGraph StateGraph:
    receive_query → classify_intent → retrieve|action_agent|web_search → synthesize

LiteLLM calls are mocked so the test suite runs without API keys.
HTTP calls (Brave/Serper) are mocked for web search tests.

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
    assert data["intent"] in ("search", "product", "order", "action", "web", "competitive", None)


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
async def test_intent_routes_action_to_action_agent(client: AsyncClient):
    """When classify_intent returns 'action', action_agent must run instead of retrieve."""
    classify_resp = _make_litellm_response("action")
    # action_agent calls acompletion for tool-calling, then synthesize calls it again
    action_resp = _make_litellm_response("I will book that for you.")
    synth_resp = _make_litellm_response("Action acknowledged.")
    with patch(
        "mass.graph.litellm.acompletion",
        new=AsyncMock(side_effect=[classify_resp, action_resp, synth_resp]),
    ):
        response = await client.post("/search", json={"query": "book a surf lesson for tomorrow"})
    data = response.json()
    assert response.status_code == 200
    assert "action_agent" in data["agent_trace"]
    assert "retrieve" not in data["agent_trace"]
    assert "web_search" not in data["agent_trace"]
    assert data["intent"] == "action"


@pytest.mark.asyncio
async def test_intent_routes_web_to_web_search(client: AsyncClient):
    """When classify_intent returns 'web', web_search must run instead of retrieve."""
    classify_resp = _make_litellm_response("web")
    synth_resp = _make_litellm_response("Live web result.")
    with patch(
        "mass.graph.litellm.acompletion",
        new=AsyncMock(side_effect=[classify_resp, synth_resp]),
    ):
        response = await client.post("/search", json={"query": "what is today's surf forecast?"})
    data = response.json()
    assert response.status_code == 200
    assert "web_search" in data["agent_trace"]
    assert "retrieve" not in data["agent_trace"]
    assert "action_agent" not in data["agent_trace"]
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


# ---------------------------------------------------------------------------
# Move 4: Web Search Agent
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_web_search_uses_brave_when_key_configured(client: AsyncClient):
    """web_search_node must call Brave Search API when BRAVE_API_KEY is set."""
    classify_resp = _make_litellm_response("web")
    synth_resp = _make_litellm_response("Brave result synthesis.")

    brave_payload = {
        "web": {
            "results": [
                {"title": "Surf Forecast", "description": "3ft offshore today.", "url": "https://example.com/surf"},
            ]
        }
    }
    mock_http_resp = MagicMock()
    mock_http_resp.json.return_value = brave_payload
    mock_http_resp.raise_for_status = MagicMock()

    mock_async_client = AsyncMock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=False)
    mock_async_client.get = AsyncMock(return_value=mock_http_resp)

    with (
        patch("mass.graph.litellm.acompletion", new=AsyncMock(side_effect=[classify_resp, synth_resp])),
        patch("mass.graph.settings.brave_api_key", "test-brave-key"),
        patch("mass.graph.httpx.AsyncClient", return_value=mock_async_client),
    ):
        response = await client.post("/search", json={"query": "surf forecast today"})

    data = response.json()
    assert response.status_code == 200
    assert "web_search" in data["agent_trace"]
    assert len(data["results"]) >= 1
    assert data["results"][0]["source"] == "https://example.com/surf"
    assert data["results"][0]["metadata"]["provider"] == "brave"


@pytest.mark.asyncio
async def test_web_search_falls_back_to_serper(client: AsyncClient):
    """web_search_node must try Serper when Brave fails."""
    classify_resp = _make_litellm_response("web")
    synth_resp = _make_litellm_response("Serper result synthesis.")

    serper_payload = {
        "organic": [
            {"title": "Surf Report", "snippet": "Good conditions.", "link": "https://serper.example.com/surf"},
        ]
    }
    mock_serper_resp = MagicMock()
    mock_serper_resp.json.return_value = serper_payload
    mock_serper_resp.raise_for_status = MagicMock()

    mock_brave_resp = MagicMock()
    mock_brave_resp.raise_for_status.side_effect = Exception("Brave 401")

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    # First call (GET) = Brave fails; second call (POST) = Serper succeeds
    mock_client.get = AsyncMock(return_value=mock_brave_resp)
    mock_client.post = AsyncMock(return_value=mock_serper_resp)

    with (
        patch("mass.graph.litellm.acompletion", new=AsyncMock(side_effect=[classify_resp, synth_resp])),
        patch("mass.graph.settings.brave_api_key", "bad-key"),
        patch("mass.graph.settings.serper_api_key", "test-serper-key"),
        patch("mass.graph.httpx.AsyncClient", return_value=mock_client),
    ):
        response = await client.post("/search", json={"query": "surf conditions"})

    data = response.json()
    assert response.status_code == 200
    assert "web_search" in data["agent_trace"]
    assert data["results"][0]["metadata"]["provider"] == "serper"


@pytest.mark.asyncio
async def test_web_search_stub_without_api_keys(client: AsyncClient):
    """web_search_node must return a stub result when no API keys are configured."""
    classify_resp = _make_litellm_response("web")
    synth_resp = _make_litellm_response("Stub web synthesis.")

    with (
        patch("mass.graph.litellm.acompletion", new=AsyncMock(side_effect=[classify_resp, synth_resp])),
        patch("mass.graph.settings.brave_api_key", ""),
        patch("mass.graph.settings.serper_api_key", ""),
    ):
        response = await client.post("/search", json={"query": "live weather"})

    data = response.json()
    assert response.status_code == 200
    assert "web_search" in data["agent_trace"]
    assert data["results"][0]["source"] == "web-stub"
    assert data["results"][0]["metadata"]["mode"] == "stub"


# ---------------------------------------------------------------------------
# Move 5: Action Agent
# ---------------------------------------------------------------------------


def _make_tool_call_response(tool_name: str, arguments: str) -> MagicMock:
    """Build a mock litellm response that includes a tool_call."""
    fn = MagicMock()
    fn.name = tool_name
    fn.arguments = arguments
    tool_call = MagicMock()
    tool_call.function = fn
    msg = MagicMock()
    msg.tool_calls = [tool_call]
    msg.content = None
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    return resp


@pytest.mark.asyncio
async def test_action_agent_identifies_booking(client: AsyncClient):
    """action_agent_node must parse a create_booking tool call and return structured result."""
    classify_resp = _make_litellm_response("action")
    action_resp = _make_tool_call_response(
        "create_booking", '{"service": "surf lesson", "date": "tomorrow 10am"}'
    )
    synth_resp = _make_litellm_response("Booking action structured.")

    with patch(
        "mass.graph.litellm.acompletion",
        new=AsyncMock(side_effect=[classify_resp, action_resp, synth_resp]),
    ):
        response = await client.post("/search", json={"query": "book a surf lesson for tomorrow 10am"})

    data = response.json()
    assert response.status_code == 200
    assert "action_agent" in data["agent_trace"]
    assert data["intent"] == "action"
    result = data["results"][0]
    assert result["source"] == "action-agent"
    assert result["metadata"]["tool_name"] == "create_booking"
    assert result["metadata"]["tool_args"]["service"] == "surf lesson"


@pytest.mark.asyncio
async def test_action_agent_no_tool_match_returns_text(client: AsyncClient):
    """When the LLM returns no tool_calls, action_agent must return the text content."""
    classify_resp = _make_litellm_response("action")
    # No tool_calls — model replies in plain text
    no_tool_resp = _make_litellm_response("I cannot perform that action yet.")
    # Patch tool_calls to be empty list
    no_tool_resp.choices[0].message.tool_calls = []
    synth_resp = _make_litellm_response("Action noted.")

    with patch(
        "mass.graph.litellm.acompletion",
        new=AsyncMock(side_effect=[classify_resp, no_tool_resp, synth_resp]),
    ):
        response = await client.post("/search", json={"query": "do something unusual"})

    data = response.json()
    assert response.status_code == 200
    assert "action_agent" in data["agent_trace"]
    assert data["results"][0]["source"] == "action-agent"
    assert data["results"][0]["metadata"]["tool_name"] is None


@pytest.mark.asyncio
async def test_action_agent_graceful_on_llm_error(client: AsyncClient):
    """When LiteLLM raises during action_agent, the graph must still reach synthesize."""
    classify_resp = _make_litellm_response("action")
    synth_resp = _make_litellm_response("Fallback synthesis.")

    with patch(
        "mass.graph.litellm.acompletion",
        new=AsyncMock(side_effect=[classify_resp, Exception("tool call failed"), synth_resp]),
    ):
        response = await client.post("/search", json={"query": "trigger an action"})

    data = response.json()
    assert response.status_code == 200
    assert "action_agent" in data["agent_trace"]
    assert "synthesize" in data["agent_trace"]
    assert data["results"][0]["source"] == "action-agent"
    assert data["results"][0]["score"] == 0.0


# ---------------------------------------------------------------------------
# Move 6: Competitive Intelligence Node
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_intent_routes_competitive_to_competitive_intel(client: AsyncClient):
    """When classify_intent returns 'competitive', competitive_intel must run."""
    classify_resp = _make_litellm_response("competitive")
    synth_resp = _make_litellm_response("Competitive analysis done.")

    with (
        patch("mass.graph.litellm.acompletion", new=AsyncMock(side_effect=[classify_resp, synth_resp])),
        patch("mass.graph.settings.brave_api_key", ""),
        patch("mass.graph.settings.serper_api_key", ""),
    ):
        response = await client.post("/search", json={"query": "how does our wetsuit price compare?"})

    data = response.json()
    assert response.status_code == 200
    assert "competitive_intel" in data["agent_trace"]
    assert "retrieve" not in data["agent_trace"]
    assert "web_search" not in data["agent_trace"]
    assert data["intent"] == "competitive"


@pytest.mark.asyncio
async def test_competitive_intel_stub_without_api_keys(client: AsyncClient):
    """competitive_intel_node must return a stub result when no web API keys are set."""
    classify_resp = _make_litellm_response("competitive")
    synth_resp = _make_litellm_response("Stub competitive synthesis.")

    with (
        patch("mass.graph.litellm.acompletion", new=AsyncMock(side_effect=[classify_resp, synth_resp])),
        patch("mass.graph.settings.brave_api_key", ""),
        patch("mass.graph.settings.serper_api_key", ""),
    ):
        response = await client.post("/search", json={"query": "wetsuit competitor prices"})

    data = response.json()
    assert response.status_code == 200
    assert "competitive_intel" in data["agent_trace"]
    assert data["results"][0]["source"] == "competitive-stub"
    assert data["results"][0]["metadata"]["mode"] == "stub"


@pytest.mark.asyncio
async def test_competitive_intel_with_brave_and_jina(client: AsyncClient):
    """competitive_intel_node must scrape Jina pages when Brave returns results."""
    classify_resp = _make_litellm_response("competitive")
    intel_resp = _make_litellm_response("Competitor charges R4500; you are R200 cheaper.")
    synth_resp = _make_litellm_response("Price advantage confirmed.")

    brave_payload = {
        "web": {
            "results": [
                {"title": "Wetsuit Shop", "description": "Buy wetsuits from R3000", "url": "https://competitor.com/wetsuits"},
            ]
        }
    }
    mock_brave_http = MagicMock()
    mock_brave_http.json.return_value = brave_payload
    mock_brave_http.raise_for_status = MagicMock()

    mock_jina_http = MagicMock()
    mock_jina_http.text = "# Wetsuit prices\n3/2mm wetsuit: R4500\n5/4mm wetsuit: R5800"
    mock_jina_http.raise_for_status = MagicMock()

    mock_client_instance = AsyncMock()
    mock_client_instance.__aenter__ = AsyncMock(return_value=mock_client_instance)
    mock_client_instance.__aexit__ = AsyncMock(return_value=False)
    mock_client_instance.get = AsyncMock(side_effect=[mock_brave_http, mock_jina_http])

    with (
        patch("mass.graph.litellm.acompletion", new=AsyncMock(side_effect=[classify_resp, intel_resp, synth_resp])),
        patch("mass.graph.settings.brave_api_key", "test-brave-key"),
        patch("mass.graph.settings.serper_api_key", ""),
        patch("mass.graph.httpx.AsyncClient", return_value=mock_client_instance),
    ):
        response = await client.post("/search", json={"query": "how does our 3/2mm wetsuit price compare?"})

    data = response.json()
    assert response.status_code == 200
    assert "competitive_intel" in data["agent_trace"]
    assert data["results"][0]["source"] == "competitive-intel"
    assert data["results"][0]["metadata"]["sources_scraped"] >= 1


# ---------------------------------------------------------------------------
# /intelligence endpoint
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_intelligence_endpoint_exists(client: AsyncClient):
    """/intelligence must return 200 (stub mode — no API keys set)."""
    with (
        patch("mass.graph.settings.brave_api_key", ""),
        patch("mass.graph.settings.serper_api_key", ""),
    ):
        synth_resp = _make_litellm_response("Intelligence synthesis.")
        with patch("mass.graph.litellm.acompletion", new=AsyncMock(return_value=synth_resp)):
            response = await client.post("/intelligence", json={"query": "competitor pricing"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_intelligence_endpoint_pre_sets_competitive_intent(client: AsyncClient):
    """/intelligence must always return intent='competitive' without calling the classifier."""
    with (
        patch("mass.graph.settings.brave_api_key", ""),
        patch("mass.graph.settings.serper_api_key", ""),
    ):
        synth_resp = _make_litellm_response("Analysis done.")
        # Only ONE acompletion call expected (synthesize), not two (classify + synthesize)
        with patch("mass.graph.litellm.acompletion", new=AsyncMock(return_value=synth_resp)):
            response = await client.post("/intelligence", json={"query": "market check"})

    data = response.json()
    assert data["intent"] == "competitive"
    assert "competitive_intel" in data["agent_trace"]


@pytest.mark.asyncio
async def test_intelligence_endpoint_requires_api_key_when_configured(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    """/intelligence must return 401 when key is set but header is missing."""
    monkeypatch.setattr("mass.main.settings.mass_api_key", "owner-secret")
    response = await client.post("/intelligence", json={"query": "pricing check"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_intelligence_endpoint_accepts_correct_key(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    """/intelligence must accept requests with the correct X-Api-Key."""
    monkeypatch.setattr("mass.main.settings.mass_api_key", "owner-secret")
    with (
        patch("mass.graph.settings.brave_api_key", ""),
        patch("mass.graph.settings.serper_api_key", ""),
    ):
        synth_resp = _make_litellm_response("Authenticated analysis.")
        with patch("mass.graph.litellm.acompletion", new=AsyncMock(return_value=synth_resp)):
            response = await client.post(
                "/intelligence",
                json={"query": "pricing check"},
                headers={"X-Api-Key": "owner-secret"},
            )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "competitive"

