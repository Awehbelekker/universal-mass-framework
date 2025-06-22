"""
Tests for Phase 1.2 - Multi-Agent Collaboration and Advanced AI Features
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from core.agent_collaboration_manager import collaboration_manager, CollaborationSession, SubTask, TaskPriority
from agents.ai_agents.project_analysis_agent import ProjectAnalysisAgent
from agents.ai_agents.intelligent_code_suggestion_engine import IntelligentCodeSuggestionEngine, CodeSuggestion, CodeContext

# Don't use global client - each test class will create its own

class TestMultiAgentCollaboration:
    """Tests for multi-agent collaboration functionality"""
    
    def setup_method(self):
        """Setup test environment with proper app factory"""
        from main import create_app
        from core.auth_service import AuthenticationService
        from core.database_manager import DatabaseManager
        
        # Create test database and auth service
        self.db_manager = DatabaseManager(":memory:")
        self.auth_service = AuthenticationService(
            secret_key="test_secret_key",
            token_expiry_hours=1,
            db_manager=self.db_manager
        )
        
        # Create app with injected dependencies
        self.app = create_app(self.auth_service, self.db_manager)
        
        # Inject collaboration manager (it should already be injected by create_app)
        from core.agent_collaboration_manager import collaboration_manager
        self.app.state.collaboration_manager = collaboration_manager
        
        from fastapi.testclient import TestClient
        self.client = TestClient(self.app)
    
    def test_collaboration_manager_initialization(self):
        """Test collaboration manager initializes correctly"""
        assert collaboration_manager is not None
        assert hasattr(collaboration_manager, 'agent_registry')
        assert hasattr(collaboration_manager, 'active_sessions')
        assert hasattr(collaboration_manager, 'collaboration_templates')
    
    def test_collaboration_templates_loaded(self):
        """Test that collaboration templates are loaded"""
        templates = collaboration_manager.collaboration_templates
        assert len(templates) > 0
        assert 'full_development_cycle' in templates
        assert 'code_review_and_improvement' in templates
        assert 'debugging_and_fixing' in templates
        
        # Verify template structure
        full_cycle = templates['full_development_cycle']
        assert 'description' in full_cycle
        assert 'stages' in full_cycle
        assert len(full_cycle['stages']) > 0
    
    @pytest.mark.asyncio
    async def test_agent_registration(self):
        """Test agent registration with collaboration manager"""
        # Create mock agent
        mock_agent = Mock()
        mock_agent.agent_id = "test_agent"
        mock_agent.name = "Test Agent"
        
        # Register agent
        collaboration_manager.register_agent(mock_agent)
        
        # Verify registration
        assert "test_agent" in collaboration_manager.agent_registry
        assert collaboration_manager.agent_registry["test_agent"] == mock_agent
    
    @pytest.mark.asyncio
    async def test_orchestrate_multi_agent_task(self):
        """Test multi-agent task orchestration"""
        # Mock LLM service for planning
        with patch('core.agent_collaboration_manager.llm_service') as mock_llm:
            mock_llm.chat_completion = AsyncMock()
            mock_llm.chat_completion.return_value.content = json.dumps({
                "agents": ["ai_code_generator"],
                "subtasks": [
                    {
                        "id": "task1",
                        "description": "Generate code",
                        "assigned_agent": "ai_code_generator",
                        "dependencies": [],
                        "priority": "high",
                        "estimated_duration": 10
                    }
                ],
                "execution_strategy": "sequential",
                "aggregation_method": "direct"
            })
            
            # Mock agent for execution
            mock_agent = AsyncMock()
            mock_agent.agent_id = "ai_code_generator"
            mock_agent.process_task.return_value = {"success": True, "result": "Generated code"}
            collaboration_manager.register_agent(mock_agent)
            
            # Start collaboration
            session = await collaboration_manager.orchestrate_multi_agent_task(
                task_description="Generate a simple Python function",
                context={"language": "python"}
            )
            
            # Verify session created
            assert session is not None
            assert session.main_task == "Generate a simple Python function"
            assert len(session.subtasks) == 1
            assert session.subtasks[0].assigned_agent == "ai_code_generator"

class TestCollaborationAPIEndpoints:
    """Tests for collaboration API endpoints"""
    
    def setup_method(self):
        """Set up test app with mocked collaboration manager"""
        from main import create_app
        from core.auth_service import AuthenticationService
        from core.database_manager import DatabaseManager
        
        # Create test database and auth service
        self.db_manager = DatabaseManager(":memory:")
        self.auth_service = AuthenticationService(
            secret_key="test_secret_key",
            token_expiry_hours=1,
            db_manager=self.db_manager
        )
        
        # Create mock collaboration manager
        self.mock_manager = Mock()
        
        # Create app with real auth service and mock collaboration manager
        self.app = create_app(self.auth_service, self.db_manager)
        
        # Inject mock collaboration manager into app.state
        self.app.state.collaboration_manager = self.mock_manager
        
        from fastapi.testclient import TestClient
        self.client = TestClient(self.app)
    
    def test_orchestrate_endpoint(self):
        """Test /api/collaboration/orchestrate endpoint"""
        mock_session = Mock()
        mock_session.id = "session123"
        mock_session.status = Mock()
        mock_session.status.value = "planning"
        mock_session.main_task = "Test task"
        mock_session.participating_agents = ["agent1"]
        mock_session.subtasks = []
        mock_session.created_at.isoformat.return_value = "2025-06-14T10:00:00"
        
        self.mock_manager.orchestrate_multi_agent_task = AsyncMock(return_value=mock_session)
        
        response = self.client.post("/api/collaboration/orchestrate", json={
            "task_description": "Test task",
            "context": {"test": "data"},
            "template": "full_development_cycle"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "session123"
        assert data["status"] == "planning"
        assert data["main_task"] == "Test task"
    
    def test_get_collaboration_status(self):
        """Test /api/collaboration/status/{session_id} endpoint"""
        self.mock_manager.get_collaboration_status = AsyncMock(return_value={
            "session_id": "session123",
            "status": "completed",
            "main_task": "Test task",
            "total_subtasks": 3,            "completed_subtasks": 3
        })
        
        response = self.client.get("/api/collaboration/status/session123")
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "session123"
        assert data["status"] == "completed"
    
    def test_list_collaboration_sessions(self):
        """Test /api/collaboration/sessions endpoint"""
        # Return simple serializable data without circular references
        self.mock_manager.list_active_sessions = AsyncMock(return_value=[
            {
                "session_id": "session1",
                "status": "executing",
                "main_task": "Task 1",
                "created_at": "2025-06-14T10:00:00",
                "participating_agents": ["agent1"]
            }
        ])
        
        response = self.client.get("/api/collaboration/sessions")
        
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
        assert len(data["sessions"]) == 1
        assert data["sessions"][0]["session_id"] == "session1"
    
    def test_get_collaboration_templates(self):
        """Test /api/collaboration/templates endpoint"""
        self.mock_manager.collaboration_templates = {
            "full_development_cycle": {"description": "Full cycle"},
            "bug_fixing": {"description": "Bug fixing"},
            "documentation": {"description": "Documentation"}
        }
        
        response = self.client.get("/api/collaboration/templates")
        
        assert response.status_code == 200
        data = response.json()
        assert "templates" in data
        assert len(data["templates"]) == 3
        assert "full_development_cycle" in data["templates"]

class TestProjectAnalysisAgent:
    """Tests for Project Analysis Agent"""
    
    def test_agent_initialization(self):
        """Test project analysis agent initializes correctly"""
        agent = ProjectAnalysisAgent()
        assert agent.agent_id == "ai_project_analyzer"
        assert agent.name == "AI Project Analysis Agent"
        assert len(agent.capabilities) > 0
        assert "project_structure_analysis" in agent.capabilities
    
    @pytest.mark.asyncio
    async def test_process_task_project_structure(self):
        """Test project structure analysis task"""
        agent = ProjectAnalysisAgent()
        
        with patch('os.path.exists', return_value=True):
            with patch('os.walk', return_value=[
                ('.', ['src'], ['main.py', 'requirements.txt']),
                ('./src', [], ['app.py', 'utils.py'])
            ]):
                with patch('core.llm_service.llm_service.chat_completion', new_callable=AsyncMock) as mock_chat:
                    mock_chat.return_value.content = "AI analysis of project structure"
                    
                    task = {
                        "type": "analyze_project_structure",
                        "project_path": "/test/project"
                    }
                    
                    result = await agent.process_task(task)
                    
                    assert result["success"] is True
                    assert result["analysis_type"] == "project_structure"
                    assert "structure" in result
                    assert "file_stats" in result
                    assert "ai_insights" in result
    
    @pytest.mark.asyncio
    async def test_process_task_dependencies(self):
        """Test dependency analysis task"""
        agent = ProjectAnalysisAgent()
        
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data="requests==2.25.1\nflask==2.0.1")):
                with patch('core.llm_service.llm_service.chat_completion', new_callable=AsyncMock) as mock_chat:
                    mock_chat.return_value.content = "AI analysis of dependencies"
                    
                    task = {
                        "type": "analyze_dependencies",
                        "project_path": "/test/project"
                    }
                    
                    result = await agent.process_task(task)
                    
                    assert result["success"] is True
                    assert result["analysis_type"] == "dependencies"
                    assert "dependencies" in result
                    assert "analysis" in result
    
    @pytest.mark.asyncio
    async def test_process_task_code_quality(self):
        """Test code quality assessment task"""
        agent = ProjectAnalysisAgent()
        
        with patch('os.walk', return_value=[
            ('.', [], ['test.py'])
        ]):
            with patch('builtins.open', mock_open(read_data="def test_function():\n    print('test')\n")):
                with patch('core.llm_service.llm_service.chat_completion', new_callable=AsyncMock) as mock_chat:
                    mock_chat.return_value.content = "AI code quality assessment"
                    
                    task = {
                        "type": "assess_code_quality",
                        "project_path": "/test/project"
                    }
                    
                    result = await agent.process_task(task)
                    
                    assert result["success"] is True
                    assert result["analysis_type"] == "code_quality"
                    assert "metrics" in result
                    assert "quality_score" in result

class TestIntelligentCodeSuggestionEngine:
    """Tests for Intelligent Code Suggestion Engine"""
    
    def test_agent_initialization(self):
        """Test code suggestion engine initializes correctly"""
        engine = IntelligentCodeSuggestionEngine()
        assert engine.agent_id == "ai_code_suggestion_engine"
        assert engine.name == "Intelligent Code Suggestion Engine"
        assert len(engine.capabilities) > 0
        assert "code_completion" in engine.capabilities
    
    @pytest.mark.asyncio
    async def test_process_task_get_suggestions(self):
        """Test getting code suggestions"""
        engine = IntelligentCodeSuggestionEngine()
        
        task = {
            "type": "get_suggestions",
            "code": "def hello():\n    print('hello')",
            "language": "python",
            "cursor_position": 10
        }
        
        with patch('core.llm_service.llm_service.chat_completion', new_callable=AsyncMock) as mock_chat:
            mock_chat.return_value.content = json.dumps([{
                "completion": "world')",
                "description": "Complete the string",
                "confidence": 0.9,
                "type": "string"
            }])
            
            result = await engine.process_task(task)
            
            assert result["success"] is True
            assert "suggestions" in result
            assert "context" in result
    
    @pytest.mark.asyncio
    async def test_process_task_complete_code(self):
        """Test code completion functionality"""
        engine = IntelligentCodeSuggestionEngine()
        
        task = {
            "type": "complete_code",
            "code": "import os\nprint(os.path.",
            "cursor_position": 20,
            "language": "python"
        }
        
        with patch('core.llm_service.llm_service.chat_completion', new_callable=AsyncMock) as mock_chat:
            mock_chat.return_value.content = json.dumps([{
                "completion": "join(",
                "description": "os.path.join function",
                "confidence": 0.95,
                "type": "method"
            }])
            
            result = await engine.process_task(task)
            
            assert result["success"] is True
            assert "completions" in result
            assert len(result["completions"]) > 0
    
    @pytest.mark.asyncio
    async def test_process_task_refactor_code(self):
        """Test code refactoring suggestions"""
        engine = IntelligentCodeSuggestionEngine()
        
        task = {
            "type": "refactor_code",
            "code": "def long_function():\n    x = 1\n    y = 2\n    return x + y",
            "refactor_type": "general",
            "language": "python"
        }
        
        with patch('core.llm_service.llm_service.chat_completion', new_callable=AsyncMock) as mock_chat:
            mock_chat.return_value.content = json.dumps([{
                "type": "simplify",
                "description": "Simplify the function",
                "original_code": "def long_function():\n    x = 1\n    y = 2\n    return x + y",
                "refactored_code": "def long_function():\n    return 1 + 2",
                "benefits": ["Reduced complexity"],
                "confidence": 0.8
            }])
            
            result = await engine.process_task(task)
            
            assert result["success"] is True
            assert "refactoring_suggestions" in result
            assert len(result["refactoring_suggestions"]) > 0
    
    def test_code_context_building(self):
        """Test code context building functionality"""
        engine = IntelligentCodeSuggestionEngine()
        
        # Test Python context building
        code = """
