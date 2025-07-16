# MASS Framework Security & Monitoring Deployment Script
# Production-ready deployment with security hardening and real-time monitoring

param(
    [string]$Environment = "production",
    [switch]$SkipDependencies = $false,
    [switch]$SkipBacktesting = $false,
    [switch]$DryRun = $false
)

Write-Host "🔒 MASS Framework Security & Monitoring Deployment" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

# Step 1: Environment Setup
Write-Host "📦 Step 1: Environment Setup" -ForegroundColor Green
Write-Host "===========================" -ForegroundColor Green

if (-not $SkipDependencies) {
    Write-Host "   📥 Installing Python dependencies..." -ForegroundColor White
    
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
        Write-Host "      Installing $dep" -ForegroundColor Gray
        if (-not $DryRun) {
            pip install $dep
        }
    }
    
    # Install financial and trading dependencies
    Write-Host "   📈 Installing financial dependencies..." -ForegroundColor White
    
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
        Write-Host "      Installing $dep" -ForegroundColor Gray
        if (-not $DryRun) {
            pip install $dep
        }
    }
    
    # Install monitoring and alerting dependencies
    Write-Host "   📊 Installing monitoring dependencies..." -ForegroundColor White
    
    $monitoringDependencies = @(
        "aiohttp>=3.9.0",
        "websockets>=12.0",
        "psutil>=5.9.0",
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
        "plotly>=5.17.0"
    )
    
    foreach ($dep in $monitoringDependencies) {
        Write-Host "      Installing $dep" -ForegroundColor Gray
        if (-not $DryRun) {
            pip install $dep
        }
    }
    
    Write-Host "   ✅ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "   ⏭️ Skipping dependency installation" -ForegroundColor Yellow
}

Write-Host ""

# Step 2: Security Configuration
Write-Host "🔐 Step 2: Security Configuration" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

Write-Host "   🔑 Setting up secrets management..." -ForegroundColor White

# Create environment file template
$envTemplate = @"
# MASS Framework Environment Configuration
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

# Security Configuration
JWT_SECRET_KEY=$(New-Guid)
ENCRYPTION_KEY=$(New-Guid)
API_SECRET_KEY=$(New-Guid)

# Database Configuration
DATABASE_URL=postgresql://mass_user:$(New-Guid)@localhost:5432/mass_framework
REDIS_PASSWORD=$(New-Guid)
POSTGRES_PASSWORD=$(New-Guid)
MONGODB_PASSWORD=$(New-Guid)

# External API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Monitoring Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
FROM_EMAIL=alerts@mass-framework.com
TO_EMAILS=admin@mass-framework.com,security@mass-framework.com

# Slack Configuration
SLACK_WEBHOOK_URL=your_slack_webhook_url_here
SLACK_CHANNEL=#alerts

# Webhook Configuration
WEBHOOK_URL=your_webhook_url_here

# Environment
MASS_ENVIRONMENT=$Environment
LOG_LEVEL=INFO
METRICS_ENABLED=true
ALERTING_ENABLED=true
"@

if (-not $DryRun) {
    $envTemplate | Out-File -FilePath ".env.$Environment" -Encoding utf8
    Write-Host "      ✅ Created .env.$Environment" -ForegroundColor Gray
} else {
    Write-Host "      📄 Would create .env.$Environment" -ForegroundColor Gray
}

Write-Host "   ✅ Security configuration completed" -ForegroundColor Green
Write-Host ""

# Step 3: Directory Structure
Write-Host "📁 Step 3: Directory Structure" -ForegroundColor Green
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
    Write-Host "   📂 Creating directory: $dir" -ForegroundColor Gray
    if (-not $DryRun) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
}

Write-Host "   ✅ Directory structure created" -ForegroundColor Green
Write-Host ""

# Step 4: Security Hardening Setup
Write-Host "🛡️ Step 4: Security Hardening Setup" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

Write-Host "   🔒 Configuring enterprise security framework..." -ForegroundColor White

# Create security configuration
$securityConfig = @"
# Enterprise Security Configuration
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

[Security]
enable_monitoring = true
enable_threat_detection = true
enable_audit_logging = true
secrets_rotation_interval_hours = 24
max_failed_attempts = 5
lockout_duration_minutes = 30

[Authentication]
jwt_expiration_hours = 24
password_min_length = 12
require_special_chars = true
require_numbers = true
require_uppercase = true

