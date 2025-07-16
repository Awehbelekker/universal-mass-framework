"""
Test suite for authentication and registration system
Tests the new /auth/register, /auth/login, and related endpoints
"""

import pytest
import asyncio
import json
import tempfile
import os
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import create_app, app
from core.auth_service import AuthService, AuthenticationService
from core.database_manager import DatabaseManager


class TestAuthRegistration:
    """Test authentication and registration functionality"""

    @pytest.fixture
    async def test_app(self):
        """Create test app with isolated database"""
        # Create temporary database for testing
        with tempfile.NamedTemporaryFile(delete=False) as tmp_db:
            tmp_db_path = tmp_db.name
        
        try:
            # Initialize test services with temporary database
            db_manager = DatabaseManager(db_path=tmp_db_path)
            auth_service = AuthService(db_manager)
            
            # Create test app
            app = create_app(auth_service=auth_service, db_manager=db_manager)
            
            yield app
            
        finally:
            # Cleanup
            if os.path.exists(tmp_db_path):
                os.unlink(tmp_db_path)

    @pytest.fixture
    async def test_client(self, test_app):
        """Create test client"""
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            yield clientdef test_user_registration_basic():
    """Test basic user registration using sync TestClient"""
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    registration_data = {
        "username": "testuser_sync",
        "email": "test_sync@example.com", 
        "password": "securepassword123",
        "full_name": "Test User Sync"
    }
    
    response = client.post("/auth/register", json=registration_data)
    
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["username"] == "testuser_sync"
    assert data["user"]["email"] == "test_sync@example.com"

def test_health_endpoint_basic():
    """Test health check endpoint using sync TestClient"""
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_user_registration_duplicate_username(self, test_client):
        """Test registration with duplicate username"""
        registration_data = {
            "username": "duplicate",
            "email": "first@example.com",
            "password": "password123",
            "full_name": "First User"
        }
        
        # First registration should succeed
        response1 = await test_client.post("/auth/register", json=registration_data)
        assert response1.status_code == 201
        
        # Second registration with same username should fail
        registration_data["email"] = "second@example.com"
        response2 = await test_client.post("/auth/register", json=registration_data)
        assert response2.status_code == 400
        data = response2.json()
        assert "already exists" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_user_registration_duplicate_email(self, test_client):
        """Test registration with duplicate email"""
        registration_data = {
            "username": "user1", 
            "email": "duplicate@example.com",
            "password": "password123",
            "full_name": "First User"
        }
        
        # First registration should succeed
        response1 = await test_client.post("/auth/register", json=registration_data)
        assert response1.status_code == 201
        
        # Second registration with same email should fail
        registration_data["username"] = "user2"
        response2 = await test_client.post("/auth/register", json=registration_data)
        assert response2.status_code == 400
        data = response2.json()
        assert "already exists" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_user_registration_invalid_data(self, test_client):
        """Test registration with invalid data"""
        # Missing required fields
        response1 = await test_client.post("/auth/register", json={
            "username": "test",
            "password": "pass"
            # Missing email and full_name
        })
        assert response1.status_code == 422  # Validation error
        
        # Invalid email format
        response2 = await test_client.post("/auth/register", json={
            "username": "test",
            "email": "invalid-email",
            "password": "password123",
            "full_name": "Test User"
        })
        assert response2.status_code == 422

    @pytest.mark.asyncio
    async def test_user_login_success(self, test_client):
        """Test successful user login"""
        # First register a user
        registration_data = {
            "username": "logintest",
            "email": "login@example.com",
            "password": "loginpassword123",
            "full_name": "Login Test"
        }
        await test_client.post("/auth/register", json=registration_data)
        
        # Then test login
        login_data = {
            "username": "logintest",
            "password": "loginpassword123"
        }
        
        response = await test_client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["username"] == "logintest"

    @pytest.mark.asyncio
    async def test_user_login_invalid_credentials(self, test_client):
        """Test login with invalid credentials"""
        # Test with non-existent user
        response1 = await test_client.post("/auth/login", json={
            "username": "nonexistent",
            "password": "password123"
        })
        assert response1.status_code == 401
        
        # Register a user first
        await test_client.post("/auth/register", json={
            "username": "validuser",
            "email": "valid@example.com", 
            "password": "correctpassword",
            "full_name": "Valid User"
        })
        
        # Test with wrong password
        response2 = await test_client.post("/auth/login", json={
            "username": "validuser",
            "password": "wrongpassword"
        })
        assert response2.status_code == 401

    @pytest.mark.asyncio
    async def test_protected_me_endpoint(self, test_client):
        """Test the /auth/me protected endpoint"""
        # Register and login to get token
        registration_data = {
            "username": "protectedtest",
            "email": "protected@example.com",
            "password": "password123",
            "full_name": "Protected Test"
        }
        reg_response = await test_client.post("/auth/register", json=registration_data)
        token = reg_response.json()["access_token"]
        
        # Test protected endpoint with valid token
        headers = {"Authorization": f"Bearer {token}"}
        response = await test_client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "protectedtest"
        assert data["email"] == "protected@example.com"

    @pytest.mark.asyncio
    async def test_protected_endpoint_no_token(self, test_client):
        """Test protected endpoint without token"""
        response = await test_client.get("/auth/me")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_protected_endpoint_invalid_token(self, test_client):
        """Test protected endpoint with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = await test_client.get("/auth/me", headers=headers)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_health_endpoint(self, test_client):
        """Test health check endpoint"""
        response = await test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    @pytest.mark.asyncio
    async def test_registration_loading_simulation(self, test_client):
        """Test registration with various scenarios to simulate loading states"""
        import time
        
        # Test multiple rapid registrations to simulate loading
        tasks = []
        for i in range(3):
            registration_data = {
                "username": f"loadtest{i}",
                "email": f"loadtest{i}@example.com",
                "password": "password123",
                "full_name": f"Load Test {i}"
            }
            # Add small delay to simulate real-world usage
            time.sleep(0.1)
            tasks.append(test_client.post("/auth/register", json=registration_data))
        
        # Execute all registrations
        responses = []
        for task in tasks:
            response = await task
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 201
            data = response.json()
            assert "access_token" in data
            assert "user" in data

if __name__ == "__main__":
    # Allow running this test file directly
    pytest.main([__file__, "-v"])
