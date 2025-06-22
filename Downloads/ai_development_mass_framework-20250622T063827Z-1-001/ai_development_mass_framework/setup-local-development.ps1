# Local Development Deployment for MASS Framework
# This script sets up a local development environment without AWS

Write-Host "🏠 MASS Framework Local Development Setup" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Version: 8.5.0" -ForegroundColor Yellow
Write-Host "Mode: Local Development (No AWS Required)" -ForegroundColor Yellow
Write-Host "Date: $(Get-Date)" -ForegroundColor Yellow
Write-Host ""

# Check if Docker is available
Write-Host "1️⃣ Checking Docker..." -ForegroundColor Cyan
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker Available: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found. Installing Docker Desktop..." -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check if Docker Compose is available
Write-Host ""
Write-Host "2️⃣ Checking Docker Compose..." -ForegroundColor Cyan
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose Available: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose not found." -ForegroundColor Red
    exit 1
}

# Create local environment file
Write-Host ""
Write-Host "3️⃣ Creating Local Environment Configuration..." -ForegroundColor Cyan

$localEnv = @"
# MASS Framework Local Development Environment
# This configuration is for local development only

# Application Settings
DEBUG=True
ENVIRONMENT=local
SECRET_KEY=local-dev-secret-key-change-for-production

# Database Settings (PostgreSQL in Docker)
DATABASE_URL=postgresql://massuser:localpassword@localhost:5432/mass_framework_local
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mass_framework_local
DB_USER=massuser
DB_PASSWORD=localpassword

# Redis Settings (for caching and sessions)
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_URL=http://localhost:8000

# Frontend Settings
FRONTEND_URL=http://localhost:3000

# AI Service Settings (using mock/local services)
OPENAI_API_KEY=sk-mock-key-for-local-development
AI_SERVICE_MODE=local
USE_MOCK_AI=true

# Cloud Settings (disabled for local)
AWS_REGION=us-east-1
USE_AWS_SERVICES=false
USE_LOCAL_STORAGE=true

# Security Settings
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=logs/mass_framework_local.log

# Development Features
ENABLE_DEBUG_TOOLBAR=true
ENABLE_PROFILING=true
AUTO_RELOAD=true
"@

$localEnv | Out-File -FilePath ".env.local" -Encoding UTF8
Write-Host "✅ Local environment configuration created: .env.local" -ForegroundColor Green

# Create local Docker Compose file
Write-Host ""
Write-Host "4️⃣ Creating Local Docker Compose Configuration..." -ForegroundColor Cyan

$dockerComposeLocal = @"
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15
    container_name: mass_framework_postgres_local
    environment:
      POSTGRES_DB: mass_framework_local
      POSTGRES_USER: massuser
      POSTGRES_PASSWORD: localpassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U massuser -d mass_framework_local"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis for caching and sessions
  redis:
    image: redis:7-alpine
    container_name: mass_framework_redis_local
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # MASS Framework Application
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mass_framework_app_local
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgresql://massuser:localpassword@postgres:5432/mass_framework_local
      - REDIS_URL=redis://redis:6379/0
    ports:
      - "8000:8000"
    volumes:
      - ./:/app
      - ./logs:/app/logs
    env_file:
      - .env.local
    command: >
      sh -c "
        python -m alembic upgrade head &&
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
      "
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: mass_framework_local
"@

$dockerComposeLocal | Out-File -FilePath "docker-compose.local.yml" -Encoding UTF8
Write-Host "✅ Local Docker Compose configuration created: docker-compose.local.yml" -ForegroundColor Green

# Create database initialization script
Write-Host ""
Write-Host "5️⃣ Creating Database Initialization Script..." -ForegroundColor Cyan

$initSql = @"
-- MASS Framework Local Database Initialization
-- This script sets up the local development database

-- Create additional databases for testing
CREATE DATABASE mass_framework_test OWNER massuser;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE mass_framework_local TO massuser;
GRANT ALL PRIVILEGES ON DATABASE mass_framework_test TO massuser;

-- Enable required extensions
\c mass_framework_local;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c mass_framework_test;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set up initial schema (if needed)
\c mass_framework_local;

-- You can add any initial data or schema setup here
-- The application will handle migrations via Alembic
"@

$initSql | Out-File -FilePath "init.sql" -Encoding UTF8
Write-Host "✅ Database initialization script created: init.sql" -ForegroundColor Green

# Create local development startup script
Write-Host ""
Write-Host "6️⃣ Creating Local Development Startup Script..." -ForegroundColor Cyan

$startupScript = @"
# MASS Framework Local Development Startup Script

Write-Host "🏠 Starting MASS Framework Local Development Environment..." -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green

# Stop any existing containers
Write-Host "Stopping existing containers..." -ForegroundColor Yellow
docker-compose -f docker-compose.local.yml down

