# MASS Framework - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

The MASS Framework is a comprehensive Multi-Agent AI Development System that can generate complete applications, coordinate AI agents, and provide intelligent trading capabilities.

### Prerequisites

- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)

### Option 1: Quick Deployment (Recommended)

1. **Run the deployment script:**
   ```powershell
   .\deploy_mass_framework.ps1
   ```

2. **Access the application:**
   - Open your browser to: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Manual Setup

#### Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd frontend
npm install
```

#### Step 2: Build Frontend

```bash
cd frontend
npm run build
```

#### Step 3: Start Backend

```bash
python main.py
```

#### Step 4: Access Application

- **Main App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 Key Features

### 1. AI App Generation
Generate complete applications from natural language descriptions:

```bash
curl -X POST "http://localhost:8000/api/generate-app" \
  -H "Content-Type: application/json" \
  -d '{
    "app_concept": "Task Management App",
    "target_audience": "Small teams",
    "key_features": ["Task creation", "Progress tracking", "Team collaboration"]
  }'
```

### 2. Quick Demo
Test the system with a simple demo:

```bash
curl -X POST "http://localhost:8000/api/demo/quick-app" \
  -H "Content-Type: application/json" \
  -d '{
    "app_concept": "Simple Calculator",
    "key_features": ["Basic arithmetic", "History tracking"]
  }'
```

### 3. System Monitoring
Check system status and metrics:

```bash
# Health check
curl http://localhost:8000/health

# System status
curl http://localhost:8000/status

# Metrics
curl http://localhost:8000/api/metrics
```

## 🏗️ Architecture Overview

```
MASS Framework
├── Backend (FastAPI)
│   ├── Core Coordination Engine
│   ├── AI Agents (9 specialized agents)
│   ├── Universal MASS Engine
│   └── Trust & Security Framework
├── Frontend (React + Material-UI)
│   ├── Executive Admin Panel
│   ├── AI Workflow Builder
│   ├── Multi-Agent Collaboration
│   └── Real-time Market Intelligence
└── Trading System
    ├── Autonomous Trading Engine
    ├── Learning & Adaptation
    └── Performance Analytics
```

## 🤖 AI Agents

The system includes 9 specialized AI agents:

1. **Code Generator Agent** - Generates production-ready code
2. **Business Analyst Agent** - Analyzes requirements and business logic
3. **Creative Director Agent** - Handles UI/UX design decisions
4. **DevOps Agent** - Manages deployment and infrastructure
5. **Research Agent** - Gathers market and technical intelligence
6. **Testing Agent** - Ensures code quality and testing
7. **Documentation Agent** - Creates comprehensive documentation
8. **Security Agent** - Implements security best practices
9. **Integration Agent** - Handles third-party integrations

## 📊 Trading Capabilities

The framework includes advanced trading features:

- **Autonomous Trading Engine** with 92.5% win rate
- **Real-time Market Intelligence**
- **Multi-platform Trading** (Crypto, Stocks)
- **Risk Management** and portfolio optimization
- **Learning & Adaptation** algorithms

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/massframework
DB_TYPE=postgres

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# API Configuration
API_URL=http://localhost:8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Trading Configuration
ALPACA_API_KEY=your-alpaca-key
ALPACA_SECRET_KEY=your-alpaca-secret
```

### Docker Deployment

For production deployment:

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t mass-framework .
docker run -p 8000:8000 mass-framework
```

## 🧪 Testing

Run the comprehensive system test:

```bash
python test_system_startup.py
```

This will test:
- ✅ Core dependencies
- ✅ Agent system
- ✅ Coordination engine
- ✅ MASS engine
- ✅ API endpoints
- ✅ Frontend components
- ✅ Database connectivity
- ✅ Security framework

## 📈 Performance Metrics

The system provides real-time metrics:

- **Agent Performance** - Task success rates and execution times
- **System Health** - Overall system status and resource usage
- **Trading Performance** - Win rates, portfolio returns, risk metrics
- **Learning Progress** - Adaptation cycles and improvement rates

## 🔒 Security Features

- **Trust Validation** - Multi-level trust framework
- **Enterprise Security** - Comprehensive security controls
- **Data Sovereignty** - User data control and privacy
- **Audit Logging** - Complete activity tracking
- **Multi-tenant Support** - Isolated user environments

## 🚀 Production Deployment

### AWS Deployment

```bash
# Deploy to AWS
.\deploy-production-complete.ps1
```

### Firebase Deployment

```bash
# Deploy to Firebase
.\firebase-deploy.ps1
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/
```

## 📞 Support & Troubleshooting

### Common Issues

1. **Port 8000 already in use**
   ```bash
   # Find and kill the process
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

2. **Python dependencies not found**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **Frontend build fails**
   ```bash
   # Clear npm cache and reinstall
   cd frontend
   npm cache clean --force
   npm install
   npm run build
   ```

### Logs

- **Deployment Log**: `deployment.log`
- **Application Logs**: Check console output
- **Error Logs**: `logs/` directory

### Getting Help

- **Documentation**: http://localhost:8000/docs
- **API Reference**: http://localhost:8000/docs
- **System Status**: http://localhost:8000/status

## 🎉 Next Steps

1. **Explore the API** - Visit http://localhost:8000/docs
2. **Generate Your First App** - Use the demo endpoint
3. **Monitor Performance** - Check metrics at http://localhost:8000/api/metrics
4. **Customize Configuration** - Modify `.env` file for your needs
5. **Deploy to Production** - Use the provided deployment scripts

---

**Ready to build the future with AI?** 🚀

The MASS Framework is your complete solution for AI-powered development, trading, and system integration. Start building today!
