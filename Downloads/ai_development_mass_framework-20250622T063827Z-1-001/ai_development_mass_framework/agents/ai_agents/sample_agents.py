"""
Sample agent implementations for the MASS Framework
"""

from agents.ai_agents.core import MassEnabledAgent

from core.agent_base import AgentBase
from typing import Dict, Any, List
import asyncio
import random

class CodeAnalyzerAgent(MassEnabledAgent):
    """Agent specialized in code analysis and suggestions (MASS-enabled)"""
    
    def __init__(self, config=None):
        super().__init__("code_analyzer", self.on_message, config, agent_id="code_analyzer", specialization="Code Analyzer Agent")
        self.supported_languages = ["python", "javascript", "typescript", "java", "c++"]
        self.prompt_variations = {
            'analyze_file': [
                "Analyze this file for code quality:",
                "Step by step, analyze this file for maintainability:",
                "Provide a detailed analysis of this file:"
            ]
        }
        self.optimized_prompt = None
    
    async def optimize_local_prompts(self, validation_data):
        self.optimized_prompt = await self.mass_optimizer.prompt_optimizer.evaluate_prompts(
            self.prompt_variations['analyze_file'], validation_data, metric='accuracy')
        return self.optimized_prompt
    
    async def on_message(self, sender, message):
        pass
    
    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input data and return insights"""
        return {
            "analysis_type": "code_analysis",
            "input_type": input_data.get("type", "unknown"),
            "complexity": "medium",
            "recommendations": ["Add type hints", "Improve documentation"]
        }
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents for complex tasks"""
        return {
            "coordination_status": "ready",
            "can_collaborate_with": other_agents,
            "shared_context": task_context.get("shared_data", {})
        }
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code and provide suggestions"""
        task_type = task.get("type", "")
        
        if task_type == "analyze_file":
            return await self._analyze_file(task.get("file_path", ""))
        elif task_type == "suggest_improvements":
            return await self._suggest_improvements(task.get("code", ""))
        elif task_type == "detect_patterns":
            return await self._detect_patterns(task.get("project_path", ""))
        else:
            return {"error": f"Unknown task type: {task_type}"}
    
    async def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file"""
        # Simulate analysis delay
        await asyncio.sleep(1)
        
        return {
            "file_path": file_path,
            "analysis": {
                "complexity": random.randint(1, 10),
                "maintainability": random.choice(["high", "medium", "low"]),
                "test_coverage": f"{random.randint(60, 95)}%",
                "issues": [
                    {"type": "warning", "message": "Consider adding type hints"},
                    {"type": "info", "message": "Function could be optimized"}
                ]
            },
            "suggestions": [
                "Add docstrings to functions",
                "Consider breaking down large functions",
                "Add unit tests for edge cases"
            ]
        }
    
    async def _suggest_improvements(self, code: str) -> Dict[str, Any]:
        """Suggest code improvements"""
        await asyncio.sleep(0.5)
        
        return {
            "improvements": [
                {
                    "priority": "high",
                    "type": "performance",
                    "description": "Use list comprehension instead of loop"
                },
                {
                    "priority": "medium", 
                    "type": "readability",
                    "description": "Add descriptive variable names"
                }
            ],
            "estimated_impact": "15% performance improvement"
        }
    
    async def _detect_patterns(self, project_path: str) -> Dict[str, Any]:
        """Detect code patterns in the project"""
        await asyncio.sleep(2)
        
        return {
            "patterns": [
                {"pattern": "Singleton", "count": 3, "files": ["config.py", "database.py"]},
                {"pattern": "Factory", "count": 1, "files": ["agent_factory.py"]},
                {"pattern": "Observer", "count": 2, "files": ["events.py", "notifications.py"]}
            ],
            "anti_patterns": [
                {"pattern": "God Object", "severity": "medium", "files": ["main.py"]}
            ]
        }

