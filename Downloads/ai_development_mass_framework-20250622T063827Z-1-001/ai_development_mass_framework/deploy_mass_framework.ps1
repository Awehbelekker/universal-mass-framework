# MASS Framework Deployment Script
# This script deploys the complete MASS Framework system

param(
    [string]$Environment = "development",
    [string]$DeployFrontend = "true",
    [string]$DeployBackend = "true",
    [string]$RunTests = "true"
)

Write-Host "🚀 MASS Framework Deployment Script" -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host "Timestamp: $(Get-Date)" -ForegroundColor Gray

# Configuration
$ProjectRoot = $PSScriptRoot
$FrontendPath = "$ProjectRoot\frontend"
$BackendPath = $ProjectRoot
$LogPath = "$ProjectRoot\deployment.log"

# Initialize logging
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    Add-Content -Path $LogPath -Value $logMessage
}

Write-Log "Starting MASS Framework deployment..."

# Step 1: Environment Check
Write-Log "Step 1: Checking environment..."
try {
    # Check Python
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "✓ Python found: $pythonVersion"
    } else {
        throw "Python not found. Please install Python 3.8+"
    }
    
    # Check Node.js
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "✓ Node.js found: $nodeVersion"
    } else {
        throw "Node.js not found. Please install Node.js 16+"
    }
    
    # Check Docker
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "✓ Docker found: $dockerVersion"
    } else {
        Write-Log "⚠ Docker not found. Some features may not work."
    }
    
} catch {
    Write-Log "❌ Environment check failed: $($_.Exception.Message)" -Level "ERROR"
    exit 1
}

# Step 2: Install Dependencies
Write-Log "Step 2: Installing dependencies..."
try {
    # Install Python dependencies
    if ($DeployBackend -eq "true") {
        Write-Log "Installing Python dependencies..."
        Set-Location $BackendPath
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✓ Python dependencies installed successfully"
        } else {
            throw "Failed to install Python dependencies"
        }
    }
    
    # Install Node.js dependencies
    if ($DeployFrontend -eq "true") {
        Write-Log "Installing Node.js dependencies..."
        Set-Location $FrontendPath
        npm install
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✓ Node.js dependencies installed successfully"
        } else {
            throw "Failed to install Node.js dependencies"
        }
    }
    
} catch {
    Write-Log "❌ Dependency installation failed: $($_.Exception.Message)" -Level "ERROR"
    exit 1
}

# Step 3: Run Tests
if ($RunTests -eq "true") {
    Write-Log "Step 3: Running system tests..."
    try {
        Set-Location $BackendPath
        python test_system_startup.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✓ All system tests passed"
        } else {
            throw "System tests failed"
        }
    } catch {
        Write-Log "❌ System tests failed: $($_.Exception.Message)" -Level "ERROR"
        Write-Log "Continuing with deployment despite test failures..."
    }
}

# Step 4: Build Frontend
if ($DeployFrontend -eq "true") {
    Write-Log "Step 4: Building frontend..."
    try {
        Set-Location $FrontendPath
        
        # Build React app
        Write-Log "Building React application..."
        npm run build
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✓ Frontend built successfully"
        } else {
            throw "Frontend build failed"
        }
        
        # Copy build to backend static directory
        if (Test-Path "build") {
            $staticPath = "$BackendPath\static"
            if (Test-Path $staticPath) {
                Remove-Item $staticPath -Recurse -Force
            }
            Copy-Item "build" $staticPath -Recurse
            Write-Log "✓ Frontend copied to backend static directory"
        }
        
    } catch {
        Write-Log "❌ Frontend build failed: $($_.Exception.Message)" -Level "ERROR"
        exit 1
    }
}

