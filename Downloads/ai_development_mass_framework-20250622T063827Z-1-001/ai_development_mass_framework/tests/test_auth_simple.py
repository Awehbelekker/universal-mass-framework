"""
Simple test suite for authentication and registration system
"""

import pytest
from fastapi.testclient import TestClient
from main import app


def test_health_endpoint():
    """Test health check endpoint"""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_user_registration():
    """Test user registration endpoint"""
    client = TestClient(app)
    
    registration_data = {
        "username": "testuser123",
        "email": "testuser123@example.com", 
        "password": "securepassword123",
        "full_name": "Test User"
    }
    
    response = client.post("/auth/register", json=registration_data)
    
    # Should return 201 for successful registration
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["username"] == "testuser123"
    assert data["user"]["email"] == "testuser123@example.com"
    assert "password" not in data["user"]  # Password should not be returned


def test_user_login():
    """Test user login endpoint"""
    client = TestClient(app)
    
    # First register a user
    registration_data = {
        "username": "loginuser123",
        "email": "loginuser123@example.com",
        "password": "loginpassword123",
        "full_name": "Login User"
    }
    reg_response = client.post("/auth/register", json=registration_data)
    assert reg_response.status_code == 201
    
    # Then test login
    login_data = {
        "username": "loginuser123",
        "password": "loginpassword123"
    }
    
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["username"] == "loginuser123"


def test_protected_me_endpoint():
    """Test the protected /auth/me endpoint"""
    client = TestClient(app)
    
    # Register and get token
    registration_data = {
        "username": "protecteduser123",
        "email": "protecteduser123@example.com",
        "password": "password123",
        "full_name": "Protected User"
    }
    reg_response = client.post("/auth/register", json=registration_data)
    assert reg_response.status_code == 201
    token = reg_response.json()["access_token"]
    
    # Test protected endpoint with valid token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "protecteduser123"
    assert data["email"] == "protecteduser123@example.com"


def test_protected_endpoint_without_token():
    """Test protected endpoint without authentication"""
    client = TestClient(app)
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_invalid_login():
    """Test login with invalid credentials"""
    client = TestClient(app)
    
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
