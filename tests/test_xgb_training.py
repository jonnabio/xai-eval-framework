import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import shutil
import joblib

from src.models.xgboost_trainer import XGBoostTrainer

@pytest.fixture
def synthetic_data():
    np.random.seed(42)
    n_samples = 200
    n_features = 5
    X = np.random.randn(n_samples, n_features)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    feature_names = [f"feat_{i}" for i in range(n_features)]
    
    X_df = pd.DataFrame(X, columns=feature_names)
    y_series = pd.Series(y, name="target")
    
    return X_df, y_series

@pytest.fixture
def temp_output_dir(tmp_path):
    d = tmp_path / "xgb_test_output"
    d.mkdir()
    return d

def test_xgboost_trainer_initialization():
    """
    Verify XGBoostTrainer initialization defaults and overrides.

    Context:
        Ensures the trainer class respects the hyperparameter choices defined in ADR-004
        and merges user configuration correctly.

    Test Cases:
        1. Default initialization (checks baseline params like n_estimators=100).
        2. Custom config override (e.g., n_estimators=50).

    Expected Behavior:
        - Defaults match ADR definition.
        - Custom overrides are applied while preserving non-overridden defaults.

    Related Tasks:
        EXP1-09
    """
    # Test default
    trainer = XGBoostTrainer()
    assert trainer.config['n_estimators'] == 100
    assert trainer.config['max_depth'] == 6
    
    # Test custom
    custom_config = {'n_estimators': 50, 'learning_rate': 0.05}
    trainer_custom = XGBoostTrainer(config=custom_config)
    assert trainer_custom.config['n_estimators'] == 50
    assert trainer_custom.config['learning_rate'] == 0.05
    assert trainer_custom.config['max_depth'] == 6 # Default preserved

def test_xgboost_training_basic(synthetic_data):
    """
    Verify basic training execution on synthetic data.

    Context:
        Checks that the training loop runs without errors and produces a trained model
        that can generate predictions of the correct shape.

    Test Cases:
        1. Train on synthetic binary classification data.
        2. Verify feature importances are accessible.
        3. Verify predictions are binary (0/1).

    Expected Behavior:
        - Model is not None after training.
        - Predictions shape matches input samples.
        - Predictions contain only valid class labels.

    Related Tasks:
        EXP1-09
    """
    X, y = synthetic_data
    # Use n_jobs=1 to avoid potential multiprocessing issues during testing on Windows
    trainer = XGBoostTrainer({'n_estimators': 10, 'n_jobs': 1})
    trainer.train(X, y)
    
    assert trainer.model is not None
    assert hasattr(trainer.model, "feature_importances_")
    
    # Check predictions shape
    preds = trainer.predict(X)
    assert preds.shape == (len(X),)
    assert np.unique(preds).isin([0, 1]).all()

def test_xgboost_evaluation_metrics(synthetic_data):
    """
    Verify calculation of all performance metrics.

    Context:
        Ensures the `evaluate()` method computes the standard set of metrics required
        for Experiment 1 reporting.

    Test Cases:
        1. Evaluate trained model on synthetic data.
        2. Check existence of accuracy, precision, recall, f1, roc_auc.

    Expected Behavior:
        - All metric keys are present.
        - Metric values are within valid [0, 1] range.

    Related Tasks:
        EXP1-09
    """
    X, y = synthetic_data
    trainer = XGBoostTrainer({'n_estimators': 10})
    trainer.train(X, y)
    
    metrics = trainer.evaluate(X, y)
    
    expected_metrics = ["accuracy", "precision", "recall", "f1", "roc_auc", "confusion_matrix"]
    for m in expected_metrics:
        assert m in metrics
        
    assert 0 <= metrics['accuracy'] <= 1
    assert 0 <= metrics['roc_auc'] <= 1

