#!/bin/bash

# Check why SSM is not working and provide fix
echo "Investigating SSM issue..."

INSTANCE_ID="i-03f885aa16abdfd92"
REGION="us-east-1"

# Check IAM instance profile
echo "Checking IAM instance profile..."
INSTANCE_PROFILE=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --region $REGION --query 'Reservations[0].Instances[0].IamInstanceProfile.Id' --output text 2>/dev/null)

if [ "$INSTANCE_PROFILE" = "None" ] || [ -z "$INSTANCE_PROFILE" ]; then
    echo "❌ No IAM instance profile attached - this is why SSM doesn't work"
    echo ""
    echo "To fix SSM, you need to:"
    echo "1. Create an IAM role with SSM permissions"
    echo "2. Attach it to the instance"
    echo ""
    echo "Quick fix commands:"
    echo ""
    cat << 'FIX_SSM'
# Create IAM role for SSM
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
}'

# Attach SSM policy to role
aws iam attach-role-policy --role-name EC2-SSM-Role --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore

# Create instance profile
aws iam create-instance-profile --instance-profile-name EC2-SSM-Profile

# Add role to instance profile
aws iam add-role-to-instance-profile --instance-profile-name EC2-SSM-Profile --role-name EC2-SSM-Role

# Wait for propagation
echo "Waiting for IAM role propagation..."
sleep 10

# Attach to instance
aws ec2 associate-iam-instance-profile --instance-id i-03f885aa16abdfd92 --iam-instance-profile Name=EC2-SSM-Profile

echo "✅ SSM role attached. Wait 5 minutes, then try again."
FIX_SSM
else
    echo "✅ Instance has IAM profile: $INSTANCE_PROFILE"
    echo "SSM should work - agent may be installing"
fi

echo ""
echo "For immediate deployment, use AWS Console EC2 Instance Connect!"
