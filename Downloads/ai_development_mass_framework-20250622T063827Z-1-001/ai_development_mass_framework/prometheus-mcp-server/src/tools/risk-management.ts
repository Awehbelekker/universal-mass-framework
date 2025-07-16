/**
 * PROMETHEUS MCP Server - Risk Management Tools
 * Tools for portfolio risk analysis, limits, and alerts
 */

import { logger } from '../utils/logger';
import { cache } from '../utils/cache';
import { 
  RiskMetrics, 
  RiskParameters, 
  Alert, 
  ApiResponse,
  ErrorCodes
} from '../types';
import axios from 'axios';

export class RiskManagementTools {
  private static readonly RISK_CACHE_TTL = 60000; // 1 minute

  /**
   * Get portfolio risk metrics
   */
  static async getRiskMetrics(params: { userId: string }): Promise<ApiResponse<RiskMetrics>> {
    try {
      const { userId } = params;
      logger.info('Getting risk metrics', { userId });

      // Check cache first
      const cacheKey = `risk:metrics:${userId}`;
      const cached = await cache.get<RiskMetrics>(cacheKey);
      
      if (cached) {
        logger.info('Risk metrics retrieved from cache', { userId });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `risk-metrics-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get(`/api/v1/risk/${userId}/metrics`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL || 'https://api.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY || ''}`,
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });

      const metrics: RiskMetrics = response.data;
      const latency = Date.now() - startTime;

      // Cache the result
      await cache.set(cacheKey, metrics, this.RISK_CACHE_TTL);

      logger.info('Risk metrics retrieved successfully', { userId, latency });

      return {
        success: true,
        data: metrics,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `risk-metrics-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get risk metrics', { userId: params.userId, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to retrieve risk metrics',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Set risk management parameters
   */
  static async setRiskParameters(params: {
    userId: string;
    maxPositionSize: number;
    maxDailyLoss: number;
    maxOpenPositions: number;
  }): Promise<ApiResponse<{ success: boolean; message: string }>> {
    try {
      const { userId, maxPositionSize, maxDailyLoss, maxOpenPositions } = params;
      logger.info('Setting risk parameters', { userId, maxPositionSize, maxDailyLoss, maxOpenPositions });

      // Validate parameters
      if (maxPositionSize <= 0 || maxPositionSize > 1) {
        return {
          success: false,
          error: {
            code: ErrorCodes.INVALID_PARAMETERS,
            message: 'Max position size must be between 0 and 1 (0-100%)',
            timestamp: new Date().toISOString()
          }
        };
      }

      if (maxDailyLoss <= 0) {
        return {
          success: false,
          error: {
            code: ErrorCodes.INVALID_PARAMETERS,
            message: 'Max daily loss must be greater than 0',
            timestamp: new Date().toISOString()
          }
        };
      }

      if (maxOpenPositions <= 0 || maxOpenPositions > 100) {
        return {
          success: false,
          error: {
            code: ErrorCodes.INVALID_PARAMETERS,
            message: 'Max open positions must be between 1 and 100',
            timestamp: new Date().toISOString()
          }
        };
      }

      const riskParams: RiskParameters = {
        maxPositionSize,
        maxDailyLoss,
        maxOpenPositions,
        maxSectorExposure: 0.3, // Default 30%
        stopLossPercentage: 0.05, // Default 5%
        leverageLimit: 1, // Default no leverage
        correlationLimit: 0.7 // Default max 70% correlation
      };

      // Set parameters via API
      const startTime = Date.now();
      const response = await axios.put(`/api/v1/risk/${userId}/parameters`, riskParams, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL || 'https://api.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY || ''}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const latency = Date.now() - startTime;

      // Clear cached risk metrics to force refresh
      await cache.delete(`risk:metrics:${userId}`);

      logger.info('Risk parameters set successfully', { userId, latency });

      return {
        success: true,
        data: {
          success: true,
          message: 'Risk parameters updated successfully'
        },
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `risk-params-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to set risk parameters', { params, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to set risk parameters',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get current risk alerts
   */
  static async getRiskAlerts(params: { userId: string }): Promise<ApiResponse<Alert[]>> {
    try {
      const { userId } = params;
      logger.info('Getting risk alerts', { userId });

      // Check cache first
      const cacheKey = `risk:alerts:${userId}`;
      const cached = await cache.get<Alert[]>(cacheKey);
      
      if (cached) {
        logger.info('Risk alerts retrieved from cache', { userId, count: cached.length });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `risk-alerts-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get(`/api/v1/risk/${userId}/alerts`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL || 'https://api.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY || ''}`,
          'Content-Type': 'application/json'
        },
        params: {
          status: 'active',
          limit: 50
        },
        timeout: 10000
      });

      const alerts: Alert[] = response.data;
      const latency = Date.now() - startTime;

      // Cache the result for shorter time due to dynamic nature
      await cache.set(cacheKey, alerts, 30000); // 30 seconds

      // Log critical alerts
      const criticalAlerts = alerts.filter(alert => alert.severity === 'CRITICAL');
      if (criticalAlerts.length > 0) {
        criticalAlerts.forEach(alert => {
          logger.logRiskAlert(alert.id, alert.type, alert.symbol || 'PORTFOLIO', alert.severity, userId);
        });
      }

      logger.info('Risk alerts retrieved successfully', { 
        userId, 
        totalAlerts: alerts.length,
        criticalAlerts: criticalAlerts.length,
        latency 
      });

      return {
        success: true,
        data: alerts,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `risk-alerts-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get risk alerts', { userId: params.userId, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to retrieve risk alerts',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Calculate position risk for a potential trade
   */
  static async calculatePositionRisk(params: {
    userId: string;
    symbol: string;
    quantity: number;
    price: number;
    stopLoss?: number;
  }): Promise<ApiResponse<{
    riskAmount: number;
    riskPercentage: number;
    positionSize: number;
    positionPercentage: number;
    isWithinLimits: boolean;
    warnings: string[];
    recommendations: string[];
  }>> {
    try {
      const { userId, symbol, quantity, price, stopLoss } = params;
      logger.info('Calculating position risk', { userId, symbol, quantity, price, stopLoss });

      // Get current portfolio to calculate risk
      const portfolioResponse = await axios.get(`/api/v1/portfolio/${userId}`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL || 'https://api.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY || ''}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const portfolio = portfolioResponse.data;
      const totalValue = portfolio.totalValue;
      const positionValue = quantity * price;
      const positionPercentage = positionValue / totalValue;

      // Calculate risk if stop loss is provided
      let riskAmount = 0;
      let riskPercentage = 0;
      if (stopLoss) {
        riskAmount = quantity * Math.abs(price - stopLoss);
        riskPercentage = riskAmount / totalValue;
      }

      // Get risk parameters
      const riskParamsResponse = await axios.get(`/api/v1/risk/${userId}/parameters`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL || 'https://api.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY || ''}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const riskParams = riskParamsResponse.data;

      // Check against limits
      const warnings: string[] = [];
      const recommendations: string[] = [];
      let isWithinLimits = true;

      if (positionPercentage > riskParams.maxPositionSize) {
        warnings.push(`Position size (${(positionPercentage * 100).toFixed(1)}%) exceeds maximum allowed (${(riskParams.maxPositionSize * 100).toFixed(1)}%)`);
        isWithinLimits = false;
      }

      if (riskPercentage > 0.02) { // 2% max risk rule
        warnings.push(`Risk amount (${(riskPercentage * 100).toFixed(1)}%) exceeds recommended maximum (2%)`);
        recommendations.push('Consider reducing position size or adjusting stop loss');
      }

      if (positionPercentage > 0.1) { // 10% concentration limit
        warnings.push(`Position concentration is high (${(positionPercentage * 100).toFixed(1)}%)`);
        recommendations.push('Consider diversifying across more positions');
      }

      if (!stopLoss) {
        recommendations.push('Consider setting a stop loss to limit downside risk');
      }

      const result = {
        riskAmount,
        riskPercentage,
        positionSize: positionValue,
        positionPercentage,
        isWithinLimits,
        warnings,
        recommendations
      };

      logger.info('Position risk calculated successfully', { 
        userId, 
        symbol,
        riskPercentage: riskPercentage * 100,
        positionPercentage: positionPercentage * 100,
        isWithinLimits
      });

      return {
        success: true,
        data: result,
        metadata: {
          timestamp: new Date().toISOString(),
          latency: 0,
          cache: false,
          requestId: `position-risk-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to calculate position risk', { params, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to calculate position risk',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get portfolio correlation matrix
   */
  static async getCorrelationMatrix(params: { 
    userId: string;
    timeframe?: '1M' | '3M' | '6M' | '1Y';
  }): Promise<ApiResponse<{
    correlations: { [symbol: string]: { [symbol: string]: number } };
    avgCorrelation: number;
    maxCorrelation: number;
    highlyCorrelatedPairs: Array<{
      symbol1: string;
      symbol2: string;
      correlation: number;
    }>;
    diversificationScore: number;
  }>> {
    try {
      const { userId, timeframe = '3M' } = params;
      logger.info('Getting correlation matrix', { userId, timeframe });

      // Check cache first
      const cacheKey = `risk:correlation:${userId}:${timeframe}`;
      const cached = await cache.get<any>(cacheKey);
      
      if (cached) {
        logger.info('Correlation matrix retrieved from cache', { userId, timeframe });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `correlation-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get(`/api/v1/risk/${userId}/correlation`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL || 'https://api.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY || ''}`,
          'Content-Type': 'application/json'
        },
        params: { timeframe },
        timeout: 15000
      });

      const correlationData = response.data;
      const latency = Date.now() - startTime;

      // Cache the result for longer time since correlation changes slowly
      await cache.set(cacheKey, correlationData, 3600000); // 1 hour

      logger.info('Correlation matrix retrieved successfully', { 
        userId, 
        timeframe,
        avgCorrelation: correlationData.avgCorrelation,
        diversificationScore: correlationData.diversificationScore,
        latency 
      });

      return {
        success: true,
        data: correlationData,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `correlation-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get correlation matrix', { params, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to retrieve correlation matrix',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Acknowledge risk alert
   */
  static async acknowledgeAlert(params: {
    userId: string;
    alertId: string;
    note?: string;
  }): Promise<ApiResponse<{ acknowledged: boolean; timestamp: string }>> {
    try {
      const { userId, alertId, note } = params;
      logger.info('Acknowledging risk alert', { userId, alertId });

      const startTime = Date.now();
      const response = await axios.patch(`/api/v1/risk/${userId}/alerts/${alertId}/acknowledge`, {
        note,
        acknowledgedAt: new Date().toISOString()
      }, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL || 'https://api.prometheus-trading.com',
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY || ''}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const latency = Date.now() - startTime;

      // Clear cached alerts to force refresh
      await cache.delete(`risk:alerts:${userId}`);

      logger.info('Risk alert acknowledged successfully', { userId, alertId, latency });

      return {
        success: true,
        data: {
          acknowledged: true,
          timestamp: new Date().toISOString()
        },
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `acknowledge-alert-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to acknowledge risk alert', { params, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to acknowledge risk alert',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }
}
