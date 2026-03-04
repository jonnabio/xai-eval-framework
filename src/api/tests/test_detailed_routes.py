import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.main import app
from src.api.services.data_loader import get_experiment_result

client = TestClient(app)

# Sample Data
SAMPLE_EXP_DATA = {
    "experiment_metadata": {
        "name": "test_model_v1",
        "dataset": "adult",
        "timestamp": "2023-01-01T12:00:00",
        "duration_seconds": 10.0
    },
    "model_info": {
        "name": "test_model",
        "explainer_method": "shap"
    },
    "metrics": {"fidelity": 0.8}, # Top level metrics
    "instance_evaluations": [
        {
            "instance_id": i,
            "metrics": {"fidelity": 0.9, "stability": 0.8},
            "explanation": {"feature": "value"}
        }
        for i in range(150) # Create 150 instances to test pagination
    ]
}

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear lru_cache before each test to ensure fresh mocks."""
    get_experiment_result.cache_clear()
    yield

def test_get_run_details_success():
    """Test retrieving detailed experiment results."""
    with patch("src.api.services.data_loader.load_all_experiments") as mock_load:
        mock_load.return_value = [SAMPLE_EXP_DATA]
        
        # We need the ID. We can simulate matching logic or just inspect the calls.
        # But to call the API we need the ID.
        # Let's get the ID by using the transformer momentarily
        from src.api.services.transformer import transform_experiment_to_run
        run = transform_experiment_to_run(SAMPLE_EXP_DATA)
        run_id = run.id
        
        response = client.get(f"/api/runs/{run_id}/details")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["metadata"]["name"] == "test_model_v1"
        assert len(data["data"]["instance_evaluations"]) == 150

def test_get_run_details_not_found():
    """Test 404 when run ID does not exist."""
    with patch("src.api.services.data_loader.load_all_experiments") as mock_load:
        mock_load.return_value = [SAMPLE_EXP_DATA]
        
        response = client.get("/api/runs/non_existent_id/details")
        assert response.status_code == 404

def test_get_instances_pagination_default():
    """Test instances pagination with default limits."""
    with patch("src.api.services.data_loader.load_all_experiments") as mock_load:
        mock_load.return_value = [SAMPLE_EXP_DATA]
        from src.api.services.transformer import transform_experiment_to_run
        run_id = transform_experiment_to_run(SAMPLE_EXP_DATA).id
        
        # Default limit is 50
        response = client.get(f"/api/runs/{run_id}/instances")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 50
        assert data["pagination"]["total"] == 150
        assert data["pagination"]["hasNext"] is True

def test_get_instances_pagination_custom():
    """Test instances pagination with custom offset and limit."""
    with patch("src.api.services.data_loader.load_all_experiments") as mock_load:
        mock_load.return_value = [SAMPLE_EXP_DATA]
        from src.api.services.transformer import transform_experiment_to_run
        run_id = transform_experiment_to_run(SAMPLE_EXP_DATA).id
        
        # Get 20 items starting from 50 (50-69)
        response = client.get(f"/api/runs/{run_id}/instances?offset=50&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 20
        assert data["data"][0]["instance_id"] == 50
        assert data["pagination"]["offset"] == 50

def test_get_instances_boundary_conditions():
    """Test pagination beyond available items."""
    with patch("src.api.services.data_loader.load_all_experiments") as mock_load:
        mock_load.return_value = [SAMPLE_EXP_DATA]
        from src.api.services.transformer import transform_experiment_to_run
        run_id = transform_experiment_to_run(SAMPLE_EXP_DATA).id
        
        # Offset beyond total
        response = client.get(f"/api/runs/{run_id}/instances?offset=200&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0
        assert data["pagination"]["total"] == 150

def test_malformed_json_handling():
    """Test handling of experiments that fail transformation."""
    # This effectively tests the try-catch block in get_experiment_result
    bad_data = {"broken": "data"} # Missing metadata etc to cause transformer error
    
    with patch("src.api.services.data_loader.load_all_experiments") as mock_load:
        mock_load.return_value = [bad_data, SAMPLE_EXP_DATA] # One bad, one good
        
        from src.api.services.transformer import transform_experiment_to_run
        good_id = transform_experiment_to_run(SAMPLE_EXP_DATA).id
        
        # Good one should still work (skipping bad one)
        response = client.get(f"/api/runs/{good_id}/details")
        assert response.status_code == 200
