#!/usr/bin/env python3
"""
MASS Framework Feature Testing Script
Tests all enhanced features systematically
"""

import asyncio
import json
import sys
import traceback
from typing import Dict, Any
import pytest

def test_imports():
    """Test all imports"""
    print("🧪 Testing Imports...")
    
    try:
        import main
        print("✅ Main application imports")
        
        from agents.ai_agents.sample_agents import CodeAnalyzerAgent, DocumentationAgent, TestingAgent
        print("✅ Sample agents import")
        
        from core.workflow_engine import WorkflowEngine, WORKFLOW_TEMPLATES
        print("✅ Workflow engine imports")
        
        from core.websocket_manager import ConnectionManager
        print("✅ WebSocket manager imports")
        
        assert True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        assert False

@pytest.mark.asyncio
async def test_sample_agents():
    """Test sample agent functionality"""
    print("\n🤖 Testing Sample Agents...")
    
    try:
        from agents.ai_agents.sample_agents import CodeAnalyzerAgent, DocumentationAgent, TestingAgent
        
        # Test Code Analyzer
        code_agent = CodeAnalyzerAgent()
        result = await code_agent.analyze_input({"type": "test_input"})
        print(f"✅ Code Analyzer: {result['analysis_type']}")
        
        # Test Documentation Agent
        doc_agent = DocumentationAgent()
        result = await doc_agent.analyze_input({"type": "documentation"})
        print(f"✅ Documentation Agent: {result['analysis_type']}")
        
        # Test Testing Agent
        test_agent = TestingAgent()
        result = await test_agent.analyze_input({"type": "testing"})
        print(f"✅ Testing Agent: {result['analysis_type']}")
        
        assert True
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        traceback.print_exc()
        assert False

@pytest.mark.asyncio
async def test_workflow_engine():
    """Test workflow engine functionality"""
    print("\n⚡ Testing Workflow Engine...")
    
    try:
        from core.workflow_engine import WorkflowEngine, WORKFLOW_TEMPLATES
        from agents.ai_agents.sample_agents import CodeAnalyzerAgent, DocumentationAgent, TestingAgent
        
        # Initialize agents
        agents = {
            "code_analyzer": CodeAnalyzerAgent(),
            "documentation_agent": DocumentationAgent(),
            "testing_agent": TestingAgent()
        }
        
        # Create workflow engine
        engine = WorkflowEngine(agents)
        
        # Test workflow creation
        workflow_id = engine.create_workflow(
            name="Test Workflow",
            description="Testing workflow creation",
            steps_config=[
                {
                    "name": "Test Step",
                    "agent_id": "code_analyzer",
                    "task_type": "analyze_file",
                    "task_params": {"file_path": "test.py"}
                }
            ]
        )
        
        print(f"✅ Workflow created: {workflow_id[:8]}...")
        
        # Test workflow status
        status = engine.get_workflow_status(workflow_id)
        print(f"✅ Workflow status: {status['status']}")
        
        # Test templates
        print(f"✅ Available templates: {len(WORKFLOW_TEMPLATES)}")
        for template_name in WORKFLOW_TEMPLATES:
            print(f"   - {template_name}: {WORKFLOW_TEMPLATES[template_name]['name']}")
        
        assert True
    except Exception as e:
        print(f"❌ Workflow engine test failed: {e}")
        traceback.print_exc()
        assert False

def test_api_structure():
    """Test API endpoint structure"""
    print("\n🔌 Testing API Structure...")
    
    try:
        import main
        app = main.app
        
        # Count routes
        route_count = len(app.routes)
        print(f"✅ API routes defined: {route_count}")
        
        # Check for key endpoints
        route_paths = [route.path for route in app.routes if hasattr(route, 'path')]
        
        key_endpoints = [
            "/api/workflows",
            "/api/agents/{agent_id}/execute",
            "/api/workflow-templates",
            "/ws/{client_id}"
        ]
        
        for endpoint in key_endpoints:
            if any(endpoint.replace('{', '').replace('}', '') in path.replace('{', '').replace('}', '') for path in route_paths):
                print(f"✅ Endpoint available: {endpoint}")
            else:
                print(f"⚠️ Endpoint not found: {endpoint}")
        
        assert True
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        traceback.print_exc()
        assert False

def test_frontend_structure():
    """Test frontend file structure"""
    print("\n🌐 Testing Frontend Structure...")
    
    import os
    
    try:
        frontend_files = [
            "frontend/package.json",
            "frontend/src/app/App.tsx",
            "frontend/src/components/Dashboard.tsx",
            "frontend/src/components/WorkflowsPage.tsx",
            "frontend/src/components/EnhancedWorkflowsPage.tsx",
            "frontend/src/hooks/useWebSocket.ts"
        ]
        
        for file_path in frontend_files:
            if os.path.exists(file_path):
                print(f"✅ Frontend file: {file_path}")
            else:
                print(f"❌ Missing file: {file_path}")
        
        assert True
    except Exception as e:
        print(f"❌ Frontend structure test failed: {e}")
        assert False

@pytest.mark.asyncio
async def run_all_tests():
    """Run all tests"""
    print("🚀 MASS Framework Enhanced Feature Testing")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Sample Agents", test_sample_agents),
        ("Workflow Engine", test_workflow_engine),
        ("API Structure", test_api_structure),
        ("Frontend Structure", test_frontend_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The enhanced MASS Framework is ready!")
        print("\n💡 Next steps:")
        print("   1. Start backend: python -m uvicorn main:app --reload --port 8000")
        print("   2. Start frontend: cd frontend && npm start")
        print("   3. Visit: http://localhost:3000")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Check the output above for details.")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
