#!/bin/bash

# 🚀 MASS Framework - Firebase Production Launch Script
# Automated deployment to Firebase with full error checking

echo "🔥 MASS Framework - Firebase Production Launch 🔥"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "firebase.json" ]; then
    print_error "firebase.json not found. Please run this script from the ai_development_mass_framework directory."
    exit 1
fi

print_status "Starting MASS Framework Firebase deployment..."

# Step 1: Check Firebase CLI
print_status "Checking Firebase CLI installation..."
if ! command -v firebase &> /dev/null; then
    print_warning "Firebase CLI not found. Installing..."
    npm install -g firebase-tools
    if [ $? -ne 0 ]; then
        print_error "Failed to install Firebase CLI. Please install manually: npm install -g firebase-tools"
        exit 1
    fi
else
    print_success "Firebase CLI found"
fi

# Step 2: Check if user is logged in
print_status "Checking Firebase authentication..."
firebase projects:list > /dev/null 2>&1
if [ $? -ne 0 ]; then
    print_warning "Not logged into Firebase. Please login..."
    firebase login
    if [ $? -ne 0 ]; then
        print_error "Firebase login failed. Please try again."
        exit 1
    fi
else
    print_success "Firebase authentication verified"
fi

# Step 3: Check for Firebase project initialization
if [ ! -f ".firebaserc" ]; then
    print_warning "Firebase project not initialized. Running firebase init..."
    echo ""
    echo "🔧 Firebase Init Instructions:"
    echo "1. Select: Hosting, Functions, Firestore"
    echo "2. Choose: Use an existing project OR create new project"
    echo "3. Public directory: public"
    echo "4. Single-page app: Yes"
    echo "5. Functions language: JavaScript"
    echo "6. Install dependencies: Yes"
    echo ""
    read -p "Press Enter to continue with firebase init..."
    
    firebase init
    if [ $? -ne 0 ]; then
        print_error "Firebase initialization failed."
        exit 1
    fi
else
    print_success "Firebase project already initialized"
fi

# Step 4: Install function dependencies
print_status "Installing Firebase Functions dependencies..."
if [ -d "functions" ]; then
    cd functions
    if [ ! -d "node_modules" ]; then
        npm install
        if [ $? -ne 0 ]; then
            print_error "Failed to install function dependencies"
            cd ..
            exit 1
        fi
    else
        print_success "Dependencies already installed"
    fi
    cd ..
else
    print_error "Functions directory not found"
    exit 1
fi

# Step 5: Check Firebase config in frontend files
print_status "Checking Firebase configuration in frontend files..."
if grep -q "YOUR_CONFIG_HERE" public/index.html || grep -q "YOUR_CONFIG_HERE" public/dashboard.html; then
    print_warning "Firebase config not updated in frontend files!"
    echo ""
    echo "🔧 Please update Firebase config:"
    echo "1. Go to Firebase Console → Project Settings → General"
    echo "2. Scroll to 'Your apps' → Web app → Config"
    echo "3. Copy the firebaseConfig object"
    echo "4. Replace 'YOUR_CONFIG_HERE' in public/index.html (line ~85)"
    echo "5. Replace 'YOUR_CONFIG_HERE' in public/dashboard.html (line ~120)"
    echo ""
    read -p "Press Enter after updating the config files..."
fi

# Step 6: Build and deploy functions first
print_status "Deploying Firebase Functions..."
firebase deploy --only functions
if [ $? -ne 0 ]; then
    print_error "Function deployment failed"
    print_warning "Continuing with hosting deployment..."
fi

# Step 7: Deploy Firestore rules
print_status "Deploying Firestore rules..."
firebase deploy --only firestore:rules
if [ $? -ne 0 ]; then
    print_warning "Firestore rules deployment failed, but continuing..."
fi

# Step 8: Deploy hosting
print_status "Deploying Firebase Hosting..."
firebase deploy --only hosting
if [ $? -ne 0 ]; then
    print_error "Hosting deployment failed"
    exit 1
fi

# Step 9: Get deployment info
print_status "Getting deployment information..."
PROJECT_ID=$(firebase use --display-name 2>/dev/null || echo "unknown")
HOSTING_URL="https://${PROJECT_ID}.web.app"

# Success message
echo ""
echo "🎉 MASS Framework Successfully Deployed! 🎉"
echo "============================================"
print_success "Frontend URL: $HOSTING_URL"
print_success "API Endpoint: $HOSTING_URL/api"
print_success "Dashboard: $HOSTING_URL/dashboard.html"

echo ""
echo "🔧 Next Steps:"
echo "1. Visit your site: $HOSTING_URL"
echo "2. Test user registration/login"
echo "3. Enable authentication providers in Firebase Console"
echo "4. Set up custom domain (optional)"
echo "5. Configure environment variables for production"

echo ""
echo "📊 Monitoring:"
echo "• Firebase Console: https://console.firebase.google.com/project/${PROJECT_ID}"
echo "• Function logs: firebase functions:log"
echo "• Hosting metrics: Firebase Console → Hosting"

echo ""
echo "🚨 Emergency Commands:"
echo "• Rollback: firebase hosting:channel:deploy production --rollback"
echo "• View logs: firebase functions:log --limit 50"

print_success "MASS Framework is now LIVE on Firebase! 🚀"

# Optional: Open the site
read -p "Open the deployed site in browser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open "$HOSTING_URL"
    elif command -v open &> /dev/null; then
        open "$HOSTING_URL"
    else
        print_status "Please open $HOSTING_URL in your browser"
    fi
fi

echo ""
print_success "Deployment complete! Your MASS Framework is ready for beta testing! 🎉"
