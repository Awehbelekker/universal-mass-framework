/**
 * PROMETHEUS MCP Server - Advanced Logging System
 * Winston-based logging with structured output and multiple transports
 */

import winston from 'winston';
import { LogEntry } from '../types';

interface LoggerConfig {
  level: string;
  file?: string;
  console: boolean;
  json: boolean;
  timestamp: boolean;
  colorize: boolean;
  maxSize: string;
  maxFiles: number;
  requestIdKey: string;
  userIdKey: string;
}

class PrometheusLogger {
  private logger!: winston.Logger;
  private config: LoggerConfig;

  constructor(config: Partial<LoggerConfig> = {}) {
    this.config = {
      level: process.env.LOG_LEVEL || 'info',
      file: process.env.LOG_FILE,
      console: true,
      json: process.env.NODE_ENV === 'production',
      timestamp: true,
      colorize: process.env.NODE_ENV !== 'production',
      maxSize: '10m',
      maxFiles: 5,
      requestIdKey: 'requestId',
      userIdKey: 'userId',
      ...config
    };

    this.initializeLogger();
  }

  private initializeLogger(): void {
    // Custom format for structured logging
    const customFormat = winston.format.combine(
      winston.format.timestamp(),
      winston.format.errors({ stack: true }),
      winston.format.json(),
      winston.format.printf((info) => {
        const { timestamp, level, message, ...meta } = info;
        
        const logEntry: LogEntry = {
          level: level as LogEntry['level'],
          message: String(message),
          timestamp: String(timestamp),
          ...meta
        };

        return this.config.json 
          ? JSON.stringify(logEntry)
          : `${timestamp} [${level.toUpperCase()}] ${message} ${Object.keys(meta).length ? JSON.stringify(meta) : ''}`;
      })
    );

    // Console format for development
    const consoleFormat = winston.format.combine(
      winston.format.colorize(),
      winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
      winston.format.printf((info) => {
        const { timestamp, level, message, ...meta } = info;
        const metaString = Object.keys(meta).length ? ` ${JSON.stringify(meta)}` : '';
        return `${timestamp} [${level}] ${message}${metaString}`;
      })
    );

    // Configure transports
    const transports: winston.transport[] = [];

    // Console transport
    if (this.config.console) {
      transports.push(
        new winston.transports.Console({
          format: this.config.colorize ? consoleFormat : customFormat,
          level: this.config.level
        })
      );
    }

    // File transport
    if (this.config.file) {
      transports.push(
        new winston.transports.File({
          filename: this.config.file,
          format: customFormat,
          level: this.config.level,
          maxsize: this.parseSize(this.config.maxSize),
          maxFiles: this.config.maxFiles,
          tailable: true
        })
      );

      // Separate error log file
      transports.push(
        new winston.transports.File({
          filename: this.config.file.replace('.log', '.error.log'),
          format: customFormat,
          level: 'error',
          maxsize: this.parseSize(this.config.maxSize),
          maxFiles: this.config.maxFiles,
          tailable: true
        })
      );
    }

    // Create logger instance
    this.logger = winston.createLogger({
      level: this.config.level,
      transports,
      exitOnError: false,
      silent: process.env.NODE_ENV === 'test'
    });

    // Handle uncaught exceptions
    this.logger.exceptions.handle(
      new winston.transports.File({
        filename: this.config.file?.replace('.log', '.exceptions.log') || 'exceptions.log',
        format: customFormat
      })
    );

    // Handle unhandled promise rejections
    this.logger.rejections.handle(
      new winston.transports.File({
        filename: this.config.file?.replace('.log', '.rejections.log') || 'rejections.log',
        format: customFormat
      })
    );
  }

  private parseSize(size: string): number {
    const units: { [key: string]: number } = {
      b: 1,
      k: 1024,
      m: 1024 * 1024,
      g: 1024 * 1024 * 1024
    };

    const match = size.toLowerCase().match(/^(\d+)([kmg]?)$/);
    if (!match) return 10 * 1024 * 1024; // Default 10MB

    const value = parseInt(match[1]!);
    const unit = match[2] || 'b';
    
    return value * (units[unit] || 1);
  }

  private createLogMethod(level: LogEntry['level']) {
    return (message: string, meta: Record<string, any> = {}) => {
      this.logger.log(level, message, meta);
    };
  }

  // Core logging methods
  error = this.createLogMethod('error');
  warn = this.createLogMethod('warn');
  info = this.createLogMethod('info');
  debug = this.createLogMethod('debug');

  // Specialized logging methods for PROMETHEUS
  logRequest(requestId: string, method: string, path: string, userId?: string, meta: Record<string, any> = {}): void {
    this.info(`${method} ${path}`, {
      requestId,
      userId,
      type: 'request',
      ...meta
    });
  }

  logResponse(requestId: string, statusCode: number, duration: number, userId?: string, meta: Record<string, any> = {}): void {
    this.info(`Response ${statusCode} in ${duration}ms`, {
      requestId,
      userId,
      statusCode,
      duration,
      type: 'response',
      ...meta
    });
  }

