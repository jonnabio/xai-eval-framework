import pytest
from datetime import datetime
from src.api.models.schemas import (
    MetricSet, LikertScores, LlmEval, Run,
    ModelType, Dataset, XaiMethod, RunStatus
)
from src.api.main import app
from fastapi.testclient import TestClient
from pathlib import Path

@pytest.fixture
def valid_metric_set():
    """Returns a valid MetricSet instance with all metrics populated."""
    return MetricSet(
        Fidelity=0.92,
        Stability=0.88,
        Sparsity=0.75,
        CausalAlignment=0.85,
        CounterfactualSensitivity=0.78,
        EfficiencyMS=125.5
    )

@pytest.fixture
def valid_likert_scores():
    """Returns a valid LikertScores instance."""
    return LikertScores(
        clarity=4,
        usefulness=4,
        completeness=3,
        trustworthiness=4,
        overall=4
    )

@pytest.fixture
def valid_llm_eval(valid_likert_scores):
    """Returns a valid LlmEval instance."""
    return LlmEval(
        Likert=valid_likert_scores,
        Justification="This is a valid justification text that meets the minimum length requirement."
    )

@pytest.fixture
def valid_run_data(valid_metric_set, valid_llm_eval):
    """Returns a dictionary with complete valid Run data."""
    return {
        "id": "run-123-abc",
        "modelName": "RandomForest_Classifier",
        "modelType": ModelType.CLASSICAL,
        "dataset": Dataset.ADULT_INCOME,
        "method": XaiMethod.SHAP,
        "accuracy": 88.5,
        "explainabilityScore": 0.85,
        "processingTime": 1500.0,
        "status": RunStatus.COMPLETED,
        "timestamp": datetime.now(),
        "metrics": valid_metric_set,
        "llmEval": valid_llm_eval,
        "config": {"max_depth": 10},
        "errorMessage": None,
        "metadata": {"version": "1.0.0"}
    }

@pytest.fixture(scope="session")
def test_client():
    """
    FastAPI test client for integration tests.
    
    Scope: session - created once for all tests
    """
    return TestClient(app)

@pytest.fixture(scope="session")
def sample_data_path():
    """
    Path to sample experiment data.
    
    Returns path to experiments/sample_data directory.
    """
    return Path("experiments/exp1_adult")

@pytest.fixture(scope="session")
def ensure_sample_data_exists(sample_data_path):
    """
    Verify sample data exists before running integration tests.
    
    Raises error if sample data directory doesn't exist.
    """
    results_dir = sample_data_path / "results"
    
    if not results_dir.exists():
        pytest.fail(
            f"Sample data not found at {results_dir}. "
            f"Run INT-10 to create sample data."
        )
    
    json_files = list(results_dir.glob("*.json"))
    if len(json_files) == 0:
        pytest.fail(
            f"No JSON files found in {results_dir}. "
            f"Run INT-10 to create sample data."
        )
    
    return results_dir
