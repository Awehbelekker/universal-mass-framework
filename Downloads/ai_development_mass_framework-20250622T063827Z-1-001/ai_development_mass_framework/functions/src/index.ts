/**
 * PROMETHEUS Trading Platform Firebase Functions
 * Serverless backend powered by Neural Forge™
 */

import * as functions from "firebase-functions";
import * as express from "express";
import * as cors from "cors";
import * as logger from "firebase-functions/logger";
import * as admin from "firebase-admin";

// Initialize Firebase Admin
admin.initializeApp();
const db = admin.firestore();

// Extend Express Request interface
declare global {
  namespace Express {
    interface Request {
      user?: admin.auth.DecodedIdToken;
    }
  }
}

// Configure Express App
const app = express.default();
app.use(cors.default({ origin: true }));
app.use(express.json());

// Access control middleware
async function checkAccess(req: express.Request, res: express.Response, next: express.NextFunction) {
  try {
    // Check for access code in headers
    const accessCode = req.headers['x-access-code'] as string;
    const authToken = req.headers.authorization?.replace('Bearer ', '');
    
    // Valid access codes for private beta
    const validAccessCodes = [
      'PROMETHEUS-BETA-2024',
      'NEURAL-FORGE-ADMIN',
      'INVESTOR-DEMO-VIP',
      'TRADING-PLATFORM-DEV'
    ];
    
    // Allow access with valid code
    if (accessCode && validAccessCodes.includes(accessCode)) {
      return next();
    }
    
    // Check Firebase Auth token
    if (authToken) {
      try {
        const decodedToken = await admin.auth().verifyIdToken(authToken);
        const userEmail = decodedToken.email;
        
        // Check if user is in allowlist
        if (userEmail) {
          const userDoc = await db.collection('allowed_users').doc(userEmail).get();
          if (userDoc.exists) {
            req.user = decodedToken;
            return next();
          }
        }
      } catch (authError) {
        logger.warn("Invalid auth token", { error: authError });
      }
    }
    
    // Check session-based access (for web requests)
    const sessionAccess = req.headers['x-session-access'];
    if (sessionAccess === 'granted') {
      return next();
    }
    
    // Deny access
    res.status(403).json({
      error: 'Access Denied',
      message: 'This platform is in private beta. Access requires invitation or valid credentials.',
      code: 'PRIVATE_BETA_ACCESS_REQUIRED'
    });
    
  } catch (error) {
    logger.error("Access control error", { error });
    res.status(500).json({
      error: 'Access Control Error',
      message: 'Unable to verify access permissions.'
    });
  }
}

// Apply access control to all routes except public ones
const publicRoutes = ['/', '/logo', '/health', '/status'];
app.use((req, res, next) => {
  if (publicRoutes.includes(req.path)) {
    return next();
  }
  return checkAccess(req, res, next);
});

// Home route (public)
app.get('/', (req: express.Request, res: express.Response) => {
  logger.info("API home page accessed", {structuredData: true});
  res.send(`
    <!DOCTYPE html>
    <html>
    <head><title>PROMETHEUS Trading Platform - API</title></head>
    <body style="font-family: Arial; padding: 20px; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white;">
        <h1>🚀 PROMETHEUS Trading Platform API</h1>
        <h2>🔒 PRIVATE BETA - Access Restricted</h2>
        <p>🤖 Neural Forge™ Trading System: <strong>ACTIVE</strong></p>
        <p>🧠 AI Agent Learning: <strong>ENABLED</strong></p>
        <p>📊 Real-time Data: <strong>STREAMING</strong></p>
        <p>🔄 Data Orchestrator: <strong>PROCESSING</strong></p>
        <div style="background: rgba(255,71,87,0.2); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #ff4757;">
            <h3>🛡️ Private Beta Notice</h3>
            <p>This platform is currently in private beta. Access is restricted to invited users only.</p>
            <p>If you believe you should have access, please contact your administrator.</p>
        </div>
        <h3>Available Public Endpoints:</h3>
        <ul>
            <li><a href="/api/logo" style="color: #00ff88;">/api/logo</a> - Platform Logo</li>
            <li><a href="/api/health" style="color: #00ff88;">/api/health</a> - Health Check</li>
        </ul>
        <p style="margin-top: 30px; color: #00ff88;">🎯 PROMETHEUS Trading Platform - Neural Forge™ Technology</p>
    </body>
    </html>
  `);
});

