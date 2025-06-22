import logging
import pytest
import asyncio
from agents.ai_agents.core import Agent
from agents.ai_agents.types import DataFetcherAgent, DecisionAgent
from agents.ai_agents.distributed import DistributedCoordinator
from agents.ai_agents.message_bus import MessageBus

class DataFetcherAgent(Agent):
    async def on_message(self, sender, message):
        if message.get("type") == "fetch":
            url = message.get("url")
            if url:
                data = await self.fetch_live_data(url)
                logging.info(f"{self.name} fetched data from {url}: {data}")

class DecisionAgent(Agent):
    async def on_message(self, sender, message):
        if message.get("type") == "decision_request":
            # Simulate a decision based on message content
            decision = "approve" if message.get("value", 0) > 0 else "reject"
            logging.info(f"{self.name} made decision: {decision}")
            await self.send(sender, "decision_response", {"decision": decision})

@pytest.mark.asyncio
async def test_distributed_coordination():
    results = []

    async def on_message(sender, message):
        if message.get("type") == "conflict_resolved":
            results.append(message["details"])

    bus = MessageBus()
    agent1 = DataFetcherAgent("Fetcher1", on_message, bus=bus)
    agent2 = DecisionAgent("Decider1", on_message, bus=bus)
    agent3 = DataFetcherAgent("Fetcher2", on_message, bus=bus)
    agent4 = DecisionAgent("Decider2", on_message, bus=bus)

    group1 = [agent1, agent2]
    group2 = [agent3, agent4]
    coordinator = DistributedCoordinator([group1, group2])

    task1 = asyncio.create_task(agent1.run())
    task2 = asyncio.create_task(agent2.run())
    task3 = asyncio.create_task(agent3.run())
    task4 = asyncio.create_task(agent4.run())

    # Simulate distributed conflict
    await coordinator.resolve_conflict({"details": "node sync issue"})
    await asyncio.sleep(0.1)

    agent1.stop()
    agent2.stop()
    agent3.stop()
    agent4.stop()
    for t in [task1, task2, task3, task4]:
        t.cancel()
    await asyncio.gather(task1, task2, task3, task4, return_exceptions=True)

    # The results list will have one entry per agent, so check all entries
    assert results and all(r == "node sync issue" or (isinstance(r, dict) and r.get("details") == "node sync issue") for r in results)