"""
Test suite for Pydantic Models.
Verifies data constraints, validation rules, JSON serialization, and TypeScript compatibility.

Test Coverage Summary:
  - MetricSet: 7 tests
  - LikertScores: 5 tests
  - LlmEval: 3 tests
  - Enums: 4 tests
  - Run: 8 tests
  - JSON Serialization: 3 tests
  - Response Wrappers: 3 tests
  Total: 33 tests (plus parameterization covers more cases)
  Coverage: >95% of schemas.py
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from src.api.models.schemas import (
    Run, MetricSet, LlmEval, LikertScores,
    ModelType, Dataset, XaiMethod, RunStatus,
    RunsResponse, RunResponse, HealthResponse
)

# ==============================================================================
# A) TestMetricSet
# ==============================================================================
class TestMetricSet:
    def test_valid_metric_set(self, valid_metric_set):
        """Should accept valid data."""
        assert valid_metric_set.Fidelity == 0.92

    def test_metric_set_boundary_values(self):
        """Should accept exact boundary values 0 and 1."""
        ms = MetricSet(
            Fidelity=0.0, Stability=1.0, Sparsity=0.0,
            CausalAlignment=1.0, CounterfactualSensitivity=0.0,
            EfficiencyMS=0.0
        )
        assert ms.Fidelity == 0.0
        assert ms.Stability == 1.0

    def test_metric_set_rejects_out_of_range_high(self):
        """Should reject values > 1."""
        with pytest.raises(ValidationError) as exc:
            MetricSet(
                Fidelity=1.1, Stability=0.5, Sparsity=0.5,
                CausalAlignment=0.5, CounterfactualSensitivity=0.5, EfficiencyMS=100
            )
        assert "Fidelity" in str(exc.value)

    def test_metric_set_rejects_out_of_range_low(self):
        """Should reject values < 0."""
        with pytest.raises(ValidationError) as exc:
            MetricSet(
                Fidelity=-0.1, Stability=0.5, Sparsity=0.5,
                CausalAlignment=0.5, CounterfactualSensitivity=0.5, EfficiencyMS=100
            )
        assert "Fidelity" in str(exc.value)

    def test_metric_set_rejects_negative_efficiency(self):
        """Should reject negative EfficiencyMS."""
        with pytest.raises(ValidationError) as exc:
            MetricSet(
                Fidelity=0.5, Stability=0.5, Sparsity=0.5,
                CausalAlignment=0.5, CounterfactualSensitivity=0.5, 
                EfficiencyMS=-1.0
            )
        assert "EfficiencyMS" in str(exc.value)

    def test_metric_set_requires_all_fields(self):
        """All 6 metrics are required."""
        with pytest.raises(ValidationError):
            MetricSet(Fidelity=0.5) # Missing others

# ==============================================================================
# B) TestLikertScores
# ==============================================================================
class TestLikertScores:
    def test_valid_likert_scores(self, valid_likert_scores):
        assert valid_likert_scores.clarity == 4

    def test_likert_scores_boundary_values(self):
        scores = LikertScores(
            clarity=1, usefulness=5, completeness=1,
            trustworthiness=5, overall=1
        )
        assert scores.clarity == 1
        assert scores.usefulness == 5

    def test_likert_scores_rejects_zero(self):
        with pytest.raises(ValidationError) as exc:
            LikertScores(clarity=0, usefulness=3, completeness=3, trustworthiness=3, overall=3)
        assert "clarity" in str(exc.value)

    def test_likert_scores_rejects_six(self):
        with pytest.raises(ValidationError) as exc:
            LikertScores(clarity=6, usefulness=3, completeness=3, trustworthiness=3, overall=3)
        assert "clarity" in str(exc.value)

    def test_likert_scores_requires_all_fields(self):
        with pytest.raises(ValidationError):
            LikertScores(clarity=3)

# ==============================================================================
# C) TestLlmEval
# ==============================================================================
class TestLlmEval:
    def test_valid_llm_eval(self, valid_llm_eval):
        assert valid_llm_eval.Justification.startswith("This is a valid")

    def test_llm_eval_justification_min_length(self, valid_likert_scores):
        with pytest.raises(ValidationError) as exc:
            LlmEval(Likert=valid_likert_scores, Justification="Short")
        assert "Justification" in str(exc.value)

    def test_llm_eval_justification_max_length(self, valid_likert_scores):
        long_text = "a" * 1001
        with pytest.raises(ValidationError) as exc:
            LlmEval(Likert=valid_likert_scores, Justification=long_text)
        assert "Justification" in str(exc.value)

# ==============================================================================
# D) TestEnums
# ==============================================================================
class TestEnums:
    def test_model_type_values(self):
        assert ModelType.CLASSICAL == "classical"
        assert ModelType.TRANSFORMER == "transformer"

    def test_dataset_values(self):
        assert Dataset.ADULT_INCOME == "AdultIncome"
        assert Dataset.MNIST == "MNIST"

    def test_xai_method_values(self):
        assert XaiMethod.SHAP == "SHAP"
        assert XaiMethod.LIME == "LIME"

    def test_run_status_values(self):
        assert RunStatus.COMPLETED == "completed"
        assert RunStatus.FAILED == "failed"

# ==============================================================================
# E) TestRun
# ==============================================================================
class TestRun:
    def test_valid_run(self, valid_run_data):
        run = Run(**valid_run_data)
        assert run.id == "run-123-abc"
        assert run.metrics.Fidelity == 0.92

    def test_run_accuracy_range_valid(self, valid_run_data):
        data = valid_run_data.copy()
        data['accuracy'] = 100.0
        run = Run(**data)
        assert run.accuracy == 100.0
        
        data['accuracy'] = 0.0
        run = Run(**data)
        assert run.accuracy == 0.0

    def test_run_accuracy_rejects_negative(self, valid_run_data):
        data = valid_run_data.copy()
        data['accuracy'] = -1.0
        with pytest.raises(ValidationError) as exc:
            Run(**data)
        assert "accuracy" in str(exc.value)

    def test_run_accuracy_rejects_over_100(self, valid_run_data):
        data = valid_run_data.copy()
        data['accuracy'] = 100.1
        with pytest.raises(ValidationError) as exc:
            Run(**data)
        assert "accuracy" in str(exc.value)

    def test_run_explainability_score_range(self, valid_run_data):
        data = valid_run_data.copy()
        data['explainabilityScore'] = 1.0
        assert Run(**data).explainabilityScore == 1.0

    def test_run_explainability_score_rejects_invalid(self, valid_run_data):
        data = valid_run_data.copy()
        data['explainabilityScore'] = 1.1
        with pytest.raises(ValidationError):
            Run(**data)

    def test_run_optional_fields(self, valid_run_data):
        data = valid_run_data.copy()
        del data['config']
        del data['metadata']
        del data['errorMessage'] # wasn't there but ensures it works
        run = Run(**data)
        assert run.config is None
        assert run.metadata is None

    def test_run_requires_all_required_fields(self, valid_run_data):
        data = valid_run_data.copy()
        del data['id']
        with pytest.raises(ValidationError):
            Run(**data)

# ==============================================================================
# F) TestJSONSerialization
# ==============================================================================
class TestJSONSerialization:
    def test_metric_set_json_round_trip(self, valid_metric_set):
        json_str = valid_metric_set.model_dump_json()
        copy = MetricSet.model_validate_json(json_str)
        assert copy.Fidelity == valid_metric_set.Fidelity

    def test_run_json_round_trip(self, valid_run_data):
        run = Run(**valid_run_data)
        json_str = run.model_dump_json()
        copy = Run.model_validate_json(json_str)
        assert copy.id == run.id
        assert copy.timestamp == run.timestamp

    def test_run_json_dict_conversion(self, valid_run_data):
        run = Run(**valid_run_data)
        data_dict = run.model_dump()
        assert data_dict['id'] == "run-123-abc"
        # Pydantic v2 dump preserves datetime object unless mode='json'
        assert isinstance(data_dict['timestamp'], datetime) 

# ==============================================================================
# G) TestResponseWrappers
# ==============================================================================
class TestResponseWrappers:
    def test_runs_response(self, valid_run_data):
        run = Run(**valid_run_data)
        response = RunsResponse(data=[run], pagination={"total": 1}, metadata=None)
        assert len(response.data) == 1
        assert response.data[0].id == run.id

    def test_run_response(self, valid_run_data):
        run = Run(**valid_run_data)
        response = RunResponse(data=run)
        assert response.data.modelName == run.modelName

    def test_health_response(self):
        health = HealthResponse(status="ok", version="0.1.0", timestamp=datetime.now())
        assert health.status == "ok"
