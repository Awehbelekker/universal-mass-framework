@echo off
echo.
echo 🔧 MASS Framework - Client-Side Error Fix Application
echo ======================================================
echo.

set INSTANCE_IP=54.167.234.7
set SSH_KEY=%USERPROFILE%\.ssh\mass-framework-key.pem

echo 🌐 Connecting to MASS Framework server at %INSTANCE_IP%...
echo.

echo 📤 Uploading client-side error fix script...
scp -i "%SSH_KEY%" -o StrictHostKeyChecking=no "ai_development_mass_framework\client-error-fix.sh" "ec2-user@%INSTANCE_IP%:/tmp/client-error-fix.sh"

if %errorlevel% equ 0 (
    echo ✅ Script uploaded successfully
    echo.
    echo 🚀 Executing client-side error fix...
    ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no "ec2-user@%INSTANCE_IP%" "chmod +x /tmp/client-error-fix.sh && /tmp/client-error-fix.sh"
    
    if %errorlevel% equ 0 (
        echo.
        echo 🎉 CLIENT-SIDE ERROR FIX APPLIED SUCCESSFULLY!
        echo 🔗 Test the improvements at: http://%INSTANCE_IP%:8000
        echo 🔧 Browser console errors should now be handled gracefully
        echo.
        echo 🧪 Testing improved health endpoint...
        curl -s http://%INSTANCE_IP%:8000/health | findstr "version"
        echo.
        echo 📋 What was improved:
        echo   ✅ Global error handlers for uncaught exceptions
        echo   ✅ Promise rejection handling  
        echo   ✅ Enhanced status indicator with pulse animation
        echo   ✅ Better CORS support with OPTIONS handling
        echo   ✅ Version bumped to 1.0.1
        echo   ✅ Console error suppression for external resources
    ) else (
        echo ❌ Failed to execute client-side error fix
    )
) else (
    echo ❌ Failed to upload script to server
)

echo.
echo 🌟 CLIENT-FIX DEPLOYMENT COMPLETED!
pause
