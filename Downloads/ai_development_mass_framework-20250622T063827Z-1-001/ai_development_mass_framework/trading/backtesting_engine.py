"""
📊 COMPREHENSIVE BACKTESTING ENGINE
Advanced trading strategy validation and testing

This module provides comprehensive backtesting capabilities including:
- Multi-timeframe strategy testing
- Real and synthetic data validation
- Risk assessment and analysis
- Performance metrics calculation
- Strategy optimization
- Monte Carlo simulations
- Walk-forward analysis
"""

import asyncio
import logging
import json
import time
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import uuid
from pathlib import Path
import yfinance as yf
import talib
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import asdict

# Configure backtesting logger
backtest_logger = logging.getLogger("trading.backtesting")
backtest_logger.setLevel(logging.INFO)

class BacktestMode(Enum):
    """Backtesting modes"""
    HISTORICAL = "historical"
    SYNTHETIC = "synthetic"
    MONTE_CARLO = "monte_carlo"
    WALK_FORWARD = "walk_forward"
    STRESS_TEST = "stress_test"

class StrategyType(Enum):
    """Trading strategy types"""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    BREAKOUT = "breakout"
    ARBITRAGE = "arbitrage"
    QUANTITATIVE = "quantitative"
    MACHINE_LEARNING = "machine_learning"
    QUANTUM = "quantum"

@dataclass
class BacktestConfig:
    """Backtesting configuration"""
    start_date: datetime
    end_date: datetime
    initial_capital: float = 100000.0
    commission_rate: float = 0.001  # 0.1%
    slippage_rate: float = 0.0005   # 0.05%
    risk_free_rate: float = 0.02    # 2%
    benchmark_symbol: str = "SPY"
    mode: BacktestMode = BacktestMode.HISTORICAL
    synthetic_scenarios: int = 1000
    monte_carlo_simulations: int = 1000
    walk_forward_periods: int = 12
    stress_test_scenarios: List[str] = field(default_factory=lambda: [
        "market_crash", "high_volatility", "low_liquidity", "flash_crash"
    ])

@dataclass
class Trade:
    """Trade record"""
    trade_id: str
    timestamp: datetime
    symbol: str
    side: str  # "buy" or "sell"
    quantity: float
    price: float
    commission: float
    slippage: float
    strategy: str
    signal_strength: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Position:
    """Position record"""
    symbol: str
    quantity: float
    avg_price: float
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0
    last_update: datetime = field(default_factory=datetime.utcnow)

@dataclass
class BacktestResult:
    """Backtesting result"""
    result_id: str
    strategy_name: str
    config: BacktestConfig
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    largest_win: float
    largest_loss: float
    consecutive_wins: int
    consecutive_losses: int
    trades: List[Trade] = field(default_factory=list)
    positions: Dict[str, Position] = field(default_factory=dict)
    equity_curve: List[Tuple[datetime, float]] = field(default_factory=list)
    drawdown_curve: List[Tuple[datetime, float]] = field(default_factory=list)
    benchmark_comparison: Dict[str, float] = field(default_factory=dict)
    risk_metrics: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

