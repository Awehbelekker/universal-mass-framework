"""
Multi-Provider LLM Service for MASS Framework
Provides unified interface for OpenAI, Anthropic, and local LLMs
"""

import asyncio
import json
import time
from typing import Dict, Any, List, Optional, AsyncIterator, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
import tiktoken
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from config.ai_config import ai_config_manager, AIProvider, ModelConfig
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AIMessage:
    """Standardized AI message format"""
    role: str  # "system", "user", "assistant"
    content: str
    metadata: Dict[str, Any] = None

@dataclass
class AIResponse:
    """Standardized AI response format"""
    content: str
    model: str
    provider: str
    tokens_used: int
    cost_estimate: float
    response_time: float
    metadata: Dict[str, Any] = None

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[AIMessage], 
        model: str,
        **kwargs
    ) -> AIResponse:
        """Generate a response from the LLM"""
        pass
    
    @abstractmethod
    async def generate_stream(
        self, 
        messages: List[AIMessage], 
        model: str,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate a streaming response from the LLM"""
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI API provider"""
    
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=ai_config_manager.config.openai_api_key
        )
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        try:
            return len(self.encoding.encode(text))
        except:
            # Fallback estimation
            return len(text.split()) * 1.3
    
    def _messages_to_openai_format(self, messages: List[AIMessage]) -> List[Dict[str, str]]:
        """Convert AIMessage format to OpenAI format"""
        return [{"role": msg.role, "content": msg.content} for msg in messages]
    
    async def generate_response(
        self, 
        messages: List[AIMessage], 
        model: str,
        **kwargs
    ) -> AIResponse:
        """Generate response using OpenAI API"""
        start_time = time.time()
        
        try:
            openai_messages = self._messages_to_openai_format(messages)
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=openai_messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 2000),
                **{k: v for k, v in kwargs.items() 
                   if k in ['top_p', 'frequency_penalty', 'presence_penalty', 'functions', 'function_call']}
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Calculate cost
            model_config = ai_config_manager.get_model_config(model)
            cost_estimate = (tokens_used / 1000) * (model_config.cost_per_1k_tokens if model_config else 0.002)
            
            response_time = time.time() - start_time
            
            return AIResponse(
                content=content,
                model=model,
                provider="openai",
                tokens_used=tokens_used,
                cost_estimate=cost_estimate,
                response_time=response_time,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "response_id": response.id
                }
            )
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    async def generate_stream(
        self, 
        messages: List[AIMessage], 
        model: str,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate streaming response using OpenAI API"""
        try:
            openai_messages = self._messages_to_openai_format(messages)
            
            stream = await self.client.chat.completions.create(
                model=model,
                messages=openai_messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 2000),
                stream=True,
                **{k: v for k, v in kwargs.items() 
                   if k in ['top_p', 'frequency_penalty', 'presence_penalty']}
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"OpenAI streaming error: {str(e)}")
            raise

class AnthropicProvider(LLMProvider):
    """Anthropic API provider"""
    
    def __init__(self):
        self.client = AsyncAnthropic(
            api_key=ai_config_manager.config.anthropic_api_key
        )
    
    def _count_tokens_estimate(self, text: str) -> int:
        """Estimate token count for Anthropic (rough approximation)"""
        return len(text.split()) * 1.3
    
    def _messages_to_anthropic_format(self, messages: List[AIMessage]) -> tuple:
        """Convert AIMessage format to Anthropic format"""
        system_message = ""
        conversation = []
        
        for msg in messages:
            if msg.role == "system":
                system_message += msg.content + "\n"
            else:
                conversation.append({"role": msg.role, "content": msg.content})
        
        return system_message.strip(), conversation
    
    async def generate_response(
        self, 
        messages: List[AIMessage], 
        model: str,
        **kwargs
    ) -> AIResponse:
        """Generate response using Anthropic API"""
        start_time = time.time()
        
        try:
            system_message, conversation = self._messages_to_anthropic_format(messages)
            
            request_params = {
                "model": model,
                "messages": conversation,
                "max_tokens": kwargs.get('max_tokens', 2000),
                "temperature": kwargs.get('temperature', 0.7),
            }
            
            if system_message:
                request_params["system"] = system_message
            
            response = await self.client.messages.create(**request_params)
            
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            
            # Calculate cost
            model_config = ai_config_manager.get_model_config(model)
            cost_estimate = (tokens_used / 1000) * (model_config.cost_per_1k_tokens if model_config else 0.003)
            
            response_time = time.time() - start_time
            
            return AIResponse(
                content=content,
                model=model,
                provider="anthropic",
                tokens_used=tokens_used,
                cost_estimate=cost_estimate,
                response_time=response_time,
                metadata={
                    "stop_reason": response.stop_reason,
                    "response_id": response.id
                }
            )
            
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise
    
    async def generate_stream(
        self, 
        messages: List[AIMessage], 
        model: str,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate streaming response using Anthropic API"""
        try:
            system_message, conversation = self._messages_to_anthropic_format(messages)
            
            request_params = {
                "model": model,
                "messages": conversation,
                "max_tokens": kwargs.get('max_tokens', 2000),
                "temperature": kwargs.get('temperature', 0.7),
                "stream": True,
            }
            
            if system_message:
                request_params["system"] = system_message
            
            async with self.client.messages.stream(**request_params) as stream:
                async for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            logger.error(f"Anthropic streaming error: {str(e)}")
            raise

class MockProvider(LLMProvider):
    """Mock provider for testing"""
    
    def __init__(self):
        self.call_count = 0
    
    async def generate_response(
        self, 
        messages: List[AIMessage], 
        model: str,
        **kwargs
    ) -> AIResponse:
        """Generate a mock response"""
        self.call_count += 1
        
        # Check if the request wants JSON (based on message content)
        user_content = ""
        for msg in messages:
            if msg.role == "user":
                user_content = msg.content.lower()
                break
          # Generate appropriate mock response based on request type
        if "json" in user_content and "recommend" in user_content and "agent" in user_content:
            content = """[
    {
        "agent_id": "code_generator",
        "confidence_score": 0.8,
        "reasoning": "Best for code generation tasks",
        "estimated_contribution": "Generate Python code based on requirements"
    },
    {
        "agent_id": "documentation_agent", 
        "confidence_score": 0.6,
        "reasoning": "Helpful for documentation",
        "estimated_contribution": "Create comprehensive documentation"
    },
    {
        "agent_id": "testing_agent",
        "confidence_score": 0.7,
        "reasoning": "Generate unit tests",
        "estimated_contribution": "Create test cases for generated code"
    }
]"""
        elif "json" in user_content and "task" in user_content and "analyze" in user_content:
            content = """{
    "category": "analysis",
    "complexity": "moderate",    "estimated_time_minutes": 30,    "required_agents": ["code_analyzer"],
    "optional_agents": ["documentation_agent"],
    "risk_level": "medium",
    "success_probability": 0.7,
    "reasoning": "Mock task analysis",
    "resource_requirements": {
        "compute_intensive": false,
        "requires_external_apis": false,
        "needs_human_review": true
    }
}"""
        elif "json" in user_content and "workflow" in user_content:
            content = """{
    "workflow": {
        "name": "Development Workflow",
        "description": "Mock workflow for development",
        "steps": [
            {
                "id": "step1",
                "name": "Analysis",
                "agent": "code_analyzer",
                "estimated_time": 10
            },
            {
                "id": "step2", 
                "name": "Implementation",
                "agent": "code_generator",
                "estimated_time": 20
            }
        ]
    }
}"""
        else:
            content = "This is a mock response for testing"
        
        return AIResponse(
            content=content,
            model=model,
            provider="mock",
            tokens_used=10,
            cost_estimate=0.001,
            response_time=0.1,
            metadata={"mock": True, "call_count": self.call_count}
        )
    
    async def generate_stream(
        self, 
        messages: List[AIMessage], 
        model: str,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate a mock streaming response"""
        mock_chunks = ["This ", "is ", "a ", "mock ", "streaming ", "response"]
        for chunk in mock_chunks:
            yield chunk

class LLMService:
    """Main LLM service that coordinates multiple providers"""
    
    def __init__(self):
        self.providers = {}
        self._initialize_providers()
        self.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "provider_usage": {}        }
    
    def _initialize_providers(self):
        """Initialize available providers based on configuration"""
        available_providers = ai_config_manager.get_available_providers()
        
        if AIProvider.OPENAI in available_providers:
            try:
                self.providers[AIProvider.OPENAI] = OpenAIProvider()
                logger.info("OpenAI provider initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI provider: {e}")
        
        if AIProvider.ANTHROPIC in available_providers:
            try:
                self.providers[AIProvider.ANTHROPIC] = AnthropicProvider()
                logger.info("Anthropic provider initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic provider: {e}")
        
        # If no providers are available (e.g., in test environment), use mock providers
        if not self.providers:
            logger.info("No real providers available, using mock providers for testing")
            self.providers[AIProvider.OPENAI] = MockProvider()
            self.providers[AIProvider.ANTHROPIC] = MockProvider()
    
    def _get_provider_for_model(self, model: str) -> LLMProvider:
        """Get the appropriate provider for a model"""
        model_config = ai_config_manager.get_model_config(model)
        if not model_config:
            raise ValueError(f"Model '{model}' not found in configuration")
        
        provider = self.providers.get(model_config.provider)
        if not provider:
            raise ValueError(f"Provider '{model_config.provider}' not available")
        
        return provider
    
    async def generate_response(
        self,
        messages: Union[List[AIMessage], List[Dict[str, str]], str],
        model: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        """Generate a response using the specified model"""
        
        # Convert input to standard format
        if isinstance(messages, str):
            messages = [AIMessage(role="user", content=messages)]
        elif isinstance(messages, list) and len(messages) > 0:
            if isinstance(messages[0], dict):
                messages = [AIMessage(role=msg["role"], content=msg["content"]) for msg in messages]
        
        # Use default model if not specified
        if not model:
            model = ai_config_manager.config.code_generation_model
        
        # Get provider and generate response
        provider = self._get_provider_for_model(model)
        response = await provider.generate_response(messages, model, **kwargs)
        
        # Update usage statistics
        self._update_usage_stats(response)
        
        return response
    
    async def generate_stream(
        self,
        messages: Union[List[AIMessage], List[Dict[str, str]], str],
        model: Optional[str] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate a streaming response using the specified model"""
        
        # Convert input to standard format
        if isinstance(messages, str):
            messages = [AIMessage(role="user", content=messages)]
        elif isinstance(messages, list) and len(messages) > 0:
            if isinstance(messages[0], dict):
                messages = [AIMessage(role=msg["role"], content=msg["content"]) for msg in messages]
        
        # Use default model if not specified
        if not model:
            model = ai_config_manager.config.chat_model
        
        # Get provider and generate streaming response
        provider = self._get_provider_for_model(model)
        async for chunk in provider.generate_stream(messages, model, **kwargs):
            yield chunk
    
    def _update_usage_stats(self, response: AIResponse):
        """Update usage statistics"""
        self.usage_stats["total_requests"] += 1
        self.usage_stats["total_tokens"] += response.tokens_used
        self.usage_stats["total_cost"] += response.cost_estimate
        
        if response.provider not in self.usage_stats["provider_usage"]:
            self.usage_stats["provider_usage"][response.provider] = {
                "requests": 0,
                "tokens": 0,
                "cost": 0.0
            }
        
        provider_stats = self.usage_stats["provider_usage"][response.provider]
        provider_stats["requests"] += 1
        provider_stats["tokens"] += response.tokens_used
        provider_stats["cost"] += response.cost_estimate
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return self.usage_stats.copy()
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return list(ai_config_manager.config.models.keys())
    
    def get_model_info(self, model: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model"""
        model_config = ai_config_manager.get_model_config(model)
        if not model_config:
            return None
        
        return {
            "name": model_config.name,
            "provider": model_config.provider.value,
            "max_tokens": model_config.max_tokens,
            "context_window": model_config.context_window,
            "cost_per_1k_tokens": model_config.cost_per_1k_tokens,
            "supports_functions": model_config.supports_functions
        }
    
    async def chat_completion(self, messages, model=None, **kwargs):
        """Compatibility method for tests and agent mocks. Calls generate_response and returns a simple object with 'content'."""
        response = await self.generate_response(messages, model=model, **kwargs)
        # Return a mock-like object with a 'content' attribute for test compatibility
        class Result:
            def __init__(self, content, usage=None):
                self.content = content
                self.usage = usage if usage is not None else getattr(response, 'usage', None)
        return Result(response.content if hasattr(response, 'content') else str(response), getattr(response, 'usage', None))

    async def _make_openai_request(self, *args, **kwargs):
        """Stub for OpenAI request, for test patching/mocking."""
        return None

# For backwards compatibility with tests that expect to patch OpenAI directly
try:
    from openai import OpenAI, AsyncOpenAI
    # Export these for tests that need to mock them
    __all__ = ['LLMService', 'AIMessage', 'AIResponse', 'OpenAI', 'AsyncOpenAI']
except ImportError:
    __all__ = ['LLMService', 'AIMessage', 'AIResponse']

# Global LLM service instance
llm_service = LLMService()