  logTrade(orderId: string, symbol: string, side: string, quantity: number, price: number, userId?: string, meta: Record<string, any> = {}): void {
    this.info(`Trade executed: ${side} ${quantity} ${symbol} @ ${price}`, {
      orderId,
      symbol,
      side,
      quantity,
      price,
      userId,
      type: 'trade',
      ...meta
    });
  }

  logRiskAlert(alertId: string, type: string, symbol: string, severity: string, userId?: string, meta: Record<string, any> = {}): void {
    this.warn(`Risk alert: ${type} for ${symbol}`, {
      alertId,
      type,
      symbol,
      severity,
      userId,
      alertType: 'risk',
      ...meta
    });
  }

  logNeuralForge(symbol: string, prediction: string, confidence: number, userId?: string, meta: Record<string, any> = {}): void {
    this.info(`Neural Forge prediction: ${symbol} ${prediction} (${confidence}%)`, {
      symbol,
      prediction,
      confidence,
      userId,
      type: 'neural-forge',
      ...meta
    });
  }

  logAuth(event: string, userId?: string, email?: string, meta: Record<string, any> = {}): void {
    this.info(`Auth event: ${event}`, {
      userId,
      email,
      event,
      type: 'auth',
      ...meta
    });
  }

  logCacheOperation(operation: string, key: string, hit: boolean, duration?: number, meta: Record<string, any> = {}): void {
    this.debug(`Cache ${operation}: ${key} (${hit ? 'HIT' : 'MISS'})`, {
      operation,
      key,
      hit,
      duration,
      type: 'cache',
      ...meta
    });
  }

  logWebSocket(event: string, userId?: string, connectionId?: string, meta: Record<string, any> = {}): void {
    this.info(`WebSocket ${event}`, {
      userId,
      connectionId,
      event,
      type: 'websocket',
      ...meta
    });
  }

  logRateLimit(key: string, limit: number, current: number, windowMs: number, meta: Record<string, any> = {}): void {
    this.warn(`Rate limit exceeded: ${key} (${current}/${limit} in ${windowMs}ms)`, {
      key,
      limit,
      current,
      windowMs,
      type: 'rate-limit',
      ...meta
    });
  }

  logMetrics(metrics: Record<string, any>, meta: Record<string, any> = {}): void {
    this.info('System metrics', {
      metrics,
      type: 'metrics',
      ...meta
    });
  }

  // Performance logging
  logPerformance(operation: string, duration: number, userId?: string, meta: Record<string, any> = {}): void {
    const level = duration > 1000 ? 'warn' : 'info';
    this.logger.log(level, `Performance: ${operation} took ${duration}ms`, {
      operation,
      duration,
      userId,
      type: 'performance',
      ...meta
    });
  }

  // Security logging
  logSecurity(event: string, severity: 'low' | 'medium' | 'high' | 'critical', userId?: string, ip?: string, meta: Record<string, any> = {}): void {
    const level = severity === 'critical' ? 'error' : severity === 'high' ? 'warn' : 'info';
    this.logger.log(level, `Security event: ${event}`, {
      event,
      severity,
      userId,
      ip,
      type: 'security',
      ...meta
    });
  }

  // Business logic logging
  logBusinessEvent(event: string, userId?: string, meta: Record<string, any> = {}): void {
    this.info(`Business event: ${event}`, {
      event,
      userId,
      type: 'business',
      ...meta
    });
  }

  // Create child logger with context
  child(context: Record<string, any>): PrometheusLogger {
    const childLogger = new PrometheusLogger(this.config);
    
    // Override logging methods to include context
    const originalMethods = {
      error: childLogger.error,
      warn: childLogger.warn,
      info: childLogger.info,
      debug: childLogger.debug
    };

    Object.keys(originalMethods).forEach(method => {
      childLogger[method as keyof typeof originalMethods] = (message: string, meta: Record<string, any> = {}) => {
        originalMethods[method as keyof typeof originalMethods](message, { ...context, ...meta });
      };
    });

    return childLogger;
  }

  // Get logger statistics
  getStats(): {
    level: string;
    transports: number;
    files: string[];
  } {
    const fileTransports = this.logger.transports.filter(t => t instanceof winston.transports.File);
    const files = fileTransports.map(t => (t as any).filename || '');

    return {
      level: this.config.level,
      transports: this.logger.transports.length,
      files
    };
  }

  // Graceful shutdown
  async close(): Promise<void> {
    return new Promise((resolve) => {
      if (this.logger && typeof this.logger.close === 'function') {
        this.logger.close();
      }
      resolve();
    });
  }
}

// Create singleton logger instance
export const logger = new PrometheusLogger({
  level: process.env.LOG_LEVEL || 'info',
  file: process.env.LOG_FILE,
  console: true,
  json: process.env.NODE_ENV === 'production',
  colorize: process.env.NODE_ENV !== 'production'
});

// Export logger class for custom instances
export { PrometheusLogger };

// Export convenience methods
export const createLogger = (config: Partial<LoggerConfig> = {}) => new PrometheusLogger(config);
