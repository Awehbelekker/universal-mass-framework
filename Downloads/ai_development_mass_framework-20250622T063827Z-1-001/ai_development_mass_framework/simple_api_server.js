#!/usr/bin/env node
/**
 * Simple Node.js API Server for MASS Framework Testing
 * This serves as a backup when Python environment is not available
 */

const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Logging middleware
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// Mock data
const mockUsers = [
    { id: 1, username: 'demo_user', email: 'demo@example.com', role: 'trader' },
    { id: 2, username: 'admin', email: 'admin@example.com', role: 'admin' }
];

const mockAgents = [
    { id: 1, name: 'Trading Agent', type: 'trading', status: 'active', performance: 95.2 },
    { id: 2, name: 'Analysis Agent', type: 'analysis', status: 'active', performance: 88.7 },
    { id: 3, name: 'Learning Agent', type: 'learning', status: 'training', performance: 92.1 }
];

const mockTrades = [
    { id: 1, symbol: 'AAPL', action: 'BUY', quantity: 100, price: 150.25, timestamp: new Date().toISOString() },
    { id: 2, symbol: 'GOOGL', action: 'SELL', quantity: 50, price: 2750.80, timestamp: new Date().toISOString() },
    { id: 3, symbol: 'MSFT', action: 'BUY', quantity: 75, price: 300.15, timestamp: new Date().toISOString() }
];

// Routes

// Health check
app.get('/', (req, res) => {
    res.json({
        message: '🤖 MASS Framework API Server',
        status: 'healthy',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        mode: 'Node.js Backup Server'
    });
});

app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        version: '1.0.0'
    });
});

