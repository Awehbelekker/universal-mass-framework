# Firebase Quick Start Guide

## ✅ You're Ready to Deploy!

Your Firebase project is set up and ready to go. Here's what you need to do:

## Step 1: Get Your Firebase Project ID

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to **Project Settings**
4. Copy the **Project ID** (e.g., `mass-framework-12345`)

## Step 2: Generate Firebase Token

Run this command in your terminal:
```bash
firebase login:ci --no-localhost
```

This will give you a token like: `1//0example-token-here`

## Step 3: Add GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these **2 secrets only**:

```
FIREBASE_PROJECT_ID: your-project-id-here
FIREBASE_TOKEN: your-firebase-token-here
```

## Step 4: Deploy!

### Option A: Manual Deployment
```bash
# Build your frontend
cd frontend
npm run build

# Deploy to Firebase
firebase deploy
```

### Option B: GitHub Actions (Automatic)
Just push to your main branch and it will deploy automatically!

## What You Get

✅ **Frontend**: Your React app hosted at `https://your-project.web.app`  
✅ **Backend**: API functions at `https://your-project.web.app/api/*`  
✅ **Database**: Firestore for all your data  
✅ **Authentication**: Built-in user management  
✅ **Storage**: File uploads and storage  
✅ **Real-time**: Live updates for trading data  

## Your URLs

- **Frontend**: `https://your-project-id.web.app`
- **API Health**: `https://your-project-id.web.app/api/health`
- **Trading API**: `https://your-project-id.web.app/api/trading/*`
- **AI Agents**: `https://your-project-id.web.app/api/ai-agents/*`

## No More Context Access Warnings!

This setup eliminates all the complex secrets:
- ❌ No GCP service account keys
- ❌ No database connection strings
- ❌ No Redis URLs
- ❌ No secret keys
- ✅ Only 2 simple Firebase secrets

## Next Steps

1. **Add the 2 GitHub secrets**
2. **Push to main branch** (triggers deployment)
3. **Test your app** at the Firebase URL
4. **Monitor deployment** in GitHub Actions

## Troubleshooting

### If deployment fails:
1. Check that both secrets are set correctly
2. Verify your Firebase project ID is correct
3. Make sure you're logged into Firebase CLI

### If functions don't work:
1. Check the Firebase Console → Functions
2. Look at the function logs
3. Verify the function URLs are correct

## Cost

**Free Tier Includes:**
- 10GB hosting storage
- 125K function invocations/month
- 1GB Firestore storage
- 10K users/month

**Upgrade to Blaze (Pay per use):**
- Unlimited everything
- Only pay for what you use

## Ready to Deploy?

Just add those 2 GitHub secrets and push to main branch! 🚀 