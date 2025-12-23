import pytest
from datetime import datetime
from src.api.models.schemas import (
    MetricSet, LikertScores, LlmEval, Run,
    ModelType, Dataset, XaiMethod, RunStatus
)

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
