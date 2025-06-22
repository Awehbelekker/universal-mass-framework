import asyncio
import logging
from agents.ai_agents.core import Agent

class DistributedKVAgent(Agent):
    def __init__(self, name, on_message, peers=None):
        super().__init__(name, on_message)
        self.store = {}
        self.peers = peers or []

    async def on_message(self, sender, message):
        if message.get("type") == "put":
            key, value = message["key"], message["value"]
            self.store[key] = value
            logging.info(f"{self.name} stored {key}: {value}")
            await self.send(sender, "put_ack", {"key": key})
        elif message.get("type") == "get":
            key = message["key"]
            value = self.store.get(key)
            await self.send(sender, "get_response", {"key": key, "value": value})
        elif message.get("type") == "gossip":
            remote_store = message["store"]
            self.store.update(remote_store)
            logging.info(f"{self.name} merged store via gossip.")

    async def gossip(self):
        while True:
            await asyncio.sleep(0.5)
            for peer in self.peers:
                await self.send(peer, "gossip", {"store": self.store})