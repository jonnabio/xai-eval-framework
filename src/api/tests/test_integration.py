"""
Integration tests for XAI Evaluation API.

These tests verify the complete API workflow end-to-end:
- Request → Data Loading → Transformation → Response
- Use real sample data (not mocks)
- Test actual system behavior

Run with: pytest src/api/tests/test_integration.py -v
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

# Mark all tests in this file as integration tests
pytestmark = pytest.mark.integration

@pytest.fixture(scope="module")
def client():
    """Test client for all integration tests."""
    return TestClient(app)

class TestHealthCheckIntegration:
    """Integration tests for health check endpoints."""
    
    def test_health_endpoint_accessible(self, client):
        """Test health endpoint is accessible and returns 200."""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_health_response_format(self, client):
        """Test health endpoint returns correct format."""
        response = client.get("/api/health")
        data = response.json()
        
        # Verify all expected fields present
        assert "status" in data
        assert "version" in data
        assert "timestamp" in data
        
        # Verify field types
        assert isinstance(data["status"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["timestamp"], str)
    
    def test_detailed_health_includes_system_info(self, client):
        """Test detailed health endpoint includes system information."""
        response = client.get("/api/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "system" in data
        assert "experiments_directory" in data["system"]
        assert "experiments_directory_exists" in data["system"]

class TestDataLoadingIntegration:
    """Integration tests for data loading workflow."""
    
    def test_api_loads_sample_data(self, client, ensure_sample_data_exists):
        """Test API successfully loads sample experiment data."""
        response = client.get("/api/runs")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have loaded sample data
        assert "data" in data
        assert len(data["data"]) > 0
        print(f"Loaded {len(data['data'])} experiments from sample data")
    
    def test_loaded_data_has_correct_structure(self, client, ensure_sample_data_exists):
        """Test loaded data matches Run model structure."""
        response = client.get("/api/runs?limit=1")
        
        assert response.status_code == 200
        data = response.json()
        
        # Get first run
        assert len(data["data"]) > 0
        run = data["data"][0]
        
        # Verify Run model fields
        required_fields = [
            "id", "modelName", "modelType", "dataset", "method",
            "accuracy", "explainabilityScore", "processingTime",
            "status", "timestamp", "metrics", "llmEval"
        ]
        
        for field in required_fields:
            assert field in run, f"Missing required field: {field}"
    
    def test_loaded_data_metrics_valid(self, client, ensure_sample_data_exists):
        """Test loaded data has valid metric values."""
        response = client.get("/api/runs?limit=1")
        data = response.json()
        
        run = data["data"][0]
        metrics = run["metrics"]
        
        # Verify all 6 metrics present
        metric_fields = [
            "Fidelity", "Stability", "Sparsity",
            "CausalAlignment", "CounterfactualSensitivity", "EfficiencyMS"
        ]
        
        for field in metric_fields:
            assert field in metrics, f"Missing metric: {field}"
        
        # Verify metric ranges
        assert 0 <= metrics["Fidelity"] <= 1
        assert 0 <= metrics["Stability"] <= 1
        assert 0 <= metrics["Sparsity"] <= 1
        assert metrics["EfficiencyMS"] >= 0
    
    def test_loaded_data_llm_eval_valid(self, client, ensure_sample_data_exists):
        """Test loaded data has valid LLM evaluation."""
        response = client.get("/api/runs?limit=1")
        data = response.json()
        
        run = data["data"][0]
        llm_eval = run["llmEval"]
        
        # Verify structure
        assert "Likert" in llm_eval
        assert "Justification" in llm_eval
        
        # Verify Likert scores
        likert = llm_eval["Likert"]
        score_fields = ["clarity", "usefulness", "completeness", "trustworthiness", "overall"]
        
        for field in score_fields:
            assert field in likert
            assert 1 <= likert[field] <= 5
        
        # Verify justification
        assert len(llm_eval["Justification"]) >= 10

class TestFilteringIntegration:
    """Integration tests for filtering functionality."""
    
    def test_filter_by_method_lime(self, client, ensure_sample_data_exists):
        """Test filtering by method=LIME returns only LIME experiments."""
        response = client.get("/api/runs?method=LIME")
        
        assert response.status_code == 200
        data = response.json()
        
        # All returned runs should have method=LIME
        for run in data["data"]:
            assert run["method"] == "LIME"
    
    def test_filter_by_method_shap(self, client, ensure_sample_data_exists):
        """Test filtering by method=SHAP returns only SHAP experiments."""
        response = client.get("/api/runs?method=SHAP")
        
        assert response.status_code == 200
        data = response.json()
        
        # All returned runs should have method=SHAP
        for run in data["data"]:
            assert run["method"] == "SHAP"
    
    def test_filter_by_dataset(self, client, ensure_sample_data_exists):
        """Test filtering by dataset works correctly."""
        response = client.get("/api/runs?dataset=AdultIncome")
        
        assert response.status_code == 200
        data = response.json()
        
        # All returned runs should have dataset=AdultIncome
        for run in data["data"]:
            assert run["dataset"] == "AdultIncome"
    
    def test_filter_by_model_type(self, client, ensure_sample_data_exists):
        """Test filtering by model type works correctly."""
        response = client.get("/api/runs?model_type=classical")
        
        assert response.status_code == 200
        data = response.json()
        
        # All returned runs should have modelType=classical
        for run in data["data"]:
            assert run["modelType"] == "classical"
    
    def test_filter_by_model_name(self, client, ensure_sample_data_exists):
        """Test filtering by model name works correctly."""
        response = client.get("/api/runs?model_name=random_forest")
        
        assert response.status_code == 200
        data = response.json()
        
        # All returned runs should contain 'random_forest' in name
        for run in data["data"]:
            assert "random_forest" in run["modelName"].lower()
    
    def test_multiple_filters_combined(self, client, ensure_sample_data_exists):
        """Test combining multiple filters with AND logic."""
        response = client.get("/api/runs?dataset=AdultIncome&method=LIME")
        
        assert response.status_code == 200
        data = response.json()
        
        # All runs should match both filters
        for run in data["data"]:
            assert run["dataset"] == "AdultIncome"
            assert run["method"] == "LIME"
    
    def test_filter_returns_empty_for_no_matches(self, client, ensure_sample_data_exists):
        """Test filtering returns empty list when no matches."""
        response = client.get("/api/runs?dataset=NonExistent")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return empty data array
        assert len(data["data"]) == 0
        assert data["pagination"]["total"] == 0

class TestPaginationIntegration:
    """Integration tests for pagination functionality."""
    
    def test_pagination_metadata_present(self, client, ensure_sample_data_exists):
        """Test pagination metadata is included in response."""
        response = client.get("/api/runs")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify pagination object present
        assert "pagination" in data
        pagination = data["pagination"]
        
        # Verify all pagination fields
        assert "total" in pagination
        assert "limit" in pagination
        assert "offset" in pagination
        assert "returned" in pagination
        assert "hasNext" in pagination
        assert "hasPrev" in pagination
    
    def test_pagination_limit_works(self, client, ensure_sample_data_exists):
        """Test limit parameter controls number of results."""
        response = client.get("/api/runs?limit=2")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return at most 2 results
        assert len(data["data"]) <= 2
        assert data["pagination"]["limit"] == 2
        assert data["pagination"]["returned"] == len(data["data"])
    
    def test_pagination_offset_works(self, client, ensure_sample_data_exists):
        """Test offset parameter skips results."""
        # Get first page
        response1 = client.get("/api/runs?limit=2&offset=0")
        data1 = response1.json()
        
        # Get second page
        response2 = client.get("/api/runs?limit=2&offset=2")
        data2 = response2.json()
        
        # If we have enough data, IDs should be different
        if len(data1["data"]) > 0 and len(data2["data"]) > 0:
            assert data1["data"][0]["id"] != data2["data"][0]["id"]
    
    def test_pagination_has_next_when_more_results(self, client, ensure_sample_data_exists):
        """Test hasNext is true when more results available."""
        response = client.get("/api/runs?limit=1")
        data = response.json()
        
        # If total > limit, should have next page
        if data["pagination"]["total"] > 1:
            assert data["pagination"]["hasNext"] is True
    
    def test_pagination_has_prev_when_offset_greater_than_zero(self, client, ensure_sample_data_exists):
        """Test hasPrev is true when offset > 0."""
        response = client.get("/api/runs?limit=2&offset=2")
        data = response.json()
        
        # offset > 0 means there's a previous page
        assert data["pagination"]["hasPrev"] is True
    
    def test_pagination_total_consistent(self, client, ensure_sample_data_exists):
        """Test total count is consistent across pages."""
        response1 = client.get("/api/runs?limit=1&offset=0")
        data1 = response1.json()
        
        response2 = client.get("/api/runs?limit=1&offset=1")
        data2 = response2.json()
        
        # Total should be same for both pages
        assert data1["pagination"]["total"] == data2["pagination"]["total"]

class TestSingleRunIntegration:
    """Integration tests for single run retrieval."""
    
    def test_get_single_run_by_id(self, client, ensure_sample_data_exists):
        """Test retrieving single run by ID."""
        # First get a list to find a valid ID
        list_response = client.get("/api/runs?limit=1")
        list_data = list_response.json()
        
        if len(list_data["data"]) == 0:
            pytest.skip("No sample data available")
        
        run_id = list_data["data"][0]["id"]
        
        # Now get that specific run
        response = client.get(f"/api/runs/{run_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "data" in data
        assert data["data"]["id"] == run_id
    
    def test_get_single_run_returns_complete_data(self, client, ensure_sample_data_exists):
        """Test single run endpoint returns complete Run object."""
        # Get first run ID
        list_response = client.get("/api/runs?limit=1")
        list_data = list_response.json()
        
        if len(list_data["data"]) == 0:
            pytest.skip("No sample data available")
        
        run_id = list_data["data"][0]["id"]
        
        # Get single run
        response = client.get(f"/api/runs/{run_id}")
        data = response.json()
        
        run = data["data"]
        
        # Verify all major sections present
        assert "metrics" in run
        assert "llmEval" in run
        assert "config" in run or run.get("config") is None
    
    def test_get_nonexistent_run_returns_404(self, client):
        """Test requesting non-existent run returns 404."""
        response = client.get("/api/runs/nonexistent_id_xyz_123")
        
        assert response.status_code == 404
        data = response.json()
        
        # Should have error detail
        assert "detail" in data
        assert "not found" in data["detail"].lower()

class TestErrorHandlingIntegration:
    """Integration tests for error handling."""
    
    def test_invalid_limit_returns_validation_error(self, client):
        """Test invalid limit parameter returns 400 (Custom Handler)."""
        response = client.get("/api/runs?limit=0")
        
        # Note: Custom Exception Handler returns 400, not 422
        assert response.status_code == 400
    
    def test_negative_offset_returns_validation_error(self, client):
        """Test negative offset returns 400 (Custom Handler)."""
        response = client.get("/api/runs?offset=-1")
        
        assert response.status_code == 400
    
    def test_limit_exceeding_max_returns_validation_error(self, client):
        """Test limit exceeding maximum returns 400 (Custom Handler)."""
        response = client.get("/api/runs?limit=1000")
        
        assert response.status_code == 400
    
    def test_invalid_endpoint_returns_404(self, client):
        """Test accessing non-existent endpoint returns 404."""
        response = client.get("/api/nonexistent")
        
        assert response.status_code == 404
    
    def test_cors_headers_present(self, client):
        """Test CORS headers are present in responses."""
        response = client.get(
            "/api/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers

class TestEndToEndWorkflow:
    """Integration tests for complete workflows."""
    
    def test_complete_list_filter_paginate_workflow(self, client, ensure_sample_data_exists):
        """Test complete workflow: list → filter → paginate."""
        # Step 1: Get all runs
        response1 = client.get("/api/runs")
        assert response1.status_code == 200
        total = response1.json()["pagination"]["total"]
        
        # Step 2: Filter by method
        response2 = client.get("/api/runs?method=LIME")
        assert response2.status_code == 200
        lime_total = response2.json()["pagination"]["total"]
        assert lime_total <= total
        
        # Step 3: Add pagination to filtered results
        response3 = client.get("/api/runs?method=LIME&limit=1")
        assert response3.status_code == 200
        data3 = response3.json()
        assert len(data3["data"]) <= 1
    
    def test_complete_list_to_detail_workflow(self, client, ensure_sample_data_exists):
        """Test complete workflow: list → select → detail."""
        # Step 1: Get list of runs
        list_response = client.get("/api/runs?limit=5")
        assert list_response.status_code == 200
        list_data = list_response.json()
        
        if len(list_data["data"]) == 0:
            pytest.skip("No sample data available")
        
        # Step 2: Pick a run from the list
        selected_run_id = list_data["data"][0]["id"]
        
        # Step 3: Get detailed view of that run
        detail_response = client.get(f"/api/runs/{selected_run_id}")
        assert detail_response.status_code == 200
        detail_data = detail_response.json()
        
        # Step 4: Verify it's the same run
        assert detail_data["data"]["id"] == selected_run_id
    
    def test_complete_dashboard_workflow(self, client, ensure_sample_data_exists):
        """Test complete workflow as dashboard would use it."""
        # Dashboard workflow:
        # 1. Check API health
        health_response = client.get("/api/health")
        assert health_response.status_code == 200
        
        # 2. Load initial runs (first page)
        runs_response = client.get("/api/runs?limit=20&offset=0")
        assert runs_response.status_code == 200
        runs_data = runs_response.json()
        
        # 3. Apply filter (user selects LIME)
        filtered_response = client.get("/api/runs?method=LIME&limit=20")
        assert filtered_response.status_code == 200
        
        # 4. Select specific run for details
        if len(runs_data["data"]) > 0:
            run_id = runs_data["data"][0]["id"]
            detail_response = client.get(f"/api/runs/{run_id}")
            assert detail_response.status_code == 200

def test_integration_suite_summary(ensure_sample_data_exists):
    """
    Summary of integration test suite.
    
    This test always passes and provides information about the suite.
    """
    from pathlib import Path
    
    sample_dir = Path("experiments/sample_data/results")
    json_files = list(sample_dir.glob("*.json"))
    
    print("\n" + "="*70)
    print("INTEGRATION TEST SUITE SUMMARY")
    print("="*70)
    print(f"Sample data location: {sample_dir}")
    print(f"Sample files available: {len(json_files)}")
    print("\nTest Coverage:")
    print("  ✓ Health check endpoints")
    print("  ✓ Data loading from filesystem")
    print("  ✓ Data transformation to Run models")
    print("  ✓ Filtering (dataset, method, model_type, model_name)")
    print("  ✓ Pagination (limit, offset, hasNext, hasPrev)")
    print("  ✓ Single run retrieval by ID")
    print("  ✓ Error handling (404, 400)")
    print("  ✓ CORS headers")
    print("  ✓ End-to-end workflows")
    print("="*70)
    
    assert True  # Always pass
