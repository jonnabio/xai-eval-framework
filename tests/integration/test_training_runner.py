import pytest
import shutil
import sys
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

# Adjust path to find the script
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

# Import the module to be tested
from experiments.exp1_adult import run_train_models

@pytest.fixture
def temp_exp_env(tmp_path):
    """
    Sets up a temporary environment for testing the training runner.
    Creates config, models, and results directories.
    """
    # 1. Create directory structure
    exp_dir = tmp_path / "experiments/exp1_adult"
    config_dir = exp_dir / "config"
    models_dir = exp_dir / "models"
    results_dir = exp_dir / "results"
    log_dir = exp_dir / "logs"
    
    for d in [config_dir, models_dir, results_dir, log_dir]:
        d.mkdir(parents=True)
        
    # 2. Create a valid config file
    config_path = config_dir / "test_config.yaml"
    config_data = {
        'data': {
            # Use a dummy cache dir or real one? 
            # Ideally we mock load_adult so this doesn't matter too much, 
            # but for component integration we might want real data.
            # Let's point to real cache for now but use only 1% data if we could, 
            # but load_adult doesn't support subsampling at load time.
            'test_size': 0.2,
            'random_state': 42,
            'cache_dir': str(PROJECT_ROOT / "data"), # Point to real data cache
            'preprocessor_output': str(models_dir / "preprocessor.pkl")
        },
        'models': {
            'rf': {
                'n_estimators': 2, # Small number for fast test
                'n_jobs': 1,
                'random_state': 42
            },
            'xgboost': {
                'n_estimators': 2, # Small number for fast test
                'max_depth': 2,
                'learning_rate': 0.1,
                'random_state': 42,
                'n_jobs': 1
            }
        },
        'output': {
            'models_dir': str(models_dir),
            'metrics_dir': str(results_dir),
            'log_dir': str(log_dir)
        },
        'experiment': {
            'name': 'test_exp',
            'version': '0.0.1'
        }
    }
    
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)
        
    return {
        'root': tmp_path,
        'config_path': str(config_path),
        'models_dir': models_dir,
        'results_dir': results_dir
    }

def test_full_training_pipeline(temp_exp_env):
    """
    Test complete training pipeline with minimal config.
    
    Verifies that:
    - Config loads correcty.
    - Data loads (using real cache if available).
    - Both RF and XGBoost train (with minimal trees).
    - Artifacts are produced.
    """
    # Run main with the test config
    run_train_models.main(config_path=temp_exp_env['config_path'])
    
    # Check Models
    assert (temp_exp_env['models_dir'] / "rf_model.pkl").exists()
    assert (temp_exp_env['models_dir'] / "xgboost_model.pkl").exists()
    
    # Check Metrics
    csv_files = list(temp_exp_env['results_dir'].glob("*.csv"))
    assert len(csv_files) == 1
    
    parquet_files = list(temp_exp_env['results_dir'].glob("*.parquet"))
    assert len(parquet_files) == 1

def test_dry_run_mode(temp_exp_env):
    """Test dry-run mode validates without training."""
    # We need to simulate CLI args by invoking main directly with dry_run=True, 
    # but run_train_models.main signature was updated to accept flags.
    
    run_train_models.main(
        config_path=temp_exp_env['config_path'],
        dry_run=True
    )
    
    # Verify NO models are created
    assert not (temp_exp_env['models_dir'] / "rf_model.pkl").exists()

def test_single_model_training(temp_exp_env):
    """Test training a single model filter."""
    run_train_models.main(
        config_path=temp_exp_env['config_path'],
        models_filter="rf"
    )
    
    # Verify ONLY RF is created
    assert (temp_exp_env['models_dir'] / "rf_model.pkl").exists()
    assert not (temp_exp_env['models_dir'] / "xgboost_model.pkl").exists()

def test_invalid_config_handling(tmp_path):
    """Test graceful handling of invalid/missing config."""
    invalid_path = tmp_path / "nonexistent.yaml"
    
    # Currently main catches ConfigurationError and exits 1
    # We should catch SystemExit
    with pytest.raises(SystemExit) as excinfo:
        run_train_models.main(config_path=str(invalid_path))
    
    assert excinfo.value.code == 1
