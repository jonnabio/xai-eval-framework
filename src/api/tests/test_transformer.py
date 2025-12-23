"""
Tests for Data Transformer Service.
Verifies logic for converting raw experiment data to API models.
"""
import pytest
import json
from pathlib import Path
from datetime import datetime

from src.api.services.transformer import (
    generate_run_id,
    map_model_type,
    map_dataset,
    map_xai_method,
    calculate_explainability_score,
    transform_experiment_to_run
)
from src.api.models.schemas import Run, ModelType, Dataset, XaiMethod, MetricSet

@pytest.fixture
def sample_experiment_data():
    """Load sample experiment JSON."""
    fixture_path = Path(__file__).parent / "fixtures" / "sample_experiment.json"
    with open(fixture_path) as f:
        return json.load(f)

# ==============================================================================
# A) TestGenerateRunId
# ==============================================================================
class TestGenerateRunId:
    def test_generate_run_id_format(self):
        """Test ID has correct format."""
        run_id = generate_run_id("rf", "LIME", "Adult", "2024-01-15T10:30:00")
        
        # Should be: dataset_model_method_hash
        parts = run_id.split("_")
        assert len(parts) == 4
        assert parts[0].lower() == "adult"
        assert "rf" in parts[1].lower()
        assert "lime" in parts[2].lower()
        assert len(parts[3]) == 6  # Hash is 6 chars

    def test_generate_run_id_deterministic(self):
        """Same inputs = same ID."""
        args = ("rf", "LIME", "Adult", "2024-01-15T10:30:00")
        id1 = generate_run_id(*args)
        id2 = generate_run_id(*args)
        assert id1 == id2

    def test_generate_run_id_unique(self):
        """Different timestamps = different IDs."""
        id1 = generate_run_id("rf", "LIME", "Adult", "2024-01-15T10:30:00")
        id2 = generate_run_id("rf", "LIME", "Adult", "2024-01-15T10:30:01")
        assert id1 != id2
        
    def test_generate_run_id_url_safe(self):
        """No special characters."""
        run_id = generate_run_id("My Model!", "LIME & SHAP", "Adult Dataset", "ts")
        assert " " not in run_id
        assert "&" not in run_id
        assert "!" not in run_id

# ==============================================================================
# B) TestMapModelType
# ==============================================================================
class TestMapModelType:
    def test_map_model_type_valid(self):
        assert map_model_type("classical") == ModelType.CLASSICAL
        assert map_model_type("cnn") == ModelType.CNN
    
    def test_map_model_type_case_insensitive(self):
        assert map_model_type("CLASSICAL") == ModelType.CLASSICAL
        assert map_model_type("Transformer") == ModelType.TRANSFORMER
        
    def test_map_model_type_mapped_values(self):
        assert map_model_type("random_forest") == ModelType.CLASSICAL
        assert map_model_type("bert") == ModelType.TRANSFORMER

    def test_map_model_type_invalid(self):
        with pytest.raises(ValueError):
            map_model_type("unknown_type_xyz")

# ==============================================================================
# C) TestMapDataset
# ==============================================================================
class TestMapDataset:
    def test_map_dataset_valid(self):
        assert map_dataset("AdultIncome") == Dataset.ADULT_INCOME
        assert map_dataset("CIFAR-10") == Dataset.CIFAR_10

    def test_map_dataset_case_handling(self):
        assert map_dataset("adultincome") == Dataset.ADULT_INCOME
        assert map_dataset("adult") == Dataset.ADULT_INCOME # From mapping

    def test_map_dataset_invalid(self):
        with pytest.raises(ValueError):
            map_dataset("unknown_dataset_xyz")

# ==============================================================================
# D) TestMapXaiMethod
# ==============================================================================
class TestMapXaiMethod:
    def test_map_xai_method_valid(self):
        assert map_xai_method("LIME") == XaiMethod.LIME
        assert map_xai_method("SHAP") == XaiMethod.SHAP
        
    def test_map_xai_method_case_sensitive(self):
        # Implementation is case-insensitive
        assert map_xai_method("lime") == XaiMethod.LIME
        assert map_xai_method("Lime") == XaiMethod.LIME

    def test_map_xai_method_invalid(self):
        with pytest.raises(ValueError):
            map_xai_method("unknown_method_xyz")

