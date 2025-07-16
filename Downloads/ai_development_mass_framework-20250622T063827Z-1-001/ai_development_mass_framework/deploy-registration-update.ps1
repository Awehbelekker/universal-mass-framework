#!/usr/bin/env pwsh
# PROMETHEUS Registration Update Deployment Script
# This script updates the registration system and deploys it to Firebase

Write-Host "🚀 Starting PROMETHEUS Registration Update Deployment" -ForegroundColor Cyan
Write-Host "=============================================================" -ForegroundColor Cyan

# Get the current script directory
$scriptDir = $PSScriptRoot
Write-Host "Working in directory: $scriptDir" -ForegroundColor DarkGray

# Create build directory if it doesn't exist
if (!(Test-Path -Path "$scriptDir/build")) {
    New-Item -ItemType Directory -Path "$scriptDir/build" | Out-Null
    Write-Host "Created build directory" -ForegroundColor DarkGray
}

# Copy key files to the build directory
Write-Host "`n📦 Copying registration system files..." -ForegroundColor Yellow

# Updated HTML files
$htmlFiles = @(
    @{Source = "prometheus_registration.html"; Dest = "prometheus_registration.html"},
    @{Source = "prometheus_admin.html"; Dest = "prometheus_admin.html"},
    @{Source = "private_access_gate.html"; Dest = "private_access_gate.html"}
)

foreach ($file in $htmlFiles) {
    if (Test-Path -Path "$scriptDir/$($file.Source)") {
        Copy-Item -Force -Path "$scriptDir/$($file.Source)" -Destination "$scriptDir/build/$($file.Dest)"
        Write-Host "  ✅ Copied $($file.Source)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ Warning: File $($file.Source) not found" -ForegroundColor Yellow
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
        Write-Host "  ✅ Copied $file" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ Warning: File $file not found" -ForegroundColor Yellow
    }
}

# Deploy updated Firestore rules
Write-Host "`n📦 Deploying updated Firestore rules..." -ForegroundColor Yellow
Copy-Item -Force -Path "$scriptDir/firestore.rules" -Destination "$scriptDir/build/firestore.rules"
firebase deploy --only firestore:rules

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Firestore rules deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Firestore rules deployment failed. Please check the logs above." -ForegroundColor Red
}

# Deploy to Firebase Hosting
Write-Host "`n📦 Deploying updated files to Firebase Hosting..." -ForegroundColor Yellow
firebase deploy --only hosting

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Firebase Hosting deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Firebase Hosting deployment failed. Please check the logs above." -ForegroundColor Red
}

# Final success message
Write-Host "`n🎉 PROMETHEUS Registration System Update Complete!" -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "Registration URL: https://ai-mass-trading.web.app/prometheus_registration.html" -ForegroundColor White
Write-Host "Admin Panel: https://ai-mass-trading.web.app/prometheus_admin.html" -ForegroundColor White
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "You can now register test users and approve them through the admin panel." -ForegroundColor Magenta
Write-Host "Admin credentials: admin@prometheus-trading.com / PrometheusAdmin2025!" -ForegroundColor Yellow
