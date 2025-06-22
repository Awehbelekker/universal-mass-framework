"""
AI Configuration Management for MASS Framework
Handles API keys, model settings, and provider configurations
"""

import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import yaml

class AIProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL_OLLAMA = "ollama"
    AZURE_OPENAI = "azure_openai"

@dataclass
class ModelConfig:
    """Configuration for a specific AI model"""
    name: str
    provider: AIProvider
    max_tokens: int = 4000
    temperature: float = 0.7
    cost_per_1k_tokens: float = 0.002
    supports_functions: bool = True
    context_window: int = 8192
    
@dataclass
class AIConfig:
    """Complete AI configuration for the MASS Framework"""
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    azure_openai_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    
    # Default Models
    default_provider: AIProvider = AIProvider.OPENAI
    code_generation_model: str = "gpt-4-turbo-preview"
    code_review_model: str = "gpt-4"
    documentation_model: str = "gpt-3.5-turbo"
    chat_model: str = "gpt-4"
    
    # Model Configurations
    models: Dict[str, ModelConfig] = field(default_factory=dict)
    
    # Cost Management
    max_monthly_cost: float = 100.0
    cost_alert_threshold: float = 80.0
    
    # Performance Settings
    enable_caching: bool = True
    cache_ttl_hours: int = 24
    max_retries: int = 3
    timeout_seconds: int = 30
    
    # Safety Settings
    content_filter_enabled: bool = True
    max_tokens_per_request: int = 4000
    rate_limit_per_minute: int = 60

class AIConfigManager:
    """Manages AI configuration loading and validation"""
    
    def __init__(self, config_path: str = "config/ai_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self._setup_default_models()
    
    def _load_config(self) -> AIConfig:
        """Load configuration from file and environment variables"""
        config_data = {}
        
        # Load from YAML file if exists
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config_data = yaml.safe_load(f) or {}
        
        # Override with environment variables
        env_overrides = {
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
            'azure_openai_key': os.getenv('AZURE_OPENAI_KEY'),
            'azure_openai_endpoint': os.getenv('AZURE_OPENAI_ENDPOINT'),
        }
        
        # Filter out None values and update config
        config_data.update({k: v for k, v in env_overrides.items() if v is not None})
        
        return AIConfig(**config_data)
    
    def _setup_default_models(self):
        """Setup default model configurations"""
        default_models = {
            # OpenAI Models
            "gpt-4": ModelConfig(
                name="gpt-4",
                provider=AIProvider.OPENAI,
                max_tokens=8192,
                temperature=0.7,
                cost_per_1k_tokens=0.03,
                context_window=8192,
                supports_functions=True
            ),
            "gpt-4-turbo-preview": ModelConfig(
                name="gpt-4-turbo-preview", 
                provider=AIProvider.OPENAI,
                max_tokens=4096,
                temperature=0.7,
                cost_per_1k_tokens=0.01,
                context_window=128000,
                supports_functions=True
            ),
            "gpt-3.5-turbo": ModelConfig(
                name="gpt-3.5-turbo",
                provider=AIProvider.OPENAI,
                max_tokens=4096,
                temperature=0.7,
                cost_per_1k_tokens=0.0015,
                context_window=16384,
                supports_functions=True
            ),
            # Anthropic Models
            "claude-3-sonnet-20240229": ModelConfig(
                name="claude-3-sonnet-20240229",
                provider=AIProvider.ANTHROPIC,
                max_tokens=4096,
                temperature=0.7,
                cost_per_1k_tokens=0.003,
                context_window=200000,
                supports_functions=True
            ),
            "claude-3-haiku-20240307": ModelConfig(
                name="claude-3-haiku-20240307",
                provider=AIProvider.ANTHROPIC,
                max_tokens=4096,
                temperature=0.7,
                cost_per_1k_tokens=0.00025,
                context_window=200000,
                supports_functions=True
            ),
        }
        
        # Add default models that aren't already configured
        for model_name, model_config in default_models.items():
            if model_name not in self.config.models:
                self.config.models[model_name] = model_config
    
    def get_model_config(self, model_name: str) -> Optional[ModelConfig]:
        """Get configuration for a specific model"""
        return self.config.models.get(model_name)
    
    def get_provider_models(self, provider: AIProvider) -> List[ModelConfig]:
        """Get all models for a specific provider"""
        return [model for model in self.config.models.values() 
                if model.provider == provider]
    
    def get_available_providers(self) -> List[AIProvider]:
        """Get list of available providers based on configured API keys"""
        providers = []
        
        if self.config.openai_api_key:
            providers.append(AIProvider.OPENAI)
        if self.config.anthropic_api_key:
            providers.append(AIProvider.ANTHROPIC)
        if self.config.azure_openai_key and self.config.azure_openai_endpoint:
            providers.append(AIProvider.AZURE_OPENAI)
        
        # Always include local ollama as fallback
        providers.append(AIProvider.LOCAL_OLLAMA)
        
        return providers
    
    def save_config(self):
        """Save current configuration to file"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Convert to dict for YAML serialization
        config_dict = {
            'default_provider': self.config.default_provider.value,
            'code_generation_model': self.config.code_generation_model,
            'code_review_model': self.config.code_review_model,
            'documentation_model': self.config.documentation_model,
            'chat_model': self.config.chat_model,
            'max_monthly_cost': self.config.max_monthly_cost,
            'cost_alert_threshold': self.config.cost_alert_threshold,
            'enable_caching': self.config.enable_caching,
            'cache_ttl_hours': self.config.cache_ttl_hours,
            'max_retries': self.config.max_retries,
            'timeout_seconds': self.config.timeout_seconds,
            'content_filter_enabled': self.config.content_filter_enabled,
            'max_tokens_per_request': self.config.max_tokens_per_request,
            'rate_limit_per_minute': self.config.rate_limit_per_minute,
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False)
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return any issues"""
        issues = []
        
        # Check if at least one provider is configured
        if not self.get_available_providers():
            issues.append("No AI providers configured. Please set API keys.")
        
        # Check if default models exist
        if self.config.code_generation_model not in self.config.models:
            issues.append(f"Code generation model '{self.config.code_generation_model}' not found")
        
        if self.config.code_review_model not in self.config.models:
            issues.append(f"Code review model '{self.config.code_review_model}' not found")
        
        if self.config.documentation_model not in self.config.models:
            issues.append(f"Documentation model '{self.config.documentation_model}' not found")
        
        if self.config.chat_model not in self.config.models:
            issues.append(f"Chat model '{self.config.chat_model}' not found")
        
        return issues

# Global configuration instance
ai_config_manager = AIConfigManager()
