import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.api.config import settings

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.mark.integration
def test_health_check_structure(client):
    """Verify health check returns expected structure for Render."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "environment" in data
    assert "version" in data
    assert data["status"] == "healthy"

@pytest.mark.integration
def test_production_config_loading():
    """Verify production keys in Settings."""
    # Settings are loaded at import time, so we just check the singleton
    assert hasattr(settings, "SENTRY_DSN")
    assert hasattr(settings, "ENVIRONMENT")
    
@pytest.mark.integration
def test_metrics_endpoint(client):
    """Verify Prometheus metrics endpoint is exposed."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "process_cpu_seconds_total" in response.text
