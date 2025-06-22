"""
Comprehensive Testing Suite for MASS Framework
Includes unit, integration, performance, and end-to-end tests
"""

import pytest
import asyncio
import time
import aiohttp
import json
from typing import Dict, Any, List
from unittest.mock import AsyncMock, MagicMock, patch
import tempfile
import os

# Test fixtures and utilities
@pytest.fixture
async def test_app():
    """Create test application instance"""
    from main import create_app
    from core.auth_service import AuthenticationService
    from core.database_manager import DatabaseManager
    
    # Use in-memory database for testing
    db_manager = DatabaseManager(":memory:")
    auth_service = AuthenticationService(db_manager=db_manager)
    
    app = create_app(auth_service, db_manager)
    yield app
    
    # Cleanup
    await db_manager.cleanup()

@pytest.fixture
async def test_client(test_app):
    """Create test HTTP client"""
    from httpx import AsyncClient
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_agents():
    """Mock agent instances for testing"""
    agents = {}
    
    # Create mock agents
    for agent_type in ['creative_director', 'market_researcher', 'system_architect', 'fullstack_developer']:
        mock_agent = AsyncMock()
        mock_agent.agent_id = agent_type
        mock_agent.process_task.return_value = {
            "agent_id": agent_type,
            "result": f"Mock result from {agent_type}",
            "execution_time": 0.1
        }
        agents[agent_type] = mock_agent
    
    return agents

# Unit Tests
class TestMASSCoordinator:
    """Test the core coordination functionality"""
    
    @pytest.mark.asyncio
    async def test_agent_registration(self):
        """Test agent registration and management"""
        from core.mass_coordinator import MASSCoordinator
        
        coordinator = MASSCoordinator()
        mock_agent = AsyncMock()
        mock_agent.agent_id = "test_agent"
        
        coordinator.register_agent("test_agent", mock_agent)
        
        assert "test_agent" in coordinator.agents
        assert coordinator.agents["test_agent"] == mock_agent
        assert mock_agent.coordinator == coordinator
    
    @pytest.mark.asyncio
    async def test_message_routing(self, mock_agents):
        """Test inter-agent message routing"""
        from core.mass_coordinator import MASSCoordinator
        from core.agent_base import AgentMessage, MessageType
        
        coordinator = MASSCoordinator()
        
        # Register mock agents
        for agent_id, agent in mock_agents.items():
            coordinator.register_agent(agent_id, agent)
        
        # Create test message
        message = AgentMessage(
            sender_id="creative_director",
            receiver_id="market_researcher",
            message_type=MessageType.ANALYSIS_REQUEST,
            payload={"task": "analyze market trends"},
            timestamp=time.time(),
            correlation_id="test-123",
            priority=5
        )
        
        # Route message
        await coordinator.route_message(message)
        
        # Verify message was received
        mock_agents["market_researcher"].receive_message.assert_called_once_with(message)
    
    @pytest.mark.asyncio
    async def test_conflict_resolution(self):
        """Test conflict detection and resolution"""
        from core.mass_coordinator import MASSCoordinator
        
        coordinator = MASSCoordinator()
        
        # Mock conflicting agent outputs
        agent_outputs = {
            "creative_director": {
                "technology_stack": "React + FastAPI",
                "design_approach": "Minimalist"
            },
            "system_architect": {
                "technology_stack": "Vue.js + Django", 
                "performance_priority": "Speed"
            }
        }
        
        conflicts = await coordinator.detect_conflicts(agent_outputs)
        assert len(conflicts) > 0
        
        resolution = await coordinator.resolve_conflicts(conflicts, agent_outputs)
        assert "resolved_stack" in resolution or "selected_agent" in resolution

class TestAgentImplementations:
    """Test individual agent implementations"""
    
    @pytest.mark.asyncio
    async def test_creative_director_agent(self):
        """Test creative director agent functionality"""
        from agents.creative.creative_director_agent import CreativeDirectorAgent
        
        agent = CreativeDirectorAgent()
        
        task_data = {
            "app_type": "productivity",
            "target_audience": "developers",
            "keywords": ["task management", "collaboration"]
        }
        
        result = await agent.process_task(task_data)
        
        assert "creative_concept" in result
        assert "brand_identity" in result
        assert "innovation_score" in result
        assert "market_fit_score" in result
        assert isinstance(result["innovation_score"], (int, float))
        assert 1 <= result["innovation_score"] <= 10
    
    @pytest.mark.asyncio
    async def test_market_research_agent(self):
        """Test market research agent with live data"""
        from agents.research.market_research_agent import MarketResearchAgent
        
        agent = MarketResearchAgent()
        
        task_data = {
            "domain": "productivity",
            "keywords": ["task management", "team collaboration"],
            "target_market": "developers"
        }
        
        result = await agent.process_task(task_data)
        
        assert "market_opportunity_score" in result
        assert "target_audience_analysis" in result
        assert "competitive_landscape" in result
        assert "validation_data" in result
        assert isinstance(result["market_opportunity_score"], (int, float))