// Authentication endpoints
app.post('/auth/login', (req, res) => {
    const { username, password } = req.body;
    
    if (!username || !password) {
        return res.status(400).json({ error: 'Username and password required' });
    }
    
    const user = mockUsers.find(u => u.username === username);
    if (!user) {
        return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Mock token generation
    const token = Buffer.from(`${username}:${Date.now()}`).toString('base64');
    
    res.json({
        access_token: token,
        token_type: 'bearer',
        user: user
    });
});

app.post('/auth/register', (req, res) => {
    const { username, email, password, role = 'user' } = req.body;
    
    if (!username || !email || !password) {
        return res.status(400).json({ error: 'Missing required fields' });
    }
    
    const newUser = {
        id: mockUsers.length + 1,
        username,
        email,
        role,
        created_at: new Date().toISOString()
    };
    
    mockUsers.push(newUser);
    
    res.json({
        message: 'User registered successfully',
        user: newUser
    });
});

// Agent endpoints
app.get('/api/agents', (req, res) => {
    res.json({
        agents: mockAgents,
        total: mockAgents.length
    });
});

app.post('/api/agents', (req, res) => {
    const { name, type, description } = req.body;
    
    const newAgent = {
        id: mockAgents.length + 1,
        name,
        type,
        description,
        status: 'active',
        performance: Math.random() * 100,
        created_at: new Date().toISOString()
    };
    
    mockAgents.push(newAgent);
    res.json(newAgent);
});

app.post('/api/agents/:id/execute', (req, res) => {
    const agentId = parseInt(req.params.id);
    const agent = mockAgents.find(a => a.id === agentId);
    
    if (!agent) {
        return res.status(404).json({ error: 'Agent not found' });
    }
    
    // Simulate agent execution
    setTimeout(() => {
        res.json({
            agent_id: agentId,
            status: 'completed',
            result: `Agent ${agent.name} executed successfully`,
            execution_time: Math.random() * 5000,
            timestamp: new Date().toISOString()
        });
    }, 1000);
});

// Trading endpoints
app.get('/api/trades', (req, res) => {
    res.json({
        trades: mockTrades,
        total: mockTrades.length
    });
});

app.post('/api/trades', (req, res) => {
    const { symbol, action, quantity, price } = req.body;
    
    const newTrade = {
        id: mockTrades.length + 1,
        symbol,
        action,
        quantity,
        price,
        timestamp: new Date().toISOString(),
        status: 'executed'
    };
    
    mockTrades.push(newTrade);
    res.json(newTrade);
});

// Market data endpoints
app.get('/api/market/:symbol', (req, res) => {
    const symbol = req.params.symbol.toUpperCase();
    
    // Mock market data
    const basePrice = Math.random() * 1000 + 50;
    const change = (Math.random() - 0.5) * 20;
    
    res.json({
        symbol,
        price: (basePrice + change).toFixed(2),
        change: change.toFixed(2),
        change_percent: ((change / basePrice) * 100).toFixed(2),
        volume: Math.floor(Math.random() * 1000000),
        timestamp: new Date().toISOString()
    });
});

// Analytics endpoints
app.get('/api/analytics/dashboard', (req, res) => {
    res.json({
        summary: {
            total_trades: mockTrades.length,
            total_agents: mockAgents.length,
            active_agents: mockAgents.filter(a => a.status === 'active').length,
            total_users: mockUsers.length,
            system_uptime: process.uptime()
        },
        performance: {
            success_rate: 94.5,
            avg_execution_time: 245,
            total_volume: 1250000,
            profit_loss: 12450.75
        },
        recent_activity: mockTrades.slice(-10)
    });
});

// Workflow endpoints
app.get('/api/workflows', (req, res) => {
    const mockWorkflows = [
        { id: 1, name: 'Auto Trading Strategy', status: 'active', last_run: new Date().toISOString() },
        { id: 2, name: 'Risk Analysis', status: 'paused', last_run: new Date().toISOString() },
        { id: 3, name: 'Portfolio Rebalancing', status: 'active', last_run: new Date().toISOString() }
    ];
    
    res.json({ workflows: mockWorkflows });
});

app.post('/api/workflows/:id/execute', (req, res) => {
    const workflowId = parseInt(req.params.id);
    
    // Simulate workflow execution
    res.json({
        workflow_id: workflowId,
        status: 'started',
        execution_id: `exec_${Date.now()}`,
        timestamp: new Date().toISOString()
    });
});

// Chat endpoints
app.post('/api/chat/send', (req, res) => {
    const { message } = req.body;
    
    // Mock AI response
    const responses = [
        "I understand you want to analyze the market trends. Let me process that for you.",
        "The current market conditions suggest a bullish trend in tech stocks.",
        "I recommend reviewing your portfolio allocation based on recent performance.",
        "Your trading strategy is performing well with a 94.5% success rate.",
        "Let me analyze the latest market data to provide better insights."
    ];
    
    const response = responses[Math.floor(Math.random() * responses.length)];
    
    setTimeout(() => {
        res.json({
            response: response,
            timestamp: new Date().toISOString(),
            session_id: `session_${Date.now()}`
        });
    }, 1000);
});

// Real-time status endpoint
app.get('/api/status', (req, res) => {
    res.json({
        system: {
            status: 'operational',
            version: '1.0.0',
            uptime: process.uptime(),
            timestamp: new Date().toISOString()
        },
        services: {
            api: 'running',
            database: 'connected',
            trading_engine: 'active',
            ai_agents: 'processing'
        },
        metrics: {
            requests_per_minute: Math.floor(Math.random() * 100),
            active_sessions: Math.floor(Math.random() * 50),
            memory_usage: Math.floor((process.memoryUsage().rss / 1024 / 1024)),
            cpu_usage: Math.floor(Math.random() * 100)
        }
    });
});

// Error handling
app.use((err, req, res, next) => {
    console.error('Error:', err);
    res.status(500).json({
        error: 'Internal server error',
        message: err.message,
        timestamp: new Date().toISOString()
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        error: 'Endpoint not found',
        path: req.path,
        method: req.method,
        timestamp: new Date().toISOString()
    });
});

// Start server
app.listen(PORT, () => {
    console.log('🚀 MASS Framework API Server Starting...');
    console.log('=' .repeat(50));
    console.log(`🌐 Server running on http://localhost:${PORT}`);
    console.log(`📚 API Documentation: http://localhost:${PORT}/health`);
    console.log(`⚡ Mode: Node.js Backup Server`);
    console.log(`🕐 Started at: ${new Date().toISOString()}`);
    console.log('=' .repeat(50));
    console.log('Available endpoints:');
    console.log('  GET  /              - Server info');
    console.log('  GET  /health        - Health check');
    console.log('  POST /auth/login    - User login');
    console.log('  POST /auth/register - User registration');
    console.log('  GET  /api/agents    - List agents');
    console.log('  GET  /api/trades    - List trades');
    console.log('  GET  /api/status    - System status');
    console.log('  GET  /api/analytics/dashboard - Analytics');
    console.log('Press Ctrl+C to stop the server');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down server...');
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n🛑 Shutting down server...');
    process.exit(0);
});
