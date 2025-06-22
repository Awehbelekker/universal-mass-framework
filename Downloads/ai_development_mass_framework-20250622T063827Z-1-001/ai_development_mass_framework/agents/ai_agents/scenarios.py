import asyncio
import logging
from agents.ai_agents.types import DataFetcherAgent, DecisionAgent
from agents.ai_agents.core import Coordinator

async def live_data_scenario():
    results = []

    async def fetcher_on_message(sender, message):
        if message.get("type") == "fetch":
            url = message.get("url")
            data = await fetcher.fetch_live_data(url)
            results.append((url, data))
            await fetcher.send(decider, {"type": "decision_request", "value": data.get("temp", 0)})

    async def decider_on_message(sender, message):
        if message.get("type") == "decision_request":
            value = message.get("value", 0)
            decision = "hot" if value > 20 else "cold"
            results.append(("decision", decision))
            await decider.send(fetcher, {"type": "decision_response", "decision": decision})

    fetcher = DataFetcherAgent("WeatherFetcher", fetcher_on_message)
    decider = DecisionAgent("WeatherDecider", decider_on_message)
    coordinator = Coordinator([fetcher, decider])

    task_fetcher = asyncio.create_task(fetcher.run())
    task_decider = asyncio.create_task(decider.run())

    # Simulate live weather data fetch
    await fetcher.send(fetcher, {"type": "fetch", "url": "https://api.example.com/weather"})
    await asyncio.sleep(0.2)

    fetcher.stop()
    decider.stop()
    task_fetcher.cancel()
    task_decider.cancel()
    await asyncio.gather(task_fetcher, task_decider, return_exceptions=True)
    return results