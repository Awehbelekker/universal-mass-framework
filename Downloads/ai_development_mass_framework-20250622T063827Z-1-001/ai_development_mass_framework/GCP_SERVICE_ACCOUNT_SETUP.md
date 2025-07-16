# GCP Service Account Setup Guide

## Step-by-Step Instructions

### 1. Access Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Select your project (or create a new one)

### 2. Create a Service Account
1. In the left navigation menu, go to **IAM & Admin** → **Service Accounts**
2. Click **"CREATE SERVICE ACCOUNT"**
3. Fill in the details:
   - **Service account name**: `mass-framework-deployer`
   - **Service account ID**: Will auto-generate
   - **Description**: `Service account for MASS Framework deployment`
4. Click **"CREATE AND CONTINUE"**

### 3. Grant Permissions
1. In the "Grant this service account access to project" section:
2. Add these roles:
   - **Cloud Run Admin** (for deploying to Cloud Run)
   - **Storage Admin** (for accessing container registry)
   - **Service Account User** (for running services)
   - **Cloud Build Editor** (for building containers)
3. Click **"CONTINUE"**

### 4. Create and Download the Key
1. Click **"DONE"** to finish creating the service account
2. Find your new service account in the list and click on it
3. Go to the **"KEYS"** tab
4. Click **"ADD KEY"** → **"Create new key"**
5. Choose **JSON** format
6. Click **"CREATE"**
7. The JSON file will automatically download to your computer

### 5. Locate the Downloaded File
The file will be downloaded to your default downloads folder:
- **Windows**: `C:\Users\Judy\Downloads\`
- Look for a file named something like: `mass-framework-deployer-xxxxx.json`

### 6. Use the File Path in the Setup Script
When the PowerShell script asks for the path, provide the full path to the downloaded JSON file, for example:
```
C:\Users\Judy\Downloads\mass-framework-deployer-xxxxx.json
```

## Alternative: Quick Setup Commands

If you have the Google Cloud CLI installed, you can create the service account via command line:

```bash
# Install Google Cloud CLI if not already installed
# Download from: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Create service account
gcloud iam service-accounts create mass-framework-deployer \
    --display-name="MASS Framework Deployer"

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:mass-framework-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:mass-framework-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Create and download key
gcloud iam service-accounts keys create ~/Downloads/mass-framework-deployer.json \
    --iam-account=mass-framework-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

## Security Best Practices

1. **Store the key securely**: Keep the JSON file in a secure location
2. **Don't commit to version control**: Never commit the service account key to Git
3. **Rotate regularly**: Create new keys periodically and update GitHub secrets
4. **Limit permissions**: Only grant the minimum permissions needed
5. **Monitor usage**: Check the service account's activity in Google Cloud Console

## Troubleshooting

### Common Issues:

1. **"Permission denied" errors**
   - Ensure the service account has the required roles
   - Check that you're using the correct project ID

2. **"File not found" errors**
   - Verify the file path is correct
   - Check that the file exists in the specified location

3. **"Invalid JSON" errors**
   - Ensure the file is a valid JSON service account key
   - Don't modify the downloaded file

### Getting Your Project ID:

1. In Google Cloud Console, look at the project selector in the top navigation
2. The project ID is shown there (not the project name)
3. It usually looks like: `my-project-123456` or `mass-framework-xxxxx`

## Next Steps

Once you have the service account key file:

1. **Provide the file path** to the PowerShell script
2. **The script will automatically**:
   - Read the JSON content
   - Upload it as a GitHub secret
   - Clean up the local file (for security)
3. **Test the setup** using the test workflow
4. **Monitor deployments** to ensure everything works

## File Path Examples

Common locations for the downloaded file:
```
C:\Users\Judy\Downloads\mass-framework-deployer-xxxxx.json
C:\Users\Judy\Desktop\service-account-key.json
C:\temp\gcp-key.json
```

**Note**: Replace `xxxxx` with the actual random string in your filename. 

## For the PowerShell script prompt, you need to provide the full path to your GCP service account JSON key file.

**If you already have the file:**
Enter the full path, for example:
```
C:\Users\Judy\Downloads\mass-framework-deployer-xxxxx.json
```

**If you don't have the file yet:**
1. Follow the guide I just created (`GCP_SERVICE_ACCOUNT_SETUP.md`)
2. Go to [Google Cloud Console](https://console.cloud.google.com/)
3. Create a service account and download the JSON key
4. Then provide the path to the downloaded file

**Quick check - do you have a Google Cloud project set up?** If not, you'll need to:
1. Create a Google Cloud project first
2. Enable the required APIs (Cloud Run, Container Registry, etc.)
3. Then create the service account

**What's your current situation?**
- Do you already have a Google Cloud project?
- Do you have a service account key file downloaded?
- Or do you need help setting up Google Cloud from scratch?

Let me know and I can guide you through the specific steps you need! 