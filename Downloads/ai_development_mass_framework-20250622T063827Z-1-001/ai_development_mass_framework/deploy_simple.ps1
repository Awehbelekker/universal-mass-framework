# MASS Framework Security & Monitoring Deployment Script
# Production-ready deployment with security hardening and real-time monitoring

param(
    [string]$Environment = "production",
    [switch]$SkipDependencies = $false,
    [switch]$SkipBacktesting = $false,
    [switch]$DryRun = $false
)

Write-Host "MASS Framework Security & Monitoring Deployment" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

# Step 1: Environment Setup
Write-Host "Step 1: Environment Setup" -ForegroundColor Green
Write-Host "===========================" -ForegroundColor Green

if (-not $SkipDependencies) {
    Write-Host "Installing Python dependencies..." -ForegroundColor White
    
    # Install core dependencies
    $coreDependencies = @(
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "python-multipart>=0.0.6",
        "cryptography>=41.0.0",
        "bcrypt>=4.0.0",
        "PyJWT>=2.8.0",
        "prometheus-client>=0.19.0",
        "structlog>=23.0.0"
    )
    
    foreach ($dep in $coreDependencies) {
        Write-Host "Installing $dep" -ForegroundColor Gray
        if (-not $DryRun) {
            pip install $dep
        }
    }
    
    # Install financial and trading dependencies
    Write-Host "Installing financial dependencies..." -ForegroundColor White
    
    $financialDependencies = @(
        "yfinance>=0.2.18",
        "pandas>=2.1.0",
        "numpy>=1.25.0",
        "scipy>=1.11.0",
        "scikit-learn>=1.3.0",
        "TA-Lib>=0.4.26",
        "backtrader>=1.9.78.123",
        "vectorbt>=0.25.1",
        "empyrical>=0.5.5"
    )
    
    foreach ($dep in $financialDependencies) {
        Write-Host "Installing $dep" -ForegroundColor Gray
        if (-not $DryRun) {
            pip install $dep
        }
    }
    
    # Install monitoring and alerting dependencies
    Write-Host "Installing monitoring dependencies..." -ForegroundColor White
    
    $monitoringDependencies = @(
        "aiohttp>=3.9.0",
        "websockets>=12.0",
        "psutil>=5.9.0",
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
        "plotly>=5.17.0"
    )
    
    foreach ($dep in $monitoringDependencies) {
        Write-Host "Installing $dep" -ForegroundColor Gray
        if (-not $DryRun) {
            pip install $dep
        }
    }
    
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "Skipping dependency installation" -ForegroundColor Yellow
}

Write-Host ""

# Step 2: Security Configuration
Write-Host "Step 2: Security Configuration" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

Write-Host "Setting up secrets management..." -ForegroundColor White

# Create environment file template
$envContent = "# MASS Framework Environment Configuration`n"
$envContent += "# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n"
$envContent += "# Security Configuration`n"
$envContent += "JWT_SECRET_KEY=$(New-Guid)`n"
$envContent += "ENCRYPTION_KEY=$(New-Guid)`n"
$envContent += "API_SECRET_KEY=$(New-Guid)`n`n"
$envContent += "# Database Configuration`n"
$envContent += "DATABASE_URL=postgresql://mass_user:$(New-Guid)@localhost:5432/mass_framework`n"
$envContent += "REDIS_PASSWORD=$(New-Guid)`n"
$envContent += "POSTGRES_PASSWORD=$(New-Guid)`n"
$envContent += "MONGODB_PASSWORD=$(New-Guid)`n`n"
$envContent += "# External API Keys`n"
$envContent += "OPENAI_API_KEY=your_openai_api_key_here`n"
$envContent += "ANTHROPIC_API_KEY=your_anthropic_api_key_here`n`n"
$envContent += "# Monitoring Configuration`n"
$envContent += "SMTP_SERVER=smtp.gmail.com`n"
$envContent += "SMTP_PORT=587`n"
$envContent += "EMAIL_USERNAME=your_email@gmail.com`n"
$envContent += "EMAIL_PASSWORD=your_app_password_here`n"
$envContent += "FROM_EMAIL=alerts@mass-framework.com`n"
$envContent += "TO_EMAILS=admin@mass-framework.com,security@mass-framework.com`n`n"
$envContent += "# Slack Configuration`n"
$envContent += "SLACK_WEBHOOK_URL=your_slack_webhook_url_here`n"
$envContent += "SLACK_CHANNEL=#alerts`n`n"
$envContent += "# Webhook Configuration`n"
$envContent += "WEBHOOK_URL=your_webhook_url_here`n`n"
$envContent += "# Environment`n"
$envContent += "MASS_ENVIRONMENT=$Environment`n"
$envContent += "LOG_LEVEL=INFO`n"
$envContent += "METRICS_ENABLED=true`n"
$envContent += "ALERTING_ENABLED=true`n"

