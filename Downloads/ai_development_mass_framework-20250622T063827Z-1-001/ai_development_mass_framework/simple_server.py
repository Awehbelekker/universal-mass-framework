from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="AI Development Mass Framework", version="3.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Development Mass Framework is running!"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": "2025-07-13T20:30:00",
        "version": "3.0.0",
        "services": {
            "mass_engine": "running",
            "coordinator": "running"
        }
    }

@app.get("/metrics")
async def metrics():
    return {
        "mass_system_cpu_percent": 33.3,
        "mass_system_memory_percent": 45.1,
        "mass_system_disk_percent": 76.8,
        "mass_active_agents": 0.0,
        "mass_active_workflows": 0.0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 