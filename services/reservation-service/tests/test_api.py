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
        assert data["service"] == "reservation-service"
    
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


class TestReservationEndpoints:
    """Test reservation endpoints"""
    
    def test_get_reservations_unauthorized(self):
        """Test getting reservations without token"""
        response = client.get("/api/v1/reservations/my")
        assert response.status_code == 403
    
    def test_create_reservation_unauthorized(self):
        """Test creating reservation without token"""
        response = client.post("/api/v1/reservations", json={
            "resource_id": "123",
            "date": "2024-01-15",
            "start_time": "09:00",
            "end_time": "10:00"
        })
        assert response.status_code == 403
    
    def test_get_availability_unauthorized(self):
        """Test getting availability without token"""
        response = client.get("/api/v1/availability/123?date=2024-01-15")
        assert response.status_code == 403
