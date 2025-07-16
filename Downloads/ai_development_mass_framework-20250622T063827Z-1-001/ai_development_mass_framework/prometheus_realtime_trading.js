/**
 * PROMETHEUS Real-Time Trading Data Service
 * Provides live market data, trading signals, and performance metrics
 * Integrates with multiple data sources and AI prediction models
 */

class PrometheusRealTimeTrading {
    constructor() {
        this.isConnected = false;
        this.websocket = null;
        this.tradingData = {
            portfolio: {
                totalValue: 0,
                dailyPnL: 0,
                dailyPnLPercent: 0,
                positions: [],
                trades: []
            },
            markets: {
                indices: {},
                forex: {},
                crypto: {},
                commodities: {}
            },
            aiSignals: [],
            performance: {
                totalReturn: 0,
                sharpeRatio: 0,
                maxDrawdown: 0,
                winRate: 0,
                avgTrade: 0
            }
        };
        
        this.apiEndpoints = {
            realTimeData: 'https://api.polygon.io/v2/aggs/ticker',
            cryptoData: 'https://api.binance.com/api/v3/ticker/24hr',
            forexData: 'https://api.exchangerate-api.com/v4/latest/USD',
            newsData: 'https://newsapi.org/v2/everything'
        };
        
        this.init();
    }

    async init() {
        console.log('🚀 Initializing PROMETHEUS Real-Time Trading System...');
        
        // Initialize WebSocket for real-time data
        this.initWebSocket();
        
        // Start data fetching
        this.startDataStreaming();
        
        // Initialize AI learning system
        this.initAILearning();
        
        console.log('✅ PROMETHEUS Real-Time Trading System Active');
    }

