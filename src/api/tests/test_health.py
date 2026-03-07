"""
Tests for health check endpoints.
"""

from fastapi.testclient import TestClient
from datetime import datetime

from src.api.main import app

client = TestClient(app)

class TestHealthEndpoint:
    """Tests for /api/health endpoint."""
    
    def test_health_check_returns_200(self):
        """Test health check returns 200 OK."""
        response = client.get("/api/health")
        
        assert response.status_code == 200
    
    def test_health_check_response_structure(self):
        """Test health check has correct response structure."""
        response = client.get("/api/health")
        data = response.json()
        
        assert "status" in data
        assert "version" in data
        assert "timestamp" in data
    
    def test_health_check_status_healthy(self):
        """Test health check status is 'healthy'."""
        response = client.get("/api/health")
        data = response.json()
        
        assert data["status"] == "healthy"
    
    def test_health_check_version_correct(self):
        """Test health check returns correct version."""
        from src.api.config import settings
        
        response = client.get("/api/health")
        data = response.json()
        
        assert data["version"] == settings.API_VERSION
    
    def test_health_check_timestamp_valid(self):
        """Test health check timestamp is valid ISO format."""
        response = client.get("/api/health")
        data = response.json()
        
        # Should parse as valid datetime
        timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        assert timestamp is not None

class TestDetailedHealthEndpoint:
    """Tests for /api/health/detailed endpoint."""
    
    def test_detailed_health_returns_200(self):
        """Test detailed health check returns 200 OK."""
        response = client.get("/api/health/detailed")
        
        assert response.status_code == 200
    
    def test_detailed_health_includes_system_info(self):
        """Test detailed health includes system information."""
        response = client.get("/api/health/detailed")
        data = response.json()
        
        assert "system" in data
        assert "experiments_directory" in data["system"]
        assert "experiments_directory_exists" in data["system"]
