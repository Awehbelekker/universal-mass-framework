import pytest
import asyncio
import os
import tempfile
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, Generator
import json

# Import our models and adapters
try:
    from universal_mass_framework.universal_adapters.models import Base, User, TradingAccount, Trade, Portfolio, Position, AIAgent
    from universal_mass_framework.universal_adapters.database_adapter import DatabaseAdapter
    from universal_mass_framework.core.agent_coordinator import MASSCoordinator
    from data_sources.real_api_integrations import MarketDataAPI, NewsAPI, SocialMediaAPI
except ImportError:
    # Create mock classes if imports fail
    class Base:
        pass
    
    class User:
        pass
    
    class TradingAccount:
        pass
    
    class Trade:
        pass
    
    class Portfolio:
        pass
    
    class Position:
        pass
    
    class AIAgent:
        pass
    
    class DatabaseAdapter:
        pass
    
    class MASSCoordinator:
        pass
    
    class MarketDataAPI:
        pass
    
    class NewsAPI:
        pass
    
    class SocialMediaAPI:
        pass

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_database():
    """Mock database for testing"""
    mock_db = Mock(spec=DatabaseAdapter)
    
    # Mock database initialization
    mock_db.initialize = AsyncMock(return_value=True)
    
    # Mock user operations
    mock_db.create_user = AsyncMock(return_value=1)
    mock_db.get_user_by_firebase_uid = AsyncMock(return_value={
        'id': 1,
        'firebase_uid': 'test_uid_123',
        'email': 'test@example.com',
        'username': 'testuser',
        'role': 'user',
        'is_active': True,
        'is_approved': True
    })
    
    # Mock trading account operations
    mock_db.create_trading_account = AsyncMock(return_value=1)
    mock_db.get_trading_accounts = AsyncMock(return_value=[
        {
            'id': 1,
            'user_id': 1,
            'account_type': 'paper',
            'account_name': 'Test Account',
            'balance': 10000.0,
            'currency': 'USD'
        }
    ])
    
    # Mock trade operations
    mock_db.create_trade = AsyncMock(return_value=1)
    mock_db.get_trades = AsyncMock(return_value=[])
    
    return mock_db

@pytest.fixture
def mock_coordinator():
    """Mock coordinator for testing"""
    mock_coord = Mock(spec=MASSCoordinator)
    
    # Mock agent registration
    mock_coord.register_agent = Mock()
    mock_coord.route_message = AsyncMock()
    mock_coord.execute_app_generation_workflow = AsyncMock(return_value={
        'status': 'success',
        'result': 'Mock workflow result'
    })
    
    return mock_coord

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "firebase_uid": "test_uid_123",
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890",
        "role": "user",
        "is_active": True,
        "is_approved": True,
        "kyc_status": "approved",
        "timezone": "UTC",
        "language": "en"
    }

@pytest.fixture
def sample_trade_data():
    """Sample trade data for testing"""
    return {
        "user_id": 1,
        "account_id": 1,
        "symbol": "AAPL",
        "side": "buy",
        "quantity": 10.0,
        "price": 150.0,
        "total_amount": 1500.0,
        "order_type": "market",
        "status": "pending"
    }

@pytest.fixture
def sample_trading_account_data():
    """Sample trading account data for testing"""
    return {
        "user_id": 1,
        "account_type": "paper",
        "account_name": "Test Trading Account",
        "balance": 10000.0,
        "currency": "USD",
        "broker": "Test Broker",
        "risk_level": "medium",
        "is_active": True
    }

@pytest.fixture
def mock_market_data_api():
    """Mock market data API for testing"""
    mock_api = Mock(spec=MarketDataAPI)
    
    mock_api.get_stock_data = AsyncMock(return_value={
        "symbol": "AAPL",
        "price": 150.0,
        "change": 2.5,
        "change_percent": 1.67,
        "volume": 1000000,
        "market_cap": 2500000000000,
        "timestamp": "2024-01-01T12:00:00",
        "source": "mock"
    })
    
    return mock_api

@pytest.fixture
def mock_news_api():
    """Mock news API for testing"""
    mock_api = Mock(spec=NewsAPI)
    
    mock_api.get_market_news = AsyncMock(return_value=[
        {
            "title": "Test News Article",
            "description": "This is a test news article",
            "url": "https://example.com/test",
            "source": "Test News",
            "published_at": "2024-01-01T12:00:00",
            "sentiment": "positive"
        }
    ])
    
    return mock_api

@pytest.fixture
def mock_social_api():
    """Mock social media API for testing"""
    mock_api = Mock(spec=SocialMediaAPI)
    
    mock_api.get_trading_sentiment = AsyncMock(return_value={
        "twitter": {
            "positive_count": 50,
            "negative_count": 20,
            "total_tweets": 100,
            "sentiment_score": 0.3,
            "total_engagement": 1000
        },
        "reddit": {
            "positive_count": 30,
            "negative_count": 15,
            "total_posts": 50,
            "sentiment_score": 0.2,
            "total_upvotes": 500
        },
        "combined": {
            "positive_count": 80,
            "negative_count": 35,
            "total_mentions": 150,
            "sentiment_score": 0.25,
            "sentiment_label": "positive"
        }
    })
    
    return mock_api

