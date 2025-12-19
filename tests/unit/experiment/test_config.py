"""Unit tests for experiment configuration."""

import pytest
from pathlib import Path
from pydantic import ValidationError

from src.experiment.config import (
    ModelConfig,
    ExplainerConfig,
    SamplingConfig,
    MetricsConfig,
    ExperimentConfig,
    load_config
)

def test_model_config_valid():
    """Test valid model configuration."""
    config = ModelConfig(
        name="random_forest",
        path=Path("outputs/models/adult/random_forest.pkl")
    )
    assert config.name == "random_forest"

def test_explainer_config_shap():
    """Test SHAP explainer configuration."""
    config = ExplainerConfig(
        method="shap",
        explainer_type="tree",
        params={"feature_perturbation": "tree_path_dependent"}
    )
    assert config.method == "shap"
    assert config.explainer_type == "tree"

def test_explainer_config_lime():
    """Test LIME explainer configuration."""
    config = ExplainerConfig(
        method="lime",
        num_samples=1000,
        num_features=10
    )
    assert config.method == "lime"
    assert config.num_samples == 1000

def test_sampling_config_defaults():
    """Test sampling configuration with defaults."""
    config = SamplingConfig()
    assert config.strategy == "stratified"
    assert config.samples_per_class == 25
    assert config.random_seed == 42

def test_metrics_config_all_enabled():
    """Test metrics configuration with all enabled."""
    config = MetricsConfig(
        fidelity=True,
        stability=True,
        sparsity=True,
        cost=True,
        stability_perturbations=10,
        stability_noise_level=0.1
    )
    assert all([config.fidelity, config.stability, config.sparsity, config.cost])

def test_experiment_config_full():
    """Test complete experiment configuration."""
    config = ExperimentConfig(
        name="test_exp",
        description="Test experiment",
        dataset="adult",
        model=ModelConfig(
            name="random_forest",
            path=Path("outputs/models/adult/random_forest.pkl")
        ),
        explainer=ExplainerConfig(
            method="shap",
            explainer_type="tree"
        ),
        sampling=SamplingConfig(),
        metrics=MetricsConfig(
            stability_perturbations=10,
            stability_noise_level=0.1
        )
    )
    assert config.name == "test_exp"
    assert config.version == "1.0.0"

def test_experiment_config_validation_error():
    """Test configuration validation catches errors."""
    with pytest.raises(ValidationError):
        ExperimentConfig(
            name="test",
            dataset="adult",
            # Missing required fields
        )

def test_load_config_file_not_found():
    """Test loading non-existent config file."""
    with pytest.raises(FileNotFoundError):
        load_config(Path("nonexistent.yaml"))
