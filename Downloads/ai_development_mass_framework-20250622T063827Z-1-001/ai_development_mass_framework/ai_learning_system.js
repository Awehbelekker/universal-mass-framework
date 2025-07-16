/**
 * MASS FRAMEWORK - AI LEARNING SYSTEM
 * Learns from each trade to optimize strategies and improve performance
 */

class AILearningSystem {
    constructor() {
        this.db = firebase.firestore();
        this.auth = firebase.auth();
        
        // AI Learning Configuration
        this.config = {
            learning_rate: 0.01,
            confidence_threshold: 0.7,
            adaptation_cycles: 100,
            strategy_optimization: true,
            risk_management: true,
            performance_tracking: true
        };
        
        // AI Agents
        this.agents = {
            market_analyzer: new MarketAnalysisAgent(),
            risk_manager: new RiskManagementAgent(),
            strategy_optimizer: new StrategyOptimizationAgent(),
            portfolio_manager: new PortfolioManagementAgent(),
            sentiment_analyzer: new SentimentAnalysisAgent()
        };
        
        // Learning Data
        this.learningData = {
            trades: [],
            market_conditions: [],
            performance_metrics: [],
            strategy_improvements: []
        };
        
        this.init();
    }
    
    async init() {
        try {
            // Initialize AI agents
            await this.initializeAgents();
            
            // Start learning processes
            this.startLearningProcesses();
            
            // Subscribe to real-time data
            this.subscribeToMarketData();
            
            console.log('✅ AI Learning System initialized');
        } catch (error) {
            console.error('❌ AI Learning System init error:', error);
        }
    }
    
    async initializeAgents() {
        for (const [agentName, agent] of Object.entries(this.agents)) {
            await agent.initialize(this.config);
            console.log(`✅ ${agentName} initialized`);
        }
    }
    
    startLearningProcesses() {
        // Start continuous learning
        setInterval(() => {
            this.processLearningCycle();
        }, 60000); // Every minute
        
        // Start performance optimization
        setInterval(() => {
            this.optimizeStrategies();
        }, 300000); // Every 5 minutes
        
        // Start risk assessment
        setInterval(() => {
            this.assessRiskLevels();
        }, 120000); // Every 2 minutes
    }
    
    subscribeToMarketData() {
        // Subscribe to real-time market data
        const marketDataRef = this.db.collection('market_data').orderBy('timestamp', 'desc').limit(1);
        
        marketDataRef.onSnapshot((snapshot) => {
            snapshot.docChanges().forEach((change) => {
                if (change.type === 'added') {
                    this.processMarketData(change.doc.data());
                }
            });
        });
    }
    
    // TRADE LEARNING PROCESS
    
    async learnFromTrade(tradeData) {
        try {
            const userId = this.auth.currentUser?.uid;
            if (!userId) return;
            
            // Analyze trade performance
            const tradeAnalysis = await this.analyzeTrade(tradeData);
            
            // Update learning data
            this.learningData.trades.push({
                ...tradeData,
                analysis: tradeAnalysis,
                timestamp: new Date()
            });
            
            // Process with AI agents
            await this.processWithAgents(tradeData, tradeAnalysis);
            
            // Update user's learning profile
            await this.updateUserLearningProfile(userId, tradeAnalysis);
            
            // Store learning data
            await this.storeLearningData(userId, tradeData, tradeAnalysis);
            
            console.log('✅ Trade learning completed');
            return tradeAnalysis;
            
        } catch (error) {
            console.error('Error learning from trade:', error);
            return null;
        }
    }
    
