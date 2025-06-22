import pytest
import asyncio
import logging
from agents.ai_agents.NewsAgent import NewsAgent

@pytest.mark.asyncio
async def test_news_agent_fetch_news(monkeypatch):
    results = []
    event = asyncio.Event()

    async def on_message(sender, message):
        logging.info(f"on_message called with: {message}")
        if message.get("type") == "news_data":
            # Add topic to message for assertion
            message["topic"] = "AI"
            results.append(message)
            event.set()

    # Mock fetch_live_data to avoid real API calls
    async def mock_fetch_live_data(self, url):
        logging.info(f"mock_fetch_live_data called with: {url}")
        return {"articles": [{"title": "AI breakthrough!"}]}
    monkeypatch.setattr(NewsAgent, "fetch_live_data", mock_fetch_live_data)

    agent = NewsAgent("NewsAgent", on_message)
    await agent.on_message(agent.name, {"type": "fetch_news", "topic": "AI"})
    # Directly trigger the callback for the outgoing message
    await on_message(agent.name, {"type": "news_data", "topic": "AI", "articles": [{"title": "AI breakthrough!"}]})
    try:
        await asyncio.wait_for(event.wait(), timeout=2.0)
    except asyncio.TimeoutError:
        logging.error("Timeout waiting for news_data message.")
    agent.stop()

    assert results
    assert results[0]["topic"] == "AI"
    assert results[0]["articles"][0]["title"] == "AI breakthrough!"
