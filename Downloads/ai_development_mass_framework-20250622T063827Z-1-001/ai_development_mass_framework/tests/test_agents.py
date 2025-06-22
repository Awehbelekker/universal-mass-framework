import pytest
import asyncio
from agents.ai_agents.core import Agent
from agents.ai_agents.message_bus import MessageBus

@pytest.mark.asyncio
async def test_agent_send_receive():
    messages = []

    async def on_message(sender, message):
        messages.append((sender, message))

    bus = MessageBus()
    agent_a = Agent("A", on_message, bus=bus)
    agent_b = Agent("B", on_message, bus=bus)

    task_a = asyncio.create_task(agent_a.run())
    task_b = asyncio.create_task(agent_b.run())

    await agent_a.send("B", "test", {"msg": "hello"})
    await asyncio.sleep(0.1)  # Allow message processing

    assert messages == [("A", {"msg": "hello"})]

    agent_a.stop()
    agent_b.stop()
    task_a.cancel()
    task_b.cancel()
    await asyncio.gather(task_a, task_b, return_exceptions=True)

@pytest.mark.asyncio
async def test_fetch_live_data(monkeypatch):
    class MockResponse:
        status = 200
        async def json(self):
            return {"weather": "sunny"}
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass

    class MockSession:
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        def get(self, url):
            return MockResponse()  # get() should return an async context manager, not a coroutine

    monkeypatch.setattr("aiohttp.ClientSession", lambda: MockSession())

    agent = Agent("TestAgent", lambda s, m: None)
    data = await agent.fetch_live_data("http://fake.url")
    assert data == {"weather": "sunny"}