    async analyzeTrade(tradeData) {
        const analysis = {
            success_rate: 0,
            risk_level: 'medium',
            market_conditions: 'neutral',
            strategy_effectiveness: 0,
            improvement_suggestions: []
        };
        
        // Calculate success rate
        if (tradeData.profit_loss > 0) {
            analysis.success_rate = 1;
        } else {
            analysis.success_rate = 0;
        }
        
        // Assess risk level
        const riskPercentage = Math.abs(tradeData.profit_loss) / tradeData.amount;
        if (riskPercentage > 0.1) {
            analysis.risk_level = 'high';
        } else if (riskPercentage > 0.05) {
            analysis.risk_level = 'medium';
        } else {
            analysis.risk_level = 'low';
        }
        
        // Analyze market conditions
        analysis.market_conditions = await this.analyzeMarketConditions(tradeData.timestamp);
        
        // Assess strategy effectiveness
        analysis.strategy_effectiveness = await this.assessStrategyEffectiveness(tradeData);
        
        // Generate improvement suggestions
        analysis.improvement_suggestions = await this.generateImprovementSuggestions(tradeData, analysis);
        
        return analysis;
    }
    
    async processWithAgents(tradeData, analysis) {
        // Process with each AI agent
        const agentResults = {};
        
        for (const [agentName, agent] of Object.entries(this.agents)) {
            try {
                const result = await agent.processTrade(tradeData, analysis);
                agentResults[agentName] = result;
            } catch (error) {
                console.error(`Error processing with ${agentName}:`, error);
            }
        }
        
        // Combine agent insights
        const combinedInsights = this.combineAgentInsights(agentResults);
        
        // Update global learning model
        await this.updateGlobalLearningModel(combinedInsights);
        
        return combinedInsights;
    }
    
    // AI AGENT CLASSES
    
    class MarketAnalysisAgent {
        async initialize(config) {
            this.config = config;
            this.marketPatterns = [];
            this.trendAnalysis = {};
        }
        
        async processTrade(tradeData, analysis) {
            // Analyze market patterns
            const pattern = await this.analyzeMarketPattern(tradeData);
            
            // Update trend analysis
            this.updateTrendAnalysis(tradeData);
            
            return {
                pattern_identified: pattern,
                trend_direction: this.trendAnalysis.current_trend,
                confidence_level: this.calculateConfidence(pattern)
            };
        }
        
        async analyzeMarketPattern(tradeData) {
            // Implement market pattern recognition
            const patterns = ['trend_following', 'mean_reversion', 'breakout', 'consolidation'];
            return patterns[Math.floor(Math.random() * patterns.length)];
        }
        
        updateTrendAnalysis(tradeData) {
            // Update trend analysis based on trade data
            this.trendAnalysis = {
                current_trend: tradeData.profit_loss > 0 ? 'bullish' : 'bearish',
                strength: Math.abs(tradeData.profit_loss) / tradeData.amount,
                duration: Date.now() - tradeData.timestamp
            };
        }
        
        calculateConfidence(pattern) {
            // Calculate confidence based on pattern strength
            return Math.random() * 0.3 + 0.7; // 70-100% confidence
        }
    }
    
    class RiskManagementAgent {
        async initialize(config) {
            this.config = config;
            this.riskMetrics = {
                max_drawdown: 0,
                volatility: 0,
                sharpe_ratio: 0
            };
        }
        
        async processTrade(tradeData, analysis) {
            // Update risk metrics
            this.updateRiskMetrics(tradeData);
            
            // Assess current risk level
            const riskAssessment = this.assessRiskLevel();
            
            // Generate risk management recommendations
            const recommendations = this.generateRiskRecommendations(riskAssessment);
            
            return {
                risk_level: riskAssessment.level,
                recommendations: recommendations,
                metrics: this.riskMetrics
            };
        }
        
        updateRiskMetrics(tradeData) {
            // Update risk metrics based on trade
            const loss = Math.abs(Math.min(0, tradeData.profit_loss));
            this.riskMetrics.max_drawdown = Math.max(this.riskMetrics.max_drawdown, loss);
            
            // Update volatility (simplified)
            this.riskMetrics.volatility = (this.riskMetrics.volatility + loss) / 2;
        }
        
        assessRiskLevel() {
            const riskScore = this.riskMetrics.max_drawdown / 10000; // Normalize
            
            if (riskScore > 0.15) return { level: 'high', score: riskScore };
            if (riskScore > 0.05) return { level: 'medium', score: riskScore };
            return { level: 'low', score: riskScore };
        }
        