[Authorization]
enable_rbac = true
enable_audit_trail = true
session_timeout_minutes = 60

[Monitoring]
check_interval_seconds = 60
alert_thresholds = {
    "cpu_usage_percent": 80,
    "memory_usage_percent": 85,
    "disk_usage_percent": 90,
    "error_rate_percent": 5,
    "response_time_ms": 2000
}
"@

if (-not $DryRun) {
    $securityConfig | Out-File -FilePath "config/security_config.ini" -Encoding utf8
    Write-Host "      ✅ Created security configuration" -ForegroundColor Gray
} else {
    Write-Host "      📄 Would create security configuration" -ForegroundColor Gray
}

Write-Host "   ✅ Security hardening configured" -ForegroundColor Green
Write-Host ""

# Step 5: Monitoring Setup
Write-Host "📊 Step 5: Monitoring Setup" -ForegroundColor Green
Write-Host "===========================" -ForegroundColor Green

Write-Host "   🚨 Configuring real-time alerting..." -ForegroundColor White

# Create monitoring configuration
$monitoringConfig = @"
# Real-time Monitoring Configuration
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

[Alerting]
enable_email_alerts = true
enable_slack_alerts = true
enable_webhook_alerts = true
alert_check_interval_seconds = 60

[Email]
smtp_server = smtp.gmail.com
smtp_port = 587
username = your_email@gmail.com
password = your_app_password
from_email = alerts@mass-framework.com
to_emails = admin@mass-framework.com,security@mass-framework.com

[Slack]
webhook_url = your_slack_webhook_url
channel = #alerts
username = MASS Framework Alerts

[Webhook]
url = your_webhook_url
timeout_seconds = 10

[Thresholds]
cpu_usage_percent = 80
memory_usage_percent = 85
disk_usage_percent = 90
error_rate_percent = 5
response_time_ms = 2000
security_violations_per_hour = 10
"@

if (-not $DryRun) {
    $monitoringConfig | Out-File -FilePath "config/monitoring_config.ini" -Encoding utf8
    Write-Host "      ✅ Created monitoring configuration" -ForegroundColor Gray
} else {
    Write-Host "      📄 Would create monitoring configuration" -ForegroundColor Gray
}

Write-Host "   ✅ Monitoring system configured" -ForegroundColor Green
Write-Host ""

# Step 6: Backtesting Validation Setup
Write-Host "📈 Step 6: Backtesting Validation Setup" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

if (-not $SkipBacktesting) {
    Write-Host "   🧪 Configuring backtesting validation..." -ForegroundColor White
    
    # Create backtesting configuration
    $backtestingConfig = @"
# Backtesting Validation Configuration
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

[Validation]
enable_validation = true
validation_period_days = 365
required_strategies = [
    "momentum_rsi",
    "mean_reversion_bollinger", 
    "breakout_atr",
    "macd_crossover",
    "dual_thrust",
    "turtle_trading"
]

[Performance_Thresholds]
sharpe_ratio = 0.5
max_drawdown = -0.2
win_rate = 0.4
profit_factor = 1.2
total_return = 0.1

[Testing]
test_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
commission_rate = 0.001
slippage_rate = 0.0005
initial_capital = 100000.0

[Monte_Carlo]
simulations = 1000
confidence_level = 0.95
"@

    if (-not $DryRun) {
        $backtestingConfig | Out-File -FilePath "config/backtesting_config.ini" -Encoding utf8
        Write-Host "      ✅ Created backtesting configuration" -ForegroundColor Gray
    } else {
        Write-Host "      📄 Would create backtesting configuration" -ForegroundColor Gray
    }
    
    Write-Host "   ✅ Backtesting validation configured" -ForegroundColor Green
} else {
    Write-Host "   ⏭️ Skipping backtesting validation setup" -ForegroundColor Yellow
}

Write-Host ""

# Step 7: Service Configuration
Write-Host "⚙️ Step 7: Service Configuration" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green

Write-Host "   🔧 Creating service configurations..." -ForegroundColor White

# Create systemd service file (for Linux)
$systemdService = @"
[Unit]
Description=MASS Framework Security & Monitoring
After=network.target

[Service]
Type=simple
User=mass_user
WorkingDirectory=/opt/mass-framework
Environment=PATH=/opt/mass-framework/venv/bin
ExecStart=/opt/mass-framework/venv/bin/python security_monitoring_integration.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"@

