# SSH Key Fix and Final Deployment Instructions

## The Issue
The current EC2 instance is using the key pair `mass-framework-key`, but we don't have access to the private key. This script fixes the SSH access and completes the deployment.

## Solution Options

### Option 1: Quick Fix (Recommended)
Use the `deploy-simple-fix.sh` script that:
1. Recreates the original key name (`mass-framework-key`)
2. Uses EC2 Instance Connect to inject the new key
3. Makes the key permanent
4. Completes the deployment

### Option 2: Clean Deployment
Use the `deploy-fixed.sh` script that:
1. Creates a new instance with correct SSH key
2. Stops the old instance (doesn't delete it)
3. Deploys to the new instance

## Instructions for CloudShell

### Step 1: Upload Files to CloudShell
1. Open AWS CloudShell
2. Upload these files:
   - `deploy-simple-fix.sh` (recommended)
   - `mass-framework-deployment.zip`

### Step 2: Run the Deployment
```bash
# Make the script executable
chmod +x deploy-simple-fix.sh

# Run the deployment
./deploy-simple-fix.sh
```

### Step 3: Test the Application
Once deployment completes, test at:
- **Application URL**: http://54.167.234.7:8000

### Step 4: Verify Everything Works
```bash
# SSH to the instance
ssh -i ~/.ssh/mass-framework-key.pem ec2-user@54.167.234.7

# Check application logs
cd ai_development_mass_framework
tail -f mass_framework.log

# Check if service is running
ps aux | grep python
```

## What the Script Does

1. **Fixes SSH Access**:
   - Updates security group for CloudShell IP
   - Recreates the `mass-framework-key` with new private key
   - Uses EC2 Instance Connect to inject the key
   - Makes the key permanent in authorized_keys

2. **Deploys Application**:
   - Uploads deployment package
   - Installs system dependencies
   - Extracts and sets up the application
   - Starts the MASS Framework service

3. **Verifies Deployment**:
   - Checks if application is running
   - Shows recent logs
   - Provides access details

## Troubleshooting

If SSH still fails:
- Check CloudShell IP: `curl -s http://checkip.amazonaws.com`
- Verify security group allows your IP
- Try the alternative script: `deploy-fixed.sh`

If deployment fails:
- Check the logs: `tail -f mass_framework.log`
- Verify all dependencies installed correctly
- Check disk space: `df -h`

## After Successful Deployment

1. **Test Core Features**:
   - Visit http://54.167.234.7:8000
   - Test user registration/login
   - Create a sample project
   - Test AI features

2. **Monitor Performance**:
   - Check system resources: `htop`
   - Monitor logs: `tail -f mass_framework.log`
   - Test response times

3. **Begin Beta Testing**:
   - Share the URL with beta testers
   - Monitor for issues
   - Collect feedback

## Success Indicators

✅ SSH connection works with new key
✅ Application starts without errors
✅ Web interface accessible at http://54.167.234.7:8000
✅ Core features functional
✅ No critical errors in logs

The MASS Framework will be live and ready for beta testing!
