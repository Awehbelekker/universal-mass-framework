import logging
from agents.ai_agents.core import Agent

class StockAgent(Agent):
    async def on_message(self, sender, message):
        if message.get("type") == "fetch_stock":
            symbol = message.get("symbol", "AAPL")
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token=YOUR_API_KEY"
            data = await self.fetch_live_data(url)
            price = data.get("c")
            logging.info(f"{self.name} fetched stock price for {symbol}: {price}")
            await self.send(sender, "stock_data", {"symbol": symbol, "price": price})