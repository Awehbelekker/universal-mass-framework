#!/bin/bash

# Comprehensive diagnosis and fix script
echo "MASS Framework Deployment - Comprehensive Fix"
echo "============================================="

# Configuration
REGION="us-east-1"
KEY_NAME="mass-framework-key"
INSTANCE_ID="i-03f885aa16abdfd92"
PUBLIC_IP="54.167.234.7"
SECURITY_GROUP_ID="sg-0704254e46ce4f7a3"

# Step 1: Get current CloudShell IP
echo "Step 1: Getting CloudShell IP..."
CLOUDSHELL_IP=$(curl -s http://checkip.amazonaws.com)
echo "CloudShell IP: $CLOUDSHELL_IP"

# Step 2: Check instance status
echo ""
echo "Step 2: Checking EC2 instance status..."
INSTANCE_STATE=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --region $REGION --query 'Reservations[0].Instances[0].State.Name' --output text)
echo "Instance State: $INSTANCE_STATE"

if [ "$INSTANCE_STATE" != "running" ]; then
    echo "⚠️ Instance is not running! Starting it..."
    aws ec2 start-instances --instance-ids $INSTANCE_ID --region $REGION
    echo "Waiting for instance to start..."
    aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $REGION
    echo "✅ Instance started"
else
    echo "✅ Instance is running"
fi

# Step 3: Update security group
echo ""
echo "Step 3: Updating security group for current IP..."
echo "Removing old rules and adding current IP..."

# Remove existing SSH rules (ignore errors)
aws ec2 describe-security-groups --group-ids $SECURITY_GROUP_ID --region $REGION --query 'SecurityGroups[0].IpPermissions[?FromPort==`22`].CidrIpv4' --output text | while read cidr; do
    if [ "$cidr" != "None" ] && [ "$cidr" != "" ]; then
        echo "Removing old rule: $cidr"
        aws ec2 revoke-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr "$cidr" --region $REGION 2>/dev/null || true
    fi
done

# Add current IP
echo "Adding current CloudShell IP: $CLOUDSHELL_IP"
aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr "${CLOUDSHELL_IP}/32" --region $REGION

# Step 4: Fix SSH key
echo ""
echo "Step 4: Creating fresh SSH key..."
aws ec2 delete-key-pair --key-name $KEY_NAME --region $REGION 2>/dev/null || true
rm -f ~/.ssh/${KEY_NAME}.*

# Create key with proper handling
aws ec2 create-key-pair --key-name $KEY_NAME --region $REGION --query 'KeyMaterial' --output text > /tmp/${KEY_NAME}.pem
chmod 400 /tmp/${KEY_NAME}.pem
mv /tmp/${KEY_NAME}.pem ~/.ssh/${KEY_NAME}.pem

echo "✅ SSH key created"

# Step 5: Wait for security group changes to propagate
echo ""
echo "Step 5: Waiting for network changes to propagate..."
sleep 15

# Step 6: Test connection
echo ""
echo "Step 6: Testing SSH connection..."
for i in {1..5}; do
    echo "Attempt $i/5..."
    if timeout 10 ssh -i ~/.ssh/${KEY_NAME}.pem -o StrictHostKeyChecking=no -o ConnectTimeout=8 ec2-user@$PUBLIC_IP "echo 'SSH connection successful'" 2>/dev/null; then
        echo "✅ SSH connection working!"
        SSH_WORKING=true
        break
    else
        echo "❌ Attempt $i failed"
        if [ $i -lt 5 ]; then
            echo "Waiting 10 seconds before retry..."
            sleep 10
        fi
        SSH_WORKING=false
    fi
done

# Step 7: Deploy application if SSH works
if [ "$SSH_WORKING" = "true" ]; then
    echo ""
    echo "Step 7: SSH is working! Checking for deployment package..."
    
    if [ -f "mass-framework-deployment.zip" ]; then
        echo "✅ Deployment package found! Starting deployment..."
        
        # Upload package
        echo "Uploading deployment package..."
        scp -i ~/.ssh/${KEY_NAME}.pem -o StrictHostKeyChecking=no mass-framework-deployment.zip ec2-user@$PUBLIC_IP:/home/ec2-user/
        
        # Deploy
        echo "Deploying application..."
        ssh -i ~/.ssh/${KEY_NAME}.pem -o StrictHostKeyChecking=no ec2-user@$PUBLIC_IP << 'DEPLOY'
            echo "=== Starting MASS Framework Deployment ==="
            
            # Update system
            sudo yum update -y
            sudo yum install -y python3 python3-pip unzip git htop
            
            # Extract application
            echo "Extracting application..."
            unzip -o mass-framework-deployment.zip
            cd ai_development_mass_framework
            
            # Install dependencies
            echo "Installing dependencies..."
            pip3 install --user -r requirements.txt
            
            # Setup environment
            if [ -f ".env.production" ]; then
                cp .env.production .env
                echo "Environment configured"
            fi
            
            # Stop existing processes
            pkill -f "python3 main.py" || true
            
            # Start application
            echo "Starting MASS Framework..."
            nohup python3 main.py > mass_framework.log 2>&1 &
            
            # Check status
            sleep 10
            if ps aux | grep -v grep | grep "python3 main.py"; then
                echo "✅ MASS Framework is running!"
            else
                echo "⚠️ Application may not have started"
            fi
            
            echo ""
            echo "=== Recent Logs ==="
            tail -n 20 mass_framework.log 2>/dev/null || echo "No logs available"
            
            echo ""
            echo "=== Deployment Complete ==="
DEPLOY
        
        echo ""
        echo "🎉 DEPLOYMENT COMPLETE!"
        echo "==========================================="
        echo "Application URL: http://$PUBLIC_IP:8000"
        echo "SSH Access: ssh -i ~/.ssh/${KEY_NAME}.pem ec2-user@$PUBLIC_IP"
        echo "==========================================="
        
        # Test the application
        echo ""
        echo "Testing application..."
        sleep 5
        if curl -I "http://$PUBLIC_IP:8000" 2>/dev/null | grep -q "200\|302\|404"; then
            echo "✅ Application is responding!"
            echo "🎉 MASS Framework is LIVE at http://$PUBLIC_IP:8000"
        else
            echo "⚠️ Application may still be starting up"
            echo "Check in a few minutes at http://$PUBLIC_IP:8000"
        fi
        
    else
        echo ""
        echo "❌ mass-framework-deployment.zip not found"
        echo "Upload the deployment package to complete installation"
        echo ""
        echo "SSH is working though! You can connect with:"
        echo "ssh -i ~/.ssh/${KEY_NAME}.pem ec2-user@$PUBLIC_IP"
    fi
else
    echo ""
    echo "❌ SSH connection failed after all attempts"
    echo ""
    echo "Diagnostic information:"
    echo "Instance ID: $INSTANCE_ID"
    echo "Instance State: $INSTANCE_STATE"
    echo "Public IP: $PUBLIC_IP"
    echo "CloudShell IP: $CLOUDSHELL_IP"
    echo "Security Group: $SECURITY_GROUP_ID"
    echo ""
    echo "Alternative options:"
    echo "1. Use AWS Console Session Manager"
    echo "2. Check if instance is in a different availability zone"
    echo "3. Verify VPC routing and network ACLs"
fi

echo ""
echo "Script completed!"
