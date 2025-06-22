Write-Host "Starting MASS Framework locally..." -ForegroundColor Green
docker-compose -f docker-compose.local.yml up --build -d
Start-Sleep -Seconds 10
Write-Host "MASS Framework started!" -ForegroundColor Green
Write-Host "API: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor Yellow
