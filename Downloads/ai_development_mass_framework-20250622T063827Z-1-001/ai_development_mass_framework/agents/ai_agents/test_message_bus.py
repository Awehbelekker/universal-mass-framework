import asyncio
import pytest
from agents.ai_agents.message_bus import MessageBus, Message

@pytest.mark.asyncio
async def test_message_delivery():
    bus = MessageBus()
    bus.register_agent("agent1")
    bus.register_agent("agent2")

    msg = Message(sender="agent1", recipient="agent2", type_="test", payload={"data": 123})
    await bus.send(msg)
    received = await bus.receive("agent2")

    assert received.sender == "agent1"
    assert received.recipient == "agent2"
    assert received.type == "test"
    assert received.payload == {"data": 123}

@pytest.mark.asyncio
async def test_unregistered_agent_raises():
    bus = MessageBus()
    bus.register_agent("agent1")
    msg = Message(sender="agent1", recipient="agent2", type_="test", payload=None)
    with pytest.raises(ValueError):
        await bus.send(msg)
    with pytest.raises(ValueError):
        await bus.receive("agent2")