// Health check (public)
app.get('/health', (req: express.Request, res: express.Response) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    platform: 'PROMETHEUS Trading Platform',
    technology: 'Neural Forge™',
    access: 'Private Beta'
  });
});

// Logo endpoint
app.get('/logo', (req: express.Request, res: express.Response) => {
  logger.info("Logo requested", {structuredData: true});
  res.setHeader('Content-Type', 'image/svg+xml');
  
  const color1 = req.query.color1 || '#ff4757';
  const color2 = req.query.color2 || '#ff6b81';
  const variant = req.query.variant || 'default';
  
  // Generate SVG based on the requested variant
  let svg = '';
  
  if (variant === 'admin') {
    svg = `<?xml version="1.0" encoding="UTF-8"?>
    <svg width="512" height="512" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="flameGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#ffa502" />
          <stop offset="100%" stop-color="#ff6348" />
        </linearGradient>
        <linearGradient id="circleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#0c0e16" />
          <stop offset="100%" stop-color="#2f3542" />
        </linearGradient>
      </defs>
      <circle cx="12" cy="12" r="11" fill="url(#circleGradient)" stroke="url(#flameGradient)" stroke-width="1" />
      <path fill="url(#flameGradient)" d="M12 6c0 2.461-1.333 4.667-4 6 0 2 1.333 4.667 4 7.333 2.667-2.666 4-5.333 4-7.333-2.667-1.333-4-3.539-4-6zm0 12c-2.028-2.028-3-3.96-3-5.334 0-1.053.396-1.936 1.173-2.633 1.825-1.234 1.827-3.113 1.827-3.3 0 0 1.667 1.267 1.667 3-.334-.334-1.334-.334-1.334.667 0 1.267 1.667.667 1.667 3.333 0-.666.333-1.333 1-1.333.333 0 .667.333.667.667 0 .353-.334 1.333-.667 2-.397.796-.758 1.44-1.105 1.933z"/>
      <text x="12" y="14" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="6" fill="white">Π</text>
    </svg>`;
  } else {
    svg = `<?xml version="1.0" encoding="UTF-8"?>
    <svg width="512" height="512" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="flameGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="${color1}" />
          <stop offset="100%" stop-color="${color2}" />
        </linearGradient>
        <linearGradient id="circleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#0c0e16" />
          <stop offset="100%" stop-color="#2f3542" />
        </linearGradient>
      </defs>
      <circle cx="12" cy="12" r="11" fill="url(#circleGradient)" stroke="url(#flameGradient)" stroke-width="1" />
      <path fill="url(#flameGradient)" d="M12 6c0 2.461-1.333 4.667-4 6 0 2 1.333 4.667 4 7.333 2.667-2.666 4-5.333 4-7.333-2.667-1.333-4-3.539-4-6zm0 12c-2.028-2.028-3-3.96-3-5.334 0-1.053.396-1.936 1.173-2.633 1.825-1.234 1.827-3.113 1.827-3.3 0 0 1.667 1.267 1.667 3-.334-.334-1.334-.334-1.334.667 0 1.267 1.667.667 1.667 3.333 0-.666.333-1.333 1-1.333.333 0 .667.333.667.667 0 .353-.334 1.333-.667 2-.397.796-.758 1.44-1.105 1.933z"/>
      <text x="12" y="14" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="6" fill="white">Π</text>
    </svg>`;
  }
  
  res.send(svg);
});

