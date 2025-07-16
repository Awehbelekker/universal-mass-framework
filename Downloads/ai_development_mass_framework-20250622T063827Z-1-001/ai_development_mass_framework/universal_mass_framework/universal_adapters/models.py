from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, JSON, Text, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    firebase_uid = Column(String(128), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    role = Column(String(50), default='beta_user')  # admin, investor, beta_user, developer
    is_active = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    kyc_status = Column(String(20), default='pending')  # pending, approved, rejected
    tenant_id = Column(String(100), default='default')
    permissions = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    profile_data = Column(JSON, default=dict)
    
    # Relationships
    trading_accounts = relationship("TradingAccount", back_populates="user")
    trades = relationship("Trade", back_populates="user")
    api_keys = relationship("APIKey", back_populates="user")
    workflows = relationship("Workflow", back_populates="user")

class TradingAccount(Base):
    __tablename__ = 'trading_accounts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_type = Column(String(20), default='paper')  # paper, live
    balance = Column(Float, default=0.0)
    currency = Column(String(10), default='USD')
    broker = Column(String(100))  # alpaca, interactive_brokers, etc.
    api_key = Column(String(255))
    api_secret = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_sync = Column(DateTime)
    account_data = Column(JSON, default=dict)
    
    # Relationships
    user = relationship("User", back_populates="trading_accounts")
    trades = relationship("Trade", back_populates="account")

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('trading_accounts.id'), nullable=False)
    symbol = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)  # buy, sell
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(20), default='pending')  # pending, filled, cancelled, rejected
    order_type = Column(String(20), default='market')  # market, limit, stop, stop_limit
    filled_price = Column(Float)
    commission = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    filled_at = Column(DateTime)
    cancelled_at = Column(DateTime)
    trade_data = Column(JSON, default=dict)
    
    # Relationships
    user = relationship("User", back_populates="trades")
    account = relationship("TradingAccount", back_populates="trades")

class APIKey(Base):
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    key_hash = Column(String(255), nullable=False)
    permissions = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)
    expires_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")

class AIAgent(Base):
    __tablename__ = 'ai_agents'
    
    id = Column(Integer, primary_key=True)
    agent_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    agent_type = Column(String(50), nullable=False)  # code_generator, business_analyst, etc.
    status = Column(String(20), default='active')  # active, inactive, maintenance
    capabilities = Column(JSON, default=list)
    performance_metrics = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity = Column(DateTime)
    configuration = Column(JSON, default=dict)

class Workflow(Base):
    __tablename__ = 'workflows'
    
    id = Column(Integer, primary_key=True)
    workflow_id = Column(String(100), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    workflow_type = Column(String(50), nullable=False)  # app_generation, trading, analysis
    status = Column(String(20), default='pending')  # pending, running, completed, failed
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    agents_involved = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    execution_time = Column(Float)  # in seconds
    error_message = Column(Text)

class SystemMetric(Base):
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(20))
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    category = Column(String(50))  # performance, trading, user_activity
    tags = Column(JSON, default=dict)

class TradingPerformance(Base):
    __tablename__ = 'trading_performance'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('trading_accounts.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    total_pnl = Column(Float, default=0.0)
    total_volume = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    sharpe_ratio = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserSession(Base):
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_id = Column(String(255), unique=True, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    session_data = Column(JSON, default=dict)

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50))  # trade, system, alert
    priority = Column(String(20), default='normal')  # low, normal, high, urgent
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime)
    action_url = Column(String(500))
    metadata = Column(JSON, default=dict)

# Indexes for performance
Index('idx_users_email', User.email)
Index('idx_users_firebase_uid', User.firebase_uid)
Index('idx_trades_user_symbol', Trade.user_id, Trade.symbol)
Index('idx_trades_created_at', Trade.created_at)
Index('idx_workflows_user_status', Workflow.user_id, Workflow.status)
Index('idx_system_metrics_timestamp', SystemMetric.timestamp)
Index('idx_trading_performance_date', TradingPerformance.date)
Index('idx_user_sessions_active', UserSession.user_id, UserSession.is_active) 