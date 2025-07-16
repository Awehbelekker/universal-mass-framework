/**
 * PROMETHEUS MCP Server - Trading Tools
 * Tools for executing trades, managing orders, and order status
 */

import { logger } from '../utils/logger';
import { cache } from '../utils/cache';
import { 
  OrderParams, 
  OrderConfirmation, 
  OrderStatus, 
  CancelConfirmation, 
  ApiResponse,
  ErrorCodes
} from '../types';
import axios from 'axios';

export class TradingTools {
  private static readonly ORDER_CACHE_TTL = 60000; // 1 minute

  /**
   * Place a market order
   */
  static async placeMarketOrder(params: {
    userId: string;
    symbol: string;
    side: 'BUY' | 'SELL';
    quantity: number;
  }): Promise<ApiResponse<OrderConfirmation>> {
    try {
      const { userId, symbol, side, quantity } = params;
      logger.info('Placing market order', { userId, symbol, side, quantity });

      // Validate parameters
      if (quantity <= 0) {
        return {
          success: false,
          error: {
            code: ErrorCodes.INVALID_PARAMETERS,
            message: 'Quantity must be greater than 0',
            timestamp: new Date().toISOString()
          }
        };
      }

      // Check if market is open
      const marketStatus = await this.checkMarketStatus(symbol);
      if (!marketStatus.isOpen && !marketStatus.allowsAfterHours) {
        return {
          success: false,
          error: {
            code: ErrorCodes.MARKET_CLOSED,
            message: 'Market is closed and after-hours trading is not allowed',
            timestamp: new Date().toISOString()
          }
        };
      }

      // Check risk limits
      const riskCheck = await this.checkRiskLimits(userId, symbol, side, quantity);
      if (!riskCheck.allowed) {
        return {
          success: false,
          error: {
            code: ErrorCodes.RISK_LIMIT_EXCEEDED,
            message: riskCheck.reason || 'Risk limit exceeded',
            timestamp: new Date().toISOString()
          }
        };
      }

      // Place order
      const startTime = Date.now();
      const orderRequest: OrderParams = {
        symbol,
        side,
        quantity,
        type: 'MARKET',
        clientOrderId: `mcp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
      };

      const response = await axios.post(`/api/v1/trading/${userId}/orders`, orderRequest, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });

      const orderConfirmation: OrderConfirmation = response.data;
      const latency = Date.now() - startTime;

      // Cache order status
      await cache.set(`order:${orderConfirmation.orderId}`, orderConfirmation, this.ORDER_CACHE_TTL);

      // Log trade
      logger.logTrade(
        orderConfirmation.orderId,
        symbol,
        side,
        quantity,
        orderConfirmation.executedPrice || 0,
        userId
      );

      logger.info('Market order placed successfully', { 
        userId, 
        orderId: orderConfirmation.orderId,
        latency 
      });

      return {
        success: true,
        data: orderConfirmation,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `market-order-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to place market order', { params, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to place market order',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Place a limit order
   */
  static async placeLimitOrder(params: {
    userId: string;
    symbol: string;
    side: 'BUY' | 'SELL';
    quantity: number;
    limitPrice: number;
  }): Promise<ApiResponse<OrderConfirmation>> {
    try {
      const { userId, symbol, side, quantity, limitPrice } = params;
      logger.info('Placing limit order', { userId, symbol, side, quantity, limitPrice });

      // Validate parameters
      if (quantity <= 0) {
        return {
          success: false,
          error: {
            code: ErrorCodes.INVALID_PARAMETERS,
            message: 'Quantity must be greater than 0',
            timestamp: new Date().toISOString()
          }
        };
      }

      if (limitPrice <= 0) {
        return {
          success: false,
          error: {
            code: ErrorCodes.INVALID_PARAMETERS,
            message: 'Limit price must be greater than 0',
            timestamp: new Date().toISOString()
          }
        };
      }

      // Check risk limits
      const riskCheck = await this.checkRiskLimits(userId, symbol, side, quantity, limitPrice);
      if (!riskCheck.allowed) {
        return {
          success: false,
          error: {
            code: ErrorCodes.RISK_LIMIT_EXCEEDED,
            message: riskCheck.reason || 'Risk limit exceeded',
            timestamp: new Date().toISOString()
          }
        };
      }

      // Place order
      const startTime = Date.now();
      const orderRequest: OrderParams = {
        symbol,
        side,
        quantity,
        type: 'LIMIT',
        price: limitPrice,
        clientOrderId: `mcp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
      };

      const response = await axios.post(`/api/v1/trading/${userId}/orders`, orderRequest, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });

      const orderConfirmation: OrderConfirmation = response.data;
      const latency = Date.now() - startTime;

      // Cache order status
      await cache.set(`order:${orderConfirmation.orderId}`, orderConfirmation, this.ORDER_CACHE_TTL);

      logger.info('Limit order placed successfully', { 
        userId, 
        orderId: orderConfirmation.orderId,
        latency 
      });

      return {
        success: true,
        data: orderConfirmation,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `limit-order-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to place limit order', { params, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to place limit order',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Set stop loss order
   */
  static async setStopLoss(params: {
    userId: string;
    symbol: string;
    stopPrice: number;
    quantity?: number;
  }): Promise<ApiResponse<OrderConfirmation>> {
    try {
      const { userId, symbol, stopPrice, quantity } = params;
      logger.info('Setting stop loss', { userId, symbol, stopPrice, quantity });

      // If no quantity specified, use current position size
      let stopQuantity = quantity;
      if (!stopQuantity) {
        const positionResponse = await axios.get(`/api/v1/portfolio/${userId}/positions/${symbol}`, {
          baseURL: process.env.PROMETHEUS_API_BASE_URL,
          headers: {
            'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
            'Content-Type': 'application/json'
          },
          timeout: 10000
        });

        const position = positionResponse.data;
        stopQuantity = Math.abs(position.quantity);
      }

      if (stopQuantity <= 0) {
        return {
          success: false,
          error: {
            code: ErrorCodes.INVALID_PARAMETERS,
            message: 'No position found or quantity is 0',
            timestamp: new Date().toISOString()
          }
        };
      }

      // Place stop loss order
      const startTime = Date.now();
      const orderRequest: OrderParams = {
        symbol,
        side: 'SELL', // Stop loss is always a sell order
        quantity: stopQuantity,
        type: 'STOP',
        stopPrice,
        clientOrderId: `mcp-stop-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
      };

      const response = await axios.post(`/api/v1/trading/${userId}/orders`, orderRequest, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });

      const orderConfirmation: OrderConfirmation = response.data;
      const latency = Date.now() - startTime;

      // Cache order status
      await cache.set(`order:${orderConfirmation.orderId}`, orderConfirmation, this.ORDER_CACHE_TTL);

      logger.info('Stop loss set successfully', { 
        userId, 
        orderId: orderConfirmation.orderId,
        latency 
      });

      return {
        success: true,
        data: orderConfirmation,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `stop-loss-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to set stop loss', { params, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to set stop loss',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Cancel an order
   */
  static async cancelOrder(params: {
    userId: string;
    orderId: string;
  }): Promise<ApiResponse<CancelConfirmation>> {
    try {
      const { userId, orderId } = params;
      logger.info('Canceling order', { userId, orderId });

      const startTime = Date.now();
      const response = await axios.delete(`/api/v1/trading/${userId}/orders/${orderId}`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const cancelConfirmation: CancelConfirmation = response.data;
      const latency = Date.now() - startTime;

      // Update cache
      await cache.delete(`order:${orderId}`);

      logger.info('Order canceled successfully', { 
        userId, 
        orderId,
        latency 
      });

      return {
        success: true,
        data: cancelConfirmation,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `cancel-order-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to cancel order', { params, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to cancel order',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get order status
   */
  static async getOrderStatus(params: {
    userId: string;
    orderId: string;
  }): Promise<ApiResponse<OrderStatus>> {
    try {
      const { userId, orderId } = params;
      logger.info('Getting order status', { userId, orderId });

      // Check cache first
      const cacheKey = `order:${orderId}`;
      const cached = await cache.get<OrderStatus>(cacheKey);
      
      if (cached) {
        logger.info('Order status retrieved from cache', { userId, orderId });
        return {
          success: true,
          data: cached,
          metadata: {
            timestamp: new Date().toISOString(),
            latency: 0,
            cache: true,
            requestId: `order-status-${Date.now()}`
          }
        };
      }

      // Fetch from API
      const startTime = Date.now();
      const response = await axios.get(`/api/v1/trading/${userId}/orders/${orderId}`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      const orderStatus: OrderStatus = response.data;
      const latency = Date.now() - startTime;

      // Cache the result
      await cache.set(cacheKey, orderStatus, this.ORDER_CACHE_TTL);

      logger.info('Order status retrieved successfully', { userId, orderId, latency });

      return {
        success: true,
        data: orderStatus,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `order-status-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get order status', { params, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to get order status',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Get all orders for a user
   */
  static async getAllOrders(params: {
    userId: string;
    status?: 'NEW' | 'FILLED' | 'PARTIALLY_FILLED' | 'CANCELLED' | 'REJECTED';
    limit?: number;
  }): Promise<ApiResponse<OrderStatus[]>> {
    try {
      const { userId, status, limit = 50 } = params;
      logger.info('Getting all orders', { userId, status, limit });

      const queryParams: any = { limit };
      if (status) queryParams.status = status;

      const startTime = Date.now();
      const response = await axios.get(`/api/v1/trading/${userId}/orders`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        params: queryParams,
        timeout: 10000
      });

      const orders: OrderStatus[] = response.data;
      const latency = Date.now() - startTime;

      logger.info('All orders retrieved successfully', { 
        userId, 
        count: orders.length,
        latency 
      });

      return {
        success: true,
        data: orders,
        metadata: {
          timestamp: new Date().toISOString(),
          latency,
          cache: false,
          requestId: `all-orders-${Date.now()}`
        }
      };
    } catch (error) {
      logger.error('Failed to get all orders', { params, error });
      return {
        success: false,
        error: {
          code: ErrorCodes.SERVER_ERROR,
          message: 'Failed to get all orders',
          details: error,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  /**
   * Check market status
   */
  private static async checkMarketStatus(symbol: string): Promise<{
    isOpen: boolean;
    allowsAfterHours: boolean;
    nextOpen?: string;
    nextClose?: string;
  }> {
    try {
      const response = await axios.get(`/api/v1/market/status/${symbol}`, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 5000
      });

      return response.data;
    } catch (error) {
      logger.error('Failed to check market status', { symbol, error });
      // Default to market closed if we can't check
      return {
        isOpen: false,
        allowsAfterHours: false
      };
    }
  }

  /**
   * Check risk limits before placing order
   */
  private static async checkRiskLimits(
    userId: string,
    symbol: string,
    side: 'BUY' | 'SELL',
    quantity: number,
    price?: number
  ): Promise<{
    allowed: boolean;
    reason?: string;
  }> {
    try {
      const response = await axios.post(`/api/v1/risk/${userId}/check`, {
        symbol,
        side,
        quantity,
        price
      }, {
        baseURL: process.env.PROMETHEUS_API_BASE_URL,
        headers: {
          'Authorization': `Bearer ${process.env.PROMETHEUS_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 5000
      });

      return response.data;
    } catch (error) {
      logger.error('Failed to check risk limits', { userId, symbol, error });
      // Default to not allowed if we can't check
      return {
        allowed: false,
        reason: 'Unable to verify risk limits'
      };
    }
  }
}
