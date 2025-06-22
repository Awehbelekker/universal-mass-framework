#!/usr/bin/env pwsh
# MASS Framework Frontend Startup Script

Write-Host "🌐 MASS Framework Frontend Startup" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

# Check if we're in the frontend directory
if (-not (Test-Path "package.json")) {
    Write-Host "❌ Please run this script from the frontend directory" -ForegroundColor Red
    exit 1
}

Write-Host "📦 Installing Node.js dependencies..." -ForegroundColor Yellow
npm install --legacy-peer-deps

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies. Please check the output above." -ForegroundColor Red
    exit 1
}

Write-Host "`n🚀 Starting Frontend Development Server..." -ForegroundColor Green
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Blue
Write-Host "`n💡 Make sure the backend is running on http://localhost:8000" -ForegroundColor Yellow
Write-Host "🔧 Use VS Code tasks for easier management: Ctrl+Shift+P -> Tasks: Run Task" -ForegroundColor Yellow

# Start the frontend development server
npm start
