"""
Real Data Trading Simulation for PROMETHEUS AI Trading Platform
Simulates live trading environment with real market data and admin trading capabilities
"""

import asyncio
import aiohttp
import json
import time
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import websockets
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    PARTIALLY_FILLED = "partially_filled"

@dataclass
class MarketData:
    symbol: str
    price: float
    bid: float
    ask: float
    volume: int
    timestamp: datetime
    change_24h: float
    change_percent_24h: float

@dataclass
class Order:
    id: str
    user_id: str
    symbol: str
    side: OrderSide
    type: OrderType
    quantity: float
    price: Optional[float]
    filled_quantity: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    
@dataclass
class Position:
    symbol: str
    quantity: float
    average_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float

@dataclass
class Portfolio:
    user_id: str
    cash_balance: float
    total_value: float
    positions: List[Position]
    daily_pnl: float
    total_return: float
    total_return_percent: float

class RealTimeDataFeed:
    """Simulate real-time market data feed"""
    
    def __init__(self):
        self.symbols = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "NFLX", "SPY", "QQQ"]
        self.market_data: Dict[str, MarketData] = {}
        self.subscribers: List[callable] = []
        self.running = False
        
        # Initialize with realistic base prices
        self.base_prices = {
            "AAPL": 150.0, "TSLA": 250.0, "MSFT": 300.0, "GOOGL": 140.0, "AMZN": 130.0,
            "NVDA": 450.0, "META": 280.0, "NFLX": 400.0, "SPY": 420.0, "QQQ": 350.0
        }
        
        # Initialize market data
        for symbol in self.symbols:
            self.market_data[symbol] = self._generate_initial_data(symbol)
    
    def _generate_initial_data(self, symbol: str) -> MarketData:
        """Generate initial market data for a symbol"""
        base_price = self.base_prices.get(symbol, 100.0)
        price = base_price + random.uniform(-5, 5)
        bid = price - random.uniform(0.01, 0.05)
        ask = price + random.uniform(0.01, 0.05)
        
        return MarketData(
            symbol=symbol,
            price=price,
            bid=bid,
            ask=ask,
            volume=random.randint(1000000, 50000000),
            timestamp=datetime.now(),
            change_24h=random.uniform(-10, 10),
            change_percent_24h=random.uniform(-5, 5)
        )
    
    def subscribe(self, callback: callable):
        """Subscribe to market data updates"""
        self.subscribers.append(callback)
    
    def unsubscribe(self, callback: callable):
        """Unsubscribe from market data updates"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
    
    async def start_feed(self):
        """Start the real-time data feed"""
        self.running = True
        logger.info("🔄 Starting real-time market data feed...")
        
        while self.running:
            for symbol in self.symbols:
                # Update market data with realistic price movements
                current_data = self.market_data[symbol]
                new_price = self._calculate_new_price(current_data)
                
                # Update market data
                self.market_data[symbol] = MarketData(
                    symbol=symbol,
                    price=new_price,
                    bid=new_price - random.uniform(0.01, 0.05),
                    ask=new_price + random.uniform(0.01, 0.05),
                    volume=current_data.volume + random.randint(-100000, 100000),
                    timestamp=datetime.now(),
                    change_24h=new_price - self.base_prices[symbol],
                    change_percent_24h=((new_price - self.base_prices[symbol]) / self.base_prices[symbol]) * 100
                )
                
                # Notify subscribers
                for callback in self.subscribers:
                    try:
                        await callback(self.market_data[symbol])
                    except Exception as e:
                        logger.error(f"Error in market data callback: {e}")
            
            await asyncio.sleep(1)  # Update every second
    
    def _calculate_new_price(self, current_data: MarketData) -> float:
        """Calculate new price with realistic market movement"""
        # Use random walk with mean reversion
        change_percent = random.gauss(0, 0.001)  # Small random changes
        
        # Add some volatility during "market hours"
        hour = datetime.now().hour
        if 9 <= hour <= 16:  # Market hours
            change_percent *= 2  # Increase volatility
        
        new_price = current_data.price * (1 + change_percent)
        
        # Ensure price doesn't go negative or too extreme
        base_price = self.base_prices[current_data.symbol]
        new_price = max(base_price * 0.5, min(base_price * 2.0, new_price))
        
        return round(new_price, 2)
    
    def stop_feed(self):
        """Stop the data feed"""
        self.running = False
        logger.info("⏹️ Stopping market data feed...")

class TradingEngine:
    """Realistic trading engine with order execution"""
    
    def __init__(self, data_feed: RealTimeDataFeed):
        self.data_feed = data_feed
        self.orders: Dict[str, Order] = {}
        self.portfolios: Dict[str, Portfolio] = {}
        self.positions: Dict[str, Dict[str, Position]] = {}  # user_id -> symbol -> position
        self.order_book: Dict[str, List[Order]] = {}  # symbol -> orders
        
        # Subscribe to market data for order execution
        self.data_feed.subscribe(self._process_market_update)
    
    async def _process_market_update(self, market_data: MarketData):
        """Process market data updates and execute orders"""
        symbol = market_data.symbol
        
        # Check for order executions
        if symbol in self.order_book:
            orders_to_execute = []
            
            for order in self.order_book[symbol]:
                if order.status == OrderStatus.PENDING:
                    if self._should_execute_order(order, market_data):
                        orders_to_execute.append(order)
            
            for order in orders_to_execute:
                await self._execute_order(order, market_data)
        
        # Update portfolio values
        await self._update_portfolio_values(market_data)
    
    def _should_execute_order(self, order: Order, market_data: MarketData) -> bool:
        """Determine if order should be executed based on market conditions"""
        if order.type == OrderType.MARKET:
            return True
        elif order.type == OrderType.LIMIT:
            if order.side == OrderSide.BUY:
                return market_data.ask <= order.price
            else:
                return market_data.bid >= order.price
        elif order.type == OrderType.STOP_LOSS:
            if order.side == OrderSide.SELL:
                return market_data.price <= order.price
        elif order.type == OrderType.TAKE_PROFIT:
            if order.side == OrderSide.SELL:
                return market_data.price >= order.price
        
        return False
    
    async def _execute_order(self, order: Order, market_data: MarketData):
        """Execute an order"""
        execution_price = market_data.ask if order.side == OrderSide.BUY else market_data.bid
        
        # Add slippage for market orders
        if order.type == OrderType.MARKET:
            slippage = random.uniform(0.001, 0.005)  # 0.1% to 0.5% slippage
            if order.side == OrderSide.BUY:
                execution_price *= (1 + slippage)
            else:
                execution_price *= (1 - slippage)
        
        # Execute the order
        order.filled_quantity = order.quantity
        order.status = OrderStatus.FILLED
        order.updated_at = datetime.now()
        
        # Update position
        await self._update_position(order, execution_price)
        
        logger.info(f"✅ Order executed: {order.side.value} {order.quantity} {order.symbol} at ${execution_price:.2f}")
    
    async def _update_position(self, order: Order, execution_price: float):
        """Update user position after order execution"""
        user_id = order.user_id
        symbol = order.symbol
        
        if user_id not in self.positions:
            self.positions[user_id] = {}
        
        if symbol not in self.positions[user_id]:
            self.positions[user_id][symbol] = Position(
                symbol=symbol,
                quantity=0,
                average_price=0,
                current_price=execution_price,
                unrealized_pnl=0,
                realized_pnl=0
            )
        
        position = self.positions[user_id][symbol]
        
        if order.side == OrderSide.BUY:
            # Update average price for buy orders
            total_cost = (position.quantity * position.average_price) + (order.quantity * execution_price)
            position.quantity += order.quantity
            position.average_price = total_cost / position.quantity if position.quantity > 0 else execution_price
        else:
            # Calculate realized PnL for sell orders
            realized_pnl = (execution_price - position.average_price) * order.quantity
            position.realized_pnl += realized_pnl
            position.quantity -= order.quantity
        
        position.current_price = execution_price
        position.unrealized_pnl = (position.current_price - position.average_price) * position.quantity
        
        # Update portfolio
        await self._update_portfolio(user_id)
    
    async def _update_portfolio_values(self, market_data: MarketData):
        """Update portfolio values based on market data"""
        symbol = market_data.symbol
        
        for user_id, user_positions in self.positions.items():
            if symbol in user_positions:
                position = user_positions[symbol]
                position.current_price = market_data.price
                position.unrealized_pnl = (position.current_price - position.average_price) * position.quantity
                
                # Update portfolio
                await self._update_portfolio(user_id)
    
    async def _update_portfolio(self, user_id: str):
        """Update user portfolio"""
        if user_id not in self.portfolios:
            self.portfolios[user_id] = Portfolio(
                user_id=user_id,
                cash_balance=100000.0,  # Start with $100k
                total_value=100000.0,
                positions=[],
                daily_pnl=0,
                total_return=0,
                total_return_percent=0
            )
        
        portfolio = self.portfolios[user_id]
        user_positions = self.positions.get(user_id, {})
        
        # Calculate total portfolio value
        positions_value = sum(pos.quantity * pos.current_price for pos in user_positions.values())
        total_unrealized_pnl = sum(pos.unrealized_pnl for pos in user_positions.values())
        total_realized_pnl = sum(pos.realized_pnl for pos in user_positions.values())
        
        portfolio.total_value = portfolio.cash_balance + positions_value
        portfolio.positions = list(user_positions.values())
        portfolio.total_return = total_unrealized_pnl + total_realized_pnl
        portfolio.total_return_percent = (portfolio.total_return / 100000.0) * 100  # Assuming $100k initial
    
    async def place_order(self, user_id: str, symbol: str, side: OrderSide, order_type: OrderType, 
                         quantity: float, price: Optional[float] = None) -> Order:
        """Place a new order"""
        order = Order(
            id=str(uuid.uuid4()),
            user_id=user_id,
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity,
            price=price,
            filled_quantity=0,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Validate order
        if not self._validate_order(order):
            order.status = OrderStatus.REJECTED
            logger.warning(f"❌ Order rejected: {order}")
            return order
        
        # Add to order book
        if symbol not in self.order_book:
            self.order_book[symbol] = []
        
        self.order_book[symbol].append(order)
        self.orders[order.id] = order
        
        logger.info(f"📝 Order placed: {order.side.value} {order.quantity} {order.symbol} at ${order.price or 'market'}")
        
        # Try immediate execution for market orders
        if order_type == OrderType.MARKET:
            market_data = self.data_feed.market_data.get(symbol)
            if market_data and self._should_execute_order(order, market_data):
                await self._execute_order(order, market_data)
        
        return order
    
    def _validate_order(self, order: Order) -> bool:
        """Validate order parameters"""
        # Check symbol exists
        if order.symbol not in self.data_feed.symbols:
            return False
        
        # Check quantity is positive
        if order.quantity <= 0:
            return False
        
        # Check price for limit orders
        if order.type in [OrderType.LIMIT, OrderType.STOP_LOSS, OrderType.TAKE_PROFIT]:
            if order.price is None or order.price <= 0:
                return False
        
        # Check user has sufficient balance (simplified)
        portfolio = self.portfolios.get(order.user_id)
        if portfolio and order.side == OrderSide.BUY:
            market_data = self.data_feed.market_data.get(order.symbol)
            if market_data:
                estimated_cost = order.quantity * market_data.ask
                if estimated_cost > portfolio.cash_balance:
                    return False
        
        return True
    
    def get_portfolio(self, user_id: str) -> Optional[Portfolio]:
        """Get user portfolio"""
        return self.portfolios.get(user_id)
    
    def get_orders(self, user_id: str) -> List[Order]:
        """Get user orders"""
        return [order for order in self.orders.values() if order.user_id == user_id]

class AITradingStrategy:
    """AI-powered trading strategy"""
    
    def __init__(self, trading_engine: TradingEngine):
        self.trading_engine = trading_engine
        self.strategy_name = "AI Momentum Strategy"
        self.symbols = ["AAPL", "TSLA", "MSFT", "GOOGL"]
        self.price_history: Dict[str, List[float]] = {symbol: [] for symbol in self.symbols}
        self.positions_limit = 4  # Max 4 positions
        
    async def analyze_and_trade(self, market_data: MarketData):
        """Analyze market data and make trading decisions"""
        symbol = market_data.symbol
        if symbol not in self.symbols:
            return
        
        # Store price history
        self.price_history[symbol].append(market_data.price)
        if len(self.price_history[symbol]) > 50:  # Keep last 50 prices
            self.price_history[symbol] = self.price_history[symbol][-50:]
        
        if len(self.price_history[symbol]) < 20:  # Need enough data
            return
        
        # Simple momentum strategy
        prices = np.array(self.price_history[symbol])
        
        # Calculate indicators
        sma_short = np.mean(prices[-5:])  # 5-period SMA
        sma_long = np.mean(prices[-20:])  # 20-period SMA
        rsi = self._calculate_rsi(prices)
        
        # Get current position
        portfolio = self.trading_engine.get_portfolio("ai_trader")
        if portfolio:
            current_positions = len([p for p in portfolio.positions if p.quantity > 0])
            position = next((p for p in portfolio.positions if p.symbol == symbol), None)
            
            # Trading signals
            if sma_short > sma_long * 1.02 and rsi < 70 and current_positions < self.positions_limit:
                # Strong bullish signal - Buy
                if not position or position.quantity == 0:
                    quantity = 10  # Buy 10 shares
                    await self.trading_engine.place_order(
                        "ai_trader", symbol, OrderSide.BUY, OrderType.MARKET, quantity
                    )
                    logger.info(f"🤖 AI Strategy: BUY signal for {symbol}")
            
            elif sma_short < sma_long * 0.98 or rsi > 80:
                # Bearish signal - Sell
                if position and position.quantity > 0:
                    await self.trading_engine.place_order(
                        "ai_trader", symbol, OrderSide.SELL, OrderType.MARKET, position.quantity
                    )
                    logger.info(f"🤖 AI Strategy: SELL signal for {symbol}")
    
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return 50  # Neutral value
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi

class AdminTradingInterface:
    """Admin interface for live trading management"""
    
    def __init__(self, trading_engine: TradingEngine, data_feed: RealTimeDataFeed):
        self.trading_engine = trading_engine
        self.data_feed = data_feed
        self.ai_strategy = AITradingStrategy(trading_engine)
        self.admin_user_id = "admin_trader"
        
        # Subscribe AI strategy to market data
        self.data_feed.subscribe(self.ai_strategy.analyze_and_trade)
    
    async def start_trading_session(self):
        """Start a live trading session"""
        logger.info("🚀 Starting Admin Trading Session with Real Data Simulation")
        logger.info("=" * 60)
        
        # Initialize admin portfolio
        if self.admin_user_id not in self.trading_engine.portfolios:
            self.trading_engine.portfolios[self.admin_user_id] = Portfolio(
                user_id=self.admin_user_id,
                cash_balance=500000.0,  # $500k for admin trading
                total_value=500000.0,
                positions=[],
                daily_pnl=0,
                total_return=0,
                total_return_percent=0
            )
        
        # Start market data feed
        data_feed_task = asyncio.create_task(self.data_feed.start_feed())
        
        # Start trading monitoring
        monitor_task = asyncio.create_task(self._monitor_trading())
        
        # Start user interface
        ui_task = asyncio.create_task(self._trading_interface())
        
        try:
            await asyncio.gather(data_feed_task, monitor_task, ui_task)
        except KeyboardInterrupt:
            logger.info("\n⏹️ Stopping trading session...")
            self.data_feed.stop_feed()
    
    async def _monitor_trading(self):
        """Monitor trading activity and performance"""
        while self.data_feed.running:
            portfolio = self.trading_engine.get_portfolio(self.admin_user_id)
            if portfolio:
                logger.info(f"💼 Portfolio Value: ${portfolio.total_value:,.2f} | "
                          f"PnL: ${portfolio.total_return:,.2f} ({portfolio.total_return_percent:.2f}%)")
            
            await asyncio.sleep(30)  # Update every 30 seconds
    
    async def _trading_interface(self):
        """Interactive trading interface"""
        logger.info("\n🎮 Admin Trading Interface")
        logger.info("Commands: buy [symbol] [quantity], sell [symbol] [quantity], portfolio, orders, help, quit")
        
        while self.data_feed.running:
            try:
                # Simulate user input (in real implementation, this would be actual input)
                await asyncio.sleep(5)
                
                # Auto-execute some demo trades
                if random.random() < 0.1:  # 10% chance every 5 seconds
                    await self._execute_demo_trade()
                
            except Exception as e:
                logger.error(f"Error in trading interface: {e}")
    
    async def _execute_demo_trade(self):
        """Execute a demo trade for simulation"""
        symbol = random.choice(self.data_feed.symbols)
        side = random.choice([OrderSide.BUY, OrderSide.SELL])
        quantity = random.randint(1, 20)
        
        # Get current portfolio to make intelligent decisions
        portfolio = self.trading_engine.get_portfolio(self.admin_user_id)
        if portfolio:
            position = next((p for p in portfolio.positions if p.symbol == symbol), None)
            
            # Don't sell if we don't have position
            if side == OrderSide.SELL and (not position or position.quantity <= 0):
                side = OrderSide.BUY
            
            # Limit buy orders based on available cash
            if side == OrderSide.BUY:
                market_data = self.data_feed.market_data.get(symbol)
                if market_data:
                    estimated_cost = quantity * market_data.ask
                    if estimated_cost > portfolio.cash_balance:
                        quantity = max(1, int(portfolio.cash_balance / market_data.ask))
        
        await self.trading_engine.place_order(
            self.admin_user_id, symbol, side, OrderType.MARKET, quantity
        )
    
    def get_trading_report(self) -> Dict[str, Any]:
        """Generate comprehensive trading report"""
        portfolio = self.trading_engine.get_portfolio(self.admin_user_id)
        orders = self.trading_engine.get_orders(self.admin_user_id)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "portfolio": asdict(portfolio) if portfolio else None,
            "total_orders": len(orders),
            "filled_orders": len([o for o in orders if o.status == OrderStatus.FILLED]),
            "pending_orders": len([o for o in orders if o.status == OrderStatus.PENDING]),
            "market_data": {symbol: asdict(data) for symbol, data in self.data_feed.market_data.items()},
            "performance_metrics": self._calculate_performance_metrics(portfolio, orders)
        }
        
        return report
    
    def _calculate_performance_metrics(self, portfolio: Optional[Portfolio], orders: List[Order]) -> Dict[str, Any]:
        """Calculate detailed performance metrics"""
        if not portfolio:
            return {}
        
        filled_orders = [o for o in orders if o.status == OrderStatus.FILLED]
        
        # Calculate win rate
        profitable_trades = 0
        total_trades = 0
        
        for position in portfolio.positions:
            if position.quantity == 0 and position.realized_pnl != 0:  # Closed position
                total_trades += 1
                if position.realized_pnl > 0:
                    profitable_trades += 1
        
        win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
        
        return {
            "total_return": portfolio.total_return,
            "total_return_percent": portfolio.total_return_percent,
            "win_rate": win_rate,
            "total_trades": total_trades,
            "profitable_trades": profitable_trades,
            "largest_position": max([abs(p.quantity * p.current_price) for p in portfolio.positions], default=0),
            "cash_utilization": ((500000 - portfolio.cash_balance) / 500000) * 100,
            "active_positions": len([p for p in portfolio.positions if p.quantity > 0])
        }

async def main():
    """Main function to run real data simulation"""
    logger.info("🏦 PROMETHEUS AI Trading Platform - Real Data Simulation")
    logger.info("=" * 60)
    
    # Initialize components
    data_feed = RealTimeDataFeed()
    trading_engine = TradingEngine(data_feed)
    admin_interface = AdminTradingInterface(trading_engine, data_feed)
    
    try:
        # Start trading session
        await admin_interface.start_trading_session()
    except KeyboardInterrupt:
        logger.info("\n👋 Trading simulation ended by user")
    except Exception as e:
        logger.error(f"💥 Trading simulation error: {e}")
    finally:
        # Generate final report
        final_report = admin_interface.get_trading_report()
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"trading_simulation_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(final_report, f, indent=2, default=str)
        
        logger.info(f"📊 Final trading report saved to: {filename}")
        
        # Display summary
        portfolio = final_report.get('portfolio')
        if portfolio:
            logger.info(f"\n📈 Final Portfolio Summary:")
            logger.info(f"   Total Value: ${portfolio['total_value']:,.2f}")
            logger.info(f"   Total Return: ${portfolio['total_return']:,.2f} ({portfolio['total_return_percent']:.2f}%)")
            logger.info(f"   Cash Balance: ${portfolio['cash_balance']:,.2f}")
            logger.info(f"   Active Positions: {len([p for p in portfolio['positions'] if p['quantity'] > 0])}")

if __name__ == "__main__":
    asyncio.run(main())