@pytest.fixture
def test_config():
    """Test configuration"""
    return {
        'database': {
            'postgres_url': 'postgresql+asyncpg://test:test@localhost/test_db',
            'redis_url': 'redis://localhost:6379',
            'mongo_url': 'mongodb://localhost:27017/test'
        },
        'firebase': {
            'api_key': 'test_api_key',
            'auth_domain': 'test.firebaseapp.com',
            'project_id': 'test-project'
        },
        'apis': {
            'alpha_vantage_key': 'test_key',
            'news_api_key': 'test_key',
            'twitter_bearer_token': 'test_token',
            'yahoo_finance_enabled': True,
            'reddit_enabled': True
        },
        'cache': {
            'cache_ttl': 300
        }
    }

@pytest.fixture
def temp_db_file():
    """Create a temporary database file for testing"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    yield db_path
    
    # Cleanup
    try:
        os.unlink(db_path)
    except OSError:
        pass

@pytest.fixture
def mock_firebase_auth():
    """Mock Firebase authentication"""
    with patch('firebase_admin.auth.verify_id_token') as mock_verify:
        mock_verify.return_value = {
            'uid': 'test_uid_123',
            'email': 'test@example.com',
            'email_verified': True,
            'name': 'Test User'
        }
        yield mock_verify

@pytest.fixture
def mock_http_client():
    """Mock HTTP client for API testing"""
    with patch('aiohttp.ClientSession') as mock_session:
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={'status': 'success'})
        mock_response.text = AsyncMock(return_value='{"status": "success"}')
        
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
        
        yield mock_session

@pytest.fixture
def sample_portfolio_data():
    """Sample portfolio data for testing"""
    return {
        "user_id": 1,
        "name": "Test Portfolio",
        "description": "A test portfolio for testing",
        "initial_balance": 10000.0,
        "current_balance": 10500.0,
        "currency": "USD",
        "risk_tolerance": "medium",
        "investment_goal": "growth",
        "time_horizon": "long",
        "is_active": True
    }

@pytest.fixture
def sample_position_data():
    """Sample position data for testing"""
    return {
        "user_id": 1,
        "account_id": 1,
        "portfolio_id": 1,
        "symbol": "AAPL",
        "side": "long",
        "quantity": 10.0,
        "average_price": 150.0,
        "current_price": 155.0,
        "market_value": 1550.0,
        "unrealized_pnl": 50.0,
        "is_open": True
    }

@pytest.fixture
def sample_ai_agent_data():
    """Sample AI agent data for testing"""
    return {
        "user_id": 1,
        "name": "Test Trading Agent",
        "agent_type": "trading",
        "model_type": "gpt-4",
        "status": "active",
        "configuration": {
            "risk_level": "medium",
            "max_position_size": 1000.0,
            "trading_strategy": "momentum"
        },
        "performance_metrics": {
            "total_trades": 50,
            "win_rate": 0.65,
            "total_pnl": 2500.0
        }
    }

@pytest.fixture
def mock_logger():
    """Mock logger for testing"""
    with patch('logging.getLogger') as mock_get_logger:
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        yield mock_logger

@pytest.fixture
def mock_redis():
    """Mock Redis client for testing"""
    with patch('redis.from_url') as mock_redis_client:
        mock_redis = Mock()
        mock_redis.ping = AsyncMock()
        mock_redis.get = Mock(return_value=None)
        mock_redis.set = Mock()
        mock_redis.delete = Mock()
        mock_redis_client.return_value = mock_redis
        yield mock_redis

@pytest.fixture
def mock_mongo():
    """Mock MongoDB client for testing"""
    with patch('pymongo.MongoClient') as mock_mongo_client:
        mock_mongo = Mock()
        mock_mongo.admin.command = Mock(return_value={'ok': 1})
        mock_mongo_client.return_value = mock_mongo
        yield mock_mongo

@pytest.fixture
def mock_sqlalchemy():
    """Mock SQLAlchemy for testing"""
    with patch('sqlalchemy.create_async_engine') as mock_engine, \
         patch('sqlalchemy.orm.sessionmaker') as mock_sessionmaker:
        
        mock_engine_instance = Mock()
        mock_engine.return_value = mock_engine_instance
        
        mock_session = Mock()
        mock_sessionmaker.return_value = mock_session
        
        yield {
            'engine': mock_engine_instance,
            'session': mock_session
        }

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment variables"""
    # Set test environment variables
    os.environ['TESTING'] = 'true'
    os.environ['DATABASE_URL'] = 'sqlite:///test.db'
    os.environ['REDIS_URL'] = 'redis://localhost:6379'
    
    yield
    
    # Cleanup
    if 'TESTING' in os.environ:
        del os.environ['TESTING']
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    if 'REDIS_URL' in os.environ:
        del os.environ['REDIS_URL'] 