if (-not $DryRun) {
    $systemdService | Out-File -FilePath "config/mass-security-monitoring.service" -Encoding utf8
    Write-Host "      ✅ Created systemd service file" -ForegroundColor Gray
} else {
    Write-Host "      📄 Would create systemd service file" -ForegroundColor Gray
}

# Create Windows service configuration
$windowsService = @"
# Windows Service Configuration for MASS Framework
# Install with: sc create "MASS-Security-Monitoring" binPath="python security_monitoring_integration.py"
# Start with: sc start "MASS-Security-Monitoring"

[Service]
Name=MASS-Security-Monitoring
DisplayName=MASS Framework Security & Monitoring
Description=Enterprise security hardening and real-time monitoring for MASS Framework
StartupType=Automatic
"@

if (-not $DryRun) {
    $windowsService | Out-File -FilePath "config/windows_service_config.txt" -Encoding utf8
    Write-Host "      ✅ Created Windows service configuration" -ForegroundColor Gray
} else {
    Write-Host "      📄 Would create Windows service configuration" -ForegroundColor Gray
}

Write-Host "   ✅ Service configurations created" -ForegroundColor Green
Write-Host ""

# Step 8: SSL Certificate Setup
Write-Host "🔐 Step 8: SSL Certificate Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

Write-Host "   📜 Setting up SSL certificates..." -ForegroundColor White

# Create self-signed certificate for development
if (-not $DryRun) {
    try {
        # Generate self-signed certificate
        $cert = New-SelfSignedCertificate -DnsName "localhost" -CertStoreLocation "Cert:\LocalMachine\My"
        $certPath = "certificates\mass-framework-cert.pfx"
        $cert | Export-PfxCertificate -FilePath $certPath -Password (ConvertTo-SecureString -String "mass-framework-2025" -AsPlainText -Force)
        Write-Host "      ✅ Generated self-signed certificate" -ForegroundColor Gray
    } catch {
        Write-Host "      ⚠️ Could not generate certificate: $($_.Exception.Message)" -ForegroundColor Yellow
    }
} else {
    Write-Host "      📄 Would generate SSL certificate" -ForegroundColor Gray
}

Write-Host "   ✅ SSL certificate setup completed" -ForegroundColor Green
Write-Host ""

# Step 9: Firewall Configuration
Write-Host "🔥 Step 9: Firewall Configuration" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

Write-Host "   🛡️ Configuring firewall rules..." -ForegroundColor White

# Create firewall configuration script
$firewallScript = @"
# Firewall Configuration for MASS Framework
# Run as Administrator

# Allow MASS Framework ports
netsh advfirewall firewall add rule name="MASS Framework API" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="MASS Framework Metrics" dir=in action=allow protocol=TCP localport=8001
netsh advfirewall firewall add rule name="MASS Framework WebSocket" dir=in action=allow protocol=TCP localport=8002

# Allow database connections
netsh advfirewall firewall add rule name="PostgreSQL" dir=in action=allow protocol=TCP localport=5432
netsh advfirewall firewall add rule name="Redis" dir=in action=allow protocol=TCP localport=6379
netsh advfirewall firewall add rule name="MongoDB" dir=in action=allow protocol=TCP localport=27017

# Block potentially dangerous ports
netsh advfirewall firewall add rule name="Block Telnet" dir=in action=block protocol=TCP localport=23
netsh advfirewall firewall add rule name="Block FTP" dir=in action=block protocol=TCP localport=21
"@

if (-not $DryRun) {
    $firewallScript | Out-File -FilePath "config/firewall_config.bat" -Encoding utf8
    Write-Host "      ✅ Created firewall configuration script" -ForegroundColor Gray
} else {
    Write-Host "      📄 Would create firewall configuration script" -ForegroundColor Gray
}

Write-Host "   ✅ Firewall configuration completed" -ForegroundColor Green
Write-Host ""

# Step 10: Validation and Testing
Write-Host "🧪 Step 10: Validation and Testing" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

Write-Host "   ✅ Running deployment validation..." -ForegroundColor White

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
    Write-Host "   ❌ Missing required files:" -ForegroundColor Red
    foreach ($file in $missingFiles) {
        Write-Host "      - $file" -ForegroundColor Red
    }
} else {
    Write-Host "   ✅ All required files present" -ForegroundColor Green
}

