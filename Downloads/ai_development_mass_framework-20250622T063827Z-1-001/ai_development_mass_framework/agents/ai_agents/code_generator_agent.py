"""
AI-Powered Code Generator Agent for MASS Framework
Uses LLMs to generate, refactor, and improve code
"""

from typing import Dict, Any, List, Optional
import asyncio
import os
import ast
from core.agent_base import AgentBase
from core.llm_service import llm_service, AIMessage
from config.ai_config import ai_config_manager
from agents.ai_agents.core import MassEnabledAgent
import logging

logger = logging.getLogger(__name__)

class CodeGeneratorAgent(MassEnabledAgent):
    """AI-powered agent for generating and improving code (MASS-enabled)"""
    
    def __init__(self, config=None):
        super().__init__("ai_code_generator", self.on_message, config, agent_id="ai_code_generator", specialization="AI Code Generator Agent")
        self.supported_languages = [
            "python", "javascript", "typescript", "java", "c++", "c#", 
            "go", "rust", "ruby", "php", "swift", "kotlin", "sql"
        ]
        self.code_templates = self._load_code_templates()
        self.prompt_variations = {
            'generate_code': [
                "Generate code for the following task:",
                "Step by step, generate code for this task:",
                "Provide a function with error handling and tests:",
                "Write production-ready code for this requirement:"
            ]
        }
        self.optimized_prompt = None

    def _load_code_templates(self) -> Dict[str, str]:
        """Load code templates for different scenarios"""
        return {
            "class": """Create a well-structured class with:
- Clear documentation
- Type hints (for Python/TypeScript)
- Proper error handling
- Unit test examples""",
            
            "function": """Create a function with:
- Clear purpose and documentation
- Input validation
- Type hints/annotations
- Error handling
- Usage examples""",
            
            "api_endpoint": """Create a REST API endpoint with:
- Proper HTTP methods
- Input validation
- Error handling
- Response formatting
- Authentication if needed""",
            
            "database_model": """Create a database model with:
- Proper field types
- Relationships
- Validation rules
- Index definitions
- Migration scripts""",
            
            "test_suite": """Create comprehensive tests with:
- Unit tests
- Integration tests
- Edge case testing
- Mock setups
- Assertion examples"""
        }
    
    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input and determine code generation approach"""
        return {
            "analysis_type": "ai_code_analysis",
            "input_type": input_data.get("type", "unknown"),
            "supported_languages": self.supported_languages,
            "available_templates": list(self.code_templates.keys()),
            "ai_capabilities": [
                "code_generation",
                "code_refactoring", 
                "code_review",
                "test_generation",
                "documentation_generation"
            ]
        }
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents for complex code generation tasks"""
        coordination_plan = {
            "coordination_status": "ready",
            "collaboration_opportunities": []
        }
        
        # Check for documentation agent
        if "documentation_agent" in other_agents:
            coordination_plan["collaboration_opportunities"].append({
                "agent": "documentation_agent",
                "task": "generate_comprehensive_docs",
                "benefit": "Auto-generate documentation for generated code"
            })
        
        # Check for testing agent
        if "testing_agent" in other_agents:
            coordination_plan["collaboration_opportunities"].append({
                "agent": "testing_agent", 
                "task": "generate_test_suite",
                "benefit": "Auto-generate tests for generated code"
            })
        
        # Check for code analyzer
        if "code_analyzer" in other_agents:
            coordination_plan["collaboration_opportunities"].append({
                "agent": "code_analyzer",
                "task": "analyze_generated_code",
                "benefit": "Review and optimize generated code"
            })
        
        return coordination_plan
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process AI code generation tasks"""
        task_type = task.get("type", "")
        
        try:
            if task_type == "generate_code":
                return await self._generate_code(task)
            elif task_type == "refactor_code":
                return await self._refactor_code(task)
            elif task_type == "review_code":
                return await self._review_code(task)
            elif task_type == "generate_tests":
                return await self._generate_tests(task)
            elif task_type == "explain_code":
                return await self._explain_code(task)
            elif task_type == "fix_bugs":
                return await self._fix_bugs(task)
            else:
                return {"error": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            logger.error(f"AI Code Generator error: {str(e)}")
            return {"error": f"Task failed: {str(e)}"}
    
    async def _generate_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code from natural language description"""
        description = task.get("description", "")
        language = task.get("language", "python")
        template_type = task.get("template", "function")
        
        if not description:
            return {"error": "Code description is required"}
        
        # Build system prompt
        system_prompt = f"""You are an expert {language} developer. Generate high-quality, production-ready code.

Requirements:
- Write clean, readable, and maintainable code
- Include proper error handling
- Add comprehensive documentation
- Follow {language} best practices and conventions
- Include type hints/annotations where applicable
- Add inline comments for complex logic

Template context: {self.code_templates.get(template_type, '')}"""
        
        user_prompt = f"""Generate {language} code for the following requirement:

{description}

Additional specifications:
- Language: {language}
- Template type: {template_type}
- Include usage examples
- Add error handling
- Make it production-ready"""
        
        messages = [
            AIMessage(role="system", content=system_prompt),
            AIMessage(role="user", content=user_prompt)
        ]
          # Generate code using AI
        model = ai_config_manager.config.code_generation_model
        response = await llm_service.generate_response(messages, model=model)
        
        return {
            "status": "success",
            "generated_code": response.content,
            "language": language,
            "template_type": template_type,
            "model_used": response.model,
            "tokens_used": response.tokens_used,
            "cost_estimate": response.cost_estimate,
            "generation_time": response.response_time,
            "suggestions": [
                "Review the generated code carefully",
                "Test thoroughly before production use",
                "Consider security implications",
                "Add additional validation if needed"
            ]
        }
    
    async def _refactor_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Refactor existing code for better quality"""
        code = task.get("code", "")
        language = task.get("language", "python")
        focus_areas = task.get("focus_areas", ["readability", "performance"])
        
        if not code:
            return {"error": "Code to refactor is required"}
        
        system_prompt = f"""You are an expert {language} developer specializing in code refactoring.
        
