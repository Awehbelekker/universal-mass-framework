const functions = require('firebase-functions');
const admin = require('firebase-admin');
const cors = require('cors')({ origin: true });

// Initialize Firebase Admin
admin.initializeApp();

const db = admin.firestore();

// Health check endpoint
exports.health = functions.https.onRequest((req, res) => {
  cors(req, res, () => {
    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'MASS Framework Firebase Functions'
    });
  });
});

// Trading API endpoints
exports.trading = functions.https.onRequest((req, res) => {
  cors(req, res, async () => {
    try {
      const { method, path } = req;
      
      switch (path) {
        case '/api/trading/portfolio':
          // Get user portfolio
          const portfolio = await getPortfolio(req.user.uid);
          res.json(portfolio);
          break;
          
        case '/api/trading/orders':
          // Handle trading orders
          const order = await processOrder(req.body, req.user.uid);
          res.json(order);
          break;
          
        default:
          res.status(404).json({ error: 'Endpoint not found' });
      }
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });
});

// AI Agents API
exports.aiAgents = functions.https.onRequest((req, res) => {
  cors(req, res, async () => {
    try {
      const { method, path } = req;
      
      switch (path) {
        case '/api/ai-agents':
          // Get user's AI agents
          const agents = await getAIAgents(req.user.uid);
          res.json(agents);
          break;
          
        case '/api/ai-agents/execute':
          // Execute AI agent
          const result = await executeAIAgent(req.body, req.user.uid);
          res.json(result);
          break;
          
        default:
          res.status(404).json({ error: 'Endpoint not found' });
      }
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });
});

// User management
exports.users = functions.https.onRequest((req, res) => {
  cors(req, res, async () => {
    try {
      const { method, path } = req;
      
      switch (path) {
        case '/api/users/profile':
          // Get user profile
          const profile = await getUserProfile(req.user.uid);
          res.json(profile);
          break;
          
        case '/api/users/settings':
          // Update user settings
          const settings = await updateUserSettings(req.body, req.user.uid);
          res.json(settings);
          break;
          
        default:
          res.status(404).json({ error: 'Endpoint not found' });
      }
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });
});

// Market data
exports.marketData = functions.https.onRequest((req, res) => {
  cors(req, res, async () => {
    try {
      const { symbol } = req.query;
      
      if (!symbol) {
        return res.status(400).json({ error: 'Symbol required' });
      }
      
      // Get market data from Firestore
      const marketData = await getMarketData(symbol);
      res.json(marketData);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });
});

// Helper functions
async function getPortfolio(userId) {
  const portfolioRef = db.collection('trading_accounts').where('userId', '==', userId);
  const snapshot = await portfolioRef.get();
  
  const portfolio = [];
  snapshot.forEach(doc => {
    portfolio.push({ id: doc.id, ...doc.data() });
  });
  
  return portfolio;
}

async function processOrder(orderData, userId) {
  // Validate order
  if (!orderData.symbol || !orderData.quantity) {
    throw new Error('Invalid order data');
  }
  
  // Create trade record
  const tradeRef = await db.collection('trades').add({
    userId,
    symbol: orderData.symbol,
    quantity: orderData.quantity,
    type: orderData.type || 'market',
    status: 'pending',
    timestamp: admin.firestore.FieldValue.serverTimestamp()
  });
  
  return { id: tradeRef.id, status: 'pending' };
}

async function getAIAgents(userId) {
  const agentsRef = db.collection('ai_agents').where('userId', '==', userId);
  const snapshot = await agentsRef.get();
  
  const agents = [];
  snapshot.forEach(doc => {
    agents.push({ id: doc.id, ...doc.data() });
  });
  
  return agents;
}

async function executeAIAgent(agentData, userId) {
  // Execute AI agent logic
  const result = {
    agentId: agentData.agentId,
    status: 'executed',
    timestamp: new Date().toISOString(),
    predictions: []
  };
  
  // Save execution result
  await db.collection('ai_executions').add({
    userId,
    agentId: agentData.agentId,
    result,
    timestamp: admin.firestore.FieldValue.serverTimestamp()
  });
  
  return result;
}

async function getUserProfile(userId) {
  const userRef = db.collection('users').doc(userId);
  const doc = await userRef.get();
  
  if (!doc.exists) {
    throw new Error('User not found');
  }
  
  return doc.data();
}

async function updateUserSettings(settings, userId) {
  const userRef = db.collection('users').doc(userId);
  await userRef.update({
    settings,
    updatedAt: admin.firestore.FieldValue.serverTimestamp()
  });
  
  return settings;
}

async function getMarketData(symbol) {
  const marketDataRef = db.collection('market_data').doc(symbol);
  const doc = await marketDataRef.get();
  
  if (!doc.exists) {
    return { symbol, price: null, timestamp: null };
  }
  
  return doc.data();
}

// Scheduled functions
exports.scheduledDataUpdate = functions.pubsub.schedule('every 5 minutes').onRun(async (context) => {
  try {
    // Update market data
    console.log('Updating market data...');
    
    // This would connect to your market data provider
    // For now, we'll just log the execution
    console.log('Market data update completed');
    
    return null;
  } catch (error) {
    console.error('Error updating market data:', error);
    return null;
  }
});

// AI Agent processing
exports.processAIAgents = functions.pubsub.schedule('every 1 minutes').onRun(async (context) => {
  try {
    console.log('Processing AI agents...');
    
    // Get active AI agents
    const agentsRef = db.collection('ai_agents').where('status', '==', 'active');
    const snapshot = await agentsRef.get();
    
    for (const doc of snapshot.docs) {
      const agent = doc.data();
      
      // Process AI agent logic here
      console.log(`Processing agent: ${agent.name}`);
      
      // Update agent status
      await doc.ref.update({
        lastProcessed: admin.firestore.FieldValue.serverTimestamp()
      });
    }
    
    console.log('AI agents processing completed');
    return null;
  } catch (error) {
    console.error('Error processing AI agents:', error);
    return null;
  }
});
