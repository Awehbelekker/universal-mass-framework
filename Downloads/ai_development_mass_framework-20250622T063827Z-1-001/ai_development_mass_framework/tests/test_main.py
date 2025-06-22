import pytest
import asyncio
import builtins

@pytest.mark.asyncio
async def test_main_script(monkeypatch):
    # Patch print to capture output
    output = []
    monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: output.append(args))

    import main
    await main.main()

    # Check that results and raft heartbeats are present in output
    found_results = any("Results:" in str(line) for line in output)
    found_raft = any("Raft Heartbeats:" in str(line) for line in output)
    assert found_results
    assert found_raft