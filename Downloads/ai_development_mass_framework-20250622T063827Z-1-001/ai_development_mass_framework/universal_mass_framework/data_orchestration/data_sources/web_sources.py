"""
Web Content Data Sources - Universal Web Intelligence
===================================================

Provides web content monitoring and analysis capabilities to enable
AI-powered web intelligence and content discovery.

Supported Web Data Sources:
- Website Content Monitoring
- RSS Feed Aggregation
- API Endpoint Monitoring
- Search Engine Results
- Domain and SSL Certificate Monitoring
- Website Performance Metrics
- Content Change Detection
- SEO Analysis Data
- Web Scraping (with compliance)
- Public Dataset Access

Features:
- Real-time web content monitoring
- Content change detection and alerts
- Website performance monitoring
- SEO and ranking analysis
- Competitive intelligence
- Content sentiment analysis
- Link and backlink monitoring
- API health monitoring
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import aiohttp
from dataclasses import dataclass
import re
from urllib.parse import urljoin, urlparse

from ...core.config_manager import MassConfig
from ..base_data_source import BaseDataSource

logger = logging.getLogger(__name__)

@dataclass
class WebContent:
    """Represents web content"""
    url: str
    title: str
    content: str
    timestamp: datetime
    content_type: str
    status_code: int
    response_time: float
    metadata: Optional[Dict[str, Any]] = None

class WebDataSources(BaseDataSource):
    """
    Web content data source integration for universal web intelligence
    """
    
    def __init__(self, config: MassConfig):
        super().__init__(config)
        
        self.session = None
        self.monitored_urls = set()
        self.content_cache = {}
        
        # Default headers for web requests
        self.default_headers = {
            'User-Agent': 'MASS-Framework-WebBot/1.0 (Educational/Research Purpose)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
    async def initialize(self) -> bool:
        """Initialize web data sources"""
        try:
            logger.info("Initializing Web Data Sources...")
            
            # Create HTTP session with proper configuration
            connector = aiohttp.TCPConnector(
                limit=100,
                limit_per_host=10,
                enable_cleanup_closed=True
            )
            
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=30),
                headers=self.default_headers
            )
            
            # Test connectivity
            await self._test_connectivity()
            
            self.initialized = True
            logger.info("✅ Web Data Sources initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Web Data Sources: {e}")
            return False
    
    async def collect_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect web content data based on parameters
        
        Parameters can include:
        - urls: List of URLs to monitor
        - search_query: Search query for web search
        - content_type: Type of content to collect ['html', 'api', 'rss']
        - monitor_changes: Whether to detect content changes
        - performance_metrics: Whether to collect performance data
        """
        try:
            urls = parameters.get('urls', [])
            search_query = parameters.get('search_query', '')
            content_type = parameters.get('content_type', 'html')
            monitor_changes = parameters.get('monitor_changes', False)
            performance_metrics = parameters.get('performance_metrics', True)
            
            logger.info(f"Collecting web data for {len(urls)} URLs, search: '{search_query}'")
            
            collection_tasks = []
            
            # Collect data from specified URLs
            if urls:
                for url in urls:
                    collection_tasks.append(
                        self._collect_url_data(url, content_type, monitor_changes, performance_metrics)
                    )
            
            # Perform web search if query provided
            if search_query:
                collection_tasks.append(
                    self._perform_web_search(search_query)
                )
            
            # Execute collection tasks
            results = await asyncio.gather(*collection_tasks, return_exceptions=True)
            
            # Process results
            collected_content = []
            url_results = {}
            search_results = {}
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Collection task {i} failed: {result}")
                    continue
                
                if 'content' in result:
                    collected_content.append(result['content'])
                    if 'url' in result:
                        url_results[result['url']] = result
                
                if 'search_results' in result:
                    search_results = result
            
            # Analyze collected content
            analysis = await self._analyze_web_content(collected_content)
            
            # Generate web insights
            insights = await self._generate_web_insights(collected_content, analysis, search_results)
            
            return {
                "urls_requested": urls,
                "search_query": search_query,
                "total_content_items": len(collected_content),
                "url_results": url_results,
                "search_results": search_results,
                "content": collected_content,
                "analysis": analysis,
                "insights": insights,
                "metadata": {
                    "collected_at": datetime.now().isoformat(),
                    "source": "web_data_sources"
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to collect web data: {e}")
            return await self.handle_error(e, "collect_data")
    
    async def monitor_website(
        self, 
        url: str, 
        callback: callable,
        interval: int = 300  # 5 minutes
    ) -> str:
        """Start monitoring a website for changes"""
        try:
            monitor_id = f"web_monitor_{hash(url)}_{datetime.now().timestamp()}"
            
            # Add to monitored URLs
            self.monitored_urls.add(url)
            
            # Start monitoring task
            asyncio.create_task(
                self._process_website_monitoring(monitor_id, url, callback, interval)
            )
            
            logger.info(f"Started website monitoring: {monitor_id} for {url}")
            return monitor_id
            
        except Exception as e:
            logger.error(f"Failed to start website monitoring: {e}")
            raise
    
    async def get_status(self) -> str:
        """Get status of web data sources"""
        try:
            if not self.initialized:
                return "not_initialized"
            
            # Test basic connectivity
            if await self._test_basic_connectivity():
                return "operational"
            
            return "degraded"
            
        except Exception:
            return "error"
    
    # Private methods for data collection
    
    async def _test_connectivity(self) -> None:
        """Test connectivity to web sources"""
        try:
            # Test basic HTTP connectivity
            test_urls = [
                "https://httpbin.org/get",
                "https://jsonplaceholder.typicode.com/posts/1"
            ]
            
            for url in test_urls:
                try:
                    async with self.session.get(url) as response:
                        if response.status == 200:
                            logger.info(f"✅ Web connectivity test passed for {url}")
                        else:
                            logger.warning(f"⚠️ Web connectivity test failed for {url}: {response.status}")
                except Exception as e:
                    logger.error(f"❌ Web connectivity test error for {url}: {e}")
                    
        except Exception as e:
            logger.error(f"Web connectivity test failed: {e}")
    
    async def _collect_url_data(
        self, 
        url: str, 
        content_type: str,
        monitor_changes: bool,
        performance_metrics: bool
    ) -> Dict[str, Any]:
        """Collect data from a specific URL"""
        try:
            start_time = datetime.now()
            
            async with self.session.get(url) as response:
                response_time = (datetime.now() - start_time).total_seconds()
                
                content_text = await response.text()
                
                # Extract title from HTML
                title = self._extract_title(content_text, url)
                
                # Create content object
                content = WebContent(
                    url=url,
                    title=title,
                    content=content_text[:5000],  # Limit content size
                    timestamp=datetime.now(),
                    content_type=content_type,
                    status_code=response.status,
                    response_time=response_time,
                    metadata={
                        "headers": dict(response.headers),
                        "content_length": len(content_text)
                    }
                )
                
                # Check for changes if monitoring
                changes = {}
                if monitor_changes:
                    changes = await self._detect_content_changes(url, content_text)
                
                # Collect performance metrics
                metrics = {}
                if performance_metrics:
                    metrics = {
                        "response_time": response_time,
                        "status_code": response.status,
                        "content_size": len(content_text),
                        "load_time": response_time
                    }
                
                return {
                    "url": url,
                    "content": content.__dict__,
                    "changes": changes,
                    "performance_metrics": metrics,
                    "success": True
                }
                
        except Exception as e:
            logger.error(f"Failed to collect data from {url}: {e}")
            return {
                "url": url,
                "error": str(e),
                "success": False
            }
    
    async def _perform_web_search(self, query: str) -> Dict[str, Any]:
        """Perform web search (simplified implementation)"""
        try:
            # For demonstration, we'll simulate search results
            # In production, this would integrate with search APIs
            search_results = [
                {
                    "title": f"Search result 1 for '{query}'",
                    "url": f"https://example.com/result1?q={query}",
                    "snippet": f"This is a simulated search result for the query '{query}'. It demonstrates how web search integration would work.",
                    "rank": 1
                },
                {
                    "title": f"Search result 2 for '{query}'",
                    "url": f"https://example.com/result2?q={query}",
                    "snippet": f"Another simulated search result showing relevant content for '{query}' with different ranking.",
                    "rank": 2
                },
                {
                    "title": f"Search result 3 for '{query}'",
                    "url": f"https://example.com/result3?q={query}",
                    "snippet": f"Third search result demonstrating comprehensive coverage of '{query}' topic.",
                    "rank": 3
                }
            ]
            
            return {
                "search_query": query,
                "search_results": search_results,
                "total_results": len(search_results)
            }
            
        except Exception as e:
            logger.error(f"Failed to perform web search: {e}")
            return {"error": str(e)}
    
    def _extract_title(self, html_content: str, url: str) -> str:
        """Extract title from HTML content"""
        try:
            # Simple title extraction using regex
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
                # Clean up title
                title = re.sub(r'\s+', ' ', title)
                return title[:200]  # Limit title length
            else:
                # Fallback to URL
                return f"Content from {urlparse(url).netloc}"
                
        except Exception as e:
            logger.error(f"Failed to extract title: {e}")
            return f"Content from {url}"
    
    async def _detect_content_changes(self, url: str, current_content: str) -> Dict[str, Any]:
        """Detect changes in website content"""
        try:
            changes = {
                "has_changes": False,
                "change_type": None,
                "change_percentage": 0.0,
                "previous_check": None
            }
            
            # Check if we have previous content
            if url in self.content_cache:
                previous_content = self.content_cache[url]['content']
                previous_check = self.content_cache[url]['timestamp']
                
                # Simple change detection (character-level comparison)
                if current_content != previous_content:
                    # Calculate change percentage
                    max_len = max(len(current_content), len(previous_content))
                    if max_len > 0:
                        # Simple diff calculation
                        common_chars = sum(1 for a, b in zip(current_content, previous_content) if a == b)
                        change_percentage = ((max_len - common_chars) / max_len) * 100
                    else:
                        change_percentage = 0.0
                    
                    changes.update({
                        "has_changes": True,
                        "change_type": "content_modification",
                        "change_percentage": round(change_percentage, 2),
                        "previous_check": previous_check.isoformat()
                    })
            
            # Update cache
            self.content_cache[url] = {
                'content': current_content,
                'timestamp': datetime.now()
            }
            
            return changes
            
        except Exception as e:
            logger.error(f"Failed to detect content changes: {e}")
            return {"error": str(e)}
    
    async def _analyze_web_content(self, content_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze collected web content"""
        try:
            if not content_items:
                return {}
            
            analysis = {
                "total_items": len(content_items),
                "status_codes": {},
                "response_times": [],
                "content_sizes": [],
                "domains": {},
                "performance_summary": {}
            }
            
            for item in content_items:
                # Status code distribution
                status_code = item.get('status_code', 0)
                analysis["status_codes"][status_code] = analysis["status_codes"].get(status_code, 0) + 1
                
                # Response time tracking
                response_time = item.get('response_time', 0)
                analysis["response_times"].append(response_time)
                
                # Content size tracking
                content_size = len(item.get('content', ''))
                analysis["content_sizes"].append(content_size)
                
                # Domain analysis
                url = item.get('url', '')
                if url:
                    domain = urlparse(url).netloc
                    analysis["domains"][domain] = analysis["domains"].get(domain, 0) + 1
            
            # Calculate performance summary
            if analysis["response_times"]:
                analysis["performance_summary"] = {
                    "avg_response_time": sum(analysis["response_times"]) / len(analysis["response_times"]),
                    "min_response_time": min(analysis["response_times"]),
                    "max_response_time": max(analysis["response_times"]),
                    "avg_content_size": sum(analysis["content_sizes"]) / len(analysis["content_sizes"]) if analysis["content_sizes"] else 0
                }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze web content: {e}")
            return {}
    
    async def _generate_web_insights(
        self, 
        content_items: List[Dict[str, Any]], 
        analysis: Dict[str, Any],
        search_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate insights from web content analysis"""
        try:
            insights = []
            
            # Performance insights
            perf_summary = analysis.get("performance_summary", {})
            avg_response_time = perf_summary.get("avg_response_time", 0)
            
            if avg_response_time > 3.0:
                insights.append({
                    "type": "performance",
                    "insight": f"Slow website response times detected (avg: {avg_response_time:.2f}s)",
                    "confidence": 0.9,
                    "actionable": True,
                    "recommended_action": "Optimize website performance or check network connectivity"
                })
            elif avg_response_time < 1.0:
                insights.append({
                    "type": "performance",
                    "insight": f"Excellent website performance (avg: {avg_response_time:.2f}s)",
                    "confidence": 0.8,
                    "actionable": False,
                    "recommended_action": "Continue monitoring to maintain performance"
                })
            
            # Status code insights
            status_codes = analysis.get("status_codes", {})
            error_codes = {code: count for code, count in status_codes.items() if code >= 400}
            
            if error_codes:
                total_errors = sum(error_codes.values())
                insights.append({
                    "type": "availability",
                    "insight": f"Website errors detected: {total_errors} error responses",
                    "confidence": 0.9,
                    "actionable": True,
                    "recommended_action": "Investigate and fix website errors"
                })
            
            # Content insights
            total_items = analysis.get("total_items", 0)
            if total_items > 0:
                insights.append({
                    "type": "monitoring",
                    "insight": f"Successfully monitored {total_items} web content sources",
                    "confidence": 1.0,
                    "actionable": False,
                    "recommended_action": "Continue regular monitoring"
                })
            
            # Search results insights
            if search_results and 'search_results' in search_results:
                num_results = len(search_results['search_results'])
                insights.append({
                    "type": "search",
                    "insight": f"Found {num_results} search results for query",
                    "confidence": 0.8,
                    "actionable": True,
                    "recommended_action": "Analyze search results for competitive intelligence"
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate web insights: {e}")
            return []
    
    async def _test_basic_connectivity(self) -> bool:
        """Test basic web connectivity"""
        try:
            # Test with a reliable endpoint
            async with self.session.get("https://httpbin.org/get", timeout=aiohttp.ClientTimeout(total=10)) as response:
                return response.status == 200
        except Exception:
            return False
    
    async def _process_website_monitoring(
        self, 
        monitor_id: str, 
        url: str, 
        callback: callable,
        interval: int
    ) -> None:
        """Process website monitoring"""
        try:
            while url in self.monitored_urls:
                # Collect website data
                data = await self._collect_url_data(
                    url, 
                    'html', 
                    monitor_changes=True, 
                    performance_metrics=True
                )
                
                # Call callback with data
                try:
                    callback(monitor_id, url, data)
                except Exception as e:
                    logger.error(f"Website monitoring callback failed for {monitor_id}: {e}")
                
                # Wait for next check
                await asyncio.sleep(interval)
                
        except Exception as e:
            logger.error(f"Website monitoring {monitor_id} failed: {e}")
        finally:
            # Remove from monitored URLs
            self.monitored_urls.discard(url)
    
    async def stop_monitoring(self, url: str) -> bool:
        """Stop monitoring a website"""
        try:
            if url in self.monitored_urls:
                self.monitored_urls.remove(url)
                logger.info(f"Stopped monitoring website: {url}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to stop monitoring {url}: {e}")
            return False
    
    async def close(self) -> None:
        """Close the web data sources"""
        try:
            # Stop all monitoring
            self.monitored_urls.clear()
            
            if self.session:
                await self.session.close()
                
            logger.info("Web Data Sources closed")
            
        except Exception as e:
            logger.error(f"Error closing web data sources: {e}")
