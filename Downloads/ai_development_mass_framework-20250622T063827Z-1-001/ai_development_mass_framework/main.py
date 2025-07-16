"""
MASS Framework - Main Application Entry Point

This is the main FastAPI application that serves as the backend API
for the Multi-Agent AI Development System.
"""

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Import core components
from core.advanced_mass_coordinator import AdvancedMASSCoordinator
from universal_mass_framework.core.mass_engine import MassEngine
from core.enhanced_agent_base import EnhancedAgentBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MASS Framework API",
    description="Multi-Agent AI Development System API",
    version="3.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core systems
mass_coordinator = AdvancedMASSCoordinator()
mass_engine = MassEngine()

@app.on_event("startup")
async def startup_event():
    """Initialize systems on startup"""
    try:
        logger.info("Starting MASS Framework...")
        await mass_engine.start()
        logger.info("MASS Framework started successfully")
    except Exception as e:
        logger.error(f"Failed to start MASS Framework: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        await mass_engine.stop()
        logger.info("MASS Framework stopped successfully")
    except Exception as e:
        logger.error(f"Error stopping MASS Framework: {e}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "3.0.0",
        "services": {
            "mass_engine": "running",
            "coordinator": "running"
        }
    }

# Status endpoint
@app.get("/status")
async def system_status():
    """Get system status"""
    return {
        "status": "online",
        "timestamp": datetime.utcnow().isoformat(),
        "active_workflows": len(mass_coordinator.active_workflows),
        "registered_agents": len(mass_coordinator.agents),
        "engine_status": "running"
    }

# App generation endpoint
@app.post("/api/generate-app")
async def generate_app(requirements: Dict[str, Any]):
    """Generate a complete application based on requirements"""
    try:
        workflow_id = f"app_gen_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        result = await mass_coordinator.execute_enterprise_app_generation(
            user_id="demo_user",
            tenant_id="demo_tenant",
            requirements=requirements
        )
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"App generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Demo endpoint
@app.post("/api/demo/quick-app")
async def quick_app_demo(request: Dict[str, Any]):
    """Quick app generation demo"""
    try:
        # Simulate app generation
        app_name = f"{request.get('app_concept', 'Demo App')} v1.0"
        execution_time = 2.5
        estimated_value = 15000
        
        return {
            "success": True,
            "app_name": app_name,
            "execution_time": execution_time,
            "estimated_value": estimated_value,
            "features": request.get('key_features', []),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Workflow status endpoint
@app.get("/api/workflow/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get workflow status"""
    try:
        status = await mass_coordinator.get_workflow_status(workflow_id)
        return status
    except Exception as e:
        logger.error(f"Failed to get workflow status: {e}")
        raise HTTPException(status_code=404, detail="Workflow not found")

# Metrics endpoint
@app.get("/api/metrics")
async def get_metrics():
    """Get system metrics"""
    try:
        metrics = await mass_coordinator.get_enterprise_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files
if os.path.exists("frontend/build"):
    app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main application"""
    try:
        with open("frontend/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
            <head><title>MASS Framework</title></head>
            <body>
                <h1>MASS Framework API</h1>
                <p>API is running. Check <a href="/docs">/docs</a> for API documentation.</p>
            </body>
        </html>
        """)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
