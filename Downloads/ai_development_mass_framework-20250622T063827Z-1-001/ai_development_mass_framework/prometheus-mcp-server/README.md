# PROMETHEUS MCP Server

> **AI-Powered Trading Platform with Neural Forge™ Technology**

A comprehensive Model Context Protocol (MCP) server implementation for the PROMETHEUS trading platform, enabling seamless AI-driven trading operations through Claude and other AI assistants.

## 🚀 Features

### Core Capabilities
- **Portfolio Management** - Real-time portfolio tracking and performance analytics
- **Market Data** - Live quotes, historical data, and market analysis
- **Trading Operations** - Order execution, position management, and risk controls
- **Neural Forge™** - AI-powered strategy creation and optimization
- **Risk Management** - Advanced risk assessment and position sizing

### Technical Features
- **MCP Protocol** - Full Model Context Protocol implementation
- **Authentication** - JWT-based security with API key validation
- **Caching** - Redis-based high-performance caching layer
- **Logging** - Structured logging with Winston
- **TypeScript** - Full type safety and modern JavaScript features
- **Testing** - Comprehensive test suite with Jest

## 📋 Requirements

- Node.js 18.0.0 or higher
- Redis 6.0.0 or higher
- TypeScript 5.0.0 or higher

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/prometheus-trading/mcp-server.git
cd prometheus-mcp-server

# Install dependencies
npm install

# Build the project
npm run build

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
# Server Configuration
PORT=3000
HOST=0.0.0.0
NODE_ENV=production

# Authentication
JWT_SECRET=your-jwt-secret-here
JWT_EXPIRATION=24h
API_KEY=your-api-key-here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
REDIS_DB=0

# Trading API
PROMETHEUS_API_BASE_URL=https://api.prometheus-trading.com
PROMETHEUS_API_KEY=your-prometheus-api-key

# Logging
LOG_LEVEL=info
LOG_FILE=/var/log/prometheus-mcp-server.log

# Neural Forge
NEURAL_FORGE_ENABLED=true
NEURAL_FORGE_MODEL_PATH=/models/neural-forge
```

## 🚀 Usage

### Development Mode
```bash
npm run dev
```

### Production Mode
```bash
npm start
```

### Running Tests
```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## 🔧 API Endpoints

### Authentication
- `POST /auth/login` - User authentication
- `POST /auth/refresh` - Token refresh
- `POST /auth/logout` - User logout

### Portfolio Management
- `POST /api/v1/tools/portfolio/balance` - Get portfolio balance
- `POST /api/v1/tools/portfolio/positions` - Get positions
- `POST /api/v1/tools/portfolio/performance` - Get performance metrics

### Market Data
- `POST /api/v1/tools/market-data/quotes` - Get real-time quotes
- `POST /api/v1/tools/market-data/historical` - Get historical data
- `POST /api/v1/tools/market-data/news` - Get market news

### Trading Operations
- `POST /api/v1/tools/trading/order` - Place order
- `POST /api/v1/tools/trading/cancel-order` - Cancel order
- `POST /api/v1/tools/trading/order-status` - Get order status

### Neural Forge
- `POST /api/v1/tools/neural-forge/strategy` - Create strategy
- `POST /api/v1/tools/neural-forge/backtest` - Backtest strategy
- `POST /api/v1/tools/neural-forge/optimize` - Optimize strategy

### Risk Management
- `POST /api/v1/tools/risk-management/calculate-risk` - Calculate portfolio risk
- `POST /api/v1/tools/risk-management/set-limits` - Set risk limits
- `POST /api/v1/tools/risk-management/alerts` - Get risk alerts

## 🏗️ Architecture

### Core Components

```
src/
├── server.ts              # Main MCP server implementation
├── auth/
│   └── middleware.ts      # JWT authentication middleware
├── config/
│   └── default.ts         # Default configuration
├── tools/
│   ├── portfolio.ts       # Portfolio management tools
│   ├── market-data.ts     # Market data tools
│   ├── trading.ts         # Trading operation tools
│   ├── neural-forge.ts    # Neural Forge AI tools
│   └── risk-management.ts # Risk management tools
├── utils/
│   ├── cache.ts           # Redis cache utility
│   └── logger.ts          # Winston logger utility
└── types/
    └── index.ts           # TypeScript type definitions
```

### MCP Protocol Integration

The server implements the Model Context Protocol specification:

- **Tools** - Executable functions for trading operations
- **Resources** - Data sources and real-time information
- **Subscriptions** - Real-time event streaming
- **Authentication** - Secure access control

## 🔐 Security

### Authentication Flow
1. User authenticates with username/password
2. Server issues JWT token
3. Client includes token in Authorization header
4. Server validates token and permissions

### Security Features
- JWT-based authentication
- API key validation
- Rate limiting
- Input validation
- Audit logging
- Environment-based configuration

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:3000/health
```

### Metrics
- Request rate and response times
- Error rates and types
- Redis cache performance
- Memory and CPU usage
- Active connections

## 🧪 Testing

### Unit Tests
```bash
npm run test:unit
```

### Integration Tests
```bash
npm run test:integration
```

### Load Testing
```bash
npm run test:load
```

## 🐳 Docker Deployment

```bash
# Build Docker image
docker build -t prometheus-mcp-server .

# Run container
docker run -p 3000:3000 \
  -e JWT_SECRET=your-secret \
  -e REDIS_HOST=redis \
  prometheus-mcp-server
```

### Docker Compose
```yaml
version: '3.8'
services:
  prometheus-mcp-server:
    build: .
    ports:
      - "3000:3000"
    environment:
      - JWT_SECRET=your-secret
      - REDIS_HOST=redis
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [PROMETHEUS Trading Platform](https://prometheus-trading.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Neural Forge™ Documentation](https://docs.prometheus-trading.com/neural-forge)

## 📞 Support

For support and questions:
- Email: support@prometheus-trading.com
- Discord: [PROMETHEUS Community](https://discord.gg/prometheus)
- Documentation: [docs.prometheus-trading.com](https://docs.prometheus-trading.com)

---

**Built with ❤️ by the PROMETHEUS Trading Team**
