from core.agent_base import AgentBase, AgentMessage
from typing import Dict, Any, List
from data_sources.live_data_orchestrator import LiveDataOrchestrator

class SystemArchitectAgent(AgentBase):
    """
    ROLE: Design optimal technical architecture and technology stack
    RESPONSIBILITIES:
    - Analyze app requirements and design system architecture
    - Select optimal technology stack for performance and scalability
    - Define API specifications and data flow
    - Plan deployment and infrastructure requirements
    - Ensure security and performance optimization
    """
    def __init__(self):
        super().__init__("system_architect", "system_architecture")
        self.live_data = LiveDataOrchestrator()

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        # Use live data for technology trends
        tech_trends = await self.live_data.get_technology_trends(tech_categories=task_data.get("tech_categories", ["frontend", "backend"]))
        return {
            "system_architecture": "Architecture diagram",
            "technology_stack": ["FastAPI", "React", "PostgreSQL"],
            "api_specifications": {"endpoints": ["/api/v1/resource"]},
            "database_schema": "Schema SQL",
            "security_plan": "OAuth2, JWT",
            "performance_requirements": {"response_time": "<200ms"},
            "deployment_strategy": "Docker, Kubernetes",
            "tech_trends": tech_trends.get("frameworks", {})
        }

    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"analysis": "Requirements analyzed."}

    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        return {"coordination": "Coordinated with technical agents."}

    async def select_technology_stack(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        # Use live data for technology trends
        tech_trends = await self.live_data.get_technology_trends(tech_categories=["frontend", "backend"])
        return {"stack": ["FastAPI", "React"], "trends": tech_trends.get("frameworks", {})}
