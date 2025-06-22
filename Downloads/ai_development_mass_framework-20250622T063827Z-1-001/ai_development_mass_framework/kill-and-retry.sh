#!/bin/bash

# Kill hanging processes and try a simpler approach
echo "Killing hanging SSH processes and trying manual approach..."

# Kill any hanging SSH processes
pkill -f "ssh.*54.167.234.7" || true
pkill -f "quick-fix" || true

# Simple direct approach
REGION="us-east-1"
KEY_NAME="mass-framework-key"
INSTANCE_ID="i-03f885aa16abdfd92"
PUBLIC_IP="54.167.234.7"

echo "Attempting simple SSH test..."

# Check if we already have a working key
if [ -f ~/.ssh/${KEY_NAME}.pem ]; then
    echo "Testing existing key..."
    if timeout 5 ssh -i ~/.ssh/${KEY_NAME}.pem -o StrictHostKeyChecking=no -o ConnectTimeout=3 ec2-user@$PUBLIC_IP "echo 'SSH works'" 2>/dev/null; then
        echo "✅ SSH already working with existing key!"
        
        # Test the application
        echo "Testing application..."
        curl -I http://$PUBLIC_IP:8000 || echo "Application not responding yet"
        
        exit 0
    fi
fi

echo "Existing key not working. Creating new approach..."

# Clean slate
rm -f ~/.ssh/mass-framework-key.*

# Create key
aws ec2 create-key-pair --key-name $KEY_NAME --region $REGION --query 'KeyMaterial' --output text > ~/.ssh/${KEY_NAME}.pem
chmod 400 ~/.ssh/${KEY_NAME}.pem

# Generate public key
ssh-keygen -y -f ~/.ssh/${KEY_NAME}.pem > ~/.ssh/${KEY_NAME}.pub

echo "New key created. Attempting Instance Connect..."

# Use Instance Connect
aws ec2-instance-connect send-ssh-public-key \
    --instance-id $INSTANCE_ID \
    --availability-zone us-east-1a \
    --instance-os-user ec2-user \
    --ssh-public-key file://~/.ssh/${KEY_NAME}.pub \
    --region $REGION

echo "Key sent via Instance Connect. Testing connection immediately..."

# Quick test with very short timeout
if timeout 5 ssh -i ~/.ssh/${KEY_NAME}.pem -o StrictHostKeyChecking=no -o ConnectTimeout=3 ec2-user@$PUBLIC_IP "echo 'Connected via Instance Connect'" 2>/dev/null; then
    echo "✅ Instance Connect worked! Making key permanent..."
    
    # Make permanent in background to avoid hanging
    (
        echo "$(cat ~/.ssh/${KEY_NAME}.pub)" | ssh -i ~/.ssh/${KEY_NAME}.pem -o StrictHostKeyChecking=no -o ConnectTimeout=5 ec2-user@$PUBLIC_IP "mkdir -p ~/.ssh; chmod 700 ~/.ssh; cat >> ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys; echo 'Key made permanent'"
    ) &
    
    # Wait a moment
    sleep 3
    
    # Test permanent access
    if timeout 5 ssh -i ~/.ssh/${KEY_NAME}.pem -o StrictHostKeyChecking=no -o ConnectTimeout=3 ec2-user@$PUBLIC_IP "echo 'Permanent SSH confirmed'" 2>/dev/null; then
        echo "✅ SSH access is now permanent!"
        echo ""
        echo "SSH Command: ssh -i ~/.ssh/${KEY_NAME}.pem ec2-user@$PUBLIC_IP"
        echo "Application URL: http://$PUBLIC_IP:8000"
        echo ""
        echo "Upload mass-framework-deployment.zip and run deployment manually if needed"
    else
        echo "❌ Still having SSH issues"
    fi
else
    echo "❌ Instance Connect failed"
    echo ""
    echo "Alternative: Try AWS Systems Manager Session Manager"
    echo "aws ssm start-session --target $INSTANCE_ID --region $REGION"
fi
