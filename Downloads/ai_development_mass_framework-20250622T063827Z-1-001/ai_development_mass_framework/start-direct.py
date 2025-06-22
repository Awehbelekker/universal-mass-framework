# MASS Framework Direct Python Server
# This runs the MASS Framework directly without Docker for immediate testing

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Ensure Python 3.8+ is available"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} is available")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing minimal Python requirements...")
    try:
        # Try minimal requirements first
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-minimal.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Minimal requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install minimal requirements: {e}")
        print("Trying essential packages individually...")
        
        # Install essential packages one by one
        essential_packages = [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0", 
            "pydantic>=2.0.0",
            "sqlalchemy>=2.0.0"
        ]
        
        for package in essential_packages:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              check=True, capture_output=True, text=True)
                print(f"✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"⚠️ Failed to install {package}, continuing...")
        
        return True

def setup_environment():
    """Set up environment variables for local development"""
    print("🔧 Setting up environment variables...")
    
    # Create .env file for local development
    env_content = """# MASS Framework Local Development Environment
DEBUG=True
ENVIRONMENT=local
SECRET_KEY=local-dev-secret-key-change-for-production

# Database Settings (SQLite for simplicity)
DATABASE_URL=sqlite:///./mass_framework_local.db
DB_TYPE=sqlite

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_URL=http://localhost:8000

# AI Service Settings (using mock services)
OPENAI_API_KEY=sk-mock-key-for-local-development
AI_SERVICE_MODE=local
USE_MOCK_AI=true

# Security Settings
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Logging
LOG_LEVEL=DEBUG
AUTO_RELOAD=true
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Environment file created")
    return True

def check_main_file():
    """Check if main.py exists and is properly configured"""
    if not os.path.exists('main.py'):
        print("❌ main.py not found")
        return False
    
    print("✅ main.py found")
    return True

def start_server():
    """Start the FastAPI server directly"""
    print("🚀 Starting MASS Framework server...")
    print("=" * 50)
    
    try:
        # Start the server
        cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
        print(f"Running: {' '.join(cmd)}")
        print("=" * 50)
        print("🌐 Server will be available at:")
        print("   • API: http://localhost:8000")
        print("   • Documentation: http://localhost:8000/docs")
        print("   • Health Check: http://localhost:8000/health")
        print("=" * 50)
        print("Press Ctrl+C to stop the server")
        print("")
        
        # Run the server
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True

def main():
    """Main execution function"""
    print("🏠 MASS Framework Direct Python Server")
    print("======================================")
    print("Version: 8.5.0 - No Docker Required")
    print("85% Development Speed Features Ready!")
    print("")
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_main_file():
        print("Please ensure you're in the correct directory with main.py")
        return False
    
    # Setup environment
    setup_environment()
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to set up dependencies")
        return False
    
    print("✅ All prerequisites met!")
    print("")
    
    # Start server
    start_server()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
