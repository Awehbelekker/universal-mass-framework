import logging
from agents.ai_agents.core import Agent

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
            await self.send(sender, {"type": "decision_response", "decision": decision})