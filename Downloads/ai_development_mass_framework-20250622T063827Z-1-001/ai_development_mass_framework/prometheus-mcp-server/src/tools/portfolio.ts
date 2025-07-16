/**
 * PROMETHEUS MCP Server - Portfolio Management Tools
 * Tools for managing portfolios, positions, and performance metrics
 */

import { logger } from '../utils/logger';
import { cache } from '../utils/cache';
import { Portfolio, Position, PerformanceMetrics, ApiResponse } from '../types';
import axios from 'axios';

export class PortfolioTools {
  private static readonly CACHE_TTL = 30000; // 30 seconds

  /**
   * Get current portfolio overview
   */
  static async getPortfolio(params: { userId: string }): Promise<ApiResponse<Portfolio>> {
    try {
      const { userId } = params;
      logger.info('Getting portfolio', { userId });

      // Check cache first
      const cacheKey = `portfolio:${userId}`;
      const cached = await cache.get<Portfolio>(cacheKey);
      
      if (cached) {
        logger.info('Portfolio retrieved from cache', { userId });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `portfolio-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get(`/api/v1/portfolio/${userId}`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL || 'http://localhost:8000',
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const portfolio: Portfolio = response.data;
      const latency = Date.now() - startTime;

      // Cache the result
      await cache.set(cacheKey, portfolio, this.CACHE_TTL);

      logger.info('Portfolio retrieved successfully', { userId, latency });

      return {
        success: true,
        data: portfolio,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `portfolio-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get portfolio', { userId: params.userId, error });
      return {
        success: false,
        error: {
          code: 'PORTFOLIO_ERROR',
          message: 'Failed to retrieve portfolio',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get specific position details
   */
  static async getPosition(params: { userId: string; symbol: string }): Promise<ApiResponse<Position>> {
    try {
      const { userId, symbol } = params;
      logger.info('Getting position', { userId, symbol });

      // Check cache first
      const cacheKey = `position:${userId}:${symbol}`;
      const cached = await cache.get<Position>(cacheKey);
      
      if (cached) {
        logger.info('Position retrieved from cache', { userId, symbol });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `position-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get(`/api/v1/portfolio/${userId}/positions/${symbol}`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const position: Position = response.data;
      const latency = Date.now() - startTime;

      // Cache the result
      await cache.set(cacheKey, position, this.CACHE_TTL);

      logger.info('Position retrieved successfully', { userId, symbol, latency });

      return {
        success: true,
        data: position,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `position-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get position', { userId: params.userId, symbol: params.symbol, error });
      return {
        success: false,
        error: {
          code: 'POSITION_ERROR',
          message: 'Failed to retrieve position',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Calculate optimal position size based on risk parameters
   */
  static async calculatePositionSize(params: {
    userId: string;
    symbol: string;
    riskPercentage: number;
    stopLoss: number;
  }): Promise<ApiResponse<{
    shares: number;
    dollarAmount: number;
    riskAmount: number;
    maxPositionSize: number;
    recommendation: string;
  }>> {
    try {
      const { userId, symbol, riskPercentage, stopLoss } = params;
      logger.info('Calculating position size', { userId, symbol, riskPercentage, stopLoss });

      // First get current portfolio to understand available capital
      const portfolioResponse = await this.getPortfolio({ userId });
      if (!portfolioResponse.success || !portfolioResponse.data) {
        return {
          success: false,
          error: {
            code: 'PORTFOLIO_ERROR',
            message: 'Failed to retrieve portfolio for position sizing',
            timestamp: new Date().toISOString()
          }
        };
      }

      const portfolio = portfolioResponse.data;
      
      // Get current quote for the symbol
      const quoteResponse = await axios.get(`/api/v1/market/quote/${symbol}`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const currentPrice = quoteResponse.data.price;
      
      // Calculate position size based on risk management
      const totalCapital = portfolio.totalValue;
      const riskAmount = (totalCapital * riskPercentage) / 100;
      const priceRisk = Math.abs(currentPrice - stopLoss);
      const maxShares = Math.floor(riskAmount / priceRisk);
      const dollarAmount = maxShares * currentPrice;
      
      // Apply portfolio concentration limits (max 10% per position)
      const maxPositionSize = totalCapital * 0.1;
      const recommendedShares = Math.min(maxShares, Math.floor(maxPositionSize / currentPrice));
      const recommendedDollarAmount = recommendedShares * currentPrice;

      // Generate recommendation
      let recommendation = '';
      if (dollarAmount > maxPositionSize) {
        recommendation = `Recommended position size reduced from ${maxShares} to ${recommendedShares} shares to maintain portfolio diversification (max 10% per position)`;
      } else if (riskPercentage > 2) {
        recommendation = `Consider reducing risk percentage. Current risk of ${riskPercentage}% is above recommended 2% maximum`;
      } else {
        recommendation = `Position size appears appropriate based on risk management rules`;
      }

      const result = {
        shares: recommendedShares,
        dollarAmount: recommendedDollarAmount,
        riskAmount,
        maxPositionSize,
        recommendation
      };

      logger.info('Position size calculated successfully', { 
        userId, 
        symbol, 
        result 
      });

      return {
        success: true,
        data: result,
        metadata: {
          timestamp: new Date().toISOString(),
          latency: 0,
          cache: false,
          requestId: `position-size-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to calculate position size', { 
        userId: params.userId, 
        symbol: params.symbol, 
        error 
      });
      return {
        success: false,
        error: {
          code: 'POSITION_SIZE_ERROR',
          message: 'Failed to calculate position size',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get portfolio performance metrics
   */
  static async getPerformanceMetrics(params: { userId: string }): Promise<ApiResponse<PerformanceMetrics>> {
    try {
      const { userId } = params;
      logger.info('Getting performance metrics', { userId });

      // Check cache first
      const cacheKey = `performance:${userId}`;
      const cached = await cache.get<PerformanceMetrics>(cacheKey);
      
      if (cached) {
        logger.info('Performance metrics retrieved from cache', { userId });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `performance-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get(`/api/v1/portfolio/${userId}/performance`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const metrics: PerformanceMetrics = response.data;
      const latency = Date.now() - startTime;

      // Cache the result
      await cache.set(cacheKey, metrics, this.CACHE_TTL);

      logger.info('Performance metrics retrieved successfully', { userId, latency });

      return {
        success: true,
        data: metrics,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `performance-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get performance metrics', { userId: params.userId, error });
      return {
        success: false,
        error: {
          code: 'PERFORMANCE_ERROR',
          message: 'Failed to retrieve performance metrics',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get portfolio summary with key metrics
   */
  static async getPortfolioSummary(params: { userId: string }): Promise<ApiResponse<{
    totalValue: number;
    dayPnL: number;
    dayPnLPercentage: number;
    positionsCount: number;
    topPositions: Position[];
    riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
    recommendations: string[];
  }>> {
    try {
      const { userId } = params;
      logger.info('Getting portfolio summary', { userId });

      // Get full portfolio data
      const portfolioResponse = await this.getPortfolio({ userId });
      if (!portfolioResponse.success || !portfolioResponse.data) {
        return {
          success: false,
          error: {
            code: 'PORTFOLIO_ERROR',
            message: 'Failed to retrieve portfolio for summary',
            timestamp: new Date().toISOString()
          }
        };
      }

      const portfolio = portfolioResponse.data;
      
      // Calculate risk level based on portfolio metrics
      let riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' = 'LOW';
      const dayPnLPercentage = Math.abs(portfolio.dailyPnLPercentage);
      
      if (dayPnLPercentage > 5) {
        riskLevel = 'HIGH';
      } else if (dayPnLPercentage > 2) {
        riskLevel = 'MEDIUM';
      }

      // Get top positions by value
      const topPositions = portfolio.positions
        .sort((a, b) => b.marketValue - a.marketValue)
        .slice(0, 5);

      // Generate recommendations
      const recommendations: string[] = [];
      
      if (portfolio.positions.length > 20) {
        recommendations.push('Consider reducing number of positions for better portfolio management');
      }
      
      if (topPositions[0] && topPositions[0].marketValue > portfolio.totalValue * 0.2) {
        recommendations.push('Largest position exceeds 20% of portfolio - consider rebalancing');
      }
      
      if (riskLevel === 'HIGH') {
        recommendations.push('High daily volatility detected - review risk management settings');
      }

      const summary = {
        totalValue: portfolio.totalValue,
        dayPnL: portfolio.dailyPnL,
        dayPnLPercentage: portfolio.dailyPnLPercentage,
        positionsCount: portfolio.positions.length,
        topPositions,
        riskLevel,
        recommendations
      };

      logger.info('Portfolio summary generated successfully', { userId, summary });

      return {
        success: true,
        data: summary,
        metadata: {
          timestamp: new Date().toISOString(),
          latency: 0,
          cache: false,
          requestId: `portfolio-summary-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get portfolio summary', { userId: params.userId, error });
      return {
        success: false,
        error: {
          code: 'PORTFOLIO_SUMMARY_ERROR',
          message: 'Failed to generate portfolio summary',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }
}
