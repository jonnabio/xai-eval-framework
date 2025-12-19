"""
Unit tests for XAI Metrics.
"""
import pytest
import numpy as np
from src.metrics import (
    CostMetric, 
    SparsityMetric, 
    FidelityMetric, 
    StabilityMetric
)

# --- Sparsity Tests ---

def test_sparsity_basic():
    """Test sparsity calculation."""
    metric = SparsityMetric(threshold=0.1)
    # 2 active, 3 zero (out of 5)
    exp_vec = np.array([0.5, 0.3, 0.05, 0.0, 0.0])
    
    res = metric.compute(exp_vec)
    assert res['nonzero_count'] == 2
    assert res['nonzero_percentage'] == 0.4
    assert 'gini_index' in res

def test_sparsity_gini():
    """Test Gini index for perfect equality and inequality."""
    metric = SparsityMetric()
    
    # Perfect equality (all ones) -> Gini 0?
    # Actually Gini of uniform dist is 0? Let's check formula behavior or just consistency.
    # Uniform: [1, 1, 1]
    res_eq = metric.compute(np.array([1, 1, 1]))
    # Calculation: sorted=[1,1,1], cum=[1,2,3], sum=3, n=3
    # 2*sum(1*1, 2*1, 3*1) / (3*3) - (4/3) = 2*6/9 - 1.33 = 1.33 - 1.33 = 0
    assert abs(res_eq['gini_index']) < 1e-5
    
    # Perfect inequality (one 1, rest 0)
    res_ineq = metric.compute(np.array([1, 0, 0]))
    # Usually Gini closer to 1.
    assert res_ineq['gini_index'] > 0.5

# --- Cost Tests ---

def test_cost_context_manager():
    """Test timing."""
    import time
    metric = CostMetric()
    
    def slow_func():
        time.sleep(0.01)
        return "done"
        
    res, metrics = metric.measure(slow_func)
    
    assert res == "done"
    assert metrics['time_ms'] >= 10.0 # 10ms + overhead

def test_cost_from_metadata():
    """Test reading time from metadata."""
    metric = CostMetric()
    explanation = {'metadata': {'total_time_seconds': 0.5}}
    
    res = metric.compute(explanation)
    assert res['time_ms'] == 500.0

# --- Fidelity Tests ---

class MockLinearModel:
    def predict(self, X):
        # Perfect linear model: y = x0 + x1
        return np.sum(X[:, :2], axis=1)

def test_fidelity_perfect():
    """Test R2=1.0 for perfect linear mimic."""
    metric = FidelityMetric(n_samples=50)
    
    # Original data
    instance = np.zeros(3)
    
    # The 'black box' is actually linear here
    bb_model = MockLinearModel()
    
    # The explanation accurately reflects the weights (1, 1, 0)
    # Weights match the mock model behavior
    explanation_weights = np.array([1.0, 1.0, 0.0])
    
    res = metric.compute(explanation_weights, model=bb_model, data=instance)
    
    assert res['r2_score'] > 0.99
    assert res['mae'] < 1e-5

# --- Stability Tests ---

def test_stability_perfect():
    """Test stability=1.0 when explainer is deterministic."""
    metric = StabilityMetric(n_iterations=5)
    
    model = "dummy"
    data = np.zeros(3)
    
    # Explainer always returns same vector
    def mock_explainer(m, d):
        return {'feature_importance': np.array([0.5, 0.5, 0.0])}
        
    res = metric.compute(None, model=model, data=data, explainer_func=mock_explainer)
    
    assert abs(res['cosine_similarity_mean'] - 1.0) < 1e-5
    assert res['cosine_similarity_std'] < 1e-5

def test_stability_random():
    """Test stability < 1.0 for random explainer."""
    metric = StabilityMetric(n_iterations=20) # More iterations for stat sig
    
    def random_explainer(m, d):
        return {'feature_importance': np.random.rand(3)}
        
    res = metric.compute(None, model="dummy", data=np.zeros(3), explainer_func=random_explainer)
    
    assert res['cosine_similarity_mean'] < 0.9 # Should be much lower
