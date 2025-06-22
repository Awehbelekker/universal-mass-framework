"""
Universal Adapters - System Integration Engine

This module provides the core adapter framework for integrating with ANY existing system.
The Universal MASS Framework can connect to and enhance any system through these adapters.

Key Features:
- Auto-detect system architecture and protocols
- Establish secure connections to any system type
- Map data schemas and business processes
- Deploy appropriate intelligence agents
- Monitor system performance and health

Supported System Types:
- REST/GraphQL APIs
- SQL/NoSQL Databases
- Message Queues (Kafka, RabbitMQ, SQS)
- WebSocket/SSE Streams
- File Systems and Data Lakes
- Custom Protocols and Legacy Systems
"""

from .universal_adapter import (
    UniversalAdapter,
    SystemType,
    IntegrationCapability,
    SystemAnalysis,
    IntegrationResult
)

from .rest_api_adapter import RestApiAdapter
from .database_adapter import DatabaseAdapter
from .websocket_adapter import WebSocketAdapter
from .message_queue_adapter import MessageQueueAdapter
from .file_system_adapter import FileSystemAdapter
from .webhook_adapter import WebhookAdapter
from .custom_adapter_template import CustomAdapterTemplate

__all__ = [
    'UniversalAdapter',
    'SystemType',
    'IntegrationCapability', 
    'SystemAnalysis',
    'IntegrationResult',
    'RestApiAdapter',
    'DatabaseAdapter',
    'WebSocketAdapter',
    'MessageQueueAdapter',
    'FileSystemAdapter',
    'WebhookAdapter',
    'CustomAdapterTemplate'
]

# Version information
__version__ = "1.0.0"
__author__ = "Universal MASS Framework"
__description__ = "Universal System Integration Adapters"