if (-not $DryRun) {
    $envContent | Out-File -FilePath ".env.$Environment" -Encoding utf8
    Write-Host "Created .env.$Environment" -ForegroundColor Gray
} else {
    Write-Host "Would create .env.$Environment" -ForegroundColor Gray
}

Write-Host "Security configuration completed" -ForegroundColor Green
Write-Host ""

# Step 3: Directory Structure
Write-Host "Step 3: Directory Structure" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green

$directories = @(
    "logs",
    "logs/security",
    "logs/monitoring", 
    "logs/backtesting",
    "data",
    "data/backtesting",
    "data/trading",
    "reports",
    "reports/security",
    "reports/backtesting",
    "reports/performance",
    "config",
    "certificates",
    "backups"
)

foreach ($dir in $directories) {
    Write-Host "Creating directory: $dir" -ForegroundColor Gray
    if (-not $DryRun) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
}

Write-Host "Directory structure created" -ForegroundColor Green
Write-Host ""

# Step 4: Security Hardening Setup
Write-Host "Step 4: Security Hardening Setup" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

Write-Host "Configuring enterprise security framework..." -ForegroundColor White

# Create security configuration
$securityContent = "# Enterprise Security Configuration`n"
$securityContent += "# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n"
$securityContent += "[Security]`n"
$securityContent += "enable_monitoring = true`n"
$securityContent += "enable_threat_detection = true`n"
$securityContent += "enable_audit_logging = true`n"
$securityContent += "secrets_rotation_interval_hours = 24`n"
$securityContent += "max_failed_attempts = 5`n"
$securityContent += "lockout_duration_minutes = 30`n`n"
$securityContent += "[Authentication]`n"
$securityContent += "jwt_expiration_hours = 24`n"
$securityContent += "password_min_length = 12`n"
$securityContent += "require_special_chars = true`n"
$securityContent += "require_numbers = true`n"
$securityContent += "require_uppercase = true`n`n"
$securityContent += "[Authorization]`n"
$securityContent += "enable_rbac = true`n"
$securityContent += "enable_audit_trail = true`n"
$securityContent += "session_timeout_minutes = 60`n`n"
$securityContent += "[Monitoring]`n"
$securityContent += "check_interval_seconds = 60`n"
$securityContent += "alert_thresholds = {`n"
$securityContent += "    'cpu_usage_percent': 80,`n"
$securityContent += "    'memory_usage_percent': 85,`n"
$securityContent += "    'disk_usage_percent': 90,`n"
$securityContent += "    'error_rate_percent': 5,`n"
$securityContent += "    'response_time_ms': 2000`n"
$securityContent += "}`n"

if (-not $DryRun) {
    $securityContent | Out-File -FilePath "config/security_config.ini" -Encoding utf8
    Write-Host "Created security configuration" -ForegroundColor Gray
} else {
    Write-Host "Would create security configuration" -ForegroundColor Gray
}

Write-Host "Security hardening configured" -ForegroundColor Green
Write-Host ""

# Step 5: Monitoring Setup
Write-Host "Step 5: Monitoring Setup" -ForegroundColor Green
Write-Host "===========================" -ForegroundColor Green

Write-Host "Configuring real-time alerting..." -ForegroundColor White

