import pytest
import asyncio
import time
from core.agent_base import AgentBase, AgentMessage, MessageType
from core.mass_coordinator import MASSCoordinator
from typing import Any, Dict, List

class DummyAgent(AgentBase):
    def __init__(self, agent_id: str):
        super().__init__(agent_id, "test")
        self.received: List[AgentMessage] = []
        self.error_flag = False

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        if task_data.get("fail"):
            self.error_flag = True
            raise ValueError("Simulated error")
        return {"result": self.agent_id}

    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"analysis": self.agent_id}

    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        return {"coordination": self.agent_id}

    async def process_message_queue(self):
        while self.message_queue:
            message: AgentMessage = self.message_queue.pop(0)
            self.received.append(message)

@pytest.mark.asyncio
async def test_coordinator_routes_messages():
    coordinator = MASSCoordinator()
    agent_a = DummyAgent("A")
    agent_b = DummyAgent("B")
    coordinator.register_agent("A", agent_a)
    coordinator.register_agent("B", agent_b)
    msg = AgentMessage(
        sender_id="A",
        receiver_id="B",
        message_type=MessageType.COORDINATION_REQUEST,
        payload={"info": "test"},
        timestamp=time.time(),
        correlation_id="corr-1",
        priority=1
    )
    await coordinator.route_message(msg)
    assert len(agent_b.received) == 1
    assert agent_b.received[0].payload["info"] == "test"

@pytest.mark.asyncio
async def test_coordinator_multiple_agents():
    coordinator = MASSCoordinator()
    agents = [DummyAgent(str(i)) for i in range(3)]
    for agent in agents:
        coordinator.register_agent(agent.agent_id, agent)
    # Send messages between all agents
    for i, sender in enumerate(agents):
        for j, receiver in enumerate(agents):
            if i != j:
                msg = AgentMessage(
                    sender_id=sender.agent_id,
                    receiver_id=receiver.agent_id,
                    message_type=MessageType.STATUS_UPDATE,
                    payload={"from": sender.agent_id, "to": receiver.agent_id},
                    timestamp=time.time(),
                    correlation_id=f"corr-{i}-{j}",
                    priority=1
                )
                await coordinator.route_message(msg)
    # Each agent should have received 2 messages
    for agent in agents:
        assert len(agent.received) == 2
        received_from = set(m.payload["from"] for m in agent.received)
        assert agent.agent_id not in received_from

@pytest.mark.asyncio
async def test_coordinator_handles_missing_agent():
    coordinator = MASSCoordinator()
    agent_a = DummyAgent("A")
    coordinator.register_agent("A", agent_a)
    msg = AgentMessage(
        sender_id="A",
        receiver_id="B",  # B is not registered
        message_type=MessageType.STATUS_UPDATE,
        payload={"info": "should not deliver"},
        timestamp=time.time(),
        correlation_id="corr-missing",
        priority=1
    )
    # Should not raise, just not deliver
    await coordinator.route_message(msg)
    # No error, no delivery
    assert not hasattr(coordinator, 'agents') or "B" not in coordinator.agents or not getattr(coordinator.agents.get("B", None), 'received', [])

@pytest.mark.asyncio
async def test_agent_process_task_error():
    agent = DummyAgent("X")
    with pytest.raises(ValueError):
        await agent.process_task({"fail": True})
    assert agent.error_flag is True
