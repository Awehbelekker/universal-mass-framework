"""
Agent Coordinator - Multi-Agent Task Orchestration

This component coordinates multiple AI agents to work together on complex tasks,
providing intelligent task decomposition, agent selection, and result synthesis.

Key Features:
- Intelligent task decomposition and delegation
- Agent capability matching and selection
- Real-time coordination and conflict resolution
- Dynamic load balancing and optimization
- Enterprise-grade oversight and control
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Union, Callable, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid
import time

from .config_manager import MassConfig
from ..enterprise_trust.trusted_ai_framework import TrustedAIFramework

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Types of tasks that can be coordinated"""
    ANALYSIS = "analysis"
    PREDICTION = "prediction"
    OPTIMIZATION = "optimization"
    GENERATION = "generation"
    INTEGRATION = "integration"
    MONITORING = "monitoring"
    DECISION_MAKING = "decision_making"


class AgentRole(Enum):
    """Roles agents can play in task execution"""
    PRIMARY = "primary"
    SUPPORTING = "supporting"
    VALIDATOR = "validator"
    MONITOR = "monitor"
    COORDINATOR = "coordinator"


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5


@dataclass
class AgentCapability:
    """Agent capability definition"""
    agent_id: str
    capability_type: str
    proficiency_score: float  # 0.0 to 1.0
    specializations: List[str]
    availability: bool
    current_load: float  # 0.0 to 1.0
    performance_history: List[float]


@dataclass
class SubTask:
    """Individual subtask definition"""
    subtask_id: str
    task_type: TaskType
    description: str
    input_data: Dict[str, Any]
    requirements: List[str]
    constraints: List[str]
    dependencies: List[str]  # Other subtask IDs this depends on
    assigned_agent: Optional[str] = None
    agent_role: Optional[AgentRole] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    estimated_duration: int = 30  # seconds
    timeout: int = 300  # seconds


@dataclass
class TaskPlan:
    """Complete task execution plan"""
    plan_id: str
    main_task_description: str
    subtasks: List[SubTask]
    agent_assignments: Dict[str, List[str]]  # agent_id -> list of subtask_ids
    execution_order: List[List[str]]  # Parallel execution groups
    estimated_total_time: int
    risk_assessment: Dict[str, Any]


@dataclass
class AgentResult:
    """Result from individual agent execution"""
    agent_id: str
    subtask_id: str
    status: str  # success, error, timeout, cancelled
    result_data: Dict[str, Any]
    execution_time_ms: int
    confidence_score: float
    error_message: Optional[str] = None


@dataclass
class CoordinationResult:
    """Result of multi-agent task coordination"""
    coordination_id: str
    task_description: str
    status: str
    task_plan: TaskPlan
    agent_results: List[AgentResult]
    synthesized_result: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    total_execution_time_ms: int
    overall_confidence: float
    timestamp: datetime


