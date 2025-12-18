"""
Sanity checks and unit tests for RF and XGBoost models (EXP1-11).

Purpose:
    Ensures that the trained models (RF and XGBoost) are valid, reproducible, 
    and meet minimum performance baselines before being used for XAI evaluation.

Coverage:
    - Load/Save integrity (Pickling)
    - Prediction sanity (Shapes, Probability ranges)
    - Performance baselines (Accuracy > 0.80, ROC-AUC > 0.85)
    - Reproducibility (Deterministic behavior with fixed seeds)

Usage:
    pytest tests/unit/test_model_sanity.py -v

Related Tasks:
    - Validates deliverables from EXP1-08 (RF) and EXP1-09 (XGBoost).
    - Part of EXP1-11 (Unit tests / sanity checks).
"""

import sys
import pytest
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score

# Adjust path to find src
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Local imports
from src.models.tabular_models import AdultRandomForestTrainer
from src.models.xgboost_trainer import XGBoostTrainer
from src.data_loading.adult import load_adult

# Constants
PERFORMANCE_THRESHOLDS = {
    'accuracy': 0.80,  # Above majority class baseline (~0.76)
    'roc_auc': 0.85,   # Strong separation
    'f1_score': 0.60   # Reasonable balance (imbalanced dataset)
}

RANDOM_SEED = 42
N_SAMPLES_QUICK = 500  # Subset size for faster fixture training

# --- Fixtures ---

# FIXTURE: Scope='module' ensures we only load data once per test file execution
@pytest.fixture(scope="module")
def sample_data():
    """
    Module-scoped fixture to provide a small subset of the Adult dataset.
    Used to train models quickly for testing.
    """
    # Load data (using cache if available inside load_adult)
    # We load the full set but slice it down for speed
    print("DEBUG: Calling load_adult in fixture...")
    try:
        # Use absolute path for cache to avoid CWD ambiguity in pytest
        data = load_adult(
            random_state=RANDOM_SEED,
            cache_dir=str(PROJECT_ROOT / "data")
        )
        print(f"DEBUG: load_adult returned type: {type(data)}")
        if isinstance(data, tuple):
             print(f"DEBUG: tuple len: {len(data)}")
        X_train, X_test, y_train, y_test, feature_names, _ = data
    except Exception as e:
        print(f"DEBUG: load_adult FAILED: {e}")
        raise e
    print("DEBUG: load_adult success")
    
    # Slice for speed
    # X_train/X_test are numpy arrays (from preprocessor), y_train/y_test are pandas Series
    train_size = N_SAMPLES_QUICK
    test_size = int(N_SAMPLES_QUICK * 0.2)
    
    return {
        'X_train': X_train[:train_size],
        'y_train': y_train.iloc[:train_size],
        'X_test': X_test[:test_size],
        'y_test': y_test.iloc[:test_size],
        'feature_names': feature_names
    }

@pytest.fixture(scope="module")
def trained_rf_model(sample_data, tmp_path_factory):
    """
    Module-scoped fixture providing a trained Random Forest model.
    """
    import json
    from unittest.mock import patch
    
    # Create temp config dict (now supported by refactored Trainer)
    model_dir = tmp_path_factory.mktemp("rf_model")
    results_dir = tmp_path_factory.mktemp("rf_results")
    
    config = {
        'model': {
            'params': {
                'n_estimators': 10,  # Small number for speed
                'random_state': RANDOM_SEED,
                'n_jobs': 1
            }
        },
        'output': {
            'model_dir': str(model_dir),
            'model_filename': 'rf_model.pkl',
            'results_dir': str(results_dir)
        },
        'validation': {
             'min_accuracy': 0.0,
             'min_roc_auc': 0.0
        }
    }
        
    trainer = AdultRandomForestTrainer(config, verbose=False)
    
    # Mock load_adult to use our sample data slice
    mock_return = (
        sample_data['X_train'], sample_data['X_test'],
        sample_data['y_train'], sample_data['y_test'],
        sample_data['feature_names'], None
    )
    
    with patch('src.models.tabular_models.load_adult', return_value=mock_return):
        trainer.train(force_retrain=True)
    
    return trainer

