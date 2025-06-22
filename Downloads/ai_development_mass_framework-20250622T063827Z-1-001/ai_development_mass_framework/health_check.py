
"""
Health check endpoint for MASS Framework
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time
import psutil
import asyncio

app = FastAPI()

@app.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "uptime": time.time() - start_time
    }

@app.get("/metrics")
async def metrics():
    """System metrics"""
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "timestamp": time.time()
    }

start_time = time.time()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
