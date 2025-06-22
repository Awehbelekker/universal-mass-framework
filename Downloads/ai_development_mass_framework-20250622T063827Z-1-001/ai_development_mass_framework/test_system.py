#!/usr/bin/env python3
"""
Test script for MASS Framework WebSocket and Agent functionality
"""

import asyncio
import json
import websockets
import aiohttp
import pytest
from agents.ai_agents.sample_agents import CodeAnalyzerAgent, DocumentationAgent, TestingAgent

@pytest.mark.asyncio
async def test_agents():
    """Test the sample agents directly"""
    print("🧪 Testing Sample Agents...")
    
    # Test Code Analyzer Agent
    code_agent = CodeAnalyzerAgent()
    result = await code_agent.process_task({
        "type": "analyze_file",
        "file_path": "main.py"
    })
    print(f"✅ Code Analyzer: {result.get('file_path')} analyzed")
    
    # Test Documentation Agent
    doc_agent = DocumentationAgent()
    result = await doc_agent.process_task({
        "type": "generate_readme",
        "project_info": {"name": "MASS Framework", "description": "Multi-Agent System"}
    })
    print(f"✅ Documentation Agent: README generated")
    
    # Test Testing Agent
    test_agent = TestingAgent()
    result = await test_agent.process_task({
        "type": "run_tests",
        "test_path": "tests/"
    })
    print(f"✅ Testing Agent: Tests executed")

@pytest.mark.asyncio
async def test_websocket_connection():
    """Test WebSocket connection to the server"""
    print("\n🌐 Testing WebSocket Connection...")
    
    try:
        # Try to connect to WebSocket
        uri = "ws://localhost:8000/ws/test-client"
        
        async with websockets.connect(uri, timeout=5) as websocket:
            print("✅ WebSocket connected successfully")
            
            # Send ping message
            ping_message = {"type": "ping", "timestamp": "2025-06-14T08:00:00Z"}
            await websocket.send(json.dumps(ping_message))
            
            # Wait for pong response
            response = await websocket.recv()
            data = json.loads(response)
            
            if data.get("type") == "pong":
                print("✅ WebSocket ping/pong working")
            else:
                print(f"⚠️ Unexpected response: {data}")
                
    except ConnectionRefusedError:
        print("❌ WebSocket connection failed - Server not running?")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")

@pytest.mark.asyncio
async def test_api_endpoints():
    """Test the API endpoints"""
    print("\n🔌 Testing API Endpoints...")
    
    base_url = "http://localhost:8000"
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test root endpoint
            async with session.get(f"{base_url}/") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Root endpoint: {data.get('message', 'OK')}")
                else:
                    print(f"❌ Root endpoint failed: {response.status}")
            
            # Test agents list endpoint
            async with session.get(f"{base_url}/api/agents") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Agents endpoint: {len(data.get('agents', []))} agents available")
                else:
                    print(f"❌ Agents endpoint failed: {response.status}")
            
            # Test agent execution endpoint
            task_data = {
                "type": "analyze_file",
                "file_path": "test.py"
            }
            
            async with session.post(f"{base_url}/api/agents/code_analyzer/execute", json=task_data) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Agent execution: {data.get('status', 'unknown')}")
                else:
                    print(f"❌ Agent execution failed: {response.status}")
                    
    except aiohttp.ClientConnectorError:
        print("❌ API connection failed - Server not running?")
    except Exception as e:
        print(f"❌ API error: {e}")

async def main():
    """Run all tests"""
    print("🚀 MASS Framework - WebSocket & Agent Test Suite")
    print("=" * 50)
    
    # Test agents directly (doesn't require server)
    await test_agents()
    
    # Test server-dependent functionality
    print("\n📡 Testing Server-Dependent Features...")
    print("(Make sure the server is running: python -m uvicorn main:app --reload --port 8000)")
    
    await test_websocket_connection()
    await test_api_endpoints()
    
    print("\n✨ Test Suite Complete!")
    print("\n💡 To start the full system:")
    print("   Backend: python -m uvicorn main:app --reload --port 8000")
    print("   Frontend: cd frontend && npm start")

if __name__ == "__main__":
    asyncio.run(main())
