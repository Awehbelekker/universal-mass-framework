import asyncio
import random
import logging
from agents.ai_agents.core import Agent

class RaftAgent(Agent):
    def __init__(self, name, on_message, peers):
        super().__init__(name, on_message)
        self.peers = peers  # List of RaftAgent
        self.state = "follower"
        self.current_term = 0
        self.voted_for = None
        self.leader = None

    async def on_message(self, sender, message):
        if message.get("type") == "vote_request":
            term = message["term"]
            if term > self.current_term:
                self.current_term = term
                self.voted_for = sender
                await self.send(sender, "vote_granted", {"term": term})
        elif message.get("type") == "vote_granted":
            # Handled in election logic
            pass
        elif message.get("type") == "heartbeat":
            self.leader = sender
            self.state = "follower"

    async def start_election(self):
        self.state = "candidate"
        self.current_term += 1
        self.voted_for = self.name
        votes = 1  # Vote for self

        for peer in self.peers:
            await self.send(peer, "vote_request", {"term": self.current_term})

        def vote_collector(sender, message):
            nonlocal votes
            if message.get("type") == "vote_granted" and message.get("term") == self.current_term:
                votes += 1

        self.on_message = vote_collector
        await asyncio.sleep(random.uniform(0.05, 0.15))  # Election timeout

        if votes > (len(self.peers) + 1) // 2:
            self.state = "leader"
            self.leader = self.name
            logging.info(f"{self.name} elected as leader for term {self.current_term}")
            await self.send_heartbeats()

    async def send_heartbeats(self):
        while self.state == "leader":
            for peer in self.peers:
                await self.send(peer, "heartbeat", {})
            await asyncio.sleep(0.1)