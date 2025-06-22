import logging
from typing import Dict, Any, Optional, Callable, Awaitable
from agents.ai_agents.core import MassEnabledAgent

class NewsAgent(MassEnabledAgent):
    def __init__(self, name: str, on_message: Callable[[str, Any], Awaitable[None]], config: Optional[Dict[str, Any]] = None):
        super().__init__(name, on_message, config, agent_id=name, specialization="News Agent")
        self.prompt_variations = {
            'relevance_analysis': [
                "Analyze this news for gaming relevance:",
                "Step-by-step news analysis for gaming platform: 1) Identify key entities 2) Assess impact",
                "Analyze news relevance using this framework: Political events (weight: 0.3), Economic (0.4), Social (0.3)",
                "Think like a gaming economist analyzing this news. Consider: Will this create new opportunities?"
            ]
        }
        self.optimized_prompt = None

    async def optimize_local_prompts(self, validation_data: Dict[str, Any]) -> Optional[str]:
        self.optimized_prompt = await self.mass_optimizer.prompt_optimizer.evaluate_prompts(
            self.prompt_variations['relevance_analysis'], validation_data, metric='relevance_accuracy')
        return self.optimized_prompt

    async def on_message(self, sender: str, message: Dict[str, Any]) -> None:
        logging.info(f"NewsAgent.on_message called with: {message}")
        if message.get("type") == "fetch_news":
            topic = message.get("topic", "technology")
            url = f"https://newsapi.org/v2/everything?q={topic}&apiKey=YOUR_NEWSAPI_KEY"
            data = await self.fetch_live_data(url)
            articles = data.get("articles", [])
            logging.info(f"{self.name} fetched {len(articles)} articles for topic '{topic}'")
            await self.send(sender, "news_data", {"topic": topic, "articles": articles})
            logging.info(f"NewsAgent sent news_data message for topic '{topic}' to {sender}")