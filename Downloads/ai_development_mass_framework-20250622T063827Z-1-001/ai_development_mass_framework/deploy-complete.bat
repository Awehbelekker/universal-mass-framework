@echo off
echo.
echo 🚀 MASS Framework - Complete Application Deployment
echo ===================================================
echo.

set INSTANCE_IP=54.167.234.7
set SSH_KEY=%USERPROFILE%\.ssh\mass-framework-key.pem

echo 🌐 Deploying complete MASS Framework to: %INSTANCE_IP%
echo.

echo 📤 Uploading deployment script...
scp -i "%SSH_KEY%" -o StrictHostKeyChecking=no "deploy-complete-mass.sh" "ec2-user@%INSTANCE_IP%:/tmp/deploy-complete-mass.sh"

if %errorlevel% equ 0 (
    echo ✅ Script uploaded successfully
    echo.
    echo 🚀 Executing complete deployment...
    echo ⏳ This will install dependencies and start the full application...
    echo.
    ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no "ec2-user@%INSTANCE_IP%" "chmod +x /tmp/deploy-complete-mass.sh && /tmp/deploy-complete-mass.sh"
    
    if %errorlevel% equ 0 (
        echo.
        echo 🎉 COMPLETE MASS FRAMEWORK DEPLOYED SUCCESSFULLY!
        echo =================================================
        echo.
        echo 🔗 Application URL: http://%INSTANCE_IP%:8000
        echo.
        echo 🔐 LOGIN CREDENTIALS:
        echo 👤 Admin: admin / admin
        echo 👨‍💻 Developer: demo / secret123
        echo.
        echo ✅ FEATURES NOW AVAILABLE:
        echo   🔐 Full Authentication System
        echo   🤖 AI Development Agents
        echo   🔄 Workflow Management  
        echo   💬 Interactive AI Chat
        echo   📊 Dashboard ^& Analytics
        echo   🎨 Modern Web Application
        echo.
        echo 🎯 READY FOR BETA TESTING!
        echo.
        echo 🧪 Testing application health...
        curl -s http://%INSTANCE_IP%:8000/health
        echo.
    ) else (
        echo ❌ Deployment execution failed
    )
) else (
    echo ❌ Failed to upload deployment script
)

echo.
echo 🌟 MASS FRAMEWORK DEPLOYMENT COMPLETE!
pause
