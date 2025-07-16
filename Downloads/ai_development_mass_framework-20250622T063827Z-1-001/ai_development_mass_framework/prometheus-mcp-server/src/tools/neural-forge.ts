/**
 * PROMETHEUS MCP Server - Neural Forge AI Tools
 * Tools for AI predictions, strategy analysis, and market insights
 */

import { logger } from '../utils/logger';
import { cache } from '../utils/cache';
import { 
  NeuralForgePrediction, 
  StrategyAnalysis, 
  AIInsight, 
  ApiResponse 
} from '../types';
import axios from 'axios';

export class NeuralForgeTools {
  private static readonly PREDICTION_CACHE_TTL = 300000; // 5 minutes
  private static readonly INSIGHTS_CACHE_TTL = 600000; // 10 minutes

  /**
   * Get AI predictions from Neural Forge
   */
  static async getPrediction(params: {
    symbol: string;
    timeframe: string;
  }): Promise<ApiResponse<NeuralForgePrediction>> {
    try {
      const { symbol, timeframe } = params;
      logger.info('Getting Neural Forge prediction', { symbol, timeframe });

      // Check cache first
      const cacheKey = `prediction:${symbol}:${timeframe}`;
      const cached = await cache.get<NeuralForgePrediction>(cacheKey);
      
      if (cached) {
        logger.info('Neural Forge prediction retrieved from cache', { symbol, timeframe });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `prediction-${Date.now()}`
          }
        };
      }

