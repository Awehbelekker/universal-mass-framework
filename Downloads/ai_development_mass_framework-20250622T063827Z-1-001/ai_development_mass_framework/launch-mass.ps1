# MASS Framework - Final Production Deployment

Write-Host ""
Write-Host "MASS Framework - Final Production Deployment" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "Deployment started at: $timestamp" -ForegroundColor Green
Write-Host ""

# Get instance details
Write-Host "Finding EC2 instance..." -ForegroundColor Yellow
$instanceData = aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query "Reservations[0].Instances[0]" --output json | ConvertFrom-Json

if (-not $instanceData) {
    Write-Host "No running instances found!" -ForegroundColor Red
    exit 1
}

$instanceId = $instanceData.InstanceId
$publicIp = $instanceData.PublicIpAddress

Write-Host "Found instance: $instanceId" -ForegroundColor Green
Write-Host "Public IP: $publicIp" -ForegroundColor Green
Write-Host ""

# Read the deployment script
$scriptPath = ".\final-mass-deploy.sh"
if (-not (Test-Path $scriptPath)) {
    Write-Host "Deployment script not found: $scriptPath" -ForegroundColor Red
    exit 1
}

$deployScript = Get-Content $scriptPath -Raw

Write-Host "Uploading and executing deployment script via AWS SSM..." -ForegroundColor Yellow

# Execute via SSM
try {
    $result = aws ssm send-command --instance-ids $instanceId --document-name "AWS-RunShellScript" --parameters "commands=`"$deployScript`"" --output json | ConvertFrom-Json
    
    if ($result) {
        $commandId = $result.Command.CommandId
        Write-Host "Command sent successfully: $commandId" -ForegroundColor Green
        
        Write-Host "Waiting for deployment to complete..." -ForegroundColor Yellow
        Start-Sleep 20
        
        # Get command output
        $output = aws ssm get-command-invocation --command-id $commandId --instance-id $instanceId --output json | ConvertFrom-Json
        
        Write-Host ""
        Write-Host "Deployment Status: $($output.Status)" -ForegroundColor $(if($output.Status -eq "Success"){"Green"}else{"Red"})
        
        if ($output.StandardOutputContent) {
            Write-Host ""
            Write-Host "Deployment Output:" -ForegroundColor Cyan
            Write-Host $output.StandardOutputContent -ForegroundColor White
        }
        
        if ($output.StandardErrorContent) {
            Write-Host ""
            Write-Host "Deployment Errors:" -ForegroundColor Red
            Write-Host $output.StandardErrorContent -ForegroundColor Red
        }
        
        if ($output.Status -eq "Success") {
            Write-Host ""
            Write-Host "MASS Framework Successfully Deployed!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Production URLs:" -ForegroundColor Cyan
            Write-Host "  Main Site: http://$publicIp:8000" -ForegroundColor White
            Write-Host "  Health Check: http://$publicIp:8000/health" -ForegroundColor White
            Write-Host "  API Endpoint: http://$publicIp:8000/api" -ForegroundColor White
            Write-Host ""
            
            # Test external connectivity
            Write-Host "Testing external connectivity..." -ForegroundColor Yellow
            try {
                $response = Invoke-WebRequest -Uri "http://$publicIp:8000/health" -Method GET -TimeoutSec 15 -UseBasicParsing
                Write-Host "External access successful!" -ForegroundColor Green
                Write-Host "  Status Code: $($response.StatusCode)" -ForegroundColor Green
                $preview = $response.Content.Substring(0, [Math]::Min(150, $response.Content.Length))
                Write-Host "  Response Preview: $preview..." -ForegroundColor Gray
                Write-Host ""
                Write-Host "MASS Framework is now LIVE and accessible to the public!" -ForegroundColor Green
                Write-Host "Share this URL with beta testers: http://$publicIp:8000" -ForegroundColor Cyan
                
            } catch {
                Write-Host "External access test failed: $($_.Exception.Message)" -ForegroundColor Yellow
                Write-Host "The server may be running but blocked by network configuration." -ForegroundColor Yellow
                Write-Host "Try accessing manually: http://$publicIp:8000" -ForegroundColor White
            }
            
        } else {
            Write-Host ""
            Write-Host "Deployment failed. Check the error output above." -ForegroundColor Red
        }
        
    } else {
        Write-Host "Failed to send SSM command" -ForegroundColor Red
    }
    
} catch {
    Write-Host "Error during deployment: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Test the URLs above in your web browser" -ForegroundColor White
Write-Host "2. If not accessible, check AWS Console - EC2 - Security Groups" -ForegroundColor White
Write-Host "3. Verify port 8000 is open to 0.0.0.0/0" -ForegroundColor White
Write-Host "4. For SSH access, use EC2 Instance Connect in AWS Console" -ForegroundColor White
Write-Host ""

$endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "Deployment completed at: $endTime" -ForegroundColor Green
Write-Host ""
