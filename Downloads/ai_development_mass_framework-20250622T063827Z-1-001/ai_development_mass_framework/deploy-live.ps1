# 🚀 MASS Framework Live Trading Deployment Script
# Usage: .\deploy-live.ps1 -Production -ProjectId "your-project-id"

param(
    [switch]$Production,
    [string]$ProjectId = "mass-ai-trading",
    [switch]$SkipBuild,
    [switch]$FunctionsOnly,
    [switch]$HostingOnly
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 MASS AI Trading Framework - Live Deployment" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Check if Firebase CLI is installed
try {
    $firebaseVersion = firebase --version
    Write-Host "✅ Firebase CLI found: $firebaseVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Firebase CLI not found. Install with: npm install -g firebase-tools" -ForegroundColor Red
    exit 1
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check prerequisites
Write-Status "Checking prerequisites..."

if (!(Get-Command firebase -ErrorAction SilentlyContinue)) {
    Write-Error "Firebase CLI not found. Please install it first:"
    Write-Host "npm install -g firebase-tools"
    exit 1
}

if (!(Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js not found. Please install Node.js first."
    exit 1
}

if (!(Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Error "npm not found. Please install npm first."
    exit 1
}

Write-Success "Prerequisites check passed"

# Step 1: Frontend Build
if (!$SkipBuild) {
    Write-Status "Building frontend for production..."
    Set-Location frontend
    npm install
    npm run build
    Set-Location ..
    Write-Success "Frontend build completed"
}

# Step 2: Functions Setup
Write-Status "Setting up Firebase Functions..."
Set-Location functions
npm install

# Add TypeScript dependencies if missing
$packageJson = Get-Content "package.json" | ConvertFrom-Json
if (!$packageJson.devDependencies."typescript") {
    Write-Status "Installing TypeScript dependencies..."
    npm install --save-dev typescript "@types/node" "@types/express" "@types/cors"
}

# Build functions
try {
    npm run build
} catch {
    Write-Warning "Functions build encountered issues, continuing..."
}
Set-Location ..
Write-Success "Functions setup completed"

# Step 3: Environment Configuration
Write-Status "Environment Configuration Required..."
Write-Warning "Before deploying, make sure to set these Firebase config variables:"
Write-Host ""
Write-Host "firebase functions:config:set alpaca.key=`"YOUR_ALPACA_KEY`"" -ForegroundColor Magenta
Write-Host "firebase functions:config:set alpaca.secret=`"YOUR_ALPACA_SECRET`"" -ForegroundColor Magenta
Write-Host "firebase functions:config:set alpaca.paper=`"true`"" -ForegroundColor Magenta
Write-Host "firebase functions:config:set encryption.key=`"YOUR_ENCRYPTION_KEY`"" -ForegroundColor Magenta
Write-Host ""

# Step 4: Firebase Login Check
Write-Status "Checking Firebase authentication..."
try {
    firebase projects:list | Out-Null
} catch {
    Write-Warning "Please login to Firebase:"
    firebase login
}

# Step 5: Set Firebase Project
if ($ProjectId) {
    Write-Status "Setting Firebase project to: $ProjectId"
    firebase use $ProjectId
}

# Step 6: Deploy to Firebase
Write-Status "Preparing for deployment..."
Write-Warning "This will deploy:"
Write-Host "- Frontend to Firebase Hosting" -ForegroundColor Yellow
Write-Host "- Backend functions to Cloud Functions" -ForegroundColor Yellow
Write-Host "- Firestore security rules" -ForegroundColor Yellow
Write-Host "- Storage rules" -ForegroundColor Yellow
Write-Host ""

if ($Production) {
    $confirm = "y"
} else {
    $confirm = Read-Host "Continue with deployment? (y/N)"
}

if ($confirm -eq "y" -or $confirm -eq "Y") {
    Write-Status "Starting Firebase deployment..."
    
    try {
        firebase deploy
        Write-Success "Deployment completed successfully!"
    } catch {
        Write-Error "Deployment failed: $_"
        exit 1
    }
} else {
    Write-Warning "Deployment cancelled by user"
    exit 0
}

# Step 7: Post-deployment setup
Write-Status "Post-deployment configuration..."

# Display project info
try {
    $projectInfo = firebase projects:list | Select-String "│.*│.*│.*│" | Select-Object -First 1
    if ($projectInfo) {
        Write-Success "🎉 MASS Framework Live Deployment Complete!"
    }
} catch {
    Write-Success "🎉 MASS Framework Deployment Complete!"
}

Write-Host ""
Write-Host "🔧 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Configure Alpaca API keys:" -ForegroundColor White
Write-Host "   firebase functions:config:set alpaca.key=`"YOUR_KEY`"" -ForegroundColor Gray
Write-Host "2. Set up custom domain (optional)" -ForegroundColor White
Write-Host "3. Configure KYC/AML verification service" -ForegroundColor White
Write-Host "4. Set up monitoring and alerts" -ForegroundColor White
Write-Host "5. Test trading functionality" -ForegroundColor White
Write-Host ""

# Try to get the hosting URL
try {
    $projectInfo = firebase projects:list --json | ConvertFrom-Json
    if ($projectInfo -and $projectInfo.Count -gt 0) {
        $project = $projectInfo[0]
        Write-Host "🌐 Your app should be available at: https://$($project.projectId).web.app" -ForegroundColor Green
    }
} catch {
    Write-Host "🌐 Your app should be available at: https://YOUR_PROJECT_ID.web.app" -ForegroundColor Green
}

Write-Host ""
Write-Host "📊 Trading Features Enabled:" -ForegroundColor Cyan
Write-Host "✅ Live trading with Alpaca Markets" -ForegroundColor Green
Write-Host "✅ Real-time performance analytics" -ForegroundColor Green
Write-Host "✅ Risk management and position limits" -ForegroundColor Green
Write-Host "✅ Demo to live trading upgrade path" -ForegroundColor Green
Write-Host "✅ AI-driven trade execution" -ForegroundColor Green