      // Fetch from Neural Forge API
      const startTime = Date.now();
      const response = await axios.post('/api/v1/neural-forge/predict', {
        symbol,
        timeframe,
        features: ['price', 'volume', 'sentiment', 'technical_indicators'],
        modelVersion: 'latest'
      }, {
        baseURL: process.env.NEURAL_FORGE_ENDPOINT || 'https://neural-forge.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.NEURAL_FORGE_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });

      const prediction: NeuralForgePrediction = {
        symbol,
        direction: response.data.direction,
        confidence: response.data.confidence,
        priceTarget: response.data.priceTarget,
        timeframe,
        supportLevels: response.data.supportLevels || [],
        resistanceLevels: response.data.resistanceLevels || [],
        keyFactors: response.data.keyFactors || [],
        modelVersion: response.data.modelVersion || 'v1.0',
        timestamp: new Date().toISOString()
      };

      const latency = Date.now() - startTime;

      // Cache the result
      await cache.set(cacheKey, prediction, this.PREDICTION_CACHE_TTL);

      // Log Neural Forge usage
      logger.logNeuralForge(
        symbol,
        prediction.direction,
        prediction.confidence * 100
      );

      logger.info('Neural Forge prediction retrieved successfully', { 
        symbol, 
        timeframe,
        direction: prediction.direction,
        confidence: prediction.confidence,
        latency 
      });

      return {
        success: true,
        data: prediction,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `prediction-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get Neural Forge prediction', { params, error });
      return {
        success: false,
        error: {
          code: 'NEURAL_FORGE_ERROR',
          message: 'Failed to get AI prediction',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Analyze trading strategy with AI
   */
  static async analyzeStrategy(params: {
    strategy: string;
    symbols: string[];
    backtest?: boolean;
  }): Promise<ApiResponse<StrategyAnalysis>> {
    try {
      const { strategy, symbols, backtest = false } = params;
      logger.info('Analyzing strategy with Neural Forge', { strategy, symbols, backtest });

      // Check cache first
      const cacheKey = `strategy:${Buffer.from(JSON.stringify(params)).toString('base64')}`;
      const cached = await cache.get<StrategyAnalysis>(cacheKey);
      
      if (cached) {
        logger.info('Strategy analysis retrieved from cache', { strategy });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `strategy-${Date.now()}`
          }
        };
      }

      // Analyze with Neural Forge
      const startTime = Date.now();
      const response = await axios.post('/api/v1/neural-forge/analyze-strategy', {
        strategy,
        symbols,
        backtest,
        analysisType: 'comprehensive',
        includeRiskMetrics: true,
        includeOptimization: true
      }, {
        baseURL: process.env.NEURAL_FORGE_ENDPOINT || 'https://neural-forge.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.NEURAL_FORGE_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 30000 // Strategy analysis can take longer
      });

      const analysis: StrategyAnalysis = {
        strategyName: strategy,
        symbols,
        backtestResults: backtest ? response.data.backtestResults : undefined,
        optimization: response.data.optimization || {
          parameters: {},
          score: 0,
          recommendations: []
        },
        riskAnalysis: response.data.riskAnalysis || {
          expectedDrawdown: 0,
          correlation: 0,
          volatility: 0
        },
        timestamp: new Date().toISOString()
      };

      const latency = Date.now() - startTime;

      // Cache the result (longer cache for strategy analysis)
      await cache.set(cacheKey, analysis, this.PREDICTION_CACHE_TTL * 2);

      logger.info('Strategy analysis completed successfully', { 
        strategy,
        symbols: symbols.length,
        score: analysis.optimization.score,
        latency 
      });

      return {
        success: true,
        data: analysis,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `strategy-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to analyze strategy', { params, error });
      return {
        success: false,
        error: {
          code: 'STRATEGY_ANALYSIS_ERROR',
          message: 'Failed to analyze trading strategy',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get AI market insights and suggestions
   */
  static async getInsights(params: {
    userId: string;
  }): Promise<ApiResponse<{
    marketOverview: string;
    topOpportunities: Array<{
      symbol: string;
      recommendation: 'BUY' | 'SELL' | 'HOLD';
      confidence: number;
      reasoning: string;
    }>;
    riskAlerts: AIInsight[];
    suggestions: string[];
    personalizedInsights: string[];
  }>> {
    try {
      const { userId } = params;
      logger.info('Getting AI insights', { userId });

      // Check cache first
      const cacheKey = `insights:${userId}`;
      const cached = await cache.get<any>(cacheKey);
      
      if (cached) {
        logger.info('AI insights retrieved from cache', { userId });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `insights-${Date.now()}`
          }
        };
      }

      // Get user's portfolio for personalized insights
      const portfolioResponse = await axios.get(`/api/v1/portfolio/${userId}`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const portfolio = portfolioResponse.data;

      // Get insights from Neural Forge
      const startTime = Date.now();
      const response = await axios.post('/api/v1/neural-forge/insights', {
        userId,
        portfolio,
        includeMarketOverview: true,
        includeOpportunities: true,
        includeRiskAlerts: true,
        includeSuggestions: true,
        personalizeForUser: true
      }, {
        baseURL: process.env.NEURAL_FORGE_ENDPOINT || 'https://neural-forge.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.NEURAL_FORGE_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 20000
      });

      const insights = {
        marketOverview: response.data.marketOverview || 'Market analysis unavailable',
        topOpportunities: response.data.topOpportunities || [],
        riskAlerts: response.data.riskAlerts || [],
        suggestions: response.data.suggestions || [],
        personalizedInsights: response.data.personalizedInsights || []
      };

      const latency = Date.now() - startTime;

      // Cache the result
      await cache.set(cacheKey, insights, this.INSIGHTS_CACHE_TTL);

      logger.info('AI insights retrieved successfully', { 
        userId,
        opportunitiesCount: insights.topOpportunities.length,
        alertsCount: insights.riskAlerts.length,
        latency 
      });

      return {
        success: true,
        data: insights,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `insights-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get AI insights', { params, error });
      return {
        success: false,
        error: {
          code: 'INSIGHTS_ERROR',
          message: 'Failed to get AI insights',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get sentiment analysis for a symbol
   */
  static async getSentimentAnalysis(params: {
    symbol: string;
    sources?: string[];
  }): Promise<ApiResponse<{
    symbol: string;
    overallSentiment: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
    sentimentScore: number; // -1 to 1
    sources: {
      news: { sentiment: number; confidence: number; articles: number };
      social: { sentiment: number; confidence: number; mentions: number };
      options: { sentiment: number; confidence: number; putCallRatio: number };
      insider: { sentiment: number; confidence: number; transactions: number };
    };
    keyTopics: string[];
    timeframe: string;
  }>> {
    try {
      const { symbol, sources = ['news', 'social', 'options', 'insider'] } = params;
      logger.info('Getting sentiment analysis', { symbol, sources });

      // Check cache first
      const cacheKey = `sentiment:${symbol}:${sources.join(',')}`;
      const cached = await cache.get<any>(cacheKey);
      
      if (cached) {
        logger.info('Sentiment analysis retrieved from cache', { symbol });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `sentiment-${Date.now()}`
          }
        };
      }

      // Get sentiment from Neural Forge
      const startTime = Date.now();
      const response = await axios.post('/api/v1/neural-forge/sentiment', {
        symbol,
        sources,
        timeframe: '24h',
        includeTopics: true,
        aggregateScore: true
      }, {
        baseURL: process.env.NEURAL_FORGE_ENDPOINT || 'https://neural-forge.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.NEURAL_FORGE_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });

      const sentiment = {
        symbol,
        overallSentiment: response.data.overallSentiment || 'NEUTRAL',
        sentimentScore: response.data.sentimentScore || 0,
        sources: response.data.sources || {},
        keyTopics: response.data.keyTopics || [],
        timeframe: response.data.timeframe || '24h'
      };

      const latency = Date.now() - startTime;

      // Cache the result
      await cache.set(cacheKey, sentiment, 300000); // 5 minutes cache

      logger.info('Sentiment analysis retrieved successfully', { 
        symbol,
        sentiment: sentiment.overallSentiment,
        score: sentiment.sentimentScore,
        latency 
      });

      return {
        success: true,
        data: sentiment,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `sentiment-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get sentiment analysis', { params, error });
      return {
        success: false,
        error: {
          code: 'SENTIMENT_ERROR',
          message: 'Failed to get sentiment analysis',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get market regime analysis
   */
  static async getMarketRegime(): Promise<ApiResponse<{
    regime: 'BULL_MARKET' | 'BEAR_MARKET' | 'SIDEWAYS' | 'VOLATILE' | 'TRANSITIONAL';
    confidence: number;
    indicators: {
      trend: number; // -1 to 1
      volatility: number; // 0 to 1
      momentum: number; // -1 to 1
      breadth: number; // -1 to 1
    };
    characteristics: string[];
    tradingGuidance: string[];
    duration: string;
    probabilityMatrix: {
      nextRegime: string;
      probability: number;
    }[];
  }>> {
    try {
      logger.info('Getting market regime analysis');

      // Check cache first
      const cacheKey = 'market:regime';
      const cached = await cache.get<any>(cacheKey);
      
      if (cached) {
        logger.info('Market regime analysis retrieved from cache');
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `regime-${Date.now()}`
          }
        };
      }

      // Get regime analysis from Neural Forge
      const startTime = Date.now();
      const response = await axios.post('/api/v1/neural-forge/market-regime', {
        analysisType: 'comprehensive',
        includeGuidance: true,
        includeProbabilities: true,
        timeframe: 'current'
      }, {
        baseURL: process.env.NEURAL_FORGE_ENDPOINT || 'https://neural-forge.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.NEURAL_FORGE_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });

      const regime = {
        regime: response.data.regime || 'TRANSITIONAL',
        confidence: response.data.confidence || 0.5,
        indicators: response.data.indicators || {
          trend: 0,
          volatility: 0.5,
          momentum: 0,
          breadth: 0
        },
        characteristics: response.data.characteristics || [],
        tradingGuidance: response.data.tradingGuidance || [],
        duration: response.data.duration || 'Unknown',
        probabilityMatrix: response.data.probabilityMatrix || []
      };

      const latency = Date.now() - startTime;

      // Cache the result for 1 hour
      await cache.set(cacheKey, regime, 3600000);

      logger.info('Market regime analysis retrieved successfully', { 
        regime: regime.regime,
        confidence: regime.confidence,
        latency 
      });

      return {
        success: true,
        data: regime,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `regime-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get market regime analysis', { error });
      return {
        success: false,
        error: {
          code: 'REGIME_ERROR',
          message: 'Failed to get market regime analysis',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }
}
