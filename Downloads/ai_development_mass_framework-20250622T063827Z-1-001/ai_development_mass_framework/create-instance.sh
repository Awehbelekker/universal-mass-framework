#!/bin/bash

# Check what EC2 instances exist and create a new one if needed
echo "Checking EC2 instances..."

REGION="us-east-1"

# List all instances
echo "Current EC2 instances in $REGION:"
aws ec2 describe-instances --region $REGION --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress,Tags[?Key==`Name`].Value|[0]]' --output table

echo ""
echo "Checking for our specific instance i-03f885aa16abdfd92..."
INSTANCE_EXISTS=$(aws ec2 describe-instances --instance-ids i-03f885aa16abdfd92 --region $REGION 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✅ Instance exists"
    aws ec2 describe-instances --instance-ids i-03f885aa16abdfd92 --region $REGION --query 'Reservations[0].Instances[0].[InstanceId,State.Name,PublicIpAddress]' --output table
else
    echo "❌ Instance i-03f885aa16abdfd92 does not exist"
    echo ""
    echo "We need to create a new EC2 instance for MASS Framework!"
    echo ""
    
    # Get available AMIs
    echo "Finding suitable AMI..."
    AMI_ID=$(aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*" "Name=architecture,Values=x86_64" --query 'Images|sort_by(@, &CreationDate)[-1].ImageId' --output text --region $REGION)
    echo "Using AMI: $AMI_ID"
    
    # Get default VPC and subnet
    echo "Getting default VPC and subnet..."
    VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text --region $REGION)
    SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[0].SubnetId' --output text --region $REGION)
    
    echo "VPC ID: $VPC_ID"
    echo "Subnet ID: $SUBNET_ID"
    
    # Create security group
    echo "Creating security group..."
    SECURITY_GROUP_ID=$(aws ec2 create-security-group \
        --group-name mass-framework-sg \
        --description "Security group for MASS Framework" \
        --vpc-id $VPC_ID \
        --region $REGION \
        --query 'GroupId' \
        --output text 2>/dev/null || aws ec2 describe-security-groups --filters "Name=group-name,Values=mass-framework-sg" --query 'SecurityGroups[0].GroupId' --output text --region $REGION)
    
    echo "Security Group ID: $SECURITY_GROUP_ID"
    
    # Add security group rules
    echo "Adding security group rules..."
    CLOUDSHELL_IP=$(curl -s http://checkip.amazonaws.com)
    
    # Allow SSH from CloudShell
    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp \
        --port 22 \
        --cidr "${CLOUDSHELL_IP}/32" \
        --region $REGION 2>/dev/null || echo "SSH rule already exists"
    
    # Allow HTTP (port 8000) from anywhere
    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp \
        --port 8000 \
        --cidr "0.0.0.0/0" \
        --region $REGION 2>/dev/null || echo "HTTP rule already exists"
    
    # Create or use existing key pair
    echo "Creating SSH key pair..."
    aws ec2 delete-key-pair --key-name mass-framework-key --region $REGION 2>/dev/null || true
    aws ec2 create-key-pair --key-name mass-framework-key --region $REGION --query 'KeyMaterial' --output text > ~/.ssh/mass-framework-key.pem
    chmod 400 ~/.ssh/mass-framework-key.pem
    
    # Create IAM role for SSM (so we don't have SSH issues)
    echo "Creating IAM role for SSM..."
    aws iam create-role --role-name EC2-SSM-Role --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }' 2>/dev/null || echo "Role already exists"
    
    aws iam attach-role-policy --role-name EC2-SSM-Role --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore 2>/dev/null || echo "Policy already attached"
    
    aws iam create-instance-profile --instance-profile-name EC2-SSM-Profile 2>/dev/null || echo "Profile already exists"
    
    aws iam add-role-to-instance-profile --instance-profile-name EC2-SSM-Profile --role-name EC2-SSM-Role 2>/dev/null || echo "Role already in profile"
    
    # Wait for IAM propagation
    echo "Waiting for IAM role propagation..."
    sleep 10
    
    # Launch new instance
    echo "Launching new EC2 instance..."
    NEW_INSTANCE_ID=$(aws ec2 run-instances \
        --image-id $AMI_ID \
        --instance-type t2.micro \
        --key-name mass-framework-key \
        --security-group-ids $SECURITY_GROUP_ID \
        --subnet-id $SUBNET_ID \
        --associate-public-ip-address \
        --iam-instance-profile Name=EC2-SSM-Profile \
        --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MASS-Framework-Server}]' \
        --region $REGION \
        --query 'Instances[0].InstanceId' \
        --output text)
    
    echo "✅ New instance created: $NEW_INSTANCE_ID"
    
    # Wait for instance to be running
    echo "Waiting for instance to be running..."
    aws ec2 wait instance-running --instance-ids $NEW_INSTANCE_ID --region $REGION
    
    # Get public IP
    PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $NEW_INSTANCE_ID --region $REGION --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
    
    echo ""
    echo "🎉 NEW MASS FRAMEWORK INSTANCE CREATED!"
    echo "======================================"
    echo "Instance ID: $NEW_INSTANCE_ID"
    echo "Public IP: $PUBLIC_IP"
    echo "SSH Key: ~/.ssh/mass-framework-key.pem"
    echo "Security Group: $SECURITY_GROUP_ID"
    echo ""
    echo "Wait 2-3 minutes for the instance to fully initialize, then:"
    echo "1. SSH: ssh -i ~/.ssh/mass-framework-key.pem ec2-user@$PUBLIC_IP"
    echo "2. Or use AWS Console Session Manager"
    echo "3. Deploy your application"
    echo ""
    echo "Application will be available at: http://$PUBLIC_IP:8000"
    echo "======================================"
fi
