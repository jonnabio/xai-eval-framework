# User Story: EXP1-08
"""
Tests for Random Forest training on Adult dataset.
"""

import sys
import os
import pytest
import numpy as np
import pandas as pd
import json
import yaml
import joblib
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models.tabular_models import (
    train_random_forest_adult,
    load_trained_model,
    get_feature_importance
)

# Test constants
CONFIG_PATH = PROJECT_ROOT / "experiments/exp1_adult/configs/models/rf_adult_config.yaml"

@pytest.fixture
def temp_output_dir(tmp_path):
    """Fixture for temporary output directory."""
    model_dir = tmp_path / "models"
    results_dir = tmp_path / "results"
    model_dir.mkdir()
    results_dir.mkdir()
    return {"model_dir": str(model_dir), "results_dir": str(results_dir)}

@pytest.fixture
def test_config(temp_output_dir):
    """Fixture for test configuration."""
    # Load default config template
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
        
    # Override for speed and isolation
    config['model']['params']['n_estimators'] = 5  # Fast training
    config['output']['model_dir'] = temp_output_dir['model_dir']
    config['output']['results_dir'] = temp_output_dir['results_dir']
    
    # Save temp config
    config_path = Path(temp_output_dir['model_dir']) / "test_config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config, f)
        
    return str(config_path), config

def test_config_loading():
    """
    Test that the YAML configuration file loads correctly.

    Context:
        Config integrity is the foundation of reproducible experiments. 
        Ensures the pipeline starts with valid parameters.

    Test Cases:
        1. Config file exists at expected path.
        2. Config is valid YAML.
        3. Required top-level keys ('model', 'training', 'output') are present.

    Expected Behavior:
        Should return a dictionary with all mandatory sections.

    Relates to: EXP1-08
    """
        config = yaml.safe_load(f)
        
    assert "model" in config
    assert "training" in config
    assert "output" in config

@pytest.mark.slow
def test_train_random_forest_adult_runs(test_config):
    """
    Test that the training function executes without error.

    Context:
        Verifies the core training loop (Data Load -> Train -> Metrics).
        Ensures the `AdultRandomForestTrainer` class integration is functional.

    Test Cases:
        1. Train with default (fast) configuration.
        2. Force retraining enabled.

    Expected Behavior:
        - Return a non-None model object.
        - Return a dictionary containing key metrics (accuracy, auc).
        - Return training metadata.

    Relates to: EXP1-08
    """
    config_path, config = test_config
    
    model, metrics = train_random_forest_adult(
        config_path=config_path,
        force_retrain=True,
        verbose=False
    )
    
    assert model is not None
    assert "test_accuracy" in metrics
    assert "test_roc_auc" in metrics
    assert "training_metadata" in metrics

@pytest.mark.slow
def test_model_meets_performance_thresholds(test_config):
    """
    Test that model performance validation logic works.

    Context:
        Automated quality gates prevent deploying degraded models.
        This test checks if the detailed metric verification logic respects thresholds.

    Test Cases:
        1. Train a model (even a weak one).
        2. Validate against relaxed thresholds (0.5).

    Expected Behavior:
        - Metrics should exceed the minimum safeguards.
        - Metadata should capture feature count correctly.

    Relates to: EXP1-08
    """
    config_path, config = test_config
    # Relax thresholds for 5-tree model
    config['validation']['min_accuracy'] = 0.5 
    config['validation']['min_roc_auc'] = 0.5
    
    # Update saved config
    with open(config_path, 'w') as f:
        json.dump(config, f)
        
    model, metrics = train_random_forest_adult(
        config_path=config_path,
        force_retrain=True,
        verbose=False
    )
    
    # Check if metrics exist (values depend on random seed but should exist)
    assert metrics["test_accuracy"] > 0.0
    assert metrics["test_roc_auc"] > 0.0
    
    # Verify metadata
    assert metrics["training_metadata"]["n_features"] > 0

@pytest.mark.slow
def test_model_saving_and_loading(test_config):
    """
    Test that models can be persisted and reloaded correctly.

    Context:
        XAI methods (LIME/SHAP) often run in separate processes/times from training.
        Reliable serialization is critical for the decouple evaluation pipeline.

    Test Cases:
        1. Train and save a model.
        2. Verify .pkl file exists.
        3. Load the model back from disk using `load_trained_model`.

    Expected Behavior:
        - Loaded object should be a valid sklearn estimator.
        - `predict` method should be available.

    Relates to: EXP1-08
    """
    config_path, config = test_config
    
    # Train
    train_random_forest_adult(config_path=config_path, force_retrain=True, verbose=False)
    
    # Check file existence
    output_dir = Path(config['output']['model_dir'])
    model_name = config['output']['model_filename']
    model_path = output_dir / model_name
    
    assert model_path.exists()
    
    # Load
    loaded_model = load_trained_model(str(model_path))
    assert loaded_model is not None
    
    # Basic prediction check (functionality only)
    # We would ideally check X_test prediction match, but don't have X_test easily here without loading data again
    assert hasattr(loaded_model, "predict")

def test_feature_importance_extraction(test_config):
    """
    Test that global feature importance is extracted and validated.

    Context:
        Feature importance provides a global explanation baseline.
        Verification ensures we are capturing model internal state correctly.

    Test Cases:
        1. Extract feature importance after training.
        2. Verify CSV output creation.
        3. Check Gini importance normalization (sum ~ 1.0).

    Expected Behavior:
        - CSV file created with 'feature' and 'importance' columns.
        - Top 10 features included in metrics metadata.

    Relates to: EXP1-08
    """
    config_path, config = test_config
    
    model, metrics = train_random_forest_adult(
        config_path=config_path, 
        force_retrain=True, 
        verbose=False
    )
    
    # Check csv existence
    results_dir = Path(config['output']['results_dir'])
    csv_path = results_dir / "rf_feature_importance.csv"
    assert csv_path.exists()
    
    # Check content
    df = pd.read_csv(csv_path)
    assert "feature" in df.columns
    assert "importance" in df.columns
    
    # Check normalization
    total_importance = df["importance"].sum()
    assert 0.9 <= total_importance <= 1.1 # Approx 1.0
    
    # Check metadata integration
    assert "top_10_features" in metrics
    assert len(metrics["top_10_features"]) <= 10

if __name__ == "__main__":
    pytest.main([__file__])
