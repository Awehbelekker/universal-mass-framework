# GitHub Secrets Setup Script for MASS Framework
# This script helps set up all required GitHub secrets

param(
    [string]$RepoOwner = "your-username",
    [string]$RepoName = "ai_development_mass_framework",
    [string]$GcpProjectId = "",
    [string]$GcpServiceAccountKeyPath = "",
    [string]$DatabaseUrl = "",
    [string]$RedisUrl = "",
    [string]$FirebaseProjectId = "",
    [switch]$DryRun
)

Write-Host "=== MASS Framework GitHub Secrets Setup ===" -ForegroundColor Green
Write-Host ""

# Check if GitHub CLI is installed
try {
    $ghVersion = gh --version
    Write-Host "✓ GitHub CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ GitHub CLI is not installed. Please install it from: https://cli.github.com/" -ForegroundColor Red
    exit 1
}

# Check if user is authenticated
try {
    $authStatus = gh auth status
    Write-Host "✓ GitHub authentication verified" -ForegroundColor Green
} catch {
    Write-Host "✗ Please authenticate with GitHub CLI first: gh auth login" -ForegroundColor Red
    exit 1
}

# Function to generate a secure secret key
function Generate-SecretKey {
    $bytes = New-Object Byte[] 32
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($bytes)
    return [Convert]::ToBase64String($bytes)
}

# Function to set a secret
function Set-GitHubSecret {
    param(
        [string]$SecretName,
        [string]$SecretValue,
        [string]$Description = ""
    )
    
    if ($DryRun) {
        Write-Host "[DRY RUN] Would set secret: $SecretName" -ForegroundColor Yellow
        return
    }
    
    try {
        gh secret set $SecretName --body $SecretValue --repo "$RepoOwner/$RepoName"
        Write-Host "✓ Set secret: $SecretName" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to set secret: $SecretName" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}

# Function to prompt for input
function Read-SecureInput {
    param([string]$Prompt)
    
    Write-Host $Prompt -ForegroundColor Cyan
    $input = Read-Host
    return $input
}

Write-Host "Setting up GitHub secrets for repository: $RepoOwner/$RepoName" -ForegroundColor Yellow
Write-Host ""

# 1. GCP Project ID
if ([string]::IsNullOrEmpty($GcpProjectId)) {
    $GcpProjectId = Read-SecureInput "Enter your Google Cloud Project ID:"
}
Set-GitHubSecret -SecretName "GCP_PROJECT_ID" -SecretValue $GcpProjectId

# 2. GCP Service Account Key
if ([string]::IsNullOrEmpty($GcpServiceAccountKeyPath)) {
    $GcpServiceAccountKeyPath = Read-SecureInput "Enter path to your GCP service account JSON key file:"
}

if (Test-Path $GcpServiceAccountKeyPath) {
    $serviceAccountKey = Get-Content $GcpServiceAccountKeyPath -Raw
    Set-GitHubSecret -SecretName "GCP_SA_KEY" -SecretValue $serviceAccountKey
} else {
    Write-Host "✗ Service account key file not found: $GcpServiceAccountKeyPath" -ForegroundColor Red
    Write-Host "Please create a service account key in Google Cloud Console and provide the path." -ForegroundColor Yellow
}

# 3. Database URL
if ([string]::IsNullOrEmpty($DatabaseUrl)) {
    $DatabaseUrl = Read-SecureInput "Enter your PostgreSQL database URL (format: postgresql://user:pass@host:5432/db):"
}
Set-GitHubSecret -SecretName "DATABASE_URL" -SecretValue $DatabaseUrl

# 4. Redis URL
if ([string]::IsNullOrEmpty($RedisUrl)) {
    $RedisUrl = Read-SecureInput "Enter your Redis URL (format: redis://:pass@host:6379):"
}
Set-GitHubSecret -SecretName "REDIS_URL" -SecretValue $RedisUrl

# 5. Secret Key
$secretKey = Generate-SecretKey
Set-GitHubSecret -SecretName "SECRET_KEY" -SecretValue $secretKey

# 6. Firebase Project ID
if ([string]::IsNullOrEmpty($FirebaseProjectId)) {
    $FirebaseProjectId = Read-SecureInput "Enter your Firebase Project ID:"
}
Set-GitHubSecret -SecretName "FIREBASE_PROJECT_ID" -SecretValue $FirebaseProjectId

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""

# Verify secrets
Write-Host "Verifying secrets..." -ForegroundColor Yellow
try {
    $secrets = gh secret list --repo "$RepoOwner/$RepoName" --json name
    $secretNames = $secrets | ConvertFrom-Json | ForEach-Object { $_.name }
    
    $requiredSecrets = @("GCP_SA_KEY", "GCP_PROJECT_ID", "DATABASE_URL", "REDIS_URL", "SECRET_KEY", "FIREBASE_PROJECT_ID")
    
    foreach ($secret in $requiredSecrets) {
        if ($secretNames -contains $secret) {
            Write-Host "✓ $secret" -ForegroundColor Green
        } else {
            Write-Host "✗ $secret (missing)" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "✗ Failed to verify secrets" -ForegroundColor Red
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Test the workflow with a small change" -ForegroundColor White
Write-Host "2. Monitor the first deployment" -ForegroundColor White
Write-Host "3. Set up environment protection rules" -ForegroundColor White
Write-Host "4. Configure monitoring and alerting" -ForegroundColor White 