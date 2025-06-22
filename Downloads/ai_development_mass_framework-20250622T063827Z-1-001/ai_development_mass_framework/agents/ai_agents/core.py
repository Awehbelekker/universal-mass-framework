import asyncio
import aiohttp
import logging
from typing import Any, Dict, List, Callable, Awaitable, Optional
from agents.ai_agents.strategies import ConflictResolutionStrategy, FirstComeFirstServeStrategy
from core.mass_framework import MassFramework
from agents.ai_agents.message_bus import MessageBus, Message

class Agent:
    def __init__(self, name: str, on_message: Callable[[str, Any], Awaitable[None]], bus: Optional[MessageBus] = None):
        self.name = name
        self.on_message = on_message
        self.bus = bus or MessageBus()
        self.bus.register_agent(self.name)
        self.running = True
    
    async def send(self, recipient: str, type_: str, payload: Any) -> None:
        msg = Message(sender=self.name, recipient=recipient, type_=type_, payload=payload)
        await self.bus.send(msg)
    
    async def receive(self) -> None:
        msg = await self.bus.receive(self.name)
        await self.on_message(msg.sender, msg.payload)
    
    async def fetch_live_data(self, url: str) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        logging.info(f"{self.name} fetched data: {data}")
                        return data
                    else:
                        logging.error(f"{self.name} failed to fetch data from {url} (status {response.status})")
                        return {}
        except Exception as e:
            logging.error(f"{self.name} encountered error fetching data: {e}")
            return {}

    async def run(self) -> None:
        try:
            while self.running:
                await self.receive()
        except asyncio.CancelledError:
            logging.info(f"{self.name} shutting down gracefully.")

    def stop(self) -> None:
        self.running = False

class Coordinator:
    def __init__(self, agents: List[Agent], strategy: Optional[ConflictResolutionStrategy] = None):
        self.agents = agents
        self.conflicts: List[Dict[str, Any]] = []
        self.strategy = strategy or FirstComeFirstServeStrategy()
        # Use the bus from the first agent (all agents should share the same bus)
        self.bus = agents[0].bus if agents else None

    async def resolve_conflict(self, conflict: Dict[str, Any]) -> None:
        self.conflicts.append(conflict)
        logging.info(f"Received conflict: {conflict}")
        resolution = self.strategy.resolve(self.conflicts)
        logging.info(f"Resolved conflict: {resolution}")
        # Send a message to all agents via the bus
        for agent in self.agents:
            await self.bus.send(Message(
                sender="Coordinator",
                recipient=agent.name,
                type_="conflict_resolved",
                payload={"type": "conflict_resolved", "details": resolution}
            ))
        self.conflicts.clear()

    async def monitor(self):
        # Example: monitor for conflicts and resolve periodically
        while True:
            await asyncio.sleep(1)
            if self.conflicts:
                await self.resolve_conflict(self.conflicts[-1])

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )

def main():
    setup_logging()
    # Example: initialize agents and coordinator here if running as script
    pass

if __name__ == "__main__":
    main()

import pytest
import asyncio
from agents.ai_agents.core import Agent, Coordinator
from agents.ai_agents.strategies import FirstComeFirstServeStrategy, MajorityVoteStrategy

@pytest.mark.asyncio
async def test_coordinator_resolves_conflict():
    resolutions = []
    bus = MessageBus()

    async def on_message(sender, message):
        if message.get("type") == "conflict_resolved":
            resolutions.append(message["details"])

    agent1 = Agent("Agent1", on_message, bus=bus)
    agent2 = Agent("Agent2", on_message, bus=bus)
    coordinator = Coordinator([agent1, agent2], strategy=FirstComeFirstServeStrategy())

    # Start agent event loops
    t1 = asyncio.create_task(agent1.run())
    t2 = asyncio.create_task(agent2.run())

    # Simulate a conflict
    conflict = {"details": "resource contention"}
    await coordinator.resolve_conflict(conflict)
    await asyncio.sleep(0.1)

    agent1.stop()
    agent2.stop()
    await asyncio.gather(t1, t2)

    assert resolutions and resolutions[0]["details"] == "resource contention"

@pytest.mark.asyncio
async def test_majority_vote_strategy():
    strategy = MajorityVoteStrategy()
    conflicts = [
        {"details": "A"},
        {"details": "B"},
        {"details": "A"},
    ]
    resolution = strategy.resolve(conflicts)
    assert resolution["details"] == "A"

class MassEnabledAgent(Agent):
    def __init__(
        self, 
        name: str, 
        on_message: Callable[[str, Any], Awaitable[None]], 
        config: Optional[Dict[str, Any]] = None, 
        agent_id: Optional[str] = None, 
        specialization: Optional[str] = None
    ):
        super().__init__(name, on_message)
        self.agent_id = agent_id or name
        self.specialization = specialization or name
        self.mass_optimizer = MassFramework(config or {})
        self.optimization_phase = 'local'  # local → topology → global
        self.prompt_variations: Dict[str, List[str]] = {}
        self.optimized_prompt: Optional[str] = None

    async def optimize_with_mass(
        self, 
        agents: Dict[str, Any], 
        validation_data: Dict[str, List[Dict[str, Any]]], 
        validation_scenarios: List[Dict[str, Any]]
    ) -> None:
        await self.mass_optimizer.optimize_with_mass(agents, validation_data, validation_scenarios)