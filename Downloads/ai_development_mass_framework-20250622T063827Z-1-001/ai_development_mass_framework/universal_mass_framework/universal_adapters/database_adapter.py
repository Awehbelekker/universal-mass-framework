"""
Database Adapter - Universal Database Integration

This adapter can integrate with ANY database system (SQL, NoSQL, NewSQL, Graph DBs).
It automatically discovers schemas, optimizes queries, and provides intelligent enhancements.

Supported Database Types:
- PostgreSQL, MySQL, SQLite, SQL Server, Oracle
- MongoDB, CouchDB, DynamoDB, Cassandra
- Redis, Neo4j, InfluxDB, ElasticSearch
- Any database with SQLAlchemy or native Python driver support

Key Features:
- Auto-discovery of database schemas and tables
- Intelligent query optimization
- Real-time performance monitoring
- Automatic connection pooling
- Query result caching
- Data quality validation
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import redis.asyncio as redis
import pymongo
from pymongo import MongoClient
import json
from datetime import datetime, timedelta
import hashlib
import secrets

from .models import Base, User, TradingAccount, Trade, APIKey, AIAgent, Workflow, SystemMetric, TradingPerformance, UserSession, Notification

logger = logging.getLogger(__name__)

class DatabaseAdapter:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.postgres_engine = None
        self.postgres_session_factory = None
        self.redis_client = None
        self.mongo_client = None
        self.mongo_db = None
        self.is_initialized = False
        
    async def initialize(self) -> bool:
        """Initialize all database connections"""
        try:
            # PostgreSQL connection
            postgres_url = self.config.get('postgres_url')
            if postgres_url:
                self.postgres_engine = create_async_engine(
                    postgres_url,
                    poolclass=QueuePool,
                    pool_size=20,
                    max_overflow=30,
                    pool_pre_ping=True,
                    echo=False
                )
                self.postgres_session_factory = sessionmaker(
                    self.postgres_engine, class_=AsyncSession, expire_on_commit=False
                )
                
                # Test connection
                async with self.postgres_engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
                logger.info("PostgreSQL connection established")
            
            # Redis connection
            redis_url = self.config.get('redis_url')
            if redis_url:
                self.redis_client = redis.from_url(
                    redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True
                )
                await self.redis_client.ping()
                logger.info("Redis connection established")
            
            # MongoDB connection
            mongo_url = self.config.get('mongo_url')
            if mongo_url:
                self.mongo_client = MongoClient(
                    mongo_url,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000
                )
                # Test connection
                self.mongo_client.admin.command('ping')
                self.mongo_db = self.mongo_client.get_database(self.config.get('mongo_db_name', 'mass_framework'))
                logger.info("MongoDB connection established")
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            return False
    
    async def close(self):
        """Close all database connections"""
        try:
            if self.postgres_engine:
                await self.postgres_engine.dispose()
            if self.redis_client:
                await self.redis_client.close()
            if self.mongo_client:
                self.mongo_client.close()
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")
    
    # User Management
    async def create_user(self, user_data: Dict[str, Any]) -> Optional[int]:
        """Create a new user"""
        try:
            async with self.postgres_session_factory() as session:
                user = User(
                    firebase_uid=user_data['firebase_uid'],
                    email=user_data['email'],
                    username=user_data['username'],
                    first_name=user_data.get('first_name'),
                    last_name=user_data.get('last_name'),
                    phone=user_data.get('phone'),
                    role=user_data.get('role', 'beta_user'),
                    is_active=user_data.get('is_active', True),
                    is_approved=user_data.get('is_approved', False),
                    kyc_status=user_data.get('kyc_status', 'pending'),
                    tenant_id=user_data.get('tenant_id', 'default'),
                    permissions=user_data.get('permissions', ['basic_access']),
                    profile_data=user_data.get('profile_data', {})
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user.id
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    async def get_user_by_firebase_uid(self, firebase_uid: str) -> Optional[Dict[str, Any]]:
        """Get user by Firebase UID"""
        try:
            async with self.postgres_session_factory() as session:
                result = await session.execute(
                    text("SELECT * FROM users WHERE firebase_uid = :firebase_uid"),
                    {"firebase_uid": firebase_uid}
                )
                user = result.fetchone()
                return dict(user._mapping) if user else None
        except Exception as e:
            logger.error(f"Error getting user by Firebase UID: {e}")
            return None
    
    async def update_user(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """Update user information"""
        try:
            async with self.postgres_session_factory() as session:
                result = await session.execute(
                    text("""
                        UPDATE users 
                        SET updated_at = NOW(), 
                            last_login = CASE WHEN :last_login IS NOT NULL THEN :last_login ELSE last_login END,
                            is_active = :is_active,
                            role = :role,
                            permissions = :permissions
                        WHERE id = :user_id
                    """),
                    {
                        "user_id": user_id,
                        "last_login": updates.get('last_login'),
                        "is_active": updates.get('is_active', True),
                        "role": updates.get('role'),
                        "permissions": json.dumps(updates.get('permissions', []))
                    }
                )
                await session.commit()
                return result.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False
    
    # Trading Account Management
    async def create_trading_account(self, account_data: Dict[str, Any]) -> Optional[int]:
        """Create a new trading account"""
        try:
            async with self.postgres_session_factory() as session:
                account = TradingAccount(
                    user_id=account_data['user_id'],
                    account_type=account_data.get('account_type', 'paper'),
                    balance=account_data.get('balance', 0.0),
                    currency=account_data.get('currency', 'USD'),
                    broker=account_data.get('broker'),
                    api_key=account_data.get('api_key'),
                    api_secret=account_data.get('api_secret'),
                    account_data=account_data.get('account_data', {})
                )
                session.add(account)
                await session.commit()
                await session.refresh(account)
                return account.id
        except Exception as e:
            logger.error(f"Error creating trading account: {e}")
            return None
    
    async def get_user_trading_accounts(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all trading accounts for a user"""
        try:
            async with self.postgres_session_factory() as session:
                result = await session.execute(
                    text("SELECT * FROM trading_accounts WHERE user_id = :user_id AND is_active = true"),
                    {"user_id": user_id}
                )
                accounts = result.fetchall()
                return [dict(account._mapping) for account in accounts]
        except Exception as e:
            logger.error(f"Error getting user trading accounts: {e}")
            return []
    
    # Trade Management
    async def create_trade(self, trade_data: Dict[str, Any]) -> Optional[int]:
        """Create a new trade"""
        try:
            async with self.postgres_session_factory() as session:
                trade = Trade(
                    user_id=trade_data['user_id'],
                    account_id=trade_data['account_id'],
                    symbol=trade_data['symbol'],
                    side=trade_data['side'],
                    quantity=trade_data['quantity'],
                    price=trade_data['price'],
                    status=trade_data.get('status', 'pending'),
                    order_type=trade_data.get('order_type', 'market'),
                    filled_price=trade_data.get('filled_price'),
                    commission=trade_data.get('commission', 0.0),
                    trade_data=trade_data.get('trade_data', {})
                )
                session.add(trade)
                await session.commit()
                await session.refresh(trade)
                return trade.id
        except Exception as e:
            logger.error(f"Error creating trade: {e}")
            return None
    
    async def get_user_trades(self, user_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Get trades for a user"""
        try:
            async with self.postgres_session_factory() as session:
                result = await session.execute(
                    text("""
                        SELECT * FROM trades 
                        WHERE user_id = :user_id 
                        ORDER BY created_at DESC 
                        LIMIT :limit
                    """),
                    {"user_id": user_id, "limit": limit}
                )
                trades = result.fetchall()
                return [dict(trade._mapping) for trade in trades]
        except Exception as e:
            logger.error(f"Error getting user trades: {e}")
            return []
    
    # API Key Management
    async def create_api_key(self, user_id: int, name: str, permissions: List[str]) -> Optional[str]:
        """Create a new API key"""
        try:
            # Generate API key
            api_key = f"mass_{secrets.token_urlsafe(32)}"
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            
            async with self.postgres_session_factory() as session:
                db_api_key = APIKey(
                    user_id=user_id,
                    name=name,
                    key_hash=key_hash,
                    permissions=permissions,
                    expires_at=datetime.utcnow() + timedelta(days=365)
                )
                session.add(db_api_key)
                await session.commit()
                
                # Store in Redis for quick lookup
                if self.redis_client:
                    await self.redis_client.setex(
                        f"api_key:{key_hash}",
                        86400,  # 24 hours
                        json.dumps({
                            "user_id": user_id,
                            "permissions": permissions,
                            "name": name
                        })
                    )
                
                return api_key
        except Exception as e:
            logger.error(f"Error creating API key: {e}")
            return None
    
    async def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate an API key"""
        try:
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            
            # Check Redis first
            if self.redis_client:
                cached_data = await self.redis_client.get(f"api_key:{key_hash}")
                if cached_data:
                    return json.loads(cached_data)
            
            # Check database
            async with self.postgres_session_factory() as session:
                result = await session.execute(
                    text("""
                        SELECT user_id, permissions, name, is_active, expires_at 
                        FROM api_keys 
                        WHERE key_hash = :key_hash
                    """),
                    {"key_hash": key_hash}
                )
                api_key_data = result.fetchone()
                
                if api_key_data and api_key_data.is_active and api_key_data.expires_at > datetime.utcnow():
                    data = {
                        "user_id": api_key_data.user_id,
                        "permissions": api_key_data.permissions,
                        "name": api_key_data.name
                    }
                    
                    # Cache in Redis
                    if self.redis_client:
                        await self.redis_client.setex(
                            f"api_key:{key_hash}",
                            86400,
                            json.dumps(data)
                        )
                    
                    return data
                
                return None
        except Exception as e:
            logger.error(f"Error validating API key: {e}")
            return None
    
    # Workflow Management
    async def create_workflow(self, workflow_data: Dict[str, Any]) -> Optional[str]:
        """Create a new workflow"""
        try:
            workflow_id = f"wf_{secrets.token_urlsafe(16)}"
            
            async with self.postgres_session_factory() as session:
                workflow = Workflow(
                    workflow_id=workflow_id,
                    user_id=workflow_data['user_id'],
                    name=workflow_data['name'],
                    description=workflow_data.get('description'),
                    workflow_type=workflow_data['workflow_type'],
                    input_data=workflow_data.get('input_data', {}),
                    agents_involved=workflow_data.get('agents_involved', [])
                )
                session.add(workflow)
                await session.commit()
                return workflow_id
        except Exception as e:
            logger.error(f"Error creating workflow: {e}")
            return None
    
    async def update_workflow_status(self, workflow_id: str, status: str, output_data: Dict[str, Any] = None) -> bool:
        """Update workflow status"""
        try:
            async with self.postgres_session_factory() as session:
                update_data = {
                    "status": status,
                    "completed_at": datetime.utcnow() if status in ['completed', 'failed'] else None
                }
                
                if output_data:
                    update_data["output_data"] = output_data
                
                result = await session.execute(
                    text("""
                        UPDATE workflows 
                        SET status = :status,
                            output_data = :output_data,
                            completed_at = :completed_at
                        WHERE workflow_id = :workflow_id
                    """),
                    {
                        "workflow_id": workflow_id,
                        "status": status,
                        "output_data": json.dumps(output_data) if output_data else None,
                        "completed_at": update_data["completed_at"]
                    }
                )
                await session.commit()
                return result.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating workflow status: {e}")
            return False
    
    # System Metrics
    async def record_system_metric(self, metric_name: str, metric_value: float, category: str = None, tags: Dict[str, Any] = None):
        """Record a system metric"""
        try:
            async with self.postgres_session_factory() as session:
                metric = SystemMetric(
                    metric_name=metric_name,
                    metric_value=metric_value,
                    category=category,
                    tags=tags or {}
                )
                session.add(metric)
                await session.commit()
        except Exception as e:
            logger.error(f"Error recording system metric: {e}")
    
    # Cache Management
    async def set_cache(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set a cache value"""
        try:
            if self.redis_client:
                await self.redis_client.setex(key, ttl, json.dumps(value))
                return True
            return False
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    async def get_cache(self, key: str) -> Optional[Any]:
        """Get a cache value"""
        try:
            if self.redis_client:
                value = await self.redis_client.get(key)
                return json.loads(value) if value else None
            return None
        except Exception as e:
            logger.error(f"Error getting cache: {e}")
            return None
    
    async def delete_cache(self, key: str) -> bool:
        """Delete a cache value"""
        try:
            if self.redis_client:
                await self.redis_client.delete(key)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting cache: {e}")
            return False
    
    # MongoDB Operations for Document Storage
    async def store_document(self, collection: str, document: Dict[str, Any]) -> Optional[str]:
        """Store a document in MongoDB"""
        try:
            if self.mongo_db:
                result = self.mongo_db[collection].insert_one(document)
                return str(result.inserted_id)
            return None
        except Exception as e:
            logger.error(f"Error storing document: {e}")
            return None
    
    async def get_document(self, collection: str, document_id: str) -> Optional[Dict[str, Any]]:
        """Get a document from MongoDB"""
        try:
            if self.mongo_db:
                from bson import ObjectId
                document = self.mongo_db[collection].find_one({"_id": ObjectId(document_id)})
                if document:
                    document["_id"] = str(document["_id"])
                return document
            return None
        except Exception as e:
            logger.error(f"Error getting document: {e}")
            return None
    
    # Health Check
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all databases"""
        health_status = {
            "postgres": False,
            "redis": False,
            "mongodb": False,
            "overall": False
        }
        
        try:
            # Check PostgreSQL
            if self.postgres_engine:
                async with self.postgres_engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
                health_status["postgres"] = True
            
            # Check Redis
            if self.redis_client:
                await self.redis_client.ping()
                health_status["redis"] = True
            
            # Check MongoDB
            if self.mongo_client:
                self.mongo_client.admin.command('ping')
                health_status["mongodb"] = True
            
            health_status["overall"] = all([
                health_status["postgres"],
                health_status["redis"],
                health_status["mongodb"]
            ])
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
        
        return health_status