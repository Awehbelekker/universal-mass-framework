Write-Host "AWS Configuration for MASS Framework Beta Launch" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

Write-Host "You have AWS Console credentials, but need CLI access keys." -ForegroundColor Yellow
Write-Host ""
Write-Host "Your Console Login:" -ForegroundColor Cyan
Write-Host "URL: https://886819404599.signin.aws.amazon.com/console" -ForegroundColor White
Write-Host "Username: MasterAdn" -ForegroundColor White
Write-Host "Password: 74iyK9J+" -ForegroundColor White
Write-Host ""

Write-Host "To get CLI access keys:" -ForegroundColor Cyan
Write-Host "1. Log into AWS Console (URL above)" -ForegroundColor White
Write-Host "2. Go to IAM > Users > MasterAdn" -ForegroundColor White
Write-Host "3. Click Security credentials tab" -ForegroundColor White
Write-Host "4. Click Create access key" -ForegroundColor White
Write-Host "5. Choose CLI option" -ForegroundColor White
Write-Host "6. Copy the Access Key ID and Secret" -ForegroundColor White
Write-Host ""

Write-Host "Then run: aws configure" -ForegroundColor Green
Write-Host "And enter:" -ForegroundColor Yellow
Write-Host "- Your Access Key ID" -ForegroundColor White
Write-Host "- Your Secret Access Key" -ForegroundColor White
Write-Host "- Region: us-east-1" -ForegroundColor White
Write-Host "- Output: json" -ForegroundColor White
Write-Host ""

$open = Read-Host "Open AWS Console now? (y/n)"
if ($open -eq 'y') {
    Start-Process "https://console.aws.amazon.com/iam/home#/users"
    Write-Host "Opening AWS Console..." -ForegroundColor Green
}

Write-Host ""
Write-Host "After configuring AWS CLI, run:" -ForegroundColor Green
Write-Host ".\one-click-deploy.ps1" -ForegroundColor Yellow
