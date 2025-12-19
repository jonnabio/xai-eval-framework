"""Integration test for experiment runner."""

import pytest
from pathlib import Path
import tempfile
import yaml
import json
import pandas as pd
import joblib
import numpy as np

from src.experiment.config import load_config, ExperimentConfig
from src.experiment.runner import ExperimentRunner

# We need a fixture that ensures a dummy model exists for testing
# Because ExperimentRunner loads models from disk

class DummyModel:
    """Dummy XGBoost-like model for testing."""
    def predict(self, X):
        return np.zeros(len(X))
    def predict_proba(self, X):
        # 2 classes
        p = np.zeros((len(X), 2))
        p[:, 0] = 1.0
        return p

@pytest.fixture
def dummy_model_path(tmp_path):
    """Create a dummy XGBoost-like model for testing."""
    model = DummyModel()
    model_path = tmp_path / "dummy_model.joblib"
    joblib.dump(model, model_path)
    return model_path

@pytest.fixture
def temp_config_file(tmp_path, dummy_model_path):
    """Create temporary experiment configuration."""
    output_dir = tmp_path / "output"
    
    config_data = {
        'name': 'test_experiment',
        'description': 'Integration test experiment',
        'dataset': 'adult',
        'version': '1.0.0',
        'random_seed': 42,
        'model': {
            'name': 'xgboost', # Using xgboost wrapper
            'path': str(dummy_model_path)
        },
        'explainer': {
            'method': 'lime', # Use LIME as it's model-agnostic
            'num_samples': 10,
            'num_features': 2
        },
        'sampling': {
            'strategy': 'stratified',
            'samples_per_class': 2,  # Very small for speed
            'random_seed': 42
        },
        'metrics': {
            'fidelity': True,
            'stability': True,
            'sparsity': True,
            'cost': True,
            'stability_perturbations': 2,
            'stability_noise_level': 0.1
        },
        'output_dir': str(output_dir)
    }
    
    config_path = tmp_path / "test_config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)
        
    return config_path

def test_experiment_runner_full_pipeline(temp_config_file):
    """Test complete experiment execution pipeline."""
    # Load config
    config = load_config(temp_config_file)
    assert config.name == 'test_experiment'
    
    # Initialize runner
    runner = ExperimentRunner(config)
    
    # Run experiment
    results = runner.run()
    
    # Verify structure
    assert 'experiment_metadata' in results
    assert 'model_info' in results
    assert 'instance_evaluations' in results
    assert 'aggregated_metrics' in results
    
    # Verify metadata
    assert results['experiment_metadata']['name'] == 'test_experiment'
    
    # Verify instance evaluations
    # 4 quadrants * 2 samples = 8? 
    # But stratified sampler might not match exactly if dummy model predictions/labels don't create all quadrants
    # Dummy model predicts all 0. 
    # If dataset has both 0 and 1 labels, we get TN and FN. 
    # TP and FP requires pred=1. So only 2 quadrants populated.
    # 2 quadrants * 2 samples = 4 evaluations.
    assert len(results['instance_evaluations']) > 0
    
    first_instance = results['instance_evaluations'][0]
    assert 'metrics' in first_instance
    
    # Verify metrics present
    metrics = first_instance['metrics']
    assert 'fidelity' in metrics
    assert 'stability' in metrics
    assert 'sparsity' in metrics
    assert 'cost' in metrics
    
    # Verify output files
    output_dir = Path(config.output_dir)
    assert (output_dir / 'results.json').exists()
    assert (output_dir / 'metrics.csv').exists()
    
    # Verify CSV content
    df = pd.read_csv(output_dir / 'metrics.csv')
    assert not df.empty
    assert 'metric_fidelity' in df.columns
