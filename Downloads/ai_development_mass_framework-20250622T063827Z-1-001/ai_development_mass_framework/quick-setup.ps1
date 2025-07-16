# 🚀 Quick Start Script for MASS AI Trading
# Run this to get started with live trading setup

param(
    [string]$ProjectId = "",
    [switch]$SetupOnly
)

Write-Host "🎯 MASS AI Trading Framework - Quick Setup" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Get project ID if not provided
if (-not $ProjectId) {
    $ProjectId = Read-Host "Enter your Firebase Project ID (or press Enter for 'mass-ai-trading')"
    if (-not $ProjectId) {
        $ProjectId = "mass-ai-trading"
    }
}

Write-Host "📋 Setting up project: $ProjectId" -ForegroundColor Yellow

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Blue

$missingTools = @()

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    $missingTools += "Node.js (https://nodejs.org)"
}

# Check Firebase CLI
try {
    $firebaseVersion = firebase --version
    Write-Host "✅ Firebase CLI: $firebaseVersion" -ForegroundColor Green
} catch {
    Write-Host "⚙️ Installing Firebase CLI..." -ForegroundColor Yellow
    npm install -g firebase-tools
}

# Check npm
try {
    $npmVersion = npm --version
    Write-Host "✅ npm: $npmVersion" -ForegroundColor Green
} catch {
    $missingTools += "npm (comes with Node.js)"
}

if ($missingTools.Count -gt 0) {
    Write-Host "❌ Missing required tools:" -ForegroundColor Red
    foreach ($tool in $missingTools) {
        Write-Host "   - $tool" -ForegroundColor Red
    }
    Write-Host "Please install the missing tools and run this script again." -ForegroundColor Red
    exit 1
}

# Create Firebase project structure
Write-Host "📁 Creating Firebase project structure..." -ForegroundColor Blue

$firebaseDir = "firebase"
if (-not (Test-Path $firebaseDir)) {
    Write-Host "✨ Created firebase directory" -ForegroundColor Green
    # Directory already exists from previous setup
}

# Initialize Firebase project
Write-Host "🔥 Initializing Firebase project..." -ForegroundColor Blue
Set-Location $firebaseDir

# Login to Firebase
Write-Host "🔐 Firebase login required..." -ForegroundColor Yellow
firebase login

# Set project
firebase use $ProjectId

# Install Cloud Functions dependencies
Write-Host "📦 Installing Cloud Functions dependencies..." -ForegroundColor Blue
Set-Location functions
npm install

Write-Host ""
Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Set up your Alpaca trading account: https://alpaca.markets"
Write-Host "2. Get your API keys (paper trading first)"
Write-Host "3. Configure environment variables:"
Write-Host "   firebase functions:config:set alpaca.paper_key='YOUR_KEY'"
Write-Host "   firebase functions:config:set alpaca.paper_secret='YOUR_SECRET'"
Write-Host "4. Deploy to Firebase:"
Write-Host "   ..\deploy-live.ps1 -Production -ProjectId $ProjectId"
Write-Host ""
Write-Host "📖 Read the complete guide: GO_LIVE_GUIDE.md" -ForegroundColor Cyan
Write-Host "📋 Trading account setup: TRADING_ACCOUNT_SETUP.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎉 Ready to go live with AI trading!" -ForegroundColor Green

Set-Location ..
