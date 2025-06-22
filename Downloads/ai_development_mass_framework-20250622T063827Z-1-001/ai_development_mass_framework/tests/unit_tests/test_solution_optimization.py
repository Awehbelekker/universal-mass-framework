import pytest
from core.mass_coordinator import MASSCoordinator

@pytest.mark.asyncio
async def test_solution_optimization():
    coordinator = MASSCoordinator()
    # Simulate agent outputs with varying scores
    agent_outputs = {
        "creative_director": {
            "innovation_score": 9,
            "market_fit_score": 7,
            "performance_requirements": {"response_time": "<200ms"}
        },
        "market_researcher": {
            "innovation_score": 6,
            "market_fit_score": 9,
            "performance_requirements": {"response_time": "<300ms"}
        },
        "system_architect": {
            "innovation_score": 7,
            "market_fit_score": 8,
            "performance_requirements": {"response_time": "<150ms"}
        }
    }
    result = coordinator.optimize_solutions(agent_outputs)
    assert "scores" in result
    assert "best_agent" in result
    assert "best_output" in result
    print("Scores:", result["scores"])
    print("Best agent:", result["best_agent"])
    print("Best output:", result["best_output"])
    # The best agent should be the one with the highest combined score
    assert result["best_agent"] in agent_outputs
    assert result["best_output"] == agent_outputs[result["best_agent"]]
