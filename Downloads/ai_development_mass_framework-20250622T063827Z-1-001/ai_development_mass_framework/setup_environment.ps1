# MASS Framework Environment Setup Script
# This script helps set up the environment for the MASS Framework

Write-Host "🔧 MASS Framework Environment Setup" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonInstalled = $false

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
        $pythonInstalled = $true
    }
} catch {
    Write-Host "Python not found via 'python' command" -ForegroundColor Yellow
}

if (-not $pythonInstalled) {
    try {
        $pythonVersion = py --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
            $pythonInstalled = $true
        }
    } catch {
        Write-Host "Python not found via 'py' command" -ForegroundColor Yellow
    }
}

if (-not $pythonInstalled) {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "To install Python:" -ForegroundColor Yellow
    Write-Host "1. Download Python from: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "2. During installation, make sure to check 'Add Python to PATH'" -ForegroundColor White
    Write-Host "3. Restart this terminal after installation" -ForegroundColor White
    Write-Host ""
    Write-Host "Or install via Microsoft Store:" -ForegroundColor Yellow
    Write-Host "1. Open Microsoft Store" -ForegroundColor White
    Write-Host "2. Search for 'Python'" -ForegroundColor White
    Write-Host "3. Install Python 3.8 or later" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
    } else {
        throw "Node.js not found"
    }
} catch {
    Write-Host "❌ Node.js is not installed" -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    # Upgrade pip
    python -m pip install --upgrade pip
    
    # Install requirements
    python -m pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python dependencies installed successfully" -ForegroundColor Green
    } else {
        throw "Failed to install Python dependencies"
    }
} catch {
    Write-Host "❌ Failed to install Python dependencies: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
try {
    Set-Location "frontend"
    npm install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Node.js dependencies installed successfully" -ForegroundColor Green
    } else {
        throw "Failed to install Node.js dependencies"
    }
    
    Set-Location ".."
} catch {
    Write-Host "❌ Failed to install Node.js dependencies: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Build frontend
Write-Host "Building frontend..." -ForegroundColor Yellow
try {
    Set-Location "frontend"
    npm run build
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Frontend built successfully" -ForegroundColor Green
        
        # Copy build to static directory
        if (Test-Path "build") {
            $staticPath = "..\static"
            if (Test-Path $staticPath) {
                Remove-Item $staticPath -Recurse -Force
            }
            Copy-Item "build" $staticPath -Recurse
            Write-Host "✓ Frontend copied to static directory" -ForegroundColor Green
        }
    } else {
        throw "Frontend build failed"
    }
    
    Set-Location ".."
} catch {
    Write-Host "❌ Frontend build failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Continuing without frontend build..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Environment setup complete!" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Start the server: python main.py" -ForegroundColor White
Write-Host "2. Open browser to: http://localhost:8000" -ForegroundColor White
Write-Host "3. Check API docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Ready to start the MASS Framework!" -ForegroundColor Green 