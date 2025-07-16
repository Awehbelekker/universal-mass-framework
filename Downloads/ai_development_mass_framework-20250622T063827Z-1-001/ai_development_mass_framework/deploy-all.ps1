#!/usr/bin/env pwsh
# PROMETHEUS Trading Platform Full Deployment Script
# This script deploys both the Firebase Functions and the enhanced UI

Write-Host "🚀 Starting PROMETHEUS Trading Platform Full Deployment" -ForegroundColor Cyan
Write-Host "=============================================================" -ForegroundColor Cyan

# Step 1: Build and deploy Firebase Functions
Write-Host "`n📦 Step 1: Building and deploying Firebase Functions..." -ForegroundColor Yellow
Set-Location ./functions
Write-Host "Installing dependencies for Firebase Functions..." -ForegroundColor DarkGray
npm install --quiet

Write-Host "Building Firebase Functions..." -ForegroundColor DarkGray
npm run build

Write-Host "Deploying Firebase Functions..." -ForegroundColor DarkGray
firebase deploy --only functions

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Firebase Functions deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Firebase Functions deployment failed. Please check the logs above." -ForegroundColor Red
    exit 1
}

# Step 2: Prepare frontend files for deployment
Write-Host "`n📦 Step 2: Preparing frontend files for deployment..." -ForegroundColor Yellow
Set-Location ..

# Get the current script directory
$scriptDir = $PSScriptRoot
Write-Host "Working in directory: $scriptDir" -ForegroundColor DarkGray

# Create build directory if it doesn't exist
if (!(Test-Path -Path "$scriptDir/build")) {
    New-Item -ItemType Directory -Path "$scriptDir/build" | Out-Null
    Write-Host "Created build directory" -ForegroundColor DarkGray
}

# Update API endpoints in HTML files to use Firebase Functions
Write-Host "Updating API endpoints to Firebase Functions..." -ForegroundColor DarkGray
$files = @("prometheus_dashboard.html", "prometheus_admin.html", "prometheus_landing.html", "prometheus_login.html")
foreach ($file in $files) {
    if (Test-Path -Path "$scriptDir/$file") {
        $content = Get-Content -Path "$scriptDir/$file" -Raw
        $updatedContent = $content -replace "http://localhost:8000", "https://us-central1-ai-mass-trading.cloudfunctions.net/api"
        Set-Content -Path "$scriptDir/$file" -Value $updatedContent
        Write-Host "  - Updated API endpoints in $file" -ForegroundColor DarkGray
    } else {
        Write-Host "  - Warning: File $file not found" -ForegroundColor Yellow
    }
}

# Copy landing page and other HTML files to the build directory
Write-Host "Copying landing page and UI files to build directory..." -ForegroundColor DarkGray

# Main HTML files
$htmlFiles = @(
    @{Source = "prometheus_landing.html"; Dest = "index.html"},
    @{Source = "prometheus_dashboard.html"; Dest = "prometheus_dashboard.html"},
    @{Source = "prometheus_admin.html"; Dest = "prometheus_admin.html"},
    @{Source = "prometheus_login.html"; Dest = "prometheus_login.html"},
    @{Source = "prometheus_registration.html"; Dest = "prometheus_registration.html"},
    @{Source = "private_access_gate.html"; Dest = "private_access_gate.html"},
    @{Source = "prometheus_ux_demo.html"; Dest = "prometheus_ux_demo.html"},
    @{Source = "api_test_suite.html"; Dest = "api_test_suite.html"}
)

foreach ($file in $htmlFiles) {
    if (Test-Path -Path "$scriptDir/$($file.Source)") {
        Copy-Item -Force -Path "$scriptDir/$($file.Source)" -Destination "$scriptDir/build/$($file.Dest)"
        Write-Host "  - Copied $($file.Source) to $($file.Dest)" -ForegroundColor DarkGray
    } else {
        Write-Host "  - Warning: File $($file.Source) not found" -ForegroundColor Yellow
    }
}

# JavaScript files
$jsFiles = @(
    "prometheus_logo.js",
    "prometheus_streamlined_ux.js",
    "prometheus_enhanced_quick_actions.js",
    "prometheus_access_control.js",
    "prometheus_mobile_responsiveness.js"
)

foreach ($file in $jsFiles) {
    if (Test-Path -Path "$scriptDir/$file") {
        Copy-Item -Force -Path "$scriptDir/$file" -Destination "$scriptDir/build/$file"
        Write-Host "  - Copied $file" -ForegroundColor DarkGray
    } else {
        Write-Host "  - Warning: File $file not found" -ForegroundColor Yellow
    }
}

# Other assets
if (Test-Path -Path "$scriptDir/favicon.svg") {
    Copy-Item -Force -Path "$scriptDir/favicon.svg" -Destination "$scriptDir/build/favicon.svg"
    Write-Host "  - Copied favicon" -ForegroundColor DarkGray
}

# Documentation for reference
$docsFiles = @(
    "DEMO_CREDENTIALS.md",
    "INVESTOR_PRESENTATION.md",
    "FINAL_QA_CHECKLIST.md",
    "UX_IMPLEMENTATION_GUIDE.md"
)

$docsDir = "$scriptDir/build/docs"
if (!(Test-Path -Path $docsDir)) {
    New-Item -ItemType Directory -Path $docsDir | Out-Null
    Write-Host "Created docs directory" -ForegroundColor DarkGray
}

foreach ($file in $docsFiles) {
    if (Test-Path -Path "$scriptDir/$file") {
        Copy-Item -Force -Path "$scriptDir/$file" -Destination "$docsDir/$file"
        Write-Host "  - Copied documentation: $file" -ForegroundColor DarkGray
    }
}

Write-Host "✅ Frontend files prepared for deployment!" -ForegroundColor Green

# Step 3: Deploy to Firebase Hosting
Write-Host "`n📦 Step 3: Deploying to Firebase Hosting..." -ForegroundColor Yellow
firebase deploy --only hosting

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Firebase Hosting deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Firebase Hosting deployment failed. Please check the logs above." -ForegroundColor Red
    exit 1
}

# Final success message
Write-Host "`n🎉 PROMETHEUS Trading Platform deployment complete!" -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "Backend API: https://us-central1-ai-mass-trading.cloudfunctions.net/api" -ForegroundColor White
Write-Host "Frontend: https://ai-mass-trading.web.app" -ForegroundColor White
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "Neural Forge™ is now fully operational and ready for trading!" -ForegroundColor Magenta
