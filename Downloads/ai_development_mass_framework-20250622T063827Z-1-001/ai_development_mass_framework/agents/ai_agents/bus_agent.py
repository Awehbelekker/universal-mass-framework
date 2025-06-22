import asyncio
from agents.ai_agents.message_bus import MessageBus, Message
from typing import Any, Callable, Awaitable

class BusAgent:
    def __init__(self, name: str, bus: MessageBus, on_message: Callable[[Message], Awaitable[None]]):
        self.name = name
        self.bus = bus
        self.on_message = on_message
        self.bus.register_agent(self.name)
        self.running = True

    async def send(self, recipient: str, type_: str, payload: Any):
        msg = Message(sender=self.name, recipient=recipient, type_=type_, payload=payload)
        await self.bus.send(msg)

    async def receive(self):
        msg = await self.bus.receive(self.name)
        await self.on_message(msg)

    async def run(self):
        while self.running:
            await self.receive()

    def stop(self):
        self.running = False

# Example usage: two agents exchanging messages
if __name__ == "__main__":
    async def agent1_handler(msg: Message):
        print(f"Agent1 received from {msg.sender}: {msg.payload}")
        if msg.payload == "ping":
            await agent1.send("agent2", "reply", "pong")

    async def agent2_handler(msg: Message):
        print(f"Agent2 received from {msg.sender}: {msg.payload}")
        if msg.payload == "pong":
            agent1.stop()
            agent2.stop()

    bus = MessageBus()
    agent1 = BusAgent("agent1", bus, agent1_handler)
    agent2 = BusAgent("agent2", bus, agent2_handler)

    async def main():
        # Start both agents
        t1 = asyncio.create_task(agent1.run())
        t2 = asyncio.create_task(agent2.run())
        # Send initial message
        await agent1.send("agent2", "greeting", "ping")
        await asyncio.gather(t1, t2)

    asyncio.run(main())
