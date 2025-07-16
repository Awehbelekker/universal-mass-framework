/**
 * PROMETHEUS MCP Server Type Definitions
 * Core types for the Model Context Protocol server
 */

import { Request } from 'express';

// Extended Request interface with user authentication
export interface AuthenticatedRequest extends Request {
  user?: User;
  token?: string;
}

// User interface
export interface User {
  id: string;
  email: string;
  role: 'admin' | 'user' | 'trader';
  approved: boolean;
  createdAt: Date;
  updatedAt: Date;
}

// Authentication configuration
export interface AuthConfig {
  jwtSecret: string;
  tokenExpiration: string;
  apiKey: string;
  bcryptRounds: number;
}

// Server configuration interface
export interface ServerConfig {
  port: number;
  host: string;
  cors: {
    origin: string[];
    credentials: boolean;
  };
  redis: {
    host: string;
    port: number;
    password?: string;
    db: number;
    clusterMode: boolean;
    ttl: {
      default: number;
      quotes: number;
      portfolio: number;
      marketData: number;
      userSession: number;
      rateLimit: number;
    };
  };
  auth: AuthConfig;
  trading: {
    apiKey: string;
    baseUrl: string;
    timeout: number;
    rateLimit: {
      requests: number;
      period: number;
    };
  };
  neuralForge: {
    enabled: boolean;
    modelPath: string;
    batchSize: number;
    timeout: number;
  };
  logging: {
    level: 'error' | 'warn' | 'info' | 'debug';
    file?: string;
    console: boolean;
    json: boolean;
  };
  rateLimiting: {
    windowMs: number;
    max: number;
    message: string;
  };
  monitoring: {
    enabled: boolean;
    interval: number;
    alertThresholds: {
      errorRate: number;
      responseTime: number;
      memoryUsage: number;
    };
  };
}

export interface MCPServerConfig {
  name: string;
  version: string;
  description: string;
  protocol: string;
  capabilities: {
    tools: boolean;
    resources: boolean;
    subscriptions: boolean;
  };
}

export interface Position {
  symbol: string;
  quantity: number;
  avgPrice: number;
  currentPrice: number;
  pnl: number;
  pnlPercentage: number;
  marketValue: number;
  side: 'LONG' | 'SHORT';
  timestamp: string;
}

export interface PerformanceMetrics {
  totalReturn: number;
  totalReturnPercentage: number;
  dayReturn: number;
  dayReturnPercentage: number;
  sharpeRatio: number;
  maxDrawdown: number;
  winRate: number;
  averageWin: number;
  averageLoss: number;
  profitFactor: number;
}

export interface Portfolio {
  totalValue: number;
  cashBalance: number;
  dailyPnL: number;
  dailyPnLPercentage: number;
  positions: Position[];
  performance: PerformanceMetrics;
  lastUpdated: string;
}

export interface TechnicalIndicators {
  rsi: number;
  macd: {
    line: number;
    signal: number;
    histogram: number;
  };
  bollinger: {
    upper: number;
    middle: number;
    lower: number;
  };
  ma50: number;
  ma200: number;
  volume: number;
  volatility: number;
}

export interface SentimentScore {
  overall: number;
  news: number;
  social: number;
  options: number;
  insider: number;
  institutional: number;
}

export interface MarketQuote {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  bid: number;
  ask: number;
  high: number;
  low: number;
  open: number;
  close: number;
  timestamp: string;
}

export interface MarketAnalysis {
  symbol: string;
  technicalIndicators: TechnicalIndicators;
  sentiment: SentimentScore;
  neuralForgeScore: number;
  recommendation: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  priceTarget: number;
  supportLevels: number[];
  resistanceLevels: number[];
  analysis: string;
  timestamp: string;
}

export interface Opportunity {
  symbol: string;
  type: 'BREAKOUT' | 'REVERSAL' | 'MOMENTUM' | 'ARBITRAGE';
  score: number;
  description: string;
  entry: number;
  target: number;
  stopLoss: number;
  riskReward: number;
  timeframe: string;
  confidence: number;
}

export interface OrderParams {
  symbol: string;
  side: 'BUY' | 'SELL';
  quantity: number;
  type: 'MARKET' | 'LIMIT' | 'STOP' | 'STOP_LIMIT';
  price?: number;
  stopPrice?: number;
  timeInForce?: 'GTC' | 'IOC' | 'FOK' | 'DAY';
  clientOrderId?: string;
}

export interface OrderConfirmation {
  orderId: string;
  clientOrderId?: string;
  symbol: string;
  side: 'BUY' | 'SELL';
  quantity: number;
  price?: number;
  status: 'NEW' | 'FILLED' | 'PARTIALLY_FILLED' | 'CANCELLED' | 'REJECTED';
  timestamp: string;
  executedQuantity: number;
  executedPrice?: number;
  commission?: number;
  message?: string;
}

export interface OrderStatus {
  orderId: string;
  clientOrderId?: string;
  symbol: string;
  side: 'BUY' | 'SELL';
  quantity: number;
  price?: number;
  stopPrice?: number;
  status: 'NEW' | 'FILLED' | 'PARTIALLY_FILLED' | 'CANCELLED' | 'REJECTED';
  executedQuantity: number;
  executedPrice?: number;
  timestamp: string;
  updateTime: string;
}

export interface CancelConfirmation {
  orderId: string;
  clientOrderId?: string;
  symbol: string;
  status: 'CANCELLED' | 'REJECTED';
  message?: string;
  timestamp: string;
}

