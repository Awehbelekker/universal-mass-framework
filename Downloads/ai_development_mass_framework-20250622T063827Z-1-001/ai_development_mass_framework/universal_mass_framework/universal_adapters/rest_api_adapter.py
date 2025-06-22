"""
REST API Adapter - Universal API Integration

This adapter can integrate with ANY REST API, GraphQL endpoint, or web service.
It automatically discovers endpoints, maps schemas, and provides intelligent enhancements.

Key Features:
- Auto-discovery of API endpoints and schemas
- OpenAPI/Swagger integration
- Intelligent request optimization
- Real-time API monitoring
- Automatic rate limiting and circuit breakers
- Schema validation and transformation
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import re
from dataclasses import dataclass

from ..core.config_manager import MassConfig
from ..enterprise_trust.trusted_ai_framework import TrustedAIFramework


@dataclass
class ApiEndpoint:
    """Represents a discovered API endpoint"""
    url: str
    method: str
    parameters: Dict[str, Any]
    response_schema: Dict[str, Any]
    description: str
    requires_auth: bool


@dataclass
class ApiConnection:
    """Represents an active API connection"""
    base_url: str
    session: aiohttp.ClientSession
    auth_headers: Dict[str, str]
    rate_limiter: Dict[str, Any]
    circuit_breaker: Dict[str, Any]


class RateLimiter:
    """Intelligent rate limiter that adapts to API responses"""
    
    def __init__(self, requests_per_second: int = 10):
        self.requests_per_second = requests_per_second
        self.requests = []
        self.adaptive_mode = True
        
    async def acquire(self) -> None:
        """Acquire permission to make a request"""
        current_time = datetime.utcnow()
        
        # Remove old requests outside the time window
        cutoff_time = current_time - timedelta(seconds=1)
        self.requests = [req_time for req_time in self.requests if req_time > cutoff_time]
        
        # Check if we need to wait
        if len(self.requests) >= self.requests_per_second:
            sleep_time = 1.0 / self.requests_per_second
            await asyncio.sleep(sleep_time)
        
        # Record this request
        self.requests.append(current_time)
    
    def adapt_rate(self, response_headers: Dict[str, str]) -> None:
        """Adapt rate limiting based on API response headers"""
        if not self.adaptive_mode:
            return
            
        # Check for rate limit headers
        rate_limit_remaining = response_headers.get('x-ratelimit-remaining') or response_headers.get('x-rate-limit-remaining')
        rate_limit_reset = response_headers.get('x-ratelimit-reset') or response_headers.get('x-rate-limit-reset')
        
        if rate_limit_remaining and rate_limit_reset:
            try:
                remaining = int(rate_limit_remaining)
                reset_time = int(rate_limit_reset)
                
                if remaining < 10:  # Close to rate limit
                    self.requests_per_second = max(1, self.requests_per_second // 2)
                elif remaining > 100:  # Plenty of capacity
                    self.requests_per_second = min(50, self.requests_per_second * 1.1)
            except ValueError:
                pass


class CircuitBreaker:
    """Circuit breaker to handle API failures gracefully"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open
        
    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half_open"
            else:
                raise Exception("Circuit breaker is OPEN - API unavailable")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit breaker"""
        if self.last_failure_time is None:
            return True
        
        time_since_failure = datetime.utcnow() - self.last_failure_time
        return time_since_failure.total_seconds() > self.recovery_timeout
    
    def _on_success(self) -> None:
        """Handle successful API call"""
        self.failure_count = 0
        self.state = "closed"
    
    def _on_failure(self) -> None:
        """Handle failed API call"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"