Refactoring goals:
- Improve code readability and maintainability
- Optimize performance where possible
- Follow {language} best practices
- Maintain original functionality
- Add proper documentation
- Improve error handling

Focus areas for this refactoring: {', '.join(focus_areas)}"""
        
        user_prompt = f"""Please refactor the following {language} code:

```{language}
{code}
```

Refactoring requirements:
- Focus on: {', '.join(focus_areas)}
- Maintain all original functionality
- Improve code structure and readability
- Add missing documentation
- Optimize performance where possible
- Explain the changes made"""
        
        messages = [
            AIMessage(role="system", content=system_prompt),
            AIMessage(role="user", content=user_prompt)
        ]
        
        model = ai_config_manager.config.code_generation_model
        response = await llm_service.generate_response(messages, model=model)
        
        return {
            "refactored_code": response.content,
            "original_language": language,
            "focus_areas": focus_areas,
            "model_used": response.model,
            "tokens_used": response.tokens_used,
            "cost_estimate": response.cost_estimate,
            "refactoring_time": response.response_time
        }
    
    async def _review_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered code review"""
        code = task.get("code", "")
        language = task.get("language", "python")
        review_type = task.get("review_type", "comprehensive")
        
        if not code:
            return {"error": "Code to review is required"}
        
        system_prompt = f"""You are a senior {language} code reviewer with expertise in:
- Security vulnerabilities
- Performance optimization
- Code quality and maintainability
- Best practices and conventions
- Testing strategies
- Documentation quality

Provide a thorough code review with:
- Specific issues found
- Severity ratings (Critical, High, Medium, Low)
- Concrete suggestions for improvement
- Security considerations
- Performance implications"""
        
        user_prompt = f"""Please review the following {language} code:

```{language}
{code}
```

Review type: {review_type}

Provide detailed feedback on:
1. Code quality and maintainability
2. Security vulnerabilities
3. Performance issues
4. Best practice violations
5. Testing gaps
6. Documentation quality
7. Specific improvement suggestions"""
        
        messages = [
            AIMessage(role="system", content=system_prompt),
            AIMessage(role="user", content=user_prompt)
        ]
        
        model = ai_config_manager.config.code_review_model
        response = await llm_service.generate_response(messages, model=model)
        
        return {
            "review_results": response.content,
            "language": language,
            "review_type": review_type,
            "model_used": response.model,
            "tokens_used": response.tokens_used,
            "cost_estimate": response.cost_estimate,
            "review_time": response.response_time
        }
    
    async def _generate_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive test suite for code"""
        code = task.get("code", "")
        language = task.get("language", "python")
        test_framework = task.get("test_framework", "pytest")
        
        if not code:
            return {"error": "Code to test is required"}
        
        system_prompt = f"""You are an expert test engineer specializing in {language} testing.

