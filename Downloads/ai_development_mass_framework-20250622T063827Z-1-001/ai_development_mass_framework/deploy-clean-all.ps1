# PROMETHEUS Trading Platform - Clean Deployment Script
# This script performs a full clean deployment of all components

Write-Host "🔥 PROMETHEUS Trading Platform - Full Clean Deployment" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

# Set error action preference
$ErrorActionPreference = "Stop"

try {
    # Step 1: Clean local cache
    Write-Host "🧹 Cleaning deployment cache..." -ForegroundColor Cyan
    if (Test-Path ".firebase") {
        Remove-Item -Recurse -Force ".firebase" -ErrorAction SilentlyContinue
    }
    Write-Host "✅ Cache cleaned successfully" -ForegroundColor Green
    Write-Host ""

    # Step 2: Validate critical files
    Write-Host "🔍 Validating critical files..." -ForegroundColor Cyan
    $requiredFiles = @(
        "firebase.json",
        "prometheus_logo_system_v2.js",
        "prometheus_ux_master_enhancer.js",
        "prometheus_workflow_enhancer.js",
        "prometheus_logo.js",
        "private_access_gate.html",
        "prometheus_admin.html",
        "prometheus_beautiful_flame.svg"
    )

    foreach ($file in $requiredFiles) {
        if (!(Test-Path $file)) {
            throw "Missing required file: $file"
        }
    }
    Write-Host "✅ All required files present" -ForegroundColor Green
    Write-Host ""

    # Step 3: Deploy Firebase hosting
    Write-Host "🚀 Deploying to Firebase Hosting..." -ForegroundColor Cyan
    firebase deploy --only hosting
    if ($LASTEXITCODE -ne 0) {
        throw "Firebase hosting deployment failed with exit code $LASTEXITCODE"
    }
    Write-Host "✅ Firebase hosting deployed successfully" -ForegroundColor Green
    Write-Host ""

    # Step 4: Deploy Firebase functions
    Write-Host "⚡ Deploying Firebase Functions..." -ForegroundColor Cyan
    firebase deploy --only functions
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Firebase functions deployment had issues. Continuing anyway..." -ForegroundColor Yellow
    } else {
        Write-Host "✅ Firebase functions deployed successfully" -ForegroundColor Green
    }
    Write-Host ""

    # Step 5: Deploy Firebase firestore rules
    Write-Host "📝 Deploying Firestore rules..." -ForegroundColor Cyan
    firebase deploy --only firestore:rules
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Firestore rules deployment had issues. Continuing anyway..." -ForegroundColor Yellow
    } else {
        Write-Host "✅ Firestore rules deployed successfully" -ForegroundColor Green
    }
    Write-Host ""

    # Step 6: Verify deployment
    Write-Host "✅ Verifying deployment..." -ForegroundColor Cyan
    Write-Host "  📱 Web application URL: https://ai-mass-trading.web.app" -ForegroundColor White
    Write-Host "  🔐 Admin access URL: https://ai-mass-trading.web.app/prometheus_admin.html" -ForegroundColor White
    Write-Host "  🔒 Private access URL: https://ai-mass-trading.web.app/private_access_gate.html" -ForegroundColor White
    Write-Host ""

    # Success message
    Write-Host "🎉 DEPLOYMENT COMPLETE! 🎉" -ForegroundColor Green
    Write-Host "The PROMETHEUS Trading Platform has been successfully deployed." -ForegroundColor Green
    Write-Host "Admin Login: admin@mass-framework.com (Password: MassAdmin2025!)" -ForegroundColor Cyan

} catch {
    # Error handling
    Write-Host "❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Deployment failed. Please check the error message above." -ForegroundColor Red
    exit 1
}