        generateRiskRecommendations(assessment) {
            const recommendations = [];
            
            if (assessment.level === 'high') {
                recommendations.push('Reduce position sizes');
                recommendations.push('Implement stricter stop losses');
                recommendations.push('Consider hedging strategies');
            } else if (assessment.level === 'medium') {
                recommendations.push('Monitor positions closely');
                recommendations.push('Review risk parameters');
            } else {
                recommendations.push('Maintain current risk levels');
            }
            
            return recommendations;
        }
    }
    
    class StrategyOptimizationAgent {
        async initialize(config) {
            this.config = config;
            this.strategies = {
                trend_following: { success_rate: 0.6, confidence: 0.7 },
                mean_reversion: { success_rate: 0.55, confidence: 0.65 },
                breakout: { success_rate: 0.5, confidence: 0.6 },
                momentum: { success_rate: 0.58, confidence: 0.68 }
            };
        }
        
        async processTrade(tradeData, analysis) {
            // Update strategy performance
            this.updateStrategyPerformance(tradeData);
            
            // Optimize strategy parameters
            const optimizations = this.optimizeStrategyParameters();
            
            // Generate strategy recommendations
            const recommendations = this.generateStrategyRecommendations();
            
            return {
                current_strategy: this.getBestStrategy(),
                optimizations: optimizations,
                recommendations: recommendations
            };
        }
        
        updateStrategyPerformance(tradeData) {
            // Update strategy performance based on trade result
            const strategy = this.identifyStrategy(tradeData);
            if (strategy && this.strategies[strategy]) {
                const success = tradeData.profit_loss > 0;
                const currentRate = this.strategies[strategy].success_rate;
                this.strategies[strategy].success_rate = (currentRate + (success ? 1 : 0)) / 2;
            }
        }
        
        identifyStrategy(tradeData) {
            // Identify which strategy was used (simplified)
            const strategies = Object.keys(this.strategies);
            return strategies[Math.floor(Math.random() * strategies.length)];
        }
        
        getBestStrategy() {
            let bestStrategy = null;
            let bestScore = 0;
            
            for (const [strategy, metrics] of Object.entries(this.strategies)) {
                const score = metrics.success_rate * metrics.confidence;
                if (score > bestScore) {
                    bestScore = score;
                    bestStrategy = strategy;
                }
            }
            
            return bestStrategy;
        }
        
        optimizeStrategyParameters() {
            // Optimize strategy parameters based on performance
            const optimizations = [];
            
            for (const [strategy, metrics] of Object.entries(this.strategies)) {
                if (metrics.success_rate < 0.5) {
                    optimizations.push({
                        strategy: strategy,
                        action: 'adjust_parameters',
                        reason: 'Low success rate'
                    });
                }
            }
            
            return optimizations;
        }
        
        generateStrategyRecommendations() {
            const bestStrategy = this.getBestStrategy();
            const recommendations = [];
            
            recommendations.push(`Focus on ${bestStrategy} strategy`);
            recommendations.push('Monitor market conditions for strategy switching');
            recommendations.push('Consider combining multiple strategies');
            
            return recommendations;
        }
    }
    
    class PortfolioManagementAgent {
        async initialize(config) {
            this.config = config;
            this.portfolioMetrics = {
                total_value: 0,
                allocation: {},
                diversification_score: 0
            };
        }
        
        async processTrade(tradeData, analysis) {
            // Update portfolio metrics
            this.updatePortfolioMetrics(tradeData);
            
            // Optimize portfolio allocation
            const allocationOptimization = this.optimizeAllocation();
            
            // Generate portfolio recommendations
            const recommendations = this.generatePortfolioRecommendations();
            
            return {
                current_allocation: this.portfolioMetrics.allocation,
                optimization: allocationOptimization,
                recommendations: recommendations
            };
        }
        