Generate comprehensive tests using {test_framework} including:
- Unit tests for all functions/methods
- Edge case testing
- Error condition testing
- Integration tests where applicable
- Performance tests for critical paths
- Mock setups for external dependencies
- Clear test documentation"""
        
        user_prompt = f"""Generate a comprehensive test suite for the following {language} code:

```{language}
{code}
```

Requirements:
- Test framework: {test_framework}
- Include unit tests for all functions
- Test edge cases and error conditions
- Add integration tests where relevant
- Include setup and teardown methods
- Add clear test documentation
- Use appropriate mocking"""
        
        messages = [
            AIMessage(role="system", content=system_prompt),
            AIMessage(role="user", content=user_prompt)
        ]
        
        model = ai_config_manager.config.code_generation_model
        response = await llm_service.generate_response(messages, model=model)
        
        return {
            "generated_tests": response.content,
            "language": language,
            "test_framework": test_framework,
            "model_used": response.model,
            "tokens_used": response.tokens_used,
            "cost_estimate": response.cost_estimate,
            "generation_time": response.response_time
        }
    
    async def _explain_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Explain code functionality and logic"""
        code = task.get("code", "")
        language = task.get("language", "python")
        detail_level = task.get("detail_level", "intermediate")
        
        if not code:
            return {"error": "Code to explain is required"}
        
        system_prompt = f"""You are an expert {language} developer and teacher.
        
Explain code in a clear, educational manner appropriate for {detail_level} level:
- Break down the overall purpose
- Explain each major section
- Describe key algorithms or logic
- Highlight important patterns
- Explain any complex or unusual constructs
- Provide context about when/why to use this approach"""
        
        user_prompt = f"""Please explain the following {language} code:

```{language}
{code}
```

Explanation level: {detail_level}

Please provide:
1. Overall purpose and functionality
2. Step-by-step breakdown of the logic
3. Key concepts and patterns used
4. Potential improvements or alternatives
5. When this approach would be most useful"""
        
        messages = [
            AIMessage(role="system", content=system_prompt),
            AIMessage(role="user", content=user_prompt)
        ]
        
        model = ai_config_manager.config.documentation_model
        response = await llm_service.generate_response(messages, model=model)
        
        return {
            "explanation": response.content,
            "language": language,
            "detail_level": detail_level,
            "model_used": response.model,
            "tokens_used": response.tokens_used,
            "cost_estimate": response.cost_estimate,
            "explanation_time": response.response_time
        }
    
    async def _fix_bugs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered bug detection and fixing"""
        code = task.get("code", "")
        language = task.get("language", "python")
        error_message = task.get("error_message", "")
        
        if not code:
            return {"error": "Code with bugs is required"}
        
        system_prompt = f"""You are an expert {language} debugger and problem solver.

Your task is to:
1. Identify bugs and issues in the code
2. Provide fixed versions of the code
3. Explain what was wrong and why
4. Suggest preventive measures
5. Recommend testing strategies"""
        
        user_prompt = f"""Please analyze and fix the bugs in this {language} code:

```{language}
{code}
```

Error message (if available): {error_message}

Please provide:
1. Identification of all bugs found
2. Fixed version of the code
3. Explanation of each fix
4. Preventive measures for similar bugs
5. Testing recommendations"""
        
        messages = [
            AIMessage(role="system", content=system_prompt),
            AIMessage(role="user", content=user_prompt)
        ]
        
        model = ai_config_manager.config.code_generation_model
        response = await llm_service.generate_response(messages, model=model)
        
        return {
            "bug_analysis": response.content,
            "language": language,
            "error_message": error_message,
            "model_used": response.model,
            "tokens_used": response.tokens_used,
            "cost_estimate": response.cost_estimate,
            "debug_time": response.response_time
        }
    
    async def optimize_local_prompts(self, validation_data):
        self.optimized_prompt = await self.mass_optimizer.prompt_optimizer.evaluate_prompts(
            self.prompt_variations['generate_code'], validation_data, metric='accuracy')
        return self.optimized_prompt

    async def on_message(self, sender, message):
        # ...existing code or pass...
        pass