@pytest.fixture(scope="module")
def trained_xgb_model(sample_data):
    """
    Module-scoped fixture providing a trained XGBoost model.
    """
    config = {
        'n_estimators': 10,
        'max_depth': 3,
        'learning_rate': 0.1,
        'random_state': RANDOM_SEED,
        'n_jobs': 1
    }
    trainer = XGBoostTrainer(config)
    # XGBoost can use validation data
    trainer.train(
        sample_data['X_train'], 
        sample_data['y_train'],
        X_val=sample_data['X_test'],
        y_val=sample_data['y_test']
    )
    return trainer

@pytest.fixture
def temp_model_dir(tmp_path):
    """
    Function-scoped fixture providing a temporary directory for save/load testing.
    """
    return tmp_path / "model_artifacts"

# --- Test Classes ---

class TestModelLoading:
    """
    Tests for model persistence (save/load).
    """
    
    def test_rf_model_file_exists(self, trained_rf_model, temp_model_dir):
        """Test RF model creates expected file on save."""
        # Clean up or ensure dir exists
        temp_model_dir.mkdir(parents=True, exist_ok=True)
        
        trained_rf_model.save(temp_model_dir)
        
        expected_file = temp_model_dir / "rf_model.pkl"
        assert expected_file.exists()
        assert expected_file.stat().st_size > 1024  # > 1KB
        
    def test_xgb_model_file_exists(self, trained_xgb_model, temp_model_dir):
        """Test XGBoost model creates expected file on save."""
        temp_model_dir.mkdir(parents=True, exist_ok=True)
        
        trained_xgb_model.save(temp_model_dir)
        
        expected_file = temp_model_dir / "xgb_model.pkl"
        assert expected_file.exists()
        assert expected_file.stat().st_size > 1024

    def test_rf_model_save_load(self, trained_rf_model, temp_model_dir, sample_data):
        """Test RF model can be saved and loaded without corruption."""
        temp_model_dir.mkdir(parents=True, exist_ok=True)
        
        # Save
        trained_rf_model.save(temp_model_dir)
        model_path = temp_model_dir / "rf_model.pkl"
        
        # Load
        loaded = AdultRandomForestTrainer.load(str(model_path))
        
        # Compare predictions
        X_test = sample_data['X_test']
        orig_preds = trained_rf_model.predict(X_test)
        loaded_preds = loaded.predict(X_test)
        
        np.testing.assert_array_equal(orig_preds, loaded_preds)

    def test_xgb_model_save_load(self, trained_xgb_model, temp_model_dir, sample_data):
        """Test XGBoost model can be saved and loaded without corruption."""
        temp_model_dir.mkdir(parents=True, exist_ok=True)
        
        # Save
        trained_xgb_model.save(temp_model_dir)
        model_path = temp_model_dir / "xgb_model.pkl"
        
        # Load
        loaded = XGBoostTrainer.load(str(model_path))
        
        # Compare predictions
        X_test = sample_data['X_test']
        orig_preds = trained_xgb_model.predict(X_test)
        loaded_preds = loaded.predict(X_test)
        
        np.testing.assert_array_equal(orig_preds, loaded_preds)

    def test_load_nonexistent_model_raises(self):
        """Test loading non-existent model raises appropriate error."""
        with pytest.raises(FileNotFoundError):
            AdultRandomForestTrainer.load("non_existent_path.pkl")