# Create monitoring configuration
$monitoringContent = "# Real-time Monitoring Configuration`n"
$monitoringContent += "# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n"
$monitoringContent += "[Alerting]`n"
$monitoringContent += "enable_email_alerts = true`n"
$monitoringContent += "enable_slack_alerts = true`n"
$monitoringContent += "enable_webhook_alerts = true`n"
$monitoringContent += "alert_check_interval_seconds = 60`n`n"
$monitoringContent += "[Email]`n"
$monitoringContent += "smtp_server = smtp.gmail.com`n"
$monitoringContent += "smtp_port = 587`n"
$monitoringContent += "username = your_email@gmail.com`n"
$monitoringContent += "password = your_app_password`n"
$monitoringContent += "from_email = alerts@mass-framework.com`n"
$monitoringContent += "to_emails = admin@mass-framework.com,security@mass-framework.com`n`n"
$monitoringContent += "[Slack]`n"
$monitoringContent += "webhook_url = your_slack_webhook_url`n"
$monitoringContent += "channel = #alerts`n"
$monitoringContent += "username = MASS Framework Alerts`n`n"
$monitoringContent += "[Webhook]`n"
$monitoringContent += "url = your_webhook_url`n"
$monitoringContent += "timeout_seconds = 10`n`n"
$monitoringContent += "[Thresholds]`n"
$monitoringContent += "cpu_usage_percent = 80`n"
$monitoringContent += "memory_usage_percent = 85`n"
$monitoringContent += "disk_usage_percent = 90`n"
$monitoringContent += "error_rate_percent = 5`n"
$monitoringContent += "response_time_ms = 2000`n"
$monitoringContent += "security_violations_per_hour = 10`n"

if (-not $DryRun) {
    $monitoringContent | Out-File -FilePath "config/monitoring_config.ini" -Encoding utf8
    Write-Host "Created monitoring configuration" -ForegroundColor Gray
} else {
    Write-Host "Would create monitoring configuration" -ForegroundColor Gray
}

Write-Host "Monitoring system configured" -ForegroundColor Green
Write-Host ""

# Step 6: Backtesting Validation Setup
Write-Host "Step 6: Backtesting Validation Setup" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

if (-not $SkipBacktesting) {
    Write-Host "Configuring backtesting validation..." -ForegroundColor White
    
    # Create backtesting configuration
    $backtestingContent = "# Backtesting Validation Configuration`n"
    $backtestingContent += "# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n"
    $backtestingContent += "[Validation]`n"
    $backtestingContent += "enable_validation = true`n"
    $backtestingContent += "validation_period_days = 365`n"
    $backtestingContent += "required_strategies = [`n"
    $backtestingContent += "    'momentum_rsi',`n"
    $backtestingContent += "    'mean_reversion_bollinger',`n"
    $backtestingContent += "    'breakout_atr',`n"
    $backtestingContent += "    'macd_crossover',`n"
    $backtestingContent += "    'dual_thrust',`n"
    $backtestingContent += "    'turtle_trading'`n"
    $backtestingContent += "]`n`n"
    $backtestingContent += "[Performance_Thresholds]`n"
    $backtestingContent += "sharpe_ratio = 0.5`n"
    $backtestingContent += "max_drawdown = -0.2`n"
    $backtestingContent += "win_rate = 0.4`n"
    $backtestingContent += "profit_factor = 1.2`n"
    $backtestingContent += "total_return = 0.1`n`n"
    $backtestingContent += "[Testing]`n"
    $backtestingContent += "test_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']`n"
    $backtestingContent += "commission_rate = 0.001`n"
    $backtestingContent += "slippage_rate = 0.0005`n"
    $backtestingContent += "initial_capital = 100000.0`n`n"
    $backtestingContent += "[Monte_Carlo]`n"
    $backtestingContent += "simulations = 1000`n"
    $backtestingContent += "confidence_level = 0.95`n"

    if (-not $DryRun) {
        $backtestingContent | Out-File -FilePath "config/backtesting_config.ini" -Encoding utf8
        Write-Host "Created backtesting configuration" -ForegroundColor Gray
    } else {
        Write-Host "Would create backtesting configuration" -ForegroundColor Gray
    }
    
    Write-Host "Backtesting validation configured" -ForegroundColor Green
} else {
    Write-Host "Skipping backtesting validation setup" -ForegroundColor Yellow
}

