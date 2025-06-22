"""
AI-Powered Testing Agent for MASS Framework
Uses LLMs to generate comprehensive test suites
"""

from typing import Dict, Any, List, Optional
import asyncio
from core.agent_base import AgentBase
from core.llm_service import llm_service, AIMessage
from config.ai_config import ai_config_manager
import logging

logger = logging.getLogger(__name__)

class AITestingAgent(AgentBase):
    """AI-powered agent for generating comprehensive test suites"""
    
    def __init__(self):
        super().__init__("ai_testing_agent", "AI Testing Agent")
        self.test_types = [
            "unit_tests",
            "integration_tests",
            "end_to_end_tests",
            "performance_tests",
            "security_tests",
            "api_tests",
            "ui_tests",
            "load_tests"
        ]
        self.test_frameworks = {
            "python": ["pytest", "unittest", "nose2"],
            "javascript": ["jest", "mocha", "cypress"],
            "typescript": ["jest", "mocha", "cypress"],
            "java": ["junit", "testng"],
            "c#": ["nunit", "xunit", "mstest"],
            "go": ["testing", "ginkgo"],
            "rust": ["cargo test"],
            "ruby": ["rspec", "minitest"]
        }
        
    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input for test generation"""
        return {
            "analysis_type": "ai_testing_analysis",
            "supported_test_types": self.test_types,
            "supported_frameworks": self.test_frameworks,
            "capabilities": [
                "test_generation",
                "test_optimization",
                "test_analysis",
                "coverage_analysis",
                "performance_testing",
                "security_testing"
            ]
        }
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents for comprehensive testing"""
        coordination_plan = {
            "coordination_status": "ready",
            "collaboration_opportunities": []
        }
        
        # Coordinate with code generator
        if "ai_code_generator" in other_agents:
            coordination_plan["collaboration_opportunities"].append({
                "agent": "ai_code_generator",
                "task": "generate_testable_code",
                "benefit": "Generate code with built-in test hooks"
            })
            
        # Coordinate with documentation agent
        if "ai_documentation_agent" in other_agents:
            coordination_plan["collaboration_opportunities"].append({
                "agent": "ai_documentation_agent",
                "task": "document_tests",
                "benefit": "Generate comprehensive test documentation"
            })
            
        return coordination_plan
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process test generation tasks"""
        task_type = task.get("type", "")
        
        try:
            if task_type == "generate_tests":
                return await self._generate_tests(task)
            elif task_type == "analyze_coverage":
                return await self._analyze_coverage(task)
            elif task_type == "optimize_tests":
                return await self._optimize_tests(task)
            elif task_type == "generate_performance_tests":
                return await self._generate_performance_tests(task)
            elif task_type == "generate_security_tests":
                return await self._generate_security_tests(task)
            else:
                return {"error": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            logger.error(f"AI Testing Agent error: {str(e)}")
            return {"error": f"Task failed: {str(e)}"}
    
    async def _generate_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive test suite"""
        code = task.get("code", "")
        language = task.get("language", "python")
        test_type = task.get("test_type", "unit_tests")
        framework = task.get("framework", "")
        
        # Auto-select framework if not specified
        if not framework and language in self.test_frameworks:
            framework = self.test_frameworks[language][0]
        
        system_prompt = f"""You are a testing expert specializing in {language} and {framework}. Generate comprehensive, production-ready test suites.

Test Requirements:
- {test_type} using {framework}
- Test all edge cases and error conditions
- Include setup and teardown
- Clear test names and descriptions
- Proper assertions
- Mock external dependencies
- Follow {language} testing best practices"""

        user_prompt = f"""Generate {test_type} for this {language} code using {framework}:

```{language}
{code}
```

Please create comprehensive tests that cover:
1. Happy path scenarios
2. Edge cases
3. Error conditions
4. Input validation
5. Boundary conditions"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "test_type": test_type,
                "framework": framework,
                "language": language,
                "test_code": response.content,
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Test generation failed: {str(e)}")
            return {"error": f"Test generation failed: {str(e)}"}
    
    async def _analyze_coverage(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze test coverage and suggest improvements"""
        code = task.get("code", "")
        existing_tests = task.get("existing_tests", "")
        language = task.get("language", "python")
        
        system_prompt = f"""You are a test coverage expert for {language}. Analyze code and existing tests to identify coverage gaps.

Focus on:
- Uncovered code paths
- Missing edge cases
- Untested error conditions
- Integration test gaps
- Performance test opportunities"""

        user_prompt = f"""Analyze test coverage for this {language} code:

Source Code:
```{language}
{code}
```

Existing Tests:
```{language}
{existing_tests}
```

Please provide:
1. Coverage analysis
2. Missing test scenarios
3. Recommended additional tests
4. Coverage improvement suggestions"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "coverage_analysis": response.content,
                "language": language,
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Coverage analysis failed: {str(e)}")
            return {"error": f"Coverage analysis failed: {str(e)}"}
    
    async def _optimize_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize existing test suite"""
        existing_tests = task.get("existing_tests", "")
        language = task.get("language", "python")
        framework = task.get("framework", "")
        
        system_prompt = f"""You are a test optimization expert for {language} and {framework}. Optimize test suites for performance, maintainability, and reliability.

Optimization areas:
- Remove redundant tests
- Improve test performance
- Enhance test reliability
- Better test organization
- Reduce test flakiness"""

        user_prompt = f"""Optimize this {language} test suite using {framework}:

```{language}
{existing_tests}
```

Please provide optimized tests with:
1. Performance improvements
2. Better organization
3. Reduced redundancy
4. Enhanced reliability
5. Cleaner code structure"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "optimized_tests": response.content,
                "language": language,
                "framework": framework,
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Test optimization failed: {str(e)}")
            return {"error": f"Test optimization failed: {str(e)}"}
    
    async def _generate_performance_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance test suite"""
        code = task.get("code", "")
        language = task.get("language", "python")
        performance_requirements = task.get("performance_requirements", {})
        
        system_prompt = f"""You are a performance testing expert for {language}. Generate comprehensive performance tests.

Performance Testing Areas:
- Response time testing
- Load testing
- Stress testing
- Memory usage testing
- Throughput testing
- Scalability testing"""

        user_prompt = f"""Generate performance tests for this {language} code:

```{language}
{code}
```

Performance Requirements: {performance_requirements}

Please create performance tests covering:
1. Response time benchmarks
2. Load testing scenarios
3. Memory usage validation
4. Throughput measurements
5. Scalability testing"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "performance_tests": response.content,
                "language": language,
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Performance test generation failed: {str(e)}")
            return {"error": f"Performance test generation failed: {str(e)}"}
    
    async def _generate_security_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate security test suite"""
        code = task.get("code", "")
        language = task.get("language", "python")
        security_requirements = task.get("security_requirements", {})
        
        system_prompt = f"""You are a security testing expert for {language}. Generate comprehensive security tests.

Security Testing Areas:
- Input validation testing
- Authentication testing
- Authorization testing
- SQL injection testing
- XSS testing
- CSRF testing
- Data encryption testing"""

        user_prompt = f"""Generate security tests for this {language} code:

```{language}
{code}
```

Security Requirements: {security_requirements}

Please create security tests covering:
1. Input validation
2. Authentication bypass attempts
3. Authorization violations
4. Injection attacks
5. Data security
6. Session management"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "security_tests": response.content,
                "language": language,
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Security test generation failed: {str(e)}")
            return {"error": f"Security test generation failed: {str(e)}"}
