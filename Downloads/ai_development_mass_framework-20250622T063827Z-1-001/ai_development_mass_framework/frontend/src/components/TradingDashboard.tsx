import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  Grid, 
  Button, 
  Chip,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Alert,
  Badge,
  Tooltip,
  Divider
} from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
  Filler,
} from 'chart.js';
import {
  PlayArrow,
  Stop,
  TrendingUp,
  TrendingDown,
  Assessment,
  ShowChart,
  SmartToy,
  Whatshot
} from '@mui/icons-material';

// Register Chart.js components globally
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ChartTooltip,
  Legend,
  Filler
);

interface TradeData {
  id: string;
  symbol: string;
  action: 'BUY' | 'SELL';
  quantity: number;
  price: number;
  timestamp: string;
  profit_loss: number;
  status: 'EXECUTED' | 'PENDING' | 'CANCELLED';
  ai_confidence: number;
  strategy: string;
  market_condition: string;
}

interface TradingState {
  status: 'IDLE' | 'ANALYZING' | 'BUYING' | 'SELLING' | 'HOLDING' | 'STOPPED';
  current_analysis: string;
  next_action: string;
  ai_state: string;
  last_update: string;
}

interface Position {
  symbol: string;
  quantity: number;
  avg_price: number;
  current_price: number;
  unrealized_pnl: number;
  percentage_change: number;
}

interface AIAgent {
  id: string;
  name: string;
  role: string;
  status: 'active' | 'idle' | 'training';
  performance: number;
  confidence: number;
  lastAction: string;
  successRate: number;
}

interface MarketInsight {
  symbol: string;
  insight: string;
  source: string;
  confidence: number;
  timestamp: string;
}

