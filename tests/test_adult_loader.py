import pytest
import numpy as np
import pandas as pd
import os
import joblib
from pathlib import Path
from src.data_loading.adult import load_adult, load_preprocessor, get_original_feature_names

# Fixture for small test size to speed up tests
@pytest.fixture
def small_data_params(tmp_path):
    return {
        "test_size": 0.2,
        "random_state": 42,
        "preprocessor_path": str(tmp_path / "preprocessor.joblib"),
        "verbose": False
    }

def test_load_adult_shapes(small_data_params):
    """Verify all shapes are consistent."""
    X_train, X_test, y_train, y_test, features, _ = load_adult(**small_data_params)
    
    # Check dimensions
    assert X_train.shape[1] == len(features)
    assert X_test.shape[1] == len(features)
    assert X_train.shape[0] == y_train.shape[0]
    assert X_test.shape[0] == y_test.shape[0]
    
    # Check that we have data
    assert X_train.shape[0] > 0
    assert X_test.shape[0] > 0

def test_load_adult_values(small_data_params):
    """Check value ranges, binary labels, no NaN."""
    X_train, X_test, y_train, y_test, _, _ = load_adult(**small_data_params)
    
    # Check target is binary 0/1
    assert set(np.unique(y_train)).issubset({0, 1})
    assert set(np.unique(y_test)).issubset({0, 1})
    
    # Check no NaNs in processed data
    assert not np.isnan(X_train).any()
    assert not np.isnan(X_test).any()
    
    # Check numeric types
    assert X_train.dtype in [np.float64, np.float32]
    assert X_test.dtype in [np.float64, np.float32]

def test_preprocessor_persistence(small_data_params, tmp_path):
    """Test saving/loading preprocessor."""
    path = small_data_params["preprocessor_path"]
    
    # Run load_adult which should save the preprocessor
    _, _, _, _, _, original_prep = load_adult(**small_data_params)
    
    assert os.path.exists(path)
    
    # Load it back
    loaded_prep = load_preprocessor(path)
    
    # Verify it's a Pipeline/ColumnTransformer and matches type
    assert type(loaded_prep) == type(original_prep)

def test_stratified_split(small_data_params):
    """Verify class balance is maintained."""
    X_train, X_test, y_train, y_test, _, _ = load_adult(**small_data_params)
    
    train_ratio = y_train.mean()
    test_ratio = y_test.mean()
    
    # Check that ratios are close (within 1% tolerance)
    assert abs(train_ratio - test_ratio) < 0.01

def test_feature_names(small_data_params):
    """Ensure feature names match array dimensions."""
    X_train, _, _, _, features, _ = load_adult(**small_data_params)
    
    assert len(features) == X_train.shape[1]
    
    # Check original features utility
    num, cat = get_original_feature_names()
    assert len(num) > 0
    assert len(cat) > 0
    
    # Check that some feature names look correct (e.g. one-hot encoded)
    # Categorical features like 'workclass' should appear as 'workclass_Private', etc.
    # Note: ColumnTransformer with verbose_feature_names_out=False will have 'workclass_Private' 
    # if the OHE prefixes with column name. Sklearn default is yes.
    
    has_ohe_feature = any("workclass" in f for f in features)
    assert has_ohe_feature