# ==============================================================================
# E) TestCalculateExplainabilityScore
# ==============================================================================
class TestCalculateExplainabilityScore:
    def test_calculate_score_valid(self):
        # Weights: Fid 0.3, Stab 0.25, Spar 0.2, Caus 0.15, Sens 0.1
        # 1.0 * (0.3+0.25+0.2+0.15+0.1) = 1.0
        metrics = MetricSet(
            Fidelity=1.0, Stability=1.0, Sparsity=1.0, 
            CausalAlignment=1.0, CounterfactualSensitivity=1.0, EfficiencyMS=0
        )
        assert calculate_explainability_score(metrics) == 1.0

    def test_calculate_score_all_half(self):
        metrics = MetricSet(
            Fidelity=0.5, Stability=0.5, Sparsity=0.5,
            CausalAlignment=0.5, CounterfactualSensitivity=0.5, EfficiencyMS=0
        )
        # Should be 0.5 * 1.0 sum of weights
        assert abs(calculate_explainability_score(metrics) - 0.5) < 0.0001
        
    def test_calculate_score_mixed(self):
        # Fid 1.0 * .3 = .3
        # Stab 0.0 * .25 = 0
        # Rest 0
        metrics = MetricSet(
            Fidelity=1.0, Stability=0.0, Sparsity=0.0,
            CausalAlignment=0.0, CounterfactualSensitivity=0.0, EfficiencyMS=0
        )
        assert abs(calculate_explainability_score(metrics) - 0.3) < 0.0001

    def test_calculate_score_range(self):
        # Use model_construct to bypass validation and test that calculation logic clamps to 1.0
        metrics = MetricSet.model_construct(
            Fidelity=1.5, Stability=1.5, Sparsity=1.5, 
            CausalAlignment=1.5, CounterfactualSensitivity=1.5, EfficiencyMS=0
        )
        assert calculate_explainability_score(metrics) == 1.0

# ==============================================================================
# F) TestTransformExperimentToRun
# ==============================================================================
class TestTransformExperimentToRun:
    def test_transform_complete_valid_data(self, sample_experiment_data):
        """Test complete transformation of valid data."""
        run = transform_experiment_to_run(sample_experiment_data)
        
        # Verify Run instance
        assert isinstance(run, Run)
        assert run.modelName == "random_forest"
        assert run.modelType == ModelType.CLASSICAL
        assert run.dataset == Dataset.ADULT_INCOME
        assert run.method == XaiMethod.LIME
        assert run.accuracy == 85.23
        
        # Verify metrics
        assert run.metrics.Fidelity == 0.92
        assert run.metrics.Stability == 0.88
        
        # Verify LLM eval
        assert run.llmEval.Likert.clarity == 4
        assert "clear insights" in run.llmEval.Justification
        
        # Verify calculated score
        assert 0 <= run.explainabilityScore <= 1
    
    def test_transform_field_mapping(self, sample_experiment_data):
        # model_name -> modelName
        run = transform_experiment_to_run(sample_experiment_data)
        assert run.modelName == sample_experiment_data["model_name"]
        assert run.processingTime == 125.5

    def test_transform_missing_required_field(self):
        """Test transformation fails with missing/invalid required data that causes internal error or validation error."""
        incomplete_data = {
            "model_name": "rf",
            # Missing mappings
        }
        
        with pytest.raises(Exception): # ValueError or KeyError or ValidationError
            transform_experiment_to_run(incomplete_data)

    def test_transform_default_accuracy(self, sample_experiment_data):
        # If accuracy missing, try test_accuracy
        data = sample_experiment_data.copy()
        del data["accuracy"]
        data["test_accuracy"] = 0.85 # Should become 85.0
        
        run = transform_experiment_to_run(data)
        assert run.accuracy == 85.0

    def test_transform_nested_instance_evaluations(self):
        # Test the aggregation logic which isn't in sample_experiment.json
        data = {
            "model_name": "rf",
            "model_type": "classical",
            "dataset": "adult",
            "xai_method": "shap",
            "timestamp": "2024-01-01",
            "instance_evaluations": [
                {"metrics": {"fidelity": 0.8, "stability": 0.8}},
                {"metrics": {"fidelity": 0.9, "stability": 0.9}},
            ]
        }
        run = transform_experiment_to_run(data)
        # Avg fidelity = 0.85
        assert abs(run.metrics.Fidelity - 0.85) < 0.0001
