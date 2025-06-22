import asyncio
import logging
from agents.ai_agents.core import Coordinator, Agent

class DistributedCoordinator(Coordinator):
    def __init__(self, agent_groups):
        # agent_groups: List[List[Agent]]
        self.agent_groups = agent_groups
        self.conflicts = []

    async def broadcast(self, message):
        for group in self.agent_groups:
            for agent in group:
                await agent.send(agent.name, message.get("type", "broadcast"), message)

    async def resolve_conflict(self, conflict):
        self.conflicts.append(conflict)
        logging.info(f"DistributedCoordinator resolving: {conflict}")
        # Broadcast resolution to all groups
        await self.broadcast({"type": "conflict_resolved", "details": conflict})
        self.conflicts.clear()