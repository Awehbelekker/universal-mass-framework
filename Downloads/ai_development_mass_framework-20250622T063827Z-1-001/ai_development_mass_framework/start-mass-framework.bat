@echo off
echo ====================================
echo  MASS Framework - Quick Launch
echo  85%% Development Speed Increase
echo ====================================
echo.
echo Trying to start MASS Framework...
echo.

REM Try multiple server options
echo Attempting simple_server.py on port 8003...
python simple_server.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying working_server.py...
    python working_server.py
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Trying basic uvicorn command...
        python -m uvicorn simple_server:app --host 127.0.0.1 --port 8005
    )
)

echo.
echo Server session ended.
pause
