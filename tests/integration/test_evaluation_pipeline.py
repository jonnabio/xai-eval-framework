"""
Integration test for the full Evaluation Pipeline.
End-to-end: Sampler -> LIME/SHAP -> Metrics.
"""
import pytest
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from src.evaluation.sampler import EvaluationSampler
from src.xai.lime_tabular import LIMETabularWrapper
from src.xai.shap_tabular import SHAPTabularWrapper
from src.metrics import (
    FidelityMetric, 
    StabilityMetric, 
    SparsityMetric, 
    CostMetric
)

# --- Mocking ---

class MockProbaModel(BaseEstimator):
    def predict(self, X):
        # Predict class 1 if sum(first 2 features) > 1
        return (np.sum(X[:, :2], axis=1) > 1.0).astype(int)
        
    def predict_proba(self, X):
        # Proba related to sum
        s = np.sum(X[:, :2], axis=1)
        p = 1 / (1 + np.exp(-(s - 1.0)))
        return np.vstack([1-p, p]).T

@pytest.fixture
def pipeline_data():
    """Setup small dataset and model."""
    X = np.random.rand(20, 4)
    y = (np.sum(X[:, :2], axis=1) > 1.0).astype(int)
    feature_names = ['f0', 'f1', 'f2', 'f3']
    model = MockProbaModel()
    return model, X, y, feature_names

def test_full_pipeline(pipeline_data):
    """Run full flow: Sampler -> SHAP -> Metrics."""
    model, X, y, feature_names = pipeline_data
    
    # 1. Sampler
    # Create evaluation set (small)
    sampler = EvaluationSampler(model, X, y, random_state=42)
    eval_df = sampler.sample_stratified_by_error(n_per_group=2)
    assert len(eval_df) > 0
    
    # 2. XAI Generation (SHAP)
    # Use real SHAP wrapper on mock data/model
    # Note: SHAP TreeExplainer needs Tree model. Use specific model_type='kernel' for mock.
    shap_wrapper = SHAPTabularWrapper(
        model=model,
        training_data=X[:10],
        feature_names=feature_names,
        model_type="kernel",
        n_background_samples=5
    )
    
    # Pick one instance to evaluate
    instance_row = eval_df.iloc[0]
    # Extract features (drop metadata)
    metadata_cols = ['original_index', 'target', 'prediction', 'quadrant']
    instance_data = instance_row.drop(labels=metadata_cols).values.astype(float)
    
    # Generate Explanation
    with CostMetric() as cost_tracker:
        explanation = shap_wrapper.explain_instance(model, instance_data, return_full=True)
        # explain_instance returns (weights, result_dict)
        weights, result_dict = explanation
        
    # 3. Metrics Calculation
    metrics_report = {}
    
    # A. Cost (from tracker)
    # Check if context manager worked? 
    # Actually CostMetric stores start_time. We need to calculate manually or use .measure
    # Let's use the explicit check from metadata
    cost_m = CostMetric()
    metrics_report['cost'] = cost_m.compute(result_dict)
    
    # B. Sparsity
    sparsity_m = SparsityMetric(threshold=0.01)
    metrics_report['sparsity'] = sparsity_m.compute(weights)
    
    # C. Fidelity
    fidelity_m = FidelityMetric(n_samples=50)
    metrics_report['fidelity'] = fidelity_m.compute(weights, model=model, data=instance_data)
    
    # D. Stability
    # Needs a function to re-generate explanation
    def explainer_func(m, d):
        w, res = shap_wrapper.explain_instance(m, d[0], return_full=True)
        return {'feature_importance': list(w)} # Stability expects dict with feature_importance
        
    stability_m = StabilityMetric(n_iterations=2)
    metrics_report['stability'] = stability_m.compute(
        None, model=model, data=instance_data, explainer_func=explainer_func
    )
    
    # 4. Assertions
    assert metrics_report['cost']['time_ms'] > 0
    assert 0 <= metrics_report['sparsity']['nonzero_percentage'] <= 1.0
    assert -10.0 <= metrics_report['fidelity']['r2_score'] <= 1.0 # R2 can be negative
    assert 0 <= metrics_report['stability']['cosine_similarity_mean'] <= 1.0 + 1e-5
