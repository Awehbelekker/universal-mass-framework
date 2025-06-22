import pytest
import asyncio
from core.workflow_engine import WorkflowEngine
from agents.creative.creative_director_agent import CreativeDirectorAgent
from agents.research.market_research_agent import MarketResearchAgent
from agents.development.system_architect_agent import SystemArchitectAgent

@pytest.mark.asyncio
async def test_basic_app_generation_workflow():
    # Instantiate agents
    creative_agent = CreativeDirectorAgent()
    market_agent = MarketResearchAgent()
    architect_agent = SystemArchitectAgent()
    agents = {
        "creative_director": creative_agent,
        "market_researcher": market_agent,
        "system_architect": architect_agent
    }
    # Create workflow engine
    engine = WorkflowEngine(agents)
    # Define workflow steps
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
            "dependencies": ["step_1"]
        },
        {
            "name": "Design Architecture",
            "agent_id": "system_architect",
            "task_type": "design_architecture",
            "task_params": {},
            "dependencies": ["step_2"]
        }
    ]
    workflow_id = engine.create_workflow(
        name="App Generation Workflow",
        description="End-to-end app generation with creative, market, and architecture agents.",
        steps_config=steps
    )
    # Execute workflow
    result = await engine.execute_workflow_by_id(workflow_id)
    assert result["status"] in ("completed", "partial")
    assert len(result["step_results"]) == 3
    assert any("creative_concept" in (step["result"] or {}) for step in result["step_results"])
    assert any("market_opportunity_score" in (step["result"] or {}) for step in result["step_results"])
    assert any("system_architecture" in (step["result"] or {}) for step in result["step_results"])