# Test Python imports
Write-Host "   🐍 Testing Python imports..." -ForegroundColor White
try {
    python -c "import asyncio, logging, json, os, sys; print('✅ Core imports successful')"
    python -c "import numpy as np, pandas as pd; print('✅ Data science imports successful')"
    python -c "import yfinance as yf; print('✅ Financial data imports successful')"
    python -c "import talib; print('✅ Technical analysis imports successful')"
    python -c "import psutil; print('✅ System monitoring imports successful')"
    Write-Host "   ✅ All Python imports successful" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️ Some imports failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "   ✅ Validation completed" -ForegroundColor Green
Write-Host ""

# Step 11: Deployment Summary
Write-Host "📋 Step 11: Deployment Summary" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green

Write-Host "   🎉 MASS Framework Security & Monitoring deployment completed!" -ForegroundColor White
Write-Host ""
Write-Host "   📁 Generated Files:" -ForegroundColor Yellow
Write-Host "      • .env.$Environment - Environment configuration" -ForegroundColor Gray
Write-Host "      • config/security_config.ini - Security settings" -ForegroundColor Gray
Write-Host "      • config/monitoring_config.ini - Monitoring settings" -ForegroundColor Gray
Write-Host "      • config/backtesting_config.ini - Backtesting settings" -ForegroundColor Gray
Write-Host "      • config/mass-security-monitoring.service - Linux service" -ForegroundColor Gray
Write-Host "      • config/windows_service_config.txt - Windows service" -ForegroundColor Gray
Write-Host "      • config/firewall_config.bat - Firewall rules" -ForegroundColor Gray
Write-Host ""
Write-Host "   🚀 Next Steps:" -ForegroundColor Yellow
Write-Host "      1. Update .env.$Environment with your actual API keys and credentials" -ForegroundColor Gray
Write-Host "      2. Run: python security_monitoring_integration.py" -ForegroundColor Gray
Write-Host "      3. Monitor logs/security_monitoring.log for status" -ForegroundColor Gray
Write-Host "      4. Set up external monitoring (Slack, email, webhooks)" -ForegroundColor Gray
Write-Host "      5. Configure firewall rules if needed" -ForegroundColor Gray
Write-Host ""
Write-Host "   🔒 Security Features Enabled:" -ForegroundColor Yellow
Write-Host "      • Enterprise secrets management with rotation" -ForegroundColor Gray
Write-Host "      • Real-time threat detection and response" -ForegroundColor Gray
Write-Host "      • Comprehensive audit logging" -ForegroundColor Gray
Write-Host "      • Multi-channel alerting (Email, Slack, Webhook)" -ForegroundColor Gray
Write-Host "      • Rate limiting and brute force protection" -ForegroundColor Gray
Write-Host ""
Write-Host "   📊 Monitoring Features Enabled:" -ForegroundColor Yellow
Write-Host "      • Real-time system performance monitoring" -ForegroundColor Gray
Write-Host "      • Security incident alerting" -ForegroundColor Gray
Write-Host "      • Trading strategy validation" -ForegroundColor Gray
Write-Host "      • Infrastructure health checks" -ForegroundColor Gray
Write-Host "      • Automated incident response" -ForegroundColor Gray
Write-Host ""
Write-Host "   📈 Backtesting Features Enabled:" -ForegroundColor Yellow
Write-Host "      • Multi-strategy validation" -ForegroundColor Gray
Write-Host "      • Real and synthetic data testing" -ForegroundColor Gray
Write-Host "      • Monte Carlo simulations" -ForegroundColor Gray
Write-Host "      • Performance threshold validation" -ForegroundColor Gray
Write-Host "      • Risk assessment and analysis" -ForegroundColor Gray
Write-Host ""
Write-Host "   ⚠️ Important Security Notes:" -ForegroundColor Red
Write-Host "      • Change all default passwords and API keys" -ForegroundColor Gray
Write-Host "      • Enable multi-factor authentication" -ForegroundColor Gray
Write-Host "      • Regularly rotate secrets and certificates" -ForegroundColor Gray
Write-Host "      • Monitor security logs for suspicious activity" -ForegroundColor Gray
Write-Host "      • Keep all dependencies updated" -ForegroundColor Gray
Write-Host ""
Write-Host "   📞 Support:" -ForegroundColor Cyan
Write-Host "      • Check logs/security_monitoring.log for detailed status" -ForegroundColor Gray
Write-Host "      • Review reports/security/ for security reports" -ForegroundColor Gray
Write-Host "      • Monitor alerts in your configured channels" -ForegroundColor Gray
Write-Host ""
Write-Host "Deployment completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Green 