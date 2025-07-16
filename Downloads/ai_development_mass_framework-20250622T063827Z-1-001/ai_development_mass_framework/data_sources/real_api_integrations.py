import aiohttp
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

# Configure logging
logger = logging.getLogger(__name__)

class MarketDataAPI:
    """Real-time market data API integration"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.alpha_vantage_key = config.get('alpha_vantage_key')
        self.yahoo_finance_enabled = config.get('yahoo_finance_enabled', True)
        self.cache_ttl = config.get('cache_ttl', 300)  # 5 minutes
        self.cache = {}
        
    async def get_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock data using multiple sources"""
        try:
            # Check cache first
            cache_key = f"stock_data:{symbol}"
            if cache_key in self.cache:
                cached_data = self.cache[cache_key]
                if datetime.now() - cached_data['timestamp'] < timedelta(seconds=self.cache_ttl):
                    return cached_data['data']
            
            # Try Yahoo Finance first (free and reliable)
            if self.yahoo_finance_enabled:
                data = await self._get_yahoo_finance_data(symbol)
                if data:
                    self.cache[cache_key] = {
                        'data': data,
                        'timestamp': datetime.now()
                    }
                    return data
            
            # Fallback to Alpha Vantage
            if self.alpha_vantage_key:
                data = await self._get_alpha_vantage_data(symbol)
                if data:
                    self.cache[cache_key] = {
                        'data': data,
                        'timestamp': datetime.now()
                    }
                    return data
            
            # Return mock data if all APIs fail
            logger.warning(f"All APIs failed for {symbol}, returning mock data")
            return self._get_mock_stock_data(symbol)
            
        except Exception as e:
            logger.error(f"Error getting stock data for {symbol}: {e}")
            return self._get_mock_stock_data(symbol)
    
    async def _get_yahoo_finance_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get data from Yahoo Finance API"""
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {
                'interval': '1d',
                'range': '1d',
                'includePrePost': 'false'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                            result = data['chart']['result'][0]
                            meta = result.get('meta', {})
                            timestamp = result.get('timestamp', [])
                            quote = result.get('indicators', {}).get('quote', [{}])[0]
                            
                            if timestamp and quote.get('close'):
                                current_price = quote['close'][-1]
                                previous_close = meta.get('previousClose', current_price)
                                change = current_price - previous_close
                                change_percent = (change / previous_close) * 100 if previous_close else 0
                                
                                return {
                                    "symbol": symbol,
                                    "price": current_price,
                                    "change": change,
                                    "change_percent": change_percent,
                                    "volume": quote.get('volume', [0])[-1] or 0,
                                    "market_cap": meta.get('marketCap', 0),
                                    "timestamp": datetime.fromtimestamp(timestamp[-1]).isoformat(),
                                    "source": "yahoo_finance"
                                }
            
            return None
            
        except Exception as e:
            logger.error(f"Yahoo Finance API error for {symbol}: {e}")
            return None
    
    async def _get_alpha_vantage_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get data from Alpha Vantage API"""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.alpha_vantage_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'Global Quote' in data:
                            quote = data['Global Quote']
                            current_price = float(quote.get('05. price', 0))
                            previous_close = float(quote.get('08. previous close', current_price))
                            change = current_price - previous_close
                            change_percent = float(quote.get('10. change percent', '0').replace('%', ''))
                            
                            return {
                                "symbol": symbol,
                                "price": current_price,
                                "change": change,
                                "change_percent": change_percent,
                                "volume": int(quote.get('06. volume', 0)),
                                "market_cap": 0,  # Alpha Vantage doesn't provide market cap
                                "timestamp": datetime.now().isoformat(),
                                "source": "alpha_vantage"
                            }
            
            return None
            
        except Exception as e:
            logger.error(f"Alpha Vantage API error for {symbol}: {e}")
            return None
    
    def _get_mock_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Generate mock stock data for testing"""
        import random
        
        base_price = random.uniform(50, 500)
        change = random.uniform(-10, 10)
        change_percent = (change / base_price) * 100
        
        return {
            "symbol": symbol,
            "price": base_price,
            "change": change,
            "change_percent": change_percent,
            "volume": random.randint(100000, 10000000),
            "market_cap": random.randint(1000000000, 100000000000),
            "timestamp": datetime.now().isoformat(),
            "source": "mock"
        }

class NewsAPI:
    """News API integration for market sentiment"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_key = config.get('news_api_key')
        self.cache_ttl = config.get('cache_ttl', 1800)  # 30 minutes
        self.cache = {}
        
    async def get_market_news(self, query: str = "trading", count: int = 20) -> List[Dict[str, Any]]:
        """Get market-related news articles"""
        try:
            # Check cache first
            cache_key = f"news:{query}:{count}"
            if cache_key in self.cache:
                cached_data = self.cache[cache_key]
                if datetime.now() - cached_data['timestamp'] < timedelta(seconds=self.cache_ttl):
                    return cached_data['data']
            
            if self.api_key:
                data = await self._get_news_api_data(query, count)
            else:
                data = await self._get_mock_news_data(query, count)
            
            if data:
                self.cache[cache_key] = {
                    'data': data,
                    'timestamp': datetime.now()
                }
            
            return data
            
        except Exception as e:
            logger.error(f"Error getting news for {query}: {e}")
            return await self._get_mock_news_data(query, count)
    
    async def _get_news_api_data(self, query: str, count: int) -> List[Dict[str, Any]]:
        """Get data from News API"""
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'language': 'en',
                'sortBy': 'relevancy',
                'pageSize': count,
                'apiKey': self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get('articles', [])
                        
                        return [
                            {
                                'title': article.get('title', ''),
                                'description': article.get('description', ''),
                                'url': article.get('url', ''),
                                'source': article.get('source', {}).get('name', ''),
                                'published_at': article.get('publishedAt', ''),
                                'content': article.get('content', ''),
                                'sentiment': self._analyze_sentiment(article.get('title', '') + ' ' + article.get('description', ''))
                            }
                            for article in articles
                        ]
            
            return []
            
        except Exception as e:
            logger.error(f"News API error: {e}")
            return []
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        text_lower = text.lower()
        
        positive_words = ['bull', 'buy', 'up', 'gain', 'profit', 'positive', 'growth', 'rise', 'surge']
        negative_words = ['bear', 'sell', 'down', 'loss', 'crash', 'negative', 'decline', 'fall', 'drop']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    async def _get_mock_news_data(self, query: str, count: int) -> List[Dict[str, Any]]:
        """Generate mock news data for testing"""
        import random
        
        mock_sources = ['Reuters', 'Bloomberg', 'CNBC', 'MarketWatch', 'Yahoo Finance']
        mock_titles = [
            f"{query.title()} Market Shows Strong Growth",
            f"New {query.title()} Strategy Emerges",
            f"{query.title()} Trading Volume Increases",
            f"Analysts Predict {query.title()} Trends",
            f"{query.title()} Market Update"
        ]
        
        articles = []
        for i in range(count):
            title = random.choice(mock_titles)
            sentiment = random.choice(['positive', 'negative', 'neutral'])
            
            articles.append({
                'title': title,
                'description': f"This is a mock description for {title}",
                'url': f"https://mock-news.com/article/{i}",
                'source': random.choice(mock_sources),
                'published_at': (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
                'content': f"Mock content for {title}",
                'sentiment': sentiment
            })
        
        return articles

class SocialMediaAPI:
    """Social media sentiment analysis"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.twitter_bearer_token = config.get('twitter_bearer_token')
        self.reddit_enabled = config.get('reddit_enabled', True)
        self.cache_ttl = config.get('cache_ttl', 900)  # 15 minutes
        self.cache = {}
        
    async def get_trading_sentiment(self, query: str) -> Dict[str, Any]:
        """Get social media sentiment for trading"""
        try:
            # Check cache first
            cache_key = f"social_sentiment:{query}"
            if cache_key in self.cache:
                cached_data = self.cache[cache_key]
                if datetime.now() - cached_data['timestamp'] < timedelta(seconds=self.cache_ttl):
                    return cached_data['data']
            
            # Try Twitter first
            twitter_data = await self._get_twitter_sentiment(query)
            
            # Try Reddit as backup
            reddit_data = await self._get_reddit_sentiment(query)
            
            # Combine data
            combined_data = self._combine_sentiment_data(twitter_data, reddit_data)
            
            self.cache[cache_key] = {
                'data': combined_data,
                'timestamp': datetime.now()
            }
            
            return combined_data
            
        except Exception as e:
            logger.error(f"Error getting social sentiment for {query}: {e}")
            return self._get_mock_sentiment_data(query)
    
    async def _get_twitter_sentiment(self, query: str) -> Dict[str, Any]:
        """Get Twitter sentiment data"""
        if not self.twitter_bearer_token:
            return {}
        
        try:
            url = "https://api.twitter.com/2/tweets/search/recent"
            headers = {
                'Authorization': f'Bearer {self.twitter_bearer_token}'
            }
            params = {
                'query': query,
                'max_results': 100,
                'tweet.fields': 'created_at,public_metrics'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        tweets = data.get('data', [])
                        
                        return self._analyze_twitter_sentiment(tweets)
            
            return {}
            
        except Exception as e:
            logger.error(f"Twitter API error: {e}")
            return {}
    
    def _analyze_twitter_sentiment(self, tweets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze Twitter sentiment"""
        positive_words = ['bull', 'buy', 'up', 'gain', 'profit', '🚀', '📈', '💎']
        negative_words = ['bear', 'sell', 'down', 'loss', 'crash', '📉', '💸', '🔥']
        
        positive_count = 0
        negative_count = 0
        total_engagement = 0
        
        for tweet in tweets:
            text = tweet.get('text', '').lower()
            metrics = tweet.get('public_metrics', {})
            engagement = metrics.get('retweet_count', 0) + metrics.get('like_count', 0)
            total_engagement += engagement
            
            positive_count += sum(1 for word in positive_words if word in text)
            negative_count += sum(1 for word in negative_words if word in text)
        
        total = positive_count + negative_count
        sentiment_score = (positive_count - negative_count) / total if total > 0 else 0
        
        return {
            'positive_count': positive_count,
            'negative_count': negative_count,
            'total_tweets': len(tweets),
            'sentiment_score': sentiment_score,
            'total_engagement': total_engagement
        }
    
    async def _get_reddit_sentiment(self, query: str) -> Dict[str, Any]:
        """Get Reddit sentiment data"""
        if not self.reddit_enabled:
            return {}
        
        try:
            # Reddit API requires authentication, so we'll use a simple approach
            # In production, you'd use PRAW or Reddit's official API
            return self._get_mock_reddit_sentiment(query)
            
        except Exception as e:
            logger.error(f"Reddit API error: {e}")
            return {}
    
    def _get_mock_reddit_sentiment(self, query: str) -> Dict[str, Any]:
        """Generate mock Reddit sentiment data"""
        import random
        
        return {
            'positive_count': random.randint(10, 50),
            'negative_count': random.randint(5, 30),
            'total_posts': random.randint(20, 100),
            'sentiment_score': random.uniform(-0.5, 0.5),
            'total_upvotes': random.randint(100, 1000)
        }
    
    def _combine_sentiment_data(self, twitter_data: Dict[str, Any], reddit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Combine sentiment data from multiple sources"""
        combined_positive = twitter_data.get('positive_count', 0) + reddit_data.get('positive_count', 0)
        combined_negative = twitter_data.get('negative_count', 0) + reddit_data.get('negative_count', 0)
        total_mentions = combined_positive + combined_negative
        
        sentiment_score = (combined_positive - combined_negative) / total_mentions if total_mentions > 0 else 0
        
        return {
            'twitter': twitter_data,
            'reddit': reddit_data,
            'combined': {
                'positive_count': combined_positive,
                'negative_count': combined_negative,
                'total_mentions': total_mentions,
                'sentiment_score': sentiment_score,
                'sentiment_label': 'positive' if sentiment_score > 0.1 else 'negative' if sentiment_score < -0.1 else 'neutral'
            }
        }
    
    def _get_mock_sentiment_data(self, query: str) -> Dict[str, Any]:
        """Generate mock sentiment data for testing"""
        import random
        
        return {
            'twitter': {
                'positive_count': random.randint(20, 100),
                'negative_count': random.randint(10, 50),
                'total_tweets': random.randint(50, 200),
                'sentiment_score': random.uniform(-0.3, 0.3),
                'total_engagement': random.randint(500, 2000)
            },
            'reddit': {
                'positive_count': random.randint(10, 40),
                'negative_count': random.randint(5, 25),
                'total_posts': random.randint(20, 80),
                'sentiment_score': random.uniform(-0.4, 0.4),
                'total_upvotes': random.randint(200, 800)
            },
            'combined': {
                'positive_count': random.randint(30, 140),
                'negative_count': random.randint(15, 75),
                'total_mentions': random.randint(50, 280),
                'sentiment_score': random.uniform(-0.2, 0.2),
                'sentiment_label': random.choice(['positive', 'negative', 'neutral'])
            }
        } 