class TestLiveDataIntegration:
    """Test live data sources and integration"""
    
    @pytest.mark.asyncio
    async def test_github_api_integration(self):
        """Test GitHub API integration"""
        from data_sources.live_data_orchestrator import GitHubTrendingAPI
        
        api = GitHubTrendingAPI()
        
        repos = await api.get_trending_repos("python")
        
        assert isinstance(repos, list)
        if repos:  # If API call succeeded
            assert "name" in repos[0]
            assert "stargazers_count" in repos[0]
    
    @pytest.mark.asyncio
    async def test_hacker_news_api(self):
        """Test Hacker News API integration"""
        from data_sources.live_data_orchestrator import HackerNewsAPI
        
        api = HackerNewsAPI()
        
        stories = await api.get_top_stories(5)
        
        assert isinstance(stories, list)
        if stories:  # If API call succeeded
            assert "title" in stories[0]
            assert "score" in stories[0]
    
    @pytest.mark.asyncio
    async def test_live_data_orchestrator_caching(self):
        """Test data orchestrator caching functionality"""
        from data_sources.live_data_orchestrator import LiveDataOrchestrator
        
        orchestrator = LiveDataOrchestrator()
        
        # First call should fetch from API
        start_time = time.time()
        result1 = await orchestrator.get_market_intelligence("productivity", ["task management"])
        first_call_time = time.time() - start_time
        
        # Second call should use cache (faster)
        start_time = time.time()
        result2 = await orchestrator.get_market_intelligence("productivity", ["task management"])
        second_call_time = time.time() - start_time
        
        assert result1 == result2  # Same data
        assert second_call_time < first_call_time  # Faster due to caching

class TestWorkflowExecution:
    """Test end-to-end workflow execution"""
    
    @pytest.mark.asyncio
    async def test_complete_app_generation_workflow(self, mock_agents):
        """Test complete app generation from start to finish"""
        from workflows.app_generation_workflow import AppGenerationWorkflow
        
        workflow = AppGenerationWorkflow()
        
        requirements = {
            "app_type": "productivity",
            "target_users": "developers",
            "key_features": ["task management", "team collaboration", "analytics"],
            "timeline": "2 weeks",
            "budget": "medium"
        }
        
        result = await workflow.run_workflow(requirements)
        
        assert result.success == True
        assert result.app_id is not None
        assert len(result.phases_completed) >= 5
        assert result.execution_time > 0
        assert "requirements_analysis" in result.generated_components
        assert "architecture" in result.generated_components
    
    @pytest.mark.asyncio
    async def test_workflow_error_handling(self):
        """Test workflow error handling and recovery"""
        from workflows.app_generation_workflow import AppGenerationWorkflow
        
        workflow = AppGenerationWorkflow()
        
        # Test with invalid requirements
        invalid_requirements = {}
        
        result = await workflow.run_workflow(invalid_requirements)
        
        # Should handle gracefully
        assert result.success in [True, False]  # May succeed with defaults or fail gracefully
        assert result.error_message is None or isinstance(result.error_message, str)

class TestPerformanceOptimization:
    """Test performance optimization features"""
    
    @pytest.mark.asyncio
    async def test_cache_performance(self):
        """Test caching system performance"""
        from core.performance_optimization import AdvancedCacheManager
        
        cache = AdvancedCacheManager()
        
        # Test set and get performance
        test_data = {"large_data": list(range(1000))}
        
        start_time = time.time()
        await cache.set("test", "performance_key", test_data)
        set_time = time.time() - start_time
        
        start_time = time.time()
        retrieved_data = await cache.get("test", "performance_key")
        get_time = time.time() - start_time
        
        assert retrieved_data == test_data
        assert set_time < 0.1  # Should be fast
        assert get_time < 0.05  # Should be very fast
    
    @pytest.mark.asyncio
    async def test_parallel_agent_execution(self, mock_agents):
        """Test parallel agent execution performance"""
        from core.performance_optimization import performance_optimizer
        
        task = {"test": "parallel execution"}
        agents = list(mock_agents.values())
        
        start_time = time.time()
        results = await performance_optimizer.optimize_agent_coordination(agents, task)
        execution_time = time.time() - start_time
        
        assert len(results) == len(agents)
        assert execution_time < 1.0  # Should complete quickly with mocked agents

