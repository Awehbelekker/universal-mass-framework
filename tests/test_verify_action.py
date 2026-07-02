"""Step 4 — verified-reasoning port: the verify_action node independently checks the action_agent's
extracted tool call against the tool's contract before synthesize."""
import asyncio

from mass.graph import build_graph, verify_action_node


def _run(coro):
    return asyncio.run(coro)


def _state(tool_args, tool_name="send_email"):
    return {
        "query": "email bob about the meeting",
        "results": [{
            "content": "orig", "source": "action-agent", "score": 1.0,
            "metadata": {"intent": "action", "tool_name": tool_name, "tool_args": tool_args},
        }],
    }


def test_graph_includes_verify_action_node():
    g = build_graph()
    assert "verify_action" in g.get_graph().nodes


def test_wellformed_action_is_verified():
    out = _run(verify_action_node(_state({"to": "a@b.com", "subject": "Hi", "body": "x"})))
    meta = out["results"][0]["metadata"]
    assert meta["verified"] is True
    assert not meta.get("escalated")
    assert out["agent_trace"] == ["verify_action"]


def test_missing_required_field_is_flagged_for_human():
    out = _run(verify_action_node(_state({"to": "a@b.com"})))  # missing subject + body
    meta = out["results"][0]["metadata"]
    assert meta["verified"] is False
    assert meta["escalated"] is True
    assert "UNVERIFIED ACTION" in out["results"][0]["content"]
    assert out["results"][0]["score"] <= 0.3


def test_wrong_type_is_flagged():
    out = _run(verify_action_node(_state({"to": 123, "subject": "Hi", "body": "x"})))
    assert out["results"][0]["metadata"]["verified"] is False


def test_no_tool_call_passes_through():
    out = _run(verify_action_node({"query": "q", "results": [{"content": "c", "metadata": {"tool_name": None}}]}))
    assert out["results"][0]["metadata"]["verified"] is None


def test_empty_results_is_safe():
    out = _run(verify_action_node({"query": "q", "results": []}))
    assert "verify_action:skip" in out["agent_trace"]
