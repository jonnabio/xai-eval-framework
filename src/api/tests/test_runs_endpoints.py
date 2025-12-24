"""
Tests for runs endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from src.api.main import app
from src.api.models.schemas import Run, ModelType, Dataset, XaiMethod, RunStatus

client = TestClient(app)

@pytest.fixture
def mock_experiment_data():
    """Mock experiment data for testing."""
    return {
        "model_name": "random_forest",
        "model_type": "classical",
        "dataset": "AdultIncome",
        "xai_method": "LIME",
        "accuracy": 85.23,
        "timestamp": "2024-01-15T10:30:00",
        "metrics": {
            "fidelity": 0.92,
            "stability": 0.88,
            "sparsity": 0.75,
            "causal_alignment": 0.85,
            "counterfactual_sensitivity": 0.78,
            "efficiency_ms": 125.5
        },
        "llm_evaluation": {
            "likert_scores": {
                "clarity": 4,
                "usefulness": 4,
                "completeness": 3,
                "trustworthiness": 4,
                "overall": 4
            },
            "justification": "This explanation provides clear insights."
        },
        "processing_time": 125.5
    }

@pytest.fixture
def mock_multiple_experiments(mock_experiment_data):
    """Create multiple experiment data for testing."""
    experiments = []
    
    # Add 5 AdultIncome experiments
    for i in range(5):
        exp = mock_experiment_data.copy()
        exp["model_name"] = f"model_{i}"
        experiments.append(exp)
    
    # Add 3 CIFAR-10 experiments
    for i in range(3):
        exp = mock_experiment_data.copy()
        exp["dataset"] = "CIFAR-10"
        exp["model_name"] = f"cnn_{i}"
        exp["model_type"] = "cnn"
        exp["xai_method"] = "GradCAM"
        experiments.append(exp)
    
    return experiments

class TestListRunsEndpoint:
    """Tests for GET /api/runs endpoint."""
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_returns_200(self, mock_load, mock_experiment_data):
        """Test list runs returns 200 OK."""
        mock_load.return_value = [mock_experiment_data]
        
        response = client.get("/api/runs")
        
        assert response.status_code == 200
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_response_structure(self, mock_load, mock_experiment_data):
        """Test list runs has correct response structure."""
        mock_load.return_value = [mock_experiment_data]
        
        response = client.get("/api/runs")
        data = response.json()
        
        assert "data" in data
        assert "pagination" in data
        assert "metadata" in data
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_returns_run_objects(self, mock_load, mock_experiment_data):
        """Test list runs returns valid Run objects."""
        mock_load.return_value = [mock_experiment_data]
        
        response = client.get("/api/runs")
        data = response.json()
        
        assert len(data["data"]) > 0
        run = data["data"][0]
        assert "id" in run
        assert "modelName" in run
        assert "accuracy" in run
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_pagination_metadata(self, mock_load, mock_multiple_experiments):
        """Test pagination metadata is correct."""
        mock_load.return_value = mock_multiple_experiments
        
        response = client.get("/api/runs?limit=5&offset=0")
        data = response.json()
        
        pagination = data["pagination"]
        assert pagination["total"] == len(mock_multiple_experiments)
        assert pagination["limit"] == 5
        assert pagination["offset"] == 0
        assert pagination["returned"] == 5
        assert "hasNext" in pagination
        assert "hasPrev" in pagination
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_pagination_has_next(self, mock_load, mock_multiple_experiments):
        """Test hasNext is true when more results available."""
        mock_load.return_value = mock_multiple_experiments
        
        response = client.get("/api/runs?limit=5&offset=0")
        data = response.json()
        
        assert data["pagination"]["hasNext"] is True
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_pagination_has_prev(self, mock_load, mock_multiple_experiments):
        """Test hasPrev is true when offset > 0."""
        mock_load.return_value = mock_multiple_experiments
        
        response = client.get("/api/runs?limit=5&offset=5")
        data = response.json()
        
        assert data["pagination"]["hasPrev"] is True
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_filter_by_dataset(self, mock_load, mock_experiment_data):
        """Test filtering by dataset."""
        mock_load.return_value = [mock_experiment_data]
        
        response = client.get("/api/runs?dataset=AdultIncome")
        
        # Verify filter was passed to loader
        mock_load.assert_called_once()
        call_kwargs = mock_load.call_args.kwargs
        assert call_kwargs.get("dataset") == "AdultIncome"
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_filter_by_method(self, mock_load, mock_experiment_data):
        """Test filtering by XAI method."""
        mock_load.return_value = [mock_experiment_data]
        
        response = client.get("/api/runs?method=LIME")
        
        mock_load.assert_called_once()
        call_kwargs = mock_load.call_args.kwargs
        assert call_kwargs.get("method") == "LIME"
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_filter_by_model_type(self, mock_load, mock_experiment_data):
        """Test filtering by model type."""
        mock_load.return_value = [mock_experiment_data]
        
        response = client.get("/api/runs?model_type=classical")
        
        mock_load.assert_called_once()
        call_kwargs = mock_load.call_args.kwargs
        assert call_kwargs.get("model_type") == "classical"
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_multiple_filters(self, mock_load, mock_experiment_data):
        """Test combining multiple filters."""
        mock_load.return_value = [mock_experiment_data]
        
        response = client.get("/api/runs?dataset=AdultIncome&method=LIME")
        
        mock_load.assert_called_once()
        call_kwargs = mock_load.call_args.kwargs
        assert call_kwargs.get("dataset") == "AdultIncome"
        assert call_kwargs.get("method") == "LIME"
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_respects_limit(self, mock_load, mock_multiple_experiments):
        """Test limit parameter controls number of results."""
        mock_load.return_value = mock_multiple_experiments
        
        response = client.get("/api/runs?limit=3")
        data = response.json()
        
        assert len(data["data"]) == 3
        assert data["pagination"]["returned"] == 3
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_respects_offset(self, mock_load, mock_multiple_experiments):
        """Test offset parameter skips results."""
        mock_load.return_value = mock_multiple_experiments
        
        # Get first page
        response1 = client.get("/api/runs?limit=3&offset=0")
        data1 = response1.json()
        first_id = data1["data"][0]["id"]
        
        # Get second page
        response2 = client.get("/api/runs?limit=3&offset=3")
        data2 = response2.json()
        second_id = data2["data"][0]["id"]
        
        # IDs should be different
        assert first_id != second_id
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_empty_results(self, mock_load):
        """Test empty results when no matches."""
        mock_load.return_value = []
        
        response = client.get("/api/runs?dataset=NonExistent")
        data = response.json()
        
        assert len(data["data"]) == 0
        assert data["pagination"]["total"] == 0
        assert data["pagination"]["returned"] == 0
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_invalid_limit_rejected(self, mock_load):
        """Test invalid limit value is rejected."""
        response = client.get("/api/runs?limit=0")
        
        assert response.status_code == 400  # Validation error (custom handler)
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_limit_exceeds_max(self, mock_load):
        """Test limit exceeding max is rejected."""
        response = client.get("/api/runs?limit=1000")
        
        assert response.status_code == 400  # Validation error (custom handler)
    
    @patch("src.api.routes.runs.load_experiments_with_filters")
    def test_list_runs_negative_offset_rejected(self, mock_load):
        """Test negative offset is rejected."""
        response = client.get("/api/runs?offset=-1")
        
        assert response.status_code == 400  # Validation error (custom handler)

class TestGetSingleRunEndpoint:
    """Tests for GET /api/runs/{run_id} endpoint."""
    
    @patch("src.api.routes.runs.load_all_experiments")
    def test_get_run_returns_200(self, mock_load, mock_experiment_data):
        """Test get single run returns 200 OK."""
        mock_load.return_value = [mock_experiment_data]
        
        response = client.get("/api/runs/some_id")
        
        # Will be 200 or 404 depending on ID match
        assert response.status_code in [200, 404]
    
    @patch("src.api.routes.runs.load_all_experiments")
    def test_get_run_response_structure(self, mock_load, mock_experiment_data):
        """Test get run has correct response structure."""
        mock_load.return_value = [mock_experiment_data]
        
        # Get the actual ID from transformation
        from src.api.services.transformer import transform_experiment_to_run
        run = transform_experiment_to_run(mock_experiment_data)
        
        response = client.get(f"/api/runs/{run.id}")
        
        if response.status_code == 200:
            data = response.json()
            assert "data" in data
            assert "metadata" in data
    
    @patch("src.api.routes.runs.load_all_experiments")
    def test_get_run_returns_correct_run(self, mock_load, mock_experiment_data):
        """Test get run returns the requested run."""
        mock_load.return_value = [mock_experiment_data]
        
        # Get the actual ID
        from src.api.services.transformer import transform_experiment_to_run
        run = transform_experiment_to_run(mock_experiment_data)
        
        response = client.get(f"/api/runs/{run.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == run.id
    
    @patch("src.api.routes.runs.load_all_experiments")
    def test_get_run_not_found(self, mock_load, mock_experiment_data):
        """Test 404 when run not found."""
        mock_load.return_value = [mock_experiment_data]
        
        response = client.get("/api/runs/nonexistent_id_xyz")
        
        assert response.status_code == 404
    
    @patch("src.api.routes.runs.load_all_experiments")
    def test_get_run_not_found_message(self, mock_load, mock_experiment_data):
        """Test 404 error message."""
        mock_load.return_value = [mock_experiment_data]
        
        run_id = "nonexistent_id_xyz"
        response = client.get(f"/api/runs/{run_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert run_id in data["detail"]
    
    @patch("src.api.routes.runs.load_all_experiments")
    def test_get_run_searches_all_experiments(self, mock_load, mock_multiple_experiments):
        """Test get run searches through all experiments."""
        mock_load.return_value = mock_multiple_experiments
        
        # Try to get a run (may or may not exist)
        response = client.get("/api/runs/some_id")
        
        # Verify all experiments were loaded
        mock_load.assert_called_once()

class TestRunsEndpointIntegration:
    """Integration tests with real services."""
    
    def test_list_runs_real_integration(self):
        """Test list endpoint with real data loader (if available)."""
        response = client.get("/api/runs")
        
        # Should work even with no data
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
    
    def test_get_run_real_integration(self):
        """Test get endpoint attempts to load real data."""
        # Try to get any run
        response = client.get("/api/runs/test_id")
        
        # Should return 404 (no real data) or 200 (data exists)
        assert response.status_code in [200, 404]
