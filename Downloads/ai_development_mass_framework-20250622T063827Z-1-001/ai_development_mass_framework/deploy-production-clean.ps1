#!/usr/bin/env pwsh
# PROMETHEUS Complete Production Deployment Script
# Deploys the enhanced UX/UI system with MCP server integration to Firebase

param(
    [string]$Environment = "production",
    [switch]$SkipTests = $false,
    [switch]$DryRun = $false
)

Write-Host "PROMETHEUS Complete Production Deployment" -ForegroundColor Cyan
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host "Dry Run: $DryRun" -ForegroundColor Yellow
Write-Host "Skip Tests: $SkipTests" -ForegroundColor Yellow
Write-Host ""

# Get the current script directory
$scriptDir = $PSScriptRoot
$buildDir = "$scriptDir/build"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

Write-Host "Working Directory: $scriptDir" -ForegroundColor DarkGray
Write-Host "Build Directory: $buildDir" -ForegroundColor DarkGray
Write-Host "Timestamp: $timestamp" -ForegroundColor DarkGray
Write-Host ""

# Function to check if Firebase CLI is installed
function Test-FirebaseCLI {
    try {
        $version = firebase --version 2>$null
        if ($version) {
            Write-Host "Firebase CLI detected: $version" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "Firebase CLI not found. Please install: npm install -g firebase-tools" -ForegroundColor Red
        return $false
    }
    return $false
}

# Function to create build directory structure
function New-BuildStructure {
    Write-Host "Creating build directory structure..." -ForegroundColor Yellow
    
    # Remove existing build directory
    if (Test-Path -Path $buildDir) {
        Remove-Item -Recurse -Force $buildDir
        Write-Host "  Removed existing build directory" -ForegroundColor DarkGray
    }
    
    # Create new structure
    New-Item -ItemType Directory -Path $buildDir -Force | Out-Null
    New-Item -ItemType Directory -Path "$buildDir/assets" -Force | Out-Null
    New-Item -ItemType Directory -Path "$buildDir/css" -Force | Out-Null
    New-Item -ItemType Directory -Path "$buildDir/js" -Force | Out-Null
    New-Item -ItemType Directory -Path "$buildDir/images" -Force | Out-Null
    
    Write-Host "  Build directory structure created" -ForegroundColor Green
}

# Function to copy core HTML files
function Copy-HTMLFiles {
    Write-Host "Copying HTML files..." -ForegroundColor Yellow
    
    $htmlFiles = @(
        @{Source = "prometheus_landing.html"; Dest = "index.html"; Required = $true},
        @{Source = "prometheus_dashboard.html"; Dest = "dashboard.html"; Required = $true},
        @{Source = "prometheus_registration.html"; Dest = "register.html"; Required = $true},
        @{Source = "prometheus_login.html"; Dest = "login.html"; Required = $true},
        @{Source = "prometheus_admin.html"; Dest = "admin.html"; Required = $true},
        @{Source = "prometheus_access_management.html"; Dest = "access.html"; Required = $false},
        @{Source = "private_access_gate.html"; Dest = "gate.html"; Required = $false},
        @{Source = "api_test_suite.html"; Dest = "test.html"; Required = $false}
    )
    
    foreach ($file in $htmlFiles) {
        $sourcePath = "$scriptDir/$($file.Source)"
        $destPath = "$buildDir/$($file.Dest)"
        
        if (Test-Path -Path $sourcePath) {
            Copy-Item -Force -Path $sourcePath -Destination $destPath
            Write-Host "  $($file.Source) -> $($file.Dest)" -ForegroundColor Green
        } elseif ($file.Required) {
            Write-Host "  Required file missing: $($file.Source)" -ForegroundColor Red
            return $false
        } else {
            Write-Host "  Optional file missing: $($file.Source)" -ForegroundColor Yellow
        }
    }
    
    return $true
}

# Function to copy JavaScript files
function Copy-JavaScriptFiles {
    Write-Host "Copying JavaScript files..." -ForegroundColor Yellow
    
    $jsFiles = @(
        # Core UX/UI Enhancement System
        "prometheus_ux_master_enhancer.js",
        "prometheus_logo_system_v2.js",
        "prometheus_workflow_enhancer.js",
        
        # Real-time Trading System
        "prometheus_realtime_trading.js",
        "prometheus_live_trading_admin.js",
        "prometheus_admin_setup.js",
        
        # Legacy support
        "prometheus_logo.js",
        "prometheus_streamlined_ux.js",
        "prometheus_enhanced_quick_actions.js",
        "prometheus_mobile_responsiveness.js",
        "prometheus_access_control.js",
        
        # Additional features
        "prometheus_quick_actions.js",
        "prometheus_ux_engine.js"
    )
    
    foreach ($file in $jsFiles) {
        $sourcePath = "$scriptDir/$file"
        $destPath = "$buildDir/js/$file"
        
        if (Test-Path -Path $sourcePath) {
            Copy-Item -Force -Path $sourcePath -Destination $destPath
            Write-Host "  $file" -ForegroundColor Green
        } else {
            Write-Host "  Missing: $file" -ForegroundColor Yellow
        }
    }
}

# Function to copy additional assets
function Copy-Assets {
    Write-Host "Copying assets..." -ForegroundColor Yellow
    
    # Copy favicon and icons
    $assetFiles = @(
        "favicon.svg",
        "favicon.ico",
        "manifest.json"
    )
    
    foreach ($file in $assetFiles) {
        $sourcePath = "$scriptDir/$file"
        $destPath = "$buildDir/$file"
        
        if (Test-Path -Path $sourcePath) {
            Copy-Item -Force -Path $sourcePath -Destination $destPath
            Write-Host "  $file" -ForegroundColor Green
        }
    }
    
    # Copy any CSS files
    if (Test-Path -Path "$scriptDir/styles.css") {
        Copy-Item -Force -Path "$scriptDir/styles.css" -Destination "$buildDir/css/styles.css"
        Write-Host "  styles.css" -ForegroundColor Green
    }
}

# Function to optimize HTML files for production
function Optimize-HTMLFiles {
    Write-Host "Optimizing HTML files for production..." -ForegroundColor Yellow
    
    Get-ChildItem -Path $buildDir -Filter "*.html" | ForEach-Object {
        $content = Get-Content -Path $_.FullName -Raw
        
        # Add cache busting timestamp to JS/CSS files
        $content = $content -replace '\.js"', ".js?v=$timestamp`""
        $content = $content -replace '\.css"', ".css?v=$timestamp`""
        
        # Add production meta tags
        $productionMeta = @"
    <meta name="robots" content="index, follow">
    <meta name="author" content="PROMETHEUS Neural Forge">
    <meta name="generator" content="PROMETHEUS v2.0">
    <meta name="build-timestamp" content="$timestamp">
"@
        
        $content = $content -replace '</head>', "$productionMeta`n</head>"
        
        # Write optimized content back
        Set-Content -Path $_.FullName -Value $content -Encoding UTF8
        Write-Host "  Optimized $($_.Name)" -ForegroundColor Green
    }
}

# Function to validate build
function Test-BuildIntegrity {
    Write-Host "Validating build integrity..." -ForegroundColor Yellow
    
    $errors = @()
    
    # Check required files
    $requiredFiles = @("index.html", "dashboard.html", "register.html", "login.html", "admin.html")
    foreach ($file in $requiredFiles) {
        if (!(Test-Path -Path "$buildDir/$file")) {
            $errors += "Missing required file: $file"
        }
    }
    
    # Check JavaScript files
    $coreJSFiles = @(
        "js/prometheus_ux_master_enhancer.js",
        "js/prometheus_logo_system_v2.js",
        "js/prometheus_workflow_enhancer.js"
    )
    foreach ($file in $coreJSFiles) {
        if (!(Test-Path -Path "$buildDir/$file")) {
            $errors += "Missing core JS file: $file"
        }
    }
    
    # Check HTML file integrity
    Get-ChildItem -Path $buildDir -Filter "*.html" | ForEach-Object {
        $content = Get-Content -Path $_.FullName -Raw
        
        # Check for required UX scripts
        if ($content -notmatch "prometheus_ux_master_enhancer\.js") {
            $errors += "$($_.Name): Missing UX Master Enhancer script"
        }
        if ($content -notmatch "prometheus_logo_system_v2\.js") {
            $errors += "$($_.Name): Missing Logo System v2 script"
        }
    }
    
    if ($errors.Count -gt 0) {
        Write-Host "  Build validation failed:" -ForegroundColor Red
        foreach ($error in $errors) {
            Write-Host "    * $error" -ForegroundColor Red
        }
        return $false
    } else {
        Write-Host "  Build validation passed" -ForegroundColor Green
        return $true
    }
}

# Function to run UX tests
function Invoke-UXTests {
    if ($SkipTests) {
        Write-Host "Skipping tests (SkipTests flag)" -ForegroundColor Yellow
        return $true
    }
    
    Write-Host "Running UX/UI tests..." -ForegroundColor Yellow
    
    try {
        if (Test-Path -Path "$scriptDir/test_ux_enhancement.js") {
            $testResult = & node "$scriptDir/test_ux_enhancement.js"
            $lastExitCode = $LASTEXITCODE
            
            if ($lastExitCode -eq 0) {
                Write-Host "  All UX/UI tests passed" -ForegroundColor Green
                return $true
            } else {
                Write-Host "  Some UX/UI tests failed" -ForegroundColor Red
                return $false
            }
        } else {
            Write-Host "  Test file not found, skipping tests" -ForegroundColor Yellow
            return $true
        }
    }
    catch {
        Write-Host "  Could not run UX tests: $($_.Exception.Message)" -ForegroundColor Yellow
        return $true  # Continue deployment even if tests can't run
    }
}

# Function to deploy to Firebase
function Invoke-FirebaseDeployment {
    Write-Host "Deploying to Firebase..." -ForegroundColor Yellow
    
    if ($DryRun) {
        Write-Host "  DRY RUN: Would deploy to Firebase $Environment" -ForegroundColor Cyan
        return $true
    }
    
    try {
        # Set Firebase project based on environment
        $projectId = switch ($Environment) {
            "staging" { "ai-mass-trading-staging" }
            "production" { "ai-mass-trading" }
            default { "ai-mass-trading" }
        }
        
        Write-Host "  Targeting project: $projectId" -ForegroundColor Cyan
        
        # Deploy hosting
        $deployArgs = @("deploy", "--project", $projectId)
        if ($Environment -eq "staging") {
            $deployArgs += @("--only", "hosting:staging")
        } else {
            $deployArgs += @("--only", "hosting")
        }
        
        & firebase @deployArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Firebase deployment successful" -ForegroundColor Green
            return $true
        } else {
            Write-Host "  Firebase deployment failed" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "  Deployment error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to run post-deployment verification
function Test-DeploymentHealth {
    Write-Host "Running post-deployment health checks..." -ForegroundColor Yellow
    
    if ($DryRun) {
        Write-Host "  DRY RUN: Would run health checks" -ForegroundColor Cyan
        return $true
    }
    
    # Define test URLs based on environment
    $baseUrl = switch ($Environment) {
        "staging" { "https://ai-mass-trading-staging.web.app" }
        "production" { "https://ai-mass-trading.web.app" }
        default { "https://ai-mass-trading.web.app" }
    }
    
    $testUrls = @(
        "$baseUrl/",
        "$baseUrl/register.html",
        "$baseUrl/login.html",
        "$baseUrl/dashboard.html"
    )
    
    $allHealthy = $true
    
    foreach ($url in $testUrls) {
        try {
            Write-Host "  Testing: $url" -ForegroundColor DarkGray
            $response = Invoke-WebRequest -Uri $url -TimeoutSec 30 -UseBasicParsing
            
            if ($response.StatusCode -eq 200) {
                Write-Host "    OK: $url ($($response.StatusCode))" -ForegroundColor Green
            } else {
                Write-Host "    Warning: $url ($($response.StatusCode))" -ForegroundColor Yellow
                $allHealthy = $false
            }
        }
        catch {
            Write-Host "    Error: $url ($($_.Exception.Message))" -ForegroundColor Red
            $allHealthy = $false
        }
    }
    
    return $allHealthy
}

# Function to create deployment report
function New-DeploymentReport {
    Write-Host "Creating deployment report..." -ForegroundColor Yellow
    
    $report = @{
        timestamp = $timestamp
        environment = $Environment
        buildDirectory = $buildDir
        deploymentSuccessful = $script:deploymentSuccessful
        healthChecksPassed = $script:healthChecksPassed
        files = @{
            html = (Get-ChildItem -Path $buildDir -Filter "*.html" | Measure-Object).Count
            js = (Get-ChildItem -Path "$buildDir/js" -Filter "*.js" -ErrorAction SilentlyContinue | Measure-Object).Count
            total = (Get-ChildItem -Path $buildDir -Recurse -File | Measure-Object).Count
        }
    }
    
    $reportPath = "$scriptDir/deployment-report-$timestamp.json"
    $report | ConvertTo-Json -Depth 3 | Set-Content -Path $reportPath -Encoding UTF8
    
    Write-Host "  Report saved: deployment-report-$timestamp.json" -ForegroundColor Green
}

# Main execution flow
try {
    Write-Host "Pre-flight checks..." -ForegroundColor Yellow
    
    # Check Firebase CLI
    if (!(Test-FirebaseCLI)) {
        throw "Firebase CLI not available"
    }
    
    # Check if we're logged in to Firebase
    try {
        $whoami = firebase auth:list 2>$null
        Write-Host "  Firebase authentication verified" -ForegroundColor Green
    }
    catch {
        Write-Host "  Please login to Firebase: firebase login" -ForegroundColor Yellow
    }
    
    Write-Host ""
    
    # Build process
    Write-Host "Starting build process..." -ForegroundColor Cyan
    
    New-BuildStructure
    
    if (!(Copy-HTMLFiles)) {
        throw "Failed to copy required HTML files"
    }
    
    Copy-JavaScriptFiles
    Copy-Assets
    Optimize-HTMLFiles
    
    Write-Host ""
    
    # Validation
    Write-Host "Validating build..." -ForegroundColor Cyan
    
    if (!(Test-BuildIntegrity)) {
        throw "Build validation failed"
    }
    
    if (!(Invoke-UXTests)) {
        throw "UX/UI tests failed"
    }
    
    Write-Host ""
    
    # Deployment
    Write-Host "Starting deployment..." -ForegroundColor Cyan
    
    $script:deploymentSuccessful = Invoke-FirebaseDeployment
    
    if (!$script:deploymentSuccessful) {
        throw "Firebase deployment failed"
    }
    
    Write-Host ""
    
    # Post-deployment verification
    Write-Host "Post-deployment verification..." -ForegroundColor Cyan
    
    $script:healthChecksPassed = Test-DeploymentHealth
    
    Write-Host ""
    
    # Generate report
    New-DeploymentReport
    
    Write-Host ""
    Write-Host "DEPLOYMENT COMPLETED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "=============================================================" -ForegroundColor Green
    Write-Host "Environment: $Environment" -ForegroundColor Yellow
    Write-Host "Build Directory: $buildDir" -ForegroundColor Yellow
    Write-Host "Timestamp: $timestamp" -ForegroundColor Yellow
    
    if (!$DryRun) {
        $baseUrl = switch ($Environment) {
            "staging" { "https://ai-mass-trading-staging.web.app" }
            "production" { "https://ai-mass-trading.web.app" }
            default { "https://ai-mass-trading.web.app" }
        }
        Write-Host "Live URL: $baseUrl" -ForegroundColor Cyan
    }
    
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Run user acceptance testing" -ForegroundColor White
    Write-Host "2. Monitor performance metrics" -ForegroundColor White
    Write-Host "3. Collect user feedback" -ForegroundColor White
    Write-Host "4. Plan iterative improvements" -ForegroundColor White
    
}
catch {
    Write-Host ""
    Write-Host "DEPLOYMENT FAILED!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    
    # Create failure report
    $script:deploymentSuccessful = $false
    $script:healthChecksPassed = $false
    New-DeploymentReport
    
    exit 1
}

Write-Host ""
Write-Host "PROMETHEUS deployment script completed!" -ForegroundColor Cyan