const TradingDashboard: React.FC = () => {
  // Basic trading state
  const [isTrading, setIsTrading] = useState(false);
  const [trialActive, setTrialActive] = useState(false);
  const [trialTimeRemaining, setTrialTimeRemaining] = useState(48 * 60 * 60);
  const [trades, setTrades] = useState<TradeData[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);
  const [tradingState, setTradingState] = useState<TradingState>({
    status: 'IDLE',
    current_analysis: 'Waiting for market data...',
    next_action: 'None',
    ai_state: 'Initializing',
    last_update: new Date().toLocaleTimeString()
  });
  
  // Portfolio metrics
  const [portfolioValue, setPortfolioValue] = useState(10000);
  const [totalPnL, setTotalPnL] = useState(0);
  const [totalTrades, setTotalTrades] = useState(0);
  const [profitableTrades, setProfitableTrades] = useState(0);
  const [portfolioHistory, setPortfolioHistory] = useState<number[]>([10000]);
  const [dailyChange, setDailyChange] = useState(0);
  const [weeklyChange, setWeeklyChange] = useState(0);
  const [monthlyChange, setMonthlyChange] = useState(0);
  
  // Enhanced metrics for an advanced dashboard
  const [riskScore, setRiskScore] = useState<number>(65); // 0-100
  const [tradingFrequency, setTradingFrequency] = useState<number>(0);
  const [avgTradeProfit, setAvgTradeProfit] = useState<number>(0);
  const [marketSentiment, setMarketSentiment] = useState<number>(0); // -1 to 1
  const [traderRanking, setTraderRanking] = useState<number>(0); // Percentile
  
  // AI Agents integration
  const [activeAgents, setActiveAgents] = useState<AIAgent[]>([
    {
      id: 'agent-1',
      name: 'Alpha Seeker',
      role: 'Market Analysis',
      status: 'active',
      performance: 8.2,
      confidence: 0.85,
      lastAction: 'Analyzing market trends',
      successRate: 0.78
    },
    {
      id: 'agent-2',
      name: 'Risk Manager',
      role: 'Risk Assessment',
      status: 'active',
      performance: 9.1,
      confidence: 0.92,
      lastAction: 'Optimizing position sizing',
      successRate: 0.94
    },
    {
      id: 'agent-3', 
      name: 'Sentiment Analyzer',
      role: 'News & Social Media',
      status: 'active',
      performance: 7.5,
      confidence: 0.77,
      lastAction: 'Processing market news',
      successRate: 0.71
    }
  ]);
  
  // Market insights from AI
  const [marketInsights, setMarketInsights] = useState<MarketInsight[]>([]);
  
  // Live trading state
  const [isLiveTrading, setIsLiveTrading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [liveResults, setLiveResults] = useState<string[]>([]);

  const simulateTradingActivity = () => {
    const symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NVDA'];
    const actions = ['BUY', 'SELL'] as const;
    const strategies = ['Momentum', 'Mean Reversion', 'Technical Analysis', 'News Sentiment'];
    const conditions = ['Bullish', 'Bearish', 'Neutral', 'Volatile'];

    // Update trading state
    const states = ['ANALYZING', 'BUYING', 'SELLING', 'HOLDING'] as const;
    const currentState = states[Math.floor(Math.random() * states.length)];
    
    setTradingState(prev => ({
      ...prev,
      status: currentState,
      current_analysis: generateAnalysis(currentState),
      next_action: generateNextAction(currentState),
      ai_state: generateAIState(currentState),
      last_update: new Date().toLocaleTimeString()
    }));

    // Generate new trade occasionally
    if (Math.random() < 0.4) { // 40% chance of new trade
      const symbol = symbols[Math.floor(Math.random() * symbols.length)];
      const action = actions[Math.floor(Math.random() * actions.length)];
      const quantity = Math.floor(Math.random() * 100) + 1;
      const price = Math.random() * 200 + 50; // Price between $50-$250
      const confidence = Math.random() * 40 + 60; // 60-100% confidence
      const profitLoss = (Math.random() - 0.5) * 200; // Random P&L

      const newTrade: TradeData = {
        id: Date.now().toString(),
        symbol,
        action,
        quantity,
        price,
        timestamp: new Date().toLocaleString(),
        profit_loss: profitLoss,
        status: Math.random() > 0.1 ? 'EXECUTED' : 'PENDING',
        ai_confidence: confidence,
        strategy: strategies[Math.floor(Math.random() * strategies.length)],
        market_condition: conditions[Math.floor(Math.random() * conditions.length)]
      };

      setTrades(prev => [newTrade, ...prev.slice(0, 19)]); // Keep last 20 trades
      
      // Update statistics
      setTotalTrades(prev => prev + 1);
      if (profitLoss > 0) {
        setProfitableTrades(prev => prev + 1);
      }
      setTotalPnL(prev => prev + profitLoss);

      // Update positions
      updatePositions(newTrade);
    }
  };

  const updatePositions = (trade: TradeData) => {
    setPositions(prev => {
      const existingIndex = prev.findIndex(p => p.symbol === trade.symbol);
      const currentPrice = trade.price + (Math.random() - 0.5) * 5; // Simulate price movement

      if (existingIndex >= 0) {
        const updated = [...prev];
        const existing = updated[existingIndex];
        
        if (trade.action === 'BUY') {
          const newQuantity = existing.quantity + trade.quantity;
          const newAvgPrice = ((existing.avg_price * existing.quantity) + (trade.price * trade.quantity)) / newQuantity;
          updated[existingIndex] = {
            ...existing,
            quantity: newQuantity,
            avg_price: newAvgPrice,
            current_price: currentPrice,
            unrealized_pnl: (currentPrice - newAvgPrice) * newQuantity,
            percentage_change: ((currentPrice - newAvgPrice) / newAvgPrice) * 100
          };
        } else {
          const newQuantity = existing.quantity - trade.quantity;
          if (newQuantity <= 0) {
            updated.splice(existingIndex, 1);
          } else {
            updated[existingIndex] = {
              ...existing,
              quantity: newQuantity,
              current_price: currentPrice,
              unrealized_pnl: (currentPrice - existing.avg_price) * newQuantity,
              percentage_change: ((currentPrice - existing.avg_price) / existing.avg_price) * 100
            };
          }
        }
        return updated;
      } else if (trade.action === 'BUY') {
        return [...prev, {
          symbol: trade.symbol,
          quantity: trade.quantity,
          avg_price: trade.price,
          current_price: currentPrice,
          unrealized_pnl: (currentPrice - trade.price) * trade.quantity,
          percentage_change: ((currentPrice - trade.price) / trade.price) * 100
        }];
      }
      return prev;
    });
  };

  const updatePortfolioValue = () => {
    const change = (Math.random() - 0.48) * 100; // Slight upward bias
    setPortfolioValue(prev => {
      const newValue = Math.max(prev + change, 1000); // Don't go below $1000
      setPortfolioHistory(prevHistory => {
        const newHistory = [...prevHistory, newValue];
        return newHistory.slice(-50); // Keep last 50 data points
      });
      return newValue;
    });
  };

  const generateMarketInsights = () => {
    const symbols = ['BTC/USD', 'ETH/USD', 'SPY', 'AAPL', 'MSFT', 'TSLA', 'NVDA', 'AMZN'];
    const sources = ['Technical Analysis', 'Social Sentiment', 'News Analysis', 'Volume Patterns', 'Price Action'];
    const insights = [
      'Strong bullish divergence detected',
      'Unusual trading volume spike',
      'Positive sentiment shift on social media',
      'Institutional buying pressure increasing',
      'Support level held after multiple tests',
      'Negative earnings reaction expected',
      'Breakout above resistance with volume confirmation',
      'Overbought conditions with bearish momentum'
    ];
    const newInsights: MarketInsight[] = [];
    const count = 1 + Math.floor(Math.random() * 3); // 1-3 new insights
    for (let i = 0; i < count; i++) {
      const symbol = symbols[Math.floor(Math.random() * symbols.length)];
      const source = sources[Math.floor(Math.random() * sources.length)];
      const insight = insights[Math.floor(Math.random() * insights.length)];
      newInsights.push({
        symbol,
        insight,
        source,
        confidence: 0.6 + Math.random() * 0.35, // 0.6 - 0.95
        timestamp: new Date().toISOString()
      });
    }
    setMarketInsights(prev => [...newInsights, ...prev].slice(0, 10)); // Keep last 10 insights
    setMarketSentiment((Math.random() * 2) - 1); // -1 to 1
  };

  const updateAIAgents = () => {
    setActiveAgents(prev => prev.map(agent => {
      // 15% chance to change status
      const newStatus = Math.random() > 0.85 
        ? (['active', 'idle', 'training'] as const)[Math.floor(Math.random() * 3)] 
        : agent.status;
      // New performance value (slight change)
      const perfChange = (Math.random() - 0.5) * 0.5;
      const newPerformance = Math.min(10, Math.max(1, agent.performance + perfChange));
      // New confidence level (slight change)
      const confChange = (Math.random() - 0.5) * 0.1;
      const newConfidence = Math.min(0.99, Math.max(0.5, agent.confidence + confChange));
      // New last action
      const actions = [
        'Analyzing market trends', 
        'Processing market data', 
        'Optimizing trading parameters',
        'Evaluating risk factors',
        'Scanning for trading opportunities',
        'Learning from recent trades'
      ];
      const newAction = Math.random() > 0.7 
        ? actions[Math.floor(Math.random() * actions.length)]
        : agent.lastAction;
      return {
        ...agent,
        status: newStatus,
        performance: newPerformance,
        confidence: newConfidence,
        lastAction: newAction,
        successRate: Math.min(0.99, Math.max(0.5, agent.successRate + (Math.random() - 0.5) * 0.05))
      };
    }));
  };

  const updateAdvancedMetrics = () => {
    setRiskScore(prev => Math.min(100, Math.max(0, prev + (Math.random() - 0.5) * 10)));
    setTradingFrequency(0.5 + Math.random() * 4.5); // 0.5 to 5 trades per hour
    const avgProfit = (totalPnL / (totalTrades || 1));
    setAvgTradeProfit(avgProfit);
    setTraderRanking(Math.min(100, Math.max(1, 70 + (Math.random() - 0.5) * 20)));
    const lastValue = portfolioHistory.length > 0 ? portfolioHistory[portfolioHistory.length - 1] : 10000;
    const dailyValue = portfolioHistory.length > 24 ? portfolioHistory[portfolioHistory.length - 24] : 10000;
    const weeklyValue = portfolioHistory.length > 168 ? portfolioHistory[portfolioHistory.length - 168] : 10000;
    const monthlyValue = portfolioHistory.length > 720 ? portfolioHistory[portfolioHistory.length - 720] : 10000;
    setDailyChange(((lastValue - dailyValue) / dailyValue) * 100);
    setWeeklyChange(((lastValue - weeklyValue) / weeklyValue) * 100);
    setMonthlyChange(((lastValue - monthlyValue) / monthlyValue) * 100);
  };

  // Simulate real-time trading activity
  useEffect(() => {
    if (!isTrading) return;

    const interval = setInterval(() => {
      simulateTradingActivity();
      updatePortfolioValue();
      
      // Also update AI-related data
      if (Math.random() > 0.7) generateMarketInsights();
      if (Math.random() > 0.8) updateAIAgents();
      updateAdvancedMetrics();
    }, 3000); // Update every 3 seconds

    return () => clearInterval(interval);
  }, [isTrading]);

  // Trial countdown timer
  useEffect(() => {
    if (!trialActive) return;

    const timer = setInterval(() => {
      setTrialTimeRemaining((prev) => {
        if (prev <= 1) {
          setTrialActive(false);
          setIsTrading(false);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [trialActive]);

  // Function to start live trading (real money)
  const startLiveTrading = async () => {
    setIsLoading(true);
    setApiError(null);
    
    try {
      // Get token from localStorage
      const token = localStorage.getItem('auth_token');
      if (!token) {
        throw new Error('Authentication required. Please log in again.');
      }
      
      // Call the API to start trading (using relative URL for compatibility with all environments)
      const response = await fetch('/api/trading/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        if (response.status === 503) {
          const errorData = await response.json().catch(() => ({ detail: 'Trading system not available' }));
          const message = errorData.detail || 'This is a demo environment. Live trading is not available.';
          throw new Error(message);
        }
        const errorData = await response.text();
        throw new Error(`Failed to start live trading: ${response.status} ${errorData}`);
      }
      
      const data = await response.json();
      setIsLiveTrading(true);
      setLiveResults(prev => [...prev, `[${new Date().toLocaleTimeString()}] Live trading started successfully.`]);
      
    } catch (error) {
      console.error('Error starting live trading:', error);
      setApiError(error instanceof Error ? error.message : 'Failed to start live trading. Please try again later.');
      setLiveResults(prev => [...prev, `[${new Date().toLocaleTimeString()}] ERROR: ${error instanceof Error ? error.message : 'Failed to connect to trading server'}`]);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Function to stop live trading
  const stopLiveTrading = async () => {
    setIsLoading(true);
    setApiError(null);
    
    try {
      // Get token from localStorage
      const token = localStorage.getItem('auth_token');
      if (!token) {
        throw new Error('Authentication required. Please log in again.');
      }
      
      // Call the API to stop trading (using relative URL for compatibility with all environments)
      const response = await fetch('/api/trading/stop', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`Failed to stop live trading: ${response.status} ${errorData}`);
      }
      
      const data = await response.json();
      setIsLiveTrading(false);
      setLiveResults(prev => [...prev, `[${new Date().toLocaleTimeString()}] Live trading stopped successfully.`]);
      
    } catch (error) {
      console.error('Error stopping live trading:', error);
      setApiError(error instanceof Error ? error.message : 'Failed to stop live trading. Please try again later.');
      setLiveResults(prev => [...prev, `[${new Date().toLocaleTimeString()}] ERROR: ${error instanceof Error ? error.message : 'Failed to connect to trading server'}`]);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Function to check live trading status
  const checkLiveTradingStatus = async () => {
    try {
      // Get token from localStorage
      const token = localStorage.getItem('auth_token');
      if (!token) {
        return; // Silent fail if no token
      }
      
      // Call the API to get trading status (using relative URL for compatibility with all environments)
      const response = await fetch('/api/trading/status', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        return; // Silent fail if API fails
      }
      
      const data = await response.json();
      setIsLiveTrading(data.is_active || false);
      
      // Update logs if there's new activity
      if (data.recent_activity && data.recent_activity.length > 0) {
        setLiveResults(prev => {
          const newLogs = data.recent_activity.filter((log: string) => !prev.includes(log));
          return [...prev, ...newLogs];
        });
      }
      
    } catch (error) {
      console.error('Error checking live trading status:', error);
      // We don't set errors here to avoid disrupting the UI
    }
  };

  // Poll for live trading status periodically
  useEffect(() => {
    const checkInterval = setInterval(checkLiveTradingStatus, 30000); // every 30 seconds
    
    // Check on initial load
    checkLiveTradingStatus();
    
    return () => clearInterval(checkInterval);
  }, []);

  const generateAnalysis = (state: string): string => {
    const analyses = {
      ANALYZING: [
        'Scanning market trends and technical indicators...',
        'Evaluating earnings reports and news sentiment...',
        'Analyzing volume patterns and price action...',
        'Processing real-time market data feeds...'
      ],
      BUYING: [
        'Executing buy orders based on bullish signals...',
        'Accumulating position in oversold securities...',
        'Capitalizing on momentum breakout patterns...',
        'Building positions in high-confidence setups...'
      ],
      SELLING: [
        'Taking profits on overbought positions...',
        'Executing stop-loss orders to limit downside...',
        'Reducing exposure to high-risk assets...',
        'Realizing gains on target price achievements...'
      ],
      HOLDING: [
        'Monitoring existing positions for changes...',
        'Waiting for optimal entry/exit opportunities...',
        'Maintaining current portfolio allocation...',
        'Observing market consolidation patterns...'
      ]
    };
    
    const stateAnalyses = analyses[state as keyof typeof analyses] || ['Processing market data...'];
    return stateAnalyses[Math.floor(Math.random() * stateAnalyses.length)];
  };

  const generateNextAction = (state: string): string => {
    const actions = {
      ANALYZING: ['Evaluate buy signals', 'Check technical levels', 'Monitor news flow'],
      BUYING: ['Complete order execution', 'Monitor fill price', 'Set stop losses'],
      SELLING: ['Execute profit taking', 'Complete position exit', 'Monitor slippage'],
      HOLDING: ['Watch for breakouts', 'Monitor support levels', 'Prepare for signals']
    };
    
    const stateActions = actions[state as keyof typeof actions] || ['Monitor markets'];
    return stateActions[Math.floor(Math.random() * stateActions.length)];
  };

  const generateAIState = (state: string): string => {
    const aiStates = {
      ANALYZING: ['Pattern Recognition Active', 'Data Processing', 'Signal Generation'],
      BUYING: ['Order Optimization', 'Execution Management', 'Risk Assessment'],
      SELLING: ['Exit Strategy Active', 'Profit Optimization', 'Loss Mitigation'],
      HOLDING: ['Position Monitoring', 'Opportunity Scanning', 'Risk Management']
    };
    
    const currentStates = aiStates[state as keyof typeof aiStates] || ['System Active'];
    return currentStates[Math.floor(Math.random() * currentStates.length)];
  };

  const startTrial = () => {
    setTrialActive(true);
    setTrialTimeRemaining(48 * 60 * 60);
    setIsTrading(true);
  };

  const toggleTrading = () => {
    if (!trialActive && !isTrading) {
      startTrial();
    } else {
      setIsTrading(!isTrading);
    }
  };

  const formatTime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours}h ${minutes}m ${secs}s`;
  };

  const getStateColor = (status: string) => {
    switch (status) {
      case 'BUYING': return 'success';
      case 'SELLING': return 'warning';
      case 'ANALYZING': return 'info';
      case 'HOLDING': return 'secondary';
      case 'STOPPED': return 'error';
      default: return 'default';
    }
  };

  const getActionColor = (action: string) => {
    return action === 'BUY' ? 'success' : 'error';
  };

  // Chart data and options
  const chartData = {
    labels: Array.from({ length: 50 }, (_, i) => `Day ${i + 1}`),
    datasets: [
      {
        label: 'Portfolio Value',
        data: portfolioHistory.slice(-50),
        borderColor: '#2196f3',
        backgroundColor: 'rgba(33, 150, 243, 0.2)',
        fill: true,
        tension: 0.4
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Portfolio Growth Over Time',
        font: {
          size: 16,
          weight: 'bold' as const,
        },
        padding: {
          top: 10,
          bottom: 30
        }
      },
      tooltip: {
        mode: 'index' as const,
        intersect: false,
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Time',
          font: {
            weight: 'bold' as const,
          }
        },
        ticks: {
          autoSkip: true,
          maxTicksLimit: 10,
        }
      },
      y: {
        title: {
          display: true,
          text: 'Value (USD)',
          font: {
            weight: 'bold' as const,
          }
        },
        ticks: {
          // Fix chartOptions.y.ticks.callback signature to match Chart.js expected type
          callback: function(this: any, tickValue: string | number, index: number, ticks: any[]): string {
            // Only format if tickValue is a number
            if (typeof tickValue === 'number') {
              return `$${tickValue.toLocaleString()}`;
            }
            return String(tickValue);
          }
        }
      }
    }
  };

  return (
    <Box sx={{ p: 3, bgcolor: '#f5f7fa' }}>
      {/* Header with premium look */}
      <Box sx={{ 
        mb: 3, 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        p: 2,
        borderRadius: 2,
        bgcolor: 'background.paper',
        boxShadow: '0 2px 10px rgba(0,0,0,0.08)',
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Whatshot sx={{ mr: 2, color: 'primary.main', fontSize: 40 }} />
          <Box>
            <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
              MASS AI Trading Hub
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Powered by Neural Forge™
            </Typography>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          {trialActive && (
            <Chip 
              label={`Trial: ${formatTime(trialTimeRemaining)}`}
              color="primary"
              variant="outlined"
              sx={{ fontWeight: 'bold' }}
            />
          )}
          <Button
            variant="contained"
            size="large"
            color={isTrading ? "error" : "success"}
            startIcon={isTrading ? <Stop /> : <PlayArrow />}
            onClick={toggleTrading}
            sx={{ 
              fontWeight: 'bold',
              boxShadow: '0 4px 10px rgba(0,0,0,0.15)',
              px: 3
            }}
          >
            {isTrading ? 'Stop Trading' : trialActive ? 'Resume Trading' : 'Start 48h Trial'}
          </Button>
        </Box>
      </Box>

      {/* Demo Environment Banner */}
      <Alert severity="info" sx={{ 
        mb: 3, 
        fontWeight: 'bold',
        backgroundColor: 'rgba(33, 150, 243, 0.1)',
        border: '1px solid rgba(33, 150, 243, 0.3)'
      }}>
        🚀 <strong>Demo Environment</strong> - This is a demonstration of the MASS AI Trading Framework. 
        All trading data is simulated. Live trading requires production setup and API keys.
      </Alert>

      {/* Admin Live Trading Control Section */}
      <Card sx={{ mb: 3, bgcolor: 'background.paper', border: '1px solid rgba(59, 130, 246, 0.5)' }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
              Admin Live Trading Control
            </Typography>
            <Chip 
              label={isLiveTrading ? "ACTIVE" : "INACTIVE"}
              color={isLiveTrading ? "success" : "default"}
              variant={isLiveTrading ? "filled" : "outlined"}
            />
          </Box>
          
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Box sx={{ mb: 2 }}>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<PlayArrow />}
                  disabled={isLiveTrading || isLoading}
                  onClick={startLiveTrading}
                  fullWidth
                  sx={{ mb: 1 }}
                >
                  {isLoading && !isLiveTrading ? 'Starting...' : 'Start Live Trading'}
                </Button>
                
                <Button
                  variant="contained"
                  color="error"
                  startIcon={<Stop />}
                  disabled={!isLiveTrading || isLoading}
                  onClick={stopLiveTrading}
                  fullWidth
                >
                  {isLoading && isLiveTrading ? 'Stopping...' : 'Stop Live Trading'}
                </Button>
              </Box>
              
              {apiError && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {apiError}
                </Alert>
              )}
              
              <Typography variant="caption" color="text.secondary">
                Live trading uses real funds. Please ensure all settings and risk parameters are properly configured before starting.
              </Typography>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card variant="outlined" sx={{ bgcolor: 'rgba(0,0,0,0.03)', height: '100%', overflow: 'auto', maxHeight: '200px' }}>
                <CardContent>
                  <Typography variant="subtitle2" sx={{ mb: 1 }}>
                    Live Trading Results (Real Money)
                  </Typography>
                  
                  {liveResults.length === 0 ? (
                    <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                      Results and logs will appear here after live trading is started.
                    </Typography>
                  ) : (
                    <Box component="pre" sx={{ 
                      fontSize: '0.75rem', 
                      m: 0, 
                      fontFamily: 'monospace', 
                      whiteSpace: 'pre-wrap',
                      wordBreak: 'break-word'
                    }}>
                      {liveResults.map((log, index) => (
                        <div key={index}>{log}</div>
                      ))}
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      
      {/* Portfolio Overview */}
      <Card sx={{ mb: 3, bgcolor: 'background.paper', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold', display: 'flex', alignItems: 'center' }}>
            <Assessment sx={{ mr: 1 }} /> Portfolio Performance Overview
          </Typography>
          
          <Grid container spacing={3}>
            {/* Main portfolio value card */}
            <Grid item xs={12} md={4}>
              <Card sx={{ bgcolor: '#f8faff', boxShadow: 'none', border: '1px solid rgba(0,0,0,0.08)' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Typography variant="overline" color="text.secondary">Current Portfolio Value</Typography>
                    <Chip 
                      label={`${(dailyChange >= 0 ? '+' : '')}${dailyChange.toFixed(2)}% Today`} 
                      color={dailyChange >= 0 ? 'success' : 'error'} 
                      size="small"
                    />
                  </Box>
                  <Typography variant="h3" sx={{ my: 1, fontWeight: 'bold', color: 'primary.main' }}>
                    ${portfolioValue.toLocaleString()}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Weekly
                      </Typography>
                      <Typography 
                        variant="body2" 
                        color={weeklyChange >= 0 ? 'success.main' : 'error.main'} 
                        sx={{ fontWeight: 'bold' }}
                      >
                        {weeklyChange >= 0 ? '+' : ''}{weeklyChange.toFixed(2)}%
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Monthly
                      </Typography>
                      <Typography 
                        variant="body2"
                        color={monthlyChange >= 0 ? 'success.main' : 'error.main'} 
                        sx={{ fontWeight: 'bold' }}
                      >
                        {monthlyChange >= 0 ? '+' : ''}{monthlyChange.toFixed(2)}%
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Total P&L
                      </Typography>
                      <Typography 
                        variant="body2"
                        color={totalPnL >= 0 ? 'success.main' : 'error.main'} 
                        sx={{ fontWeight: 'bold' }}
                      >
                        ${totalPnL.toFixed(2)}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            
            {/* Performance metrics */}
            <Grid item xs={12} md={4}>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Card sx={{ boxShadow: 'none', border: '1px solid rgba(0,0,0,0.08)', height: '100%' }}>
                    <CardContent>
                      <Typography variant="caption" color="text.secondary">Win Rate</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'flex-end', gap: 0.5 }}>
                        <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                          {totalTrades > 0 ? ((profitableTrades / totalTrades) * 100).toFixed(1) : '0'}%
                        </Typography>
                        <Typography variant="caption" sx={{ mb: 0.5 }}>
                          ({profitableTrades}/{totalTrades})
                        </Typography>
                      </Box>
                      <LinearProgress 
                        variant="determinate" 
                        value={totalTrades > 0 ? (profitableTrades / totalTrades) * 100 : 0}
                        sx={{ height: 5, borderRadius: 2 }}
                      />
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={6}>
                  <Card sx={{ boxShadow: 'none', border: '1px solid rgba(0,0,0,0.08)', height: '100%' }}>
                    <CardContent>
                      <Typography variant="caption" color="text.secondary">Avg. Profit Per Trade</Typography>
                      <Typography variant="h5" sx={{ fontWeight: 'bold', color: avgTradeProfit >= 0 ? 'success.main' : 'error.main' }}>
                        ${avgTradeProfit.toFixed(2)}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {tradingFrequency.toFixed(1)} trades/hr
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={6}>
                  <Card sx={{ boxShadow: 'none', border: '1px solid rgba(0,0,0,0.08)', height: '100%' }}>
                    <CardContent>
                      <Typography variant="caption" color="text.secondary">Risk Score</Typography>
                      <Typography variant="h5" sx={{ 
                        fontWeight: 'bold', 
                        color: riskScore < 30 ? 'success.main' : riskScore > 70 ? 'error.main' : 'warning.main' 
                      }}>
                        {riskScore.toFixed(0)}/100
                      </Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={riskScore}
                        color={riskScore < 30 ? 'success' : riskScore > 70 ? 'error' : 'warning'}
                        sx={{ height: 5, borderRadius: 2 }}
                      />
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={6}>
                  <Card sx={{ boxShadow: 'none', border: '1px solid rgba(0,0,0,0.08)', height: '100%' }}>
                    <CardContent>
                      <Typography variant="caption" color="text.secondary">Trader Ranking</Typography>
                      <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                        Top {100 - Math.round(traderRanking)}%
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Better than {Math.round(traderRanking)}% of traders
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Grid>
            
            {/* Trading chart */}
            <Grid item xs={12} md={4}>
              <Card sx={{ boxShadow: 'none', border: '1px solid rgba(0,0,0,0.08)', height: '100%' }}>
                <CardContent sx={{ height: '100%' }}>
                  <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
                    Portfolio Growth Trend
                  </Typography>
                  <Box sx={{ height: '85%' }}>
                    <Line 
                      data={chartData} 
                      options={{
                        ...chartOptions,
                        maintainAspectRatio: false,
                        plugins: { 
                          ...chartOptions.plugins,
                          legend: { display: false },
                          title: { display: false }
                        }
                      }}
                    />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Trading State Card - Modernized */}
      <Card sx={{ mb: 3, bgcolor: 'background.paper', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6" sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center' }}>
              <Assessment sx={{ mr: 1 }} /> Live Trading Status
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Chip 
                label={tradingState.status}
                color={getStateColor(tradingState.status) as any}
                sx={{ fontWeight: 'bold' }}
              />
              <Typography variant="caption" color="text.secondary">
                Updated: {tradingState.last_update}
              </Typography>
            </Box>
          </Box>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card sx={{ mb: 2, borderLeft: '4px solid #2196f3', boxShadow: 'none', bgcolor: '#f8faff' }}>
                <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                  <Typography variant="subtitle2" color="primary.main" gutterBottom>
                    Current Analysis
                  </Typography>
                  <Typography variant="body1">
                    {tradingState.current_analysis}
                  </Typography>
                </CardContent>
              </Card>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Card sx={{ borderLeft: '4px solid #66bb6a', boxShadow: 'none', bgcolor: '#f8fff9' }}>
                    <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                      <Typography variant="subtitle2" color="success.main" gutterBottom>
                        Next Action
                      </Typography>
                      <Typography variant="body1">
                        {tradingState.next_action}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={6}>
                  <Card sx={{ borderLeft: '4px solid #ff9800', boxShadow: 'none', bgcolor: '#fffbf5' }}>
                    <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                      <Typography variant="subtitle2" color="warning.main" gutterBottom>
                        AI System State
                      </Typography>
                      <Typography variant="body1">
                        {tradingState.ai_state}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="subtitle1" gutterBottom>
                    Trade Performance
                  </Typography>
                  
                  {isTrading && (
                    <Box sx={{ mb: 3 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="caption" color="text.secondary">
                          System Processing
                        </Typography>
                        <Typography variant="caption" color="primary">
                          Active
                        </Typography>
                      </Box>
                      <LinearProgress 
                        sx={{ height: 6, borderRadius: 3 }}
                        variant="indeterminate"
                        color="primary"
                      />
                    </Box>
                  )}
                </Box>
                
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                  <Card sx={{ boxShadow: 'none', border: '1px solid rgba(0,0,0,0.08)', minWidth: 110 }}>
                    <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
                      <Typography variant="caption" color="text.secondary">
                        Total Trades
                      </Typography>
                      <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                        {totalTrades}
                      </Typography>
                    </CardContent>
                  </Card>
                  
                  <Card sx={{ boxShadow: 'none', border: '1px solid rgba(0,0,0,0.08)', minWidth: 110 }}>
                    <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
                      <Typography variant="caption" color="text.secondary">
                        Profitable
                      </Typography>
                      <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'success.main' }}>
                        {profitableTrades}
                      </Typography>
                    </CardContent>
                  </Card>
                  
                  <Card sx={{ boxShadow: 'none', border: '1px solid rgba(0,0,0,0.08)', minWidth: 110 }}>
                    <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
                      <Typography variant="caption" color="text.secondary">
                        Total P&L
                      </Typography>
                      <Typography variant="h6" sx={{ 
                        fontWeight: 'bold',
                        color: totalPnL >= 0 ? 'success.main' : 'error.main' 
                      }}>
                        ${totalPnL.toFixed(2)}
                      </Typography>
                    </CardContent>
                  </Card>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Portfolio Performance */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Portfolio Performance
              </Typography>
              <Line data={chartData} options={chartOptions} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" color="primary">
                    ${portfolioValue.toLocaleString()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Portfolio Value
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography 
                    variant="h6" 
                    color={totalPnL >= 0 ? "success.main" : "error.main"}
                  >
                    ${totalPnL.toFixed(2)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total P&L
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" color="info.main">
                    {totalTrades > 0 ? ((profitableTrades / totalTrades) * 100).toFixed(1) : '0'}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Win Rate
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Grid>
      </Grid>

      {/* Current Positions - Enhanced */}
      <Card sx={{ mb: 3, bgcolor: 'background.paper', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold', display: 'flex', alignItems: 'center' }}>
            <ShowChart sx={{ mr: 1 }} /> Current Asset Positions
          </Typography>
          
          {positions.length === 0 ? (
            <Alert severity="info" icon={<ShowChart />} sx={{ mb: 2 }}>
              No open positions. AI-driven positions will appear here when the system begins trading.
            </Alert>
          ) : (
            <Table size="small" sx={{ 
              '& .MuiTableCell-root': { 
                borderColor: 'rgba(0,0,0,0.08)',
                py: 1.5
              },
              '& .MuiTableRow-root:hover': {
                backgroundColor: 'rgba(0,0,0,0.03)'
              }
            }}>
              <TableHead sx={{ 
                backgroundColor: 'rgba(0,0,0,0.02)', 
                '& .MuiTableCell-root': { 
                  fontWeight: 'bold', 
                  color: 'text.secondary' 
                } 
              }}>
                <TableRow>
                  <TableCell>Symbol</TableCell>
                  <TableCell align="right">Quantity</TableCell>
                  <TableCell align="right">Avg Price</TableCell>
                  <TableCell align="right">Current Price</TableCell>
                  <TableCell align="right">Unrealized P&L</TableCell>
                  <TableCell align="right">% Change</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {positions.map((position) => (
                  <TableRow key={position.symbol}>
                    <TableCell component="th" scope="row">
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Box 
                          sx={{ 
                            width: 12, 
                            height: 12, 
                            borderRadius: '50%', 
                            backgroundColor: position.percentage_change >= 0 ? 'success.main' : 'error.main',
                            mr: 1 
                          }} 
                        />
                        <Typography sx={{ fontWeight: 'bold' }}>
                          {position.symbol}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell align="right">
                      <Tooltip title={`${position.quantity} shares`}>
                        <span>{position.quantity.toLocaleString()}</span>
                      </Tooltip>
                    </TableCell>
                    <TableCell align="right">${position.avg_price.toFixed(2)}</TableCell>
                    <TableCell align="right">
                      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: 0.5 }}>
                        ${position.current_price.toFixed(2)}
                        <Tooltip title={position.percentage_change >= 0 ? "Price rising" : "Price falling"}>
                          {position.percentage_change >= 0 
                            ? <TrendingUp fontSize="small" sx={{ color: 'success.main' }} /> 
                            : <TrendingDown fontSize="small" sx={{ color: 'error.main' }} />}
                        </Tooltip>
                      </Box>
                    </TableCell>
                    <TableCell align="right">
                      <Typography
                        sx={{ 
                          fontWeight: 'bold',
                          color: position.unrealized_pnl >= 0 ? 'success.main' : 'error.main' 
                        }}
                      >
                        ${position.unrealized_pnl.toFixed(2)}
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Chip 
                        label={`${position.percentage_change >= 0 ? '+' : ''}${position.percentage_change.toFixed(2)}%`}
                        size="small"
                        sx={{ 
                          fontWeight: 'bold',
                          backgroundColor: position.percentage_change >= 0 ? 'rgba(76, 175, 80, 0.1)' : 'rgba(244, 67, 54, 0.1)', 
                          color: position.percentage_change >= 0 ? 'success.main' : 'error.main',
                          border: '1px solid',
                          borderColor: position.percentage_change >= 0 ? 'success.light' : 'error.light',
                        }}
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Recent Trading Activity */}
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              Recent Trading Activity
            </Typography>
            <Badge badgeContent={trades.length} color="primary">
              <ShowChart />
            </Badge>
          </Box>
          
          {trades.length === 0 ? (
            <Alert severity="info">
              No trades executed yet. Start trading to see activity here.
            </Alert>
          ) : (
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Time</TableCell>
                  <TableCell>Symbol</TableCell>
                  <TableCell>Action</TableCell>
                  <TableCell align="right">Quantity</TableCell>
                  <TableCell align="right">Price</TableCell>
                  <TableCell align="right">P&L</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Strategy</TableCell>
                  <TableCell align="right">AI Confidence</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {trades.map((trade) => (
                  <TableRow key={trade.id}>
                    <TableCell>
                      {new Date(trade.timestamp).toLocaleTimeString()}
                    </TableCell>
                    <TableCell>
                      <strong>{trade.symbol}</strong>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={trade.action}
                        color={getActionColor(trade.action) as any}
                        size="small"
                        icon={trade.action === 'BUY' ? <TrendingUp /> : <TrendingDown />}
                      />
                    </TableCell>
                    <TableCell align="right">{trade.quantity}</TableCell>
                    <TableCell align="right">${trade.price.toFixed(2)}</TableCell>
                    <TableCell 
                      align="right"
                      sx={{ color: trade.profit_loss >= 0 ? 'success.main' : 'error.main' }}
                    >
                      ${trade.profit_loss.toFixed(2)}
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={trade.status}
                        color={trade.status === 'EXECUTED' ? 'success' : trade.status === 'PENDING' ? 'warning' : 'error'}
                        size="small"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>
                      <Tooltip title={`Market: ${trade.market_condition}`}>
                        <span>{trade.strategy}</span>
                      </Tooltip>
                    </TableCell>
                    <TableCell align="right">
                      <Chip 
                        label={`${(trade.ai_confidence * 100).toFixed(0)}%`}
                        size="small"
                        color={trade.ai_confidence > 0.8 ? 'success' : trade.ai_confidence > 0.6 ? 'warning' : 'error'}
                        variant="outlined"
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default TradingDashboard;