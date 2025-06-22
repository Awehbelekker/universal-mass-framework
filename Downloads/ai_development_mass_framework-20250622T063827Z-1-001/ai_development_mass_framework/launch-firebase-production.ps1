# 🚀 MASS Framework - Firebase Production Launch Script (PowerShell)
# Automated deployment to Firebase with full error checking

Write-Host "🔥 MASS Framework - Firebase Production Launch 🔥" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

function Write-Status {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if we're in the right directory
if (-not (Test-Path "firebase.json")) {
    Write-Error "firebase.json not found. Please run this script from the ai_development_mass_framework directory."
    exit 1
}

Write-Status "Starting MASS Framework Firebase deployment..."

# Step 1: Check Firebase CLI
Write-Status "Checking Firebase CLI installation..."
try {
    firebase --version | Out-Null
    Write-Success "Firebase CLI found"
} catch {
    Write-Warning "Firebase CLI not found. Installing..."
    npm install -g firebase-tools
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install Firebase CLI. Please install manually: npm install -g firebase-tools"
        exit 1
    }
}

# Step 2: Check if user is logged in
Write-Status "Checking Firebase authentication..."
try {
    firebase projects:list | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Not authenticated"
    }
    Write-Success "Firebase authentication verified"
} catch {
    Write-Warning "Not logged into Firebase. Please login..."
    firebase login
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Firebase login failed. Please try again."
        exit 1
    }
}

# Step 3: Check for Firebase project initialization
if (-not (Test-Path ".firebaserc")) {
    Write-Warning "Firebase project not initialized. Running firebase init..."
    Write-Host ""
    Write-Host "🔧 Firebase Init Instructions:" -ForegroundColor Yellow
    Write-Host "1. Select: Hosting, Functions, Firestore" -ForegroundColor White
    Write-Host "2. Choose: Use an existing project OR create new project" -ForegroundColor White
    Write-Host "3. Public directory: public" -ForegroundColor White
    Write-Host "4. Single-page app: Yes" -ForegroundColor White
    Write-Host "5. Functions language: JavaScript" -ForegroundColor White
    Write-Host "6. Install dependencies: Yes" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to continue with firebase init"
    
    firebase init
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Firebase initialization failed."
        exit 1
    }
} else {
    Write-Success "Firebase project already initialized"
}

# Step 4: Install function dependencies
Write-Status "Installing Firebase Functions dependencies..."
if (Test-Path "functions") {
    Set-Location functions
    if (-not (Test-Path "node_modules")) {
        npm install
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to install function dependencies"
            Set-Location ..
            exit 1
        }
    } else {
        Write-Success "Dependencies already installed"
    }
    Set-Location ..
} else {
    Write-Error "Functions directory not found"
    exit 1
}

# Step 5: Check Firebase config in frontend files
Write-Status "Checking Firebase configuration in frontend files..."
$indexContent = Get-Content "public/index.html" -Raw
$dashboardContent = Get-Content "public/dashboard.html" -Raw

if ($indexContent -match "YOUR_CONFIG_HERE" -or $dashboardContent -match "YOUR_CONFIG_HERE") {
    Write-Warning "Firebase config not updated in frontend files!"
    Write-Host ""
    Write-Host "🔧 Please update Firebase config:" -ForegroundColor Yellow
    Write-Host "1. Go to Firebase Console → Project Settings → General" -ForegroundColor White
    Write-Host "2. Scroll to 'Your apps' → Web app → Config" -ForegroundColor White
    Write-Host "3. Copy the firebaseConfig object" -ForegroundColor White
    Write-Host "4. Replace 'YOUR_CONFIG_HERE' in public/index.html (line ~85)" -ForegroundColor White
    Write-Host "5. Replace 'YOUR_CONFIG_HERE' in public/dashboard.html (line ~120)" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter after updating the config files"
}

# Step 6: Build and deploy functions first
Write-Status "Deploying Firebase Functions..."
firebase deploy --only functions
if ($LASTEXITCODE -ne 0) {
    Write-Error "Function deployment failed"
    Write-Warning "Continuing with hosting deployment..."
}

# Step 7: Deploy Firestore rules
Write-Status "Deploying Firestore rules..."
firebase deploy --only firestore:rules
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Firestore rules deployment failed, but continuing..."
}

# Step 8: Deploy hosting
Write-Status "Deploying Firebase Hosting..."
firebase deploy --only hosting
if ($LASTEXITCODE -ne 0) {
    Write-Error "Hosting deployment failed"
    exit 1
}

# Step 9: Get deployment info
Write-Status "Getting deployment information..."
try {
    $ProjectInfo = firebase use | Out-String
    $ProjectId = ($ProjectInfo -split "`n" | Where-Object { $_ -match "Active Project:" } | ForEach-Object { ($_ -split ": ")[1] }).Trim()
    if (-not $ProjectId) {
        $ProjectId = "your-project-id"
    }
} catch {
    $ProjectId = "your-project-id"
}

$HostingUrl = "https://$ProjectId.web.app"

# Success message
Write-Host ""
Write-Host "🎉 MASS Framework Successfully Deployed! 🎉" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Success "Frontend URL: $HostingUrl"
Write-Success "API Endpoint: $HostingUrl/api"
Write-Success "Dashboard: $HostingUrl/dashboard.html"

Write-Host ""
Write-Host "🔧 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Visit your site: $HostingUrl" -ForegroundColor White
Write-Host "2. Test user registration/login" -ForegroundColor White
Write-Host "3. Enable authentication providers in Firebase Console" -ForegroundColor White
Write-Host "4. Set up custom domain (optional)" -ForegroundColor White
Write-Host "5. Configure environment variables for production" -ForegroundColor White

Write-Host ""
Write-Host "📊 Monitoring:" -ForegroundColor Yellow
Write-Host "• Firebase Console: https://console.firebase.google.com/project/$ProjectId" -ForegroundColor White
Write-Host "• Function logs: firebase functions:log" -ForegroundColor White
Write-Host "• Hosting metrics: Firebase Console → Hosting" -ForegroundColor White

Write-Host ""
Write-Host "🚨 Emergency Commands:" -ForegroundColor Red
Write-Host "• Rollback: firebase hosting:channel:deploy production --rollback" -ForegroundColor White
Write-Host "• View logs: firebase functions:log --limit 50" -ForegroundColor White

Write-Success "MASS Framework is now LIVE on Firebase! 🚀"

# Optional: Open the site
$OpenSite = Read-Host "Open the deployed site in browser? (y/n)"
if ($OpenSite -eq "y" -or $OpenSite -eq "Y") {
    Start-Process $HostingUrl
}

Write-Host ""
Write-Success "Deployment complete! Your MASS Framework is ready for beta testing! 🎉"
