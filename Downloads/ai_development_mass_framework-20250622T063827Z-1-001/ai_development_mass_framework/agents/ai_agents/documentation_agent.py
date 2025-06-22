"""
AI-Powered Documentation Agent for MASS Framework
Uses LLMs to generate comprehensive documentation
"""

from typing import Dict, Any, List, Optional
import asyncio
from core.agent_base import AgentBase
from core.llm_service import llm_service, AIMessage
from config.ai_config import ai_config_manager
import logging

logger = logging.getLogger(__name__)

class AIDocumentationAgent(AgentBase):
    """AI-powered agent for generating comprehensive documentation"""
    
    def __init__(self):
        super().__init__("ai_documentation_agent", "AI Documentation Agent")
        self.doc_types = [
            "api_documentation",
            "user_guide", 
            "technical_specification",
            "readme",
            "changelog",
            "installation_guide",
            "troubleshooting_guide",
            "architecture_overview"
        ]
        
    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input for documentation generation"""
        return {
            "analysis_type": "ai_documentation_analysis",
            "supported_doc_types": self.doc_types,
            "capabilities": [
                "code_documentation",
                "api_documentation", 
                "user_guide_generation",
                "technical_writing",
                "markdown_formatting",
                "diagram_descriptions"
            ]
        }
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents for comprehensive documentation"""
        coordination_plan = {
            "coordination_status": "ready",
            "collaboration_opportunities": []
        }
        
        # Coordinate with code generator
        if "ai_code_generator" in other_agents:
            coordination_plan["collaboration_opportunities"].append({
                "agent": "ai_code_generator",
                "task": "code_analysis_for_docs",
                "benefit": "Generate documentation from code analysis"
            })
            
        # Coordinate with testing agent
        if "ai_testing_agent" in other_agents:
            coordination_plan["collaboration_opportunities"].append({
                "agent": "ai_testing_agent", 
                "task": "test_documentation",
                "benefit": "Document testing procedures and examples"
            })
            
        return coordination_plan
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process documentation generation tasks"""
        task_type = task.get("type", "")
        
        try:
            if task_type == "generate_documentation":
                return await self._generate_documentation(task)
            elif task_type == "update_documentation":
                return await self._update_documentation(task)
            elif task_type == "analyze_code_for_docs":
                return await self._analyze_code_for_docs(task)
            elif task_type == "generate_api_docs":
                return await self._generate_api_docs(task)
            else:
                return {"error": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            logger.error(f"AI Documentation Agent error: {str(e)}")
            return {"error": f"Task failed: {str(e)}"}
    
    async def _generate_documentation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive documentation"""
        doc_type = task.get("doc_type", "readme")
        content = task.get("content", "")
        project_info = task.get("project_info", {})
        
        system_prompt = f"""You are a technical documentation expert. Generate comprehensive, clear, and well-structured documentation.

Documentation Type: {doc_type}
Requirements:
- Clear structure with proper headers
- Easy to understand explanations
- Code examples where appropriate
- Proper markdown formatting
- Professional tone
- Complete coverage of the topic"""

        user_prompt = f"""Generate {doc_type} documentation for:

Project Information: {project_info}
Content to document: {content}

Please create comprehensive documentation that covers all important aspects."""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "doc_type": doc_type,
                "documentation": response.content,
                "format": "markdown",
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Documentation generation failed: {str(e)}")
            return {"error": f"Documentation generation failed: {str(e)}"}
    
    async def _update_documentation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing documentation"""
        existing_doc = task.get("existing_doc", "")
        updates = task.get("updates", "")
        
        system_prompt = """You are a technical documentation expert. Update existing documentation while maintaining consistency and clarity."""

        user_prompt = f"""Update the following documentation:

Existing Documentation:
{existing_doc}

Requested Updates:
{updates}

Please update the documentation while maintaining the existing structure and style."""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "updated_documentation": response.content,
                "format": "markdown",
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Documentation update failed: {str(e)}")
            return {"error": f"Documentation update failed: {str(e)}"}
    
    async def _analyze_code_for_docs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code to generate documentation"""
        code = task.get("code", "")
        language = task.get("language", "python")
        
        system_prompt = f"""You are a code documentation expert. Analyze {language} code and generate comprehensive documentation.

Requirements:
- Function/class documentation
- Parameter descriptions
- Return value descriptions
- Usage examples
- Error handling documentation"""

        user_prompt = f"""Analyze this {language} code and generate documentation:

```{language}
{code}
```

Please provide comprehensive documentation for this code."""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "code_documentation": response.content,
                "language": language,
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Code analysis for docs failed: {str(e)}")
            return {"error": f"Code analysis failed: {str(e)}"}
    
    async def _generate_api_docs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API documentation"""
        api_spec = task.get("api_spec", "")
        endpoints = task.get("endpoints", [])
        
        system_prompt = """You are an API documentation expert. Generate comprehensive API documentation with clear examples and descriptions."""

        user_prompt = f"""Generate API documentation for:

API Specification: {api_spec}
Endpoints: {endpoints}

Please create comprehensive API documentation including:
- Endpoint descriptions
- Request/response examples
- Error codes
- Authentication requirements
- Rate limiting information"""

        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "status": "success",
                "api_documentation": response.content,
                "format": "markdown",
                "token_usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"API documentation generation failed: {str(e)}")
            return {"error": f"API documentation generation failed: {str(e)}"}
