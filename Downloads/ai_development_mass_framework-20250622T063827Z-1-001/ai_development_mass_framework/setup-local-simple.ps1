# Local Development Setup for MASS Framework

Write-Host "MASS Framework Local Development Setup" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

# Check Docker
Write-Host "Checking Docker..." -ForegroundColor Cyan
try {
    docker --version | Out-Null
    Write-Host "Docker is available" -ForegroundColor Green
} catch {
    Write-Host "Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Create environment file
Write-Host "Creating local environment file..." -ForegroundColor Cyan
$envContent = @'
DEBUG=True
ENVIRONMENT=local
SECRET_KEY=local-dev-secret

DATABASE_URL=postgresql://massuser:localpassword@localhost:5432/mass_framework_local
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mass_framework_local
DB_USER=massuser
DB_PASSWORD=localpassword

REDIS_URL=redis://localhost:6379/0
API_HOST=0.0.0.0
API_PORT=8000

OPENAI_API_KEY=sk-mock-key
AI_SERVICE_MODE=local
USE_MOCK_AI=true
'@

$envContent | Out-File -FilePath ".env.local" -Encoding UTF8
Write-Host "Environment file created: .env.local" -ForegroundColor Green

# Create Docker Compose file
Write-Host "Creating Docker Compose configuration..." -ForegroundColor Cyan
$composeContent = @'
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: mass_postgres_local
    environment:
      POSTGRES_DB: mass_framework_local
      POSTGRES_USER: massuser
      POSTGRES_PASSWORD: localpassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    container_name: mass_redis_local
    ports:
      - "6379:6379"

  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mass_app_local
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"
    volumes:
      - ./:/app
    env_file:
      - .env.local
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
'@

$composeContent | Out-File -FilePath "docker-compose.local.yml" -Encoding UTF8
Write-Host "Docker Compose file created: docker-compose.local.yml" -ForegroundColor Green

# Create start script
$startScript = @'
Write-Host "Starting MASS Framework locally..." -ForegroundColor Green
docker-compose -f docker-compose.local.yml up --build -d
Start-Sleep -Seconds 10
Write-Host "MASS Framework started!" -ForegroundColor Green
Write-Host "API: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor Yellow
'@

$startScript | Out-File -FilePath "start-local.ps1" -Encoding UTF8
Write-Host "Start script created: start-local.ps1" -ForegroundColor Green

# Create stop script
$stopScript = @'
Write-Host "Stopping MASS Framework..." -ForegroundColor Red
docker-compose -f docker-compose.local.yml down
Write-Host "MASS Framework stopped." -ForegroundColor Green
'@

$stopScript | Out-File -FilePath "stop-local.ps1" -Encoding UTF8
Write-Host "Stop script created: stop-local.ps1" -ForegroundColor Green

Write-Host ""
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "===============" -ForegroundColor Green
Write-Host ""
Write-Host "To start: .\start-local.ps1" -ForegroundColor Yellow
Write-Host "To stop:  .\stop-local.ps1" -ForegroundColor Yellow
Write-Host ""

$start = Read-Host "Start the local environment now? (y/N)"
if ($start -eq 'y' -or $start -eq 'Y') {
    Write-Host "Starting now..." -ForegroundColor Green
    & .\start-local.ps1
}
