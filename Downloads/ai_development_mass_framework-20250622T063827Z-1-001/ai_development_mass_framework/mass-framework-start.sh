#!/bin/bash

echo "=== MASS Framework Diagnostic and Start ==="
echo "Current Time: $(date)"
echo "Current User: $(whoami)"
echo "Current Directory: $(pwd)"
echo ""

echo "=== Checking Python processes ==="
ps aux | grep python || echo "No Python processes found"
echo ""

echo "=== Checking port 8000 usage ==="
netstat -tlnp | grep 8000 || echo "Port 8000 not in use"
echo ""

echo "=== Checking home directory ==="
ls -la /home/ec2-user/
echo ""

echo "=== Checking mass-framework directory ==="
if [ -d "/home/ec2-user/mass-framework" ]; then
    echo "Mass framework directory exists"
    ls -la /home/ec2-user/mass-framework/
    echo ""
    echo "=== Checking virtual environment ==="
    if [ -d "/home/ec2-user/mass-framework/venv" ]; then
        echo "Virtual environment exists"
        echo "=== Starting MASS Framework ==="
        cd /home/ec2-user/mass-framework
        source venv/bin/activate
        export PYTHONPATH=/home/ec2-user/mass-framework
        
        echo "Killing any existing Python processes..."
        pkill -f python || echo "No Python processes to kill"
        
        echo "Starting MASS Framework server..."
        nohup python -m ai_development_mass_framework.main --host 0.0.0.0 --port 8000 > mass_framework.log 2>&1 &
        
        sleep 3
        echo "=== Post-start status ==="
        ps aux | grep python
        netstat -tlnp | grep 8000
        
        echo "=== Recent log output ==="
        tail -20 mass_framework.log
    else
        echo "Virtual environment not found!"
        echo "Creating virtual environment and installing requirements..."
        cd /home/ec2-user/mass-framework
        python3 -m venv venv
        source venv/bin/activate
        pip install -r ai_development_mass_framework/requirements.txt
        export PYTHONPATH=/home/ec2-user/mass-framework
        nohup python -m ai_development_mass_framework.main --host 0.0.0.0 --port 8000 > mass_framework.log 2>&1 &
        sleep 3
        ps aux | grep python
        netstat -tlnp | grep 8000
        tail -20 mass_framework.log
    fi
else
    echo "Mass framework directory NOT found!"
    echo "Available directories in /home/ec2-user/:"
    ls -la /home/ec2-user/
fi

echo ""
echo "=== Final status check ==="
echo "Python processes:"
ps aux | grep python | grep -v grep
echo "Port 8000 status:"
netstat -tlnp | grep 8000
echo ""
echo "=== Diagnostic complete ==="
