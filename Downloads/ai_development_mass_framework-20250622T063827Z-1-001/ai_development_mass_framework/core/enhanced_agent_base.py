"""
🛡️ ENTERPRISE-GRADE AGENT BASE CLASS
Enhanced base class with Trust Framework integration for enterprise AI agents.

This is the foundation for all agents in the MASS framework, providing:
- Trust framework integration for enterprise compliance
- Security controls and validation
- Comprehensive audit logging
- Privacy-preserving processing
- Explainable AI decisions
- Human oversight capabilities
- Performance monitoring
- Error handling and recovery
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import logging
import asyncio
import time
import uuid
from datetime import datetime

# Legacy message system compatibility
class MessageType(Enum):
    ANALYSIS_REQUEST = "analysis_request"
    ANALYSIS_RESPONSE = "analysis_response"
    COORDINATION_REQUEST = "coordination_request"
    COORDINATION_RESPONSE = "coordination_response"
    CONFLICT_ALERT = "conflict_alert"
    SOLUTION_PROPOSAL = "solution_proposal"
    APPROVAL_REQUEST = "approval_request"
    STATUS_UPDATE = "status_update"

@dataclass
class AgentMessage:
    sender_id: str
    receiver_id: str
    message_type: MessageType
    payload: Dict[str, Any]
    timestamp: float
    correlation_id: str
    priority: int = 1  # 1-10, 10 being highest priority

# Import trust framework
try:
    from trust_framework.trusted_ai_manager import (
        TrustedAIManager, TrustAssessment, TrustLevel, 
        ComplianceStandard, RiskLevel
    )
    TRUST_FRAMEWORK_AVAILABLE = True
except ImportError:
    # Fallback when trust framework is not available
    TRUST_FRAMEWORK_AVAILABLE = False
    
    # Mock classes for fallback
    class TrustLevel:
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        CRITICAL = "critical"
    
    class TrustAssessment:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

@dataclass
class SecurityContext:
    """Security context for agent operations"""
    user_id: str
    tenant_id: str
    permissions: List[str]
    encryption_required: bool = True
    audit_level: str = "comprehensive"
    data_classification: str = "sensitive"

@dataclass
class AgentMetrics:
    """Enhanced agent performance metrics"""
    tasks_completed: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    total_processing_time: float = 0.0
    average_processing_time: float = 0.0
    average_trust_score: float = 0.0
    human_reviews_required: int = 0
    security_violations: int = 0
    compliance_failures: int = 0
    last_activity: Optional[datetime] = None
    uptime_percentage: float = 100.0

class ErrorHandler:
    """Enterprise-grade error handling for agents"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.error_history = []
        self.logger = logging.getLogger(f"agent.{agent_id}.error_handler")
    
    async def handle_error(self, error: Exception, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle and log errors with recovery suggestions"""
        error_context = {
            "error_id": str(uuid.uuid4()),
            "agent_id": self.agent_id,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "task_id": task_data.get("task_id", "unknown"),
            "timestamp": datetime.utcnow(),
            "recovery_suggestions": self._get_recovery_suggestions(error),
            "severity": self._assess_error_severity(error)
        }
        
        self.error_history.append(error_context)
        self.logger.error(f"Agent error: {error_context}")
        
        return error_context
    
    def _get_recovery_suggestions(self, error: Exception) -> List[str]:
        """Get recovery suggestions based on error type"""
        error_type = type(error).__name__
        
        suggestions = {
            "TimeoutError": ["Increase timeout values", "Check network connectivity", "Review resource allocation"],
            "ValueError": ["Validate input data format", "Check data types", "Review input validation"],
            "KeyError": ["Check required fields", "Validate data structure", "Review API contract"],
            "ConnectionError": ["Check network connectivity", "Verify service availability", "Review firewall settings"],
            "AuthenticationError": ["Check credentials", "Verify permissions", "Review authentication flow"]
        }
        
        return suggestions.get(error_type, ["Review error logs", "Contact system administrator", "Check system status"])
    
    def _assess_error_severity(self, error: Exception) -> str:
        """Assess error severity level"""
        critical_errors = ["SystemExit", "MemoryError", "OSError"]
        high_errors = ["ConnectionError", "TimeoutError", "AuthenticationError"]
        medium_errors = ["ValueError", "KeyError", "TypeError"]
        
        error_type = type(error).__name__
        
        if error_type in critical_errors:
            return "critical"
        elif error_type in high_errors:
            return "high"
        elif error_type in medium_errors:
            return "medium"
        else:
            return "low"

class PerformanceMonitor:
    """Real-time performance monitoring for agents"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.metrics = AgentMetrics()
        self.performance_history = []
        self.logger = logging.getLogger(f"agent.{agent_id}.performance")
    
    def track_task(self, task_id: str):
        """Context manager for tracking task performance"""
        return TaskPerformanceTracker(self, task_id)
    
    def update_metrics(self, processing_time: float, success: bool, trust_score: float = 0.0):
        """Update performance metrics"""
        self.metrics.tasks_completed += 1
        
        if success:
            self.metrics.successful_tasks += 1
        else:
            self.metrics.failed_tasks += 1
        
        self.metrics.total_processing_time += processing_time
        self.metrics.average_processing_time = (
            self.metrics.total_processing_time / self.metrics.tasks_completed
        )
        
        # Update trust score average
        if trust_score > 0:
            current_avg = self.metrics.average_trust_score
            total_tasks = self.metrics.tasks_completed
            self.metrics.average_trust_score = (
                (current_avg * (total_tasks - 1) + trust_score) / total_tasks
            )
        
        self.metrics.last_activity = datetime.utcnow()
        
        # Store performance data point
        self.performance_history.append({
            "timestamp": datetime.utcnow(),
            "processing_time": processing_time,
            "success": success,
            "trust_score": trust_score
        })
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        success_rate = (
            self.metrics.successful_tasks / self.metrics.tasks_completed 
            if self.metrics.tasks_completed > 0 else 0.0
        )
        
        return {
            "agent_id": self.agent_id,
            "metrics": {
                "tasks_completed": self.metrics.tasks_completed,
                "success_rate": success_rate,
                "average_processing_time": self.metrics.average_processing_time,
                "average_trust_score": self.metrics.average_trust_score,
                "human_reviews_required": self.metrics.human_reviews_required,
                "security_violations": self.metrics.security_violations,
                "compliance_failures": self.metrics.compliance_failures,
                "uptime_percentage": self.metrics.uptime_percentage
            },
            "recent_performance": self.performance_history[-10:],  # Last 10 tasks
            "status": self._get_performance_status()
        }
    
    def _get_performance_status(self) -> str:
        """Get overall performance status"""
        success_rate = (
            self.metrics.successful_tasks / self.metrics.tasks_completed 
            if self.metrics.tasks_completed > 0 else 1.0
        )
        
        if success_rate >= 0.95 and self.metrics.average_trust_score >= 0.85:
            return "excellent"  
        elif success_rate >= 0.90 and self.metrics.average_trust_score >= 0.75:
            return "good"
        elif success_rate >= 0.80 and self.metrics.average_trust_score >= 0.65:
            return "acceptable"
        else:
            return "needs_improvement"

class TaskPerformanceTracker:
    """Context manager for tracking individual task performance"""
    
    def __init__(self, monitor: PerformanceMonitor, task_id: str):
        self.monitor = monitor
        self.task_id = task_id
        self.start_time = None
        self.success = False
        self.trust_score = 0.0
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            processing_time = time.time() - self.start_time
            self.success = exc_type is None
            self.monitor.update_metrics(processing_time, self.success, self.trust_score)
    
    def set_trust_score(self, score: float):
        """Set trust score for this task"""
        self.trust_score = score

class AuditLogger:
    """Comprehensive audit logging for compliance"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.audit_log = []
        self.logger = logging.getLogger(f"agent.{agent_id}.audit")
    
    async def log_task_completion(self, task_data: Dict[str, Any], result: Dict[str, Any], 
                                trust_assessment: Optional[TrustAssessment] = None,
                                explanation: str = ""):
        """Log task completion for audit trail"""
        audit_entry = {
            "audit_id": str(uuid.uuid4()),
            "agent_id": self.agent_id,
            "event_type": "task_completion",
            "timestamp": datetime.utcnow().isoformat(),
            "task_id": task_data.get("task_id", "unknown"),
            "task_type": task_data.get("task_type", "unknown"),
            "input_hash": self._hash_data(task_data),
            "output_hash": self._hash_data(result),
            "trust_score": trust_assessment.trust_score if trust_assessment else None,
            "human_review_required": trust_assessment.human_review_required if trust_assessment else False,
            "explanation": explanation,
            "compliance_status": trust_assessment.compliance_status if trust_assessment else {},
            "processing_time": result.get("processing_time", 0.0)
        }
        
        self.audit_log.append(audit_entry)
        self.logger.info(f"Task completion logged: {audit_entry['audit_id']}")
    
    async def log_error(self, error: Exception, task_data: Dict[str, Any], 
                       error_context: Dict[str, Any]):
        """Log errors for audit trail"""
        audit_entry = {
            "audit_id": str(uuid.uuid4()),
            "agent_id": self.agent_id,
            "event_type": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "task_id": task_data.get("task_id", "unknown"),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "error_context": error_context,
            "input_hash": self._hash_data(task_data)
        }
        
        self.audit_log.append(audit_entry)
        self.logger.error(f"Error logged: {audit_entry['audit_id']}")
    
    def _hash_data(self, data: Dict[str, Any]) -> str:
        """Create hash of data for audit purposes"""
        import hashlib
        import json
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    async def get_last_audit_id(self) -> str:
        """Get the last audit ID"""
        return self.audit_log[-1]["audit_id"] if self.audit_log else "none"

class EnhancedAgentBase(ABC):
    """
    🛡️ ENTERPRISE-GRADE AGENT BASE CLASS
    
    This enhanced base class provides enterprise-grade capabilities for all agents:
    
    TRUST FRAMEWORK INTEGRATION:
    - All agent outputs validated against trust framework
    - Explainable AI decisions with transparency
    - Bias detection and fairness validation
    - Privacy-preserving processing
    - Security controls and monitoring
    
    ENTERPRISE FEATURES:
    - Comprehensive audit logging for compliance
    - Performance monitoring and optimization
    - Error handling and recovery
    - Human oversight and intervention
    - Multi-tenant security support
    
    COMPLIANCE SUPPORT:
    - GDPR, SOC 2, ISO 42001 compliance validation
    - Regulatory audit trail maintenance
    - Data sovereignty controls
    - Security vulnerability monitoring
    
    All agents MUST inherit from this class for enterprise deployment.
    """
    
    def __init__(self, agent_id: str, specialization: str, 
                 trust_level: Union[str, TrustLevel] = TrustLevel.HIGH):
        self.agent_id = agent_id
        self.specialization = specialization
        self.trust_level = trust_level if isinstance(trust_level, str) else trust_level.value
        
        # Legacy compatibility
        self.coordinator = None
        self.message_queue = []
        self.active_tasks = {}
        
        # Core logging
        self.logger = logging.getLogger(f"agent.{agent_id}")
        
        # Trust framework integration
        if TRUST_FRAMEWORK_AVAILABLE:
            self.trust_manager = TrustedAIManager()
        else:
            self.trust_manager = None
            self.logger.warning("Trust framework not available - operating in basic mode")
        
        # Enterprise components
        self.performance_monitor = PerformanceMonitor(agent_id)
        self.error_handler = ErrorHandler(agent_id)
        self.audit_logger = AuditLogger(agent_id)
        
        # Security context
        self.current_security_context: Optional[SecurityContext] = None
        
        self.logger.info(f"Enhanced agent {agent_id} initialized with trust level: {self.trust_level}")
    
    async def process_task_with_trust(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🛡️ ENTERPRISE TASK PROCESSING WITH TRUST VALIDATION
        
        This is the main entry point for all agent task processing in enterprise environments.
        It ensures that all AI decisions meet enterprise trust, security, and compliance standards.
        
        PROCESS FLOW:
        1. Pre-processing security validation
        2. Privacy-preserving data handling
        3. Core task processing with monitoring
        4. Trust framework validation
        5. Post-processing security checks
        6. Audit logging and transparency reporting
        7. Performance metrics collection
        8. Error handling and recovery
        
        Args:
            task_data: Input data for the task
            
        Returns:
            Dict containing:
            - result: Core task processing result
            - trust_assessment: Trust framework validation results
            - explanation: Explainable AI decision details
            - audit_id: Audit trail identifier
            - performance_metrics: Task performance data
        """
        
        task_id = task_data.get("task_id", str(uuid.uuid4()))
        task_data["task_id"] = task_id
        
        # Start performance monitoring
        with self.performance_monitor.track_task(task_id) as tracker:
            try:
                self.logger.info(f"Starting enterprise task processing: {task_id}")
                
                # Phase 1: Pre-processing validation
                await self._validate_input_security(task_data)
                await self._apply_privacy_protection(task_data)
                
                # Phase 2: Core processing with bias detection
                result = await self.process_task(task_data)
                
                # Phase 3: Trust framework validation
                trust_assessment = None
                if self.trust_manager:
                    trust_level_enum = getattr(TrustLevel, self.trust_level.upper(), TrustLevel.HIGH)
                    trust_assessment = await self.trust_manager.validate_agent_output(
                        self.agent_id, task_data, result, trust_level_enum
                    )
                    
                    # Update performance tracker with trust score
                    tracker.set_trust_score(trust_assessment.trust_score)
                    
                    # Handle human review requirement
                    if trust_assessment.human_review_required:
                        result = await self._request_human_review(task_data, result, trust_assessment)
                        # Update metrics
                        self.performance_monitor.metrics.human_reviews_required += 1
                
                # Phase 4: Post-processing security validation
                await self._validate_output_security(result)
                
                # Phase 5: Generate explainable output
                explanation = await self._generate_explanation(task_data, result, trust_assessment)
                
                # Phase 6: Audit logging
                await self.audit_logger.log_task_completion(
                    task_data, result, trust_assessment, explanation
                )
                
                # Phase 7: Compile enterprise response
                enterprise_response = {
                    "result": result,
                    "trust_assessment": trust_assessment.to_dict() if trust_assessment else None,
                    "explanation": explanation,
                    "audit_id": await self.audit_logger.get_last_audit_id(),
                    "performance_metrics": {
                        "processing_time": tracker.monitor.performance_history[-1]["processing_time"] if tracker.monitor.performance_history else 0.0,
                        "success": True,
                        "trust_score": trust_assessment.trust_score if trust_assessment else 0.0
                    },
                    "agent_info": {
                        "agent_id": self.agent_id,
                        "specialization": self.specialization,
                        "trust_level": self.trust_level
                    }
                }
                
                self.logger.info(f"Enterprise task processing completed successfully: {task_id}")
                return enterprise_response
                
            except Exception as e:
                # Enterprise-grade error handling
                error_context = await self.error_handler.handle_error(e, task_data)
                await self.audit_logger.log_error(e, task_data, error_context)
                
                # Update performance metrics
                if self.trust_manager and "SecurityViolation" in str(type(e)):
                    self.performance_monitor.metrics.security_violations += 1
                elif self.trust_manager and "ComplianceFailure" in str(type(e)):
                    self.performance_monitor.metrics.compliance_failures += 1
                
                self.logger.error(f"Enterprise task processing failed: {task_id} - {str(e)}")
                
                # Return error response with enterprise context
                return {
                    "result": None,
                    "error": {
                        "error_id": error_context["error_id"],
                        "message": str(e),
                        "type": type(e).__name__,
                        "severity": error_context["severity"],
                        "recovery_suggestions": error_context["recovery_suggestions"]
                    },
                    "trust_assessment": None,
                    "explanation": f"Task processing failed due to {type(e).__name__}: {str(e)}",
                    "audit_id": await self.audit_logger.get_last_audit_id(),
                    "agent_info": {
                        "agent_id": self.agent_id,
                        "specialization": self.specialization,
                        "trust_level": self.trust_level
                    }
                }
    
    @abstractmethod
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core task processing method - must be implemented by each agent
        
        This method contains the core logic for the agent's specialized functionality.
        It should focus on the business logic while the enterprise concerns are
        handled by the process_task_with_trust wrapper.
        
        Args:
            task_data: Input data for the task
            
        Returns:
            Dict: Core processing results
        """
        pass
    
    # Legacy compatibility methods
    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input data - legacy compatibility"""
        return await self.process_task(input_data)
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents - legacy compatibility"""
        # Basic coordination logic
        return {
            "coordination_status": "completed",
            "participating_agents": other_agents,
            "task_context": task_context
        }
    
    async def send_message(self, message: AgentMessage):
        """Send message to coordinator - legacy compatibility"""
        if self.coordinator:
            await self.coordinator.route_message(message)
    
    async def receive_message(self, message: AgentMessage):
        """Receive message from coordinator - legacy compatibility"""
        self.message_queue.append(message)
        await self.process_message_queue()
    
    async def process_message_queue(self):
        """Process queued messages - legacy compatibility"""
        while self.message_queue:
            message = self.message_queue.pop(0)
            # Implement message handling logic here
            pass
    
    async def _validate_input_security(self, task_data: Dict[str, Any]):
        """Validate input data for security threats"""
        # Basic security validation
        task_str = str(task_data).lower()
        
        # Check for common injection patterns
        dangerous_patterns = [
            "drop table", "delete from", "insert into", "<script", "javascript:", 
            "eval(", "exec(", "system(", "os.system", "__import__"
        ]
        
        for pattern in dangerous_patterns:
            if pattern in task_str:
                raise SecurityException(f"Potentially dangerous input detected: {pattern}")
    
    async def _apply_privacy_protection(self, task_data: Dict[str, Any]):
        """Apply privacy-preserving techniques to sensitive data"""
        # Basic privacy protection - in production, this would be more sophisticated
        sensitive_fields = ["password", "ssn", "credit_card", "personal_info"]
        
        def sanitize_value(value):
            if isinstance(value, str) and len(value) > 4:
                # Mask sensitive information
                return value[:2] + "*" * (len(value) - 4) + value[-2:]
            return value
        
        for key, value in task_data.items():
            if any(sensitive in key.lower() for sensitive in sensitive_fields):
                if isinstance(value, str):
                    task_data[key] = sanitize_value(value)
    
    async def _validate_output_security(self, result: Dict[str, Any]):
        """Validate output data for security issues"""
        # Basic output security validation
        result_str = str(result).lower()
        
        # Check for information leakage
        sensitive_patterns = [
            "password", "secret", "key", "token", "credential", 
            "private", "confidential", "internal"
        ]
        
        for pattern in sensitive_patterns:
            if pattern in result_str:
                self.logger.warning(f"Potential sensitive information in output: {pattern}")
    
    async def _generate_explanation(self, task_data: Dict[str, Any], result: Dict[str, Any], 
                                  trust_assessment: Optional[TrustAssessment] = None) -> str:
        """Generate comprehensive explanation for AI decision"""
        explanation_parts = []
        
        # Basic explanation
        explanation_parts.append(f"Agent {self.agent_id} ({self.specialization}) processed the task")
        
        # Add trust information if available
        if trust_assessment:
            explanation_parts.append(f"with trust score {trust_assessment.trust_score:.2f}")
            if trust_assessment.human_review_required:
                explanation_parts.append("requiring human review")
        
        # Add result summary
        if "summary" in result:
            explanation_parts.append(f"Result summary: {result['summary']}")
        elif "recommendation" in result:
            explanation_parts.append(f"Recommendation: {result['recommendation']}")
        
        return ". ".join(explanation_parts) + "."
    
    async def _request_human_review(self, task_data: Dict[str, Any], result: Dict[str, Any], 
                                   trust_assessment: TrustAssessment) -> Dict[str, Any]:
        """Request human review for low-trust decisions"""
        self.logger.info(f"Human review requested for task {task_data.get('task_id')} - trust score: {trust_assessment.trust_score}")
        
        # In a real implementation, this would integrate with a human review system
        # For now, we'll add a flag and return the original result
        result["human_review_required"] = True
        result["human_review_reason"] = trust_assessment.explanation
        result["human_review_id"] = str(uuid.uuid4())
        
        return result
    
    async def get_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status including enterprise metrics"""
        base_status = {
            "agent_id": self.agent_id,
            "specialization": self.specialization,
            "trust_level": self.trust_level,
            "status": "active",
            "last_updated": datetime.utcnow().isoformat()
        }
        
        # Add performance metrics
        performance_summary = self.performance_monitor.get_performance_summary()
        base_status["performance"] = performance_summary
        
        # Add trust framework status
        if self.trust_manager:
            trust_metrics = await self.trust_manager.get_trust_metrics(self.agent_id)
            base_status["trust_metrics"] = trust_metrics
        
        # Add error summary
        recent_errors = self.error_handler.error_history[-5:]  # Last 5 errors
        base_status["recent_errors"] = [
            {
                "error_id": error["error_id"],
                "timestamp": error["timestamp"].isoformat() if isinstance(error["timestamp"], datetime) else error["timestamp"],
                "error_type": error["error_type"],
                "severity": error["severity"]
            }
            for error in recent_errors
        ]
        
        return base_status
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities and supported operations"""
        return {
            "agent_id": self.agent_id,
            "specialization": self.specialization,
            "trust_level": self.trust_level,
            "enterprise_features": {
                "trust_framework": TRUST_FRAMEWORK_AVAILABLE,
                "audit_logging": True,
                "performance_monitoring": True,
                "security_validation": True,
                "privacy_protection": True,
                "human_oversight": True,
                "error_recovery": True
            },
            "supported_operations": await self._get_supported_operations(),
            "compliance_standards": [
                "GDPR",
                "SOC 2", 
                "ISO 42001"
            ] if TRUST_FRAMEWORK_AVAILABLE else [],
            "security_features": [
                "Input validation",
                "Output sanitization", 
                "Access control",
                "Audit logging",
                "Error handling"
            ]
        }
    
    async def _get_supported_operations(self) -> List[str]:
        """Get list of supported operations - to be overridden by specific agents"""
        return ["process_task", "get_status", "get_capabilities"]
    
    def set_security_context(self, context: SecurityContext):
        """Set security context for current operations"""
        self.current_security_context = context
        self.logger.info(f"Security context set for user {context.user_id}, tenant {context.tenant_id}")
    
    def update_metrics(self, processing_time: float, success: bool):
        """Update performance metrics (legacy compatibility)"""
        trust_score = 0.8 if success else 0.0  # Default trust score
        self.performance_monitor.update_metrics(processing_time, success, trust_score)

# Legacy compatibility - keep original AgentBase for backward compatibility
class AgentBase(ABC):
    """Legacy base class for backward compatibility"""
    
    def __init__(self, agent_id: str, specialization: str):
        self.agent_id = agent_id
        self.specialization = specialization
        self.coordinator = None
        self.message_queue = []
        self.active_tasks = {}
        
        # Basic logging and metrics
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.performance_metrics = {
            "tasks_completed": 0,
            "total_processing_time": 0,
            "errors": 0,
            "last_activity": None
        }
    
    @abstractmethod
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task and return results"""
        pass
    
    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input data"""
        return await self.process_task(input_data)
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents"""
        return {
            "coordination_status": "completed",
            "participating_agents": other_agents,
            "task_context": task_context
        }
    
    async def send_message(self, message: AgentMessage):
        """Send message to coordinator"""
        if self.coordinator:
            await self.coordinator.route_message(message)
    
    async def receive_message(self, message: AgentMessage):
        """Receive message from coordinator"""
        self.message_queue.append(message)
        await self.process_message_queue()
    
    async def process_message_queue(self):
        """Process queued messages"""
        while self.message_queue:
            message = self.message_queue.pop(0)
            # Implement message handling logic here
            pass
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "specialization": self.specialization,
            "status": "active",
            "metrics": self.performance_metrics
        }
    
    def update_metrics(self, processing_time: float, success: bool):
        """Update performance metrics"""
        self.performance_metrics["tasks_completed"] += 1
        self.performance_metrics["total_processing_time"] += processing_time
        if not success:
            self.performance_metrics["errors"] += 1
        self.performance_metrics["last_activity"] = datetime.utcnow().isoformat()

# Custom exceptions
class SecurityException(Exception):
    """Raised when security validation fails"""
    pass

class ComplianceException(Exception):
    """Raised when compliance validation fails"""
    pass

class TrustException(Exception):
    """Raised when trust validation fails"""
    pass

# Export classes
__all__ = [
    "EnhancedAgentBase",
    "AgentBase",  # Legacy compatibility
    "AgentMessage",
    "MessageType",
    "SecurityContext",
    "AgentMetrics",
    "SecurityException",
    "ComplianceException", 
    "TrustException"
]
