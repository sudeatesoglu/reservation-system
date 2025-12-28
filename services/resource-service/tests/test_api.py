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
        assert data["service"] == "resource-service"
    
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


class TestResourceTypeEndpoints:
    """Test resource type endpoints"""
    
    def test_get_resource_types(self):
        """Test getting all resource types"""
        response = client.get("/api/v1/resource-types")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


class TestResourceEndpoints:
    """Test resource endpoints"""
    
    def test_get_resources_unauthorized(self):
        """Test getting resources without token"""
        response = client.get("/api/v1/resources")
        assert response.status_code == 403
    
    def test_create_resource_unauthorized(self):
        """Test creating resource without admin token"""
        response = client.post("/api/v1/resources", json={
            "name": "Test Room",
            "resource_type": "study_room",
            "location": "Building A"
        })
        assert response.status_code == 403
