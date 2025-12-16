"""
Verification tests for EXP1-02 metrics.
User Story: EXP1-02
"""

import sys
import os
import time
import pytest
import numpy as np

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
# Check if running from root or inside tests dir
# If __file__ is experiments/exp1_adult/tests/test_metrics.py -> dirname is experiments/exp1_adult/tests
# ../src is experiments/exp1_adult/src
src_path = os.path.abspath(os.path.join(current_dir, '../src'))
sys.path.insert(0, src_path)

from exp1_adult.evaluation.metrics import (
    compute_fidelity,
    compute_stability,
    compute_sparsity,
    compute_cost
)

def test_compute_fidelity():
    # Perfect match
    y_true = np.array([1, 0, 1, 0])
    y_pred = np.array([1, 0, 1, 0])
    metrics = compute_fidelity(y_pred, y_true)
    assert metrics['r2_score'] == 1.0
    assert metrics['mse'] == 0.0

    # No match - inverse
    y_pred_inv = np.array([0, 1, 0, 1])
    metrics_inv = compute_fidelity(y_pred_inv, y_true)
    assert metrics_inv['r2_score'] < 0
    assert metrics_inv['mse'] == 1.0

def test_compute_stability():
    explanation = [0.1, 0.2, 0.7]
    X_instance = [1, 2, 3]
    
    # Mock perturbation function: returns original explanation + small noise
    def mock_perturb(X, noise):
        return [x + 0.001 for x in explanation]
    
    metrics = compute_stability(explanation, mock_perturb, X_instance, n_perturbations=3)
    
    # Expect very high similarity
    assert metrics['cosine_similarity'] > 0.99
    assert metrics['kendall_tau'] > 0.9
    assert metrics['spearman_rho'] > 0.9

def test_compute_sparsity():
    explanation = [0.001, 0.002, 0.5, 0.4]
    # Threshold 0.01 -> 2 features non-zero (0.5 and 0.4)
    metrics = compute_sparsity(explanation, threshold=0.01)
    
    assert metrics['non_zero_ratio'] == 0.5  # 2/4
    # Top 5 mass handles <5 items safely
    assert 'top_5_mass' in metrics
    assert metrics['gini_coefficient'] > 0

def test_compute_cost():
    def dummy_explainer(x):
        time.sleep(0.01)
        return "result"
    
    metrics, result = compute_cost(dummy_explainer, "input")
    
    assert result == "result"
    assert metrics['wall_time_ms'] >= 10  # at least 10ms

if __name__ == "__main__":
    print("Running tests manually...")
    try:
        test_compute_fidelity()
        print("test_compute_fidelity passed")
        test_compute_stability()
        print("test_compute_stability passed")
        test_compute_sparsity()
        print("test_compute_sparsity passed")
        test_compute_cost()
        print("test_compute_cost passed")
        print("All tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
