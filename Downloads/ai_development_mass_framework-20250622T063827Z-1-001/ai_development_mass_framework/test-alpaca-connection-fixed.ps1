# MASS AI Trading - Alpaca API Connection Test (PowerShell)
# Test Alpaca paper trading API connectivity

# API Configuration
$API_KEY = "PKD86B3W4830DOMGZWED"
$SECRET_KEY = "nqF3VPLLNuFqaTtKFbXQg6F3bhXUwVAxdfkIebQa"
$BASE_URL = "https://paper-api.alpaca.markets/v2"

# Headers for authentication
$headers = @{
    "APCA-API-KEY-ID" = $API_KEY
    "APCA-API-SECRET-KEY" = $SECRET_KEY
    "Content-Type" = "application/json"
}

Write-Host "🚀 MASS AI Trading - Alpaca API Connection Test" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Green
Write-Host "Testing connection to: $BASE_URL" -ForegroundColor White
Write-Host "API Key: $API_KEY" -ForegroundColor White
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor White
Write-Host ("=" * 50) -ForegroundColor Green

$testsPassed = 0
$totalTests = 4

# Test 1: Account Information
Write-Host "`n🔍 Testing account information..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/account" -Headers $headers -Method Get
    Write-Host "✅ Account Info Retrieved Successfully!" -ForegroundColor Green
    Write-Host "   Account ID: $($response.id)" -ForegroundColor White
    Write-Host "   Buying Power: `$$($response.buying_power)" -ForegroundColor White
    Write-Host "   Cash: `$$($response.cash)" -ForegroundColor White
    Write-Host "   Portfolio Value: `$$($response.portfolio_value)" -ForegroundColor White
    Write-Host "   Day Trade Count: $($response.daytrade_count)" -ForegroundColor White
    $testsPassed++
} catch {
    Write-Host "❌ Account Info Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Market Data
Write-Host "`n📊 Testing market data..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/stocks/AAPL/quotes/latest" -Headers $headers -Method Get
    Write-Host "✅ Market Data Retrieved Successfully!" -ForegroundColor Green
    Write-Host "   Symbol: AAPL" -ForegroundColor White
    Write-Host "   Latest Quote: Available" -ForegroundColor White
    $testsPassed++
} catch {
    Write-Host "❌ Market Data Failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Note: Market data may require additional subscription" -ForegroundColor Yellow
}

# Test 3: Positions
Write-Host "`n📈 Testing positions..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/positions" -Headers $headers -Method Get
    Write-Host "✅ Positions Retrieved Successfully!" -ForegroundColor Green
    Write-Host "   Current Positions: $($response.Count)" -ForegroundColor White
    if ($response.Count -gt 0) {
        $response[0..2] | ForEach-Object {
            Write-Host "   - $($_.symbol): $($_.qty) shares @ `$$($_.avg_cost_basis)" -ForegroundColor White
        }
    } else {
        Write-Host "   - No positions currently held" -ForegroundColor White
    }
    $testsPassed++
} catch {
    Write-Host "❌ Positions Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Order Placement
Write-Host "`n💰 Testing order placement (limit order - won't execute)..." -ForegroundColor Yellow
try {
    $orderData = @{
        symbol = "AAPL"
        qty = 1
        side = "buy"
        type = "limit"
        time_in_force = "day"
        limit_price = "50.00"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$BASE_URL/orders" -Headers $headers -Method Post -Body $orderData
    Write-Host "✅ Order Placed Successfully!" -ForegroundColor Green
    Write-Host "   Order ID: $($response.id)" -ForegroundColor White
    Write-Host "   Symbol: $($response.symbol)" -ForegroundColor White
    Write-Host "   Status: $($response.status)" -ForegroundColor White
    Write-Host "   Side: $($response.side)" -ForegroundColor White
    Write-Host "   Limit Price: `$$($response.limit_price)" -ForegroundColor White
    
    # Cancel the order immediately
    try {
        Invoke-RestMethod -Uri "$BASE_URL/orders/$($response.id)" -Headers $headers -Method Delete
        Write-Host "✅ Order Canceled Successfully!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Order Cancel Warning: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    $testsPassed++
} catch {
    Write-Host "❌ Order Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Results Summary
Write-Host ("=" * 50) -ForegroundColor Green
Write-Host "🎯 Test Results: $testsPassed/$totalTests tests passed" -ForegroundColor Cyan

if ($testsPassed -eq $totalTests) {
    Write-Host "🎉 All tests passed! Your Alpaca API is ready for trading!" -ForegroundColor Green
    Write-Host "`n🚀 Next Steps:" -ForegroundColor Cyan
    Write-Host "1. Run: firebase functions:config:set alpaca.paper_key='PKD86B3W4830DOMGZWED'" -ForegroundColor White
    Write-Host "2. Run: firebase functions:config:set alpaca.paper_secret='nqF3VPLLNuFqaTtKFbXQg6F3bhXUwVAxdfkIebQa'" -ForegroundColor White
    Write-Host "3. Deploy to Firebase: .\deploy-live.ps1 -Production" -ForegroundColor White
} else {
    Write-Host "❌ Some tests failed. Please check your API keys and network connection." -ForegroundColor Red
}

Write-Host ("=" * 50) -ForegroundColor Green