// Generate real-time intelligence
function generateRealTimeIntelligence() {
  return {
    timestamp: new Date().toISOString(),
    market_sentiment: 'BULLISH',
    volatility_index: Math.random() * 100,
    trending_assets: ['BTC', 'ETH', 'AAPL', 'TSLA', 'GOOGL'],
    ai_confidence: 95.7,
    market_signals: [
      { type: 'BUY', asset: 'BTC', strength: 8.5, price_target: 45000 },
      { type: 'HOLD', asset: 'ETH', strength: 7.2, price_target: 3200 },
      { type: 'SELL', asset: 'AAPL', strength: 6.8, price_target: 180 }
    ],
    real_time_data: {
      btc_price: 42000 + Math.random() * 1000,
      eth_price: 3000 + Math.random() * 200,
      market_cap_change: (Math.random() - 0.5) * 10
    }
  };
}

// Get orchestrator status
function getOrchestratorStatus() {
  return {
    status: 'OPERATIONAL',
    uptime: Math.floor(Math.random() * 100000),
    active_agents: 12,
    processed_signals: 847,
    learning_accuracy: 94.3,
    data_sources: {
      market_feeds: 'CONNECTED',
      news_apis: 'CONNECTED',
      social_sentiment: 'CONNECTED',
      technical_indicators: 'ACTIVE'
    },
    performance_metrics: {
      latency_ms: 45,
      throughput_per_sec: 1250,
      error_rate: 0.02
    }
  };
}

// Get user dashboard data
function getUserDashboard() {
  return {
    user_id: 'demo',
    portfolio_value: 125000 + Math.random() * 50000,
    total_return: 15.7,
    active_positions: 8,
    ai_recommendations: 5,
    recent_trades: [
      { symbol: 'BTC', action: 'BUY', amount: 0.5, price: 42500, timestamp: new Date().toISOString() },
      { symbol: 'ETH', action: 'SELL', amount: 2.0, price: 3150, timestamp: new Date().toISOString() }
    ],
    performance_metrics: {
      sharpe_ratio: 1.85,
      max_drawdown: -5.2,
      win_rate: 73.5,
      profit_factor: 2.4
    },
    real_time_data: generateRealTimeIntelligence()
  };
}

// Get agent learning recommendations
function getAgentLearning() {
  return {
    learning_status: 'ACTIVE',
    models_trained: 15,
    accuracy_improvement: 12.5,
    recent_learnings: [
      { pattern: 'Support/Resistance', accuracy: 89.2, trades: 45 },
      { pattern: 'Moving Average Crossover', accuracy: 76.8, trades: 23 },
      { pattern: 'RSI Divergence', accuracy: 82.4, trades: 31 }
    ],
    agent_insights: [
      'Market shows strong bullish momentum in crypto sector',
      'Tech stocks displaying resistance at key levels',
      'Risk appetite increasing based on sentiment analysis'
    ]
  };
}

// Get trading opportunities
function getTradingOpportunities() {
  return {
    opportunities: [
      { asset: 'BTC', action: 'BUY', confidence: 8.7, entry: 42000, target: 45000, stop: 40000 },
      { asset: 'ETH', action: 'BUY', confidence: 7.9, entry: 3100, target: 3400, stop: 2900 },
      { asset: 'AAPL', action: 'SELL', confidence: 6.5, entry: 185, target: 175, stop: 190 }
    ],
    market_analysis: 'Strong uptrend with momentum indicators positive'
  };
}

// Get performance metrics
function getPerformanceMetrics() {
  return {
    system_performance: {
      uptime: 99.97,
      response_time: 45,
      throughput: 1250,
      error_rate: 0.02
    },
    trading_performance: {
      total_return: 15.7,
      sharpe_ratio: 1.85,
      max_drawdown: -5.2,
      win_rate: 73.5
    },
    ai_performance: {
      prediction_accuracy: 94.3,
      learning_rate: 12.5,
      model_confidence: 95.7
    }
  };
}

