# PowerShell script for comprehensive agent learning system integration test

# Set the console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "    AGENT LEARNING SYSTEM INTEGRATION TEST" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install required dependencies
Write-Host "Step 1: Installing required dependencies..." -ForegroundColor Yellow
python -m pip install numpy pandas requests flask fastapi uvicorn

# Step 2: Set up the test environment
Write-Host "Step 2: Setting up test environment..." -ForegroundColor Yellow
if (Test-Path -Path "trading_data") {
    Write-Host "  - Trading data directory already exists" -ForegroundColor Green
} else {
    Write-Host "  - Creating trading data directory structure" -ForegroundColor Green
    python initialize_trading_data.py
}

# Step 3: Validate system components
Write-Host "Step 3: Validating system components..." -ForegroundColor Yellow
$allComponentsPresent = $true

$requiredFiles = @(
    "trading_data_preservation.py",
    "agent_learning_manager.py",
    "remote_monitor.py",
    "test_agent_learning.py"
)

foreach ($file in $requiredFiles) {
    if (Test-Path -Path $file) {
        Write-Host "  - $file: Present" -ForegroundColor Green
    } else {
        Write-Host "  - $file: Missing" -ForegroundColor Red
        $allComponentsPresent = $false
    }
}

if (-not $allComponentsPresent) {
    Write-Host "ERROR: Missing required components. Cannot proceed with test." -ForegroundColor Red
    exit 1
}

# Step 4: Run short integration test (30 seconds)
Write-Host "Step 4: Running short integration test (30 seconds)..." -ForegroundColor Yellow
python test_agent_learning.py --duration 30

# Step 5: Verify integration between agent learning and data preservation
Write-Host "Step 5: Verifying integration points..." -ForegroundColor Yellow

# Check for agent learning directories
if (Test-Path -Path "trading_data/agent_learnings") {
    Write-Host "  - Agent learnings directory: Present" -ForegroundColor Green
    
    # Check for files in the directory
    $files = Get-ChildItem -Path "trading_data/agent_learnings" -ErrorAction SilentlyContinue
    if ($files.Count -gt 0) {
        Write-Host "  - Agent learning data files: $($files.Count) files found" -ForegroundColor Green
    } else {
        Write-Host "  - Agent learning data files: No files found" -ForegroundColor Yellow
    }
} else {
    Write-Host "  - Agent learnings directory: Missing" -ForegroundColor Red
}

# Step 6: Launch full test with monitor UI
Write-Host "Step 6: Would you like to run the full test with monitor UI? (y/n)" -ForegroundColor Yellow
$response = Read-Host

if ($response -eq "y" -or $response -eq "Y") {
    Write-Host "Starting full test with monitor UI..." -ForegroundColor Cyan
    Write-Host "The test will run for 2 minutes. You can view the monitor at http://localhost:8000" -ForegroundColor Cyan
    python launch_agent_learning_test.py --duration 120
} else {
    Write-Host "Skipping full test with monitor UI." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "    INTEGRATION TEST COMPLETED" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
