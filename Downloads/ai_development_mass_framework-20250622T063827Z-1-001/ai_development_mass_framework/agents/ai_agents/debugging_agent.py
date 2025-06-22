"""
AI-Powered Debugging Agent for MASS Framework
Uses LLMs to analyze and fix bugs in code
"""

from typing import Dict, Any, List, Optional
import asyncio
import re
from core.agent_base import AgentBase
from core.llm_service import llm_service, AIMessage
from config.ai_config import ai_config_manager
import logging

logger = logging.getLogger(__name__)

class AIDebuggingAgent(AgentBase):
    """AI-powered agent for debugging and fixing code issues"""
    
    def __init__(self):
        super().__init__("ai_debugging_agent", "AI Debugging Agent")
        self.bug_types = [
            "syntax_errors",
            "runtime_errors",
            "logic_errors", 
            "performance_issues",
            "memory_leaks",
            "security_vulnerabilities",
            "concurrency_issues",
            "integration_issues"
        ]
        self.debugging_techniques = [
            "error_analysis",
            "code_review",
            "trace_analysis",
            "performance_profiling",
            "memory_analysis",
            "security_audit"
        ]
        
    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input for debugging requirements"""
        return {
            "analysis_type": "ai_debugging_analysis",
            "supported_bug_types": self.bug_types,
            "debugging_techniques": self.debugging_techniques,
            "capabilities": [
                "error_diagnosis",
                "bug_fixing",
                "code_optimization",
                "performance_improvement",
                "security_hardening",
                "refactoring_suggestions"
            ]
        }
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents for comprehensive debugging"""
        coordination_plan = {
            "coordination_status": "ready",
            "collaboration_opportunities": []
        }
        
        # Coordinate with code generator for fixes
        if "ai_code_generator" in other_agents:
            coordination_plan["collaboration_opportunities"].append({
                "agent": "ai_code_generator",
                "task": "generate_fixed_code",
                "benefit": "Generate corrected code based on debug analysis"
            })
            
        # Coordinate with testing agent for verification
        if "ai_testing_agent" in other_agents:
            coordination_plan["collaboration_opportunities"].append({
                "agent": "ai_testing_agent",
                "task": "verify_fixes",
                "benefit": "Generate tests to verify bug fixes"
            })
            
        return coordination_plan
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process debugging tasks"""
        task_type = task.get("type", "")
        
        try:
            if task_type == "debug_error":
                return await self._debug_error(task)
            elif task_type == "analyze_performance":
                return await self._analyze_performance(task)
            elif task_type == "find_memory_leaks":
                return await self._find_memory_leaks(task)
            elif task_type == "security_audit":
                return await self._security_audit(task)
            elif task_type == "fix_bug":
                return await self._fix_bug(task)
            elif task_type == "optimize_code":
                return await self._optimize_code(task)
            else:
                return {"error": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            logger.error(f"AI Debugging Agent error: {str(e)}")
            return {"error": f"Task failed: {str(e)}"}
    
    async def _debug_error(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Debug and analyze errors in code"""
        code = task.get("code", "")
        error_message = task.get("error_message", "")
        language = task.get("language", "python")
        stack_trace = task.get("stack_trace", "")
        
        system_prompt = f"""You are an expert {language} debugger. Analyze errors and provide detailed debugging information.

Debugging Approach:
1. Analyze the error message and stack trace
2. Identify the root cause
3. Explain what went wrong
4. Provide step-by-step debugging guidance
5. Suggest multiple potential fixes
6. Include prevention strategies"""

        user_prompt = f"""Debug this {language} error:

Code:
```{language}
{code}
```

Error Message: {error_message}

Stack Trace:
{stack_trace}

Please provide:
1. Root cause analysis
2. Explanation of the error
3. Step-by-step debugging approach
4. Multiple fix options
5. Prevention strategies"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "debug_analysis": response.content,
                "language": language,
                "error_type": self._classify_error(error_message),
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Error debugging failed: {str(e)}")
            return {"error": f"Error debugging failed: {str(e)}"}
    
    async def _analyze_performance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code performance and identify bottlenecks"""
        code = task.get("code", "")
        language = task.get("language", "python")
        performance_data = task.get("performance_data", {})
        
        system_prompt = f"""You are a {language} performance expert. Analyze code for performance issues and optimization opportunities.

Performance Analysis Areas:
- Algorithm complexity
- Memory usage patterns
- I/O operations
- Database queries
- Loop optimizations
- Caching opportunities
- Concurrency improvements"""

        user_prompt = f"""Analyze performance for this {language} code:

```{language}
{code}
```

Performance Data: {performance_data}

Please provide:
1. Performance bottleneck identification
2. Complexity analysis
3. Memory usage analysis
4. Optimization recommendations
5. Code improvements
6. Best practices suggestions"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "performance_analysis": response.content,
                "language": language,
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Performance analysis failed: {str(e)}")
            return {"error": f"Performance analysis failed: {str(e)}"}
    
    async def _find_memory_leaks(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Find and analyze memory leaks"""
        code = task.get("code", "")
        language = task.get("language", "python")
        memory_profile = task.get("memory_profile", {})
        
        system_prompt = f"""You are a {language} memory management expert. Analyze code for memory leaks and inefficient memory usage.

Memory Analysis Areas:
- Object lifecycle management
- Resource cleanup
- Circular references
- Large object handling
- Memory allocation patterns
- Garbage collection issues"""

        user_prompt = f"""Analyze memory usage for this {language} code:

```{language}
{code}
```

Memory Profile: {memory_profile}

Please identify:
1. Potential memory leaks
2. Inefficient memory usage
3. Resource cleanup issues
4. Memory optimization opportunities
5. Best practices for memory management"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "memory_analysis": response.content,
                "language": language,
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Memory leak analysis failed: {str(e)}")
            return {"error": f"Memory leak analysis failed: {str(e)}"}
    
    async def _security_audit(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform security audit on code"""
        code = task.get("code", "")
        language = task.get("language", "python")
        
        system_prompt = f"""You are a {language} security expert. Perform comprehensive security audit on code.

Security Areas to Check:
- Input validation vulnerabilities
- SQL injection risks
- XSS vulnerabilities
- Authentication bypasses
- Authorization flaws
- Data exposure risks
- Cryptographic issues
- Configuration security"""

        user_prompt = f"""Perform security audit on this {language} code:

```{language}
{code}
```

Please identify:
1. Security vulnerabilities
2. Risk assessment for each issue
3. Exploitation scenarios
4. Mitigation strategies
5. Security best practices
6. Compliance considerations"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "security_audit": response.content,
                "language": language,
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Security audit failed: {str(e)}")
            return {"error": f"Security audit failed: {str(e)}"}
    
    async def _fix_bug(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Fix identified bugs in code"""
        code = task.get("code", "")
        bug_description = task.get("bug_description", "")
        language = task.get("language", "python")
        
        system_prompt = f"""You are an expert {language} developer specializing in bug fixes. Provide corrected code with detailed explanations.

Bug Fix Requirements:
- Maintain existing functionality
- Follow coding best practices
- Add error handling if needed
- Include comments explaining changes
- Ensure code readability
- Preserve performance"""

        user_prompt = f"""Fix the bug in this {language} code:

```{language}
{code}
```

Bug Description: {bug_description}

Please provide:
1. Corrected code
2. Explanation of changes made
3. Why the original code was buggy
4. Additional improvements
5. Testing recommendations"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "fixed_code": response.content,
                "language": language,
                "bug_type": self._classify_bug(bug_description),
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Bug fix failed: {str(e)}")
            return {"error": f"Bug fix failed: {str(e)}"}
    
    async def _optimize_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize code for better performance and maintainability"""
        code = task.get("code", "")
        language = task.get("language", "python")
        optimization_goals = task.get("optimization_goals", ["performance", "readability"])
        
        system_prompt = f"""You are a {language} optimization expert. Optimize code while maintaining functionality.

Optimization Goals: {optimization_goals}

Optimization Areas:
- Algorithm efficiency
- Data structure selection
- Code readability
- Memory usage
- Execution speed
- Maintainability"""

        user_prompt = f"""Optimize this {language} code:

```{language}
{code}
```

Optimization Goals: {optimization_goals}

Please provide:
1. Optimized code
2. Performance improvements
3. Readability enhancements
4. Explanation of changes
5. Benchmarking suggestions"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "optimized_code": response.content,
                "language": language,
                "optimization_goals": optimization_goals,
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Code optimization failed: {str(e)}")
            return {"error": f"Code optimization failed: {str(e)}"}
    
    def _classify_error(self, error_message: str) -> str:
        """Classify error type based on error message"""
        error_message_lower = error_message.lower()
        
        if any(keyword in error_message_lower for keyword in ["syntax", "invalid syntax", "unexpected token"]):
            return "syntax_error"
        elif any(keyword in error_message_lower for keyword in ["name", "not defined", "undefined"]):
            return "name_error"
        elif any(keyword in error_message_lower for keyword in ["type", "argument", "operand"]):
            return "type_error"
        elif any(keyword in error_message_lower for keyword in ["index", "key", "out of range"]):
            return "access_error"
        elif any(keyword in error_message_lower for keyword in ["import", "module", "package"]):
            return "import_error"
        elif any(keyword in error_message_lower for keyword in ["attribute", "has no"]):
            return "attribute_error"
        else:
            return "runtime_error"
    
    def _classify_bug(self, bug_description: str) -> str:
        """Classify bug type based on description"""
        bug_description_lower = bug_description.lower()
        
        if any(keyword in bug_description_lower for keyword in ["performance", "slow", "timeout"]):
            return "performance_issue"
        elif any(keyword in bug_description_lower for keyword in ["memory", "leak", "usage"]):
            return "memory_issue"
        elif any(keyword in bug_description_lower for keyword in ["security", "vulnerability", "exploit"]):
            return "security_issue"
        elif any(keyword in bug_description_lower for keyword in ["logic", "incorrect", "wrong result"]):
            return "logic_error"
        elif any(keyword in bug_description_lower for keyword in ["crash", "exception", "error"]):
            return "runtime_error"
        else:
            return "general_bug"
