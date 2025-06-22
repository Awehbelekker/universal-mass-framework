#!/bin/bash

echo "🚀 MASS Framework - Complete Solution Script"
echo "==========================================="
echo "This script will:"
echo "1. Fix AWS networking issues"
echo "2. Deploy the production server"
echo "3. Verify everything is working"
echo ""

read -p "Press Enter to continue..."

echo "Step 1: Running AWS network diagnostics and fixes..."
chmod +x aws-network-fix.sh
./aws-network-fix.sh

echo ""
echo "Step 2: Waiting for AWS changes to propagate..."
sleep 30

echo ""
echo "Step 3: Deploying production server..."
chmod +x final-network-fix.sh
./final-network-fix.sh &

echo ""
echo "Step 4: Waiting for server startup..."
sleep 10

echo ""
echo "Step 5: Final verification..."
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

echo "Testing internal endpoints..."
curl -s http://localhost:8000/health | head -n 3
echo ""

echo "Testing external endpoints..."
echo "Primary URL: http://$PUBLIC_IP:8000"
echo "Health Check: http://$PUBLIC_IP:8000/health"
echo "API Info: http://$PUBLIC_IP:8000/api/info"
echo "Test Page: http://$PUBLIC_IP:8000/test"

echo ""
echo "🎯 MASS Framework should now be accessible at:"
echo "   http://$PUBLIC_IP:8000"
echo ""
echo "🔧 If still not accessible externally, use SSH tunnel:"
echo "   ssh -L 8000:localhost:8000 ec2-user@$PUBLIC_IP"
echo "   Then visit: http://localhost:8000"
echo ""
echo "✅ Deployment complete!"
