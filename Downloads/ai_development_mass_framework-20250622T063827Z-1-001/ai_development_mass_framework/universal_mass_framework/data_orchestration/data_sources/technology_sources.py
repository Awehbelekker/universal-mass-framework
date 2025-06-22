"""Technology trends and adoption data source implementation."""

import aiohttp
import logging
from typing import Dict, Any, List
from datetime import datetime

class TechnologyDataSources:
    """Technology trends and adoption intelligence."""
    
    def __init__(self):
        self.session = None
        
    async def get_contextual_data(self, context) -> List[Dict[str, Any]]:
        """Get technology trend data."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        # Get GitHub trending data (public API)
        tech_data = await self._get_github_trends()
        return [tech_data] if tech_data else []
    
    async def _get_github_trends(self) -> Dict[str, Any]:
        """Get GitHub trending repositories."""
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": "created:>2024-01-01",
                "sort": "stars",
                "order": "desc",
                "per_page": 10
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    repos = data.get("items", [])
                    
                    return {
                        "type": "technology_trends",
                        "timestamp": datetime.utcnow().isoformat(),
                        "data": {
                            "trending_repos": len(repos),
                            "top_languages": self._extract_languages(repos),
                            "total_stars": sum(repo.get("stargazers_count", 0) for repo in repos)
                        },
                        "source": "github",
                        "confidence": 0.8
                    }
        except Exception as e:
            logging.error(f"Error fetching GitHub trends: {e}")
            return {"type": "technology_trends", "error": str(e)}
    
    def _extract_languages(self, repos: List[Dict]) -> List[str]:
        """Extract programming languages from repos."""
        languages = [repo.get("language") for repo in repos if repo.get("language")]
        return list(set(languages))[:5]
    
    async def close(self):
        if self.session:
            await self.session.close()
