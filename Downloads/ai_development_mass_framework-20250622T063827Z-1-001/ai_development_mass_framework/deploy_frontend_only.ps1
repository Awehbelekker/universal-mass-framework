# Frontend Deployment Script
# This script deploys only the frontend components

param(
    [string]$Environment = "development",
    [switch]$Force = $false
)

Write-Host "🚀 Starting Frontend Deployment..." -ForegroundColor Green

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js first." -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check if npm is installed
try {
    $npmVersion = npm --version
    Write-Host "✅ npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found. Please install npm first." -ForegroundColor Red
    exit 1
}

# Navigate to frontend directory
if (Test-Path "frontend") {
    Set-Location "frontend"
    Write-Host "📁 Navigated to frontend directory" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend directory not found" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
try {
    npm install
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Build the frontend
Write-Host "🔨 Building frontend..." -ForegroundColor Yellow
try {
    npm run build
    Write-Host "✅ Frontend built successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to build frontend" -ForegroundColor Red
    exit 1
}

# Copy built files to deployment directory
$deployDir = "../deploy/frontend"
if (-not (Test-Path $deployDir)) {
    New-Item -ItemType Directory -Path $deployDir -Force
}

Write-Host "📋 Copying built files to deployment directory..." -ForegroundColor Yellow
try {
    Copy-Item -Path "dist/*" -Destination $deployDir -Recurse -Force
    Write-Host "✅ Files copied successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to copy files" -ForegroundColor Red
    exit 1
}

# Start development server if requested
if ($Environment -eq "development") {
    Write-Host "🌐 Starting development server..." -ForegroundColor Yellow
    try {
        Start-Process -FilePath "npm" -ArgumentList "run", "dev" -NoNewWindow
        Write-Host "✅ Development server started" -ForegroundColor Green
        Write-Host "🌍 Frontend available at: http://localhost:3000" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Failed to start development server" -ForegroundColor Red
    }
}

Write-Host "🎉 Frontend deployment completed successfully!" -ForegroundColor Green
Write-Host "📁 Built files are in: $deployDir" -ForegroundColor Cyan

# Return to original directory
Set-Location ".." 