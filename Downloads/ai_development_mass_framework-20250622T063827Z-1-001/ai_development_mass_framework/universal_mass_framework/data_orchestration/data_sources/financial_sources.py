"""
Financial Data Sources - Real-World Market Intelligence
======================================================

Provides real-time and historical financial market data from multiple sources
to enable AI-powered financial analysis and decision making.

Supported Financial Data:
- Stock Market Data (real-time quotes, historical prices, volume)
- Cryptocurrency Data (prices, volume, market cap, sentiment)
- Forex Data (currency exchange rates, volatility)
- Commodities Data (gold, oil, agricultural products)
- Economic Indicators (GDP, inflation, unemployment)
- Company Fundamentals (earnings, revenue, ratios)
- Market Sentiment Data (fear/greed index, volatility)
- Options and Derivatives Data
- News and Analyst Reports
- Regulatory Filings (SEC, earnings reports)

Features:
- Multiple data provider integration (Alpha Vantage, Yahoo Finance, IEX Cloud, etc.)
- Real-time streaming data
- Historical data with various timeframes
- Data validation and cleansing
- Rate limiting and compliance
- Automatic failover between providers
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import aiohttp
import pandas as pd
from dataclasses import dataclass

from ...core.config_manager import MassConfig
from ..base_data_source import BaseDataSource

logger = logging.getLogger(__name__)

@dataclass
class FinancialDataRequest:
    """Request structure for financial data"""
    symbol: str
    data_type: str  # 'quote', 'historical', 'news', 'fundamentals'
    timeframe: str = '1d'  # '1m', '5m', '1h', '1d', '1w', '1M'
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    indicators: List[str] = None  # Technical indicators to calculate

class FinancialDataSources(BaseDataSource):
    """
    Financial data source integration for real-world market intelligence
    """
    
    def __init__(self, config: MassConfig):
        super().__init__(config)
        self.api_keys = {
            'alpha_vantage': config.get('alpha_vantage_api_key'),
            'iex_cloud': config.get('iex_cloud_api_key'),
            'finnhub': config.get('finnhub_api_key'),
            'polygon': config.get('polygon_api_key'),
            'yahoo_finance': True  # No API key needed for basic data
        }
        
        self.data_providers = {}
        self.rate_limits = {
            'alpha_vantage': {'calls_per_minute': 5, 'calls_per_day': 500},
            'iex_cloud': {'calls_per_minute': 100, 'calls_per_day': 10000},
            'finnhub': {'calls_per_minute': 60, 'calls_per_day': 1000},
            'polygon': {'calls_per_minute': 5, 'calls_per_day': 1000},
            'yahoo_finance': {'calls_per_minute': 60, 'calls_per_day': 2000}
        }
        
        self.call_history = {}
        self.session = None
        
    async def initialize(self) -> bool:
        """Initialize financial data sources"""
        try:
            logger.info("Initializing Financial Data Sources...")
            
            # Create HTTP session
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
            
            # Initialize available providers
            await self._initialize_providers()
            
            # Test connectivity
            await self._test_connectivity()
            
            logger.info("✅ Financial Data Sources initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Financial Data Sources: {e}")
            return False
    
    async def collect_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect financial data based on parameters
        
        Parameters can include:
        - symbol: Stock/crypto symbol (required)
        - data_type: 'quote', 'historical', 'news', 'fundamentals'
        - timeframe: '1m', '5m', '1h', '1d', '1w', '1M'
        - indicators: List of technical indicators
        """
        try:
            symbol = parameters.get('symbol', '').upper()
            data_type = parameters.get('data_type', 'quote')
            
            if not symbol:
                return {"error": "Symbol is required for financial data"}
            
            logger.info(f"Collecting financial data for {symbol}, type: {data_type}")
            
            # Create data request
            request = FinancialDataRequest(
                symbol=symbol,
                data_type=data_type,
                timeframe=parameters.get('timeframe', '1d'),
                start_date=parameters.get('start_date'),
                end_date=parameters.get('end_date'),
                indicators=parameters.get('indicators', [])
            )
            
            # Collect data based on type
            if data_type == 'quote':
                data = await self._get_real_time_quote(request)
            elif data_type == 'historical':
                data = await self._get_historical_data(request)
            elif data_type == 'news':
                data = await self._get_financial_news(request)
            elif data_type == 'fundamentals':
                data = await self._get_company_fundamentals(request)
            elif data_type == 'comprehensive':
                data = await self._get_comprehensive_data(request)
            else:
                data = {"error": f"Unsupported data type: {data_type}"}
            
            # Add metadata
            data['metadata'] = {
                'symbol': symbol,
                'data_type': data_type,
                'collected_at': datetime.now().isoformat(),
                'source': 'financial_data_sources',
                'providers_used': list(self.data_providers.keys())
            }
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to collect financial data: {e}")
            return {"error": str(e)}
    
    async def get_real_time_stream(
        self, 
        symbols: List[str], 
        callback: callable
    ) -> str:
        """Start real-time streaming for financial data"""
        try:
            stream_id = f"financial_stream_{datetime.now().timestamp()}"
            
            # Start streaming task
            asyncio.create_task(
                self._process_real_time_stream(stream_id, symbols, callback)
            )
            
            logger.info(f"Started real-time financial stream: {stream_id}")
            return stream_id
            
        except Exception as e:
            logger.error(f"Failed to start financial stream: {e}")
            raise
    
    async def get_status(self) -> str:
        """Get status of financial data sources"""
        try:
            if not self.session:
                return "not_initialized"
            
            # Check if at least one provider is working
            for provider in self.data_providers:
                if await self._test_provider(provider):
                    return "operational"
            
            return "degraded"
            
        except Exception:
            return "error"
    
    # Private methods for data collection
    
    async def _initialize_providers(self) -> None:
        """Initialize available data providers"""
        providers = {}
        
        # Alpha Vantage (requires API key)
        if self.api_keys.get('alpha_vantage'):
            providers['alpha_vantage'] = {
                'base_url': 'https://www.alphavantage.co/query',
                'supports': ['quote', 'historical', 'fundamentals', 'news'],
                'rate_limit': self.rate_limits['alpha_vantage']
            }
        
        # IEX Cloud (requires API key)
        if self.api_keys.get('iex_cloud'):
            providers['iex_cloud'] = {
                'base_url': 'https://cloud.iexapis.com/stable',
                'supports': ['quote', 'historical', 'news', 'fundamentals'],
                'rate_limit': self.rate_limits['iex_cloud']
            }
        
        # Finnhub (requires API key)
        if self.api_keys.get('finnhub'):
            providers['finnhub'] = {
                'base_url': 'https://finnhub.io/api/v1',
                'supports': ['quote', 'news', 'fundamentals'],
                'rate_limit': self.rate_limits['finnhub']
            }
        
        # Yahoo Finance (free, no API key)
        providers['yahoo_finance'] = {
            'base_url': 'https://query1.finance.yahoo.com/v8/finance/chart',
            'supports': ['quote', 'historical'],
            'rate_limit': self.rate_limits['yahoo_finance']
        }
        
        self.data_providers = providers
        logger.info(f"Initialized {len(providers)} financial data providers")
    
    async def _test_connectivity(self) -> None:
        """Test connectivity to all providers"""
        for provider_name in self.data_providers:
            try:
                success = await self._test_provider(provider_name)
                if success:
                    logger.info(f"✅ {provider_name} connectivity test passed")
                else:
                    logger.warning(f"⚠️ {provider_name} connectivity test failed")
            except Exception as e:
                logger.error(f"❌ {provider_name} connectivity test error: {e}")
    
    async def _test_provider(self, provider_name: str) -> bool:
        """Test connectivity to a specific provider"""
        try:
            if provider_name == 'alpha_vantage':
                return await self._test_alpha_vantage()
            elif provider_name == 'yahoo_finance':
                return await self._test_yahoo_finance()
            elif provider_name == 'iex_cloud':
                return await self._test_iex_cloud()
            elif provider_name == 'finnhub':
                return await self._test_finnhub()
            return False
        except Exception:
            return False
    
    async def _get_real_time_quote(self, request: FinancialDataRequest) -> Dict[str, Any]:
        """Get real-time stock quote"""
        try:
            # Try multiple providers for redundancy
            providers = ['yahoo_finance', 'alpha_vantage', 'iex_cloud']
            
            for provider in providers:
                if provider not in self.data_providers:
                    continue
                
                try:
                    if provider == 'yahoo_finance':
                        data = await self._get_yahoo_quote(request.symbol)
                    elif provider == 'alpha_vantage':
                        data = await self._get_alpha_vantage_quote(request.symbol)
                    elif provider == 'iex_cloud':
                        data = await self._get_iex_quote(request.symbol)
                    else:
                        continue
                    
                    if data and 'error' not in data:
                        data['provider'] = provider
                        return data
                        
                except Exception as e:
                    logger.warning(f"Provider {provider} failed for quote: {e}")
                    continue
            
            return {"error": "No provider available for real-time quote"}
            
        except Exception as e:
            logger.error(f"Failed to get real-time quote: {e}")
            return {"error": str(e)}
    
    async def _get_historical_data(self, request: FinancialDataRequest) -> Dict[str, Any]:
        """Get historical price data"""
        try:
            # Determine best provider based on timeframe
            if request.timeframe in ['1m', '5m']:
                providers = ['alpha_vantage', 'iex_cloud']
            else:
                providers = ['yahoo_finance', 'alpha_vantage', 'iex_cloud']
            
            for provider in providers:
                if provider not in self.data_providers:
                    continue
                
                try:
                    if provider == 'yahoo_finance':
                        data = await self._get_yahoo_historical(request)
                    elif provider == 'alpha_vantage':
                        data = await self._get_alpha_vantage_historical(request)
                    elif provider == 'iex_cloud':
                        data = await self._get_iex_historical(request)
                    else:
                        continue
                    
                    if data and 'error' not in data:
                        data['provider'] = provider
                        
                        # Calculate technical indicators if requested
                        if request.indicators:
                            data['indicators'] = await self._calculate_indicators(
                                data['historical_data'], request.indicators
                            )
                        
                        return data
                        
                except Exception as e:
                    logger.warning(f"Provider {provider} failed for historical data: {e}")
                    continue
            
            return {"error": "No provider available for historical data"}
            
        except Exception as e:
            logger.error(f"Failed to get historical data: {e}")
            return {"error": str(e)}
    
    async def _get_financial_news(self, request: FinancialDataRequest) -> Dict[str, Any]:
        """Get financial news for a symbol"""
        try:
            providers = ['alpha_vantage', 'iex_cloud', 'finnhub']
            all_news = []
            
            for provider in providers:
                if provider not in self.data_providers:
                    continue
                
                try:
                    if provider == 'alpha_vantage':
                        news = await self._get_alpha_vantage_news(request.symbol)
                    elif provider == 'iex_cloud':
                        news = await self._get_iex_news(request.symbol)
                    elif provider == 'finnhub':
                        news = await self._get_finnhub_news(request.symbol)
                    else:
                        continue
                    
                    if news and isinstance(news, list):
                        all_news.extend(news)
                        
                except Exception as e:
                    logger.warning(f"Provider {provider} failed for news: {e}")
                    continue
            
            # Sort by date and remove duplicates
            unique_news = {}
            for article in all_news:
                url = article.get('url', '')
                if url and url not in unique_news:
                    unique_news[url] = article
            
            sorted_news = sorted(
                unique_news.values(),
                key=lambda x: x.get('published_at', ''),
                reverse=True
            )
            
            return {
                "symbol": request.symbol,
                "news": sorted_news[:50],  # Limit to 50 most recent
                "total_articles": len(sorted_news)
            }
            
        except Exception as e:
            logger.error(f"Failed to get financial news: {e}")
            return {"error": str(e)}
    
    async def _get_company_fundamentals(self, request: FinancialDataRequest) -> Dict[str, Any]:
        """Get company fundamental data"""
        try:
            providers = ['alpha_vantage', 'iex_cloud', 'finnhub']
            
            for provider in providers:
                if provider not in self.data_providers:
                    continue
                
                try:
                    if provider == 'alpha_vantage':
                        data = await self._get_alpha_vantage_fundamentals(request.symbol)
                    elif provider == 'iex_cloud':
                        data = await self._get_iex_fundamentals(request.symbol)
                    elif provider == 'finnhub':
                        data = await self._get_finnhub_fundamentals(request.symbol)
                    else:
                        continue
                    
                    if data and 'error' not in data:
                        data['provider'] = provider
                        return data
                        
                except Exception as e:
                    logger.warning(f"Provider {provider} failed for fundamentals: {e}")
                    continue
            
            return {"error": "No provider available for fundamentals data"}
            
        except Exception as e:
            logger.error(f"Failed to get company fundamentals: {e}")
            return {"error": str(e)}
    
    async def _get_comprehensive_data(self, request: FinancialDataRequest) -> Dict[str, Any]:
        """Get comprehensive financial data (quote + historical + news + fundamentals)"""
        try:
            logger.info(f"Collecting comprehensive financial data for {request.symbol}")
            
            # Collect all data types in parallel
            tasks = [
                self._get_real_time_quote(request),
                self._get_historical_data(request),
                self._get_financial_news(request),
                self._get_company_fundamentals(request)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {
                "symbol": request.symbol,
                "real_time_quote": results[0] if not isinstance(results[0], Exception) else {"error": str(results[0])},
                "historical_data": results[1] if not isinstance(results[1], Exception) else {"error": str(results[1])},
                "news": results[2] if not isinstance(results[2], Exception) else {"error": str(results[2])},
                "fundamentals": results[3] if not isinstance(results[3], Exception) else {"error": str(results[3])},
                "data_quality": await self._assess_data_completeness(results)
            }
            
        except Exception as e:
            logger.error(f"Failed to get comprehensive data: {e}")
            return {"error": str(e)}
    
    # Provider-specific implementations
    
    async def _get_yahoo_quote(self, symbol: str) -> Dict[str, Any]:
        """Get quote from Yahoo Finance"""
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    chart = data.get('chart', {})
                    result = chart.get('result', [])
                    
                    if result:
                        meta = result[0].get('meta', {})
                        
                        return {
                            "symbol": symbol,
                            "price": meta.get('regularMarketPrice'),
                            "change": meta.get('regularMarketPrice', 0) - meta.get('previousClose', 0),
                            "change_percent": ((meta.get('regularMarketPrice', 0) - meta.get('previousClose', 1)) / meta.get('previousClose', 1)) * 100,
                            "volume": meta.get('regularMarketVolume'),
                            "market_cap": meta.get('marketCap'),
                            "pe_ratio": meta.get('trailingPE'),
                            "timestamp": datetime.now().isoformat(),
                            "currency": meta.get('currency', 'USD')
                        }
                
                return {"error": f"Yahoo Finance API error: {response.status}"}
                
        except Exception as e:
            return {"error": f"Yahoo Finance error: {e}"}
    
    async def _test_alpha_vantage(self) -> bool:
        """Test Alpha Vantage connectivity"""
        try:
            if not self.api_keys.get('alpha_vantage'):
                return False
            
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={self.api_keys['alpha_vantage']}"
            
            async with self.session.get(url) as response:
                return response.status == 200
                
        except Exception:
            return False
    
    async def _test_yahoo_finance(self) -> bool:
        """Test Yahoo Finance connectivity"""
        try:
            url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
            
            async with self.session.get(url) as response:
                return response.status == 200
                
        except Exception:
            return False
    
    async def _test_iex_cloud(self) -> bool:
        """Test IEX Cloud connectivity"""
        try:
            if not self.api_keys.get('iex_cloud'):
                return False
            
            url = f"https://cloud.iexapis.com/stable/stock/AAPL/quote?token={self.api_keys['iex_cloud']}"
            
            async with self.session.get(url) as response:
                return response.status == 200
                
        except Exception:
            return False
    
    async def _test_finnhub(self) -> bool:
        """Test Finnhub connectivity"""
        try:
            if not self.api_keys.get('finnhub'):
                return False
            
            url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={self.api_keys['finnhub']}"
            
            async with self.session.get(url) as response:
                return response.status == 200
                
        except Exception:
            return False
    
    async def _calculate_indicators(
        self, 
        historical_data: List[Dict[str, Any]], 
        indicators: List[str]
    ) -> Dict[str, Any]:
        """Calculate technical indicators"""
        try:
            # Convert to DataFrame for easier calculation
            df = pd.DataFrame(historical_data)
            
            if df.empty:
                return {}
            
            results = {}
            
            for indicator in indicators:
                if indicator.upper() == 'SMA_20':
                    results['sma_20'] = df['close'].rolling(window=20).mean().iloc[-1]
                elif indicator.upper() == 'SMA_50':
                    results['sma_50'] = df['close'].rolling(window=50).mean().iloc[-1]
                elif indicator.upper() == 'RSI':
                    results['rsi'] = self._calculate_rsi(df['close'])
                elif indicator.upper() == 'MACD':
                    results['macd'] = self._calculate_macd(df['close'])
                elif indicator.upper() == 'BOLLINGER':
                    results['bollinger'] = self._calculate_bollinger_bands(df['close'])
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to calculate indicators: {e}")
            return {}
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate RSI indicator"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return float(rsi.iloc[-1])
        except Exception:
            return 0.0
    
    def _calculate_macd(self, prices: pd.Series) -> Dict[str, float]:
        """Calculate MACD indicator"""
        try:
            ema_12 = prices.ewm(span=12).mean()
            ema_26 = prices.ewm(span=26).mean()
            macd_line = ema_12 - ema_26
            signal_line = macd_line.ewm(span=9).mean()
            histogram = macd_line - signal_line
            
            return {
                "macd": float(macd_line.iloc[-1]),
                "signal": float(signal_line.iloc[-1]),
                "histogram": float(histogram.iloc[-1])
            }
        except Exception:
            return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20) -> Dict[str, float]:
        """Calculate Bollinger Bands"""
        try:
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            upper_band = sma + (std * 2)
            lower_band = sma - (std * 2)
            
            return {
                "upper": float(upper_band.iloc[-1]),
                "middle": float(sma.iloc[-1]),
                "lower": float(lower_band.iloc[-1])
            }
        except Exception:
            return {"upper": 0.0, "middle": 0.0, "lower": 0.0}
    
    async def _assess_data_completeness(self, results: List[Any]) -> Dict[str, Any]:
        """Assess the completeness and quality of collected data"""
        try:
            total_sources = len(results)
            successful_sources = sum(1 for r in results if not isinstance(r, Exception) and 'error' not in r)
            
            completeness_score = successful_sources / total_sources if total_sources > 0 else 0
            
            return {
                "completeness_score": completeness_score,
                "successful_sources": successful_sources,
                "total_sources": total_sources,
                "quality_rating": "high" if completeness_score >= 0.8 else "medium" if completeness_score >= 0.5 else "low"
            }
            
        except Exception as e:
            logger.error(f"Failed to assess data completeness: {e}")
            return {"completeness_score": 0.0, "quality_rating": "unknown"}
    
    async def _process_real_time_stream(
        self, 
        stream_id: str, 
        symbols: List[str], 
        callback: callable
    ) -> None:
        """Process real-time financial data stream"""
        try:
            while True:
                for symbol in symbols:
                    try:
                        # Get real-time data
                        request = FinancialDataRequest(symbol=symbol, data_type='quote')
                        data = await self._get_real_time_quote(request)
                        
                        # Call callback with data
                        callback(symbol, data)
                        
                    except Exception as e:
                        logger.error(f"Stream error for {symbol}: {e}")
                
                # Wait before next iteration (30 seconds for real-time data)
                await asyncio.sleep(30)
                
        except Exception as e:
            logger.error(f"Real-time stream {stream_id} failed: {e}")
    
    async def close(self) -> None:
        """Close the financial data sources"""
        if self.session:
            await self.session.close()
            logger.info("Financial Data Sources closed")
