/**
 * PROMETHEUS MCP Server Implementation
 * Core MCP server for conversational AI trading with Claude
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ErrorCode,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';

import { logger } from './utils/logger.js';
import { cache } from './utils/cache.js';
import { defaultConfig } from './config/default.js';
import { PortfolioTools } from './tools/portfolio.js';
import { MarketDataTools } from './tools/market-data.js';
import { TradingTools } from './tools/trading.js';
import { NeuralForgeTools } from './tools/neural-forge.js';
import { RiskManagementTools } from './tools/risk-management.js';
import { AuthMiddleware } from './auth/middleware.js';
import { MCPTool, MCPResource, ServerConfig } from './types/index.js';

export class PrometheusServer {
  private server: Server;
  private config: ServerConfig;
  private authManager: AuthMiddleware;
  private tools: Map<string, MCPTool>;
  private resources: Map<string, MCPResource>;
  private isRunning: boolean = false;

  constructor(config: any = defaultConfig) {
    this.config = config;
    this.tools = new Map();
    this.resources = new Map();
    
    // Initialize server
    this.server = new Server({
      name: 'PROMETHEUS Trading Platform',
      version: '1.0.0'
    });

    this.authManager = new AuthMiddleware(config.auth);
    this.initializeServer();
  }

  private initializeServer(): void {
    // Setup request handlers
    this.setupRequestHandlers();
    
    // Register tools
    this.registerTools();
    
    // Register resources
    this.registerResources();
    
    // Setup error handlers
    this.setupErrorHandlers();
    
    logger.info('🔥 PROMETHEUS MCP Server initialized');
  }

  private setupRequestHandlers(): void {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      const tools = Array.from(this.tools.values()).map(tool => ({
        name: tool.name,
        description: tool.description,
        inputSchema: tool.inputSchema
      }));

      logger.debug('Listed tools', { count: tools.length });
      return { tools };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      const tool = this.tools.get(name);

      if (!tool) {
        throw new McpError(ErrorCode.MethodNotFound, `Tool "${name}" not found`);
      }

      try {
        logger.info(`Executing tool: ${name}`, { args });
        const result = await tool.handler(args);
        logger.info(`Tool executed successfully: ${name}`, { result });
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };
      } catch (error) {
        logger.error(`Tool execution failed: ${name}`, { error, args });
        throw new McpError(ErrorCode.InternalError, `Tool execution failed: ${error}`);
      }
    });

    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      const resources = Array.from(this.resources.values()).map(resource => ({
        uri: resource.uri,
        mimeType: resource.mimeType,
        description: resource.description
      }));

      logger.debug('Listed resources', { count: resources.length });
      return { resources };
    });

    // Handle resource reads
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const { uri } = request.params;
      const resource = this.resources.get(uri);

      if (!resource) {
        throw new McpError(ErrorCode.InvalidParams, `Resource "${uri}" not found`);
      }

      try {
        logger.info(`Reading resource: ${uri}`);
        const data = await resource.handler();
        logger.info(`Resource read successfully: ${uri}`);
        
        return {
          contents: [
            {
              uri,
              mimeType: resource.mimeType,
              text: JSON.stringify(data, null, 2)
            }
          ]
        };
      } catch (error) {
        logger.error(`Resource read failed: ${uri}`, { error });
        throw new McpError(ErrorCode.InternalError, `Resource read failed: ${error}`);
      }
    });
  }

  private registerTools(): void {
    // Portfolio Management Tools
    this.registerTool({
      name: 'getPortfolio',
      description: 'Get current portfolio overview with positions and performance metrics',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' }
        },
        required: ['userId']
      },
      handler: PortfolioTools.getPortfolio
    });

    this.registerTool({
      name: 'getPosition',
      description: 'Get details for a specific position',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' },
          symbol: { type: 'string', description: 'Stock symbol' }
        },
        required: ['userId', 'symbol']
      },
      handler: PortfolioTools.getPosition
    });

    this.registerTool({
      name: 'calculatePositionSize',
      description: 'Calculate optimal position size based on risk parameters',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' },
          symbol: { type: 'string', description: 'Stock symbol' },
          riskPercentage: { type: 'number', description: 'Risk percentage (0-100)' },
          stopLoss: { type: 'number', description: 'Stop loss price' }
        },
        required: ['userId', 'symbol', 'riskPercentage', 'stopLoss']
      },
      handler: PortfolioTools.calculatePositionSize
    });

    // Market Data Tools
    this.registerTool({
      name: 'getQuote',
      description: 'Get real-time quote for a stock symbol',
      inputSchema: {
        type: 'object',
        properties: {
          symbol: { type: 'string', description: 'Stock symbol' }
        },
        required: ['symbol']
      },
      handler: MarketDataTools.getQuote
    });

    this.registerTool({
      name: 'getMarketAnalysis',
      description: 'Get comprehensive market analysis including technical indicators and Neural Forge insights',
      inputSchema: {
        type: 'object',
        properties: {
          symbol: { type: 'string', description: 'Stock symbol' },
          timeframe: { type: 'string', description: 'Analysis timeframe (1D, 1W, 1M)', enum: ['1D', '1W', '1M'] }
        },
        required: ['symbol']
      },
      handler: MarketDataTools.getMarketAnalysis
    });

    this.registerTool({
      name: 'findOpportunities',
      description: 'Search for trading opportunities based on criteria',
      inputSchema: {
        type: 'object',
        properties: {
          sector: { type: 'string', description: 'Sector filter' },
          minVolume: { type: 'number', description: 'Minimum volume' },
          priceRange: { 
            type: 'array', 
            items: { type: 'number' },
            minItems: 2,
            maxItems: 2,
            description: 'Price range [min, max]'
          },
          technicalSetup: { type: 'string', description: 'Technical setup type' }
        },
        required: []
      },
      handler: MarketDataTools.findOpportunities
    });

    // Trading Tools
    this.registerTool({
      name: 'placeMarketOrder',
      description: 'Place a market order',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' },
          symbol: { type: 'string', description: 'Stock symbol' },
          side: { type: 'string', enum: ['BUY', 'SELL'], description: 'Order side' },
          quantity: { type: 'number', description: 'Number of shares' }
        },
        required: ['userId', 'symbol', 'side', 'quantity']
      },
      handler: TradingTools.placeMarketOrder
    });

    this.registerTool({
      name: 'placeLimitOrder',
      description: 'Place a limit order',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' },
          symbol: { type: 'string', description: 'Stock symbol' },
          side: { type: 'string', enum: ['BUY', 'SELL'], description: 'Order side' },
          quantity: { type: 'number', description: 'Number of shares' },
          limitPrice: { type: 'number', description: 'Limit price' }
        },
        required: ['userId', 'symbol', 'side', 'quantity', 'limitPrice']
      },
      handler: TradingTools.placeLimitOrder
    });

    this.registerTool({
      name: 'setStopLoss',
      description: 'Set stop loss for a position',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' },
          symbol: { type: 'string', description: 'Stock symbol' },
          stopPrice: { type: 'number', description: 'Stop price' },
          quantity: { type: 'number', description: 'Number of shares (optional)' }
        },
        required: ['userId', 'symbol', 'stopPrice']
      },
      handler: TradingTools.setStopLoss
    });

    this.registerTool({
      name: 'cancelOrder',
      description: 'Cancel an existing order',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' },
          orderId: { type: 'string', description: 'Order ID to cancel' }
        },
        required: ['userId', 'orderId']
      },
      handler: TradingTools.cancelOrder
    });

    this.registerTool({
      name: 'getOrderStatus',
      description: 'Get status of an order',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' },
          orderId: { type: 'string', description: 'Order ID' }
        },
        required: ['userId', 'orderId']
      },
      handler: TradingTools.getOrderStatus
    });

    // Neural Forge AI Tools
    this.registerTool({
      name: 'getPrediction',
      description: 'Get AI predictions from Neural Forge',
      inputSchema: {
        type: 'object',
        properties: {
          symbol: { type: 'string', description: 'Stock symbol' },
          timeframe: { type: 'string', description: 'Prediction timeframe' }
        },
        required: ['symbol', 'timeframe']
      },
      handler: NeuralForgeTools.getPrediction
    });

    this.registerTool({
      name: 'analyzeStrategy',
      description: 'Analyze trading strategy with AI',
      inputSchema: {
        type: 'object',
        properties: {
          strategy: { type: 'string', description: 'Strategy description' },
          symbols: { 
            type: 'array',
            items: { type: 'string' },
            description: 'Stock symbols to analyze'
          },
          backtest: { type: 'boolean', description: 'Run backtest' }
        },
        required: ['strategy', 'symbols']
      },
      handler: NeuralForgeTools.analyzeStrategy
    });

    this.registerTool({
      name: 'getInsights',
      description: 'Get AI market insights and suggestions',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' }
        },
        required: ['userId']
      },
      handler: NeuralForgeTools.getInsights
    });

    // Risk Management Tools
    this.registerTool({
      name: 'getRiskMetrics',
      description: 'Get portfolio risk metrics',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' }
        },
        required: ['userId']
      },
      handler: RiskManagementTools.getRiskMetrics
    });

    this.registerTool({
      name: 'setRiskParameters',
      description: 'Set risk management parameters',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' },
          maxPositionSize: { type: 'number', description: 'Maximum position size' },
          maxDailyLoss: { type: 'number', description: 'Maximum daily loss' },
          maxOpenPositions: { type: 'number', description: 'Maximum open positions' }
        },
        required: ['userId', 'maxPositionSize', 'maxDailyLoss', 'maxOpenPositions']
      },
      handler: RiskManagementTools.setRiskParameters
    });

    this.registerTool({
      name: 'getRiskAlerts',
      description: 'Get current risk alerts',
      inputSchema: {
        type: 'object',
        properties: {
          userId: { type: 'string', description: 'User ID' }
        },
        required: ['userId']
      },
      handler: RiskManagementTools.getRiskAlerts
    });

    logger.info(`🔧 Registered ${this.tools.size} tools`);
  }

  private registerResources(): void {
    // Trading history resource
    this.registerResource({
      uri: 'prometheus://trades',
      mimeType: 'application/json',
      description: 'Historical trades and performance data',
      handler: async () => {
        // Implementation would fetch from database
        return { trades: [], performance: {} };
      }
    });

    // Watchlists resource
    this.registerResource({
      uri: 'prometheus://watchlists',
      mimeType: 'application/json',
      description: 'User-defined watchlists',
      handler: async () => {
        // Implementation would fetch from database
        return { watchlists: [] };
      }
    });

    // Strategies resource
    this.registerResource({
      uri: 'prometheus://strategies',
      mimeType: 'application/json',
      description: 'Trading strategies and backtests',
      handler: async () => {
        // Implementation would fetch from database
        return { strategies: [] };
      }
    });

    logger.info(`📚 Registered ${this.resources.size} resources`);
  }

  private setupErrorHandlers(): void {
    // Handle uncaught exceptions
    process.on('uncaughtException', (error) => {
      logger.error('Uncaught exception', { error });
      this.shutdown();
    });

    // Handle unhandled promise rejections
    process.on('unhandledRejection', (reason, promise) => {
      logger.error('Unhandled rejection', { reason, promise });
    });

    // Handle SIGTERM and SIGINT
    process.on('SIGTERM', () => {
      logger.info('Received SIGTERM, shutting down gracefully');
      this.shutdown();
    });

    process.on('SIGINT', () => {
      logger.info('Received SIGINT, shutting down gracefully');
      this.shutdown();
    });
  }

  private registerTool(tool: MCPTool): void {
    this.tools.set(tool.name, tool);
  }

  private registerResource(resource: MCPResource): void {
    this.resources.set(resource.uri, resource);
  }

  public async start(): Promise<void> {
    if (this.isRunning) {
      logger.warn('Server is already running');
      return;
    }

    try {
      // Initialize cache
      await this.initializeCache();

      // Start the server
      const transport = new StdioServerTransport();
      await this.server.connect(transport);

      this.isRunning = true;
      logger.info('🚀 PROMETHEUS MCP Server started successfully');
    } catch (error) {
      logger.error('Failed to start server', { error });
      throw error;
    }
  }

  private async initializeCache(): Promise<void> {
    try {
      // Test cache connection
      await cache.set('health-check', { status: 'ok', timestamp: Date.now() }, 5000);
      const healthCheck = await cache.get('health-check');
      
      if (healthCheck) {
        logger.info('✅ Cache initialized successfully');
      } else {
        logger.warn('⚠️  Cache initialization failed, running without cache');
      }
    } catch (error) {
      logger.error('Cache initialization error', { error });
      logger.warn('⚠️  Running without cache');
    }
  }

  public async stop(): Promise<void> {
    await this.shutdown();
  }

  public async shutdown(): Promise<void> {
    if (!this.isRunning) {
      return;
    }

    try {
      logger.info('🛑 Shutting down PROMETHEUS MCP Server...');

      // Close cache connections
      await cache.disconnect();

      // Close server
      await this.server.close();

      this.isRunning = false;
      logger.info('✅ Server shutdown complete');
    } catch (error) {
      logger.error('Error during shutdown', { error });
    }
  }

  public getStatus(): {
    isRunning: boolean;
    toolsCount: number;
    resourcesCount: number;
    config: ServerConfig;
  } {
    return {
      isRunning: this.isRunning,
      toolsCount: this.tools.size,
      resourcesCount: this.resources.size,
      config: this.config
    };
  }
}

export default PrometheusServer;
