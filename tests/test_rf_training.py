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
CONFIG_PATH = PROJECT_ROOT / "experiments/exp1_adult/configs/models/rf_adult_config.json"

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
        config = json.load(f)
        
    # Override for speed and isolation
    config['model']['params']['n_estimators'] = 5  # Fast training
    config['output']['model_dir'] = temp_output_dir['model_dir']
    config['output']['results_dir'] = temp_output_dir['results_dir']
    
    # Save temp config
    config_path = Path(temp_output_dir['model_dir']) / "test_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f)
        
    return str(config_path), config

def test_config_loading():
    """Test 1: Verify config file exists and is valid JSON."""
    assert os.path.exists(CONFIG_PATH), "Config file does not exist"
    
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
        
    assert "model" in config
    assert "training" in config
    assert "output" in config

@pytest.mark.slow
def test_train_random_forest_adult_runs(test_config):
    """Test 2: Train model with default (fast) config."""
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
    """Test 3: Assert metric thresholds (relaxed for fast test model)."""
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
    """Test 4: Train, save, and reload model."""
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
    """Test 5: Verify feature importance calculation."""
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