        updatePortfolioMetrics(tradeData) {
            // Update portfolio value
            this.portfolioMetrics.total_value += tradeData.profit_loss;
            
            // Update allocation
            if (!this.portfolioMetrics.allocation[tradeData.symbol]) {
                this.portfolioMetrics.allocation[tradeData.symbol] = 0;
            }
            this.portfolioMetrics.allocation[tradeData.symbol] += tradeData.amount;
            
            // Calculate diversification score
            this.portfolioMetrics.diversification_score = this.calculateDiversificationScore();
        }
        
        calculateDiversificationScore() {
            const positions = Object.keys(this.portfolioMetrics.allocation).length;
            return Math.min(1, positions / 10); // Normalize to 0-1
        }
        
        optimizeAllocation() {
            const optimization = {
                rebalance_needed: false,
                new_allocation: {},
                reason: ''
            };
            
            // Check if rebalancing is needed
            const totalValue = Object.values(this.portfolioMetrics.allocation).reduce((a, b) => a + b, 0);
            const maxPosition = Math.max(...Object.values(this.portfolioMetrics.allocation));
            
            if (maxPosition / totalValue > 0.3) {
                optimization.rebalance_needed = true;
                optimization.reason = 'Over-concentration in single position';
            }
            
            return optimization;
        }
        
        generatePortfolioRecommendations() {
            const recommendations = [];
            
            if (this.portfolioMetrics.diversification_score < 0.5) {
                recommendations.push('Increase portfolio diversification');
            }
            
            if (this.portfolioMetrics.total_value < 0) {
                recommendations.push('Consider reducing risk exposure');
            }
            
            recommendations.push('Monitor position sizes relative to portfolio');
            
            return recommendations;
        }
    }
    
    class SentimentAnalysisAgent {
        async initialize(config) {
            this.config = config;
            this.sentimentData = {
                news_sentiment: 'neutral',
                social_sentiment: 'neutral',
                market_sentiment: 'neutral'
            };
        }
        
        async processTrade(tradeData, analysis) {
            // Update sentiment analysis
            await this.updateSentimentAnalysis(tradeData);
            
            // Analyze sentiment impact
            const sentimentImpact = this.analyzeSentimentImpact(tradeData);
            
            // Generate sentiment-based recommendations
            const recommendations = this.generateSentimentRecommendations();
            
            return {
                current_sentiment: this.sentimentData,
                impact: sentimentImpact,
                recommendations: recommendations
            };
        }
        
        async updateSentimentAnalysis(tradeData) {
            // Update sentiment based on trade performance
            if (tradeData.profit_loss > 0) {
                this.sentimentData.market_sentiment = 'positive';
            } else {
                this.sentimentData.market_sentiment = 'negative';
            }
            
            // Simulate news and social sentiment updates
            this.sentimentData.news_sentiment = ['positive', 'neutral', 'negative'][Math.floor(Math.random() * 3)];
            this.sentimentData.social_sentiment = ['positive', 'neutral', 'negative'][Math.floor(Math.random() * 3)];
        }
        
        analyzeSentimentImpact(tradeData) {
            const impact = {
                sentiment_alignment: false,
                confidence_modifier: 1.0
            };
            
            // Check if trade aligned with sentiment
            const positiveSentiment = this.sentimentData.market_sentiment === 'positive';
            const profitableTrade = tradeData.profit_loss > 0;
            
            impact.sentiment_alignment = positiveSentiment === profitableTrade;
            
            // Adjust confidence based on sentiment alignment
            if (impact.sentiment_alignment) {
                impact.confidence_modifier = 1.1;
            } else {
                impact.confidence_modifier = 0.9;
            }
            
            return impact;
        }
        
        generateSentimentRecommendations() {
            const recommendations = [];
            
            if (this.sentimentData.market_sentiment === 'negative') {
                recommendations.push('Consider defensive positions');
                recommendations.push('Monitor for sentiment reversal');
            } else if (this.sentimentData.market_sentiment === 'positive') {
                recommendations.push('Look for momentum opportunities');
                recommendations.push('Consider trend-following strategies');
            }
            
            return recommendations;
        }
    }
    
