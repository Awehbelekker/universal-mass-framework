"""
Configuration Manager for Universal MASS Framework

Handles all configuration management including environment variables,
data source configurations, and enterprise settings.
"""

import os
import json
import yaml
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Environment(Enum):
    """Supported environments"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class SecurityLevel(Enum):
    """Security configuration levels"""
    BASIC = "basic"
    STANDARD = "standard"
    HIGH = "high"
    ENTERPRISE = "enterprise"


@dataclass
class DataSourceConfig:
    """Configuration for data sources"""
    name: str
    type: str
    endpoint: str
    api_key: Optional[str] = None
    rate_limit: int = 100
    timeout: int = 30
    retry_attempts: int = 3
    enabled: bool = True
    priority: int = 1
    cache_ttl: int = 300


@dataclass
class TrustConfig:
    """Configuration for enterprise trust framework"""
    enabled: bool = True
    human_review_required: bool = False
    explanation_depth: str = "standard"  # basic, standard, detailed
    audit_level: str = "comprehensive"   # basic, standard, comprehensive
    compliance_standards: List[str] = field(default_factory=lambda: ["SOC2", "GDPR"])
    bias_detection: bool = True
    fairness_monitoring: bool = True


@dataclass
class PerformanceConfig:
    """Performance and scaling configuration"""
    max_concurrent_requests: int = 1000
    request_timeout: int = 30
    cache_size_mb: int = 512
    connection_pool_size: int = 50
    worker_processes: int = 4
    enable_clustering: bool = False


class MassConfig:
    """
    Comprehensive configuration manager for Universal MASS Framework
    
    Handles configuration from multiple sources:
    - Environment variables
    - Configuration files (YAML/JSON)
    - Runtime settings
    - Enterprise overrides
    """
    
    def __init__(self, config_path: Optional[str] = None, environment: Optional[str] = None):
        self.environment = Environment(environment or os.getenv("MASS_ENVIRONMENT", "development"))
        self.config_path = config_path or self._get_default_config_path()
        
        # Initialize configurations
        self.data_sources: Dict[str, DataSourceConfig] = {}
        self.trust_config = TrustConfig()
        self.performance_config = PerformanceConfig()
        
        # Core settings
        self.api_keys = {}
        self.database_url = ""
        self.redis_url = ""
        self.log_level = "INFO"
        self.debug = False
        
        # Enterprise settings
        self.enterprise_mode = False
        self.data_residency_region = "us-east-1"
        self.customer_managed_encryption = False
        
        # Load configuration
        self._load_configuration()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        base_path = Path(__file__).parent.parent
        return str(base_path / "config" / f"{self.environment.value}.yaml")
    
    def _load_configuration(self):
        """Load configuration from all sources"""
        try:
            # Load from environment variables
            self._load_from_environment()
            
            # Load from configuration file if exists
            if os.path.exists(self.config_path):
                self._load_from_file()
            else:
                logger.warning(f"Configuration file not found: {self.config_path}")
                self._create_default_config()
            
            # Load data source configurations
            self._load_data_sources()
            
            # Validate configuration
            self._validate_configuration()
            
            logger.info(f"Configuration loaded successfully for {self.environment.value} environment")
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            raise
    
    def _load_from_environment(self):
        """Load configuration from environment variables"""
        # Core settings
        self.debug = os.getenv("MASS_DEBUG", "false").lower() == "true"
        self.log_level = os.getenv("MASS_LOG_LEVEL", "INFO")
        self.database_url = os.getenv("MASS_DATABASE_URL", "sqlite:///mass_framework.db")
        self.redis_url = os.getenv("MASS_REDIS_URL", "redis://localhost:6379")
        
        # Enterprise settings
        self.enterprise_mode = os.getenv("MASS_ENTERPRISE_MODE", "false").lower() == "true"
        self.data_residency_region = os.getenv("MASS_DATA_RESIDENCY_REGION", "us-east-1")
        self.customer_managed_encryption = os.getenv("MASS_CUSTOMER_ENCRYPTION", "false").lower() == "true"
        
        # API keys
        self.api_keys = {
            "alpha_vantage": os.getenv("ALPHA_VANTAGE_API_KEY"),
            "twitter": os.getenv("TWITTER_API_KEY"),
            "reddit": os.getenv("REDDIT_API_KEY"),
            "news_api": os.getenv("NEWS_API_KEY"),
            "openweather": os.getenv("OPENWEATHER_API_KEY"),
            "github": os.getenv("GITHUB_API_KEY"),
        }
        
        # Performance settings
        self.performance_config.max_concurrent_requests = int(
            os.getenv("MASS_MAX_CONCURRENT_REQUESTS", "1000")
        )
        self.performance_config.request_timeout = int(
            os.getenv("MASS_REQUEST_TIMEOUT", "30")
        )
        self.performance_config.worker_processes = int(
            os.getenv("MASS_WORKER_PROCESSES", "4")
        )
    
    def _load_from_file(self):
        """Load configuration from YAML/JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    config_data = yaml.safe_load(f)
                else:
                    config_data = json.load(f)
            
            # Update settings from file
            if 'trust_framework' in config_data:
                trust_data = config_data['trust_framework']
                self.trust_config = TrustConfig(
                    enabled=trust_data.get('enabled', True),
                    human_review_required=trust_data.get('human_review_required', False),
                    explanation_depth=trust_data.get('explanation_depth', 'standard'),
                    audit_level=trust_data.get('audit_level', 'comprehensive'),
                    compliance_standards=trust_data.get('compliance_standards', ['SOC2', 'GDPR']),
                    bias_detection=trust_data.get('bias_detection', True),
                    fairness_monitoring=trust_data.get('fairness_monitoring', True)
                )
            
            if 'performance' in config_data:
                perf_data = config_data['performance']
                self.performance_config = PerformanceConfig(
                    max_concurrent_requests=perf_data.get('max_concurrent_requests', 1000),
                    request_timeout=perf_data.get('request_timeout', 30),
                    cache_size_mb=perf_data.get('cache_size_mb', 512),
                    connection_pool_size=perf_data.get('connection_pool_size', 50),
                    worker_processes=perf_data.get('worker_processes', 4),
                    enable_clustering=perf_data.get('enable_clustering', False)
                )
            
            logger.info("Configuration loaded from file successfully")
            
        except Exception as e:
            logger.error(f"Failed to load configuration file: {str(e)}")
            raise
    
    def _create_default_config(self):
        """Create default configuration file"""
        default_config = {
            "environment": self.environment.value,
            "trust_framework": {
                "enabled": True,
                "human_review_required": self.environment == Environment.PRODUCTION,
                "explanation_depth": "standard",
                "audit_level": "comprehensive",
                "compliance_standards": ["SOC2", "GDPR"],
                "bias_detection": True,
                "fairness_monitoring": True
            },
            "performance": {
                "max_concurrent_requests": 1000,
                "request_timeout": 30,
                "cache_size_mb": 512,
                "connection_pool_size": 50,
                "worker_processes": 4,
                "enable_clustering": False
            },
            "data_sources": {
                "enabled_sources": [
                    "alpha_vantage",
                    "twitter",
                    "reddit", 
                    "news_api",
                    "openweather",
                    "github"
                ],
                "rate_limits": {
                    "default": 100,
                    "alpha_vantage": 5,
                    "twitter": 300
                }
            }
        }
        
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Write default config
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        logger.info(f"Default configuration created at {self.config_path}")
    
    def _load_data_sources(self):
        """Load and configure data sources"""
        # Financial sources
        if self.api_keys.get("alpha_vantage"):
            self.data_sources["alpha_vantage"] = DataSourceConfig(
                name="alpha_vantage",
                type="financial",
                endpoint="https://www.alphavantage.co/query",
                api_key=self.api_keys["alpha_vantage"],
                rate_limit=5,  # Alpha Vantage has strict rate limits
                priority=1
            )
        
        # Social sources
        if self.api_keys.get("twitter"):
            self.data_sources["twitter"] = DataSourceConfig(
                name="twitter",
                type="social",
                endpoint="https://api.twitter.com/2",
                api_key=self.api_keys["twitter"],
                rate_limit=300,
                priority=1
            )
        
        if self.api_keys.get("reddit"):
            self.data_sources["reddit"] = DataSourceConfig(
                name="reddit",
                type="social",
                endpoint="https://oauth.reddit.com",
                api_key=self.api_keys["reddit"],
                rate_limit=60,
                priority=2
            )
        
        # News sources
        if self.api_keys.get("news_api"):
            self.data_sources["news_api"] = DataSourceConfig(
                name="news_api",
                type="news",
                endpoint="https://newsapi.org/v2",
                api_key=self.api_keys["news_api"],
                rate_limit=100,
                priority=1
            )
        
        # Weather sources
        if self.api_keys.get("openweather"):
            self.data_sources["openweather"] = DataSourceConfig(
                name="openweather",
                type="weather",
                endpoint="https://api.openweathermap.org/data/2.5",
                api_key=self.api_keys["openweather"],
                rate_limit=60,
                priority=3
            )
        
        # Technology sources
        if self.api_keys.get("github"):
            self.data_sources["github"] = DataSourceConfig(
                name="github",
                type="technology",
                endpoint="https://api.github.com",
                api_key=self.api_keys["github"],
                rate_limit=5000,
                priority=2
            )
        
        # Free sources (no API key required)
        self.data_sources["yahoo_finance"] = DataSourceConfig(
            name="yahoo_finance",
            type="financial",
            endpoint="https://query1.finance.yahoo.com",
            rate_limit=100,
            priority=2
        )
        
        self.data_sources["coingecko"] = DataSourceConfig(
            name="coingecko",
            type="financial",
            endpoint="https://api.coingecko.com/api/v3",
            rate_limit=50,
            priority=2
        )
        
        logger.info(f"Loaded {len(self.data_sources)} data source configurations")
    
    def _validate_configuration(self):
        """Validate configuration settings"""
        # Check required settings for production
        if self.environment == Environment.PRODUCTION:
            if not self.database_url or self.database_url.startswith("sqlite"):
                logger.warning("Production environment should use a production database")
            
            if not self.customer_managed_encryption:
                logger.warning("Consider enabling customer-managed encryption for production")
        
        # Validate trust configuration
        if self.enterprise_mode and not self.trust_config.enabled:
            raise ValueError("Trust framework is required for enterprise mode")
        
        # Validate data source configurations
        enabled_sources = [name for name, config in self.data_sources.items() if config.enabled]
        if len(enabled_sources) < 3:
            logger.warning("Less than 3 data sources enabled - intelligence quality may be reduced")
        
        logger.info("Configuration validation completed")
    
    def get_data_source_config(self, source_name: str) -> Optional[DataSourceConfig]:
        """Get configuration for a specific data source"""
        return self.data_sources.get(source_name)
    
    def get_enabled_data_sources(self) -> Dict[str, DataSourceConfig]:
        """Get all enabled data source configurations"""
        return {name: config for name, config in self.data_sources.items() if config.enabled}
    
    def update_api_key(self, source_name: str, api_key: str):
        """Update API key for a data source"""
        self.api_keys[source_name] = api_key
        if source_name in self.data_sources:
            self.data_sources[source_name].api_key = api_key
    
    def enable_enterprise_mode(self, data_residency_region: str = "us-east-1"):
        """Enable enterprise mode with enhanced security and compliance"""
        self.enterprise_mode = True
        self.data_residency_region = data_residency_region
        self.customer_managed_encryption = True
        self.trust_config.enabled = True
        self.trust_config.human_review_required = True
        self.trust_config.audit_level = "comprehensive"
        
        logger.info("Enterprise mode enabled with enhanced security")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "environment": self.environment.value,
            "enterprise_mode": self.enterprise_mode,
            "data_residency_region": self.data_residency_region,
            "customer_managed_encryption": self.customer_managed_encryption,
            "debug": self.debug,
            "log_level": self.log_level,
            "trust_config": {
                "enabled": self.trust_config.enabled,
                "human_review_required": self.trust_config.human_review_required,
                "explanation_depth": self.trust_config.explanation_depth,
                "audit_level": self.trust_config.audit_level,
                "compliance_standards": self.trust_config.compliance_standards,
                "bias_detection": self.trust_config.bias_detection,
                "fairness_monitoring": self.trust_config.fairness_monitoring
            },
            "performance_config": {
                "max_concurrent_requests": self.performance_config.max_concurrent_requests,
                "request_timeout": self.performance_config.request_timeout,
                "cache_size_mb": self.performance_config.cache_size_mb,
                "connection_pool_size": self.performance_config.connection_pool_size,
                "worker_processes": self.performance_config.worker_processes,
                "enable_clustering": self.performance_config.enable_clustering
            },
            "data_sources_count": len(self.get_enabled_data_sources())
        }