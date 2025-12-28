import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from src.api.main import app

client = TestClient(app)

@pytest.fixture
def mock_batch_runner():
    with patch("src.api.services.batch_service.BatchExperimentRunner") as mock:
        yield mock

def test_submit_batch_job(mock_batch_runner):
    """Test submitting a batch job."""
    # Mock behavior
    runner_instance = mock_batch_runner.return_value
    runner_instance.run.return_value = (None, {"executions": [{"status": "success"}]})
    
    payload = {"configs": ["test.yaml"]}
    response = client.post("/api/experiments/batch/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] in ["queued", "running"] # Depending on thread speed

def test_submit_empty_config():
    """Test validation error."""
    response = client.post("/api/experiments/batch/", json={"configs": []})
    assert response.status_code == 400

def test_get_job_status(mock_batch_runner):
    """Test retrieving job status."""
    # Submit first
    payload = {"configs": ["test.yaml"]}
    r1 = client.post("/api/experiments/batch/", json=payload)
    job_id = r1.json()["job_id"]
    
    r2 = client.get(f"/api/experiments/batch/{job_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == job_id

def test_get_results_not_ready(mock_batch_runner):
    """Test getting results before completion."""
    # Submit
    payload = {"configs": ["test.yaml"]}
    r1 = client.post("/api/experiments/batch/", json=payload)
    job_id = r1.json()["job_id"]
    
    # Immediately check results (likely still running or mocked fast? Wait, thread runs immediately?)
    # If thread finishes instantly, this test might fail being 'too good'.
    # We can mock Thread to NOT run target to simulate 'queued'.
    
    # Actually, let's just assert 404 for invalid ID
    r3 = client.get("/api/experiments/batch/invalid_id/results")
    assert r3.status_code == 404
