
import pytest
import numpy as np
from src.analysis.sensitivity import compute_cv, detect_plateau, classify_sensitivity, compute_percent_change

def test_compute_cv():
    # Mean=10, Std=1 -> CV=0.1
    values = [9, 10, 11] # Variance=1, Std=1
    # np.std defaults to population std (ddof=0) usually in numpy, but check implementation
    # With [9,10,11], mean=10. sum((x-mean)^2) = 1+0+1=2. var=2/3=0.66, std=0.816
    # Let's use simple numbers.
    # Mean=100, Std=10 -> CV = 0.1
    val = [90, 100, 110] # std ~8.16
    cv = compute_cv(val)
    assert cv > 0
    
    # Zero mean
    assert compute_cv([0, 0, 0]) == 0.0

def test_compute_percent_change():
    assert compute_percent_change(105, 100) == 5.0
    assert compute_percent_change(90, 100) == -10.0
    assert compute_percent_change(100, 100) == 0.0

def test_detect_plateau():
    params = [100, 200, 300, 400]
    
    # 1. Clear plateau at 200
    # 0.80 -> 0.85 (big jump) -> 0.851 (tiny) -> 0.852 (tiny)
    metrics_plat = [0.80, 0.85, 0.851, 0.852]
    # At i=0 (100): change is (0.85-0.80)/0.80 = 6% > 1%. Keep going.
    # At i=1 (200): change is (0.851-0.85)/0.85 = 0.11% < 1%. STOP. Return 200.
    assert detect_plateau(params, metrics_plat, threshold_pct=1.0) == 200
    
    # 2. No plateau (linear growth)
    metrics_linear = [0.80, 0.82, 0.84, 0.86]
    # changes ~2.5% each step. Should return last param (400).
    assert detect_plateau(params, metrics_linear, threshold_pct=1.0) == 400

def test_classify_sensitivity():
    assert classify_sensitivity(0.01) == "robust"
    assert classify_sensitivity(0.049) == "robust"
    assert classify_sensitivity(0.05) == "moderate"
    assert classify_sensitivity(0.09) == "moderate"
    assert classify_sensitivity(0.11) == "sensitive"