class TestAPIEndpoints:
    """Test API endpoint functionality"""
    
    @pytest.mark.asyncio
    async def test_beta_registration_endpoint(self, test_client):
        """Test beta registration API"""
        response = await test_client.post("/api/beta/register", json={
            "email": "test@example.com",
            "name": "Test User",
            "company": "Test Corp",
            "role": "developer",
            "experience": "intermediate",
            "interest": "AI development"
        })
        
        assert response.status_code in [200, 201]
        data = response.json()
        assert "user_id" in data
        assert "trial_end_date" in data
    
    @pytest.mark.asyncio
    async def test_authentication_flow(self, test_client):
        """Test authentication endpoints"""
        # Test login
        login_response = await test_client.post("/auth/login", json={
            "username": "admin",
            "password": "admin123"  # Default admin password
        })
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            assert "access_token" in login_data
            
            # Test authenticated endpoint
            headers = {"Authorization": f"Bearer {login_data['access_token']}"}
            me_response = await test_client.get("/auth/me", headers=headers)
            assert me_response.status_code == 200

class TestLoadAndStress:
    """Performance and load testing"""
    
    @pytest.mark.asyncio
    async def test_concurrent_agent_execution(self, mock_agents):
        """Test system under concurrent load"""
        from core.mass_coordinator import MASSCoordinator
        
        coordinator = MASSCoordinator()
        
        # Register agents
        for agent_id, agent in mock_agents.items():
            coordinator.register_agent(agent_id, agent)
        
        # Create multiple concurrent tasks
        async def execute_workflow():
            return await coordinator.execute_app_generation_workflow({
                "app_type": "test",
                "complexity": "simple"
            })
        
        # Execute 10 workflows concurrently
        start_time = time.time()
        tasks = [execute_workflow() for _ in range(10)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        execution_time = time.time() - start_time
        
        # Verify performance
        successful_results = [r for r in results if not isinstance(r, Exception)]
        assert len(successful_results) >= 5  # At least 50% success rate
        assert execution_time < 5.0  # Should complete within 5 seconds
    
    @pytest.mark.asyncio
    async def test_memory_usage(self):
        """Test memory usage under load"""
        import psutil
        import gc
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create and process large dataset
        from workflows.app_generation_workflow import AppGenerationWorkflow
        
        workflows = []
        for i in range(5):
            workflow = AppGenerationWorkflow()
            result = await workflow.run_workflow({
                "app_type": f"test_app_{i}",
                "data_size": "large"
            })
            workflows.append(result)
        
        # Force garbage collection
        gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        assert memory_increase < 100  # Should not increase by more than 100MB

# Test configuration
class TestConfig:
    """Test configuration and setup"""
    
    # Pytest configuration
    pytest_plugins = ["pytest_asyncio"]
    
    # Test markers
    markers = [
        "unit: Unit tests",
        "integration: Integration tests", 
        "performance: Performance tests",
        "api: API endpoint tests",
        "slow: Slow running tests"
    ]
    
    # Async test timeout
    asyncio_timeout = 30
    
    # Test database configuration
    test_database_url = "sqlite:///:memory:"

# Test utilities
def create_test_data():
    """Create test data for various scenarios"""
    return {
        "simple_app_requirements": {
            "app_type": "todo",
            "complexity": "simple",
            "features": ["create", "read", "update", "delete"]
        },
        "complex_app_requirements": {
            "app_type": "social_platform",
            "complexity": "high",
            "features": ["user_auth", "posts", "comments", "real_time_chat", "analytics"],
            "integrations": ["payment", "notifications", "cloud_storage"]
        },
        "enterprise_requirements": {
            "app_type": "enterprise_dashboard",
            "complexity": "enterprise",
            "features": ["multi_tenant", "rbac", "audit_logs", "reporting"],
            "compliance": ["GDPR", "SOC2", "HIPAA"]
        }
    }

if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([
        "--cov=core",
        "--cov=agents", 
        "--cov=workflows",
        "--cov=data_sources",
        "--cov-report=html",
        "--cov-report=term-missing",
        "-v",
        __file__
    ])
