"""
Universal Adapter - Core Integration Engine

This is the main adapter that can integrate with ANY existing system and make it exponentially
smarter using real-world data intelligence. This is the "jQuery of AI" for system integration.

Key Features:
- Auto-detect system architecture and protocols
- Establish secure connections to any system type
- Map data schemas and business processes
- Identify optimal integration points
- Deploy appropriate intelligence agents
- Monitor system performance and health
"""

import asyncio
import aiohttp
import logging
import json
from typing import Dict, Any, List, Optional, Union, Type
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
import inspect

from ..core.config_manager import MassConfig
from ..enterprise_trust.trusted_ai_framework import TrustedAIFramework


class SystemType(Enum):
    """Supported system types for integration"""
    WEB_APPLICATION = "web_application"
    DATABASE_SYSTEM = "database_system"
    API_SERVICE = "api_service"
    MESSAGE_QUEUE = "message_queue"
    FILE_SYSTEM = "file_system"
    REALTIME_STREAM = "realtime_stream"
    WEBHOOK_SYSTEM = "webhook_system"
    CUSTOM_SYSTEM = "custom_system"


class IntegrationCapability(Enum):
    """Integration capabilities that can be detected/enabled"""
    READ_DATA = "read_data"
    WRITE_DATA = "write_data"
    STREAM_DATA = "stream_data"
    EXECUTE_OPERATIONS = "execute_operations"
    MONITOR_EVENTS = "monitor_events"
    SEND_NOTIFICATIONS = "send_notifications"
    BATCH_PROCESSING = "batch_processing"
    REAL_TIME_UPDATES = "real_time_updates"


@dataclass
class SystemAnalysis:
    """Comprehensive analysis of a target system"""
    system_type: SystemType
    capabilities: List[IntegrationCapability]
    data_schemas: Dict[str, Any]
    api_endpoints: List[str]
    integration_points: List[str]
    enhancement_opportunities: List[str]
    recommended_intelligence: List[str]
    security_requirements: Dict[str, Any]
    performance_characteristics: Dict[str, Any]
    compliance_requirements: List[str]


@dataclass 
class IntegrationResult:
    """Result of a successful integration"""
    integration_id: str
    system_analysis: SystemAnalysis
    deployed_adapters: Dict[str, Any]
    active_connections: Dict[str, Any]
    intelligence_agents: List[str]
    monitoring_setup: Dict[str, Any]
    enhancement_opportunities: List[str]
    performance_baseline: Dict[str, Any]