# Step 5: Start Backend Server
if ($DeployBackend -eq "true") {
    Write-Log "Step 5: Starting backend server..."
    try {
        Set-Location $BackendPath
        
        # Check if server is already running
        $serverProcess = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
            $_.CommandLine -like "*main.py*" -or $_.CommandLine -like "*uvicorn*"
        }
        
        if ($serverProcess) {
            Write-Log "⚠ Backend server already running. Stopping existing process..."
            $serverProcess | Stop-Process -Force
            Start-Sleep -Seconds 2
        }
        
        # Start server in background
        Write-Log "Starting MASS Framework backend server..."
        Start-Process -FilePath "python" -ArgumentList "main.py" -WindowStyle Hidden
        
        # Wait for server to start
        $maxAttempts = 30
        $attempt = 0
        $serverReady = $false
        
        while ($attempt -lt $maxAttempts -and -not $serverReady) {
            Start-Sleep -Seconds 2
            $attempt++
            
            try {
                $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
                if ($response.status -eq "healthy") {
                    $serverReady = $true
                    Write-Log "✓ Backend server started successfully"
                }
            } catch {
                Write-Log "Waiting for server to start... (attempt $attempt/$maxAttempts)"
            }
        }
        
        if (-not $serverReady) {
            throw "Backend server failed to start within timeout"
        }
        
    } catch {
        Write-Log "❌ Backend server startup failed: $($_.Exception.Message)" -Level "ERROR"
        exit 1
    }
}

# Step 6: Verify Deployment
Write-Log "Step 6: Verifying deployment..."
try {
    # Test health endpoint
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Log "✓ Health endpoint: $($healthResponse.status)"
    
    # Test status endpoint
    $statusResponse = Invoke-RestMethod -Uri "http://localhost:8000/status" -Method Get
    Write-Log "✓ Status endpoint: $($statusResponse.status)"
    
    # Test frontend (if deployed)
    if ($DeployFrontend -eq "true") {
        $frontendResponse = Invoke-WebRequest -Uri "http://localhost:8000" -Method Get
        if ($frontendResponse.StatusCode -eq 200) {
            Write-Log "✓ Frontend accessible"
        } else {
            Write-Log "⚠ Frontend may not be accessible"
        }
    }
    
} catch {
    Write-Log "❌ Deployment verification failed: $($_.Exception.Message)" -Level "ERROR"
    exit 1
}

# Step 7: Display Access Information
Write-Log "Step 7: Deployment complete!"
Write-Host ""
Write-Host "🎉 MASS Framework Deployment Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access URLs:" -ForegroundColor Yellow
Write-Host "  • Main Application: http://localhost:8000" -ForegroundColor White
Write-Host "  • API Documentation: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  • Health Check: http://localhost:8000/health" -ForegroundColor White
Write-Host "  • System Status: http://localhost:8000/status" -ForegroundColor White
Write-Host ""
Write-Host "API Endpoints:" -ForegroundColor Yellow
Write-Host "  • Generate App: POST http://localhost:8000/api/generate-app" -ForegroundColor White
Write-Host "  • Quick Demo: POST http://localhost:8000/api/demo/quick-app" -ForegroundColor White
Write-Host "  • Workflow Status: GET http://localhost:8000/api/workflow/{id}" -ForegroundColor White
Write-Host "  • System Metrics: GET http://localhost:8000/api/metrics" -ForegroundColor White
Write-Host ""
Write-Host "Logs:" -ForegroundColor Yellow
Write-Host "  • Deployment Log: $LogPath" -ForegroundColor White
Write-Host ""
Write-Host "To stop the server:" -ForegroundColor Yellow
Write-Host "  • Press Ctrl+C in this terminal" -ForegroundColor White
Write-Host "  • Or run: Get-Process -Name python | Where-Object {`$_.CommandLine -like '*main.py*'} | Stop-Process" -ForegroundColor White
Write-Host ""

# Step 8: Optional - Open Browser
$openBrowser = Read-Host "Open MASS Framework in browser? (y/n)"
if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
    Start-Process "http://localhost:8000"
    Write-Log "Opened MASS Framework in browser"
}

Write-Log "Deployment script completed successfully" 