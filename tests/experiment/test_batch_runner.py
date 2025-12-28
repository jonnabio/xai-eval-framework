"""
Tests for BatchExperimentRunner.
"""

import pytest
import json
import pandas as pd
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.experiment.batch_runner import BatchExperimentRunner
from src.experiment.config import ExperimentConfig

@pytest.fixture
def mock_configs(tmp_path):
    """Create dummy config files."""
    configs = []
    for i in range(3):
        p = tmp_path / f"config_{i}.yaml"
        # Minimal valid yaml for load_config to try, 
        # but we'll mostly mock load_config
        with open(p, 'w') as f:
            f.write(f"name: experiment_{i}\n")
        configs.append(p)
    return configs

@pytest.fixture
def mock_experiment_runner():
    with patch("src.experiment.batch_runner.ExperimentRunner") as mock:
        yield mock

@pytest.fixture
def mock_load_config():
    with patch("src.experiment.batch_runner.load_config") as mock:
        yield mock

def test_initialization_validation(tmp_path):
    """Test path validation and deduplication."""
    p1 = tmp_path / "c1.yaml"
    p1.touch()
    p2 = tmp_path / "c2.yaml" # Doesn't exist
    
    runner = BatchExperimentRunner([p1, p1, p2])
    assert len(runner.config_paths) == 1
    assert runner.config_paths[0] == p1

def test_checkpointing_skip(mock_configs, mock_load_config):
    """Test that existing results cause a skip."""
    # Setup config mocks
    config_objs = []
    for i, p in enumerate(mock_configs):
        c = MagicMock(spec=ExperimentConfig)
        c.name = f"exp_{i}"
        c.output_dir = p.parent / f"out_{i}"
        config_objs.append(c)
        
    mock_load_config.side_effect = config_objs
    
    # Simulate result existing for ONLY the first config
    (config_objs[0].output_dir / "results.json").parent.mkdir(parents=True, exist_ok=True)
    with open(config_objs[0].output_dir / "results.json", 'w') as f:
        json.dump({"experiment_metadata": {"name": "exp_0"}, "aggregated_metrics": {"acc": {"mean": 0.9}}}, f)
        
    runner = BatchExperimentRunner(mock_configs)
    
    # Run in sequential mode for easier mocking inspection
    # We need to mock _run_single_experiment or rely on the loop logic
    # Since _run_single_experiment is top-level, we patch it
    with patch("src.experiment.batch_runner._run_single_experiment") as mock_run:
        mock_run.return_value = {"status": "success", "experiment_name": "mock", "results": {}}
        
        df, manifest = runner.run(parallel=False)
        
        # Should have called run only 2 times (3 total - 1 skipped)
        assert mock_run.call_count == 2
        
        # Check manifest
        skipped = [e for e in manifest["executions"] if e["status"] == "skipped"]
        assert len(skipped) == 1
        assert skipped[0]["id"] == "exp_0"
        
        # Check dataframe aggregation (loaded from file)
        assert not df.empty
        assert "exp_0" in df["experiment_name"].values

def test_error_handling(mock_configs, mock_load_config):
    """Test that a single failure doesn't stop the batch."""
    # Setup configs
    config_objs = []
    for i, p in enumerate(mock_configs):
        c = MagicMock(spec=ExperimentConfig)
        c.name = f"exp_{i}"
        c.output_dir = p.parent / f"out_{i}"
        config_objs.append(c)
    mock_load_config.side_effect = config_objs
    
    runner = BatchExperimentRunner(mock_configs)
    
    with patch("src.experiment.batch_runner._run_single_experiment") as mock_run:
        # 1 success, 1 fail, 1 success
        mock_run.side_effect = [
            {"status": "success", "experiment_name": "exp_0", "results": {"experiment_metadata": {"name": "exp_0"}}},
            {"status": "failed", "experiment_name": "exp_1", "error": "Boom"},
            {"status": "success", "experiment_name": "exp_2", "results": {"experiment_metadata": {"name": "exp_2"}}}
        ]
        
        df, manifest = runner.run(parallel=False)
        
        assert len(df) == 2 # Only successes in DF
        assert len(manifest["executions"]) == 3
        
        failed = [e for e in manifest["executions"] if e["status"] == "failed"]
        assert len(failed) == 1
        assert failed[0]["error"] == "Boom"

def test_parallel_execution_integration(tmp_path):
    """
    Real integration test ensuring ProcessPoolExecutor works.
    We need minimal real configs/runner since we can't easily mock pickleable top-level func across processes.
    """
    # Create a real dummy config
    config_path = tmp_path / "test_config.yaml"
    with open(config_path, 'w') as f:
        f.write("""
name: "test"
dataset: "adult"
model:
  name: "rf"
  path: "dummy.joblib" 
explainer:
  method: "shap"
sampling:
  samples_per_class: 1
metrics:
  fidelity: false
  stability: false
  sparsity: false
  cost: false
  domain: false
""")
    
    # We must patch load_config and ExperimentRunner inside the worker process
    # But patching across processes is hard. 
    # Instead, we rely on the fact that _run_single_experiment handles exceptions.
    # If we provide a bad config/model path, it should return 'failed' status safely.
    
    runner = BatchExperimentRunner([config_path])
    
    # This will fail inside worker because 'dummy.joblib' doesn't exist
    # But it proves the worker started and returned a result dict
    df, manifest = runner.run(parallel=True, max_workers=2)
    
    assert len(manifest["executions"]) == 1
    assert manifest["executions"][0]["status"] in ["failed", "config_error"]
