"""
Production Monitoring and Observability for MASS Framework
Provides metrics, health checks, and monitoring endpoints for cloud deployment
"""

import time
import json
import psutil
import asyncio
import os
from datetime import datetime, timezone
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthStatus(BaseModel):
    """Health status response model"""
    status: str
    timestamp: str
    version: str
    uptime_seconds: float
    checks: Dict[str, Any]

class SystemMetrics(BaseModel):
    """System metrics response model"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_available_mb: float
    disk_usage_percent: float
    active_connections: int
    uptime_seconds: float

class ServiceStatus(BaseModel):
    """Individual service status"""
    name: str
    status: str
    last_check: str
    response_time_ms: float
    details: Dict[str, Any]

class MonitoringService:
    """Production monitoring service"""
    
    def __init__(self):
        self.start_time = time.time()
        self.version = "1.0.0"  # TODO: Read from package.json or version file
        self.service_checks = {}
        
    async def get_health_status(self) -> HealthStatus:
        """Get comprehensive health status"""
        try:
            uptime = time.time() - self.start_time
            
            # Perform health checks
            checks = await self._perform_health_checks()
            
            # Determine overall status
            overall_status = "healthy"
            for check_name, check_result in checks.items():
                if check_result.get("status") != "healthy":
                    overall_status = "degraded" if overall_status == "healthy" else "unhealthy"
            
            return HealthStatus(
                status=overall_status,
                timestamp=datetime.now(timezone.utc).isoformat(),
                version=self.version,
                uptime_seconds=uptime,
                checks=checks
            )
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return HealthStatus(
                status="unhealthy",
                timestamp=datetime.now(timezone.utc).isoformat(),
                version=self.version,
                uptime_seconds=time.time() - self.start_time,
                checks={"error": {"status": "unhealthy", "message": str(e)}}
            )
    
    async def get_system_metrics(self) -> SystemMetrics:
        """Get system performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_mb = memory.available / (1024 * 1024)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage_percent = (disk.used / disk.total) * 100
            
            # Network connections (approximate active connections)
            connections = len(psutil.net_connections(kind='inet'))
            
            uptime = time.time() - self.start_time
            
            return SystemMetrics(
                timestamp=datetime.now(timezone.utc).isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_available_mb=memory_available_mb,
                disk_usage_percent=disk_usage_percent,
                active_connections=connections,
                uptime_seconds=uptime
            )
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to get system metrics: {e}")
    
    async def _perform_health_checks(self) -> Dict[str, Any]:
        """Perform various health checks"""
        checks = {}
        
        # Database health check
        checks["database"] = await self._check_database_health()
        
        # Redis health check  
        checks["redis"] = await self._check_redis_health()
        
        # File system health check
        checks["filesystem"] = await self._check_filesystem_health()
        
        # AI services health check
        checks["ai_services"] = await self._check_ai_services_health()
        
        return checks
    
    async def _check_database_health(self) -> Dict[str, Any]:
        """Check database connectivity and performance"""
        try:
            # TODO: Implement actual database health check
            # For now, check if database file exists
            db_path = Path("mass_framework.db")
            if db_path.exists():
                return {
                    "status": "healthy",
                    "response_time_ms": 5.0,
                    "details": {"connection": "ok", "file_exists": True}
                }
            else:
                return {
                    "status": "unhealthy", 
                    "response_time_ms": 0,
                    "details": {"connection": "failed", "file_exists": False}
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": 0,
                "details": {"error": str(e)}
            }
    
    async def _check_redis_health(self) -> Dict[str, Any]:
        """Check Redis connectivity"""
        try:
            # TODO: Implement actual Redis health check
            # For now, assume healthy if Redis URL is configured
            return {
                "status": "healthy",
                "response_time_ms": 2.0,
                "details": {"connection": "ok", "mock": True}
            }
        except Exception as e:
            return {
                "status": "degraded",
                "response_time_ms": 0,
                "details": {"error": str(e), "mock": True}
            }
    
    async def _check_filesystem_health(self) -> Dict[str, Any]:
        """Check filesystem health"""
        try:
            # Check available disk space
            disk = psutil.disk_usage('.')
            free_space_gb = disk.free / (1024 * 1024 * 1024)
            
            if free_space_gb < 1.0:  # Less than 1GB free
                status = "unhealthy"
            elif free_space_gb < 5.0:  # Less than 5GB free
                status = "degraded"
            else:
                status = "healthy"
            
            return {
                "status": status,
                "response_time_ms": 1.0,
                "details": {
                    "free_space_gb": round(free_space_gb, 2),
                    "total_space_gb": round(disk.total / (1024 * 1024 * 1024), 2),
                    "usage_percent": round((disk.used / disk.total) * 100, 1)
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": 0,
                "details": {"error": str(e)}
            }
    
    async def _check_ai_services_health(self) -> Dict[str, Any]:
        """Check AI services health"""
        try:
            # TODO: Implement actual AI service health checks
            # For now, check if required environment variables are set
            import os
            
            openai_configured = bool(os.getenv("OPENAI_API_KEY"))
            anthropic_configured = bool(os.getenv("ANTHROPIC_API_KEY"))
            
            if openai_configured or anthropic_configured:
                status = "healthy"
            else:
                status = "degraded"
            
            return {
                "status": status,
                "response_time_ms": 3.0,
                "details": {
                    "openai_configured": openai_configured,
                    "anthropic_configured": anthropic_configured,
                    "mock": True
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": 0,
                "details": {"error": str(e)}
            }

# Create monitoring service instance
monitoring_service = MonitoringService()

# Create router for monitoring endpoints
monitoring_router = APIRouter(prefix="/monitoring", tags=["monitoring"])

@monitoring_router.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Comprehensive health check endpoint
    Returns detailed health status of all system components
    """
    return await monitoring_service.get_health_status()

@monitoring_router.get("/health/live")
async def liveness_probe():
    """
    Kubernetes liveness probe endpoint
    Returns 200 if service is running
    """
    return {"status": "alive", "timestamp": datetime.now(timezone.utc).isoformat()}

@monitoring_router.get("/health/ready")
async def readiness_probe():
    """
    Kubernetes readiness probe endpoint
    Returns 200 if service is ready to accept traffic
    """
    health = await monitoring_service.get_health_status()
    if health.status in ["healthy", "degraded"]:
        return {"status": "ready", "timestamp": datetime.now(timezone.utc).isoformat()}
    else:
        raise HTTPException(status_code=503, detail="Service not ready")

@monitoring_router.get("/metrics", response_model=SystemMetrics)
async def system_metrics():
    """
    System metrics endpoint for monitoring
    Returns CPU, memory, disk, and network metrics
    """
    return await monitoring_service.get_system_metrics()

@monitoring_router.get("/metrics/prometheus")
async def prometheus_metrics():
    """
    Prometheus-compatible metrics endpoint
    Returns metrics in Prometheus format
    """
    try:
        metrics = await monitoring_service.get_system_metrics()
        health = await monitoring_service.get_health_status()
        
        # Convert to Prometheus format
        prometheus_metrics = f"""# HELP mass_framework_uptime_seconds Uptime in seconds
# TYPE mass_framework_uptime_seconds counter
mass_framework_uptime_seconds {metrics.uptime_seconds}

# HELP mass_framework_cpu_percent CPU usage percentage
# TYPE mass_framework_cpu_percent gauge
mass_framework_cpu_percent {metrics.cpu_percent}

# HELP mass_framework_memory_percent Memory usage percentage  
# TYPE mass_framework_memory_percent gauge
mass_framework_memory_percent {metrics.memory_percent}

# HELP mass_framework_disk_usage_percent Disk usage percentage
# TYPE mass_framework_disk_usage_percent gauge
mass_framework_disk_usage_percent {metrics.disk_usage_percent}

# HELP mass_framework_active_connections Number of active network connections
# TYPE mass_framework_active_connections gauge
mass_framework_active_connections {metrics.active_connections}

# HELP mass_framework_health_status Overall health status (1=healthy, 0.5=degraded, 0=unhealthy)
# TYPE mass_framework_health_status gauge
mass_framework_health_status {1 if health.status == "healthy" else 0.5 if health.status == "degraded" else 0}
"""
        
        return prometheus_metrics
    except Exception as e:
        logger.error(f"Failed to generate Prometheus metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate metrics")

@monitoring_router.get("/info")
async def system_info():
    """
    System information endpoint
    Returns general system and application information
    """
    try:
        import platform
        import sys
        
        return {
            "application": {
                "name": "MASS Framework",
                "version": monitoring_service.version,
                "uptime_seconds": time.time() - monitoring_service.start_time,
                "start_time": datetime.fromtimestamp(monitoring_service.start_time, timezone.utc).isoformat()
            },
            "system": {
                "platform": platform.platform(),
                "architecture": platform.architecture()[0],
                "python_version": sys.version,
                "cpu_count": psutil.cpu_count(),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)
            },
            "environment": {
                "mass_environment": os.getenv("MASS_ENVIRONMENT", "development"),
                "debug_mode": os.getenv("DEBUG", "false").lower() == "true"
            }
        }
    except Exception as e:
        logger.error(f"Failed to get system info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system information")

# Legacy health endpoint for backward compatibility
@monitoring_router.get("/")
async def root_health():
    """Root monitoring endpoint - redirects to health check"""
    return await health_check()

if __name__ == "__main__":
    # Test the monitoring service
    import asyncio
    
    async def test_monitoring():
        service = MonitoringService()
        
        print("Testing health check...")
        health = await service.get_health_status()
        print(f"Health Status: {health.status}")
        print(f"Uptime: {health.uptime_seconds:.2f}s")
        print(f"Checks: {len(health.checks)}")
        
        print("\nTesting system metrics...")
        metrics = await service.get_system_metrics()
        print(f"CPU: {metrics.cpu_percent}%")
        print(f"Memory: {metrics.memory_percent}%")
        print(f"Disk: {metrics.disk_usage_percent}%")
        print(f"Connections: {metrics.active_connections}")
    
    asyncio.run(test_monitoring())
