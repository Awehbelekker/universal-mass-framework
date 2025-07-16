/**
 * PROMETHEUS MCP Server - Redis Cache Implementation
 * Advanced caching layer with clustering support and intelligent TTL management
 */

import Redis from 'ioredis';
import { logger } from './logger';
import { CacheEntry, MetricsData } from '../types';

interface CacheConfig {
  host: string;
  port: number;
  password?: string;
  db: number;
  clusterMode: boolean;
  retryDelayOnFailover: number;
  retryDelayOnClusterDown: number;
  retryDelayOnReconnect: number;
  maxRetriesPerRequest: number;
  lazyConnect: boolean;
  keyPrefix: string;
  ttl: {
    default: number;
    quotes: number;
    portfolio: number;
    marketData: number;
    userSession: number;
    rateLimit: number;
  };
}

export class PrometheusCache {
  private redis!: Redis;
  private config: CacheConfig;
  private isConnected: boolean = false;
  private metrics: {
    hits: number;
    misses: number;
    sets: number;
    deletes: number;
    errors: number;
  };

  constructor(config: CacheConfig) {
    this.config = config;
    this.metrics = {
      hits: 0,
      misses: 0,
      sets: 0,
      deletes: 0,
      errors: 0
    };

    this.initializeRedis();
  }

  private initializeRedis(): void {
    try {
      if (this.config.clusterMode) {
        // Redis Cluster configuration
        this.redis = new Redis.Cluster([
          {
            host: this.config.host,
            port: this.config.port
          }
        ], {
          redisOptions: {
            password: this.config.password,
            keyPrefix: this.config.keyPrefix,
            maxRetriesPerRequest: this.config.maxRetriesPerRequest,
            lazyConnect: this.config.lazyConnect
          }
        }) as any;
      } else {
        // Single Redis instance
        this.redis = new Redis({
          host: this.config.host,
          port: this.config.port,
          password: this.config.password,
          db: this.config.db,
          keyPrefix: this.config.keyPrefix,
          maxRetriesPerRequest: this.config.maxRetriesPerRequest,
          lazyConnect: this.config.lazyConnect
        });
      }

      this.setupEventHandlers();
      this.connect();
    } catch (error) {
      logger.error('Failed to initialize Redis', { error });
      throw error;
    }
  }

  private setupEventHandlers(): void {
    this.redis.on('connect', () => {
      logger.info('Redis connected successfully');
      this.isConnected = true;
    });

    this.redis.on('ready', () => {
      logger.info('Redis ready to accept commands');
    });

    this.redis.on('error', (error) => {
      logger.error('Redis error', { error });
      this.metrics.errors++;
      this.isConnected = false;
    });

    this.redis.on('close', () => {
      logger.warn('Redis connection closed');
      this.isConnected = false;
    });

    this.redis.on('reconnecting', () => {
      logger.info('Redis reconnecting');
    });

    this.redis.on('end', () => {
      logger.info('Redis connection ended');
      this.isConnected = false;
    });
  }

  private async connect(): Promise<void> {
    try {
      await this.redis.connect();
      logger.info('Redis connection established');
    } catch (error) {
      logger.error('Failed to connect to Redis', { error });
      throw error;
    }
  }

  /**
   * Get value from cache with automatic deserialization
   */
  async get<T>(key: string): Promise<T | null> {
    try {
      if (!this.isConnected) {
        logger.warn('Redis not connected, cache miss');
        this.metrics.misses++;
        return null;
      }

      const cached = await this.redis.get(key);
      
      if (cached === null) {
        this.metrics.misses++;
        return null;
      }

      const entry: CacheEntry<T> = JSON.parse(cached);
      
      // Check if entry has expired
      if (Date.now() > entry.timestamp + entry.ttl) {
        await this.delete(key);
        this.metrics.misses++;
        return null;
      }

      this.metrics.hits++;
      return entry.data;
    } catch (error) {
      logger.error('Cache get error', { key, error });
      this.metrics.errors++;
      return null;
    }
  }

  /**
   * Set value in cache with automatic serialization and TTL
   */
  async set<T>(key: string, value: T, ttl?: number): Promise<boolean> {
    try {
      if (!this.isConnected) {
        logger.warn('Redis not connected, cache set failed');
        return false;
      }

      const entry: CacheEntry<T> = {
        data: value,
        timestamp: Date.now(),
        ttl: ttl || this.config.ttl.default
      };

      const serialized = JSON.stringify(entry);
      const result = await this.redis.setex(key, Math.ceil(entry.ttl / 1000), serialized);
      
      this.metrics.sets++;
      return result === 'OK';
    } catch (error) {
      logger.error('Cache set error', { key, error });
      this.metrics.errors++;
      return false;
    }
  }