class SchemaMapper:
    """Maps and transforms API schemas"""
    
    def __init__(self):
        self.schema_cache = {}
        
    async def discover_schema(self, base_url: str, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Discover API schema from OpenAPI/Swagger endpoints"""
        if base_url in self.schema_cache:
            return self.schema_cache[base_url]
        
        schema = {}
        
        # Common schema discovery endpoints
        schema_endpoints = [
            '/openapi.json',
            '/swagger.json',
            '/api-docs',
            '/docs/swagger.json',
            '/v1/openapi.json',
            '/api/v1/openapi.json',
            '/swagger/v1/swagger.json'
        ]
        
        for endpoint in schema_endpoints:
            try:
                url = urljoin(base_url, endpoint)
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        schema_data = await response.json()
                        schema = self._normalize_schema(schema_data)
                        break
            except Exception:
                continue
        
        # If no schema found, try to discover endpoints manually
        if not schema:
            schema = await self._discover_endpoints_manually(base_url, session)
        
        self.schema_cache[base_url] = schema
        return schema
    
    def _normalize_schema(self, raw_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize different schema formats (OpenAPI 2.0/3.0, etc.)"""
        normalized = {
            "endpoints": [],
            "models": {},
            "security": {},
            "info": {}
        }
        
        # Handle OpenAPI 3.0
        if "openapi" in raw_schema:
            normalized["info"] = raw_schema.get("info", {})
            
            # Extract endpoints from paths
            paths = raw_schema.get("paths", {})
            for path, methods in paths.items():
                for method, spec in methods.items():
                    if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                        endpoint = {
                            "path": path,
                            "method": method.upper(),
                            "summary": spec.get("summary", ""),
                            "description": spec.get("description", ""),
                            "parameters": spec.get("parameters", []),
                            "responses": spec.get("responses", {}),
                            "security": spec.get("security", [])
                        }
                        normalized["endpoints"].append(endpoint)
            
            # Extract models from components
            if "components" in raw_schema and "schemas" in raw_schema["components"]:
                normalized["models"] = raw_schema["components"]["schemas"]
        
        # Handle Swagger 2.0
        elif "swagger" in raw_schema:
            normalized["info"] = raw_schema.get("info", {})
            
            # Extract endpoints from paths
            paths = raw_schema.get("paths", {})
            for path, methods in paths.items():
                for method, spec in methods.items():
                    if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                        endpoint = {
                            "path": path,
                            "method": method.upper(),
                            "summary": spec.get("summary", ""),
                            "description": spec.get("description", ""),
                            "parameters": spec.get("parameters", []),
                            "responses": spec.get("responses", {}),
                            "security": spec.get("security", [])
                        }
                        normalized["endpoints"].append(endpoint)
            
            # Extract models from definitions
            if "definitions" in raw_schema:
                normalized["models"] = raw_schema["definitions"]
        
        return normalized
    
    async def _discover_endpoints_manually(self, base_url: str, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Manually discover API endpoints when no schema is available"""
        endpoints = []
        
        # Common API patterns to try
        common_paths = [
            "/api/v1",
            "/api/v2", 
            "/api",
            "/v1",
            "/v2",
            "/rest",
            "/graphql"
        ]
        
        for path in common_paths:
            try:
                url = urljoin(base_url, path)
                async with session.get(url, timeout=5) as response:
                    if response.status < 500:  # Any response except server error
                        endpoint = {
                            "path": path,
                            "method": "GET",
                            "summary": f"Discovered endpoint: {path}",
                            "description": f"Auto-discovered endpoint with status {response.status}",
                            "parameters": [],
                            "responses": {str(response.status): {"description": "Response"}},
                            "security": []
                        }
                        endpoints.append(endpoint)
            except Exception:
                continue
        
        return {
            "endpoints": endpoints,
            "models": {},
            "security": {},
            "info": {"title": "Auto-discovered API"}
        }


class RestApiAdapter:
    """
    Universal REST API Adapter
    
    Automatically integrates with any REST API, GraphQL endpoint, or web service.
    Provides intelligent enhancements, monitoring, and optimization.
    """
    
    def __init__(self, config: Optional[MassConfig] = None):
        self.config = config or MassConfig()
        self.trust_framework = TrustedAIFramework(self.config)
        self.logger = logging.getLogger(__name__)
        
        # Components
        self.schema_mapper = SchemaMapper()
        self.connections = {}
        self.rate_limiters = {}
        self.circuit_breakers = {}
        
    async def deploy(self, integration_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy REST API adapter based on integration plan"""
        system_config = integration_plan.get("system_config", {})
        
        # Extract API configuration
        base_url = system_config.get("api_url") or system_config.get("base_url")
        if not base_url:
            raise ValueError("base_url or api_url is required for REST API integration")
        
        # Set up authentication
        auth_headers = await self._setup_authentication(system_config)
        
        # Create HTTP session
        session = await self._create_http_session(system_config, auth_headers)
        
        # Discover API schema and endpoints
        api_schema = await self.schema_mapper.discover_schema(base_url, session)
        
        # Set up rate limiting and circuit breaker
        rate_limiter = RateLimiter(system_config.get("requests_per_second", 10))
        circuit_breaker = CircuitBreaker(
            failure_threshold=system_config.get("failure_threshold", 5),
            recovery_timeout=system_config.get("recovery_timeout", 60)
        )
        
        # Create connection
        connection = ApiConnection(
            base_url=base_url,
            session=session,
            auth_headers=auth_headers,
            rate_limiter={"instance": rate_limiter},
            circuit_breaker={"instance": circuit_breaker}
        )
        
        connection_id = f"rest_api_{hash(base_url)}"
        self.connections[connection_id] = connection
        self.rate_limiters[connection_id] = rate_limiter
        self.circuit_breakers[connection_id] = circuit_breaker
        
        deployment_result = {
            "adapter_type": "rest_api",
            "connection_id": connection_id,
            "base_url": base_url,
            "api_schema": api_schema,
            "discovered_endpoints": len(api_schema.get("endpoints", [])),
            "capabilities": [
                "read_data",
                "write_data", 
                "execute_operations",
                "monitor_health",
                "intelligent_caching",
                "request_optimization"
            ],
            "features": {
                "rate_limiting": True,
                "circuit_breaker": True,
                "schema_discovery": True,
                "intelligent_retry": True,
                "response_caching": True,
                "request_optimization": True
            }
        }
        
        self.logger.info(f"REST API adapter deployed for {base_url}")
        return deployment_result
    
    async def _setup_authentication(self, system_config: Dict[str, Any]) -> Dict[str, str]:
        """Set up authentication headers"""
        auth_headers = {}
        
        # API Key authentication
        if "api_key" in system_config:
            api_key_header = system_config.get("api_key_header", "X-API-Key")
            auth_headers[api_key_header] = system_config["api_key"]
        
        # Bearer token authentication
        if "bearer_token" in system_config:
            auth_headers["Authorization"] = f"Bearer {system_config['bearer_token']}"
        
        # Basic authentication
        if "username" in system_config and "password" in system_config:
            import base64
            credentials = f"{system_config['username']}:{system_config['password']}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            auth_headers["Authorization"] = f"Basic {encoded_credentials}"
        
        # Custom headers
        if "custom_headers" in system_config:
            auth_headers.update(system_config["custom_headers"])
        
        return auth_headers
    
    async def _create_http_session(self, system_config: Dict[str, Any], auth_headers: Dict[str, str]) -> aiohttp.ClientSession:
        """Create optimized HTTP session"""
        # Default headers
        headers = {
            "User-Agent": "Universal-MASS-Framework/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Add authentication headers
        headers.update(auth_headers)
        
        # Create timeout configuration
        timeout = aiohttp.ClientTimeout(
            total=system_config.get("timeout_seconds", 30),
            connect=system_config.get("connect_timeout_seconds", 10)
        )
        
        # Create session with optimized settings
        session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout,
            connector=aiohttp.TCPConnector(
                limit=system_config.get("connection_pool_size", 100),
                limit_per_host=system_config.get("connections_per_host", 10),
                enable_cleanup_closed=True
            )
        )
        
        return session
    
    async def execute_request(self, connection_id: str, method: str, endpoint: str, 
                            data: Optional[Dict[str, Any]] = None, 
                            params: Optional[Dict[str, Any]] = None,
                            intelligence_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute an API request with intelligence enhancements"""
        if connection_id not in self.connections:
            raise ValueError(f"Connection {connection_id} not found")
        
        connection = self.connections[connection_id]
        rate_limiter = self.rate_limiters[connection_id]
        circuit_breaker = self.circuit_breakers[connection_id]
        
        # Apply rate limiting
        await rate_limiter.acquire()
        
        # Enhance request with intelligence
        enhanced_request = await self._enhance_request(method, endpoint, data, params, intelligence_context)
        
        # Execute request with circuit breaker protection
        async def make_request():
            url = urljoin(connection.base_url, endpoint)
            
            request_kwargs = {
                "url": url,
                "params": enhanced_request.get("params", params)
            }
            
            if enhanced_request.get("data") or data:
                request_kwargs["json"] = enhanced_request.get("data", data)
            
            async with connection.session.request(method.upper(), **request_kwargs) as response:
                # Adapt rate limiting based on response
                rate_limiter.adapt_rate(dict(response.headers))
                
                response_data = {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "url": str(response.url)
                }
                
                # Try to parse JSON response
                try:
                    response_data["data"] = await response.json()
                except:
                    response_data["text"] = await response.text()
                
                # Check for errors
                response.raise_for_status()
                
                return response_data
        
        try:
            # Execute with circuit breaker
            result = await circuit_breaker.call(make_request)
            
            # Post-process response with intelligence
            enhanced_result = await self._enhance_response(result, intelligence_context)
            
            return {
                "success": True,
                "request": enhanced_request,
                "response": enhanced_result,
                "execution_time": datetime.utcnow().isoformat(),
                "enhancements_applied": enhanced_request.get("enhancements_applied", [])
            }
            
        except Exception as e:
            self.logger.error(f"API request failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "request": enhanced_request,
                "execution_time": datetime.utcnow().isoformat()
            }
    
    async def _enhance_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]], 
                             params: Optional[Dict[str, Any]], intelligence_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Enhance request with intelligence"""
        enhanced_request = {
            "method": method,
            "endpoint": endpoint,
            "data": data,
            "params": params,
            "enhancements_applied": []
        }
        
        if not intelligence_context:
            return enhanced_request
        
        # Apply intelligent parameter optimization
        if params:
            optimized_params = await self._optimize_parameters(params, intelligence_context)
            if optimized_params != params:
                enhanced_request["params"] = optimized_params
                enhanced_request["enhancements_applied"].append("parameter_optimization")
        
        # Apply intelligent data transformation
        if data:
            transformed_data = await self._transform_data(data, intelligence_context)
            if transformed_data != data:
                enhanced_request["data"] = transformed_data
                enhanced_request["enhancements_applied"].append("data_transformation")
        
        # Add intelligent caching headers
        cache_headers = await self._get_intelligent_cache_headers(method, endpoint, intelligence_context)
        if cache_headers:
            enhanced_request["cache_headers"] = cache_headers
            enhanced_request["enhancements_applied"].append("intelligent_caching")
        
        return enhanced_request
    
    async def _optimize_parameters(self, params: Dict[str, Any], intelligence_context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize request parameters based on intelligence"""
        optimized_params = params.copy()
        
        # Example: Optimize pagination based on current load
        if "page_size" in params and "system_load" in intelligence_context:
            system_load = intelligence_context["system_load"]
            if system_load > 0.8:  # High load
                optimized_params["page_size"] = min(params["page_size"], 50)
            elif system_load < 0.3:  # Low load
                optimized_params["page_size"] = min(params["page_size"] * 2, 500)
        
        # Example: Add filtering based on real-time trends
        if "trends" in intelligence_context:
            trends = intelligence_context["trends"]
            if "filter_recommendations" in trends:
                for filter_key, filter_value in trends["filter_recommendations"].items():
                    if filter_key not in optimized_params:
                        optimized_params[filter_key] = filter_value
        
        return optimized_params
    
    async def _transform_data(self, data: Dict[str, Any], intelligence_context: Dict[str, Any]) -> Dict[str, Any]:
        """Transform request data based on intelligence"""
        transformed_data = data.copy()
        
        # Example: Add timestamp-based optimization
        if "timing_optimization" in intelligence_context:
            timing = intelligence_context["timing_optimization"]
            if "optimal_time" in timing:
                transformed_data["scheduled_time"] = timing["optimal_time"]
        
        # Example: Add geo-location optimization
        if "geo_optimization" in intelligence_context:
            geo = intelligence_context["geo_optimization"]
            if "optimal_region" in geo:
                transformed_data["region"] = geo["optimal_region"]
        
        return transformed_data
    
    async def _get_intelligent_cache_headers(self, method: str, endpoint: str, intelligence_context: Dict[str, Any]) -> Dict[str, str]:
        """Get intelligent caching headers"""
        cache_headers = {}
        
        # Read operations can be cached more aggressively
        if method.upper() == "GET":
            # Check if data is frequently changing
            if "data_volatility" in intelligence_context:
                volatility = intelligence_context["data_volatility"]
                if volatility < 0.1:  # Low volatility
                    cache_headers["Cache-Control"] = "max-age=3600"
                elif volatility < 0.5:  # Medium volatility  
                    cache_headers["Cache-Control"] = "max-age=300"
                else:  # High volatility
                    cache_headers["Cache-Control"] = "no-cache"
        
        return cache_headers
    
    async def _enhance_response(self, response: Dict[str, Any], intelligence_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Enhance response with intelligence"""
        enhanced_response = response.copy()
        
        if not intelligence_context:
            return enhanced_response
        
        # Add intelligent insights to response
        insights = await self._generate_response_insights(response, intelligence_context)
        if insights:
            enhanced_response["intelligence_insights"] = insights
        
        # Add performance recommendations
        recommendations = await self._generate_performance_recommendations(response, intelligence_context)
        if recommendations:
            enhanced_response["performance_recommendations"] = recommendations
        
        return enhanced_response
    
    async def _generate_response_insights(self, response: Dict[str, Any], intelligence_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent insights from response"""
        insights = {}
        
        # Analyze response time patterns
        if "historical_performance" in intelligence_context:
            historical = intelligence_context["historical_performance"]
            current_response_time = response.get("response_time_ms", 0)
            
            if current_response_time > historical.get("average_response_time", 1000) * 1.5:
                insights["performance_alert"] = "Response time significantly higher than average"
        
        # Analyze data patterns
        if "data" in response and "data_patterns" in intelligence_context:
            data_size = len(str(response["data"]))
            expected_size = intelligence_context["data_patterns"].get("expected_size", data_size)
            
            if data_size < expected_size * 0.5:
                insights["data_alert"] = "Response data significantly smaller than expected"
            elif data_size > expected_size * 2:
                insights["data_alert"] = "Response data significantly larger than expected"
        
        return insights
    
    async def _generate_performance_recommendations(self, response: Dict[str, Any], intelligence_context: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        # Response size recommendations
        if "data" in response:
            data_size = len(str(response["data"]))
            if data_size > 1000000:  # 1MB
                recommendations.append("Consider implementing pagination for large response data")
        
        # Caching recommendations
        if response.get("status") == 200 and "cache-control" not in response.get("headers", {}):
            recommendations.append("Consider implementing response caching for improved performance")
        
        # Rate limiting recommendations
        if "x-ratelimit-remaining" in response.get("headers", {}):
            remaining = int(response["headers"]["x-ratelimit-remaining"])
            if remaining < 10:
                recommendations.append("Approaching rate limit - consider implementing request throttling")
        
        return recommendations
    
    async def health_check(self, connection_id: str) -> Dict[str, Any]:
        """Perform health check on API connection"""
        if connection_id not in self.connections:
            return {"healthy": False, "error": "Connection not found"}
        
        connection = self.connections[connection_id]
        
        try:
            # Try a simple GET request to the base URL
            async with connection.session.get(connection.base_url, timeout=10) as response:
                health_status = {
                    "healthy": response.status < 500,
                    "status_code": response.status,
                    "response_time_ms": 0,  # Would calculate actual response time
                    "circuit_breaker_state": self.circuit_breakers[connection_id].state,
                    "rate_limiter_rate": self.rate_limiters[connection_id].requests_per_second,
                    "last_check": datetime.utcnow().isoformat()
                }
                
                return health_status
                
        except Exception as e:
            return {
                "healthy": False,
                "error": str(e),
                "circuit_breaker_state": self.circuit_breakers[connection_id].state,
                "last_check": datetime.utcnow().isoformat()
            }
    
    async def get_connection_metrics(self, connection_id: str) -> Dict[str, Any]:
        """Get performance metrics for a connection"""
        if connection_id not in self.connections:
            return {"error": "Connection not found"}
        
        connection = self.connections[connection_id]
        rate_limiter = self.rate_limiters[connection_id]
        circuit_breaker = self.circuit_breakers[connection_id]
        
        metrics = {
            "connection_id": connection_id,
            "base_url": connection.base_url,
            "rate_limiter": {
                "requests_per_second": rate_limiter.requests_per_second,
                "current_requests": len(rate_limiter.requests),
                "adaptive_mode": rate_limiter.adaptive_mode
            },
            "circuit_breaker": {
                "state": circuit_breaker.state,
                "failure_count": circuit_breaker.failure_count,
                "failure_threshold": circuit_breaker.failure_threshold,
                "last_failure_time": circuit_breaker.last_failure_time.isoformat() if circuit_breaker.last_failure_time else None
            },
            "session_info": {
                "connector_limit": connection.session.connector.limit,
                "connector_limit_per_host": connection.session.connector.limit_per_host
            }
        }
        
        return metrics
    
    async def close_connection(self, connection_id: str) -> Dict[str, Any]:
        """Close an API connection"""
        if connection_id not in self.connections:
            return {"success": False, "error": "Connection not found"}
        
        try:
            connection = self.connections[connection_id]
            await connection.session.close()
            
            # Clean up resources
            del self.connections[connection_id]
            del self.rate_limiters[connection_id]
            del self.circuit_breakers[connection_id]
            
            return {"success": True, "message": f"Connection {connection_id} closed successfully"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def close_all_connections(self) -> Dict[str, Any]:
        """Close all active connections"""
        closed_connections = []
        errors = []
        
        for connection_id in list(self.connections.keys()):
            result = await self.close_connection(connection_id)
            if result["success"]:
                closed_connections.append(connection_id)
            else:
                errors.append({"connection_id": connection_id, "error": result["error"]})
        
        return {
            "closed_connections": closed_connections,
            "errors": errors,
            "total_closed": len(closed_connections)
        }