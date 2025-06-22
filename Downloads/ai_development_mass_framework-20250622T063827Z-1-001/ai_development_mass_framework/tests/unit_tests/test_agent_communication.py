import pytest
import asyncio
from core.agent_base import AgentBase, AgentMessage, MessageType
from typing import Dict, Any, List
import time

class DummyAgent(AgentBase):
    def __init__(self, agent_id):
        super().__init__(agent_id, "test")
        self.received = []

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"result": "ok"}

    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"analysis": "ok"}

    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        return {"coordination": "ok"}

    async def process_message_queue(self):
        while self.message_queue:
            message = self.message_queue.pop(0)
            self.received.append(message)

@pytest.mark.asyncio
async def test_agent_message_passing():
    agent_a = DummyAgent("A")
    agent_b = DummyAgent("B")
    class DummyCoordinator:
        async def route_message(self, message):
            await agent_b.receive_message(message)
    agent_a.coordinator = DummyCoordinator()
    msg = AgentMessage(
        sender_id="A",
        receiver_id="B",
        message_type=MessageType.ANALYSIS_REQUEST,
        payload={"data": 123},
        timestamp=time.time(),
        correlation_id="test-1",
        priority=5
    )
    await agent_a.send_message(msg)
    assert len(agent_b.received) == 1
    assert agent_b.received[0].payload["data"] == 123
