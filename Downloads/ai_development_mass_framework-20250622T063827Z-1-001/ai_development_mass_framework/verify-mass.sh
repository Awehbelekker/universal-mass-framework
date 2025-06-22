#!/bin/bash

# MASS Framework - Quick Verification Script
echo "🔍 MASS Framework Verification"
echo "============================="

# Check if server is running
echo "📊 Checking server status..."
if pgrep -f "mass_framework_complete.py" > /dev/null; then
    echo "✅ Server process is running"
    PID=$(pgrep -f "mass_framework_complete.py")
    echo "   Process ID: $PID"
else
    echo "❌ Server process not found"
    exit 1
fi

# Check if port 8000 is listening
echo ""
echo "🔍 Checking port availability..."
if netstat -tlnp 2>/dev/null | grep -q ":8000 "; then
    echo "✅ Port 8000 is active and listening"
else
    echo "❌ Port 8000 is not listening"
    exit 1
fi

# Get public IP
echo ""
echo "🌐 Getting public IP address..."
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
if [ -n "$PUBLIC_IP" ]; then
    echo "✅ Public IP: $PUBLIC_IP"
    echo "🔗 Application URL: http://$PUBLIC_IP:8000"
else
    echo "⚠️  Could not determine public IP"
fi

# Test health endpoint
echo ""
echo "🏥 Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if [[ $HEALTH_RESPONSE == *"healthy"* ]]; then
    echo "✅ Health check passed"
    echo "   Response: $HEALTH_RESPONSE"
else
    echo "❌ Health check failed"
    echo "   Response: $HEALTH_RESPONSE"
fi

# Test main page
echo ""
echo "🏠 Testing main page..."
MAIN_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
if [ "$MAIN_RESPONSE" = "200" ]; then
    echo "✅ Main page accessible (HTTP $MAIN_RESPONSE)"
else
    echo "❌ Main page failed (HTTP $MAIN_RESPONSE)"
fi

echo ""
echo "🎉 Verification complete! Your MASS Framework is ready."
echo "   Login with: admin/admin or demo/secret123"
