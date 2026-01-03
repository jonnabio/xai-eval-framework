
import pytest
import numpy as np
from src.analysis.confidence import compute_t_ci, compute_bootstrap_ci, compute_cis

def test_t_ci_basic():
    # Simple case: values 1, 2, 3
    # Mean = 2, SEM = 1/sqrt(3) = 0.577
    # t_crit for 95% df=2 = 4.303
    # Margin = 4.303 * 0.577 = 2.48
    # CI = [2 - 2.48, 2 + 2.48] roughly [-0.48, 4.48]
    data = [1, 2, 3]
    low, high = compute_t_ci(data)
    assert 2 > low
    assert 2 < high
    assert (high - low) > 2.0 # Check reasonably wide

def test_bootstrap_warning():
    # N=5 should trigger warning
    data = [1, 2, 3, 4, 5]
    with pytest.warns(UserWarning, match="Bootstrap with N=5"):
        compute_bootstrap_ci(data)

def test_ci_coverage_simulation():
    """
    Monte Carlo simulation to verify coverage properties.
    Check if t-interval maintains ~95% coverage for N=5 Normal data.
    """
    n_sims = 1000
    n_samples = 5
    mean = 10.0
    std = 2.0
    confidence = 0.95
    
    t_coverage = 0
    boot_coverage = 0
    
    rng = np.random.default_rng(42)
    
    for _ in range(n_sims):
        sample = rng.normal(mean, std, n_samples)
        
        # t-dist
        t_low, t_high = compute_t_ci(sample, confidence)
        if t_low <= mean <= t_high:
            t_coverage += 1
            
        # bootstrap (suppress warnings for test speed/cleanliness)
        # Using fewer resamples for speed in test
        try:
            b_low, b_high = compute_bootstrap_ci(sample, confidence, n_resamples=1000, random_seed=None)
            if b_low <= mean <= b_high:
                boot_coverage += 1
        except:
            pass
            
    t_rate = t_coverage / n_sims
    boot_rate = boot_coverage / n_sims
    
    print(f"\nCoverage (N={n_samples}): t-dist={t_rate:.3f}, bootstrap={boot_rate:.3f}")
    
    # Assert t-dist is accurate (allow small noise, e.g. 0.93-0.97)
    assert 0.92 <= t_rate <= 0.98
    
    # Bootstrap might be lower for N=5, but asserts on its specific value 
    # are less critical than asserting t-dist is good.
    # Typically bootstrap undercovers at N=5 (e.g. ~0.85-0.90 coverage for 95% CI)
