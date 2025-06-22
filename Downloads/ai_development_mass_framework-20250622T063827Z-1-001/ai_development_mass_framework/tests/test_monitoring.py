"""
Tests for Production Monitoring and Observability
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from core.monitoring import MonitoringService, monitoring_router
from fastapi.testclient import TestClient
from fastapi import FastAPI

class TestMonitoringService:
    """Test the monitoring service functionality"""
    
    @pytest.fixture
    def monitoring_service(self):
        """Create a monitoring service instance for testing"""
        return MonitoringService()
    
    @pytest.mark.asyncio
    async def test_health_status(self, monitoring_service):
        """Test health status endpoint"""
        health = await monitoring_service.get_health_status()
        
        assert health.status in ["healthy", "degraded", "unhealthy"]
        assert health.version == "1.0.0"
        assert health.uptime_seconds >= 0
        assert isinstance(health.checks, dict)
        assert len(health.checks) >= 4  # database, redis, filesystem, ai_services
    
    @pytest.mark.asyncio
    async def test_system_metrics(self, monitoring_service):
        """Test system metrics collection"""
        metrics = await monitoring_service.get_system_metrics()
        
        assert 0 <= metrics.cpu_percent <= 100
        assert 0 <= metrics.memory_percent <= 100
        assert metrics.memory_available_mb >= 0
        assert 0 <= metrics.disk_usage_percent <= 100
        assert metrics.active_connections >= 0
        assert metrics.uptime_seconds >= 0
    
    @pytest.mark.asyncio
    async def test_database_health_check(self, monitoring_service):
        """Test database health check"""
        db_health = await monitoring_service._check_database_health()
        
        assert "status" in db_health
        assert db_health["status"] in ["healthy", "degraded", "unhealthy"]
        assert "response_time_ms" in db_health
        assert "details" in db_health
    
    @pytest.mark.asyncio
    async def test_redis_health_check(self, monitoring_service):
        """Test Redis health check"""
        redis_health = await monitoring_service._check_redis_health()
        
        assert "status" in redis_health
        assert redis_health["status"] in ["healthy", "degraded", "unhealthy"]
        assert "response_time_ms" in redis_health
        assert "details" in redis_health
    
    @pytest.mark.asyncio
    async def test_filesystem_health_check(self, monitoring_service):
        """Test filesystem health check"""
        fs_health = await monitoring_service._check_filesystem_health()
        
        assert "status" in fs_health
        assert fs_health["status"] in ["healthy", "degraded", "unhealthy"]
        assert "response_time_ms" in fs_health
        assert "details" in fs_health
        assert "free_space_gb" in fs_health["details"]
    
    @pytest.mark.asyncio
    async def test_ai_services_health_check(self, monitoring_service):
        """Test AI services health check"""
        ai_health = await monitoring_service._check_ai_services_health()
        
        assert "status" in ai_health
        assert ai_health["status"] in ["healthy", "degraded", "unhealthy"]
        assert "response_time_ms" in ai_health
        assert "details" in ai_health

class TestMonitoringEndpoints:
    """Test the monitoring API endpoints"""
    
    @pytest.fixture
    def test_app(self):
        """Create a test FastAPI app with monitoring router"""
        app = FastAPI()
        app.include_router(monitoring_router)
        return app
    
    @pytest.fixture
    def client(self, test_app):
        """Create a test client"""
        return TestClient(test_app)
    
    def test_health_endpoint(self, client):
        """Test /monitoring/health endpoint"""
        response = client.get("/monitoring/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert "uptime_seconds" in data
        assert "checks" in data
        assert data["status"] in ["healthy", "degraded", "unhealthy"]
    
    def test_liveness_probe(self, client):
        """Test /monitoring/health/live endpoint"""
        response = client.get("/monitoring/health/live")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "alive"
        assert "timestamp" in data
    
    def test_readiness_probe_healthy(self, client):
        """Test /monitoring/health/ready endpoint when healthy"""
        response = client.get("/monitoring/health/ready")
        
        # Should return 200 for healthy or degraded status
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "ready"
            assert "timestamp" in data
    
    def test_metrics_endpoint(self, client):
        """Test /monitoring/metrics endpoint"""
        response = client.get("/monitoring/metrics")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "timestamp" in data
        assert "cpu_percent" in data
        assert "memory_percent" in data
        assert "memory_available_mb" in data
        assert "disk_usage_percent" in data
        assert "active_connections" in data
        assert "uptime_seconds" in data
    
    def test_prometheus_metrics(self, client):
        """Test /monitoring/metrics/prometheus endpoint"""
        response = client.get("/monitoring/metrics/prometheus")
        
        assert response.status_code == 200
        content = response.text
        
        # Check for Prometheus metric format
        assert "mass_framework_uptime_seconds" in content
        assert "mass_framework_cpu_percent" in content
        assert "mass_framework_memory_percent" in content
        assert "mass_framework_health_status" in content
        assert "# HELP" in content
        assert "# TYPE" in content
    
    def test_system_info_endpoint(self, client):
        """Test /monitoring/info endpoint"""
        response = client.get("/monitoring/info")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "application" in data
        assert "system" in data
        assert "environment" in data
        
        # Check application info
        app_info = data["application"]
        assert "name" in app_info
        assert "version" in app_info
        assert "uptime_seconds" in app_info
        
        # Check system info
        sys_info = data["system"]
        assert "platform" in sys_info
        assert "python_version" in sys_info
        assert "cpu_count" in sys_info
    
    def test_root_monitoring_endpoint(self, client):
        """Test /monitoring/ root endpoint"""
        response = client.get("/monitoring/")
        
        assert response.status_code == 200
        # Should return same as health check
        data = response.json()
        assert "status" in data
        assert "checks" in data

class TestMonitoringIntegration:
    """Test monitoring integration with the full system"""
    
    @pytest.mark.asyncio
    async def test_monitoring_performance(self):
        """Test that monitoring endpoints respond quickly"""
        monitoring = MonitoringService()
        
        import time
        
        # Test health check performance
        start_time = time.time()
        health = await monitoring.get_health_status()
        health_time = time.time() - start_time
        
        assert health_time < 2.0, "Health check should complete in under 2 seconds"
        
        # Test metrics performance
        start_time = time.time()
        metrics = await monitoring.get_system_metrics()
        metrics_time = time.time() - start_time
        
        assert metrics_time < 1.0, "Metrics collection should complete in under 1 second"
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in monitoring service"""
        monitoring = MonitoringService()
        
        # Mock psutil to raise an exception
        with patch('psutil.cpu_percent', side_effect=Exception("Mock error")):
            try:
                await monitoring.get_system_metrics()
                assert False, "Should have raised an exception"
            except Exception as e:
                assert "Failed to get system metrics" in str(e)
    
    def test_monitoring_with_environment_variables(self):
        """Test monitoring service with different environment variables"""
        import os
        
        # Test with AI keys configured
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            monitoring = MonitoringService()
            # Should indicate AI services are configured
            
        # Test without AI keys
        with patch.dict(os.environ, {}, clear=True):
            monitoring = MonitoringService()
            # Should indicate AI services are not configured

def test_monitoring_cloud_readiness():
    """Test that monitoring is ready for cloud deployment"""
    # Test that all required monitoring endpoints exist
    from core.monitoring import monitoring_router
    
    routes = [route.path for route in monitoring_router.routes]    
    required_endpoints = [
        "/monitoring/health",
        "/monitoring/health/live", 
        "/monitoring/health/ready",
        "/monitoring/metrics",
        "/monitoring/metrics/prometheus",
        "/monitoring/info"
    ]
    
    for endpoint in required_endpoints:
        assert endpoint in routes, f"Required monitoring endpoint {endpoint} not found"
    
    print("✅ All required monitoring endpoints are available")
    print("🚀 Monitoring system is cloud-ready!")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