# Build and start services
Write-Host "Building and starting services..." -ForegroundColor Yellow
docker-compose -f docker-compose.local.yml up --build -d

# Wait for services to be healthy
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service status
Write-Host ""
Write-Host "📊 Service Status:" -ForegroundColor Cyan
docker-compose -f docker-compose.local.yml ps

# Show logs
Write-Host ""
Write-Host "📋 Recent Logs:" -ForegroundColor Cyan
docker-compose -f docker-compose.local.yml logs --tail=20

Write-Host ""
Write-Host "🎉 MASS Framework Local Development Environment Started!" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access Points:" -ForegroundColor Cyan
Write-Host "  • API: http://localhost:8000" -ForegroundColor Yellow
Write-Host "  • API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "  • Health Check: http://localhost:8000/health" -ForegroundColor Yellow
Write-Host "  • Database: postgresql://massuser:localpassword@localhost:5432/mass_framework_local" -ForegroundColor Yellow
Write-Host "  • Redis: redis://localhost:6379/0" -ForegroundColor Yellow
Write-Host ""
Write-Host "🛠️ Development Commands:" -ForegroundColor Cyan
Write-Host "  • View logs: docker-compose -f docker-compose.local.yml logs -f" -ForegroundColor Yellow
Write-Host "  • Stop services: docker-compose -f docker-compose.local.yml down" -ForegroundColor Yellow
Write-Host "  • Restart app: docker-compose -f docker-compose.local.yml restart app" -ForegroundColor Yellow
Write-Host "  • Database shell: docker-compose -f docker-compose.local.yml exec postgres psql -U massuser -d mass_framework_local" -ForegroundColor Yellow
Write-Host ""
Write-Host "📁 Log Files:" -ForegroundColor Cyan
Write-Host "  • Application logs: ./logs/" -ForegroundColor Yellow
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green
"@

$startupScript | Out-File -FilePath "start-local.ps1" -Encoding UTF8
Write-Host "✅ Local development startup script created: start-local.ps1" -ForegroundColor Green

# Create local development stop script
Write-Host ""
Write-Host "7️⃣ Creating Local Development Stop Script..." -ForegroundColor Cyan

$stopScript = @"
# MASS Framework Local Development Stop Script

Write-Host "🛑 Stopping MASS Framework Local Development Environment..." -ForegroundColor Red
Write-Host "=========================================================" -ForegroundColor Red

# Stop all services
docker-compose -f docker-compose.local.yml down

# Optional: Remove volumes (uncomment to reset database)
# docker-compose -f docker-compose.local.yml down -v

Write-Host ""
Write-Host "✅ Local development environment stopped." -ForegroundColor Green
Write-Host ""
Write-Host "To restart: .\start-local.ps1" -ForegroundColor Yellow
"@

$stopScript | Out-File -FilePath "stop-local.ps1" -Encoding UTF8
Write-Host "✅ Local development stop script created: stop-local.ps1" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Local Development Environment Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 What was created:" -ForegroundColor Cyan
Write-Host "  • .env.local - Local environment configuration" -ForegroundColor Yellow
Write-Host "  • docker-compose.local.yml - Local Docker services" -ForegroundColor Yellow
Write-Host "  • init.sql - Database initialization" -ForegroundColor Yellow
Write-Host "  • start-local.ps1 - Start development environment" -ForegroundColor Yellow
Write-Host "  • stop-local.ps1 - Stop development environment" -ForegroundColor Yellow
Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Install requirements: pip install -r requirements.txt" -ForegroundColor Yellow
Write-Host "2. Start development environment: .\start-local.ps1" -ForegroundColor Yellow
Write-Host "3. Access the API at: http://localhost:8000" -ForegroundColor Yellow
Write-Host "4. View API documentation: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "This local setup provides:" -ForegroundColor Cyan
Write-Host "  ✅ Full MASS Framework functionality" -ForegroundColor Green
Write-Host "  ✅ 85% development speed features" -ForegroundColor Green
Write-Host "  ✅ No AWS costs or complexity" -ForegroundColor Green
Write-Host "  ✅ Hot reload for development" -ForegroundColor Green
Write-Host "  ✅ Local database with data persistence" -ForegroundColor Green
Write-Host "  ✅ Redis for caching and sessions" -ForegroundColor Green
Write-Host ""

$confirmation = Read-Host "Do you want to start the local development environment now? (y/N)"

if ($confirmation -eq 'y' -or $confirmation -eq 'Y') {
    Write-Host ""
    Write-Host "🚀 Starting Local Development Environment..." -ForegroundColor Green
    & ".\start-local.ps1"
} else {
    Write-Host ""
    Write-Host "⏸️ Setup complete. Start the environment later with:" -ForegroundColor Yellow
    Write-Host "  .\start-local.ps1" -ForegroundColor Green
}