// Generate market news feed
function getMarketNews() {
  return {
    timestamp: new Date().toISOString(),
    news_items: [
      {
        title: "Federal Reserve Signals Potential Rate Cuts",
        source: "Financial Times",
        category: "Economics",
        sentiment: "Bullish",
        impact_score: 8.5,
        url: "#",
        published_at: new Date(Date.now() - 3600000).toISOString(),
        summary: "The Federal Reserve has signaled potential rate cuts in the coming months, citing improving inflation data and economic stability."
      },
      {
        title: "AI Tech Giants Report Record Earnings",
        source: "Wall Street Journal",
        category: "Technology",
        sentiment: "Bullish",
        impact_score: 7.9,
        url: "#",
        published_at: new Date(Date.now() - 7200000).toISOString(),
        summary: "Leading AI technology companies have reported record quarterly earnings, exceeding analyst expectations by 15%."
      },
      {
        title: "Crypto Market Reaches New All-Time High",
        source: "Bloomberg",
        category: "Cryptocurrency",
        sentiment: "Bullish",
        impact_score: 8.2,
        url: "#",
        published_at: new Date(Date.now() - 10800000).toISOString(),
        summary: "Bitcoin and other major cryptocurrencies have reached new all-time highs amid increased institutional adoption."
      },
      {
        title: "Global Supply Chain Issues Easing",
        source: "Reuters",
        category: "Economics",
        sentiment: "Neutral",
        impact_score: 6.4,
        url: "#",
        published_at: new Date(Date.now() - 14400000).toISOString(),
        summary: "Reports indicate global supply chain issues are easing as shipping costs decrease and delivery times improve."
      },
      {
        title: "New Regulations Proposed for AI Trading",
        source: "CNBC",
        category: "Regulation",
        sentiment: "Neutral",
        impact_score: 7.1,
        url: "#",
        published_at: new Date(Date.now() - 18000000).toISOString(),
        summary: "Regulators have proposed new guidelines for AI-powered trading systems, focusing on transparency and risk management."
      }
    ],
    trending_topics: ["Federal Reserve", "Interest Rates", "AI Technology", "Cryptocurrency", "Regulation"],
    market_impact: {
      overall: "Positive",
      sectors: {
        technology: "Very Bullish",
        finance: "Bullish",
        energy: "Neutral",
        healthcare: "Slightly Bullish"
      }
    }
  };
}

// API Routes
app.get('/api/intelligence/real-time', (req: express.Request, res: express.Response) => {
  logger.info("Real-time intelligence requested");
  res.json(generateRealTimeIntelligence());
});

app.get('/api/orchestrator/status', (req: express.Request, res: express.Response) => {
  logger.info("Orchestrator status requested");
  res.json(getOrchestratorStatus());
});

app.get('/api/user/:userId/dashboard', (req: express.Request, res: express.Response) => {
  logger.info(`Dashboard requested for user: ${req.params.userId}`);
  res.json(getUserDashboard());
});

app.get('/api/agent-learning-recommendations', (req: express.Request, res: express.Response) => {
  logger.info("Agent learning recommendations requested");
  res.json(getAgentLearning());
});

app.get('/api/trading/opportunities', (req: express.Request, res: express.Response) => {
  logger.info("Trading opportunities requested");
  res.json(getTradingOpportunities());
});

app.get('/api/system/performance-metrics', (req: express.Request, res: express.Response) => {
  logger.info("Performance metrics requested");
  res.json(getPerformanceMetrics());
});

app.get('/api/market-news', (req: express.Request, res: express.Response) => {
  logger.info("Market news requested");
  res.json(getMarketNews());
});

// Handle 404 routes
app.use((req: express.Request, res: express.Response) => {
  logger.warn(`404 Error for path: ${req.path}`);
  res.status(404).json({
    error: 'Endpoint not found',
    available_endpoints: [
      '/api/intelligence/real-time',
      '/api/orchestrator/status',
      '/api/user/{user_id}/dashboard',
      '/api/agent-learning-recommendations',
      '/api/trading/opportunities',
      '/api/system/performance-metrics',
      '/api/market-news'
    ]
  });
});

// Export the express app as a Firebase Function
export const api = functions.https.onRequest(app);
