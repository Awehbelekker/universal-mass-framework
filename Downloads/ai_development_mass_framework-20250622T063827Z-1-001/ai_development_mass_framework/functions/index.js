const functions = require('firebase-functions');
const admin = require('firebase-admin');
const express = require('express');
const cors = require('cors');

// Initialize Firebase Admin
admin.initializeApp();
const db = admin.firestore();
const auth = admin.auth();

// Create Express app
const app = express();
app.use(cors({ origin: true }));
app.use(express.json());

// Middleware to verify Firebase Auth token
const verifyToken = async (req, res, next) => {
  try {
    const token = req.headers.authorization?.split('Bearer ')[1];
    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }
    
    const decodedToken = await auth.verifyIdToken(token);
    req.user = decodedToken;
    next();
  } catch (error) {
    console.error('Token verification error:', error);
    res.status(401).json({ error: 'Invalid token' });
  }
};

// API Routes

// Get user profile
app.get('/api/user/profile', verifyToken, async (req, res) => {
  try {
    const userDoc = await db.collection('users').doc(req.user.uid).get();
    if (!userDoc.exists) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(userDoc.data());
  } catch (error) {
    console.error('Error getting user profile:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update user profile
app.put('/api/user/profile', verifyToken, async (req, res) => {
  try {
    const { displayName, preferences } = req.body;
    await db.collection('users').doc(req.user.uid).update({
      displayName,
      preferences,
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });
    res.json({ success: true });
  } catch (error) {
    console.error('Error updating user profile:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get AI agents
app.get('/api/agents', verifyToken, async (req, res) => {
  try {
    const agentsSnapshot = await db.collection('agents')
      .where('owner', '==', req.user.uid)
      .orderBy('createdAt', 'desc')
      .get();
    
    const agents = [];
    agentsSnapshot.forEach(doc => {
      agents.push({ id: doc.id, ...doc.data() });
    });
    
    res.json({ agents });
  } catch (error) {
    console.error('Error getting agents:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create new AI agent
app.post('/api/agents', verifyToken, async (req, res) => {
  try {
    const { name, type, description, config } = req.body;
    
    const agentData = {
      name,
      type,
      description,
      config,
      owner: req.user.uid,
      status: 'inactive',
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    };
    
    const docRef = await db.collection('agents').add(agentData);
    res.json({ id: docRef.id, ...agentData });
  } catch (error) {
    console.error('Error creating agent:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update AI agent
app.put('/api/agents/:id', verifyToken, async (req, res) => {
  try {
    const agentId = req.params.id;
    const updates = req.body;
    
    // Verify ownership
    const agentDoc = await db.collection('agents').doc(agentId).get();
    if (!agentDoc.exists || agentDoc.data().owner !== req.user.uid) {
      return res.status(403).json({ error: 'Access denied' });
    }
    
    await db.collection('agents').doc(agentId).update({
      ...updates,
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });
    
    res.json({ success: true });
  } catch (error) {
    console.error('Error updating agent:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Delete AI agent
app.delete('/api/agents/:id', verifyToken, async (req, res) => {
  try {
    const agentId = req.params.id;
    
    // Verify ownership
    const agentDoc = await db.collection('agents').doc(agentId).get();
    if (!agentDoc.exists || agentDoc.data().owner !== req.user.uid) {
      return res.status(403).json({ error: 'Access denied' });
    }
    
    await db.collection('agents').doc(agentId).delete();
    res.json({ success: true });
  } catch (error) {
    console.error('Error deleting agent:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get workflows
app.get('/api/workflows', verifyToken, async (req, res) => {
  try {
    const workflowsSnapshot = await db.collection('workflows')
      .where('owner', '==', req.user.uid)
      .orderBy('createdAt', 'desc')
      .get();
    
    const workflows = [];
    workflowsSnapshot.forEach(doc => {
      workflows.push({ id: doc.id, ...doc.data() });
    });
    
    res.json({ workflows });
  } catch (error) {
    console.error('Error getting workflows:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create new workflow
app.post('/api/workflows', verifyToken, async (req, res) => {
  try {
    const { name, description, steps, triggers } = req.body;
    
    const workflowData = {
      name,
      description,
      steps,
      triggers,
      owner: req.user.uid,
      status: 'draft',
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    };
    
    const docRef = await db.collection('workflows').add(workflowData);
    res.json({ id: docRef.id, ...workflowData });
  } catch (error) {
    console.error('Error creating workflow:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Execute workflow
app.post('/api/workflows/:id/execute', verifyToken, async (req, res) => {
  try {
    const workflowId = req.params.id;
    const { input } = req.body;
    
    // Verify ownership
    const workflowDoc = await db.collection('workflows').doc(workflowId).get();
    if (!workflowDoc.exists || workflowDoc.data().owner !== req.user.uid) {
      return res.status(403).json({ error: 'Access denied' });
    }
    
    const workflow = workflowDoc.data();
    
    // Create execution record
    const executionData = {
      workflowId,
      status: 'running',
      input,
      startedAt: admin.firestore.FieldValue.serverTimestamp(),
      userId: req.user.uid
    };
    
    const executionRef = await db.collection('workflow_executions').add(executionData);
    
    // TODO: Implement actual workflow execution logic
    // For now, simulate execution
    setTimeout(async () => {
      await executionRef.update({
        status: 'completed',
        output: { message: 'Workflow executed successfully' },
        completedAt: admin.firestore.FieldValue.serverTimestamp()
      });
    }, 2000);
    
    res.json({ executionId: executionRef.id, status: 'started' });
  } catch (error) {
    console.error('Error executing workflow:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Chat API
app.post('/api/chat/send', verifyToken, async (req, res) => {
  try {
    const { message, sessionId } = req.body;
    
    // Create or get chat session
    let sessionRef;
    if (sessionId) {
      sessionRef = db.collection('chat_sessions').doc(sessionId);
      const sessionDoc = await sessionRef.get();
      if (!sessionDoc.exists || !sessionDoc.data().participants[req.user.uid]) {
        return res.status(403).json({ error: 'Access denied' });
      }
    } else {
      sessionRef = db.collection('chat_sessions').doc();
      await sessionRef.set({
        participants: { [req.user.uid]: true },
        createdAt: admin.firestore.FieldValue.serverTimestamp(),
        lastActivity: admin.firestore.FieldValue.serverTimestamp()
      });
    }
    
    // Add message
    const messageData = {
      text: message,
      userId: req.user.uid,
      timestamp: admin.firestore.FieldValue.serverTimestamp(),
      type: 'user'
    };
    
    await sessionRef.collection('messages').add(messageData);
    
    // TODO: Integrate with AI service for response
    // For now, simulate AI response
    setTimeout(async () => {
      const aiResponse = {
        text: `I received your message: "${message}". How can I assist you further?`,
        userId: 'ai-agent',
        timestamp: admin.firestore.FieldValue.serverTimestamp(),
        type: 'ai'
      };
      await sessionRef.collection('messages').add(aiResponse);
    }, 1000);
    
    res.json({ sessionId: sessionRef.id, success: true });
  } catch (error) {
    console.error('Error sending message:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get chat messages
app.get('/api/chat/:sessionId/messages', verifyToken, async (req, res) => {
  try {
    const sessionId = req.params.sessionId;
    
    // Verify access to session
    const sessionDoc = await db.collection('chat_sessions').doc(sessionId).get();
    if (!sessionDoc.exists || !sessionDoc.data().participants[req.user.uid]) {
      return res.status(403).json({ error: 'Access denied' });
    }
    
    const messagesSnapshot = await db.collection('chat_sessions')
      .doc(sessionId)
      .collection('messages')
      .orderBy('timestamp', 'asc')
      .limit(100)
      .get();
    
    const messages = [];
    messagesSnapshot.forEach(doc => {
      messages.push({ id: doc.id, ...doc.data() });
    });
    
    res.json({ messages });
  } catch (error) {
    console.error('Error getting messages:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Analytics
app.get('/api/analytics/dashboard', verifyToken, async (req, res) => {
  try {
    // Get user's analytics data
    const analyticsSnapshot = await db.collection('analytics')
      .where('userId', '==', req.user.uid)
      .orderBy('timestamp', 'desc')
      .limit(30)
      .get();
    
    const analytics = [];
    analyticsSnapshot.forEach(doc => {
      analytics.push(doc.data());
    });
    
    // Calculate summary stats
    const totalAgents = (await db.collection('agents').where('owner', '==', req.user.uid).get()).size;
    const totalWorkflows = (await db.collection('workflows').where('owner', '==', req.user.uid).get()).size;
    const totalExecutions = (await db.collection('workflow_executions').where('userId', '==', req.user.uid).get()).size;
    
    res.json({
      summary: {
        totalAgents,
        totalWorkflows,
        totalExecutions,
        lastActivity: new Date()
      },
      analytics
    });
  } catch (error) {
    console.error('Error getting analytics:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Log analytics event
app.post('/api/analytics/event', verifyToken, async (req, res) => {
  try {
    const { event, data } = req.body;
    
    await db.collection('analytics').add({
      event,
      data,
      userId: req.user.uid,
      timestamp: admin.firestore.FieldValue.serverTimestamp()
    });
    
    res.json({ success: true });
  } catch (error) {
    console.error('Error logging analytics:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    service: 'MASS Framework API'
  });
});

// Export the Express app as a Firebase Function
exports.api = functions.https.onRequest(app);

// Cloud function to initialize demo data
exports.initializeDemoData = functions.auth.user().onCreate(async (user) => {
  try {
    // Create user profile
    await db.collection('users').doc(user.uid).set({
      email: user.email,
      displayName: user.displayName || 'New User',
      role: 'user',
      plan: 'free',
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
      preferences: {
        theme: 'light',
        notifications: true
      }
    });
    
    // Create demo agents
    const demoAgents = [
      {
        name: 'Business Analyst',
        type: 'business',
        description: 'Analyzes business requirements and generates specifications',
        config: { model: 'gpt-4', temperature: 0.7 },
        owner: user.uid,
        status: 'active',
        createdAt: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        name: 'Code Generator',
        type: 'development',
        description: 'Generates code based on specifications',
        config: { model: 'gpt-4', temperature: 0.3 },
        owner: user.uid,
        status: 'active',
        createdAt: admin.firestore.FieldValue.serverTimestamp()
      }
    ];
    
    for (const agent of demoAgents) {
      await db.collection('agents').add(agent);
    }
    
    // Create demo workflow
    await db.collection('workflows').add({
      name: 'Welcome Workflow',
      description: 'A sample workflow to get you started',
      steps: [
        { id: 1, type: 'trigger', name: 'Manual Start' },
        { id: 2, type: 'agent', name: 'Greet User', agentType: 'business' },
        { id: 3, type: 'action', name: 'Send Welcome Email' }
      ],
      triggers: ['manual'],
      owner: user.uid,
      status: 'active',
      createdAt: admin.firestore.FieldValue.serverTimestamp()
    });
    
    console.log('Demo data initialized for user:', user.uid);
  } catch (error) {
    console.error('Error initializing demo data:', error);
  }
});

// Cleanup function for deleted users
exports.cleanupUserData = functions.auth.user().onDelete(async (user) => {
  try {
    const batch = db.batch();
    
    // Delete user profile
    batch.delete(db.collection('users').doc(user.uid));
    
    // Delete user's agents
    const agentsSnapshot = await db.collection('agents').where('owner', '==', user.uid).get();
    agentsSnapshot.forEach(doc => batch.delete(doc.ref));
    
    // Delete user's workflows
    const workflowsSnapshot = await db.collection('workflows').where('owner', '==', user.uid).get();
    workflowsSnapshot.forEach(doc => batch.delete(doc.ref));
    
    // Delete user's analytics
    const analyticsSnapshot = await db.collection('analytics').where('userId', '==', user.uid).get();
    analyticsSnapshot.forEach(doc => batch.delete(doc.ref));
    
    await batch.commit();
    console.log('User data cleaned up for:', user.uid);
  } catch (error) {
    console.error('Error cleaning up user data:', error);
  }
});
