"""Weather and environmental data source implementation."""

import aiohttp
import logging
from typing import Dict, Any, List
from datetime import datetime
from core.config_manager import config_manager

class WeatherDataSources:
    """Weather and environmental data intelligence."""
    
    def __init__(self):
        self.config = config_manager.config
        self.weather_api_key = self.config.weather_api_key
        self.session = None
        
    async def get_contextual_data(self, context) -> List[Dict[str, Any]]:
        """Get weather data relevant to context."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        # Default to major cities if no geographic context
        location = getattr(context, 'geographic_context', 'New York')
        weather_data = await self._get_current_weather(location)
        
        return [weather_data] if weather_data else []
    
    async def _get_current_weather(self, location: str) -> Dict[str, Any]:
        """Get current weather for location."""
        try:
            if not self.weather_api_key:
                return {"type": "weather", "error": "No weather API key"}
            
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location,
                "appid": self.weather_api_key,
                "units": "metric"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    return {
                        "type": "weather",
                        "timestamp": datetime.utcnow().isoformat(),
                        "data": {
                            "location": location,
                            "temperature": data.get("main", {}).get("temp"),
                            "humidity": data.get("main", {}).get("humidity"),
                            "weather": data.get("weather", [{}])[0].get("main"),
                            "description": data.get("weather", [{}])[0].get("description")
                        },
                        "source": "openweather",
                        "confidence": 0.9
                    }
        except Exception as e:
            logging.error(f"Error fetching weather data: {e}")
            return {"type": "weather", "error": str(e)}
    
    async def close(self):
        if self.session:
            await self.session.close()