class DataProvider:
    """Data provider for backtesting"""
    
    def __init__(self):
        self.cache = {}
        self.cache_expiry = {}
        
    async def get_historical_data(self, symbol: str, start_date: datetime, 
                                 end_date: datetime, interval: str = "1d") -> pd.DataFrame:
        """Get historical price data"""
        try:
            cache_key = f"{symbol}_{start_date.date()}_{end_date.date()}_{interval}"
            
            # Check cache
            if cache_key in self.cache:
                if datetime.utcnow() < self.cache_expiry.get(cache_key, datetime.min):
                    return self.cache[cache_key]
            
            # Fetch data from Yahoo Finance
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date, interval=interval)
            
            if data.empty:
                raise ValueError(f"No data available for {symbol}")
            
            # Calculate additional technical indicators
            data = self._add_technical_indicators(data)
            
            # Cache the data
            self.cache[cache_key] = data
            self.cache_expiry[cache_key] = datetime.utcnow() + timedelta(hours=1)
            
            backtest_logger.info(f"Loaded {len(data)} data points for {symbol}")
            return data
            
        except Exception as e:
            backtest_logger.error(f"Failed to get historical data for {symbol}: {e}")
            raise
    
    def _add_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add technical indicators to the data"""
        try:
            # Moving averages
            data['SMA_20'] = talib.SMA(data['Close'], timeperiod=20)
            data['SMA_50'] = talib.SMA(data['Close'], timeperiod=50)
            data['EMA_12'] = talib.EMA(data['Close'], timeperiod=12)
            data['EMA_26'] = talib.EMA(data['Close'], timeperiod=26)
            
            # MACD
            data['MACD'], data['MACD_Signal'], data['MACD_Hist'] = talib.MACD(
                data['Close'], fastperiod=12, slowperiod=26, signalperiod=9
            )
            
            # RSI
            data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
            
            # Bollinger Bands
            data['BB_Upper'], data['BB_Middle'], data['BB_Lower'] = talib.BBANDS(
                data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2
            )
            
            # Stochastic
            data['STOCH_K'], data['STOCH_D'] = talib.STOCH(
                data['High'], data['Low'], data['Close']
            )
            
            # ATR for volatility
            data['ATR'] = talib.ATR(data['High'], data['Low'], data['Close'], timeperiod=14)
            
            # Volume indicators
            data['OBV'] = talib.OBV(data['Close'], data['Volume'])
            
            return data
            
        except Exception as e:
            backtest_logger.error(f"Failed to add technical indicators: {e}")
            return data
    
    def generate_synthetic_data(self, symbol: str, start_date: datetime, 
                               end_date: datetime, volatility: float = 0.2,
                               drift: float = 0.1) -> pd.DataFrame:
        """Generate synthetic price data for testing"""
        try:
            # Generate time index
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            
            # Generate synthetic price series using geometric Brownian motion
            np.random.seed(42)  # For reproducibility
            
            # Daily returns
            daily_returns = np.random.normal(drift/252, volatility/np.sqrt(252), len(date_range))
            
            # Price series
            initial_price = 100.0
            prices = [initial_price]
            
            for ret in daily_returns[1:]:
                new_price = prices[-1] * (1 + ret)
                prices.append(new_price)
            
            # Create DataFrame
            data = pd.DataFrame({
                'Open': prices,
                'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
                'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
                'Close': prices,
                'Volume': np.random.randint(1000000, 10000000, len(prices))
            }, index=date_range)
            
            # Add technical indicators
            data = self._add_technical_indicators(data)
            
            backtest_logger.info(f"Generated {len(data)} synthetic data points for {symbol}")
            return data
            
        except Exception as e:
            backtest_logger.error(f"Failed to generate synthetic data: {e}")
            raise

class StrategyEngine:
    """Trading strategy engine"""
    
    def __init__(self):
        self.strategies = self._load_strategies()
    
    def _load_strategies(self) -> Dict[str, callable]:
        """Load trading strategies"""
        return {
            'momentum_rsi': self._momentum_rsi_strategy,
            'mean_reversion_bollinger': self._mean_reversion_bollinger_strategy,
            'breakout_atr': self._breakout_atr_strategy,
            'macd_crossover': self._macd_crossover_strategy,
            'dual_thrust': self._dual_thrust_strategy,
            'turtle_trading': self._turtle_trading_strategy
        }
    
    def get_strategy(self, strategy_name: str) -> Optional[callable]:
        """Get strategy function by name"""
        return self.strategies.get(strategy_name)
    
    def _momentum_rsi_strategy(self, data: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """RSI-based momentum strategy"""
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        rsi_period = params.get('rsi_period', 14)
        oversold = params.get('oversold', 30)
        overbought = params.get('overbought', 70)
        
        # Generate signals
        signals.loc[data['RSI'] < oversold, 'signal'] = 1  # Buy signal
        signals.loc[data['RSI'] > overbought, 'signal'] = -1  # Sell signal
        
        return signals
    
    def _mean_reversion_bollinger_strategy(self, data: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Bollinger Bands mean reversion strategy"""
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        # Generate signals
        signals.loc[data['Close'] < data['BB_Lower'], 'signal'] = 1  # Buy signal
        signals.loc[data['Close'] > data['BB_Upper'], 'signal'] = -1  # Sell signal
        
        return signals
    
    def _breakout_atr_strategy(self, data: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """ATR-based breakout strategy"""
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        atr_multiplier = params.get('atr_multiplier', 2.0)
        
        # Calculate breakout levels
        data['Upper_Breakout'] = data['SMA_20'] + (data['ATR'] * atr_multiplier)
        data['Lower_Breakout'] = data['SMA_20'] - (data['ATR'] * atr_multiplier)
        
        # Generate signals
        signals.loc[data['Close'] > data['Upper_Breakout'], 'signal'] = 1  # Buy signal
        signals.loc[data['Close'] < data['Lower_Breakout'], 'signal'] = -1  # Sell signal
        
        return signals
    
    def _macd_crossover_strategy(self, data: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """MACD crossover strategy"""
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        # Generate signals
        signals.loc[data['MACD'] > data['MACD_Signal'], 'signal'] = 1  # Buy signal
        signals.loc[data['MACD'] < data['MACD_Signal'], 'signal'] = -1  # Sell signal
        
        return signals
    
    def _dual_thrust_strategy(self, data: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Dual Thrust strategy"""
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        lookback = params.get('lookback', 20)
        
        # Calculate Dual Thrust levels
        data['Range'] = data['High'] - data['Low']
        data['Range_SMA'] = data['Range'].rolling(lookback).mean()
        
        data['Upper_Level'] = data['Open'] + (data['Range_SMA'] * 0.7)
        data['Lower_Level'] = data['Open'] - (data['Range_SMA'] * 0.7)
        
        # Generate signals
        signals.loc[data['Close'] > data['Upper_Level'], 'signal'] = 1  # Buy signal
        signals.loc[data['Close'] < data['Lower_Level'], 'signal'] = -1  # Sell signal
        
        return signals
    
    def _turtle_trading_strategy(self, data: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Turtle Trading strategy"""
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        entry_period = params.get('entry_period', 20)
        exit_period = params.get('exit_period', 10)
        
        # Calculate breakout levels
        data['Entry_High'] = data['High'].rolling(entry_period).max()
        data['Entry_Low'] = data['Low'].rolling(entry_period).min()
        data['Exit_High'] = data['High'].rolling(exit_period).max()
        data['Exit_Low'] = data['Low'].rolling(exit_period).min()
        
        # Generate signals
        signals.loc[data['Close'] > data['Entry_High'].shift(1), 'signal'] = 1  # Buy signal
        signals.loc[data['Close'] < data['Exit_Low'].shift(1), 'signal'] = -1  # Sell signal
        
        return signals

class BacktestingEngine:
    """Comprehensive backtesting engine"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.data_provider = DataProvider()
        self.strategy_engine = StrategyEngine()
        self.results: List[BacktestResult] = []
        
    async def run_backtest(self, strategy_name: str, symbol: str, 
                          strategy_params: Dict[str, Any] = None) -> BacktestResult:
        """Run backtest for a strategy"""
        try:
            backtest_logger.info(f"Starting backtest for {strategy_name} on {symbol}")
            
            # Get strategy function
            strategy_func = self.strategy_engine.get_strategy(strategy_name)
            if not strategy_func:
                raise ValueError(f"Strategy {strategy_name} not found")
            
            # Get data
            if self.config.mode == BacktestMode.SYNTHETIC:
                data = self.data_provider.generate_synthetic_data(
                    symbol, self.config.start_date, self.config.end_date
                )
            else:
                data = await self.data_provider.get_historical_data(
                    symbol, self.config.start_date, self.config.end_date
                )
            
            # Generate signals
            signals = strategy_func(data, strategy_params or {})
            
            # Execute backtest
            result = await self._execute_backtest(strategy_name, symbol, data, signals)
            
            # Store result
            self.results.append(result)
            
            backtest_logger.info(f"Backtest completed: {result.total_return:.2%} return")
            return result
            
        except Exception as e:
            backtest_logger.error(f"Backtest failed: {e}")
            raise
    
    async def _execute_backtest(self, strategy_name: str, symbol: str, 
                               data: pd.DataFrame, signals: pd.DataFrame) -> BacktestResult:
        """Execute the backtest simulation"""
        try:
            # Initialize tracking variables
            capital = self.config.initial_capital
            positions = {}
            trades = []
            equity_curve = []
            drawdown_curve = []
            
            # Track benchmark
            benchmark_data = None
            if self.config.benchmark_symbol != symbol:
                benchmark_data = await self.data_provider.get_historical_data(
                    self.config.benchmark_symbol, self.config.start_date, self.config.end_date
                )
            
            # Iterate through data
            for i, (timestamp, row) in enumerate(data.iterrows()):
                signal = signals.loc[timestamp, 'signal']
                
                # Execute trades based on signals
                if signal != 0 and symbol not in positions:
                    # Open position
                    quantity = capital * 0.95 / row['Close']  # Use 95% of capital
                    commission = quantity * row['Close'] * self.config.commission_rate
                    slippage = quantity * row['Close'] * self.config.slippage_rate
                    
                    trade = Trade(
                        trade_id=str(uuid.uuid4()),
                        timestamp=timestamp,
                        symbol=symbol,
                        side="buy" if signal > 0 else "sell",
                        quantity=quantity,
                        price=row['Close'],
                        commission=commission,
                        slippage=slippage,
                        strategy=strategy_name
                    )
                    
                    trades.append(trade)
                    
                    # Update position
                    positions[symbol] = Position(
                        symbol=symbol,
                        quantity=quantity,
                        avg_price=row['Close']
                    )
                    
                    # Update capital
                    capital -= (quantity * row['Close'] + commission + slippage)
                
                elif signal == 0 and symbol in positions:
                    # Close position
                    position = positions[symbol]
                    commission = position.quantity * row['Close'] * self.config.commission_rate
                    slippage = position.quantity * row['Close'] * self.config.slippage_rate
                    
                    # Calculate P&L
                    if position.avg_price > 0:
                        pnl = (row['Close'] - position.avg_price) * position.quantity
                    else:
                        pnl = (position.avg_price - row['Close']) * position.quantity
                    
                    trade = Trade(
                        trade_id=str(uuid.uuid4()),
                        timestamp=timestamp,
                        symbol=symbol,
                        side="sell" if signal > 0 else "buy",
                        quantity=position.quantity,
                        price=row['Close'],
                        commission=commission,
                        slippage=slippage,
                        strategy=strategy_name
                    )
                    
                    trades.append(trade)
                    
                    # Update capital
                    capital += (position.quantity * row['Close'] - commission - slippage)
                    
                    # Remove position
                    del positions[symbol]
                
                # Update equity curve
                current_value = capital
                for pos_symbol, position in positions.items():
                    current_value += position.quantity * row['Close']
                
                equity_curve.append((timestamp, current_value))
                
                # Calculate drawdown
                if equity_curve:
                    peak = max([eq[1] for eq in equity_curve])
                    drawdown = (current_value - peak) / peak
                    drawdown_curve.append((timestamp, drawdown))
            
            # Calculate final metrics
            final_capital = equity_curve[-1][1] if equity_curve else capital
            total_return = (final_capital - self.config.initial_capital) / self.config.initial_capital
            
            # Calculate performance metrics
            metrics = self._calculate_performance_metrics(trades, equity_curve, drawdown_curve)
            
            # Create result
            result = BacktestResult(
                result_id=str(uuid.uuid4()),
                strategy_name=strategy_name,
                config=self.config,
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                initial_capital=self.config.initial_capital,
                final_capital=final_capital,
                total_return=total_return,
                trades=trades,
                positions=positions,
                equity_curve=equity_curve,
                drawdown_curve=drawdown_curve,
                **metrics
            )
            
            return result
            
        except Exception as e:
            backtest_logger.error(f"Backtest execution failed: {e}")
            raise
    
    def _calculate_performance_metrics(self, trades: List[Trade], 
                                     equity_curve: List[Tuple[datetime, float]],
                                     drawdown_curve: List[Tuple[datetime, float]]) -> Dict[str, float]:
        """Calculate comprehensive performance metrics"""
        try:
            if not trades:
                return {
                    'annualized_return': 0.0,
                    'volatility': 0.0,
                    'sharpe_ratio': 0.0,
                    'max_drawdown': 0.0,
                    'win_rate': 0.0,
                    'profit_factor': 0.0,
                    'total_trades': 0,
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'avg_win': 0.0,
                    'avg_loss': 0.0,
                    'largest_win': 0.0,
                    'largest_loss': 0.0,
                    'consecutive_wins': 0,
                    'consecutive_losses': 0
                }
            
            # Calculate returns
            returns = []
            for i in range(1, len(equity_curve)):
                prev_value = equity_curve[i-1][1]
                curr_value = equity_curve[i][1]
                ret = (curr_value - prev_value) / prev_value
                returns.append(ret)
            
            # Basic metrics
            total_return = (equity_curve[-1][1] - equity_curve[0][1]) / equity_curve[0][1]
            annualized_return = (1 + total_return) ** (252 / len(equity_curve)) - 1
            volatility = np.std(returns) * np.sqrt(252)
            sharpe_ratio = (annualized_return - self.config.risk_free_rate) / volatility if volatility > 0 else 0
            
            # Drawdown metrics
            max_drawdown = min([dd[1] for dd in drawdown_curve]) if drawdown_curve else 0
            
            # Trade metrics
            total_trades = len(trades)
            winning_trades = len([t for t in trades if t.side == "sell" and t.price > 0])
            losing_trades = total_trades - winning_trades
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
            
            # Calculate trade P&L
            trade_pnls = []
            for i in range(0, len(trades), 2):
                if i + 1 < len(trades):
                    buy_trade = trades[i]
                    sell_trade = trades[i + 1]
                    pnl = (sell_trade.price - buy_trade.price) * buy_trade.quantity
                    trade_pnls.append(pnl)
            
            if trade_pnls:
                winning_pnls = [pnl for pnl in trade_pnls if pnl > 0]
                losing_pnls = [pnl for pnl in trade_pnls if pnl < 0]
                
                avg_win = np.mean(winning_pnls) if winning_pnls else 0
                avg_loss = np.mean(losing_pnls) if losing_pnls else 0
                largest_win = max(trade_pnls) if trade_pnls else 0
                largest_loss = min(trade_pnls) if trade_pnls else 0
                
                profit_factor = abs(sum(winning_pnls) / sum(losing_pnls)) if sum(losing_pnls) != 0 else float('inf')
            else:
                avg_win = avg_loss = largest_win = largest_loss = 0
                profit_factor = 0
            
            # Consecutive wins/losses
            consecutive_wins = 0
            consecutive_losses = 0
            max_consecutive_wins = 0
            max_consecutive_losses = 0
            
            for pnl in trade_pnls:
                if pnl > 0:
                    consecutive_wins += 1
                    consecutive_losses = 0
                    max_consecutive_wins = max(max_consecutive_wins, consecutive_wins)
                else:
                    consecutive_losses += 1
                    consecutive_wins = 0
                    max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
            
            return {
                'annualized_return': annualized_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': abs(max_drawdown),
                'win_rate': win_rate,
                'profit_factor': profit_factor,
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'largest_win': largest_win,
                'largest_loss': largest_loss,
                'consecutive_wins': max_consecutive_wins,
                'consecutive_losses': max_consecutive_losses
            }
            
        except Exception as e:
            backtest_logger.error(f"Failed to calculate performance metrics: {e}")
            return {}
    
    async def run_monte_carlo_simulation(self, strategy_name: str, symbol: str,
                                        strategy_params: Dict[str, Any] = None) -> List[BacktestResult]:
        """Run Monte Carlo simulation"""
        results = []
        
        for i in range(self.config.monte_carlo_simulations):
            # Generate synthetic data with different parameters
            volatility = np.random.uniform(0.15, 0.35)
            drift = np.random.uniform(-0.1, 0.2)
            
            data = self.data_provider.generate_synthetic_data(
                symbol, self.config.start_date, self.config.end_date,
                volatility=volatility, drift=drift
            )
            
            # Run backtest
            strategy_func = self.strategy_engine.get_strategy(strategy_name)
            signals = strategy_func(data, strategy_params or {})
            
            result = await self._execute_backtest(strategy_name, symbol, data, signals)
            results.append(result)
        
        return results
    
    def generate_backtest_report(self, result: BacktestResult) -> Dict[str, Any]:
        """Generate comprehensive backtest report"""
        return {
            'summary': {
                'strategy_name': result.strategy_name,
                'start_date': result.start_date.isoformat(),
                'end_date': result.end_date.isoformat(),
                'initial_capital': result.initial_capital,
                'final_capital': result.final_capital,
                'total_return': result.total_return,
                'annualized_return': result.annualized_return
            },
            'risk_metrics': {
                'volatility': result.volatility,
                'sharpe_ratio': result.sharpe_ratio,
                'max_drawdown': result.max_drawdown,
                'var_95': self._calculate_var(result.equity_curve, 0.95),
                'cvar_95': self._calculate_cvar(result.equity_curve, 0.95)
            },
            'trading_metrics': {
                'total_trades': result.total_trades,
                'winning_trades': result.winning_trades,
                'losing_trades': result.losing_trades,
                'win_rate': result.win_rate,
                'profit_factor': result.profit_factor,
                'avg_win': result.avg_win,
                'avg_loss': result.avg_loss,
                'largest_win': result.largest_win,
                'largest_loss': result.largest_loss
            },
            'equity_curve': result.equity_curve,
            'drawdown_curve': result.drawdown_curve
        }
    
    def _calculate_var(self, equity_curve: List[Tuple[datetime, float]], confidence: float) -> float:
        """Calculate Value at Risk"""
        if len(equity_curve) < 2:
            return 0.0
        
        returns = []
        for i in range(1, len(equity_curve)):
            prev_value = equity_curve[i-1][1]
            curr_value = equity_curve[i][1]
            ret = (curr_value - prev_value) / prev_value
            returns.append(ret)
        
        return np.percentile(returns, (1 - confidence) * 100)
    
    def _calculate_cvar(self, equity_curve: List[Tuple[datetime, float]], confidence: float) -> float:
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        if len(equity_curve) < 2:
            return 0.0
        
        returns = []
        for i in range(1, len(equity_curve)):
            prev_value = equity_curve[i-1][1]
            curr_value = equity_curve[i][1]
            ret = (curr_value - prev_value) / prev_value
            returns.append(ret)
        
        var = np.percentile(returns, (1 - confidence) * 100)
        return np.mean([r for r in returns if r <= var])

# Global backtesting engine instance
backtesting_engine = None 