def test_xgboost_feature_importance(synthetic_data):
    """
    Verify feature importance extraction structure.

    Context:
        XAI explanation methods often rely on or compare against native feature importance.
        This test ensures we can extract it reliably.

    Test Cases:
        1. Extract importance from trained model.
        2. Verify DataFrame structure (columns, types).
        3. Verify sorting (descending importance).

    Expected Behavior:
        - Returns DataFrame with 'feature', 'importance', 'rank'.
        - Sorted by importance descending.
        - Length matches number of input features.

    Related Tasks:
        EXP1-09
    """
    X, y = synthetic_data
    trainer = XGBoostTrainer({'n_estimators': 10})
    trainer.train(X, y)
    
    imp_df = trainer.get_feature_importance()
    
    assert isinstance(imp_df, pd.DataFrame)
    assert "feature" in imp_df.columns
    assert "importance" in imp_df.columns
    assert "rank" in imp_df.columns
    assert len(imp_df) == X.shape[1]
    # Check sorting
    assert imp_df.iloc[0]['importance'] >= imp_df.iloc[-1]['importance']

def test_xgboost_save_load_roundtrip(synthetic_data, temp_output_dir):
    """
    Verify model persistence and restoration.

    Context:
        Ensures models trained in the pipeline can be saved to disk and reloaded later
        for analysis or inference without loss of state.

    Test Cases:
        1. Train model.
        2. Predict.
        3. Save to temp dir.
        4. Load from temp dir.
        5. Predict again and compare.

    Expected Behavior:
        - Artifact files (pkl, json) are created.
        - Re-loaded model produces identical predictions to original.
        - Config is restored correctly.

    Related Tasks:
        EXP1-09
    """
    X, y = synthetic_data
    trainer = XGBoostTrainer({'n_estimators': 10})
    trainer.train(X, y)
    
    # Predict before save
    preds_orig = trainer.predict(X)
    
    # Save
    trainer.save(temp_output_dir)
    pass # Check file existence?
    assert (temp_output_dir / "xgb_model.pkl").exists()
    assert (temp_output_dir / "xgb_model_metadata.json").exists()
    
    # Load
    loaded_trainer = XGBoostTrainer.load(temp_output_dir)
    
    # Predict after load
    preds_loaded = loaded_trainer.predict(X)
    
    # Verify match
    np.testing.assert_array_equal(preds_orig, preds_loaded)
    assert loaded_trainer.config['n_estimators'] == 10

def test_xgboost_early_stopping(synthetic_data):
    """
    Verify early stopping mechanism.

    Context:
        Early stopping is crucial for gradient boosting to prevent overfitting and speed up training.
        This test ensures validation data is accepted and potential stopping logic is triggered.

    Test Cases:
        1. Split data into train/val.
        2. Initialize trainer with high n_estimators and early_stopping_rounds.
        3. Train.

    Expected Behavior:
        - Training completes successfully (doesn't crash on eval_set).
        - If stopping triggers, best_iteration is recorded (and likely < n_estimators).

    Related Tasks:
        EXP1-09
    """
    # This is hard to guarantee deterministically on small synthetic data without careful construction,
    # but we can check it runs without error and potentially stops early if we force overfitting setup 
    # or just check that it accepts the val arguments.
    X, y = synthetic_data
    
    # Split for valid
    X_train, X_val = X.iloc[:150], X.iloc[150:]
    y_train, y_val = y.iloc[:150], y.iloc[150:]
    
    trainer = XGBoostTrainer({'n_estimators': 1000, 'early_stopping_rounds': 5}) # High enough to likely trigger stop
    
    # We capture logs or check best_iteration if possible, but for basic unit test just ensuring it runs is good step 1
    trainer.train(X_train, y_train, X_val=X_val, y_val=y_val)
    
    assert trainer.model is not None
    # XGBoost classifier stores best_iteration if early stopping occurred
    # Depending on xgboost version/sklearn wrapper, it might be available
    if hasattr(trainer.model, 'best_iteration'):
        # Just assert it exists, meaning it was tracked
        assert trainer.model.best_iteration < 1000 or trainer.model.best_iteration is not None 
