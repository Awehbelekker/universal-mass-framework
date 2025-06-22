import pytest
import asyncio
from core.workflow_engine import WorkflowEngine
from agents.creative.creative_director_agent import CreativeDirectorAgent
from agents.research.market_research_agent import MarketResearchAgent
from agents.development.system_architect_agent import SystemArchitectAgent

@pytest.mark.asyncio
async def test_parallel_workflow():
    creative_agent = CreativeDirectorAgent()
    market_agent = MarketResearchAgent()
    architect_agent = SystemArchitectAgent()
    agents = {
        "creative_director": creative_agent,
        "market_researcher": market_agent,
        "system_architect": architect_agent
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
        }
    ]
    workflow_id = engine.create_workflow(
        name="Parallel App Generation Workflow",
        description="Parallel creative and market analysis, then technical design.",
        steps_config=steps
    )
    result = await engine.execute_workflow_by_id(workflow_id)
    assert result["status"] in ("completed", "partial")
    assert len(result["step_results"]) == 3
    # Ensure both creative and market steps completed before architecture
    creative_done = any(step["agent_id"] == "creative_director" for step in result["step_results"])
    market_done = any(step["agent_id"] == "market_researcher" for step in result["step_results"])
    arch_done = any(step["agent_id"] == "system_architect" for step in result["step_results"])
    assert creative_done and market_done and arch_done