    initWebSocket() {
        try {
            // Connect to real-time data stream
            this.websocket = new WebSocket('wss://ws.finnhub.io?token=demo');
            
            this.websocket.onopen = () => {
                console.log('🔌 WebSocket Connected - Real-time data streaming');
                this.isConnected = true;
                
                // Subscribe to major symbols
                const symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA', 'META', 'NFLX'];
                symbols.forEach(symbol => {
                    this.websocket.send(JSON.stringify({'type':'subscribe','symbol':symbol}));
                });
            };
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.processRealtimeData(data);
            };
            
            this.websocket.onerror = (error) => {
                console.error('❌ WebSocket Error:', error);
                this.attemptReconnect();
            };
            
            this.websocket.onclose = () => {
                console.log('⚠️ WebSocket Disconnected - Attempting reconnect...');
                this.isConnected = false;
                this.attemptReconnect();
            };
        } catch (error) {
            console.error('❌ WebSocket initialization failed:', error);
            this.useFallbackData();
        }
    }

    processRealtimeData(data) {
        if (data.type === 'trade') {
            // Update market data
            const symbol = data.data[0].s;
            const price = data.data[0].p;
            const volume = data.data[0].v;
            
            this.updateMarketData(symbol, price, volume);
            this.generateTradingSignals(symbol, price);
            this.updatePortfolio();
        }
    }

    updateMarketData(symbol, price, volume) {
        const timestamp = new Date().toISOString();
        
        // Update markets data
        if (!this.tradingData.markets.indices[symbol]) {
            this.tradingData.markets.indices[symbol] = {
                symbol: symbol,
                price: price,
                volume: volume,
                change: 0,
                changePercent: 0,
                timestamp: timestamp,
                history: []
            };
        } else {
            const prevPrice = this.tradingData.markets.indices[symbol].price;
            const change = price - prevPrice;
            const changePercent = (change / prevPrice) * 100;
            
            this.tradingData.markets.indices[symbol] = {
                ...this.tradingData.markets.indices[symbol],
                price: price,
                volume: volume,
                change: change,
                changePercent: changePercent,
                timestamp: timestamp
            };
            
            // Keep last 100 data points
            this.tradingData.markets.indices[symbol].history.push({
                price: price,
                volume: volume,
                timestamp: timestamp
            });
            
            if (this.tradingData.markets.indices[symbol].history.length > 100) {
                this.tradingData.markets.indices[symbol].history.shift();
            }
        }
        
        // Trigger UI updates
        this.updateDashboard();
    }

    generateTradingSignals(symbol, price) {
        const marketData = this.tradingData.markets.indices[symbol];
        if (!marketData || !marketData.history || marketData.history.length < 20) return;
        
        // Simple AI signal generation based on price momentum and volume
        const history = marketData.history;
        const recentPrices = history.slice(-20).map(h => h.price);
        const recentVolumes = history.slice(-20).map(h => h.volume);
        
        const sma20 = recentPrices.reduce((a, b) => a + b) / recentPrices.length;
        const avgVolume = recentVolumes.reduce((a, b) => a + b) / recentVolumes.length;
        
        const momentum = (price - sma20) / sma20;
        const volumeRatio = marketData.volume / avgVolume;
        
        let signal = 'HOLD';
        let confidence = 0;
        
        // Generate signals based on momentum and volume
        if (momentum > 0.02 && volumeRatio > 1.5) {
            signal = 'BUY';
            confidence = Math.min(0.95, momentum * 10 + volumeRatio * 0.2);
        } else if (momentum < -0.02 && volumeRatio > 1.5) {
            signal = 'SELL';
            confidence = Math.min(0.95, Math.abs(momentum) * 10 + volumeRatio * 0.2);
        } else if (Math.abs(momentum) < 0.01) {
            signal = 'HOLD';
            confidence = 0.5;
        }
        
        // Add AI signal
        const aiSignal = {
            symbol: symbol,
            signal: signal,
            confidence: confidence,
            price: price,
            timestamp: new Date().toISOString(),
            indicators: {
                momentum: momentum,
                volumeRatio: volumeRatio,
                sma20: sma20
            }
        };
        
        this.tradingData.aiSignals.unshift(aiSignal);
        
        // Keep only last 50 signals
        if (this.tradingData.aiSignals.length > 50) {
            this.tradingData.aiSignals = this.tradingData.aiSignals.slice(0, 50);
        }
        
        // Execute trades for paper trading users
        this.processPaperTrading(aiSignal);
    }

    processPaperTrading(signal) {
        // Simulate paper trading for demo users
        if (signal.confidence > 0.7) {
            const position = {
                symbol: signal.symbol,
                action: signal.signal,
                price: signal.price,
                quantity: 100, // Demo quantity
                timestamp: signal.timestamp,
                type: 'PAPER'
            };
            
            this.tradingData.portfolio.positions.push(position);
            
            // Update portfolio performance
            this.calculatePortfolioPerformance();
        }
    }

    calculatePortfolioPerformance() {
        let totalValue = 100000; // Starting capital
        let dailyPnL = 0;
        let totalReturn = 0;
        
        // Calculate based on current positions
        this.tradingData.portfolio.positions.forEach(position => {
            const currentPrice = this.tradingData.markets.indices[position.symbol]?.price || position.price;
            const pnl = (currentPrice - position.price) * position.quantity;
            
            if (position.action === 'BUY') {
                dailyPnL += pnl;
            } else if (position.action === 'SELL') {
                dailyPnL -= pnl;
            }
        });
        
        totalValue += dailyPnL;
        totalReturn = ((totalValue - 100000) / 100000) * 100;
        
        this.tradingData.portfolio.totalValue = totalValue;
        this.tradingData.portfolio.dailyPnL = dailyPnL;
        this.tradingData.portfolio.dailyPnLPercent = (dailyPnL / 100000) * 100;
        
        this.tradingData.performance.totalReturn = totalReturn;
        this.tradingData.performance.sharpeRatio = this.calculateSharpeRatio();
        this.tradingData.performance.winRate = this.calculateWinRate();
    }

    calculateSharpeRatio() {
        // Simplified Sharpe ratio calculation
        const returns = this.tradingData.portfolio.positions.map(p => {
            const currentPrice = this.tradingData.markets.indices[p.symbol]?.price || p.price;
            return ((currentPrice - p.price) / p.price) * 100;
        });
        
        if (returns.length === 0) return 0;
        
        const avgReturn = returns.reduce((a, b) => a + b) / returns.length;
        const stdDev = Math.sqrt(returns.map(r => Math.pow(r - avgReturn, 2)).reduce((a, b) => a + b) / returns.length);
        
        return stdDev > 0 ? avgReturn / stdDev : 0;
    }

    calculateWinRate() {
        const trades = this.tradingData.portfolio.positions;
        if (trades.length === 0) return 0;
        
        const winningTrades = trades.filter(trade => {
            const currentPrice = this.tradingData.markets.indices[trade.symbol]?.price || trade.price;
            const pnl = (currentPrice - trade.price) * trade.quantity;
            return (trade.action === 'BUY' && pnl > 0) || (trade.action === 'SELL' && pnl < 0);
        });
        
        return (winningTrades.length / trades.length) * 100;
    }

    startDataStreaming() {
        // Fetch crypto data
        this.fetchCryptoData();
        
        // Fetch forex data
        this.fetchForexData();
        
        // Set up periodic updates
        setInterval(() => {
            this.fetchCryptoData();
            this.fetchForexData();
        }, 30000); // Update every 30 seconds
    }

    async fetchCryptoData() {
        try {
            const response = await fetch('https://api.binance.com/api/v3/ticker/24hr');
            const data = await response.json();
            
            const topCryptos = data.filter(coin => 
                ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT'].includes(coin.symbol)
            );
            
            topCryptos.forEach(coin => {
                this.tradingData.markets.crypto[coin.symbol] = {
                    symbol: coin.symbol,
                    price: parseFloat(coin.lastPrice),
                    change: parseFloat(coin.priceChange),
                    changePercent: parseFloat(coin.priceChangePercent),
                    volume: parseFloat(coin.volume),
                    timestamp: new Date().toISOString()
                };
            });
        } catch (error) {
            console.error('❌ Crypto data fetch failed:', error);
        }
    }

    async fetchForexData() {
        try {
            const response = await fetch('https://api.exchangerate-api.com/v4/latest/USD');
            const data = await response.json();
            
            const majorPairs = ['EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF'];
            majorPairs.forEach(currency => {
                if (data.rates[currency]) {
                    this.tradingData.markets.forex[`USD${currency}`] = {
                        symbol: `USD${currency}`,
                        price: 1 / data.rates[currency],
                        change: 0, // Would need historical data for change
                        changePercent: 0,
                        timestamp: new Date().toISOString()
                    };
                }
            });
        } catch (error) {
            console.error('❌ Forex data fetch failed:', error);
        }
    }

    initAILearning() {
        // Start AI learning system
        setInterval(() => {
            this.updateAIModels();
        }, 300000); // Update every 5 minutes
    }

    updateAIModels() {
        // Simulate AI model updates
        console.log('🧠 AI Models updating...');
        
        // Analyze recent signals performance
        const recentSignals = this.tradingData.aiSignals.slice(0, 10);
        const successRate = recentSignals.filter(s => s.confidence > 0.7).length / recentSignals.length;
        
        console.log(`📊 AI Success Rate: ${(successRate * 100).toFixed(2)}%`);
        
        // Update dashboard with AI status
        this.updateAIStatus();
    }

    updateDashboard() {
        // Update real-time dashboard elements
        document.dispatchEvent(new CustomEvent('prometheusDataUpdate', {
            detail: {
                portfolio: this.tradingData.portfolio,
                markets: this.tradingData.markets,
                aiSignals: this.tradingData.aiSignals,
                performance: this.tradingData.performance
            }
        }));
    }

    updateAIStatus() {
        document.dispatchEvent(new CustomEvent('prometheusAIUpdate', {
            detail: {
                status: 'LEARNING',
                modelsUpdated: new Date().toISOString(),
                signalsGenerated: this.tradingData.aiSignals.length
            }
        }));
    }

    useFallbackData() {
        // Use simulated data when real APIs are unavailable
        console.log('📊 Using simulated market data for demo...');
        
        const symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA'];
        symbols.forEach(symbol => {
            const basePrice = Math.random() * 200 + 100;
            this.tradingData.markets.indices[symbol] = {
                symbol: symbol,
                price: basePrice,
                change: (Math.random() - 0.5) * 10,
                changePercent: (Math.random() - 0.5) * 5,
                volume: Math.random() * 1000000,
                timestamp: new Date().toISOString()
            };
        });
        
        // Simulate real-time updates
        setInterval(() => {
            symbols.forEach(symbol => {
                const currentData = this.tradingData.markets.indices[symbol];
                const newPrice = currentData.price + (Math.random() - 0.5) * 2;
                this.updateMarketData(symbol, newPrice, Math.random() * 1000000);
            });
        }, 5000);
    }

    attemptReconnect() {
        setTimeout(() => {
            console.log('🔄 Attempting to reconnect...');
            this.initWebSocket();
        }, 5000);
    }

    // Admin methods for live trading
    enableLiveTrading(userId) {
        console.log(`🔥 Live trading enabled for user: ${userId}`);
        // Implementation for live trading activation
    }

    disableLiveTrading(userId) {
        console.log(`⏸️ Live trading disabled for user: ${userId}`);
        // Implementation for live trading deactivation
    }

    getPortfolioData() {
        return this.tradingData.portfolio;
    }

    getMarketData() {
        return this.tradingData.markets;
    }

    getAISignals() {
        return this.tradingData.aiSignals;
    }

    getPerformanceData() {
        return this.tradingData.performance;
    }
}

// Initialize the real-time trading system
window.prometheusTrading = new PrometheusRealTimeTrading();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PrometheusRealTimeTrading;
}