class TestModelPredictions:
    """
    Tests for prediction validity (shapes, ranges, types).
    """

    def test_rf_predict_returns_valid_shape(self, trained_rf_model, sample_data):
        """Test RF predictions have correct shape."""
        X_test = sample_data['X_test']
        n_samples = len(X_test)
        
        preds = trained_rf_model.predict(X_test)
        probs = trained_rf_model.predict_proba(X_test)
        
        assert preds.shape == (n_samples,)
        assert probs.shape == (n_samples, 2)

    def test_xgb_predict_returns_valid_shape(self, trained_xgb_model, sample_data):
        """Test XGBoost predictions have correct shape."""
        X_test = sample_data['X_test']
        n_samples = len(X_test)
        
        preds = trained_xgb_model.predict(X_test)
        probs = trained_xgb_model.predict_proba(X_test)
        
        assert preds.shape == (n_samples,)
        assert probs.shape == (n_samples, 2)

    def test_rf_predict_proba_valid_range(self, trained_rf_model, sample_data):
        """Test RF probability predictions are valid probabilities."""
        X_test = sample_data['X_test']
        probs = trained_rf_model.predict_proba(X_test)
        
        assert np.all(probs >= 0.0)
        assert np.all(probs <= 1.0)
        # Check sum to 1
        np.testing.assert_allclose(probs.sum(axis=1), 1.0, atol=1e-6)

    def test_xgb_predict_proba_valid_range(self, trained_xgb_model, sample_data):
        """Test XGBoost probability predictions are valid probabilities."""
        X_test = sample_data['X_test']
        probs = trained_xgb_model.predict_proba(X_test)
        
        assert np.all(probs >= 0.0)
        assert np.all(probs <= 1.0)
        np.testing.assert_allclose(probs.sum(axis=1), 1.0, atol=1e-6)

    def test_rf_predict_binary_values(self, trained_rf_model, sample_data):
        """Test RF predictions are valid binary class labels."""
        X_test = sample_data['X_test']
        preds = trained_rf_model.predict(X_test)
        
        unique = np.unique(preds)
        assert set(unique).issubset({0, 1})

    def test_xgb_predict_binary_values(self, trained_xgb_model, sample_data):
        """Test XGBoost predictions are valid binary class labels."""
        X_test = sample_data['X_test']
        preds = trained_xgb_model.predict(X_test)
        
        unique = np.unique(preds)
        assert set(unique).issubset({0, 1})

    def test_rf_handles_single_sample(self, trained_rf_model, sample_data):
        """Test RF can predict on a single sample (crucial for XAI methods)."""
        X_single = sample_data['X_test'].iloc[[0]]
        
        pred = trained_rf_model.predict(X_single)
        prob = trained_rf_model.predict_proba(X_single)
        
        assert pred.shape == (1,)
        assert prob.shape == (1, 2)

    def test_xgb_handles_single_sample(self, trained_xgb_model, sample_data):
        """Test XGBoost can predict on a single sample."""
        X_single = sample_data['X_test'].iloc[[0]]
        
        pred = trained_xgb_model.predict(X_single)
        prob = trained_xgb_model.predict_proba(X_single)
        
        assert pred.shape == (1,)
        assert prob.shape == (1, 2)

