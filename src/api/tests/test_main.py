"""
Tests for main FastAPI application configuration.
"""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)

class TestRootEndpoint:
    """Tests for root endpoint."""
    
    def test_root_returns_200(self):
        """Test root endpoint returns 200 OK."""
        response = client.get("/")
        
        assert response.status_code == 200
    
    def test_root_response_structure(self):
        """Test root endpoint has correct structure."""
        response = client.get("/")
        data = response.json()
        
        assert "name" in data
        assert "version" in data
        assert "status" in data
        assert "endpoints" in data
    
    def test_root_endpoints_links(self):
        """Test root includes endpoint links."""
        response = client.get("/")
        data = response.json()
        
        endpoints = data["endpoints"]
        assert "docs" in endpoints
        assert "health" in endpoints
        assert endpoints["docs"] == "/docs"
        assert endpoints["health"] == "/api/health"

class TestAPIDocumentation:
    """Tests for API documentation endpoints."""
    
    def test_docs_accessible(self):
        """Test Swagger UI docs are accessible."""
        response = client.get("/docs")
        
        assert response.status_code == 200
    
    def test_redoc_accessible(self):
        """Test ReDoc documentation is accessible."""
        response = client.get("/redoc")
        
        assert response.status_code == 200
    
    def test_openapi_json_accessible(self):
        """Test OpenAPI JSON schema is accessible."""
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "XAI Evaluation API"
        assert "paths" in data

class TestCORSConfiguration:
    """Tests for CORS middleware."""
    
    def test_cors_headers_present(self):
        """Test CORS headers are present in response."""
        response = client.options(
            "/api/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_localhost_3000(self):
        """Test CORS allows localhost:3000."""
        response = client.get(
            "/api/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"

class TestErrorHandling:
    """Tests for error handling."""
    
    def test_404_not_found(self):
        """Test 404 error for non-existent endpoint."""
        response = client.get("/nonexistent")
        
        assert response.status_code == 404
    
    def test_validation_error_returns_400(self):
        """Test validation errors return 400."""
        # This will be more relevant when we have POST endpoints
        from src.api.middleware.exceptions import validation_exception_handler
        assert validation_exception_handler is not None