  /**
   * Delete key from cache
   */
  async delete(key: string): Promise<boolean> {
    try {
      if (!this.isConnected) {
        return false;
      }

      const result = await this.redis.del(key);
      this.metrics.deletes++;
      return result > 0;
    } catch (error) {
      logger.error('Cache delete error', { key, error });
      this.metrics.errors++;
      return false;
    }
  }

  /**
   * Check if key exists in cache
   */
  async exists(key: string): Promise<boolean> {
    try {
      if (!this.isConnected) {
        return false;
      }

      const result = await this.redis.exists(key);
      return result === 1;
    } catch (error) {
      logger.error('Cache exists error', { key, error });
      this.metrics.errors++;
      return false;
    }
  }

  /**
   * Get multiple keys at once
   */
  async mget<T>(keys: string[]): Promise<(T | null)[]> {
    try {
      if (!this.isConnected || keys.length === 0) {
        return keys.map(() => null);
      }

      const results = await this.redis.mget(keys);
      return results.map((cached, index) => {
        try {
          if (cached === null) {
            this.metrics.misses++;
            return null;
          }

          const entry: CacheEntry<T> = JSON.parse(cached);
          
          // Check if entry has expired
          if (Date.now() > entry.timestamp + entry.ttl) {
            this.delete(keys[index]!);
            this.metrics.misses++;
            return null;
          }

          this.metrics.hits++;
          return entry.data;
        } catch (error) {
          logger.error('Cache mget parse error', { key: keys[index], error });
          this.metrics.errors++;
          return null;
        }
      });
    } catch (error) {
      logger.error('Cache mget error', { keys, error });
      this.metrics.errors++;
      return keys.map(() => null);
    }
  }

  /**
   * Set multiple keys at once
   */
  async mset<T>(keyValuePairs: Array<[string, T, number?]>): Promise<boolean> {
    try {
      if (!this.isConnected || keyValuePairs.length === 0) {
        return false;
      }

      const pipeline = this.redis.pipeline();
      
      for (const [key, value, ttl] of keyValuePairs) {
        const entry: CacheEntry<T> = {
          data: value,
          timestamp: Date.now(),
          ttl: ttl || this.config.ttl.default
        };

        const serialized = JSON.stringify(entry);
        pipeline.setex(key, Math.ceil(entry.ttl / 1000), serialized);
      }

      const results = await pipeline.exec();
      const success = results?.every(result => result[1] === 'OK') || false;
      
      if (success) {
        this.metrics.sets += keyValuePairs.length;
      }
      
      return success;
    } catch (error) {
      logger.error('Cache mset error', { keyValuePairs: keyValuePairs.map(([k]) => k), error });
      this.metrics.errors++;
      return false;
    }
  }

  /**
   * Increment a numeric value
   */
  async increment(key: string, amount: number = 1): Promise<number> {
    try {
      if (!this.isConnected) {
        return 0;
      }

      const result = await this.redis.incrby(key, amount);
      return result;
    } catch (error) {
      logger.error('Cache increment error', { key, amount, error });
      this.metrics.errors++;
      return 0;
    }
  }

  /**
   * Set expiration for a key
   */
  async expire(key: string, ttl: number): Promise<boolean> {
    try {
      if (!this.isConnected) {
        return false;
      }

      const result = await this.redis.expire(key, Math.ceil(ttl / 1000));
      return result === 1;
    } catch (error) {
      logger.error('Cache expire error', { key, ttl, error });
      this.metrics.errors++;
      return false;
    }
  }

  /**
   * Get keys matching a pattern
   */
  async keys(pattern: string): Promise<string[]> {
    try {
      if (!this.isConnected) {
        return [];
      }

      const keys = await this.redis.keys(pattern);
      return keys.map(key => key.replace(this.config.keyPrefix, ''));
    } catch (error) {
      logger.error('Cache keys error', { pattern, error });
      this.metrics.errors++;
      return [];
    }
  }

  /**
   * Clear all cache entries matching a pattern
   */
  async clear(pattern: string = '*'): Promise<number> {
    try {
      if (!this.isConnected) {
        return 0;
      }

      const keys = await this.redis.keys(pattern);
      if (keys.length === 0) {
        return 0;
      }

      const result = await this.redis.del(...keys);
      this.metrics.deletes += result;
      return result;
    } catch (error) {
      logger.error('Cache clear error', { pattern, error });
      this.metrics.errors++;
      return 0;
    }
  }

