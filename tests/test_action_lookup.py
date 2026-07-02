"""Lookup layer: verify an action's *claim is true* (the referenced record actually exists),
on top of the contract check. Uses a registered stub source; degrades to contract-only when none."""
import asyncio

from mass import verify_sources
from mass.graph import verify_action_node


def _run(coro):
    return asyncio.run(coro)


def _state(args, tool="update_record"):
    return {"query": "update the order", "results": [{
        "content": "orig", "source": "action-agent", "score": 1.0,
        "metadata": {"intent": "action", "tool_name": tool, "tool_args": args},
    }]}


def setup_function(_):
    verify_sources.clear()


def teardown_function(_):
    verify_sources.clear()


def test_no_source_registered_is_contract_only():
    # well-formed args, no ground-truth source → contract passes, lookup skipped (no regression)
    out = _run(verify_action_node(_state({"record_type": "order", "record_id": "X9", "fields": {"status": "shipped"}})))
    assert out["results"][0]["metadata"]["verified"] is True


def test_existing_record_passes_contract_and_lookup():
    verify_sources.register_records({("order", "A1001"): {"status": "paid"}})
    out = _run(verify_action_node(_state({"record_type": "order", "record_id": "A1001", "fields": {"status": "shipped"}})))
    assert out["results"][0]["metadata"]["verified"] is True


def test_nonexistent_record_is_flagged_for_human():
    verify_sources.register_records({("order", "A1001"): {"status": "paid"}})
    out = _run(verify_action_node(_state({"record_type": "order", "record_id": "GHOST", "fields": {"status": "shipped"}})))
    meta = out["results"][0]["metadata"]
    assert meta["verified"] is False
    assert meta["escalated"] is True
    assert "not found" in meta["verify_detail"] or "record_exists" in meta["verify_detail"]
    assert "UNVERIFIED ACTION" in out["results"][0]["content"]
