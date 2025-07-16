# MASS AI Trading - Alpaca API Connection Test (PowerShell)

param(
    [string]$ApiKey = "PKD86B3W4830DOMGZWED",
    [string]$SecretKey = "nqF3VPLLNuFqaTtKFbXQg6F3bhXUwVAxdfkIebQa",
    [string]$BaseUrl = "https://paper-api.alpaca.markets/v2"
)

# Headers for authentication
$headers = @{
    "APCA-API-KEY-ID" = $ApiKey
    "APCA-API-SECRET-KEY" = $SecretKey
    "Content-Type" = "application/json"
}

Write-Host "MASS AI Trading - Alpaca API Connection Test" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Green
Write-Host "Testing connection to: $BaseUrl" -ForegroundColor White
Write-Host "API Key: $ApiKey" -ForegroundColor White
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Green

$testsPassed = 0
$totalTests = 3

# Test 1: Account Information
Write-Host "Testing account information..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/account" -Headers $headers -Method Get
    Write-Host "SUCCESS: Account Info Retrieved!" -ForegroundColor Green
    Write-Host "   Account ID: $($response.id)" -ForegroundColor White
    Write-Host "   Buying Power: $($response.buying_power)" -ForegroundColor White
    Write-Host "   Cash: $($response.cash)" -ForegroundColor White
    Write-Host "   Portfolio Value: $($response.portfolio_value)" -ForegroundColor White
    $testsPassed++
} catch {
    Write-Host "FAILED: Account Info - $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Positions
Write-Host "Testing positions..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/positions" -Headers $headers -Method Get
    Write-Host "SUCCESS: Positions Retrieved!" -ForegroundColor Green
    Write-Host "   Current Positions: $($response.Count)" -ForegroundColor White
    if ($response.Count -eq 0) {
        Write-Host "   - No positions currently held" -ForegroundColor White
    }
    $testsPassed++
} catch {
    Write-Host "FAILED: Positions - $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Order Placement
Write-Host "Testing order placement..." -ForegroundColor Yellow
try {
    $orderData = @{
        symbol = "AAPL"
        qty = 1
        side = "buy"
        type = "limit"
        time_in_force = "day"
        limit_price = "50.00"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$BaseUrl/orders" -Headers $headers -Method Post -Body $orderData
    Write-Host "SUCCESS: Order Placed!" -ForegroundColor Green
    Write-Host "   Order ID: $($response.id)" -ForegroundColor White
    Write-Host "   Symbol: $($response.symbol)" -ForegroundColor White
    Write-Host "   Status: $($response.status)" -ForegroundColor White
    
    # Cancel the order immediately
    try {
        Invoke-RestMethod -Uri "$BaseUrl/orders/$($response.id)" -Headers $headers -Method Delete
        Write-Host "SUCCESS: Order Canceled!" -ForegroundColor Green
    } catch {
        Write-Host "WARNING: Order Cancel Failed" -ForegroundColor Yellow
    }
    
    $testsPassed++
} catch {
    Write-Host "FAILED: Order - $($_.Exception.Message)" -ForegroundColor Red
}

# Results Summary
Write-Host "================================================" -ForegroundColor Green
Write-Host "Test Results: $testsPassed/$totalTests tests passed" -ForegroundColor Cyan

if ($testsPassed -eq $totalTests) {
    Write-Host "All tests passed! Your Alpaca API is ready for trading!" -ForegroundColor Green
    Write-Host "" -ForegroundColor White
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "1. firebase functions:config:set alpaca.paper_key='$ApiKey'" -ForegroundColor White
    Write-Host "2. firebase functions:config:set alpaca.paper_secret='$SecretKey'" -ForegroundColor White
    Write-Host "3. Run: .\deploy-live.ps1" -ForegroundColor White
} else {
    Write-Host "Some tests failed. Please check your configuration." -ForegroundColor Red
}

Write-Host "================================================" -ForegroundColor Green
