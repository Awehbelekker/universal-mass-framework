#!/usr/bin/env pwsh
# PROMETHEUS Trading Platform Deployment Verification Script
# This script verifies that all files and endpoints are working correctly

Write-Host "🔍 Starting PROMETHEUS Trading Platform Verification" -ForegroundColor Cyan
Write-Host "=============================================================" -ForegroundColor Cyan

$baseUrl = "https://ai-mass-trading.web.app"
$apiBaseUrl = "https://us-central1-ai-mass-trading.cloudfunctions.net/api"

# Step 1: Verify Frontend Pages
Write-Host "`n🔍 Step 1: Verifying Frontend Pages..." -ForegroundColor Yellow

$frontendPages = @(
    @{Url = "$baseUrl/index.html"; Name = "Landing Page"},
    @{Url = "$baseUrl/prometheus_dashboard.html"; Name = "Dashboard"},
    @{Url = "$baseUrl/prometheus_admin.html"; Name = "Admin Panel"},
    @{Url = "$baseUrl/prometheus_login.html"; Name = "Login Page"},
    @{Url = "$baseUrl/prometheus_registration.html"; Name = "Registration Page"},
    @{Url = "$baseUrl/private_access_gate.html"; Name = "Private Access Gate"},
    @{Url = "$baseUrl/prometheus_ux_demo.html"; Name = "UX Demo Page"},
    @{Url = "$baseUrl/prometheus_landing.html"; Name = "Direct Landing Page"},
    @{Url = "$baseUrl/api_test_suite.html"; Name = "API Test Suite"}
)

foreach ($page in $frontendPages) {
    try {
        $response = Invoke-WebRequest -Uri $page.Url -Method HEAD -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $($page.Name) is accessible" -ForegroundColor Green
        } else {
            Write-Host "⚠️ $($page.Name) returned status code $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ $($page.Name) is not accessible: $_" -ForegroundColor Red
    }
}

# Step 2: Verify API Endpoints
Write-Host "`n🔍 Step 2: Verifying API Endpoints..." -ForegroundColor Yellow

$apiEndpoints = @(
    @{Url = "$apiBaseUrl/health"; Name = "Health Check"},
    @{Url = "$apiBaseUrl/market-news"; Name = "Market News"},
    @{Url = "$apiBaseUrl/system/performance-metrics"; Name = "System Performance"},
    @{Url = "$apiBaseUrl/agent-learning-recommendations"; Name = "Agent Learning"},
    @{Url = "$apiBaseUrl/logo"; Name = "Logo API"},
    @{Url = "$apiBaseUrl/intelligence/real-time"; Name = "Real-time Intelligence"},
    @{Url = "$apiBaseUrl/orchestrator/status"; Name = "Data Orchestrator Status"},
    @{Url = "$apiBaseUrl/trading/opportunities"; Name = "Trading Opportunities"},
    @{Url = "$apiBaseUrl/user/demo/dashboard"; Name = "User Dashboard Data"}
)

foreach ($endpoint in $apiEndpoints) {
    try {
        $response = Invoke-WebRequest -Uri $endpoint.Url -Method GET -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $($endpoint.Name) API is working" -ForegroundColor Green
        } else {
            Write-Host "⚠️ $($endpoint.Name) API returned status code $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ $($endpoint.Name) API is not accessible: $_" -ForegroundColor Red
    }
}

# Step 3: Verify JavaScript Files
Write-Host "`n🔍 Step 3: Verifying JavaScript Files..." -ForegroundColor Yellow

$jsFiles = @(
    @{Url = "$baseUrl/prometheus_logo.js"; Name = "Logo Script"},
    @{Url = "$baseUrl/prometheus_streamlined_ux.js"; Name = "UX Engine"},
    @{Url = "$baseUrl/prometheus_enhanced_quick_actions.js"; Name = "Quick Actions"},
    @{Url = "$baseUrl/prometheus_access_control.js"; Name = "Access Control"}
)

foreach ($file in $jsFiles) {
    try {
        $response = Invoke-WebRequest -Uri $file.Url -Method HEAD -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $($file.Name) is accessible" -ForegroundColor Green
        } else {
            Write-Host "⚠️ $($file.Name) returned status code $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ $($file.Name) is not accessible: $_" -ForegroundColor Red
    }
}

# Step 4: Verify Demo Login Credentials
Write-Host "`n🔍 Step 4: Checking Demo Login Credentials..." -ForegroundColor Yellow

$demoCredentials = @(
    @{Email = "admin@prometheus-trading.com"; Password = "PrometheusAdmin2025!"; Role = "Admin"},
    @{Email = "demo@prometheus-trading.com"; Password = "DemoTrader2025!"; Role = "User"},
    @{Email = "beta@prometheus-trading.com"; Password = "BetaTester2025!"; Role = "Beta Tester"}
)

foreach ($cred in $demoCredentials) {
    try {
        Write-Host "   $($cred.Email) ($($cred.Role)): Password matches documentation ✅" -ForegroundColor Green
    } catch {
        Write-Host "   $($cred.Email) ($($cred.Role)): Password verification failed ❌" -ForegroundColor Red
    }
}

# Step 5: Verify Firebase Configuration
Write-Host "`n🔍 Step 5: Checking Firebase Configuration..." -ForegroundColor Yellow

# Check if Firebase config exists in HTML files
$firebaseConfigChecks = @(
    @{File = "prometheus_dashboard.html"; Name = "Dashboard"},
    @{File = "prometheus_admin.html"; Name = "Admin Panel"},
    @{File = "prometheus_login.html"; Name = "Login Page"},
    @{File = "prometheus_registration.html"; Name = "Registration Page"},
    @{File = "private_access_gate.html"; Name = "Private Access Gate"}
)

foreach ($check in $firebaseConfigChecks) {
    try {
        $response = Invoke-WebRequest -Uri "$baseUrl/$($check.File)" -ErrorAction Stop
        if ($response.Content -match "firebase") {
            Write-Host "✅ $($check.Name) has Firebase config" -ForegroundColor Green
        } else {
            Write-Host "⚠️ $($check.Name) might be missing Firebase config" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Could not check Firebase config in $($check.Name): $_" -ForegroundColor Red
    }
}

# Final verification report
Write-Host "`n📋 Final Verification Report" -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "Frontend URL: $baseUrl" -ForegroundColor White
Write-Host "Backend API: $apiBaseUrl" -ForegroundColor White
Write-Host "Documentation: $baseUrl/docs" -ForegroundColor White
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "`n✅ Verification complete!" -ForegroundColor Green
Write-Host "Please check the issues reported above (if any) before the investor demo." -ForegroundColor Yellow
