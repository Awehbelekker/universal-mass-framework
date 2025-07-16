# Test Alpaca API Connection (PowerShell)
# Run this to verify your API keys work correctly

$API_KEY = "PKD86B3W4830DOMGZWED"
$SECRET_KEY = "nqF3VPLLNuFqaTtKFbXQg6F3bhXUwVAxdfkIebQa"
$BASE_URL = "https://paper-api.alpaca.markets/v2"

# Headers for authentication
$headers = @{
    "APCA-API-KEY-ID" = $API_KEY
    "APCA-API-SECRET-KEY" = $SECRET_KEY
    "Content-Type" = "application/json"
}

function Test-AccountInfo {
    Write-Host "🔍 Testing account information..." -ForegroundColor Blue
    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL/account" -Method GET -Headers $headers
        Write-Host "✅ Account Info Retrieved Successfully!" -ForegroundColor Green
        Write-Host "   Account ID: $($response.id)" -ForegroundColor White
        Write-Host "   Buying Power: $([math]::Round([decimal]$response.buying_power, 2))" -ForegroundColor White
        Write-Host "   Cash: $([math]::Round([decimal]$response.cash, 2))" -ForegroundColor White
        Write-Host "   Portfolio Value: $([math]::Round([decimal]$response.portfolio_value, 2))" -ForegroundColor White
        Write-Host "   Day Trade Count: $($response.daytrade_count)" -ForegroundColor White
        return $true
    }
    catch {
        Write-Host "❌ Account Info Failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Test-MarketData {
    Write-Host "`n📊 Testing market data..." -ForegroundColor Blue
    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL/stocks/AAPL/quotes/latest" -Method GET -Headers $headers
        Write-Host "✅ Market Data Retrieved Successfully!" -ForegroundColor Green
        Write-Host "   AAPL Latest Quote:" -ForegroundColor White
        Write-Host "   Bid: $($response.quote.bp)" -ForegroundColor White
        Write-Host "   Ask: $($response.quote.ap)" -ForegroundColor White
        Write-Host "   Timestamp: $($response.quote.t)" -ForegroundColor White
        return $true
    }
    catch {
        Write-Host "❌ Market Data Failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Test-Positions {
    Write-Host "`n📈 Testing positions..." -ForegroundColor Blue
    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL/positions" -Method GET -Headers $headers
        Write-Host "✅ Positions Retrieved Successfully!" -ForegroundColor Green
        Write-Host "   Current Positions: $($response.Count)" -ForegroundColor White
        if ($response.Count -gt 0) {
            $response | Select-Object -First 3 | ForEach-Object {
                Write-Host "   - $($_.symbol): $($_.qty) shares @ $($_.avg_cost_basis)" -ForegroundColor White
            }
        } else {
            Write-Host "   - No positions currently held" -ForegroundColor White
        }
        return $true
    }
    catch {
        Write-Host "❌ Positions Failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Test-PlaceOrder {
    Write-Host "`n💰 Testing order placement (limit order - won't execute)..." -ForegroundColor Blue
    try {
        $orderData = @{
            symbol = "AAPL"
            qty = 1
            side = "buy"
            type = "limit"
            time_in_force = "day"
            limit_price = "50.00"  # Very low price, won't execute
        } | ConvertTo-Json

        $response = Invoke-RestMethod -Uri "$BASE_URL/orders" -Method POST -Headers $headers -Body $orderData
        Write-Host "✅ Order Placed Successfully!" -ForegroundColor Green
        Write-Host "   Order ID: $($response.id)" -ForegroundColor White
        Write-Host "   Symbol: $($response.symbol)" -ForegroundColor White
        Write-Host "   Status: $($response.status)" -ForegroundColor White

        # Cancel the order immediately
        try {
            Invoke-RestMethod -Uri "$BASE_URL/orders/$($response.id)" -Method DELETE -Headers $headers
            Write-Host "✅ Order Canceled Successfully!" -ForegroundColor Green
        } catch {
            Write-Host "⚠️ Could not cancel order: $($_.Exception.Message)" -ForegroundColor Yellow
        }

        return $true
    }
    catch {
        Write-Host "❌ Order Failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main execution
Write-Host "🚀 MASS AI Trading - Alpaca API Connection Test" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green
Write-Host "Testing connection to: $BASE_URL" -ForegroundColor Yellow
Write-Host "API Key: $API_KEY" -ForegroundColor Yellow
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Green

$testsPassed = 0
$totalTests = 4

# Run all tests
if (Test-AccountInfo) { $testsPassed++ }
if (Test-MarketData) { $testsPassed++ }
if (Test-Positions) { $testsPassed++ }
if (Test-PlaceOrder) { $testsPassed++ }

Write-Host "`n$('=' * 50)" -ForegroundColor Green
Write-Host "🎯 Test Results: $testsPassed/$totalTests tests passed" -ForegroundColor Cyan

if ($testsPassed -eq $totalTests) {
    Write-Host "✅ All tests passed! Your API connection is working perfectly!" -ForegroundColor Green
    Write-Host "`n🎉 Ready for live trading integration!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "1. Run: firebase functions:config:set alpaca.paper_key='PKD86B3W4830DOMGZWED'" -ForegroundColor White
    Write-Host "2. Run: firebase functions:config:set alpaca.paper_secret='nqF3VPLLNuFqaTtKFbXQg6F3bhXUwVAxdfkIebQa'" -ForegroundColor White
    Write-Host "3. Deploy to Firebase: .\deploy-live.ps1 -Production" -ForegroundColor White
} else {
    Write-Host "❌ Some tests failed. Please check your API keys and network connection." -ForegroundColor Red
}

Write-Host "=" * 50 -ForegroundColor Green
