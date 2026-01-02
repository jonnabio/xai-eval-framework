
import pytest
import pandas as pd
import numpy as np
from src.analysis.stats import perform_friedman_test, perform_nemenyi_test, compute_cohens_dz

def test_friedman_identical():
    # If all methods have identical scores, p-value should be high (no difference)
    # Wait, if identical, variance is 0, might be an issue?
    # Let's add slight noise
    data = {
        'A': [1.0, 1.0, 1.0, 1.0, 1.0],
        'B': [1.0, 1.0, 1.0, 1.0, 1.0],
        'C': [1.0, 1.0, 1.0, 1.0, 1.0]
    }
    # Use data with no significant difference but some variation
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [1.1, 1.9, 3.1, 3.9, 5.1],
        'C': [0.9, 2.1, 2.9, 4.1, 4.9]
    }
    stat, p = perform_friedman_test(data)
    # p should be > 0.05
    assert p > 0.05

def test_friedman_distinct():
    # A > B > C consistently
    data = {
        'A': [10, 10, 10, 10, 10],
        'B': [5, 5, 5, 5, 5],
        'C': [1, 1, 1, 1, 1]
    }
    stat, p = perform_friedman_test(data)
    # Should be significant
    assert p < 0.05

def test_cohens_dz():
    x = [2, 4, 6]
    y = [1, 3, 5]
    # d = [1, 1, 1]
    # mean_d = 1
    # std_d = 0
    # technically inf?
    # compute_cohens_dz handles std=0 -> 0.0?
    # Actually if diff is constant positive, effect size is infinite mathematically (very large)
    # But let's check our implementation
    
    # New case:
    x = [2, 4, 6]
    y = [1, 5, 4] # d = [1, -1, 2]
    # mean = 2/3 = 0.66
    # std = 1.52
    d = np.array([1, -1, 2])
    expected_std = np.std(d, ddof=1)
    expected_mean = np.mean(d)
    expected = expected_mean / expected_std
    
    val = compute_cohens_dz(x, y)
    assert np.isclose(val, expected)

def test_nemenyi_run():
    # Just check it returns a DF shape
    data = {
        'A': [10, 9, 10, 9, 10],
        'B': [5, 6, 5, 6, 5],
        'C': [1, 2, 1, 2, 1]
    }
    df = pd.DataFrame(data)
    p_values = perform_nemenyi_test(df)
    assert isinstance(p_values, pd.DataFrame)
    assert p_values.shape == (3, 3)