class DocumentationAgent(AgentBase):
    """Agent specialized in documentation generation and maintenance"""
    
    def __init__(self):
        super().__init__("documentation_agent", "Documentation Agent")
    
    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input for documentation needs"""
        return {
            "analysis_type": "documentation_analysis",
            "input_type": input_data.get("type", "unknown"),
            "documentation_coverage": "75%",
            "missing_sections": ["API Reference", "Examples"]
        }
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents for documentation tasks"""
        return {
            "coordination_status": "ready",
            "can_help_with": ["README generation", "API docs", "changelogs"],
            "requires_input_from": ["code_analyzer"]
        }
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate or update documentation"""
        task_type = task.get("type", "")
        
        if task_type == "generate_readme":
            return await self._generate_readme(task.get("project_info", {}))
        elif task_type == "generate_api_docs":
            return await self._generate_api_docs(task.get("api_spec", {}))
        elif task_type == "update_changelog":
            return await self._update_changelog(task.get("changes", []))
        else:
            return {"error": f"Unknown task type: {task_type}"}
    
    async def _generate_readme(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a README file"""
        await asyncio.sleep(1.5)
        
        project_name = project_info.get("name", "Project")
        description = project_info.get("description", "A sample project")
        
        readme_content = f"""# {project_name}

{description}

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from {project_name.lower()} import main
main.run()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
"""
        
        return {
            "content": readme_content,
            "sections": ["title", "description", "installation", "usage", "contributing", "license"],
            "estimated_read_time": "2 minutes"
        }
    
    async def _generate_api_docs(self, api_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API documentation"""
        await asyncio.sleep(2)
        
        return {
            "documentation": {
                "endpoints": len(api_spec.get("endpoints", [])),
                "models": len(api_spec.get("models", [])),
                "examples": 15
            },
            "formats": ["html", "markdown", "pdf"],
            "coverage": "95%"
        }
    
    async def _update_changelog(self, changes: List[str]) -> Dict[str, Any]:
        """Update project changelog"""
        await asyncio.sleep(0.8)
        
        return {
            "changelog_entry": {
                "version": "1.0.1",
                "date": "2025-06-14",
                "changes": changes
            },
            "format": "keepachangelog"
        }

class TestingAgent(AgentBase):
    """Agent specialized in test generation and execution"""
    # Pytest will not collect this as a test class if it does not start with 'Test' or does not inherit from 'object' only.
    # If you want this to be collected as a test, rename to 'TestTestingAgent' and remove __init__, or use pytest.mark.usefixtures.
    def __init__(self):
        super().__init__("testing_agent", "Testing Agent")
    
    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input for testing needs"""
        return {
            "analysis_type": "test_analysis",
            "input_type": input_data.get("type", "unknown"),
            "test_coverage": "82%",
            "test_recommendations": ["Add edge case tests", "Improve mock coverage"]
        }
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents for testing tasks"""
        return {
            "coordination_status": "ready",
            "can_test": ["code_analyzer", "documentation_agent"],
            "testing_capabilities": ["unit tests", "integration tests", "coverage reports"]
        }
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate or run tests"""
        task_type = task.get("type", "")
        
        if task_type == "generate_tests":
            return await self._generate_tests(task.get("code", ""))
        elif task_type == "run_tests":
            return await self._run_tests(task.get("test_path", ""))
        elif task_type == "coverage_report":
            return await self._generate_coverage_report(task.get("project_path", ""))
        else:
            return {"error": f"Unknown task type: {task_type}"}
    
    async def _generate_tests(self, code: str) -> Dict[str, Any]:
        """Generate unit tests for code"""
        await asyncio.sleep(1.2)
        
        return {
            "test_cases": [
                {"name": "test_function_valid_input", "type": "positive"},
                {"name": "test_function_invalid_input", "type": "negative"},
                {"name": "test_function_edge_cases", "type": "edge_case"}
            ],
            "coverage_estimate": "85%",
            "test_framework": "pytest"
        }
    
    async def _run_tests(self, test_path: str) -> Dict[str, Any]:
        """Run existing tests"""
        await asyncio.sleep(3)
        
        return {
            "results": {
                "total": 45,
                "passed": 42,
                "failed": 2,
                "skipped": 1
            },
            "duration": "2.34s",
            "coverage": "87%"
        }
    
    async def _generate_coverage_report(self, project_path: str) -> Dict[str, Any]:
        """Generate test coverage report"""
        await asyncio.sleep(2.5)
        
        return {
            "overall_coverage": "87%",
            "files": [
                {"file": "main.py", "coverage": "95%"},
                {"file": "utils.py", "coverage": "78%"},
                {"file": "models.py", "coverage": "92%"}
            ],
            "uncovered_lines": 45,
            "report_formats": ["html", "xml", "json"]
        }
