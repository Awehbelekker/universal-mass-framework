@echo off
echo.
echo ========================================
echo    MASS Framework Demo Runner
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Python found
    goto :run_demo
)

echo Checking py launcher...
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Python found via py launcher
    goto :run_demo_py
)

echo.
echo ❌ Python not found!
echo.
echo To install Python:
echo 1. Download from: https://www.python.org/downloads/
echo 2. Make sure to check "Add Python to PATH" during installation
echo 3. Restart this terminal after installation
echo.
echo Or install via Microsoft Store:
echo 1. Open Microsoft Store
echo 2. Search for "Python"
echo 3. Install Python 3.8 or later
echo.
pause
exit /b 1

:run_demo
echo.
echo 🚀 Running MASS Framework Demo...
python test_mass_framework_simple.py
goto :end

:run_demo_py
echo.
echo 🚀 Running MASS Framework Demo...
py test_mass_framework_simple.py
goto :end

:end
echo.
echo Demo completed!
echo.
echo Next steps:
echo 1. Install Python dependencies: pip install -r requirements.txt
echo 2. Start the server: python main.py
echo 3. Open browser to: http://localhost:8000
echo.
pause 