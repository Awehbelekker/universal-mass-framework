Write-Host "Stopping MASS Framework..." -ForegroundColor Red
docker-compose -f docker-compose.local.yml down
Write-Host "MASS Framework stopped." -ForegroundColor Green