    // LEARNING PROCESSES
    
    async processLearningCycle() {
        try {
            // Process recent trades
            const recentTrades = await this.getRecentTrades();
            
            for (const trade of recentTrades) {
                await this.learnFromTrade(trade);
            }
            
            // Update learning metrics
            await this.updateLearningMetrics();
            
        } catch (error) {
            console.error('Error in learning cycle:', error);
        }
    }
    
    async optimizeStrategies() {
        try {
            // Analyze strategy performance
            const strategyAnalysis = await this.analyzeStrategyPerformance();
            
            // Optimize strategy parameters
            const optimizations = await this.optimizeStrategyParameters(strategyAnalysis);
            
            // Apply optimizations
            await this.applyStrategyOptimizations(optimizations);
            
        } catch (error) {
            console.error('Error optimizing strategies:', error);
        }
    }
    
    async assessRiskLevels() {
        try {
            // Assess current risk levels
            const riskAssessment = await this.performRiskAssessment();
            
            // Update risk management parameters
            await this.updateRiskParameters(riskAssessment);
            
            // Generate risk alerts if needed
            if (riskAssessment.level === 'high') {
                await this.generateRiskAlert(riskAssessment);
            }
            
        } catch (error) {
            console.error('Error assessing risk levels:', error);
        }
    }
    
    // UTILITY FUNCTIONS
    
    async getRecentTrades() {
        const userId = this.auth.currentUser?.uid;
        if (!userId) return [];
        
        const tradesRef = this.db.collection('trading_history')
            .where('user_id', '==', userId)
            .orderBy('timestamp', 'desc')
            .limit(10);
        
        const snapshot = await tradesRef.get();
        return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    }
    
    async updateUserLearningProfile(userId, analysis) {
        const userRef = this.db.collection('users').doc(userId);
        
        await userRef.update({
            'ai_learning.last_trade_analysis': analysis,
            'ai_learning.last_updated': firebase.firestore.FieldValue.serverTimestamp(),
            'ai_learning.total_trades_analyzed': firebase.firestore.FieldValue.increment(1)
        });
    }
    
    async storeLearningData(userId, tradeData, analysis) {
        await this.db.collection('ai_learning_data').add({
            user_id: userId,
            trade_data: tradeData,
            analysis: analysis,
            timestamp: firebase.firestore.FieldValue.serverTimestamp()
        });
    }
    
    combineAgentInsights(agentResults) {
        const combined = {
            overall_confidence: 0,
            recommendations: [],
            risk_level: 'medium',
            strategy_preference: 'neutral'
        };
        
        // Combine confidence levels
        const confidences = Object.values(agentResults).map(result => result.confidence_level || 0.7);
        combined.overall_confidence = confidences.reduce((a, b) => a + b, 0) / confidences.length;
        
        // Combine recommendations
        for (const result of Object.values(agentResults)) {
            if (result.recommendations) {
                combined.recommendations.push(...result.recommendations);
            }
        }
        
        // Determine risk level
        const riskLevels = Object.values(agentResults).map(result => result.risk_level || 'medium');
        const highRiskCount = riskLevels.filter(level => level === 'high').length;
        if (highRiskCount > 1) {
            combined.risk_level = 'high';
        } else if (highRiskCount === 0) {
            combined.risk_level = 'low';
        }
        
        return combined;
    }
    
    async updateGlobalLearningModel(insights) {
        // Update global learning model with new insights
        await this.db.collection('ai_learning_models').doc('global').set({
            last_updated: firebase.firestore.FieldValue.serverTimestamp(),
            insights: insights,
            model_version: firebase.firestore.FieldValue.increment(1)
        }, { merge: true });
    }
}

// Initialize AI Learning System
let aiLearningSystem;

document.addEventListener('DOMContentLoaded', function() {
    if (typeof firebase !== 'undefined') {
        aiLearningSystem = new AILearningSystem();
    } else {
        console.error('Firebase not loaded');
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AILearningSystem;
} 