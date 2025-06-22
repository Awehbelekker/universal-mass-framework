#!/usr/bin/env python3
"""
Comprehensive System Test for MASS Framework
Tests all features: Dashboard, Workflows, Agents, WebSocket
"""

import asyncio
import aiohttp
import websockets
import json
import time
from typing import Dict, Any
import pytest

class MASSSystemTester:
    def __init__(self, base_url: str = "http://localhost:8000", ws_url: str = "ws://localhost:8000"):
        self.base_url = base_url
        self.ws_url = ws_url
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append((test_name, success, details))
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
    
    @pytest.mark.asyncio
    async def test_api_health(self):
        """Test basic API connectivity"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/") as response:
                    assert response.status == 200
                    data = await response.json()
                    self.log_test("API Health Check", True, f"Version: {data.get('version', 'unknown')}")
                    return True
        except Exception as e:
            self.log_test("API Health Check", False, f"Connection error: {str(e)}")
            assert False
    
    @pytest.mark.asyncio
    async def test_agents_list(self):
        """Test agents listing endpoint"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/agents/") as response:
                    assert response.status == 200
                    data = await response.json()
                    agents = data.get("agents", [])
                    self.log_test("Agents List", True, f"Found {len(agents)} agents")
                    return agents
        except Exception as e:
            self.log_test("Agents List", False, f"Error: {str(e)}")
            assert False
    
    @pytest.mark.asyncio
    async def test_agent_execution(self):
        """Test individual agent execution"""
        try:
            task_data = {
                "type": "analyze_file",
                "file_path": "main.py"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/agents/code_analyzer/execute",
                    json=task_data
                ) as response:
                    assert response.status == 200
                    data = await response.json()
                    self.log_test("Agent Execution", True, f"Task: {data.get('task_type', 'unknown')}")
                    return data
        except Exception as e:
            self.log_test("Agent Execution", False, f"Error: {str(e)}")
            assert False
    
    @pytest.mark.asyncio
    async def test_workflow_templates(self):
        """Test workflow templates endpoint"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/workflow-templates") as response:
                    assert response.status == 200
                    data = await response.json()
                    templates = data.get("templates", {})
                    self.log_test("Workflow Templates", True, f"Found {len(templates)} templates")
                    return templates
        except Exception as e:
            self.log_test("Workflow Templates", False, f"Error: {str(e)}")
            assert False
    
    @pytest.mark.asyncio
    async def test_workflow_creation_and_execution(self):
        """Test workflow creation and execution"""
        try:
            # Create workflow
            workflow_data = {
                "name": "System Test Workflow",
                "description": "Test workflow for system verification",
                "steps": [
                    {
                        "agent_id": "code_analyzer",
                        "task_type": "analyze_file",
                        "task_params": {"file_path": "main.py"},
                        "dependencies": []
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                # Create workflow
                async with session.post(
                    f"{self.base_url}/api/workflows/create",
                    json=workflow_data
                ) as response:
                    assert response.status == 200
                    create_data = await response.json()
                    workflow_id = create_data.get("workflow_id")
                    self.log_test("Workflow Creation", True, f"ID: {workflow_id[:8]}...")
                    
                    # Execute workflow
                    async with session.post(
                        f"{self.base_url}/api/workflows/{workflow_id}/execute"
                    ) as exec_response:
                        assert exec_response.status == 200
                        exec_data = await exec_response.json()
                        self.log_test("Workflow Execution", True, f"Status: {exec_data.get('status')}")
                        
                        # Wait a moment for completion
                        await asyncio.sleep(2)
                        
                        # Check status
                        async with session.get(
                            f"{self.base_url}/api/workflows/{workflow_id}"
                        ) as status_response:
                            assert status_response.status == 200
                            status_data = await status_response.json()
                            final_status = status_data.get("status")
                            progress = status_data.get("progress", 0)
                            self.log_test("Workflow Status Check", True, 
                                        f"Status: {final_status}, Progress: {progress}%")
                            return workflow_id
        except Exception as e:
            self.log_test("Workflow Creation/Execution", False, f"Error: {str(e)}")
            assert False
    
    @pytest.mark.asyncio
    async def test_websocket_connection(self):
        """Test WebSocket connectivity and real-time updates"""
        try:
            client_id = "test_client_" + str(int(time.time()))
            ws_uri = f"{self.ws_url}/ws/{client_id}"
            
            # Test connection
            async with websockets.connect(ws_uri) as websocket:
                self.log_test("WebSocket Connection", True, f"Client ID: {client_id}")
                
                # Send a test message
                test_message = {
                    "type": "ping",
                    "timestamp": time.time()
                }
                await websocket.send(json.dumps(test_message))
                
                # Wait for response (with timeout)
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    response_data = json.loads(response)
                    self.log_test("WebSocket Message Exchange", True, 
                                f"Response type: {response_data.get('type', 'unknown')}")
                    assert True
                except asyncio.TimeoutError:
                    self.log_test("WebSocket Message Exchange", False, "Timeout waiting for response")
                    assert False
                    
        except websockets.exceptions.ConnectionClosed:
            self.log_test("WebSocket Connection", False, "Connection closed unexpectedly")
            assert False
        except Exception as e:
            self.log_test("WebSocket Connection", False, f"Error: {str(e)}")
            assert False
    
    @pytest.mark.asyncio
    async def test_all_workflows_endpoints(self):
        """Test all workflow-related endpoints"""
        try:
            async with aiohttp.ClientSession() as session:
                # List all workflows
                async with session.get(f"{self.base_url}/api/workflows") as response:
                    assert response.status == 200
                    data = await response.json()
                    workflows = data.get("workflows", [])
                    self.log_test("Workflows List", True, f"Found {len(workflows)} workflows")
        except Exception as e:
            self.log_test("Workflows List", False, f"Error: {str(e)}")
            assert False
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("🧪 MASS FRAMEWORK SYSTEM TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)
        
        print(f"📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        print()
        
        # Group by category
        categories = {
            "API": [],
            "Agents": [],
            "Workflows": [],
            "WebSocket": [],
            "Other": []
        }
        
        for test_name, success, details in self.test_results:
            if "API" in test_name or "Health" in test_name:
                categories["API"].append((test_name, success, details))
            elif "Agent" in test_name:
                categories["Agents"].append((test_name, success, details))
            elif "Workflow" in test_name:
                categories["Workflows"].append((test_name, success, details))
            elif "WebSocket" in test_name:
                categories["WebSocket"].append((test_name, success, details))
            else:
                categories["Other"].append((test_name, success, details))
        
        for category, tests in categories.items():
            if tests:
                print(f"📁 {category}:")
                for test_name, success, details in tests:
                    status = "✅" if success else "❌"
                    print(f"   {status} {test_name}")
                    if details:
                        print(f"      {details}")
                print()
        
        # Overall status
        if passed == total:
            print("🎉 ALL TESTS PASSED! System is fully functional.")
        else:
            print(f"⚠️  {total - passed} tests failed. Check details above.")
        
        print("\n💡 Manual Testing Recommendations:")
        print("   1. Open http://localhost:3000 to test the React frontend")
        print("   2. Navigate between Dashboard, Workflows, and Enhanced Workflows tabs")
        print("   3. Create workflows from templates in Enhanced Workflows")
        print("   4. Monitor real-time updates in the Dashboard")
        print("   5. Check WebSocket connection status in browser dev tools")

@pytest.mark.asyncio
async def main():
    """Run all system tests"""
    print("🚀 MASS Framework - Comprehensive System Test")
    print("=" * 50)
    
    tester = MASSSystemTester()
    
    # Run all tests
    await tester.test_api_health()
    await tester.test_agents_list()
    await tester.test_agent_execution()
    await tester.test_workflow_templates()
    await tester.test_workflow_creation_and_execution()
    await tester.test_all_workflows_endpoints()
    await tester.test_websocket_connection()
    
    # Print summary
    tester.print_summary()

if __name__ == "__main__":
    asyncio.run(main())