export interface NeuralForgePrediction {
  symbol: string;
  direction: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
  confidence: number;
  priceTarget: number;
  timeframe: string;
  supportLevels: number[];
  resistanceLevels: number[];
  keyFactors: string[];
  modelVersion: string;
  timestamp: string;
}

export interface StrategyAnalysis {
  strategyName: string;
  symbols: string[];
  backtestResults?: {
    totalReturn: number;
    sharpeRatio: number;
    maxDrawdown: number;
    winRate: number;
    tradesCount: number;
    profitFactor: number;
  };
  optimization: {
    parameters: Record<string, any>;
    score: number;
    recommendations: string[];
  };
  riskAnalysis: {
    expectedDrawdown: number;
    correlation: number;
    volatility: number;
  };
  timestamp: string;
}

export interface AIInsight {
  type: 'MARKET_OVERVIEW' | 'OPPORTUNITY' | 'RISK_ALERT' | 'STRATEGY_SUGGESTION';
  title: string;
  content: string;
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  symbols?: string[];
  actionRequired: boolean;
  timestamp: string;
}

export interface RiskMetrics {
  portfolioBeta: number;
  sharpeRatio: number;
  maxDrawdown: number;
  valueAtRisk: number;
  expectedShortfall: number;
  volatility: number;
  correlations: CorrelationMatrix;
  exposures: {
    sector: Record<string, number>;
    geography: Record<string, number>;
    currency: Record<string, number>;
  };
  timestamp: string;
}

export interface CorrelationMatrix {
  [symbol: string]: {
    [symbol: string]: number;
  };
}

export interface RiskParameters {
  maxPositionSize: number;
  maxDailyLoss: number;
  maxOpenPositions: number;
  maxSectorExposure: number;
  stopLossPercentage: number;
  leverageLimit: number;
  correlationLimit: number;
}

export interface Alert {
  id: string;
  type: 'RISK' | 'PRICE' | 'NEWS' | 'TECHNICAL' | 'NEURAL_FORGE';
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  title: string;
  message: string;
  symbol?: string;
  timestamp: string;
  acknowledged: boolean;
  actionUrl?: string;
}

export interface PriceUpdate {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  timestamp: string;
}

export interface OrderFill {
  orderId: string;
  symbol: string;
  side: 'BUY' | 'SELL';
  quantity: number;
  price: number;
  commission: number;
  timestamp: string;
}

export interface RiskAlert {
  id: string;
  type: 'POSITION_LIMIT' | 'LOSS_LIMIT' | 'CORRELATION' | 'VOLATILITY';
  symbol?: string;
  message: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  timestamp: string;
  currentValue: number;
  threshold: number;
}

export interface ErrorResponse {
  code: string;
  message: string;
  details?: any;
  timestamp: string;
}

export enum ErrorCodes {
  INSUFFICIENT_FUNDS = 'E001',
  INVALID_SYMBOL = 'E002',
  MARKET_CLOSED = 'E003',
  RISK_LIMIT_EXCEEDED = 'E004',
  AUTHENTICATION_FAILED = 'E005',
  RATE_LIMIT_EXCEEDED = 'E006',
  INVALID_PARAMETERS = 'E007',
  SERVER_ERROR = 'E008',
  NETWORK_ERROR = 'E009',
  TIMEOUT = 'E010'
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ErrorResponse;
  metadata?: {
    timestamp: string;
    latency: number;
    cache: boolean;
    requestId: string;
  };
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
  tokenType: string;
  scope: string[];
}

export interface UserProfile {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  permissions: string[];
  accounts: string[];
  preferences: Record<string, any>;
  lastActive: string;
}

export interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number;
}

export interface RateLimitConfig {
  windowMs: number;
  maxRequests: number;
  maxOrders: number;
  maxOrdersPerDay: number;
  keyGenerator?: (req: any) => string;
}

export interface MetricsData {
  requestsPerMinute: number;
  averageLatency: number;
  errorRate: number;
  activeUsers: number;
  totalOrders: number;
  cacheHitRate: number;
  timestamp: string;
}

export interface HealthCheck {
  status: 'healthy' | 'unhealthy' | 'degraded';
  timestamp: string;
  services: {
    database: boolean;
    redis: boolean;
    api: boolean;
    websocket: boolean;
  };
  metrics: MetricsData;
}

export interface LogEntry {
  level: 'error' | 'warn' | 'info' | 'debug';
  message: string;
  timestamp: string;
  requestId?: string;
  userId?: string;
  metadata?: Record<string, any>;
}

export interface WebSocketMessage {
  type: 'PRICE_UPDATE' | 'ORDER_FILL' | 'RISK_ALERT' | 'AI_INSIGHT' | 'SYSTEM_STATUS';
  data: any;
  timestamp: string;
  userId?: string;
}

// MCP Protocol specific types
export interface MCPTool {
  name: string;
  description: string;
  inputSchema: {
    type: string;
    properties: Record<string, any>;
    required: string[];
  };
  handler: (input: any) => Promise<any>;
}

export interface MCPResource {
  uri: string;
  mimeType: string;
  description: string;
  handler: () => Promise<any>;
}

export interface MCPSubscription {
  name: string;
  description: string;
  handler: (callback: (data: any) => void) => void;
}

export interface MCPRequest {
  id: string;
  method: string;
  params: any;
  timestamp: string;
}

export interface MCPResponse {
  id: string;
  result?: any;
  error?: {
    code: number;
    message: string;
    data?: any;
  };
  timestamp: string;
}