  /**
   * Get cache statistics
   */
  getMetrics(): MetricsData & { cache: any } {
    const totalRequests = this.metrics.hits + this.metrics.misses;
    const hitRate = totalRequests > 0 ? this.metrics.hits / totalRequests : 0;

    return {
      requestsPerMinute: 0, // This would be tracked elsewhere
      averageLatency: 0,    // This would be tracked elsewhere
      errorRate: 0,         // This would be tracked elsewhere
      activeUsers: 0,       // This would be tracked elsewhere
      totalOrders: 0,       // This would be tracked elsewhere
      cacheHitRate: hitRate,
      timestamp: new Date().toISOString(),
      cache: { ...this.metrics }
    };
  }

  /**
   * Reset cache metrics
   */
  resetMetrics(): void {
    this.metrics = {
      hits: 0,
      misses: 0,
      sets: 0,
      deletes: 0,
      errors: 0
    };
  }

  /**
   * Get cache health status
   */
  async getHealth(): Promise<{ connected: boolean; latency: number; memory: any }> {
    try {
      const start = Date.now();
      await this.redis.ping();
      const latency = Date.now() - start;

      const memory = await this.redis.memory('STATS') as any[];
      
      return {
        connected: this.isConnected,
        latency,
        memory
      };
    } catch (error) {
      logger.error('Cache health check error', { error });
      return {
        connected: false,
        latency: -1,
        memory: null
      };
    }
  }

  /**
   * Close Redis connection
   */
  async disconnect(): Promise<void> {
    try {
      await this.redis.quit();
      logger.info('Redis connection closed gracefully');
    } catch (error) {
      logger.error('Error closing Redis connection', { error });
    }
  }

  /**
   * Specialized cache methods for PROMETHEUS data types
   */

  // Portfolio caching
  async getPortfolio(userId: string): Promise<any> {
    return this.get(`portfolio:${userId}`);
  }

  async setPortfolio(userId: string, portfolio: any): Promise<boolean> {
    return this.set(`portfolio:${userId}`, portfolio, this.config.ttl.portfolio);
  }

  // Market data caching
  async getQuote(symbol: string): Promise<any> {
    return this.get(`quote:${symbol}`);
  }

  async setQuote(symbol: string, quote: any): Promise<boolean> {
    return this.set(`quote:${symbol}`, quote, this.config.ttl.quotes);
  }

  // Rate limiting
  async getRateLimit(key: string): Promise<number> {
    const count = await this.get<number>(`rateLimit:${key}`);
    return count || 0;
  }

  async incrementRateLimit(key: string, window: number): Promise<number> {
    const rateLimitKey = `rateLimit:${key}`;
    const count = await this.increment(rateLimitKey);
    
    if (count === 1) {
      await this.expire(rateLimitKey, window);
    }
    
    return count;
  }

  // User session caching
  async getUserSession(sessionId: string): Promise<any> {
    return this.get(`session:${sessionId}`);
  }

  async setUserSession(sessionId: string, session: any): Promise<boolean> {
    return this.set(`session:${sessionId}`, session, this.config.ttl.userSession);
  }

  // Neural Forge predictions caching
  async getPrediction(symbol: string, timeframe: string): Promise<any> {
    return this.get(`prediction:${symbol}:${timeframe}`);
  }

  async setPrediction(symbol: string, timeframe: string, prediction: any): Promise<boolean> {
    return this.set(`prediction:${symbol}:${timeframe}`, prediction, this.config.ttl.marketData);
  }
}

// Factory function to create cache instance
export function createCache(config: Partial<CacheConfig>): PrometheusCache {
  const defaultConfig: CacheConfig = {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
    password: process.env.REDIS_PASSWORD,
    db: parseInt(process.env.REDIS_DB || '0'),
    clusterMode: process.env.REDIS_CLUSTER_MODE === 'true',
    retryDelayOnFailover: 100,
    retryDelayOnClusterDown: 300,
    retryDelayOnReconnect: 50,
    maxRetriesPerRequest: 3,
    lazyConnect: true,
    keyPrefix: 'prometheus:',
    ttl: {
      default: 60000,      // 1 minute
      quotes: 5000,        // 5 seconds
      portfolio: 30000,    // 30 seconds
      marketData: 10000,   // 10 seconds
      userSession: 3600000, // 1 hour
      rateLimit: 60000     // 1 minute
    }
  };

  const mergedConfig = { ...defaultConfig, ...config };
  return new PrometheusCache(mergedConfig);
}

// Export singleton instance
export const cache = createCache({});
