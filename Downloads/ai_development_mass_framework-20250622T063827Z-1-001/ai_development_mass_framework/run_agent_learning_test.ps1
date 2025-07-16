# PowerShell script to run the agent learning test with proper encoding

# Set the console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Run the agent learning test
Write-Host "Starting Agent Learning Test with UTF-8 encoding..." -ForegroundColor Cyan

# Install required dependencies if needed
python -m pip install numpy pandas requests

# Run the test script
python launch_agent_learning_test.py

Write-Host "Test completed. Check logs for details." -ForegroundColor Green