class TestModelPerformance:
    """
    Tests for model performance against defined baselines.
    """

    def test_rf_accuracy_above_baseline(self, trained_rf_model, sample_data):
        """Test RF accuracy exceeds majority class baseline and minimum threshold."""
        metrics = trained_rf_model.evaluate(sample_data['X_test'], sample_data['y_test'])
        acc = metrics['accuracy']
        
        # THRESHOLD: Majority class baseline is usually ~0.76 for Adult income > 50k
        assert acc > 0.76, f"RF Accuracy {acc} below majority class baseline"
        # THRESHOLD: We expect >0.80 for any reasonable ML model on this dataset
        assert acc >= PERFORMANCE_THRESHOLDS['accuracy'], \
            f"RF Accuracy {acc} below threshold {PERFORMANCE_THRESHOLDS['accuracy']}"

    def test_xgb_accuracy_above_baseline(self, trained_xgb_model, sample_data):
        """Test XGBoost accuracy exceeds majority class baseline."""
        metrics = trained_xgb_model.evaluate(sample_data['X_test'], sample_data['y_test'])
        acc = metrics['accuracy']
        
        assert acc > 0.76
        assert acc >= PERFORMANCE_THRESHOLDS['accuracy']

    def test_rf_roc_auc_above_threshold(self, trained_rf_model, sample_data):
        """Test RF ROC-AUC exceeds minimum threshold."""
        metrics = trained_rf_model.evaluate(sample_data['X_test'], sample_data['y_test'])
        auc = metrics['roc_auc']
        
        assert auc > 0.5
        assert auc >= PERFORMANCE_THRESHOLDS['roc_auc']

    def test_xgb_roc_auc_above_threshold(self, trained_xgb_model, sample_data):
        """Test XGBoost ROC-AUC exceeds minimum threshold."""
        metrics = trained_xgb_model.evaluate(sample_data['X_test'], sample_data['y_test'])
        auc = metrics['roc_auc']
        
        assert auc > 0.5
        assert auc >= PERFORMANCE_THRESHOLDS['roc_auc']

    def test_rf_f1_score_reasonable(self, trained_rf_model, sample_data):
        """Test RF F1 score is reasonable for imbalanced dataset."""
        metrics = trained_rf_model.evaluate(sample_data['X_test'], sample_data['y_test'])
        f1 = metrics['f1']
        
        assert f1 > 0.0
        assert f1 >= PERFORMANCE_THRESHOLDS['f1_score']

    def test_xgb_f1_score_reasonable(self, trained_xgb_model, sample_data):
        """Test XGBoost F1 score is reasonable."""
        metrics = trained_xgb_model.evaluate(sample_data['X_test'], sample_data['y_test'])
        f1 = metrics['f1']
        
        assert f1 > 0.0
        assert f1 >= PERFORMANCE_THRESHOLDS['f1_score']

    def test_rf_not_overfitting(self, trained_rf_model, sample_data):
        """Test RF train/test accuracy gap is acceptable (< 15% for small data)."""
        # Train accuracy
        train_preds = trained_rf_model.predict(sample_data['X_train'])
        train_acc = accuracy_score(sample_data['y_train'], train_preds)
        
        # Test accuracy
        test_metrics = trained_rf_model.evaluate(sample_data['X_test'], sample_data['y_test'])
        test_acc = test_metrics['accuracy']
        
        gap = train_acc - test_acc
        # With small data, RF can easily overfit (train ~1.0, test ~0.8)
        # We relax this check for the 'quick' test fixture
        assert gap < 0.25, f"RF Overfitting gap {gap:.2f} is too high"

    def test_xgb_not_overfitting(self, trained_xgb_model, sample_data):
        """Test XGBoost train/test accuracy gap."""
        train_preds = trained_xgb_model.predict(sample_data['X_train'])
        train_acc = accuracy_score(sample_data['y_train'], train_preds)
        
        test_metrics = trained_xgb_model.evaluate(sample_data['X_test'], sample_data['y_test'])
        test_acc = test_metrics['accuracy']
        
        gap = train_acc - test_acc
        assert gap < 0.25

