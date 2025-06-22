Write-Host "🔧 MASS Framework - Client-Side Error Fix Application" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Get-Date
Write-Host ""

$instanceIP = "54.167.234.7"
$sshKeyPath = "$env:USERPROFILE\.ssh\mass-framework-key.pem"

Write-Host "🌐 Connecting to MASS Framework server at $instanceIP..." -ForegroundColor Green

# Copy the fix script to the server
Write-Host "📤 Uploading client-side error fix script..." -ForegroundColor Yellow
$scpCommand = "scp -i `"$sshKeyPath`" -o StrictHostKeyChecking=no `"ai_development_mass_framework/client-error-fix.sh`" `"ec2-user@${instanceIP}:/tmp/client-error-fix.sh`""
Invoke-Expression $scpCommand

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Script uploaded successfully" -ForegroundColor Green
    
    # Execute the fix script
    Write-Host "🚀 Executing client-side error fix..." -ForegroundColor Yellow
    $sshCommand = "ssh -i `"$sshKeyPath`" -o StrictHostKeyChecking=no `"ec2-user@$instanceIP`" `"chmod +x /tmp/client-error-fix.sh && /tmp/client-error-fix.sh`""
    Invoke-Expression $sshCommand
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 CLIENT-SIDE ERROR FIX APPLIED SUCCESSFULLY!" -ForegroundColor Green
        Write-Host "🔗 Test the improvements at: http://$instanceIP:8000" -ForegroundColor Cyan
        Write-Host "🔧 Browser console errors should now be handled gracefully" -ForegroundColor Green
        
        # Test the health endpoint
        Write-Host ""
        Write-Host "🧪 Testing improved health endpoint..." -ForegroundColor Yellow
        try {
            $response = Invoke-RestMethod -Uri "http://$instanceIP:8000/health" -Method GET -TimeoutSec 10
            Write-Host "✅ Health check successful - Version: $($response.version)" -ForegroundColor Green
            if ($response.client_error_handling) {
                Write-Host "🔧 Client error handling: $($response.client_error_handling)" -ForegroundColor Green
            }
        } catch {
            Write-Host "⚠️  Could not test health endpoint from here, but fix should be applied" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Failed to execute client-side error fix" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Failed to upload script to server" -ForegroundColor Red
}

Write-Host ""
Write-Host "🌟 CLIENT-FIX DEPLOYMENT COMPLETED!" -ForegroundColor Magenta
