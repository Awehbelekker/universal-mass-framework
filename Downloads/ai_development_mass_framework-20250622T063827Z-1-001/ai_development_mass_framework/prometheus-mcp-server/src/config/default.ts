/**
 * PROMETHEUS MCP Server Configuration
 * Default configuration settings for the MCP server
 */

export interface ServerConfig {
  server: {
    port: number;
    host: string;
    env: 'development' | 'production' | 'test';
    cors: {
      origin: string | string[];
      credentials: boolean;
    };
    helmet: {
      enabled: boolean;
    };
    compression: {
      enabled: boolean;
      level: number;
    };
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
  
  api: {
    baseUrl: string;
    apiKey: string;
    version: string;
    timeout: number;
    retries: number;
  };
  
  oauth: {
    clientId: string;
    clientSecret: string;
    redirectUri: string;
    authorizationUrl: string;
    tokenUrl: string;
    scopes: string[];
  };
  
  jwt: {
    secret: string;
    expiresIn: string;
    refreshExpiresIn: string;
  };
  
  rateLimit: {
    windowMs: number;
    maxRequests: number;
    maxOrders: number;
    maxOrdersPerDay: number;
  };
  
  websocket: {
    port: number;
    heartbeatInterval: number;
  };
  
  neuralForge: {
    endpoint: string;
    apiKey: string;
    timeout: number;
  };
  
  monitoring: {
    enabled: boolean;
    port: number;
    healthCheckInterval: number;
  };
  
  logging: {
    level: 'error' | 'warn' | 'info' | 'debug';
    file?: string;
    console: boolean;
    json: boolean;
  };
}

export const defaultConfig: ServerConfig = {
  server: {
    port: parseInt(process.env.PORT || '3000'),
    host: process.env.HOST || 'localhost',
    env: (process.env.NODE_ENV as ServerConfig['server']['env']) || 'development',
    cors: {
      origin: process.env.CORS_ORIGIN?.split(',') || ['*'],
      credentials: process.env.CORS_CREDENTIALS === 'true'
    },
    helmet: {
      enabled: process.env.HELMET_ENABLED !== 'false'
    },
    compression: {
      enabled: true,
      level: 6
    }
  },
  
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
    password: process.env.REDIS_PASSWORD || '',
    db: parseInt(process.env.REDIS_DB || '0'),
    clusterMode: process.env.REDIS_CLUSTER_MODE === 'true',
    ttl: {
      default: parseInt(process.env.CACHE_TTL_DEFAULT || '60000'),
      quotes: parseInt(process.env.CACHE_TTL_QUOTES || '5000'),
      portfolio: parseInt(process.env.CACHE_TTL_PORTFOLIO || '30000'),
      marketData: parseInt(process.env.CACHE_TTL_MARKET_DATA || '10000'),
      userSession: parseInt(process.env.CACHE_TTL_USER_SESSION || '3600000'),
      rateLimit: parseInt(process.env.CACHE_TTL_RATE_LIMIT || '60000')
    }
  },
  
  api: {
    baseUrl: process.env.PROMETHEUS_API_BASE_URL || 'https://api.prometheus-trading.com',
    apiKey: process.env.PROMETHEUS_API_KEY || '',
    version: process.env.PROMETHEUS_API_VERSION || 'v1',
    timeout: parseInt(process.env.API_TIMEOUT || '30000'),
    retries: parseInt(process.env.API_RETRIES || '3')
  },
  
  oauth: {
    clientId: process.env.OAUTH_CLIENT_ID || '',
    clientSecret: process.env.OAUTH_CLIENT_SECRET || '',
    redirectUri: process.env.OAUTH_REDIRECT_URI || 'http://localhost:3000/auth/callback',
    authorizationUrl: process.env.OAUTH_AUTHORIZATION_URL || 'https://api.prometheus-trading.com/oauth/authorize',
    tokenUrl: process.env.OAUTH_TOKEN_URL || 'https://api.prometheus-trading.com/oauth/token',
    scopes: process.env.OAUTH_SCOPES?.split(',') || ['read', 'trade', 'manage']
  },
  
  jwt: {
    secret: process.env.JWT_SECRET || 'your-jwt-secret-here',
    expiresIn: process.env.JWT_EXPIRES_IN || '1h',
    refreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN || '7d'
  },
  
  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '60000'),
    maxRequests: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || '60'),
    maxOrders: parseInt(process.env.RATE_LIMIT_MAX_ORDERS_PER_MIN || '10'),
    maxOrdersPerDay: parseInt(process.env.RATE_LIMIT_MAX_ORDERS_PER_DAY || '100')
  },
  
  websocket: {
    port: parseInt(process.env.WS_PORT || '3001'),
    heartbeatInterval: parseInt(process.env.WS_HEARTBEAT_INTERVAL || '30000')
  },
  
  neuralForge: {
    endpoint: process.env.NEURAL_FORGE_ENDPOINT || 'https://neural-forge.prometheus-trading.com',
    apiKey: process.env.NEURAL_FORGE_API_KEY || '',
    timeout: parseInt(process.env.NEURAL_FORGE_TIMEOUT || '10000')
  },
  
  monitoring: {
    enabled: process.env.METRICS_ENABLED !== 'false',
    port: parseInt(process.env.METRICS_PORT || '3002'),
    healthCheckInterval: parseInt(process.env.HEALTH_CHECK_INTERVAL || '30000')
  },
  
  logging: {
    level: (process.env.LOG_LEVEL as ServerConfig['logging']['level']) || 'info',
    file: process.env.LOG_FILE || '',
    console: process.env.LOG_CONSOLE !== 'false',
    json: process.env.NODE_ENV === 'production'
  }
};
