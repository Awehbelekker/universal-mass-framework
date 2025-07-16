# MASS Framework Live System Test
# PowerShell script to verify all deployed components

Write-Host "🚀 MASS Framework Live System Test" -ForegroundColor Green
Write-Host "=" * 60
Write-Host "📡 API Base URL: https://us-central1-ai-mass-trading.cloudfunctions.net/api"
Write-Host "⏰ Test Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

$apiBase = "https://us-central1-ai-mass-trading.cloudfunctions.net/api"
$tests = @()

function Test-Endpoint {
    param(
        [string]$Endpoint,
        [string]$Method = "GET",
        [hashtable]$Body = $null,
        [string]$Description = ""
    )
    
    $url = "$apiBase$Endpoint"
    $description = if ($Description) { $Description } else { $Endpoint }
    
    Write-Host "Testing: $description" -ForegroundColor Yellow
    
    try {
        $headers = @{
            'Content-Type' = 'application/json'
        }
        
        if ($Method -eq "GET") {
            $response = Invoke-RestMethod -Uri $url -Method GET -Headers $headers -TimeoutSec 30
        } elseif ($Method -eq "POST") {
            $bodyJson = if ($Body) { $Body | ConvertTo-Json } else { "{}" }
            $response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -Body $bodyJson -TimeoutSec 30
        }
        
        Write-Host "  ✅ SUCCESS" -ForegroundColor Green
        Write-Host "  📋 Response: $($response | ConvertTo-Json -Depth 2 | Out-String -Stream | Select-Object -First 3 | Join-String -Separator ' ')" -ForegroundColor Gray
        Write-Host ""
        return $true
    }
    catch {
        Write-Host "  ❌ FAILED" -ForegroundColor Red
        Write-Host "  🔥 Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
        return $false
    }
}

# Test suite
Write-Host "🔍 Running System Tests..." -ForegroundColor Cyan
Write-Host ""

$testResults = @()

# Test Firebase Functions Health
$testResults += @{
    Name = "🔥 Firebase Functions Health Check"
    Result = Test-Endpoint -Endpoint "/health" -Description "🔥 Firebase Functions Health Check"
}

# Test Admin Endpoints
$testResults += @{
    Name = "👨‍💼 Admin Users Endpoint"
    Result = Test-Endpoint -Endpoint "/admin/users" -Description "👨‍💼 Admin Users Endpoint"
}

$testResults += @{
    Name = "📊 Analytics Endpoint"
    Result = Test-Endpoint -Endpoint "/admin/analytics" -Description "📊 Analytics Endpoint"
}

$testResults += @{
    Name = "🧠 AI Learning Status"
    Result = Test-Endpoint -Endpoint "/admin/ai-learning" -Description "🧠 AI Learning Status"
}

# Test Trading System
$testResults += @{
    Name = "💹 Trading System Status"
    Result = Test-Endpoint -Endpoint "/trading/status" -Description "💹 Trading System Status"
}

# Test User Creation
$testResults += @{
    Name = "👥 Create Test Users"
    Result = Test-Endpoint -Endpoint "/admin/users/bulk-create" -Method "POST" -Body @{count=3; type="test"} -Description "👥 Create Test Users"
}

# Test AI Learning Start
$testResults += @{
    Name = "▶️ Start AI Learning"
    Result = Test-Endpoint -Endpoint "/admin/ai-learning/start" -Method "POST" -Description "▶️ Start AI Learning"
}

# Test Demo Data
$testResults += @{
    Name = "🔄 Initialize Demo Data"
    Result = Test-Endpoint -Endpoint "/initializeDemoData" -Method "POST" -Description "🔄 Initialize Demo Data"
}

# Summary
Write-Host "📋 TEST SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 60

$passed = 0
foreach ($test in $testResults) {
    $status = if ($test.Result) { "✅ PASS" } else { "❌ FAIL" }
    $color = if ($test.Result) { "Green" } else { "Red" }
    Write-Host "$status $($test.Name)" -ForegroundColor $color
    if ($test.Result) { $passed++ }
}

$total = $testResults.Count
Write-Host ""
Write-Host "🎯 OVERALL RESULT: $passed/$total tests passed" -ForegroundColor Yellow

if ($passed -ge ($total - 1)) {
    Write-Host "🚀 SYSTEM IS OPERATIONAL - READY FOR LIVE TESTING!" -ForegroundColor Green
} else {
    Write-Host "⚠️  MULTIPLE FAILURES - CHECK SYSTEM STATUS" -ForegroundColor Yellow
}

Write-Host "⏰ Test Completed: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# Open the dashboard
Write-Host ""
Write-Host "🌐 Opening Live System Dashboard..." -ForegroundColor Cyan
$dashboardPath = Join-Path -Path $PWD -ChildPath "live_system_dashboard.html"
Start-Process $dashboardPath