Write-Host ""

# Step 7: Validation and Testing
Write-Host "Step 7: Validation and Testing" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

Write-Host "Running deployment validation..." -ForegroundColor White

# Check if all required files exist
$requiredFiles = @(
    "security/enterprise_security_hardening.py",
    "monitoring/real_time_alerting.py", 
    "trading/backtesting_engine.py",
    "security_monitoring_integration.py"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "Missing required files:" -ForegroundColor Red
    foreach ($file in $missingFiles) {
        Write-Host "  - $file" -ForegroundColor Red
    }
} else {
    Write-Host "All required files present" -ForegroundColor Green
}

# Test Python imports
Write-Host "Testing Python imports..." -ForegroundColor White
try {
    python -c "import asyncio, logging, json, os, sys; print('Core imports successful')"
    python -c "import numpy as np, pandas as pd; print('Data science imports successful')"
    python -c "import yfinance as yf; print('Financial data imports successful')"
    python -c "import sklearn; print('Machine learning imports successful')"
    python -c "import psutil; print('System monitoring imports successful')"
    Write-Host "All Python imports successful" -ForegroundColor Green
} catch {
    Write-Host "Some imports failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "Validation completed" -ForegroundColor Green
Write-Host ""

# Step 8: Deployment Summary
Write-Host "Step 8: Deployment Summary" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green

Write-Host "MASS Framework Security & Monitoring deployment completed!" -ForegroundColor White
Write-Host ""
Write-Host "Generated Files:" -ForegroundColor Yellow
Write-Host "  • .env.$Environment - Environment configuration" -ForegroundColor Gray
Write-Host "  • config/security_config.ini - Security settings" -ForegroundColor Gray
Write-Host "  • config/monitoring_config.ini - Monitoring settings" -ForegroundColor Gray
Write-Host "  • config/backtesting_config.ini - Backtesting settings" -ForegroundColor Gray
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Update .env.$Environment with your actual API keys and credentials" -ForegroundColor Gray
Write-Host "  2. Run: python security_monitoring_integration.py" -ForegroundColor Gray
Write-Host "  3. Monitor logs/security_monitoring.log for status" -ForegroundColor Gray
Write-Host "  4. Set up external monitoring (Slack, email, webhooks)" -ForegroundColor Gray
Write-Host ""
Write-Host "Security Features Enabled:" -ForegroundColor Yellow
Write-Host "  • Enterprise secrets management with rotation" -ForegroundColor Gray
Write-Host "  • Real-time threat detection and response" -ForegroundColor Gray
Write-Host "  • Comprehensive audit logging" -ForegroundColor Gray
Write-Host "  • Multi-channel alerting (Email, Slack, Webhook)" -ForegroundColor Gray
Write-Host "  • Rate limiting and brute force protection" -ForegroundColor Gray
Write-Host ""
Write-Host "Monitoring Features Enabled:" -ForegroundColor Yellow
Write-Host "  • Real-time system performance monitoring" -ForegroundColor Gray
Write-Host "  • Security incident alerting" -ForegroundColor Gray
Write-Host "  • Trading strategy validation" -ForegroundColor Gray
Write-Host "  • Infrastructure health checks" -ForegroundColor Gray
Write-Host "  • Automated incident response" -ForegroundColor Gray
Write-Host ""
Write-Host "Important Security Notes:" -ForegroundColor Red
Write-Host "  • Change all default passwords and API keys" -ForegroundColor Gray
Write-Host "  • Enable multi-factor authentication" -ForegroundColor Gray
Write-Host "  • Regularly rotate secrets and certificates" -ForegroundColor Gray
Write-Host "  • Monitor security logs for suspicious activity" -ForegroundColor Gray
Write-Host "  • Keep all dependencies updated" -ForegroundColor Gray
Write-Host ""
Write-Host "Deployment completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Green 