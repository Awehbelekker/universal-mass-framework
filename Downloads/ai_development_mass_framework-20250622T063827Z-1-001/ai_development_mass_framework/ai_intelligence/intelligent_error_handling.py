"""
Intelligent Error Handling & AI Suggestions System
Provides smart error resolution and proactive AI-powered suggestions
"""

from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import re
from enum import Enum
import logging
import traceback
from collections import Counter, defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ErrorCategory(Enum):
    SYNTAX = "syntax_error"
    RUNTIME = "runtime_error"
    LOGIC = "logic_error"
    PERFORMANCE = "performance_issue"
    SECURITY = "security_issue"
    USABILITY = "usability_issue"
    INTEGRATION = "integration_error"
    CONFIGURATION = "configuration_error"

class SuggestionType(Enum):
    ERROR_FIX = "error_fix"
    OPTIMIZATION = "optimization"
    BEST_PRACTICE = "best_practice"
    FEATURE_ENHANCEMENT = "feature_enhancement"
    LEARNING_OPPORTUNITY = "learning_opportunity"
    WORKFLOW_IMPROVEMENT = "workflow_improvement"

class SuggestionPriority(Enum):
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    BACKGROUND = "background"

@dataclass
class ErrorContext:
    error_id: str
    timestamp: datetime
    user_id: str
    error_type: str
    error_message: str
    stack_trace: Optional[str]
    category: ErrorCategory
    severity: ErrorSeverity
    context_data: Dict[str, Any]
    user_action: Optional[str] = None
    environment: Dict[str, Any] = field(default_factory=dict)
    resolution_attempts: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class AISuggestion:
    suggestion_id: str
    suggestion_type: SuggestionType
    priority: SuggestionPriority
    title: str
    description: str
    action_items: List[Dict[str, Any]]
    confidence_score: float
    expected_impact: str
    implementation_complexity: str
    learning_resources: List[Dict[str, Any]] = field(default_factory=list)
    success_criteria: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class ResolutionStrategy:
    strategy_id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]
    success_rate: float
    average_resolution_time: int  # in seconds
    applicable_categories: List[ErrorCategory]
    prerequisites: List[str] = field(default_factory=list)

