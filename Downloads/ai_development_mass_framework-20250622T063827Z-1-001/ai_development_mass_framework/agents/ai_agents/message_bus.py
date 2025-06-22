import asyncio
from typing import Any, Dict, Optional
import time

class Message:
    def __init__(self, sender: str, recipient: str, type_: str, payload: Any, timestamp: Optional[float] = None):
        self.sender = sender
        self.recipient = recipient
        self.type = type_
        self.payload = payload
        self.timestamp = timestamp if timestamp is not None else time.time()

class MessageBus:
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue[Message]] = {}

    def register_agent(self, agent_name: str):
        if agent_name not in self.queues:
            self.queues[agent_name] = asyncio.Queue()

    async def send(self, message: Message):
        if message.recipient in self.queues:
            await self.queues[message.recipient].put(message)
        else:
            raise ValueError(f"Recipient {message.recipient} not registered on the bus.")

    async def receive(self, agent_name: str) -> Message:
        if agent_name in self.queues:
            return await self.queues[agent_name].get()
        else:
            raise ValueError(f"Agent {agent_name} not registered on the bus.")
