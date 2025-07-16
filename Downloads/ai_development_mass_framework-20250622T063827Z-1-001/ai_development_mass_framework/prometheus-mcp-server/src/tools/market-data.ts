/**
 * PROMETHEUS MCP Server - Market Data Tools
 * Tools for retrieving market data, quotes, and analysis
 */

import { logger } from '../utils/logger';
import { cache } from '../utils/cache';
import { MarketQuote, MarketAnalysis, Opportunity, ApiResponse } from '../types';
import axios from 'axios';

export class MarketDataTools {
  private static readonly QUOTE_CACHE_TTL = 5000; // 5 seconds
  private static readonly ANALYSIS_CACHE_TTL = 10000; // 10 seconds

  /**
   * Get real-time quote for a stock symbol
   */
  static async getQuote(params: { symbol: string }): Promise<ApiResponse<MarketQuote>> {
    try {
      const { symbol } = params;
      logger.info('Getting quote', { symbol });

      // Check cache first
      const cacheKey = `quote:${symbol}`;
      const cached = await cache.get<MarketQuote>(cacheKey);
      
      if (cached) {
        logger.info('Quote retrieved from cache', { symbol });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `quote-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get(`/api/v1/market/quote/${symbol}`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const quote: MarketQuote = response.data;
      const latency = Date.now() - startTime;

      // Cache the result
      await cache.set(cacheKey, quote, this.QUOTE_CACHE_TTL);

      logger.info('Quote retrieved successfully', { symbol, latency });

      return {
        success: true,
        data: quote,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `quote-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get quote', { symbol: params.symbol, error });
      return {
        success: false,
        error: {
          code: 'QUOTE_ERROR',
          message: 'Failed to retrieve quote',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get comprehensive market analysis
   */
  static async getMarketAnalysis(params: { 
    symbol: string; 
    timeframe?: string 
  }): Promise<ApiResponse<MarketAnalysis>> {
    try {
      const { symbol, timeframe = '1D' } = params;
      logger.info('Getting market analysis', { symbol, timeframe });

      // Check cache first
      const cacheKey = `analysis:${symbol}:${timeframe}`;
      const cached = await cache.get<MarketAnalysis>(cacheKey);
      
      if (cached) {
        logger.info('Market analysis retrieved from cache', { symbol, timeframe });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `analysis-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get(`/api/v1/market/analysis/${symbol}`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        params: { timeframe },
        timeout: 15000
      });

      const analysis: MarketAnalysis = response.data;
      const latency = Date.now() - startTime;

      // Cache the result
      await cache.set(cacheKey, analysis, this.ANALYSIS_CACHE_TTL);

      logger.info('Market analysis retrieved successfully', { symbol, timeframe, latency });

      return {
        success: true,
        data: analysis,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `analysis-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get market analysis', { symbol: params.symbol, error });
      return {
        success: false,
        error: {
          code: 'ANALYSIS_ERROR',
          message: 'Failed to retrieve market analysis',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Search for trading opportunities
   */
  static async findOpportunities(params: {
    sector?: string;
    minVolume?: number;
    priceRange?: [number, number];
    technicalSetup?: string;
    limit?: number;
  }): Promise<ApiResponse<Opportunity[]>> {
    try {
      const { sector, minVolume, priceRange, technicalSetup, limit = 10 } = params;
      logger.info('Finding trading opportunities', { 
        sector, 
        minVolume, 
        priceRange, 
        technicalSetup, 
        limit 
      });

      // Build query parameters
      const queryParams: Record<string, any> = { limit };
      if (sector) queryParams.sector = sector;
      if (minVolume) queryParams.minVolume = minVolume;
      if (priceRange) {
        queryParams.minPrice = priceRange[0];
        queryParams.maxPrice = priceRange[1];
      }
      if (technicalSetup) queryParams.technicalSetup = technicalSetup;

      // Check cache first
      const cacheKey = `opportunities:${JSON.stringify(queryParams)}`;
      const cached = await cache.get<Opportunity[]>(cacheKey);
      
      if (cached) {
        logger.info('Opportunities retrieved from cache', { count: cached.length });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `opportunities-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get('/api/v1/market/opportunities', {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        params: queryParams,
        timeout: 15000
      });

      const opportunities: Opportunity[] = response.data;
      const latency = Date.now() - startTime;

      // Cache the result for 5 minutes
      await cache.set(cacheKey, opportunities, 300000);

      logger.info('Opportunities retrieved successfully', { 
        count: opportunities.length, 
        latency 
      });

      return {
        success: true,
        data: opportunities,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `opportunities-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to find opportunities', { params, error });
      return {
        success: false,
        error: {
          code: 'OPPORTUNITIES_ERROR',
          message: 'Failed to find trading opportunities',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get multiple quotes at once
   */
  static async getMultipleQuotes(params: { symbols: string[] }): Promise<ApiResponse<MarketQuote[]>> {
    try {
      const { symbols } = params;
      logger.info('Getting multiple quotes', { symbols, count: symbols.length });

      // Check cache for each symbol
      const cacheKeys = symbols.map(symbol => `quote:${symbol}`);
      const cachedQuotes = await cache.mget<MarketQuote>(cacheKeys);
      
      const quotesToFetch: string[] = [];
      const results: MarketQuote[] = [];

      symbols.forEach((symbol, index) => {
        const cached = cachedQuotes[index];
        if (cached) {
          results.push(cached);
        } else {
          quotesToFetch.push(symbol);
        }
      });

      // Fetch missing quotes
      if (quotesToFetch.length > 0) {
        const startTime = Date.now();
        const response = await axios.post('/api/v1/market/quotes', {
          symbols: quotesToFetch
        }, {
          baseURL: process.env.PROMETHEUS_API_BASE_URL,
          headers: {
            'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
            'Content-Type': 'application/json'
          },
          timeout: 10000
        });

        const freshQuotes: MarketQuote[] = response.data;
        const latency = Date.now() - startTime;

        // Cache fresh quotes
        const cachePromises = freshQuotes.map(quote => 
          cache.set(`quote:${quote.symbol}`, quote, this.QUOTE_CACHE_TTL)
        );
        await Promise.all(cachePromises);

        results.push(...freshQuotes);

        logger.info('Multiple quotes retrieved successfully', { 
          cached: cachedQuotes.filter(q => q !== null).length,
          fetched: freshQuotes.length,
          latency
        });
      }

      return {
        success: true,
        data: results,
        metadata: {
          timestamp: new Date().toISOString(),
          latency: 0,
          cache: quotesToFetch.length === 0,
          requestId: `multi-quotes-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get multiple quotes', { symbols: params.symbols, error });
      return {
        success: false,
        error: {
          code: 'MULTI_QUOTES_ERROR',
          message: 'Failed to retrieve multiple quotes',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get market summary and overview
   */
  static async getMarketSummary(): Promise<ApiResponse<{
    indices: MarketQuote[];
    sectors: Array<{
      name: string;
      change: number;
      changePercent: number;
      topGainers: MarketQuote[];
      topLosers: MarketQuote[];
    }>;
    marketStatus: 'OPEN' | 'CLOSED' | 'PRE_MARKET' | 'AFTER_HOURS';
    mostActive: MarketQuote[];
    gainers: MarketQuote[];
    losers: MarketQuote[];
  }>> {
    try {
      logger.info('Getting market summary');

      // Check cache first
      const cacheKey = 'market:summary';
      const cached = await cache.get<any>(cacheKey);
      
      if (cached) {
        logger.info('Market summary retrieved from cache');
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `market-summary-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get('/api/v1/market/summary', {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });

      const summary = response.data;
      const latency = Date.now() - startTime;

      // Cache the result for 1 minute
      await cache.set(cacheKey, summary, 60000);

      logger.info('Market summary retrieved successfully', { latency });

      return {
        success: true,
        data: summary,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `market-summary-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get market summary', { error });
      return {
        success: false,
        error: {
          code: 'MARKET_SUMMARY_ERROR',
          message: 'Failed to retrieve market summary',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get historical data for a symbol
   */
  static async getHistoricalData(params: {
    symbol: string;
    period: '1d' | '5d' | '1mo' | '3mo' | '6mo' | '1y' | '2y' | '5y' | '10y' | 'ytd' | 'max';
    interval?: '1m' | '2m' | '5m' | '15m' | '30m' | '60m' | '90m' | '1h' | '1d' | '5d' | '1wk' | '1mo' | '3mo';
  }): Promise<ApiResponse<{
    symbol: string;
    period: string;
    interval: string;
    data: Array<{
      timestamp: string;
      open: number;
      high: number;
      low: number;
      close: number;
      volume: number;
    }>;
  }>> {
    try {
      const { symbol, period, interval = '1d' } = params;
      logger.info('Getting historical data', { symbol, period, interval });

      // Check cache first
      const cacheKey = `historical:${symbol}:${period}:${interval}`;
      const cached = await cache.get<any>(cacheKey);
      
      if (cached) {
        logger.info('Historical data retrieved from cache', { symbol, period, interval });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `historical-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get(`/api/v1/market/historical/${symbol}`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        params: { period, interval },
        timeout: 15000
      });

      const historicalData = response.data;
      const latency = Date.now() - startTime;

      // Cache the result (longer cache for historical data)
      const cacheTTL = interval === '1d' ? 3600000 : 300000; // 1 hour for daily, 5 minutes for intraday
      await cache.set(cacheKey, historicalData, cacheTTL);

      logger.info('Historical data retrieved successfully', { 
        symbol, 
        period, 
        interval, 
        dataPoints: historicalData.data.length,
        latency 
      });

      return {
        success: true,
        data: historicalData,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `historical-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get historical data', { symbol: params.symbol, error });
      return {
        success: false,
        error: {
          code: 'HISTORICAL_DATA_ERROR',
          message: 'Failed to retrieve historical data',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }
}