class IntelligentErrorHandler:
    """Advanced AI-powered error handling and suggestion system"""
    
    def __init__(self):
        self.error_patterns: Dict[str, Dict[str, Any]] = {}
        self.resolution_strategies: Dict[str, ResolutionStrategy] = {}
        self.user_error_history: Dict[str, List[ErrorContext]] = defaultdict(list)
        self.suggestion_effectiveness: Dict[str, float] = {}
        self.ai_models: Dict[str, Any] = {}
        self._initialize_error_patterns()
        self._initialize_resolution_strategies()
        self._initialize_ai_models()
    
    def _initialize_error_patterns(self):
        """Initialize common error patterns and their characteristics"""
        self.error_patterns = {
            "syntax_errors": {
                "patterns": [
                    r"SyntaxError.*unexpected token",
                    r"IndentationError.*expected an indented block",
                    r"NameError.*name '.*' is not defined",
                    r"TypeError.*missing \d+ required positional argument"
                ],
                "category": ErrorCategory.SYNTAX,
                "severity": ErrorSeverity.HIGH,
                "common_causes": [
                    "Missing parentheses or brackets",
                    "Incorrect indentation",
                    "Undefined variables",
                    "Missing function arguments"
                ],
                "quick_fixes": [
                    "Check syntax highlighting",
                    "Verify indentation consistency",
                    "Check variable definitions",
                    "Verify function signatures"
                ]
            },
            "runtime_errors": {
                "patterns": [
                    r"AttributeError.*object has no attribute",
                    r"KeyError.*",
                    r"IndexError.*list index out of range",
                    r"ValueError.*invalid literal for.*with base"
                ],
                "category": ErrorCategory.RUNTIME,
                "severity": ErrorSeverity.MEDIUM,
                "common_causes": [
                    "Accessing non-existent attributes",
                    "Missing dictionary keys",
                    "Array bounds violations",
                    "Type conversion errors"
                ],
                "quick_fixes": [
                    "Add attribute/key existence checks",
                    "Validate array indices",
                    "Add type validation",
                    "Use try-catch blocks"
                ]
            },
            "performance_issues": {
                "patterns": [
                    r"TimeoutError.*",
                    r"MemoryError.*",
                    r"RecursionError.*maximum recursion depth"
                ],
                "category": ErrorCategory.PERFORMANCE,
                "severity": ErrorSeverity.HIGH,
                "common_causes": [
                    "Slow network requests",
                    "Memory leaks",
                    "Infinite recursion",
                    "Inefficient algorithms"
                ],
                "quick_fixes": [
                    "Add timeout handling",
                    "Optimize memory usage",
                    "Add recursion limits",
                    "Profile and optimize code"
                ]
            },
            "integration_errors": {
                "patterns": [
                    r"ConnectionError.*",
                    r"AuthenticationError.*",
                    r"API.*rate limit",
                    r"SSL.*certificate verify failed"
                ],
                "category": ErrorCategory.INTEGRATION,
                "severity": ErrorSeverity.HIGH,
                "common_causes": [
                    "Network connectivity issues",
                    "Invalid credentials",
                    "API rate limiting",
                    "SSL certificate problems"
                ],
                "quick_fixes": [
                    "Check network connectivity",
                    "Verify API credentials",
                    "Implement rate limiting",
                    "Update certificates"
                ]
            }
        }
    
    def _initialize_resolution_strategies(self):
        """Initialize resolution strategies for different error types"""
        self.resolution_strategies = {
            "syntax_debugging": ResolutionStrategy(
                strategy_id="syntax_debugging",
                name="Syntax Error Resolution",
                description="Step-by-step syntax error debugging",
                steps=[
                    {
                        "step": 1,
                        "action": "Identify error location",
                        "description": "Find the exact line and character where the error occurs",
                        "tools": ["syntax_highlighter", "error_locator"]
                    },
                    {
                        "step": 2,
                        "action": "Check common syntax issues",
                        "description": "Look for missing parentheses, brackets, or semicolons",
                        "tools": ["syntax_checker", "bracket_matcher"]
                    },
                    {
                        "step": 3,
                        "action": "Verify indentation",
                        "description": "Ensure consistent indentation throughout the code",
                        "tools": ["indentation_checker", "whitespace_visualizer"]
                    },
                    {
                        "step": 4,
                        "action": "Test the fix",
                        "description": "Run the code to verify the syntax error is resolved",
                        "tools": ["code_runner", "syntax_validator"]
                    }
                ],
                success_rate=0.92,
                average_resolution_time=180,
                applicable_categories=[ErrorCategory.SYNTAX]
            ),
            "runtime_debugging": ResolutionStrategy(
                strategy_id="runtime_debugging",
                name="Runtime Error Resolution",
                description="Comprehensive runtime error debugging process",
                steps=[
                    {
                        "step": 1,
                        "action": "Analyze stack trace",
                        "description": "Examine the full stack trace to understand the error flow",
                        "tools": ["stack_analyzer", "call_graph_viewer"]
                    },
                    {
                        "step": 2,
                        "action": "Add debug logging",
                        "description": "Insert logging statements to track variable values",
                        "tools": ["debug_logger", "variable_inspector"]
                    },
                    {
                        "step": 3,
                        "action": "Check data validity",
                        "description": "Verify that all data inputs are valid and expected",
                        "tools": ["data_validator", "type_checker"]
                    },
                    {
                        "step": 4,
                        "action": "Implement error handling",
                        "description": "Add appropriate try-catch blocks and error handling",
                        "tools": ["exception_handler", "error_boundary"]
                    }
                ],
                success_rate=0.85,
                average_resolution_time=300,
                applicable_categories=[ErrorCategory.RUNTIME, ErrorCategory.LOGIC]
            ),
            "performance_optimization": ResolutionStrategy(
                strategy_id="performance_optimization",
                name="Performance Issue Resolution",
                description="Systematic performance problem solving",
                steps=[
                    {
                        "step": 1,
                        "action": "Profile the application",
                        "description": "Use profiling tools to identify bottlenecks",
                        "tools": ["performance_profiler", "memory_analyzer"]
                    },
                    {
                        "step": 2,
                        "action": "Optimize critical paths",
                        "description": "Focus on the most time-consuming operations",
                        "tools": ["code_optimizer", "algorithm_analyzer"]
                    },
                    {
                        "step": 3,
                        "action": "Implement caching",
                        "description": "Add caching for frequently accessed data",
                        "tools": ["cache_manager", "memoization_helper"]
                    },
                    {
                        "step": 4,
                        "action": "Monitor improvements",
                        "description": "Measure performance gains after optimization",
                        "tools": ["performance_monitor", "benchmark_runner"]
                    }
                ],
                success_rate=0.75,
                average_resolution_time=600,
                applicable_categories=[ErrorCategory.PERFORMANCE]
            )
        }
    
    def _initialize_ai_models(self):
        """Initialize AI models for error analysis and suggestions"""
        self.ai_models = {
            "error_classifier": {
                "model_type": "text_classification",
                "accuracy": 0.89,
                "categories": [cat.value for cat in ErrorCategory]
            },
            "similarity_matcher": {
                "model_type": "semantic_similarity",
                "threshold": 0.75,
                "embedding_dimension": 384
            },
            "suggestion_generator": {
                "model_type": "text_generation",
                "context_window": 2048,
                "temperature": 0.3
            },
            "resolution_predictor": {
                "model_type": "success_prediction",
                "features": ["error_category", "user_skill", "context_complexity"],
                "accuracy": 0.82
            }
        }
    
    async def handle_error(self, error_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main error handling function with AI-powered analysis"""
        try:
            # Create error context
            error_context = self._create_error_context(error_data)
            
            # Classify and analyze the error
            classification = await self._classify_error(error_context)
            
            # Find similar past errors
            similar_errors = self._find_similar_errors(error_context)
            
            # Generate AI-powered suggestions
            suggestions = await self._generate_ai_suggestions(error_context, classification, similar_errors)
            
            # Select best resolution strategy
            resolution_strategy = self._select_resolution_strategy(error_context, classification)
            
            # Create comprehensive response
            response = {
                "error_id": error_context.error_id,
                "classification": classification,
                "severity": error_context.severity.value,
                "category": error_context.category.value,
                "ai_suggestions": [suggestion.__dict__ for suggestion in suggestions],
                "resolution_strategy": resolution_strategy.__dict__ if resolution_strategy else None,
                "similar_cases": len(similar_errors),
                "estimated_resolution_time": self._estimate_resolution_time(error_context, resolution_strategy),
                "learning_opportunities": self._identify_learning_opportunities(error_context),
                "prevention_tips": self._generate_prevention_tips(error_context)
            }
            
            # Store error for learning
            self._store_error_context(error_context)
            
            logger.info(f"Handled error {error_context.error_id} with {len(suggestions)} suggestions")
            return response
            
        except Exception as e:
            logger.error(f"Error in error handling: {e}")
            return {
                "error": "Failed to process error",
                "details": str(e),
                "fallback_suggestions": self._get_fallback_suggestions()
            }
    
    async def generate_proactive_suggestions(self, user_id: str, context: Dict[str, Any]) -> List[AISuggestion]:
        """Generate proactive suggestions based on user activity"""
        try:
            # Analyze user patterns
            user_patterns = self._analyze_user_patterns(user_id)
            
            # Identify potential issues
            potential_issues = self._identify_potential_issues(context, user_patterns)
            
            # Generate suggestions
            suggestions = []
            
            # Code quality suggestions
            if context.get("code_complexity", 0) > 10:
                suggestions.append(AISuggestion(
                    suggestion_id=f"complexity_reduction_{datetime.now().timestamp()}",
                    suggestion_type=SuggestionType.OPTIMIZATION,
                    priority=SuggestionPriority.MEDIUM,
                    title="Reduce Code Complexity",
                    description="Your code complexity is high. Consider breaking it into smaller functions.",
                    action_items=[
                        {
                            "action": "Extract functions",
                            "description": "Break large functions into smaller, focused ones",
                            "difficulty": "medium"
                        },
                        {
                            "action": "Use design patterns",
                            "description": "Apply appropriate design patterns to simplify structure",
                            "difficulty": "advanced"
                        }
                    ],
                    confidence_score=0.85,
                    expected_impact="30-50% improvement in maintainability",
                    implementation_complexity="medium"
                ))
            
            # Performance suggestions
            if context.get("response_time", 0) > 2000:
                suggestions.append(AISuggestion(
                    suggestion_id=f"performance_improvement_{datetime.now().timestamp()}",
                    suggestion_type=SuggestionType.OPTIMIZATION,
                    priority=SuggestionPriority.HIGH,
                    title="Improve Response Time",
                    description="Response times are slower than optimal. Here are some improvements.",
                    action_items=[
                        {
                            "action": "Add caching",
                            "description": "Implement caching for frequently accessed data",
                            "difficulty": "medium"
                        },
                        {
                            "action": "Optimize queries",
                            "description": "Review and optimize database queries",
                            "difficulty": "advanced"
                        }
                    ],
                    confidence_score=0.78,
                    expected_impact="40-60% faster response times",
                    implementation_complexity="medium"
                ))
            
            # Security suggestions
            security_issues = self._check_security_patterns(context)
            if security_issues:
                suggestions.append(AISuggestion(
                    suggestion_id=f"security_enhancement_{datetime.now().timestamp()}",
                    suggestion_type=SuggestionType.BEST_PRACTICE,
                    priority=SuggestionPriority.HIGH,
                    title="Security Enhancement Opportunities",
                    description="Potential security improvements identified in your application.",
                    action_items=[
                        {
                            "action": "Input validation",
                            "description": "Add comprehensive input validation",
                            "difficulty": "beginner"
                        },
                        {
                            "action": "Authentication review",
                            "description": "Review authentication mechanisms",
                            "difficulty": "intermediate"
                        }
                    ],
                    confidence_score=0.92,
                    expected_impact="Significantly improved security posture",
                    implementation_complexity="medium"
                ))
            
            # Learning suggestions
            if len(user_patterns.get("learning_opportunities", [])) > 0:
                suggestions.append(AISuggestion(
                    suggestion_id=f"learning_opportunity_{datetime.now().timestamp()}",
                    suggestion_type=SuggestionType.LEARNING_OPPORTUNITY,
                    priority=SuggestionPriority.LOW,
                    title="Expand Your Skills",
                    description="Based on your activity, here are some learning opportunities.",
                    action_items=[
                        {
                            "action": "Complete tutorial",
                            "description": "Try our advanced features tutorial",
                            "difficulty": "intermediate"
                        },
                        {
                            "action": "Join community",
                            "description": "Connect with other developers in our community",
                            "difficulty": "beginner"
                        }
                    ],
                    confidence_score=0.65,
                    expected_impact="Enhanced skills and productivity",
                    implementation_complexity="low",
                    learning_resources=[
                        {
                            "type": "tutorial",
                            "title": "Advanced Development Techniques",
                            "url": "/tutorials/advanced"
                        },
                        {
                            "type": "community",
                            "title": "Developer Community",
                            "url": "/community"
                        }
                    ]
                ))
            
            logger.info(f"Generated {len(suggestions)} proactive suggestions for user {user_id}")
            return suggestions
            
        except Exception as e:
            logger.error(f"Error generating proactive suggestions: {e}")
            return []
    
    async def provide_contextual_help(self, error_context: ErrorContext, user_request: str) -> Dict[str, Any]:
        """Provide contextual help for specific error situations"""
        try:
            # Analyze user request
            request_analysis = self._analyze_help_request(user_request, error_context)
            
            # Generate contextual response
            help_response = await self._generate_contextual_response(request_analysis, error_context)
            
            # Add interactive elements
            interactive_elements = self._create_interactive_elements(error_context, request_analysis)
            
            # Provide step-by-step guidance
            step_by_step = self._create_step_by_step_guidance(error_context, request_analysis)
            
            return {
                "response": help_response,
                "interactive_elements": interactive_elements,
                "step_by_step_guidance": step_by_step,
                "confidence": request_analysis.get("confidence", 0.7),
                "additional_resources": self._get_contextual_resources(error_context),
                "escalation_options": self._get_escalation_options(error_context)            }
            
        except Exception as e:
            logger.error(f"Error providing contextual help: {e}")
            return {"error": "Failed to provide contextual help", "details": str(e)}
    
    def track_resolution_success(self, error_id: str, resolution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track the success of error resolution attempts"""
        try:
            success = resolution_data.get("success", False)
            resolution_time = resolution_data.get("resolution_time", 0)
            strategy_used = resolution_data.get("strategy_id")
            user_feedback = resolution_data.get("user_feedback", {})
            
            # Update strategy effectiveness
            if strategy_used and strategy_used in self.resolution_strategies:
                strategy = self.resolution_strategies[strategy_used]
                alpha = 0.1  # Define alpha here
                if success:
                    # Update success rate with exponential smoothing
                    strategy.success_rate = (1 - alpha) * strategy.success_rate + alpha * 1.0
                    # Update average resolution time
                    strategy.average_resolution_time = int(
                        (1 - alpha) * strategy.average_resolution_time + alpha * resolution_time
                    )
                else:
                    strategy.success_rate = (1 - alpha) * strategy.success_rate + alpha * 0.0
            
            # Update suggestion effectiveness
            alpha = 0.2  # Define alpha for suggestions
            suggestions_used = resolution_data.get("suggestions_used", [])
            for suggestion_id in suggestions_used:
                if suggestion_id in self.suggestion_effectiveness:
                    current_score = self.suggestion_effectiveness[suggestion_id]
                    new_score = 1.0 if success else 0.0
                    self.suggestion_effectiveness[suggestion_id] = (
                        0.8 * current_score + 0.2 * new_score
                    )
                else:
                    self.suggestion_effectiveness[suggestion_id] = 1.0 if success else 0.0
            
            # Generate insights
            insights = {
                "resolution_successful": success,
                "time_taken": resolution_time,
                "strategy_effectiveness": strategy.success_rate if strategy_used and strategy_used in self.resolution_strategies else None,
                "suggestions_effectiveness": {
                    sid: self.suggestion_effectiveness.get(sid, 0.0) 
                    for sid in suggestions_used
                },
                "user_satisfaction": user_feedback.get("satisfaction_score", 0),
                "improvement_areas": self._identify_improvement_areas(resolution_data)
            }
            
            logger.info(f"Tracked resolution for error {error_id}: success={success}")
            return insights
            
        except Exception as e:
            logger.error(f"Error tracking resolution success: {e}")
            return {"error": "Failed to track resolution", "details": str(e)}
    
    def _create_error_context(self, error_data: Dict[str, Any]) -> ErrorContext:
        """Create structured error context from raw error data"""
        return ErrorContext(
            error_id=error_data.get("error_id", f"error_{datetime.now().timestamp()}"),
            timestamp=datetime.now(),
            user_id=error_data.get("user_id", "unknown"),
            error_type=error_data.get("error_type", "UnknownError"),
            error_message=error_data.get("error_message", ""),
            stack_trace=error_data.get("stack_trace"),
            category=self._categorize_error(error_data),
            severity=self._assess_severity(error_data),
            context_data=error_data.get("context", {}),
            user_action=error_data.get("user_action"),
            environment=error_data.get("environment", {})
        )
    
    def _categorize_error(self, error_data: Dict[str, Any]) -> ErrorCategory:
        """Categorize error based on type and message"""
        error_message = error_data.get("error_message", "").lower()
        error_type = error_data.get("error_type", "").lower()
        
        # Pattern matching for categorization
        for pattern_group, details in self.error_patterns.items():
            for pattern in details["patterns"]:
                if re.search(pattern.lower(), error_message) or re.search(pattern.lower(), error_type):
                    return details["category"]
        
        # Default categorization based on common keywords
        if any(keyword in error_message for keyword in ["syntax", "indentation", "unexpected"]):
            return ErrorCategory.SYNTAX
        elif any(keyword in error_message for keyword in ["timeout", "memory", "performance"]):
            return ErrorCategory.PERFORMANCE
        elif any(keyword in error_message for keyword in ["connection", "authentication", "api"]):
            return ErrorCategory.INTEGRATION
        else:
            return ErrorCategory.RUNTIME
    
    def _assess_severity(self, error_data: Dict[str, Any]) -> ErrorSeverity:
        """Assess error severity based on impact and context"""
        # Check for critical keywords
        error_message = error_data.get("error_message", "").lower()
        if any(keyword in error_message for keyword in ["critical", "fatal", "crash", "security"]):
            return ErrorSeverity.CRITICAL
        
        # Check context for severity indicators
        context = error_data.get("context", {})
        if context.get("production_environment", False):
            return ErrorSeverity.HIGH
        elif context.get("affects_multiple_users", False):
            return ErrorSeverity.HIGH
        elif any(keyword in error_message for keyword in ["warning", "deprecated"]):
            return ErrorSeverity.LOW
        else:
            return ErrorSeverity.MEDIUM
    
    async def _classify_error(self, error_context: ErrorContext) -> Dict[str, Any]:
        """Use AI to classify and analyze the error"""
        classification = {
            "primary_category": error_context.category.value,
            "confidence": 0.8,
            "subcategories": [],
            "root_cause_analysis": {},
            "impact_assessment": {}
        }
        
        # Analyze error message for patterns
        error_message = error_context.error_message.lower()
        
        # Root cause analysis
        if "undefined" in error_message or "not defined" in error_message:
            classification["root_cause_analysis"]["primary_cause"] = "undefined_variable"
            classification["root_cause_analysis"]["likelihood"] = 0.9
        elif "null" in error_message or "none" in error_message:
            classification["root_cause_analysis"]["primary_cause"] = "null_reference"
            classification["root_cause_analysis"]["likelihood"] = 0.85
        elif "timeout" in error_message:
            classification["root_cause_analysis"]["primary_cause"] = "network_timeout"
            classification["root_cause_analysis"]["likelihood"] = 0.8
        
        # Impact assessment
        if error_context.severity == ErrorSeverity.CRITICAL:
            classification["impact_assessment"] = {
                "user_impact": "high",
                "business_impact": "critical",
                "urgency": "immediate"
            }
        elif error_context.severity == ErrorSeverity.HIGH:
            classification["impact_assessment"] = {
                "user_impact": "medium",
                "business_impact": "high",
                "urgency": "within_hours"
            }
        else:
            classification["impact_assessment"] = {
                "user_impact": "low",
                "business_impact": "low",
                "urgency": "next_sprint"
            }
        
        return classification
    
    def _find_similar_errors(self, error_context: ErrorContext) -> List[ErrorContext]:
        """Find similar errors from history"""
        similar_errors = []
        
        for user_id, error_history in self.user_error_history.items():
            for past_error in error_history:
                similarity_score = self._calculate_error_similarity(error_context, past_error)
                if similarity_score > 0.7:
                    similar_errors.append(past_error)
        
        return sorted(similar_errors, key=lambda e: self._calculate_error_similarity(error_context, e), reverse=True)[:5]
    
    def _calculate_error_similarity(self, error1: ErrorContext, error2: ErrorContext) -> float:
        """Calculate similarity between two errors"""
        # Simple similarity based on error type and category
        type_similarity = 1.0 if error1.error_type == error2.error_type else 0.0
        category_similarity = 1.0 if error1.category == error2.category else 0.0
        
        # Message similarity (simplified)
        message_words1 = set(error1.error_message.lower().split())
        message_words2 = set(error2.error_message.lower().split())
        
        if len(message_words1) == 0 and len(message_words2) == 0:
            message_similarity = 1.0
        elif len(message_words1) == 0 or len(message_words2) == 0:
            message_similarity = 0.0
        else:
            intersection = len(message_words1.intersection(message_words2))
            union = len(message_words1.union(message_words2))
            message_similarity = intersection / union if union > 0 else 0.0
        
        # Weighted average
        return 0.4 * type_similarity + 0.3 * category_similarity + 0.3 * message_similarity
    
    async def _generate_ai_suggestions(self, error_context: ErrorContext, classification: Dict[str, Any], similar_errors: List[ErrorContext]) -> List[AISuggestion]:
        """Generate AI-powered suggestions for error resolution"""
        suggestions = []
        
        # Generate suggestions based on error category
        if error_context.category == ErrorCategory.SYNTAX:
            suggestions.append(AISuggestion(
                suggestion_id=f"syntax_fix_{error_context.error_id}",
                suggestion_type=SuggestionType.ERROR_FIX,
                priority=SuggestionPriority.HIGH,
                title="Fix Syntax Error",
                description="Identify and fix the syntax error in your code",
                action_items=[
                    {
                        "action": "Check line " + str(self._extract_line_number(error_context.error_message)),
                        "description": "Review the syntax at the specified line",
                        "tools": ["syntax_highlighter"]
                    },
                    {
                        "action": "Validate brackets and parentheses",
                        "description": "Ensure all brackets and parentheses are properly closed",
                        "tools": ["bracket_matcher"]
                    }
                ],
                confidence_score=0.9,
                expected_impact="Immediate error resolution",
                implementation_complexity="low"
            ))
        
        elif error_context.category == ErrorCategory.RUNTIME:
            suggestions.append(AISuggestion(
                suggestion_id=f"runtime_fix_{error_context.error_id}",
                suggestion_type=SuggestionType.ERROR_FIX,
                priority=SuggestionPriority.HIGH,
                title="Resolve Runtime Error",
                description="Add proper error handling to prevent runtime errors",
                action_items=[
                    {
                        "action": "Add try-catch block",
                        "description": "Wrap risky code in appropriate error handling",
                        "tools": ["error_handler_generator"]
                    },
                    {
                        "action": "Validate inputs",
                        "description": "Add input validation before processing",
                        "tools": ["input_validator"]
                    }
                ],
                confidence_score=0.85,
                expected_impact="Prevents future runtime errors",
                implementation_complexity="medium"
            ))
        
        elif error_context.category == ErrorCategory.PERFORMANCE:
            suggestions.append(AISuggestion(
                suggestion_id=f"performance_fix_{error_context.error_id}",
                suggestion_type=SuggestionType.OPTIMIZATION,
                priority=SuggestionPriority.MEDIUM,
                title="Optimize Performance",
                description="Improve application performance to prevent timeouts",
                action_items=[
                    {
                        "action": "Profile the code",
                        "description": "Use profiling tools to identify bottlenecks",
                        "tools": ["performance_profiler"]
                    },
                    {
                        "action": "Optimize algorithms",
                        "description": "Review and optimize slow algorithms",
                        "tools": ["algorithm_analyzer"]
                    }
                ],
                confidence_score=0.75,
                expected_impact="Faster execution and fewer timeouts",
                implementation_complexity="high"
            ))
        
        # Add suggestions based on similar errors
        if similar_errors:
            successful_resolutions = [e for e in similar_errors if len(e.resolution_attempts) > 0]
            if successful_resolutions:
                suggestions.append(AISuggestion(
                    suggestion_id=f"similar_resolution_{error_context.error_id}",
                    suggestion_type=SuggestionType.ERROR_FIX,
                    priority=SuggestionPriority.MEDIUM,
                    title="Try Previous Successful Resolution",
                    description="Based on similar errors, this approach was successful before",
                    action_items=[
                        {
                            "action": "Apply similar solution",
                            "description": f"Try the approach that worked for {len(successful_resolutions)} similar cases",
                            "success_rate": f"{len(successful_resolutions)}/{len(similar_errors)}"
                        }
                    ],
                    confidence_score=0.7,
                    expected_impact="High probability of success based on history",
                    implementation_complexity="medium"
                ))
        
        # Add learning opportunity
        suggestions.append(AISuggestion(
            suggestion_id=f"learning_opportunity_{error_context.error_id}",
            suggestion_type=SuggestionType.LEARNING_OPPORTUNITY,
            priority=SuggestionPriority.LOW,
            title="Learn from This Error",
            description="Turn this error into a learning opportunity",
            action_items=[
                {
                    "action": "Read documentation",
                    "description": f"Learn more about {error_context.category.value} errors",
                    "resources": ["official_docs", "tutorials"]
                },
                {
                    "action": "Practice prevention",
                    "description": "Learn techniques to prevent similar errors",
                    "resources": ["best_practices", "code_examples"]
                }
            ],
            confidence_score=0.6,
            expected_impact="Improved skills and fewer future errors",
            implementation_complexity="low",
            learning_resources=[
                {
                    "type": "documentation",
                    "title": f"{error_context.category.value.title()} Error Guide",
                    "url": f"/docs/errors/{error_context.category.value}"
                },
                {
                    "type": "tutorial",
                    "title": "Error Prevention Best Practices",
                    "url": "/tutorials/error-prevention"
                }
            ]
        ))
        
        return suggestions
    
    def _select_resolution_strategy(self, error_context: ErrorContext, classification: Dict[str, Any]) -> Optional[ResolutionStrategy]:
        """Select the best resolution strategy for the error"""
        applicable_strategies = [
            strategy for strategy in self.resolution_strategies.values()
            if error_context.category in strategy.applicable_categories
        ]
        
        if not applicable_strategies:
            return None
        
        # Select strategy with highest success rate
        return max(applicable_strategies, key=lambda s: s.success_rate)
    
    def _estimate_resolution_time(self, error_context: ErrorContext, strategy: Optional[ResolutionStrategy]) -> int:
        """Estimate time to resolve the error"""
        if strategy:
            base_time = strategy.average_resolution_time
        else:
            base_time = 300  # Default 5 minutes
        
        # Adjust based on error complexity
        complexity_factor = 1.0
        if error_context.severity == ErrorSeverity.CRITICAL:
            complexity_factor = 2.0
        elif error_context.severity == ErrorSeverity.HIGH:
            complexity_factor = 1.5
        
        return int(base_time * complexity_factor)
    
    def _identify_learning_opportunities(self, error_context: ErrorContext) -> List[Dict[str, Any]]:
        """Identify learning opportunities from the error"""
        opportunities = []
        
        category_learning = {
            ErrorCategory.SYNTAX: {
                "topic": "Code Syntax Best Practices",
                "resources": ["syntax_guide", "linting_tools"],
                "difficulty": "beginner"
            },
            ErrorCategory.RUNTIME: {
                "topic": "Error Handling and Defensive Programming",
                "resources": ["error_handling_guide", "testing_strategies"],
                "difficulty": "intermediate"
            },
            ErrorCategory.PERFORMANCE: {
                "topic": "Performance Optimization Techniques",
                "resources": ["profiling_guide", "optimization_patterns"],
                "difficulty": "advanced"
            },
            ErrorCategory.SECURITY: {
                "topic": "Security Best Practices",
                "resources": ["security_guide", "vulnerability_assessment"],
                "difficulty": "intermediate"
            }
        }
        
        if error_context.category in category_learning:
            opportunities.append(category_learning[error_context.category])
        
        return opportunities
    
    def _generate_prevention_tips(self, error_context: ErrorContext) -> List[str]:
        """Generate tips to prevent similar errors in the future"""
        prevention_tips = []
        
        category_tips = {
            ErrorCategory.SYNTAX: [
                "Use a code editor with syntax highlighting",
                "Enable automatic indentation",
                "Use linting tools to catch syntax errors early",
                "Practice consistent code formatting"
            ],
            ErrorCategory.RUNTIME: [
                "Add input validation to all functions",
                "Use try-catch blocks for risky operations",
                "Test edge cases thoroughly",
                "Implement proper error logging"
            ],
            ErrorCategory.PERFORMANCE: [
                "Profile your code regularly",
                "Implement caching for expensive operations",
                "Use efficient algorithms and data structures",
                "Monitor performance in production"
            ],
            ErrorCategory.INTEGRATION: [
                "Implement proper retry logic",
                "Add timeout handling for external calls",
                "Use circuit breakers for unreliable services",
                "Test integrations thoroughly"
            ]
        }
        
        return category_tips.get(error_context.category, [
            "Write comprehensive tests",
            "Use version control effectively",
            "Follow coding best practices",
            "Regularly review and refactor code"
        ])
    
    def _analyze_user_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user error patterns for insights"""
        user_errors = self.user_error_history.get(user_id, [])
        
        if not user_errors:
            return {"learning_opportunities": [], "common_issues": []}
        
        # Analyze error frequency by category
        error_categories = [error.category for error in user_errors]
        category_counts = Counter(error_categories)
        
        # Identify learning opportunities
        learning_opportunities = []
        for category, count in category_counts.most_common(3):
            if count >= 3:  # User has had this type of error multiple times
                learning_opportunities.append(category.value)
        
        return {
            "total_errors": len(user_errors),
            "common_categories": [cat.value for cat, _ in category_counts.most_common(3)],
            "learning_opportunities": learning_opportunities,
            "improvement_trend": self._calculate_improvement_trend(user_errors)
        }
    
    def _identify_potential_issues(self, context: Dict[str, Any], user_patterns: Dict[str, Any]) -> List[str]:
        """Identify potential issues before they become errors"""
        potential_issues = []
        
        # Check for complexity issues
        if context.get("code_complexity", 0) > 15:
            potential_issues.append("high_complexity")
        
        # Check for performance issues
        if context.get("response_time", 0) > 3000:
            potential_issues.append("slow_performance")
        
        # Check for security issues
        if context.get("security_score", 100) < 80:
            potential_issues.append("security_vulnerabilities")
        
        # Check user patterns for recurring issues
        common_categories = user_patterns.get("common_categories", [])
        if "syntax_error" in common_categories:
            potential_issues.append("syntax_prone")
        
        return potential_issues
    
    def _check_security_patterns(self, context: Dict[str, Any]) -> List[str]:
        """Check for common security issues"""
        security_issues = []
        
        # Simplified security checks
        if context.get("input_validation", True) == False:
            security_issues.append("missing_input_validation")
        
        if context.get("authentication", True) == False:
            security_issues.append("weak_authentication")
        
        if context.get("https_enabled", True) == False:
            security_issues.append("insecure_transport")
        
        return security_issues
    
    def _calculate_improvement_trend(self, user_errors: List[ErrorContext]) -> str:
        """Calculate if user is improving over time"""
        if len(user_errors) < 5:
            return "insufficient_data"
        
        # Sort errors by timestamp
        sorted_errors = sorted(user_errors, key=lambda e: e.timestamp)
        
        # Compare recent errors to older ones
        recent_errors = sorted_errors[-5:]
        older_errors = sorted_errors[-10:-5] if len(sorted_errors) >= 10 else sorted_errors[:-5]
        
        recent_severity_avg = sum(self._severity_to_number(e.severity) for e in recent_errors) / len(recent_errors)
        older_severity_avg = sum(self._severity_to_number(e.severity) for e in older_errors) / len(older_errors)
        
        if recent_severity_avg < older_severity_avg:
            return "improving"
        elif recent_severity_avg > older_severity_avg:
            return "declining"
        else:
            return "stable"
    
    def _severity_to_number(self, severity: ErrorSeverity) -> int:
        """Convert severity to number for comparison"""
        mapping = {
            ErrorSeverity.INFO: 1,
            ErrorSeverity.LOW: 2,
            ErrorSeverity.MEDIUM: 3,
            ErrorSeverity.HIGH: 4,
            ErrorSeverity.CRITICAL: 5
        }
        return mapping.get(severity, 3)
    
    def _store_error_context(self, error_context: ErrorContext):
        """Store error context for learning and analysis"""
        if error_context.user_id not in self.user_error_history:
            self.user_error_history[error_context.user_id] = []
        
        self.user_error_history[error_context.user_id].append(error_context)
        
        # Keep only last 100 errors per user
        if len(self.user_error_history[error_context.user_id]) > 100:
            self.user_error_history[error_context.user_id] = self.user_error_history[error_context.user_id][-100:]
    
    def _extract_line_number(self, error_message: str) -> int:
        """Extract line number from error message"""
        import re
        match = re.search(r'line (\d+)', error_message)
        return int(match.group(1)) if match else 1
    
    def _get_fallback_suggestions(self) -> List[Dict[str, Any]]:
        """Get fallback suggestions when AI analysis fails"""
        return [
            {
                "title": "Check Documentation",
                "description": "Review the relevant documentation for guidance",
                "action": "documentation_lookup"
            },
            {
                "title": "Search Similar Issues",
                "description": "Look for similar problems in the community",
                "action": "community_search"
            },
            {
                "title": "Contact Support",
                "description": "Reach out to our support team for assistance",
                "action": "contact_support"
            }
        ]
    
    def _analyze_help_request(self, user_request: str, error_context: ErrorContext) -> Dict[str, Any]:
        """Analyze user's help request"""
        request_lower = user_request.lower()
        
        analysis = {
            "intent": "general_help",
            "urgency": "normal",
            "confidence": 0.7,
            "specific_ask": None
        }
        
        # Determine intent
        if any(word in request_lower for word in ["how", "what", "why", "explain"]):
            analysis["intent"] = "explanation"
        elif any(word in request_lower for word in ["fix", "solve", "resolve"]):
            analysis["intent"] = "solution"
        elif any(word in request_lower for word in ["urgent", "critical", "asap"]):
            analysis["urgency"] = "high"
        
        return analysis
    
    async def _generate_contextual_response(self, request_analysis: Dict[str, Any], error_context: ErrorContext) -> str:
        """Generate contextual response to help request"""
        if request_analysis["intent"] == "explanation":
            return f"This {error_context.category.value} error occurs when {self._get_error_explanation(error_context)}. The specific error '{error_context.error_message}' indicates that {self._get_specific_explanation(error_context)}."
        elif request_analysis["intent"] == "solution":
            return f"To resolve this {error_context.category.value} error, I recommend following these steps: {self._get_solution_steps(error_context)}"
        else:
            return f"I can help you with this {error_context.category.value} error. Would you like me to explain what's happening or provide steps to fix it?"
    
    def _get_error_explanation(self, error_context: ErrorContext) -> str:
        """Get explanation for error category"""
        explanations = {
            ErrorCategory.SYNTAX: "there's a problem with the code syntax or structure",
            ErrorCategory.RUNTIME: "the code encounters an issue while running",
            ErrorCategory.PERFORMANCE: "the application is running slower than expected",
            ErrorCategory.INTEGRATION: "there's a problem connecting to external services"
        }
        return explanations.get(error_context.category, "an unexpected issue occurs")
    
    def _get_specific_explanation(self, error_context: ErrorContext) -> str:
        """Get specific explanation for the error message"""
        message = error_context.error_message.lower()
        
        if "undefined" in message:
            return "a variable or function is being used before it's defined"
        elif "null" in message or "none" in message:
            return "you're trying to use a value that doesn't exist"
        elif "timeout" in message:
            return "an operation is taking too long to complete"
        else:
            return "there's a specific issue that needs attention"
    
    def _get_solution_steps(self, error_context: ErrorContext) -> str:
        """Get solution steps for error category"""
        solutions = {
            ErrorCategory.SYNTAX: "1) Check the line mentioned in the error, 2) Look for missing brackets or semicolons, 3) Verify proper indentation",
            ErrorCategory.RUNTIME: "1) Add error handling with try-catch blocks, 2) Validate inputs before processing, 3) Check for null values",
            ErrorCategory.PERFORMANCE: "1) Profile your code to find bottlenecks, 2) Optimize slow operations, 3) Add caching where appropriate",
            ErrorCategory.INTEGRATION: "1) Check network connectivity, 2) Verify API credentials, 3) Implement retry logic"
        }
        return solutions.get(error_context.category, "1) Review the error details, 2) Check documentation, 3) Contact support if needed")
    
    def _create_interactive_elements(self, error_context: ErrorContext, request_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create interactive elements for help response"""
        return [
            {
                "type": "code_highlighter",
                "description": "Highlight the problematic code",
                "enabled": error_context.category == ErrorCategory.SYNTAX
            },
            {
                "type": "step_by_step_guide",
                "description": "Interactive problem-solving guide",
                "enabled": True
            },
            {
                "type": "live_chat",
                "description": "Chat with a support expert",
                "enabled": request_analysis["urgency"] == "high"
            }
        ]
    
    def _create_step_by_step_guidance(self, error_context: ErrorContext, request_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create step-by-step guidance"""
        strategy = self._select_resolution_strategy(error_context, {})
        if strategy:
            return [
                {
                    "step": step["step"],
                    "title": step["action"],
                    "description": step["description"],
                    "tools": step.get("tools", []),
                    "estimated_time": "2-5 minutes"
                }
                for step in strategy.steps
            ]
        else:
            return [
                {
                    "step": 1,
                    "title": "Analyze the Error",
                    "description": "Carefully read the error message and identify the problem area",
                    "estimated_time": "1-2 minutes"
                },
                {
                    "step": 2,
                    "title": "Research Solutions",
                    "description": "Look up similar errors and their solutions",
                    "estimated_time": "5-10 minutes"
                },
                {
                    "step": 3,
                    "title": "Apply the Fix",
                    "description": "Implement the most appropriate solution",
                    "estimated_time": "5-15 minutes"
                },
                {
                    "step": 4,
                    "title": "Test the Fix",
                    "description": "Verify that the error is resolved",
                    "estimated_time": "2-5 minutes"
                }
            ]
    
    def _get_contextual_resources(self, error_context: ErrorContext) -> List[Dict[str, Any]]:
        """Get contextual resources for the error"""
        return [
            {
                "type": "documentation",
                "title": f"{error_context.category.value.title()} Error Guide",
                "url": f"/docs/errors/{error_context.category.value}",
                "relevance": "high"
            },
            {
                "type": "tutorial",
                "title": "Error Debugging Techniques",
                "url": "/tutorials/debugging",
                "relevance": "medium"
            },
            {
                "type": "community",
                "title": "Community Q&A",
                "url": f"/community/search?q={error_context.error_type}",
                "relevance": "medium"
            }
        ]
    
    def _get_escalation_options(self, error_context: ErrorContext) -> List[Dict[str, Any]]:
        """Get escalation options based on error severity"""
        base_options = [
            {
                "type": "community_help",
                "title": "Ask the Community",
                "description": "Post your question to the community forum",
                "availability": "Always available"
            },
            {
                "type": "documentation",
                "title": "Search Documentation",
                "description": "Find detailed information in our docs",
                "availability": "Always available"
            }
        ]
        
        if error_context.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            base_options.extend([
                {
                    "type": "live_support",
                    "title": "Live Chat Support",
                    "description": "Chat with a support expert",
                    "availability": "Business hours"
                },
                {
                    "type": "priority_support",
                    "title": "Priority Support Ticket",
                    "description": "Get prioritized assistance",
                    "availability": "24/7"
                }
            ])
        
        return base_options
    
    def _identify_improvement_areas(self, resolution_data: Dict[str, Any]) -> List[str]:
        """Identify areas for improvement in error handling"""
        improvements = []
        
        if not resolution_data.get("success", False):
            improvements.append("resolution_strategy_effectiveness")
        
        if resolution_data.get("resolution_time", 0) > 1800:  # > 30 minutes
            improvements.append("resolution_time_optimization")
        
        if resolution_data.get("user_feedback", {}).get("satisfaction_score", 5) < 3:
            improvements.append("user_experience_enhancement")
        
        return improvements

# Demo class
class IntelligentErrorHandlerDemo:
    """Demonstration of the Intelligent Error Handler"""
    
    def __init__(self):
        self.error_handler = IntelligentErrorHandler()
    
    async def run_comprehensive_demo(self) -> Dict[str, Any]:
        """Run a comprehensive demonstration"""
        results = {}
        
        # Demo 1: Handle different types of errors
        error_scenarios = [
            {
                "error_id": "syntax_demo",
                "error_type": "SyntaxError",
                "error_message": "SyntaxError: unexpected token ')' at line 42",
                "user_id": "demo_user_1",
                "context": {
                    "file": "main.py",
                    "function": "calculate_total",
                    "line": 42
                },
                "environment": {"python_version": "3.9", "editor": "vscode"}
            },
            {
                "error_id": "runtime_demo",
                "error_type": "AttributeError",
                "error_message": "AttributeError: 'NoneType' object has no attribute 'split'",
                "user_id": "demo_user_2",
                "context": {
                    "file": "utils.py",
                    "function": "process_text",
                    "user_input": None
                },
                "environment": {"production_environment": True}
            },
            {
                "error_id": "performance_demo",
                "error_type": "TimeoutError",
                "error_message": "TimeoutError: Request timed out after 30 seconds",
                "user_id": "demo_user_3",
                "context": {
                    "api_endpoint": "/api/data",
                    "payload_size": "large",
                    "network_latency": "high"
                },
                "environment": {"server_load": "high"}
            }
        ]
        
        error_handling_results = {}
        for scenario in error_scenarios:
            result = await self.error_handler.handle_error(scenario)
            error_handling_results[scenario["error_id"]] = result
        
        results["error_handling"] = error_handling_results
        
        # Demo 2: Generate proactive suggestions
        proactive_contexts = [
            {
                "user_id": "demo_user_1",
                "context": {
                    "code_complexity": 12,
                    "response_time": 1500,
                    "security_score": 85,
                    "recent_errors": 2
                }
            },
            {
                "user_id": "demo_user_2",
                "context": {
                    "code_complexity": 8,
                    "response_time": 3500,
                    "security_score": 70,
                    "recent_errors": 0
                }
            }
        ]
        
        proactive_results = {}
        for context_data in proactive_contexts:
            suggestions = await self.error_handler.generate_proactive_suggestions(
                context_data["user_id"],
                context_data["context"]
            )
            proactive_results[context_data["user_id"]] = [s.__dict__ for s in suggestions]
        
        results["proactive_suggestions"] = proactive_results
        
        # Demo 3: Contextual help
        help_scenarios = [
            {
                "error_id": "syntax_demo",
                "user_request": "I don't understand why I'm getting this syntax error. Can you explain what's wrong?"
            },
            {
                "error_id": "runtime_demo",
                "user_request": "How do I fix this AttributeError? It's urgent!"
            }
        ]
        
        help_results = {}
        for scenario in help_scenarios:
            # Create error context from previous demo
            error_data = next(e for e in error_scenarios if e["error_id"] == scenario["error_id"])
            error_context = self.error_handler._create_error_context(error_data)
            
            help_response = await self.error_handler.provide_contextual_help(
                error_context,
                scenario["user_request"]
            )
            help_results[scenario["error_id"]] = help_response
        
        results["contextual_help"] = help_results
        
        # Demo 4: Resolution tracking
        resolution_scenarios = [
            {
                "error_id": "syntax_demo",
                "resolution_data": {
                    "success": True,
                    "resolution_time": 120,
                    "strategy_id": "syntax_debugging",
                    "suggestions_used": ["syntax_fix_syntax_demo"],
                    "user_feedback": {"satisfaction_score": 4}
                }
            },
            {
                "error_id": "runtime_demo",
                "resolution_data": {
                    "success": False,
                    "resolution_time": 600,
                    "strategy_id": "runtime_debugging",
                    "suggestions_used": ["runtime_fix_runtime_demo"],
                    "user_feedback": {"satisfaction_score": 2}
                }
            }
        ]
        
        tracking_results = {}
        for scenario in resolution_scenarios:
            result = self.error_handler.track_resolution_success(
                scenario["error_id"],
                scenario["resolution_data"]
            )
            tracking_results[scenario["error_id"]] = result
        
        results["resolution_tracking"] = tracking_results
        
        return results

async def main():
    """Main function for testing"""
    demo = IntelligentErrorHandlerDemo()
    results = await demo.run_comprehensive_demo()
    
    print("🔧 Intelligent Error Handler Demo Results:")
    print("=" * 60)
    
    for section, data in results.items():
        print(f"\n🎯 {section.replace('_', ' ').title()}:")
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"  📋 {key}:")
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, (dict, list)) and len(str(sub_value)) > 150:
                            print(f"    {sub_key}: [Complex data - {len(str(sub_value))} chars]")
                        else:
                            print(f"    {sub_key}: {sub_value}")
                elif isinstance(value, list):
                    print(f"    Found {len(value)} items")
                    for i, item in enumerate(value[:2]):  # Show first 2 items
                        if isinstance(item, dict):
                            title = item.get("title", item.get("suggestion_id", f"Item {i+1}"))
                            print(f"      - {title}")
                else:
                    print(f"    {value}")

if __name__ == "__main__":
    asyncio.run(main())
