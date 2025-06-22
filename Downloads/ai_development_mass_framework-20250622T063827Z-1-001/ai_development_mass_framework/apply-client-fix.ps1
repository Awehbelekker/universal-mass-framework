#!/usr/bin/env pwsh
# Apply client-side error handling fix to running MASS Framework

Write-Host "🔧 MASS Framework - Client-Side Error Fix Application" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Get-Date
Write-Host ""

# Check if SSH key exists
$sshKeyPath = "~/.ssh/mass-framework-key.pem"
if (-not (Test-Path $sshKeyPath)) {
    Write-Host "❌ SSH key not found at $sshKeyPath" -ForegroundColor Red
    exit 1
}

# Set proper permissions on SSH key (for Windows)
try {
    icacls $sshKeyPath /inheritance:r /grant:r "$env:USERNAME`:R" 2>$null | Out-Null
} catch {
    Write-Host "⚠️  Could not set SSH key permissions, continuing..." -ForegroundColor Yellow
}

$instanceIP = "54.167.234.7"
Write-Host "🌐 Connecting to MASS Framework server at $instanceIP..." -ForegroundColor Green

# Copy the fix script to the server
Write-Host "📤 Uploading client-side error fix script..." -ForegroundColor Yellow
scp -i $sshKeyPath -o StrictHostKeyChecking=no "ai_development_mass_framework/client-error-fix.sh" "ec2-user@${instanceIP}:/tmp/client-error-fix.sh"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Script uploaded successfully" -ForegroundColor Green
    
    # Execute the fix script
    Write-Host "🚀 Executing client-side error fix..." -ForegroundColor Yellow
    ssh -i $sshKeyPath -o StrictHostKeyChecking=no "ec2-user@$instanceIP" "chmod +x /tmp/client-error-fix.sh && /tmp/client-error-fix.sh"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 CLIENT-SIDE ERROR FIX APPLIED SUCCESSFULLY!" -ForegroundColor Green
        Write-Host "🔗 Test the improvements at: http://$instanceIP:8000" -ForegroundColor Cyan
        Write-Host "🔧 Browser console errors should now be handled gracefully" -ForegroundColor Green
        Write-Host ""
        
        # Test the health endpoint
        Write-Host "🧪 Testing improved health endpoint..." -ForegroundColor Yellow
        try {
            $response = Invoke-RestMethod -Uri "http://$instanceIP:8000/health" -Method GET -TimeoutSec 10
            Write-Host "✅ Health check successful - Version: $($response.version)" -ForegroundColor Green
            Write-Host "🔧 Client error handling: $($response.client_error_handling)" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  Could not test health endpoint, but fix should be applied" -ForegroundColor Yellow
        }
        
        Write-Host ""
        Write-Host "📋 What was improved:" -ForegroundColor Cyan
        Write-Host "  ✅ Global error handlers for uncaught exceptions" -ForegroundColor White
        Write-Host "  ✅ Promise rejection handling" -ForegroundColor White
        Write-Host "  ✅ Enhanced status indicator with pulse animation" -ForegroundColor White
        Write-Host "  ✅ Better CORS support with OPTIONS handling" -ForegroundColor White
        Write-Host "  ✅ Version bumped to 1.0.1" -ForegroundColor White
        Write-Host "  ✅ Console error suppression for external resources" -ForegroundColor White
        
    } else {
        Write-Host "❌ Failed to execute client-side error fix" -ForegroundColor Red
        Write-Host "💡 The server may still be running with the previous version" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Failed to upload script to server" -ForegroundColor Red
    Write-Host "💡 Please check your internet connection and SSH key permissions" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌟 CLIENT-SIDE ERROR FIX DEPLOYMENT COMPLETED!" -ForegroundColor Magenta
