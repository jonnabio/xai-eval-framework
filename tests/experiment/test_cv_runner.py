
import pytest
from unittest.mock import MagicMock, patch, mock_open
import pandas as pd
import numpy as np
from pathlib import Path
import json

from src.experiment.config import ExperimentConfig, ModelConfig, ExplainerConfig, SamplingConfig, MetricsConfig
from src.experiment.cv_runner import CrossValidationRunner

@pytest.fixture
def mock_config():
    return ExperimentConfig(
        name="test_experiment",
        dataset="adult",
        model=ModelConfig(name="xgb", path=Path("mock_model.pkl")),
        explainer=ExplainerConfig(method="lime"),
        sampling=SamplingConfig(),
        metrics=MetricsConfig(),
        output_dir=Path("outputs/test")
    )

def test_init(mock_config):
    runner = CrossValidationRunner(mock_config, n_folds=3)
    assert runner.n_folds == 3
    assert runner.base_output_dir == Path("outputs/cv/test_experiment")

def test_aggregate_results(mock_config):
    runner = CrossValidationRunner(mock_config)
    
    fold_metrics = [
        {"fidelity": {"mean": 0.8, "std": 0.1}, "stability": {"mean": 0.9}},
        {"fidelity": {"mean": 0.82, "std": 0.1}, "stability": {"mean": 0.92}},
        {"fidelity": {"mean": 0.78, "std": 0.1}, "stability": {"mean": 0.88}}
    ]
    
    runner._aggregate_cv_results(fold_metrics)
    
    agg = runner.results["aggregated_metrics"]
    assert "fidelity" in agg
    assert np.isclose(agg["fidelity"]["mean"], 0.8) # Mean of 0.8, 0.82, 0.78 is 0.8
    assert "std" in agg["fidelity"]
    assert "cv" in agg["fidelity"]
    
def test_validation_logic(mock_config):
    runner = CrossValidationRunner(mock_config)
    
    # Mock aggregated results
    runner.results["aggregated_metrics"] = {
        "fidelity": {"mean": 0.8, "std": 0.05} # CI: 0.8 +/- 0.098 => [0.702, 0.898]
    }
    
    # Mock original results existing
    original_data = {
        "aggregated_metrics": {
            "fidelity": {"mean": 0.75} # Within range
        }
    }
    
    with patch("builtins.open", mock_open(read_data=json.dumps(original_data))):
        with patch("pathlib.Path.exists", return_value=True):
            runner._validate_and_compare()
            
    assert "validation" in runner.results
    assert runner.results["validation"]["fidelity_consistent"] is True
    
    # Test FAIL case
    original_data_fail = {
        "aggregated_metrics": {
            "fidelity": {"mean": 0.95} # Outside range
        }
    }
    
    with patch("builtins.open", mock_open(read_data=json.dumps(original_data_fail))):
        with patch("pathlib.Path.exists", return_value=True):
            runner._validate_and_compare()
            
    assert runner.results["validation"]["fidelity_consistent"] is False

@patch("src.experiment.cv_runner.load_adult")
@patch("src.experiment.cv_runner.XGBoostTrainer")
@patch("src.experiment.cv_runner.ExperimentRunner")
@patch("src.experiment.cv_runner.joblib")
def test_run_flow(mock_joblib, mock_exp_runner, mock_xgb, mock_load_data, mock_config):
    # Mock data load
    df = pd.DataFrame(np.random.rand(20, 5), columns=[f"f{i}" for i in range(5)])
    y = pd.Series(np.random.randint(0, 2, 20))
    mock_load_data.return_value = (df, df, y, y, ["f0"], None)
    
    # Mock Trainer
    mock_trainer_instance = MagicMock()
    mock_trainer_instance.evaluate.return_value = {"accuracy": 0.9}
    mock_xgb.return_value = mock_trainer_instance
    
    # Mock ExperimentRunner
    mock_runner_instance = MagicMock()
    mock_runner_instance.run.return_value = {
        "aggregated_metrics": {"fidelity": {"mean": 0.8, "std": 0.1}}
    }
    mock_exp_runner.return_value = mock_runner_instance
    
    # Init runner
    cv_runner = CrossValidationRunner(mock_config, n_folds=2)
    
    # Run
    res = cv_runner.run()
    
    assert len(res["folds"]) == 2
    assert "fidelity" in res["aggregated_metrics"]
    