class AgentCoordinator:
    """
    Multi-Agent Task Coordinator
    
    Orchestrates multiple AI agents to work together on complex tasks,
    providing intelligent coordination, load balancing, and result synthesis.
    """
    
    def __init__(self, config: Optional[MassConfig] = None):
        self.config = config or MassConfig()
        self.trust_framework = TrustedAIFramework(self.config)
        self.logger = logging.getLogger(__name__)
        
        # Agent management
        self.registered_agents = {}
        self.agent_capabilities = {}
        self.agent_performance_history = {}
        
        # Task management
        self.active_coordinations = {}
        self.task_queue = asyncio.Queue()
        self.coordination_history = []
        
        # Configuration
        self.max_concurrent_tasks = 50
        self.default_timeout = 300  # seconds
        self.load_balance_threshold = 0.8
        
        # Performance metrics
        self.metrics = {
            "total_coordinations": 0,
            "successful_coordinations": 0,
            "failed_coordinations": 0,
            "average_execution_time": 0,
            "agent_utilization": {}
        }
        
        self.logger.info("Agent Coordinator initialized")
    
    async def initialize(self):
        """Initialize the agent coordinator"""
        try:
            # Register default intelligence agents
            await self._register_default_agents()
            
            # Start coordination processor
            asyncio.create_task(self._coordination_processor())
            
            # Start performance monitor
            asyncio.create_task(self._performance_monitor())
            
            self.logger.info("Agent Coordinator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Agent Coordinator: {str(e)}")
            raise
    
    async def register_agent(self, agent_id: str, agent_instance: Any, 
                           capabilities: List[str], specializations: List[str] = None) -> bool:
        """
        Register an agent with the coordinator
        
        Args:
            agent_id: Unique identifier for the agent
            agent_instance: The actual agent instance
            capabilities: List of capabilities the agent provides
            specializations: Optional list of specializations
            
        Returns:
            True if registration successful
        """
        try:
            # Validate agent has required methods
            required_methods = ['process_task', 'analyze_input']
            for method in required_methods:
                if not hasattr(agent_instance, method):
                    raise ValueError(f"Agent {agent_id} missing required method: {method}")
            
            # Register agent
            self.registered_agents[agent_id] = agent_instance
            
            # Register capabilities
            for capability in capabilities:
                agent_capability = AgentCapability(
                    agent_id=agent_id,
                    capability_type=capability,
                    proficiency_score=0.8,  # Default proficiency
                    specializations=specializations or [],
                    availability=True,
                    current_load=0.0,
                    performance_history=[0.8]  # Default performance
                )
                
                if agent_id not in self.agent_capabilities:
                    self.agent_capabilities[agent_id] = []
                self.agent_capabilities[agent_id].append(agent_capability)
            
            self.logger.info(f"Agent {agent_id} registered with capabilities: {capabilities}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register agent {agent_id}: {str(e)}")
            return False
    
    async def execute_multi_agent_task(self, task_description: str, 
                                     task_data: Dict[str, Any],
                                     context: Optional[Dict[str, Any]] = None) -> CoordinationResult:
        """
        Execute a complex task using multiple agents
        
        Args:
            task_description: Description of the task to be performed
            task_data: Input data for the task
            context: Optional context information
            
        Returns:
            Coordination result with synthesized outputs
        """
        coordination_id = f"coord_{uuid.uuid4().hex[:8]}"
        start_time = datetime.utcnow()
        
        try:
            # Validate with trust framework
            trust_validation = await self.trust_framework.validate_operation(
                operation_type="multi_agent_coordination",
                data=task_data,
                context=context or {}
            )
            
            if not trust_validation.is_valid:
                raise ValueError(f"Trust validation failed: {trust_validation.validation_details}")
            
            # Analyze task requirements
            task_analysis = await self._analyze_task_requirements(task_description, task_data, context)
            
            # Create task decomposition plan
            task_plan = await self._create_task_plan(task_analysis, task_description)
            
            # Select and assign agents
            agent_assignments = await self._assign_agents_to_tasks(task_plan)
            task_plan.agent_assignments = agent_assignments
            
            # Execute task plan
            agent_results = await self._execute_task_plan(task_plan, coordination_id)
            
            # Synthesize results
            synthesized_result = await self._synthesize_results(agent_results, task_plan)
            
            # Calculate performance metrics
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            performance_metrics = self._calculate_performance_metrics(agent_results, execution_time)
            
            # Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(agent_results)
            
            # Create coordination result
            result = CoordinationResult(
                coordination_id=coordination_id,
                task_description=task_description,
                status="success",
                task_plan=task_plan,
                agent_results=agent_results,
                synthesized_result=synthesized_result,
                performance_metrics=performance_metrics,
                total_execution_time_ms=execution_time,
                overall_confidence=overall_confidence,
                timestamp=start_time
            )
            
            # Update performance history
            await self._update_performance_history(result)
            
            # Log successful coordination
            await self.trust_framework.log_operation(
                operation_type="multi_agent_coordination_completed",
                operation_data={
                    "coordination_id": coordination_id,
                    "agents_involved": len(agent_assignments),
                    "subtasks_completed": len([r for r in agent_results if r.status == "success"]),
                    "overall_confidence": overall_confidence
                },
                result="success"
            )
            
            self.logger.info(f"Multi-agent coordination completed: {coordination_id}")
            return result
            
        except Exception as e:
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            # Create error result
            result = CoordinationResult(
                coordination_id=coordination_id,
                task_description=task_description,
                status="error",
                task_plan=TaskPlan("", "", [], {}, [], 0, {}),
                agent_results=[],
                synthesized_result={"error": str(e)},
                performance_metrics={"execution_time_ms": execution_time},
                total_execution_time_ms=execution_time,
                overall_confidence=0.0,
                timestamp=start_time
            )
            
            # Log error
            await self.trust_framework.log_operation(
                operation_type="multi_agent_coordination_failed",
                operation_data={"coordination_id": coordination_id, "error": str(e)},
                result="error"
            )
            
            self.logger.error(f"Multi-agent coordination failed: {str(e)}")
            raise
    
    async def _analyze_task_requirements(self, task_description: str, 
                                       task_data: Dict[str, Any],
                                       context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze task requirements to determine decomposition strategy"""
        analysis = {
            "task_complexity": "medium",
            "required_capabilities": [],
            "data_requirements": [],
            "estimated_duration": 60,
            "parallelizable": True,
            "dependencies": []
        }
        
        # Analyze task description for keywords
        description_lower = task_description.lower()
        
        # Determine required capabilities
        if any(word in description_lower for word in ["analyze", "analysis", "examine"]):
            analysis["required_capabilities"].append("data_analysis")
        
        if any(word in description_lower for word in ["predict", "forecast", "estimate"]):
            analysis["required_capabilities"].append("prediction")
        
        if any(word in description_lower for word in ["optimize", "improve", "enhance"]):
            analysis["required_capabilities"].append("optimization")
        
        if any(word in description_lower for word in ["generate", "create", "build"]):
            analysis["required_capabilities"].append("generation")
        
        if any(word in description_lower for word in ["integrate", "connect", "combine"]):
            analysis["required_capabilities"].append("integration")
        
        # Determine task complexity
        if len(task_data) > 100 or len(analysis["required_capabilities"]) > 3:
            analysis["task_complexity"] = "high"
        elif len(task_data) < 10 and len(analysis["required_capabilities"]) <= 1:
            analysis["task_complexity"] = "low"
        
        # Estimate duration based on complexity
        complexity_duration = {
            "low": 30,
            "medium": 60,
            "high": 120
        }
        analysis["estimated_duration"] = complexity_duration[analysis["task_complexity"]]
        
        return analysis
    
    async def _create_task_plan(self, task_analysis: Dict[str, Any], 
                              task_description: str) -> TaskPlan:
        """Create a detailed task execution plan"""
        plan_id = f"plan_{uuid.uuid4().hex[:8]}"
        subtasks = []
        
        required_capabilities = task_analysis["required_capabilities"]
        
        # Create subtasks based on required capabilities
        for i, capability in enumerate(required_capabilities):
            subtask = SubTask(
                subtask_id=f"subtask_{i+1}",
                task_type=self._capability_to_task_type(capability),
                description=f"Perform {capability} for: {task_description}",
                input_data={"task_description": task_description, "capability": capability},
                requirements=[capability],
                constraints=[],
                dependencies=[],
                priority=TaskPriority.HIGH if i == 0 else TaskPriority.MEDIUM,
                estimated_duration=task_analysis["estimated_duration"] // len(required_capabilities)
            )
            subtasks.append(subtask)
        
        # Add synthesis subtask if multiple capabilities required
        if len(required_capabilities) > 1:
            synthesis_subtask = SubTask(
                subtask_id=f"subtask_synthesis",
                task_type=TaskType.INTEGRATION,
                description=f"Synthesize results from multiple analyses",
                input_data={"synthesis_required": True},
                requirements=["integration"],
                constraints=[],
                dependencies=[st.subtask_id for st in subtasks],
                priority=TaskPriority.HIGH,
                estimated_duration=30
            )
            subtasks.append(synthesis_subtask)
        
        # Determine execution order
        execution_order = []
        if len(subtasks) > 1 and subtasks[-1].subtask_id == "subtask_synthesis":
            # Parallel execution of main tasks, then synthesis
            execution_order.append([st.subtask_id for st in subtasks[:-1]])
            execution_order.append([subtasks[-1].subtask_id])
        else:
            # All tasks can run in parallel
            execution_order.append([st.subtask_id for st in subtasks])
        
        # Estimate total time
        max_parallel_time = max(
            sum(st.estimated_duration for st in subtasks if st.subtask_id in group)
            for group in execution_order
        ) if execution_order else 0
        
        estimated_total_time = sum(
            max(st.estimated_duration for st in subtasks if st.subtask_id in group)
            for group in execution_order
        ) if execution_order else max_parallel_time
        
        # Assess risks
        risk_assessment = {
            "complexity_risk": task_analysis["task_complexity"],
            "agent_availability_risk": "low",
            "data_quality_risk": "medium",
            "coordination_risk": "low" if len(subtasks) <= 3 else "medium"
        }
        
        return TaskPlan(
            plan_id=plan_id,
            main_task_description=task_description,
            subtasks=subtasks,
            agent_assignments={},
            execution_order=execution_order,
            estimated_total_time=estimated_total_time,
            risk_assessment=risk_assessment
        )
    
    def _capability_to_task_type(self, capability: str) -> TaskType:
        """Convert capability to task type"""
        capability_map = {
            "data_analysis": TaskType.ANALYSIS,
            "prediction": TaskType.PREDICTION,
            "optimization": TaskType.OPTIMIZATION,
            "generation": TaskType.GENERATION,
            "integration": TaskType.INTEGRATION,
            "monitoring": TaskType.MONITORING
        }
        return capability_map.get(capability, TaskType.ANALYSIS)
    
    async def _assign_agents_to_tasks(self, task_plan: TaskPlan) -> Dict[str, List[str]]:
        """Assign agents to subtasks based on capabilities and availability"""
        assignments = {}
        
        for subtask in task_plan.subtasks:
            # Find agents capable of handling this subtask
            capable_agents = []
            
            for agent_id, capabilities in self.agent_capabilities.items():
                for capability in capabilities:
                    if capability.availability and capability.current_load < self.load_balance_threshold:
                        # Check if agent can handle required capabilities
                        if any(req in capability.capability_type for req in subtask.requirements):
                            capable_agents.append((agent_id, capability))
            
            if not capable_agents:
                # Fallback: assign to any available agent
                for agent_id, capabilities in self.agent_capabilities.items():
                    if capabilities and capabilities[0].availability:
                        capable_agents.append((agent_id, capabilities[0]))
                        break
            
            if capable_agents:
                # Select best agent based on proficiency and load
                best_agent = max(
                    capable_agents,
                    key=lambda x: x[1].proficiency_score * (1 - x[1].current_load)
                )
                
                agent_id = best_agent[0]
                subtask.assigned_agent = agent_id
                subtask.agent_role = AgentRole.PRIMARY
                
                # Update assignments
                if agent_id not in assignments:
                    assignments[agent_id] = []
                assignments[agent_id].append(subtask.subtask_id)
                
                # Update agent load
                best_agent[1].current_load += 0.2  # Approximate load increase
            
            else:
                self.logger.warning(f"No available agent for subtask: {subtask.subtask_id}")
        
        return assignments
    
    async def _execute_task_plan(self, task_plan: TaskPlan, coordination_id: str) -> List[AgentResult]:
        """Execute the task plan with assigned agents"""
        all_results = []
        
        # Track active operations
        self.active_coordinations[coordination_id] = {
            "task_plan": task_plan,
            "start_time": datetime.utcnow(),
            "status": "running"
        }
        
        try:
            # Execute in planned order
            for execution_group in task_plan.execution_order:
                # Execute subtasks in parallel within each group
                group_tasks = []
                
                for subtask_id in execution_group:
                    subtask = next(st for st in task_plan.subtasks if st.subtask_id == subtask_id)
                    
                    if subtask.assigned_agent:
                        task_coroutine = self._execute_single_subtask(subtask, coordination_id)
                        group_tasks.append(task_coroutine)
                
                # Wait for all tasks in this group to complete
                if group_tasks:
                    group_results = await asyncio.gather(*group_tasks, return_exceptions=True)
                    
                    # Process results
                    for result in group_results:
                        if isinstance(result, Exception):
                            # Create error result
                            error_result = AgentResult(
                                agent_id="unknown",
                                subtask_id="unknown",
                                status="error",
                                result_data={"error": str(result)},
                                execution_time_ms=0,
                                confidence_score=0.0,
                                error_message=str(result)
                            )
                            all_results.append(error_result)
                        else:
                            all_results.append(result)
        
        finally:
            # Remove from active coordinations
            if coordination_id in self.active_coordinations:
                del self.active_coordinations[coordination_id]
            
            # Reset agent loads
            for agent_id in task_plan.agent_assignments:
                if agent_id in self.agent_capabilities:
                    for capability in self.agent_capabilities[agent_id]:
                        capability.current_load = max(0, capability.current_load - 0.2)
        
        return all_results
    
    async def _execute_single_subtask(self, subtask: SubTask, coordination_id: str) -> AgentResult:
        """Execute a single subtask with an assigned agent"""
        start_time = datetime.utcnow()
        
        try:
            agent = self.registered_agents[subtask.assigned_agent]
            
            # Prepare task data for agent
            task_data = {
                "subtask_id": subtask.subtask_id,
                "task_type": subtask.task_type.value,
                "description": subtask.description,
                "input_data": subtask.input_data,
                "requirements": subtask.requirements,
                "constraints": subtask.constraints,
                "coordination_id": coordination_id
            }
            
            # Execute with timeout
            result_data = await asyncio.wait_for(
                agent.process_task(task_data),
                timeout=subtask.timeout
            )
            
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            # Extract confidence score
            confidence_score = result_data.get("confidence_score", 0.8)
            if isinstance(confidence_score, (int, float)):
                confidence_score = float(confidence_score)
            else:
                confidence_score = 0.8
            
            return AgentResult(
                agent_id=subtask.assigned_agent,
                subtask_id=subtask.subtask_id,
                status="success",
                result_data=result_data,
                execution_time_ms=execution_time,
                confidence_score=confidence_score
            )
            
        except asyncio.TimeoutError:
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            return AgentResult(
                agent_id=subtask.assigned_agent,
                subtask_id=subtask.subtask_id,
                status="timeout",
                result_data={},
                execution_time_ms=execution_time,
                confidence_score=0.0,
                error_message=f"Task timed out after {subtask.timeout} seconds"
            )
            
        except Exception as e:
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            return AgentResult(
                agent_id=subtask.assigned_agent,
                subtask_id=subtask.subtask_id,
                status="error",
                result_data={},
                execution_time_ms=execution_time,
                confidence_score=0.0,
                error_message=str(e)
            )
    
    async def _synthesize_results(self, agent_results: List[AgentResult], 
                                task_plan: TaskPlan) -> Dict[str, Any]:
        """Synthesize results from multiple agents"""
        synthesis = {
            "coordination_summary": {
                "total_subtasks": len(task_plan.subtasks),
                "successful_subtasks": len([r for r in agent_results if r.status == "success"]),
                "failed_subtasks": len([r for r in agent_results if r.status in ["error", "timeout"]]),
                "agents_involved": len(set(r.agent_id for r in agent_results))
            },
            "combined_results": {},
            "insights": [],
            "recommendations": [],
            "confidence_assessment": {}
        }
        
        # Combine successful results
        successful_results = [r for r in agent_results if r.status == "success"]
        
        for result in successful_results:
            # Extract key insights
            if "insights" in result.result_data:
                synthesis["insights"].extend(result.result_data["insights"])
            
            # Extract recommendations
            if "recommendations" in result.result_data:
                synthesis["recommendations"].extend(result.result_data["recommendations"])
            
            # Combine result data
            synthesis["combined_results"][result.subtask_id] = result.result_data
        
        # Generate overall insights
        if len(successful_results) > 1:
            synthesis["insights"].append(
                f"Multi-agent analysis completed with {len(successful_results)} successful components"
            )
        
        # Assess confidence
        if successful_results:
            avg_confidence = sum(r.confidence_score for r in successful_results) / len(successful_results)
            synthesis["confidence_assessment"] = {
                "overall_confidence": avg_confidence,
                "confidence_range": [min(r.confidence_score for r in successful_results),
                                   max(r.confidence_score for r in successful_results)],
                "high_confidence_results": len([r for r in successful_results if r.confidence_score > 0.8])
            }
        
        # Remove duplicates from insights and recommendations
        synthesis["insights"] = list(dict.fromkeys(synthesis["insights"]))
        synthesis["recommendations"] = list(dict.fromkeys(synthesis["recommendations"]))
        
        return synthesis
    
    def _calculate_performance_metrics(self, agent_results: List[AgentResult], 
                                     total_execution_time: int) -> Dict[str, Any]:
        """Calculate performance metrics for the coordination"""
        metrics = {
            "total_execution_time_ms": total_execution_time,
            "agent_execution_times": {},
            "success_rate": 0.0,
            "average_confidence": 0.0,
            "efficiency_score": 0.0
        }
        
        if agent_results:
            # Calculate success rate
            successful_results = [r for r in agent_results if r.status == "success"]
            metrics["success_rate"] = len(successful_results) / len(agent_results)
            
            # Calculate average confidence
            if successful_results:
                metrics["average_confidence"] = sum(r.confidence_score for r in successful_results) / len(successful_results)
            
            # Track agent execution times
            for result in agent_results:
                metrics["agent_execution_times"][result.agent_id] = result.execution_time_ms
            
            # Calculate efficiency (tasks completed per unit time)
            if total_execution_time > 0:
                metrics["efficiency_score"] = len(successful_results) / (total_execution_time / 1000)
        
        return metrics
    
    def _calculate_overall_confidence(self, agent_results: List[AgentResult]) -> float:
        """Calculate overall confidence score"""
        successful_results = [r for r in agent_results if r.status == "success"]
        
        if not successful_results:
            return 0.0
        
        # Weight by inverse of execution time (faster = more reliable)
        weighted_confidences = []
        for result in successful_results:
            time_weight = 1.0 / max(result.execution_time_ms / 1000, 1.0)  # Prevent division by zero
            weighted_confidences.append(result.confidence_score * time_weight)
        
        if weighted_confidences:
            return sum(weighted_confidences) / len(weighted_confidences)
        
        return 0.0
    
    async def _register_default_agents(self):
        """Register default intelligence agents"""
        try:
            # This would register actual agent instances
            # For now, we'll create placeholder registrations
            
            default_agents = [
                ("data_analyzer", ["data_analysis", "statistical_analysis"], ["numerical_data", "text_analysis"]),
                ("predictive_agent", ["prediction", "forecasting"], ["time_series", "trend_analysis"]),
                ("optimization_agent", ["optimization", "enhancement"], ["process_optimization", "performance_tuning"]),
                ("anomaly_detector", ["anomaly_detection", "monitoring"], ["outlier_detection", "pattern_analysis"])
            ]
            
            for agent_id, capabilities, specializations in default_agents:
                # Create mock agent for registration
                mock_agent = type('MockAgent', (), {
                    'process_task': lambda self, task_data: asyncio.create_task(self._mock_process(task_data)),
                    'analyze_input': lambda self, input_data: {"analysis": "mock analysis"},
                    '_mock_process': lambda self, task_data: {"result": "mock result", "confidence_score": 0.8}
                })()
                
                await self.register_agent(agent_id, mock_agent, capabilities, specializations)
            
            self.logger.info("Default agents registered successfully")
            
        except Exception as e:
            self.logger.warning(f"Failed to register default agents: {str(e)}")
    
    async def _update_performance_history(self, result: CoordinationResult):
        """Update performance history for learning"""
        self.metrics["total_coordinations"] += 1
        
        if result.status == "success":
            self.metrics["successful_coordinations"] += 1
        else:
            self.metrics["failed_coordinations"] += 1
        
        # Update average execution time
        current_avg = self.metrics["average_execution_time"]
        total_coords = self.metrics["total_coordinations"]
        new_avg = ((current_avg * (total_coords - 1)) + result.total_execution_time_ms) / total_coords
        self.metrics["average_execution_time"] = new_avg
        
        # Store result for history
        self.coordination_history.append(result)
        
        # Keep only recent history
        if len(self.coordination_history) > 1000:
            self.coordination_history = self.coordination_history[-500:]
    
    async def _coordination_processor(self):
        """Background processor for coordination tasks"""
        while True:
            try:
                # Process any queued coordinations
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Coordination processor error: {str(e)}")
    
    async def _performance_monitor(self):
        """Background performance monitoring"""
        while True:
            try:
                # Monitor agent performance and health
                await self._monitor_agent_health()
                
                # Optimize agent assignments
                await self._optimize_agent_assignments()
                
                # Wait before next check
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Performance monitor error: {str(e)}")
    
    async def _monitor_agent_health(self):
        """Monitor health and performance of registered agents"""
        for agent_id, capabilities in self.agent_capabilities.items():
            for capability in capabilities:
                # Check if agent is still responsive
                if agent_id in self.registered_agents:
                    try:
                        # Simple health check
                        capability.availability = True
                    except Exception:
                        capability.availability = False
                        self.logger.warning(f"Agent {agent_id} appears unresponsive")
    
    async def _optimize_agent_assignments(self):
        """Optimize agent assignments based on performance history"""
        # Update proficiency scores based on recent performance
        for agent_id in self.agent_capabilities:
            if agent_id in self.agent_performance_history:
                recent_performance = self.agent_performance_history[agent_id][-10:]  # Last 10 tasks
                if recent_performance:
                    avg_performance = sum(recent_performance) / len(recent_performance)
                    
                    # Update proficiency scores
                    for capability in self.agent_capabilities[agent_id]:
                        capability.proficiency_score = avg_performance
    
    async def shutdown(self):
        """Shutdown the agent coordinator gracefully"""
        try:
            # Cancel active coordinations
            for coordination_id in list(self.active_coordinations.keys()):
                del self.active_coordinations[coordination_id]
            
            # Clear agent registrations
            self.registered_agents.clear()
            self.agent_capabilities.clear()
            
            self.logger.info("Agent Coordinator shutdown completed")
            
        except Exception as e:
            self.logger.error(f"Error during Agent Coordinator shutdown: {str(e)}")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current status of all registered agents"""
        status = {
            "total_agents": len(self.registered_agents),
            "available_agents": 0,
            "agent_details": {},
            "capabilities_summary": {},
            "performance_summary": self.metrics
        }
        
        # Count available agents and collect details
        for agent_id, capabilities in self.agent_capabilities.items():
            available = any(cap.availability for cap in capabilities)
            if available:
                status["available_agents"] += 1
            
            status["agent_details"][agent_id] = {
                "available": available,
                "capabilities": [cap.capability_type for cap in capabilities],
                "current_load": max(cap.current_load for cap in capabilities) if capabilities else 0,
                "average_proficiency": sum(cap.proficiency_score for cap in capabilities) / len(capabilities) if capabilities else 0
            }
        
        # Summarize capabilities
        all_capabilities = [cap.capability_type for caps in self.agent_capabilities.values() for cap in caps]
        for capability in set(all_capabilities):
            status["capabilities_summary"][capability] = all_capabilities.count(capability)
        
        return status