class SystemAnalyzer:
    """Analyzes target systems to determine optimal integration approach"""
    
    async def analyze_system(self, system_config: Dict[str, Any]) -> SystemAnalysis:
        """Comprehensively analyze a target system"""
        system_type = await self._detect_system_type(system_config)
        capabilities = await self._detect_capabilities(system_config, system_type)
        data_schemas = await self._analyze_data_schemas(system_config, system_type)
        api_endpoints = await self._discover_api_endpoints(system_config, system_type)
        integration_points = await self._identify_integration_points(system_config, capabilities)
        enhancement_opportunities = await self._identify_enhancements(system_config, capabilities)
        recommended_intelligence = await self._recommend_intelligence(system_config, capabilities)
        security_requirements = await self._analyze_security_requirements(system_config)
        performance_characteristics = await self._analyze_performance(system_config)
        compliance_requirements = await self._analyze_compliance_needs(system_config)
        
        return SystemAnalysis(
            system_type=system_type,
            capabilities=capabilities,
            data_schemas=data_schemas,
            api_endpoints=api_endpoints,
            integration_points=integration_points,
            enhancement_opportunities=enhancement_opportunities,
            recommended_intelligence=recommended_intelligence,
            security_requirements=security_requirements,
            performance_characteristics=performance_characteristics,
            compliance_requirements=compliance_requirements
        )
    
    async def _detect_system_type(self, system_config: Dict[str, Any]) -> SystemType:
        """Auto-detect the type of system we're integrating with"""
        # Check for database indicators
        if any(key in system_config for key in ['database_url', 'connection_string', 'db_host']):
            return SystemType.DATABASE_SYSTEM
        
        # Check for API indicators
        if any(key in system_config for key in ['api_url', 'base_url', 'endpoint']):
            return SystemType.API_SERVICE
        
        # Check for message queue indicators
        if any(key in system_config for key in ['kafka_brokers', 'rabbitmq_url', 'sqs_queue']):
            return SystemType.MESSAGE_QUEUE
        
        # Check for WebSocket indicators
        if any(key in system_config for key in ['websocket_url', 'ws_endpoint']):
            return SystemType.REALTIME_STREAM
        
        # Check for file system indicators
        if any(key in system_config for key in ['file_path', 'directory', 'bucket_name']):
            return SystemType.FILE_SYSTEM
        
        # Check for webhook indicators
        if any(key in system_config for key in ['webhook_url', 'callback_url']):
            return SystemType.WEBHOOK_SYSTEM
        
        # Default to web application
        return SystemType.WEB_APPLICATION
    
    async def _detect_capabilities(self, system_config: Dict[str, Any], system_type: SystemType) -> List[IntegrationCapability]:
        """Detect what capabilities the system supports"""
        capabilities = []
        
        # Basic capabilities based on system type
        if system_type == SystemType.DATABASE_SYSTEM:
            capabilities.extend([
                IntegrationCapability.READ_DATA,
                IntegrationCapability.WRITE_DATA,
                IntegrationCapability.BATCH_PROCESSING
            ])
        elif system_type == SystemType.API_SERVICE:
            capabilities.extend([
                IntegrationCapability.READ_DATA,
                IntegrationCapability.WRITE_DATA,
                IntegrationCapability.EXECUTE_OPERATIONS
            ])
        elif system_type == SystemType.REALTIME_STREAM:
            capabilities.extend([
                IntegrationCapability.STREAM_DATA,
                IntegrationCapability.REAL_TIME_UPDATES,
                IntegrationCapability.MONITOR_EVENTS
            ])
        elif system_type == SystemType.MESSAGE_QUEUE:
            capabilities.extend([
                IntegrationCapability.SEND_NOTIFICATIONS,
                IntegrationCapability.BATCH_PROCESSING,
                IntegrationCapability.MONITOR_EVENTS
            ])
        
        # Test actual capabilities if endpoints are available
        if 'api_url' in system_config or 'base_url' in system_config:
            tested_capabilities = await self._test_api_capabilities(system_config)
            capabilities.extend(tested_capabilities)
        
        return list(set(capabilities))  # Remove duplicates
    
    async def _test_api_capabilities(self, system_config: Dict[str, Any]) -> List[IntegrationCapability]:
        """Test API endpoints to determine actual capabilities"""
        capabilities = []
        base_url = system_config.get('api_url') or system_config.get('base_url')
        
        if not base_url:
            return capabilities
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test GET capability
                try:
                    async with session.get(base_url, timeout=5) as response:
                        if response.status < 500:
                            capabilities.append(IntegrationCapability.READ_DATA)
                except:
                    pass
                
                # Test POST capability  
                try:
                    async with session.post(base_url, json={}, timeout=5) as response:
                        if response.status < 500:
                            capabilities.append(IntegrationCapability.WRITE_DATA)
                except:
                    pass
        except:
            pass
        
        return capabilities
    
    async def _analyze_data_schemas(self, system_config: Dict[str, Any], system_type: SystemType) -> Dict[str, Any]:
        """Analyze and map data schemas"""
        schemas = {}
        
        if system_type == SystemType.API_SERVICE:
            # Try to discover OpenAPI/Swagger schemas
            schemas = await self._discover_api_schemas(system_config)
        elif system_type == SystemType.DATABASE_SYSTEM:
            # Try to introspect database schemas
            schemas = await self._discover_database_schemas(system_config)
        
        return schemas
    
    async def _discover_api_schemas(self, system_config: Dict[str, Any]) -> Dict[str, Any]:
        """Discover API schemas from OpenAPI/Swagger endpoints"""
        schemas = {}
        base_url = system_config.get('api_url') or system_config.get('base_url')
        
        if not base_url:
            return schemas
        
        # Common schema discovery endpoints
        schema_endpoints = [
            '/openapi.json',
            '/swagger.json',
            '/api-docs',
            '/docs/swagger.json',
            '/api/v1/openapi.json'
        ]
        
        async with aiohttp.ClientSession() as session:
            for endpoint in schema_endpoints:
                try:
                    url = f"{base_url.rstrip('/')}{endpoint}"
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            schema_data = await response.json()
                            schemas['openapi'] = schema_data
                            break
                except:
                    continue
        
        return schemas
    
    async def _discover_database_schemas(self, system_config: Dict[str, Any]) -> Dict[str, Any]:
        """Discover database schemas (placeholder for database introspection)"""
        # This would implement actual database schema discovery
        # For now, return empty dict
        return {}
    
    async def _discover_api_endpoints(self, system_config: Dict[str, Any], system_type: SystemType) -> List[str]:
        """Discover available API endpoints"""
        endpoints = []
        
        if system_type not in [SystemType.API_SERVICE, SystemType.WEB_APPLICATION]:
            return endpoints
        
        base_url = system_config.get('api_url') or system_config.get('base_url')
        if not base_url:
            return endpoints
        
        # Common API discovery paths
        discovery_paths = [
            '/api/v1/',
            '/api/v2/',
            '/api/',
            '/v1/',
            '/v2/',
            '/'
        ]
        
        async with aiohttp.ClientSession() as session:
            for path in discovery_paths:
                try:
                    url = f"{base_url.rstrip('/')}{path}"
                    async with session.get(url, timeout=5) as response:
                        if response.status == 200:
                            endpoints.append(url)
                except:
                    continue
        
        return endpoints
    
    async def _identify_integration_points(self, system_config: Dict[str, Any], capabilities: List[IntegrationCapability]) -> List[str]:
        """Identify optimal integration points"""
        integration_points = []
        
        if IntegrationCapability.READ_DATA in capabilities:
            integration_points.append("data_extraction")
        if IntegrationCapability.WRITE_DATA in capabilities:
            integration_points.append("data_injection")
        if IntegrationCapability.EXECUTE_OPERATIONS in capabilities:
            integration_points.append("operation_enhancement")
        if IntegrationCapability.MONITOR_EVENTS in capabilities:
            integration_points.append("event_monitoring")
        if IntegrationCapability.STREAM_DATA in capabilities:
            integration_points.append("real_time_streaming")
        
        return integration_points
    
    async def _identify_enhancements(self, system_config: Dict[str, Any], capabilities: List[IntegrationCapability]) -> List[str]:
        """Identify enhancement opportunities"""
        enhancements = []
        
        # Always available enhancements
        enhancements.extend([
            "real_time_intelligence_injection",
            "predictive_analytics_enhancement",
            "anomaly_detection_monitoring",
            "performance_optimization",
            "cost_optimization",
            "security_enhancement"
        ])
        
        # Capability-specific enhancements
        if IntegrationCapability.READ_DATA in capabilities:
            enhancements.extend([
                "data_quality_improvement",
                "automated_data_validation",
                "intelligent_data_caching"
            ])
        
        if IntegrationCapability.WRITE_DATA in capabilities:
            enhancements.extend([
                "intelligent_data_transformation",
                "automated_data_enrichment",
                "smart_data_routing"
            ])
        
        if IntegrationCapability.EXECUTE_OPERATIONS in capabilities:
            enhancements.extend([
                "operation_outcome_prediction",
                "intelligent_operation_scheduling",
                "automated_error_recovery"
            ])
        
        return enhancements
    
    async def _recommend_intelligence(self, system_config: Dict[str, Any], capabilities: List[IntegrationCapability]) -> List[str]:
        """Recommend specific intelligence agents"""
        recommendations = []
        
        # Core intelligence always recommended
        recommendations.extend([
            "data_analyzer_agent",
            "pattern_detector_agent",
            "anomaly_detector_agent"
        ])
        
        # Capability-specific intelligence
        if IntegrationCapability.READ_DATA in capabilities:
            recommendations.extend([
                "data_quality_agent",
                "trend_analyzer_agent"
            ])
        
        if IntegrationCapability.EXECUTE_OPERATIONS in capabilities:
            recommendations.extend([
                "predictive_agent",
                "optimization_agent",
                "automation_agent"
            ])
        
        if IntegrationCapability.MONITOR_EVENTS in capabilities:
            recommendations.extend([
                "event_correlation_agent",
                "alert_intelligence_agent"
            ])
        
        return recommendations
    
    async def _analyze_security_requirements(self, system_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze security requirements for the integration"""
        security_reqs = {
            "authentication_required": bool(system_config.get('api_key') or system_config.get('auth_token')),
            "encryption_required": bool(system_config.get('use_tls', True)),
            "data_classification": system_config.get('data_classification', 'internal'),
            "compliance_frameworks": system_config.get('compliance_frameworks', []),
            "access_controls": system_config.get('access_controls', {})
        }
        return security_reqs
    
    async def _analyze_performance(self, system_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance characteristics"""
        performance = {
            "expected_latency_ms": system_config.get('expected_latency_ms', 1000),
            "expected_throughput_rps": system_config.get('expected_throughput_rps', 100),
            "availability_requirement": system_config.get('availability_requirement', 0.999),
            "data_volume_gb_per_day": system_config.get('data_volume_gb_per_day', 1.0)
        }
        return performance
    
    async def _analyze_compliance_needs(self, system_config: Dict[str, Any]) -> List[str]:
        """Analyze compliance requirements"""
        compliance = []
        
        # Check for common compliance indicators
        if system_config.get('gdpr_required', False):
            compliance.append('GDPR')
        if system_config.get('sox_required', False):
            compliance.append('SOX')
        if system_config.get('hipaa_required', False):
            compliance.append('HIPAA')
        if system_config.get('pci_required', False):
            compliance.append('PCI-DSS')
        
        # Add any explicitly specified compliance frameworks
        compliance.extend(system_config.get('compliance_frameworks', []))
        
        return list(set(compliance))


class IntegrationPlanner:
    """Plans optimal integration approach based on system analysis"""
    
    async def create_plan(self, system_analysis: SystemAnalysis, schema_mapping: Dict[str, Any], capabilities: List[IntegrationCapability]) -> Dict[str, Any]:
        """Create comprehensive integration plan"""
        plan = {
            "integration_strategy": await self._determine_strategy(system_analysis, capabilities),
            "adapter_configuration": await self._plan_adapter_configuration(system_analysis),
            "intelligence_deployment": await self._plan_intelligence_deployment(system_analysis),
            "monitoring_setup": await self._plan_monitoring_setup(system_analysis),
            "security_measures": await self._plan_security_measures(system_analysis),
            "performance_optimization": await self._plan_performance_optimization(system_analysis),
            "rollback_strategy": await self._plan_rollback_strategy(system_analysis)
        }
        return plan
    
    async def _determine_strategy(self, system_analysis: SystemAnalysis, capabilities: List[IntegrationCapability]) -> str:
        """Determine the best integration strategy"""
        if IntegrationCapability.REAL_TIME_UPDATES in capabilities:
            return "real_time_streaming"
        elif IntegrationCapability.BATCH_PROCESSING in capabilities:
            return "batch_processing"
        elif IntegrationCapability.READ_DATA in capabilities and IntegrationCapability.WRITE_DATA in capabilities:
            return "bidirectional_sync"
        elif IntegrationCapability.READ_DATA in capabilities:
            return "read_only_enhancement"
        else:
            return "monitoring_only"
    
    async def _plan_adapter_configuration(self, system_analysis: SystemAnalysis) -> Dict[str, Any]:
        """Plan adapter configuration"""
        config = {
            "primary_adapter": system_analysis.system_type.value,
            "fallback_adapters": [],
            "connection_pooling": True,
            "retry_strategy": "exponential_backoff",
            "circuit_breaker": True,
            "rate_limiting": True
        }
        return config
    
    async def _plan_intelligence_deployment(self, system_analysis: SystemAnalysis) -> Dict[str, Any]:
        """Plan intelligence agent deployment"""
        deployment = {
            "agents_to_deploy": system_analysis.recommended_intelligence,
            "deployment_order": "parallel",
            "resource_allocation": "auto",
            "scaling_strategy": "adaptive"
        }
        return deployment
    
    async def _plan_monitoring_setup(self, system_analysis: SystemAnalysis) -> Dict[str, Any]:
        """Plan monitoring configuration"""
        monitoring = {
            "metrics_collection": True,
            "alerting_enabled": True,
            "log_aggregation": True,
            "health_checks": True,
            "performance_tracking": True,
            "compliance_monitoring": len(system_analysis.compliance_requirements) > 0
        }
        return monitoring
    
    async def _plan_security_measures(self, system_analysis: SystemAnalysis) -> Dict[str, Any]:
        """Plan security implementation"""
        security = {
            "encryption_in_transit": True,
            "encryption_at_rest": system_analysis.security_requirements.get('data_classification') in ['confidential', 'restricted'],
            "access_control": "rbac",
            "audit_logging": True,
            "vulnerability_scanning": True,
            "penetration_testing": system_analysis.security_requirements.get('data_classification') == 'restricted'
        }
        return security
    
    async def _plan_performance_optimization(self, system_analysis: SystemAnalysis) -> Dict[str, Any]:
        """Plan performance optimization"""
        optimization = {
            "caching_strategy": "intelligent",
            "connection_pooling": True,
            "query_optimization": True,
            "resource_scaling": "auto",
            "latency_optimization": True
        }
        return optimization
    
    async def _plan_rollback_strategy(self, system_analysis: SystemAnalysis) -> Dict[str, Any]:
        """Plan rollback strategy"""
        rollback = {
            "backup_strategy": "incremental",
            "rollback_triggers": ["error_rate_threshold", "performance_degradation"],
            "rollback_time_limit": "5_minutes",
            "data_consistency_checks": True
        }
        return rollback


class UniversalAdapter:
    """Stub for UniversalAdapter. Implement universal adapter logic here."""
    def __init__(self, *args, **kwargs):
        pass
