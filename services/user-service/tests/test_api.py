import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self):
        """Test health endpoint returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "user-service"
    
    def test_readiness_check(self):
        """Test readiness endpoint returns ready status"""
        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
    
    def test_root_endpoint(self):
        """Test root endpoint returns service info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data


class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    def test_register_missing_fields(self):
        """Test registration with missing fields"""
        response = client.post("/api/v1/auth/register", json={})
        assert response.status_code == 422  # Validation error
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post("/api/v1/auth/login", json={
            "username": "nonexistent",
            "password": "wrongpassword"
        })
        assert response.status_code == 401


class TestUserEndpoints:
    """Test user endpoints"""
    
    def test_get_current_user_unauthorized(self):
        """Test getting current user without token"""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 403  # No credentials
    
    def test_get_users_unauthorized(self):
        """Test getting all users without admin token"""
        response = client.get("/api/v1/users")
        assert response.status_code == 403
