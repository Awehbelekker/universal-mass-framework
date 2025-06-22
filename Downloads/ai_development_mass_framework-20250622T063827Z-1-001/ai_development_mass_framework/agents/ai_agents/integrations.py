import os
import logging
from agents.ai_agents.core import Agent

class WeatherAgent(Agent):
    async def on_message(self, sender, message):
        if message.get("type") == "fetch_weather":
            city = message.get("city", "London")
            api_key = os.getenv("OPENWEATHER_API_KEY", "demo")
            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}&appid={api_key}&units=metric"
            )
            data = await self.fetch_live_data(url)
            temp = data.get("main", {}).get("temp")
            logging.info(f"{self.name} fetched weather for {city}: {temp}°C")
            await self.send(sender, "weather_data", {"city": city, "temp": temp})