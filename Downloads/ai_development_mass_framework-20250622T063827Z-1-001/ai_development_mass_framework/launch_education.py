#!/usr/bin/env python3
"""
MASS Framework Education Platform Launcher
Enhanced AI-powered development environment with education features coming soon!
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from main import create_app
from core.auth_service import AuthenticationService
from core.database_manager import DatabaseManager

def main():
    """Launch the MASS Framework with education features."""
    
    print("🎓 MASS Framework - Education Platform")
    print("=" * 50)
    print("🚀 Starting AI-powered development environment...")
    print("📚 Education Platform: Coming Soon!")
    print("=" * 50)
    
    try:
        # Initialize core services
        db_manager = DatabaseManager()
        auth_service = AuthenticationService(db_manager=db_manager)
        
        # Create the FastAPI app
        app = create_app(auth_service, db_manager)
        
        print("\n✅ Services initialized successfully!")
        print("\n🌐 Access Points:")
        print("   • Main Platform: http://localhost:8000")
        print("   • Education Preview: http://localhost:8000/education-coming-soon.html")
        print("   • API Documentation: http://localhost:8000/docs")
        print("   • Admin Dashboard: http://localhost:8000/dashboard.html")
        print("   • Onboarding Tour: http://localhost:8000/onboarding.html")
        print("\n🎯 Features Ready:")
        print("   • AI-powered code generation")
        print("   • Multiple builder interfaces")
        print("   • Template gallery")
        print("   • Real-time collaboration")
        print("   • Analytics dashboard")
        print("\n🎓 Education Features (Coming Q3 2025):")
        print("   • Gamified learning paths")
        print("   • AI tutoring system")
        print("   • Team coding challenges")
        print("   • Skill competitions")
        print("   • Progressive curriculum")
        print("\n" + "=" * 50)
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start the server
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000,
            log_level="info",
            reload=False
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 MASS Framework stopped. Thanks for using our platform!")
    except Exception as e:
        print(f"\n❌ Error starting MASS Framework: {str(e)}")
        print("Please check the logs and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