import os
import sys

class TestClass:
    def test_method(self):
        x = 1
        return x

def test_function():
    pass
"""
        
        asyncio.run(self._test_context_building(engine, code))
    
    async def _test_context_building(self, engine, code):
        """Helper method for testing context building"""
        context = await engine._build_python_context(code, CodeContext(
            file_path="test.py",
            language="python",
            imports=[],
            classes=[],
            functions=[],
            variables=[],
            surrounding_code=code,
            project_context={}
        ))
        
        assert "os" in context.imports
        assert "sys" in context.imports
        assert "TestClass" in context.classes
        assert "test_function" in context.functions

class TestProjectAnalysisAPIEndpoints:
    """Tests for Project Analysis API endpoints"""
    
    def setup_method(self):
        """Setup test environment with proper app factory"""
        from main import create_app
        from core.auth_service import AuthenticationService
        from core.database_manager import DatabaseManager
        
        # Create test database and auth service
        self.db_manager = DatabaseManager(":memory:")
        self.auth_service = AuthenticationService(
            secret_key="test_secret_key",
            token_expiry_hours=1,
            db_manager=self.db_manager
        )
        
        # Create app with injected dependencies
        self.app = create_app(self.auth_service, self.db_manager)
        
        from fastapi.testclient import TestClient
        self.client = TestClient(self.app)
    
    def test_analyze_project_endpoint(self):
        """Test /api/ai/analyze-project endpoint"""
        with patch('main.sample_agents') as mock_agents:
            mock_agent = AsyncMock()
            mock_agent.process_task.return_value = {
                "success": True,
                "analysis_type": "full_project_analysis",
                "results": "Analysis complete"
            }
            mock_agents.__getitem__.return_value = mock_agent
            
            response = self.client.post("/api/ai/analyze-project", json={
                "analysis_type": "full_project_analysis",
                "project_path": "/test/project"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
    
    def test_analyze_project_structure_endpoint(self):
        """Test /api/ai/analyze-project-structure endpoint"""
        with patch('main.sample_agents') as mock_agents:
            mock_agent = AsyncMock()
            mock_agent.process_task.return_value = {
                "success": True,
                "analysis_type": "project_structure",
                "structure": {}
            }
            mock_agents.__getitem__.return_value = mock_agent
            
            response = self.client.post("/api/ai/analyze-project-structure", json={
                "project_path": "/test/project"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
    
    def test_get_code_suggestions_endpoint(self):
        """Test /api/ai/get-code-suggestions endpoint"""
        with patch('main.sample_agents') as mock_agents:
            mock_agent = AsyncMock()
            mock_agent.process_task.return_value = {
                "success": True,
                "suggestions": [],
                "context": {}
            }
            mock_agents.__getitem__.return_value = mock_agent
            
            response = self.client.post("/api/ai/get-code-suggestions", json={
                "code": "def test():",
                "language": "python"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "suggestions" in data
    
    def test_complete_code_endpoint(self):
        """Test /api/ai/complete-code endpoint"""
        with patch('main.sample_agents') as mock_agents:
            mock_agent = AsyncMock()
            mock_agent.process_task.return_value = {
                "success": True,
                "completions": []
            }
            mock_agents.__getitem__.return_value = mock_agent
            
            response = self.client.post("/api/ai/complete-code", json={
                "code": "import os\nprint(os.",
                "cursor_position": 15
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "completions" in data

class TestPhase12Integration:
    """Integration tests for Phase 1.2 features"""
    
    def test_agents_registered_in_collaboration_manager(self):
        """Test that all agents are properly registered"""
        # Check that sample agents exist
        from main import sample_agents
        
        assert "ai_project_analyzer" in sample_agents
        assert "ai_code_suggestion_engine" in sample_agents
        
        # Check that they're registered with collaboration manager
        assert "ai_project_analyzer" in collaboration_manager.agent_registry
        assert "ai_code_suggestion_engine" in collaboration_manager.agent_registry
    
    @pytest.mark.asyncio
    async def test_end_to_end_collaboration_workflow(self):
        """Test complete collaboration workflow"""
        # This would test a full workflow from start to finish
        # Including task orchestration, agent execution, and result aggregation
        # Patch the correct LLM service import path
        with patch('core.agent_collaboration_manager.llm_service.chat_completion', new_callable=AsyncMock) as mock_chat:
            mock_chat.return_value.content = json.dumps({
                "agents": ["ai_code_generator", "ai_testing_agent"],
                "subtasks": [
                    {
                        "id": "generate_code",
                        "description": "Generate Python function",
                        "assigned_agent": "ai_code_generator",
                        "dependencies": [],
                        "priority": "high",
                        "estimated_duration": 5
                    },
                    {
                        "id": "test_code",
                        "description": "Generate tests for the function",
                        "assigned_agent": "ai_testing_agent",
                        "dependencies": ["generate_code"],
                        "priority": "medium",
                        "estimated_duration": 3
                    }
                ],
                "execution_strategy": "sequential",
                "aggregation_method": "combine"
            })
            # Mock agent responses
            from main import sample_agents
            for agent_id, agent in sample_agents.items():
                if hasattr(agent, 'process_task'):
                    agent.process_task = AsyncMock(return_value={
                        "success": True,
                        "result": f"Result from {agent_id}"
                    })
            # Start collaboration
            session = await collaboration_manager.orchestrate_multi_agent_task(
                task_description="Create a Python function with tests",
                context={"language": "python", "function_name": "fibonacci"}
            )
            print("DEBUG: session.subtasks:", session.subtasks)
            # Verify the workflow completed
            assert session is not None
            assert len(session.subtasks) == 2
            # Additional assertions would check the execution flow

def mock_open(read_data):
    """Helper function to create mock file opening"""
    from unittest.mock import mock_open as orig_mock_open
    return orig_mock_open(read_data=read_data)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
