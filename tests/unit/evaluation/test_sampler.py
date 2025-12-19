"""
Unit tests for EvaluationSampler.
"""
import pytest
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from src.evaluation.sampler import EvaluationSampler

# Mock Model
class MockModel(BaseEstimator):
    def __init__(self, preds):
        self.preds = preds
    
    def predict(self, X):
        return self.preds

@pytest.fixture
def sample_data():
    """Create synthetic test data causing all 4 errors."""
    # 20 samples
    X = np.random.rand(20, 3)
    # True labels: 10 zeros, 10 ones
    y = np.array([0]*10 + [1]*10)
    
    # Predictions design:
    # 0-4 (y=0): pred=0 -> TN (5)
    # 5-9 (y=0): pred=1 -> FP (5)
    # 10-14 (y=1): pred=0 -> FN (5)
    # 15-19 (y=1): pred=1 -> TP (5)
    preds = np.array([0]*5 + [1]*5 + [0]*5 + [1]*5)
    
    model = MockModel(preds)
    return model, X, y

def test_sampler_counts(sample_data):
    """Verify correct number of samples per quadrant."""
    model, X, y = sample_data
    sampler = EvaluationSampler(model, X, y)
    
    # Request 2 per group -> 8 total
    df = sampler.sample_stratified_by_error(n_per_group=2)
    
    assert len(df) == 8
    assert 'quadrant' in df.columns
    assert df['quadrant'].value_counts().to_dict() == {'TN': 2, 'FP': 2, 'FN': 2, 'TP': 2}

def test_small_groups(sample_data):
    """Verify behavior when request exceeds availability."""
    model, X, y = sample_data
    sampler = EvaluationSampler(model, X, y)
    
    # Request 10 per group (only 5 available) -> should take all 5
    df = sampler.sample_stratified_by_error(n_per_group=10)
    
    assert len(df) == 20 # 5 of each
    assert (df['quadrant'].value_counts() == 5).all()

def test_reproducibility(sample_data):
    """Verify random seed behavior."""
    model, X, y = sample_data
    
    s1 = EvaluationSampler(model, X, y, random_state=42)
    df1 = s1.sample_stratified_by_error(n_per_group=1)
    
    s2 = EvaluationSampler(model, X, y, random_state=42)
    df2 = s2.sample_stratified_by_error(n_per_group=1)
    
    pd.testing.assert_frame_equal(df1, df2)

def test_output_structure(sample_data):
    """Verify columns."""
    model, X, y = sample_data
    sampler = EvaluationSampler(model, X, y)
    df = sampler.sample_stratified_by_error(n_per_group=1)
    
    expected_cols = ['original_index', 'target', 'prediction', 'quadrant']
    for col in expected_cols:
        assert col in df.columns
    # Plus features
    assert df.shape[1] == 4 + 3 # 4 meta + 3 feature cols
