"""
WebSocket Adapter - Universal Real-time Stream Integration

This adapter can integrate with ANY real-time streaming system including WebSockets,
Server-Sent Events (SSE), and other streaming protocols. It provides intelligent
stream processing, real-time analytics, and automatic reconnection.

Key Features:
- Universal WebSocket and SSE support
- Automatic reconnection with exponential backoff
- Real-time stream analytics and pattern detection
- Intelligent message filtering and routing
- Stream health monitoring and alerting
- Message queuing during disconnections
"""

import asyncio
import websockets
import aiohttp
import json
import logging
from typing import Dict, Any, List, Optional, Callable, AsyncGenerator
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import queue
import threading
from urllib.parse import urlparse

from ..core.config_manager import MassConfig
from ..enterprise_trust.trusted_ai_framework import TrustedAIFramework


class StreamType(Enum):
    """Types of streaming connections"""
    WEBSOCKET = "websocket"
    SERVER_SENT_EVENTS = "server_sent_events"
    SOCKET_IO = "socket_io"
    CUSTOM_STREAM = "custom_stream"


class ConnectionState(Enum):
    """WebSocket connection states"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    ERROR = "error"


@dataclass
class StreamMessage:
    """Represents a message from a stream"""
    timestamp: datetime
    message_type: str
    data: Dict[str, Any]
    source: str
    processed: bool = False
    metadata: Dict[str, Any] = None


@dataclass
class StreamConnection:
    """Represents an active streaming connection"""
    connection_id: str
    stream_type: StreamType
    url: str
    connection: Any
    state: ConnectionState
    message_handlers: List[Callable]
    message_queue: queue.Queue
    statistics: Dict[str, Any]


class ReconnectionManager:
    """Manages intelligent reconnection with exponential backoff"""
    
    def __init__(self, max_retries: int = 10, base_delay: float = 1.0, max_delay: float = 300.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.retry_count = 0
        self.last_attempt = None
        
    def should_retry(self) -> bool:
        """Check if we should attempt reconnection"""
        return self.retry_count < self.max_retries
    
    def get_delay(self) -> float:
        """Get delay before next reconnection attempt"""
        if self.retry_count == 0:
            return 0
        
        delay = self.base_delay * (2 ** (self.retry_count - 1))
        return min(delay, self.max_delay)
    
    def record_attempt(self) -> None:
        """Record a reconnection attempt"""
        self.retry_count += 1
        self.last_attempt = datetime.utcnow()
    
    def reset(self) -> None:
        """Reset retry counter after successful connection"""
        self.retry_count = 0
        self.last_attempt = None


class StreamAnalyzer:
    """Analyzes streaming data for patterns and insights"""
    
    def __init__(self):
        self.message_history = []
        self.pattern_cache = {}
        self.analytics_window = timedelta(minutes=5)
        
    async def analyze_message(self, message: StreamMessage, 
                            intelligence_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze a stream message for patterns and insights"""
        analysis = {
            "message_id": f"{message.source}_{message.timestamp.isoformat()}",
            "timestamp": message.timestamp.isoformat(),
            "patterns_detected": [],
            "anomalies": [],
            "insights": [],
            "recommendations": []
        }
        
        # Add to history
        self.message_history.append(message)
        
        # Clean old messages
        cutoff_time = datetime.utcnow() - self.analytics_window
        self.message_history = [msg for msg in self.message_history if msg.timestamp > cutoff_time]
        
        # Detect patterns
        patterns = await self._detect_patterns(message)
        analysis["patterns_detected"] = patterns
        
        # Detect anomalies
        anomalies = await self._detect_anomalies(message)
        analysis["anomalies"] = anomalies
        
        # Generate insights
        insights = await self._generate_insights(message, intelligence_context)
        analysis["insights"] = insights
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(message, patterns, anomalies)
        analysis["recommendations"] = recommendations
        
        return analysis
    
    async def _detect_patterns(self, message: StreamMessage) -> List[Dict[str, Any]]:
        """Detect patterns in stream data"""
        patterns = []
        
        # Message frequency pattern
        recent_messages = [msg for msg in self.message_history 
                          if msg.timestamp > datetime.utcnow() - timedelta(minutes=1)]
        message_rate = len(recent_messages)
        
        if message_rate > 60:  # More than 1 per second
            patterns.append({
                "type": "high_frequency",
                "description": f"High message frequency: {message_rate} messages/minute",
                "confidence": 0.9
            })
        elif message_rate < 5:  # Less than 1 per 12 seconds
            patterns.append({
                "type": "low_frequency", 
                "description": f"Low message frequency: {message_rate} messages/minute",
                "confidence": 0.8
            })
        
        # Data structure pattern
        if hasattr(message.data, 'keys'):
            common_keys = set(message.data.keys())
            for msg in self.message_history[-10:]:  # Check last 10 messages
                if hasattr(msg.data, 'keys'):
                    common_keys &= set(msg.data.keys())
            
            if len(common_keys) > 0:
                patterns.append({
                    "type": "consistent_schema",
                    "description": f"Consistent data structure with keys: {list(common_keys)}",
                    "confidence": 0.85
                })
        
        # Value pattern detection
        if isinstance(message.data, dict):
            for key, value in message.data.items():
                if isinstance(value, (int, float)):
                    historical_values = [msg.data.get(key) for msg in self.message_history[-20:] 
                                       if isinstance(msg.data, dict) and key in msg.data 
                                       and isinstance(msg.data[key], (int, float))]
                    
                    if len(historical_values) > 5:
                        avg_value = sum(historical_values) / len(historical_values)
                        if abs(value - avg_value) > avg_value * 0.5:  # 50% deviation
                            patterns.append({
                                "type": "value_deviation",
                                "description": f"Significant deviation in {key}: {value} vs avg {avg_value:.2f}",
                                "confidence": 0.7
                            })
        
        return patterns
    
    async def _detect_anomalies(self, message: StreamMessage) -> List[Dict[str, Any]]:
        """Detect anomalies in stream data"""
        anomalies = []
        
        # Message timing anomaly
        if len(self.message_history) > 1:
            time_diff = (message.timestamp - self.message_history[-2].timestamp).total_seconds()
            
            # Calculate average time between messages
            if len(self.message_history) > 10:
                time_diffs = []
                for i in range(len(self.message_history) - 10, len(self.message_history) - 1):
                    diff = (self.message_history[i+1].timestamp - self.message_history[i].timestamp).total_seconds()
                    time_diffs.append(diff)
                
                avg_time_diff = sum(time_diffs) / len(time_diffs)
                
                if time_diff > avg_time_diff * 3:  # 3x longer than average
                    anomalies.append({
                        "type": "timing_anomaly",
                        "description": f"Unusually long gap between messages: {time_diff:.2f}s vs avg {avg_time_diff:.2f}s",
                        "severity": "medium"
                    })
        
        # Data size anomaly
        message_size = len(str(message.data))
        recent_sizes = [len(str(msg.data)) for msg in self.message_history[-20:]]
        
        if len(recent_sizes) > 5:
            avg_size = sum(recent_sizes) / len(recent_sizes)
            if message_size > avg_size * 5:  # 5x larger than average
                anomalies.append({
                    "type": "size_anomaly",
                    "description": f"Unusually large message: {message_size} bytes vs avg {avg_size:.0f} bytes",
                    "severity": "low"
                })
        
        # Data structure anomaly
        if isinstance(message.data, dict):
            # Check for unexpected keys
            common_keys = set()
            for msg in self.message_history[-20:]:
                if isinstance(msg.data, dict):
                    if not common_keys:
                        common_keys = set(msg.data.keys())
                    else:
                        common_keys &= set(msg.data.keys())
            
            unexpected_keys = set(message.data.keys()) - common_keys
            if unexpected_keys:
                anomalies.append({
                    "type": "schema_anomaly",
                    "description": f"Unexpected data keys: {list(unexpected_keys)}",
                    "severity": "low"
                })
        
        return anomalies
    
    async def _generate_insights(self, message: StreamMessage, 
                               intelligence_context: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate intelligent insights from stream data"""
        insights = []
        
        # Message rate insights
        current_hour = datetime.utcnow().hour
        hourly_messages = [msg for msg in self.message_history 
                          if msg.timestamp.hour == current_hour]
        
        if len(hourly_messages) > 0:
            insights.append({
                "type": "activity_level",
                "description": f"Current hour activity: {len(hourly_messages)} messages",
                "context": f"Hour {current_hour}:00"
            })
        
        # Data trend insights
        if isinstance(message.data, dict):
            for key, value in message.data.items():
                if isinstance(value, (int, float)):
                    recent_values = [msg.data.get(key) for msg in self.message_history[-10:] 
                                   if isinstance(msg.data, dict) and key in msg.data 
                                   and isinstance(msg.data[key], (int, float))]
                    
                    if len(recent_values) >= 3:
                        trend = "increasing" if recent_values[-1] > recent_values[0] else "decreasing"
                        insights.append({
                            "type": "trend",
                            "description": f"{key} is {trend}: {recent_values[0]} → {recent_values[-1]}",
                            "context": f"Based on last {len(recent_values)} values"
                        })
        
        # Intelligence context insights
        if intelligence_context:
            if "market_conditions" in intelligence_context:
                market = intelligence_context["market_conditions"]
                insights.append({
                    "type": "market_context",
                    "description": f"Market context: {market.get('sentiment', 'neutral')} sentiment",
                    "context": "Real-world market intelligence"
                })
        
        return insights
    
    async def _generate_recommendations(self, message: StreamMessage, patterns: List[Dict[str, Any]], 
                                      anomalies: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # High frequency recommendations
        if any(p["type"] == "high_frequency" for p in patterns):
            recommendations.append("Consider implementing message batching for high-frequency streams")
            recommendations.append("Monitor system resources due to high message rate")
        
        # Anomaly-based recommendations
        if any(a["type"] == "timing_anomaly" for a in anomalies):
            recommendations.append("Investigate potential connectivity issues or upstream delays")
        
        if any(a["type"] == "size_anomaly" for a in anomalies):
            recommendations.append("Review message size - consider compression for large messages")
        
        if any(a["type"] == "schema_anomaly" for a in anomalies):
            recommendations.append("Verify data format consistency - unexpected schema changes detected")
        
        # General recommendations
        if len(self.message_history) > 1000:
            recommendations.append("Consider archiving old messages to maintain performance")
        
        return recommendations


class MessageFilter:
    """Intelligent message filtering and routing"""
    
    def __init__(self):
        self.filters = {}
        self.routes = {}
        
    def add_filter(self, filter_name: str, filter_func: Callable[[StreamMessage], bool]) -> None:
        """Add a message filter"""
        self.filters[filter_name] = filter_func
    
    def add_route(self, route_name: str, condition: Callable[[StreamMessage], bool], 
                 handler: Callable[[StreamMessage], None]) -> None:
        """Add a message route"""
        self.routes[route_name] = {"condition": condition, "handler": handler}
    
    async def process_message(self, message: StreamMessage) -> Dict[str, Any]:
        """Process message through filters and routes"""
        result = {
            "message": message,
            "filtered": False,
            "routed_to": [],
            "processing_time": datetime.utcnow().isoformat()
        }
        
        # Apply filters
        for filter_name, filter_func in self.filters.items():
            try:
                if not filter_func(message):
                    result["filtered"] = True
                    result["filtered_by"] = filter_name
                    return result
            except Exception as e:
                logging.warning(f"Filter {filter_name} failed: {str(e)}")
        
        # Apply routes
        for route_name, route_config in self.routes.items():
            try:
                if route_config["condition"](message):
                    await route_config["handler"](message)
                    result["routed_to"].append(route_name)
            except Exception as e:
                logging.warning(f"Route {route_name} failed: {str(e)}")
        
        return result


class WebSocketAdapter:
    """
    Universal WebSocket/Streaming Adapter
    
    Automatically integrates with any real-time streaming system and provides
    intelligent stream processing, analytics, and monitoring.
    """
    
    def __init__(self, config: Optional[MassConfig] = None):
        self.config = config or MassConfig()
        self.trust_framework = TrustedAIFramework(self.config)
        self.logger = logging.getLogger(__name__)
        
        # Components
        self.stream_analyzer = StreamAnalyzer()
        self.message_filter = MessageFilter()
        self.reconnection_managers = {}
        
        # Active connections
        self.connections = {}
        self.connection_tasks = {}
        
    async def deploy(self, integration_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy WebSocket adapter based on integration plan"""
        system_config = integration_plan.get("system_config", {})
        
        # Extract stream configuration
        stream_url = system_config.get("websocket_url") or system_config.get("stream_url")
        if not stream_url:
            raise ValueError("websocket_url or stream_url is required for WebSocket integration")
        
        stream_type = self._detect_stream_type(stream_url, system_config)
        
        # Create connection ID
        connection_id = f"ws_{hash(stream_url)}"
        
        # Set up reconnection manager
        reconnection_manager = ReconnectionManager(
            max_retries=system_config.get("max_retries", 10),
            base_delay=system_config.get("base_delay", 1.0),
            max_delay=system_config.get("max_delay", 300.0)
        )
        self.reconnection_managers[connection_id] = reconnection_manager
        
        # Create stream connection
        connection = StreamConnection(
            connection_id=connection_id,
            stream_type=stream_type,
            url=stream_url,
            connection=None,
            state=ConnectionState.DISCONNECTED,
            message_handlers=[],
            message_queue=queue.Queue(maxsize=system_config.get("message_queue_size", 10000)),
            statistics={"messages_received": 0, "connection_attempts": 0, "last_message": None}
        )
        
        self.connections[connection_id] = connection
        
        # Start connection task
        connection_task = asyncio.create_task(self._maintain_connection(connection_id, system_config))
        self.connection_tasks[connection_id] = connection_task
        
        deployment_result = {
            "adapter_type": "websocket",
            "connection_id": connection_id,
            "stream_type": stream_type.value,
            "stream_url": stream_url,
            "capabilities": [
                "real_time_streaming",
                "message_filtering",
                "stream_analytics",
                "automatic_reconnection",
                "pattern_detection",
                "anomaly_detection"
            ],
            "features": {
                "automatic_reconnection": True,
                "message_queuing": True,
                "stream_analytics": True,
                "pattern_detection": True,
                "message_filtering": True,
                "health_monitoring": True
            }
        }
        
        self.logger.info(f"WebSocket adapter deployed for {stream_url}")
        return deployment_result
    
    def _detect_stream_type(self, url: str, system_config: Dict[str, Any]) -> StreamType:
        """Auto-detect stream type from URL and configuration"""
        url_lower = url.lower()
        
        if url_lower.startswith("ws://") or url_lower.startswith("wss://"):
            return StreamType.WEBSOCKET
        elif "eventsource" in url_lower or system_config.get("stream_type") == "sse":
            return StreamType.SERVER_SENT_EVENTS
        elif "socket.io" in url_lower or system_config.get("stream_type") == "socketio":
            return StreamType.SOCKET_IO
        else:
            return StreamType.WEBSOCKET  # Default
    
    async def _maintain_connection(self, connection_id: str, system_config: Dict[str, Any]) -> None:
        """Maintain connection with automatic reconnection"""
        connection = self.connections[connection_id]
        reconnection_manager = self.reconnection_managers[connection_id]
        
        while True:
            try:
                connection.state = ConnectionState.CONNECTING
                connection.statistics["connection_attempts"] += 1
                
                # Establish connection based on type
                if connection.stream_type == StreamType.WEBSOCKET:
                    await self._connect_websocket(connection, system_config)
                elif connection.stream_type == StreamType.SERVER_SENT_EVENTS:
                    await self._connect_sse(connection, system_config)
                else:
                    await self._connect_websocket(connection, system_config)  # Fallback
                
                # Reset reconnection manager on successful connection
                reconnection_manager.reset()
                connection.state = ConnectionState.CONNECTED
                
                self.logger.info(f"Successfully connected to {connection.url}")
                
                # Connection established, now handle messages
                await self._handle_connection(connection, system_config)
                
            except Exception as e:
                self.logger.error(f"Connection error for {connection_id}: {str(e)}")
                connection.state = ConnectionState.ERROR
                
                if reconnection_manager.should_retry():
                    delay = reconnection_manager.get_delay()
                    reconnection_manager.record_attempt()
                    
                    self.logger.info(f"Reconnecting in {delay:.2f} seconds (attempt {reconnection_manager.retry_count})")
                    connection.state = ConnectionState.RECONNECTING
                    
                    await asyncio.sleep(delay)
                else:
                    self.logger.error(f"Max reconnection attempts reached for {connection_id}")
                    connection.state = ConnectionState.DISCONNECTED
                    break
    
    async def _connect_websocket(self, connection: StreamConnection, system_config: Dict[str, Any]) -> None:
        """Connect to WebSocket"""
        # Prepare headers
        headers = {}
        if "headers" in system_config:
            headers.update(system_config["headers"])
        
        # Add authentication if provided
        if "auth_token" in system_config:
            headers["Authorization"] = f"Bearer {system_config['auth_token']}"
        
        # Connect to WebSocket
        connection.connection = await websockets.connect(
            connection.url,
            extra_headers=headers,
            ping_interval=system_config.get("ping_interval", 30),
            ping_timeout=system_config.get("ping_timeout", 10),
            close_timeout=system_config.get("close_timeout", 10)
        )
    
    async def _connect_sse(self, connection: StreamConnection, system_config: Dict[str, Any]) -> None:
        """Connect to Server-Sent Events"""
        # Prepare headers
        headers = {
            "Accept": "text/event-stream",
            "Cache-Control": "no-cache"
        }
        if "headers" in system_config:
            headers.update(system_config["headers"])
        
        # Add authentication if provided
        if "auth_token" in system_config:
            headers["Authorization"] = f"Bearer {system_config['auth_token']}"
        
        # Create session for SSE
        session = aiohttp.ClientSession(headers=headers)
        connection.connection = await session.get(connection.url)
    
    async def _handle_connection(self, connection: StreamConnection, system_config: Dict[str, Any]) -> None:
        """Handle messages from active connection"""
        try:
            if connection.stream_type == StreamType.WEBSOCKET:
                await self._handle_websocket_messages(connection, system_config)
            elif connection.stream_type == StreamType.SERVER_SENT_EVENTS:
                await self._handle_sse_messages(connection, system_config)
        finally:
            if connection.connection:
                if hasattr(connection.connection, 'close'):
                    await connection.connection.close()
                elif hasattr(connection.connection, '_session'):
                    await connection.connection._session.close()
    
    async def _handle_websocket_messages(self, connection: StreamConnection, system_config: Dict[str, Any]) -> None:
        """Handle WebSocket messages"""
        async for message in connection.connection:
            try:
                # Parse message
                if hasattr(message, 'data'):
                    message_data = message.data
                else:
                    message_data = str(message)
                
                # Try to parse as JSON
                try:
                    parsed_data = json.loads(message_data)
                except json.JSONDecodeError:
                    parsed_data = {"raw_message": message_data}
                
                # Create stream message
                stream_message = StreamMessage(
                    timestamp=datetime.utcnow(),
                    message_type="websocket",
                    data=parsed_data,
                    source=connection.connection_id,
                    metadata={"connection_id": connection.connection_id}
                )
                
                # Process message
                await self._process_stream_message(stream_message, connection, system_config)
                
            except Exception as e:
                self.logger.error(f"Error processing WebSocket message: {str(e)}")
    
    async def _handle_sse_messages(self, connection: StreamConnection, system_config: Dict[str, Any]) -> None:
        """Handle Server-Sent Events messages"""
        async for line in connection.connection.content:
            try:
                line_str = line.decode('utf-8').strip()
                
                if line_str.startswith('data: '):
                    data_str = line_str[6:]  # Remove 'data: ' prefix
                    
                    # Try to parse as JSON
                    try:
                        parsed_data = json.loads(data_str)
                    except json.JSONDecodeError:
                        parsed_data = {"raw_message": data_str}
                    
                    # Create stream message
                    stream_message = StreamMessage(
                        timestamp=datetime.utcnow(),
                        message_type="sse",
                        data=parsed_data,
                        source=connection.connection_id,
                        metadata={"connection_id": connection.connection_id}
                    )
                    
                    # Process message
                    await self._process_stream_message(stream_message, connection, system_config)
                    
            except Exception as e:
                self.logger.error(f"Error processing SSE message: {str(e)}")
    
    async def _process_stream_message(self, message: StreamMessage, connection: StreamConnection, 
                                    system_config: Dict[str, Any]) -> None:
        """Process a stream message with intelligence"""
        try:
            # Update statistics
            connection.statistics["messages_received"] += 1
            connection.statistics["last_message"] = message.timestamp.isoformat()
            
            # Queue message if queue is not full
            if not connection.message_queue.full():
                connection.message_queue.put(message)
            else:
                self.logger.warning(f"Message queue full for {connection.connection_id}, dropping message")
            
            # Apply message filtering
            filter_result = await self.message_filter.process_message(message)
            
            if filter_result["filtered"]:
                self.logger.debug(f"Message filtered by {filter_result['filtered_by']}")
                return
            
            # Analyze message
            intelligence_context = system_config.get("intelligence_context", {})
            analysis = await self.stream_analyzer.analyze_message(message, intelligence_context)
            
            # Call registered handlers
            for handler in connection.message_handlers:
                try:
                    await handler(message, analysis)
                except Exception as e:
                    self.logger.error(f"Message handler failed: {str(e)}")
            
            # Log insights and recommendations
            if analysis["insights"]:
                self.logger.info(f"Stream insights: {analysis['insights']}")
            
            if analysis["recommendations"]:
                self.logger.info(f"Stream recommendations: {analysis['recommendations']}")
            
            # Alert on anomalies
            if analysis["anomalies"]:
                for anomaly in analysis["anomalies"]:
                    if anomaly["severity"] in ["high", "critical"]:
                        self.logger.warning(f"Stream anomaly detected: {anomaly['description']}")
            
        except Exception as e:
            self.logger.error(f"Error processing stream message: {str(e)}")
    
    def add_message_handler(self, connection_id: str, handler: Callable[[StreamMessage, Dict[str, Any]], None]) -> None:
        """Add a message handler for a connection"""
        if connection_id in self.connections:
            self.connections[connection_id].message_handlers.append(handler)
    
    def add_message_filter(self, filter_name: str, filter_func: Callable[[StreamMessage], bool]) -> None:
        """Add a global message filter"""
        self.message_filter.add_filter(filter_name, filter_func)
    
    async def send_message(self, connection_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send message through WebSocket connection"""
        if connection_id not in self.connections:
            return {"success": False, "error": "Connection not found"}
        
        connection = self.connections[connection_id]
        
        if connection.state != ConnectionState.CONNECTED:
            return {"success": False, "error": f"Connection not ready, state: {connection.state.value}"}
        
        try:
            if connection.stream_type == StreamType.WEBSOCKET:
                await connection.connection.send(json.dumps(message))
                return {"success": True, "message": "Message sent successfully"}
            else:
                return {"success": False, "error": f"Sending not supported for {connection.stream_type.value}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_messages(self, connection_id: str, count: int = 10) -> Dict[str, Any]:
        """Get recent messages from connection queue"""
        if connection_id not in self.connections:
            return {"error": "Connection not found"}
        
        connection = self.connections[connection_id]
        messages = []
        
        # Get messages from queue (non-blocking)
        retrieved_count = 0
        while not connection.message_queue.empty() and retrieved_count < count:
            try:
                message = connection.message_queue.get_nowait()
                messages.append({
                    "timestamp": message.timestamp.isoformat(),
                    "message_type": message.message_type,
                    "data": message.data,
                    "source": message.source,
                    "metadata": message.metadata
                })
                retrieved_count += 1
            except queue.Empty:
                break
        
        return {
            "connection_id": connection_id,
            "messages": messages,
            "total_retrieved": len(messages),
            "queue_size": connection.message_queue.qsize()
        }
    
    async def health_check(self, connection_id: str) -> Dict[str, Any]:
        """Perform health check on stream connection"""
        if connection_id not in self.connections:
            return {"healthy": False, "error": "Connection not found"}
        
        connection = self.connections[connection_id]
        
        health_status = {
            "healthy": connection.state == ConnectionState.CONNECTED,
            "connection_state": connection.state.value,
            "stream_type": connection.stream_type.value,
            "statistics": connection.statistics,
            "queue_size": connection.message_queue.qsize(),
            "queue_full": connection.message_queue.full(),
            "last_check": datetime.utcnow().isoformat()
        }
        
        return health_status
    
    async def get_connection_metrics(self, connection_id: str) -> Dict[str, Any]:
        """Get performance metrics for a connection"""
        if connection_id not in self.connections:
            return {"error": "Connection not found"}
        
        connection = self.connections[connection_id]
        reconnection_manager = self.reconnection_managers.get(connection_id)
        
        metrics = {
            "connection_id": connection_id,
            "url": connection.url,
            "stream_type": connection.stream_type.value,
            "current_state": connection.state.value,
            "statistics": connection.statistics,
            "queue_metrics": {
                "current_size": connection.message_queue.qsize(),
                "max_size": connection.message_queue.maxsize,
                "is_full": connection.message_queue.full()
            },
            "reconnection_metrics": {
                "retry_count": reconnection_manager.retry_count if reconnection_manager else 0,
                "max_retries": reconnection_manager.max_retries if reconnection_manager else 0,
                "last_attempt": reconnection_manager.last_attempt.isoformat() if reconnection_manager and reconnection_manager.last_attempt else None
            },
            "handler_count": len(connection.message_handlers)
        }
        
        return metrics
    
    async def close_connection(self, connection_id: str) -> Dict[str, Any]:
        """Close stream connection"""
        if connection_id not in self.connections:
            return {"success": False, "error": "Connection not found"}
        
        try:
            # Cancel connection task
            if connection_id in self.connection_tasks:
                self.connection_tasks[connection_id].cancel()
                del self.connection_tasks[connection_id]
            
            # Close connection
            connection = self.connections[connection_id]
            if connection.connection:
                if hasattr(connection.connection, 'close'):
                    await connection.connection.close()
                elif hasattr(connection.connection, '_session'):
                    await connection.connection._session.close()
            
            # Clean up
            del self.connections[connection_id]
            if connection_id in self.reconnection_managers:
                del self.reconnection_managers[connection_id]
            
            return {"success": True, "message": f"Connection {connection_id} closed successfully"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}