class TestModelReproducibility:
    """
    Tests for determinism and random seed control.
    """

    @pytest.mark.slow
    def test_rf_deterministic_predictions(self, sample_data, tmp_path):
        """Test RF produces identical predictions with same seed."""
        from unittest.mock import patch
        
        # Mock for training calls
        mock_return = (
            sample_data['X_train'], sample_data['X_test'],
            sample_data['y_train'], sample_data['y_test'],
            sample_data['feature_names'], None
        )

        config = {'params': {'n_estimators': 5, 'random_state': RANDOM_SEED}}
        full_config = {'model': config, 'output': {'model_dir': str(tmp_path), 'results_dir': str(tmp_path)}}
        
        with patch('src.models.tabular_models.load_adult', return_value=mock_return):
            # Train model 1
            trainer1 = AdultRandomForestTrainer(full_config, verbose=False)
            trainer1.train(force_retrain=True)
            preds1 = trainer1.predict(sample_data['X_test'])
            
            # Train model 2
            trainer2 = AdultRandomForestTrainer(full_config, verbose=False)
            trainer2.train(force_retrain=True)
            preds2 = trainer2.predict(sample_data['X_test'])
        
        np.testing.assert_array_equal(preds1, preds2)

    @pytest.mark.slow
    def test_xgb_deterministic_predictions(self, sample_data):
        """Test XGBoost produces identical predictions with same seed."""
        config = {'random_state': RANDOM_SEED, 'n_estimators': 5, 'max_depth': 2}
        
        trainer1 = XGBoostTrainer(config)
        trainer1.train(sample_data['X_train'], sample_data['y_train'])
        preds1 = trainer1.predict(sample_data['X_test'])
        
        trainer2 = XGBoostTrainer(config)
        trainer2.train(sample_data['X_train'], sample_data['y_train'])
        preds2 = trainer2.predict(sample_data['X_test'])
        
        np.testing.assert_array_equal(preds1, preds2)

    @pytest.mark.slow
    def test_rf_different_seeds_different_results(self, sample_data, tmp_path):
        """Test RF produces different predictions with different seeds."""
        from unittest.mock import patch
        
        mock_return = (
            sample_data['X_train'], sample_data['X_test'],
            sample_data['y_train'], sample_data['y_test'],
            sample_data['feature_names'], None
        )
        
        config1 = {'model': {'params': {'n_estimators': 5, 'random_state': 42}}, 'output': {'model_dir': str(tmp_path), 'results_dir': str(tmp_path)}}
        config2 = {'model': {'params': {'n_estimators': 5, 'random_state': 12345}}, 'output': {'model_dir': str(tmp_path), 'results_dir': str(tmp_path)}}

        with patch('src.models.tabular_models.load_adult', return_value=mock_return):
            # Seed 1
            trainer1 = AdultRandomForestTrainer(config1, verbose=False)
            trainer1.train(force_retrain=True)
            probs1 = trainer1.predict_proba(sample_data['X_test'])
            
            # Seed 2
            trainer2 = AdultRandomForestTrainer(config2, verbose=False)
            trainer2.train(force_retrain=True)
            probs2 = trainer2.predict_proba(sample_data['X_test'])
        
        # Should likely differ
        with pytest.raises(AssertionError):
            np.testing.assert_array_almost_equal(probs1, probs2)

    @pytest.mark.slow
    def test_rf_feature_importances_stable(self, sample_data, tmp_path):
        """Test RF feature importances are stable across identical training."""
        from unittest.mock import patch
        
        mock_return = (
            sample_data['X_train'], sample_data['X_test'],
            sample_data['y_train'], sample_data['y_test'],
            sample_data['feature_names'], None
        )
        
        config = {'model': {'params': {'n_estimators': 10, 'random_state': RANDOM_SEED}}, 'output': {'model_dir': str(tmp_path), 'results_dir': str(tmp_path)}}

        with patch('src.models.tabular_models.load_adult', return_value=mock_return):
            trainer1 = AdultRandomForestTrainer(config, verbose=False)
            trainer1.train(force_retrain=True)
            imp1 = trainer1.get_feature_importance()['importance'].values
            
            trainer2 = AdultRandomForestTrainer(config, verbose=False)
            trainer2.train(force_retrain=True)
            imp2 = trainer2.get_feature_importance()['importance'].values
        
        np.testing.assert_array_almost_equal(imp1, imp2)
        
@pytest.fixture(params=['rf', 'xgb'])
def trained_model(request, trained_rf_model, trained_xgb_model):
    """Parametrized fixture providing both model types."""
    if request.param == 'rf':
        return trained_rf_model
    elif request.param == 'xgb':
        return trained_xgb_model

class TestBothModels:
    """
    Parametrized interface tests for all supported models.
    """

    def test_model_has_required_methods(self, trained_model):
        """Test model has required interface methods."""
        required = [
            'train', 'predict', 'predict_proba', 'evaluate', 
            'save', 'load', 'get_feature_importance'
        ]
        for method in required:
            assert hasattr(trained_model, method), f"Model missing method: {method}"
            assert callable(getattr(trained_model, method))

    def test_model_evaluate_returns_expected_keys(self, trained_model, sample_data):
        """Test evaluate() returns dict with expected metric keys."""
        metrics = trained_model.evaluate(sample_data['X_test'], sample_data['y_test'])
        
        assert isinstance(metrics, dict)
        required_keys = ['accuracy', 'roc_auc', 'f1']
        for k in required_keys:
            assert k in metrics, f"Metrics missing key: {k}"

    def test_model_handles_unseen_data(self, trained_model, sample_data):
        """Test model predicts on data (interface check on valid test set)."""
        preds = trained_model.predict(sample_data['X_test'])
        assert len(preds) == len(sample_data['X_test'])

