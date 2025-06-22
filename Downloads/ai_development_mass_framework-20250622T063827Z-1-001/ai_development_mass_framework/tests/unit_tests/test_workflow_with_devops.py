import pytest
import asyncio
from core.workflow_engine import WorkflowEngine
from agents.creative.creative_director_agent import CreativeDirectorAgent
from agents.research.market_research_agent import MarketResearchAgent
from agents.development.system_architect_agent import SystemArchitectAgent
from agents.development.devops_agent import DevOpsAgent

@pytest.mark.asyncio
async def test_workflow_with_devops():
    creative_agent = CreativeDirectorAgent()
    market_agent = MarketResearchAgent()
    architect_agent = SystemArchitectAgent()
    devops_agent = DevOpsAgent()
    agents = {
        "creative_director": creative_agent,
        "market_researcher": market_agent,
        "system_architect": architect_agent,
        "devops_agent": devops_agent
    }
    engine = WorkflowEngine(agents)
    steps = [
        {
            "name": "Generate App Concept",
            "agent_id": "creative_director",
            "task_type": "generate_concept",
            "task_params": {"topic": "AI Fitness"}
        },
        {
            "name": "Validate Market",
            "agent_id": "market_researcher",
            "task_type": "validate_market",
            "task_params": {},
        },
        {
            "name": "Design Architecture",
            "agent_id": "system_architect",
            "task_type": "design_architecture",
            "task_params": {},
            "dependencies": ["step_1", "step_2"]
        },
        {
            "name": "Deploy Application",
            "agent_id": "devops_agent",
            "task_type": "deploy_app",
            "task_params": {},
            "dependencies": ["step_3"]
        }
    ]
    workflow_id = engine.create_workflow(
        name="App Generation with Deployment Workflow",
        description="Parallel creative and market analysis, then technical design, then deployment.",
        steps_config=steps
    )
    result = await engine.execute_workflow_by_id(workflow_id)
    assert result["status"] in ("completed", "partial")
    assert len(result["step_results"]) == 4
    # Ensure all agents participated
    assert any(step["agent_id"] == "devops_agent" for step in result["step_results"])
    assert any("deployment_configs" in (step["result"] or {}) for step in result["step_results"])
