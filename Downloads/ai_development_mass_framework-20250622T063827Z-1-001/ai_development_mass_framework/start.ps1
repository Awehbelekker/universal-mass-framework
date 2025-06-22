#!/usr/bin/env pwsh
# MASS Framework Enhanced Startup Script

Write-Host "🤖 AI Development MASS Framework - Enhanced Edition" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

Write-Host "🧪 Running backend tests..." -ForegroundColor Yellow
python -m pytest tests/unit_tests/ -v

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All tests passed!" -ForegroundColor Green
} else {
    Write-Host "❌ Tests failed. Please check the output above." -ForegroundColor Red
    exit 1
}

Write-Host "`n🧪 Testing sample agents..." -ForegroundColor Yellow
python -c "
import asyncio
from agents.sample_agents import CodeAnalyzerAgent, DocumentationAgent, TestingAgent

async def test_agents():
    agents = {
        'Code Analyzer': CodeAnalyzerAgent(),
        'Documentation': DocumentationAgent(),
        'Testing': TestingAgent()
    }
    
    for name, agent in agents.items():
        result = await agent.analyze_input({'type': 'test'})
        print(f'✅ {name} Agent: {result[\"analysis_type\"]}')

asyncio.run(test_agents())
"

Write-Host "`n🚀 Starting Enhanced Backend Server..." -ForegroundColor Green
Write-Host "   Backend: http://localhost:8000" -ForegroundColor Blue
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Blue
Write-Host "   WebSocket: ws://localhost:8000/ws/your-client-id" -ForegroundColor Blue
Write-Host "`n🌟 NEW FEATURES:" -ForegroundColor Yellow
Write-Host "   ✨ Real-time WebSocket communication" -ForegroundColor White
Write-Host "   ✨ 3 Sample agents (Code, Docs, Testing)" -ForegroundColor White
Write-Host "   ✨ Workflow engine with templates" -ForegroundColor White
Write-Host "   ✨ Agent execution endpoints" -ForegroundColor White
Write-Host "`n💡 To start the frontend:" -ForegroundColor Yellow
Write-Host "   cd frontend && npm install --legacy-peer-deps && npm start" -ForegroundColor Yellow
Write-Host "`n🔧 Or use VS Code tasks: Ctrl+Shift+P -> Tasks: Run Task" -ForegroundColor Yellow

# Start the backend server
python -m uvicorn main:app --reload --port 8000 --host 127.0.0.1
