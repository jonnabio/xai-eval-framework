
import numpy as np
from scipy import stats
import warnings

def compute_t_ci(data, confidence=0.95):
    """
    Compute Confidence Interval using t-distribution.
    Recommended for small sample sizes (N < 20) where bootstrap has poor coverage.
    
    Args:
        data: Array-like of observations
        confidence: Confidence level (0 to 1)
        
    Returns:
        tuple: (lower_bound, upper_bound)
    """
    data = np.array(data)
    n = len(data)
    if n < 2:
        return np.mean(data), np.mean(data)
        
    mean = np.mean(data)
    sem = stats.sem(data)
    
    # t critical value
    t_crit = stats.t.ppf((1 + confidence) / 2, df=n-1)
    
    margin = t_crit * sem
    return mean - margin, mean + margin

def compute_bootstrap_ci(data, confidence=0.95, n_resamples=10000, random_seed=42):
    """
    Compute Confidence Interval using Bootstrap BCa method.
    
    Args:
        data: Array-like of observations
        confidence: Confidence level
        n_resamples: Number of bootstrap resamples
        random_seed: Random seed for reproducibility
        
    Returns:
        tuple: (lower_bound, upper_bound)
    """
    data = np.array(data)
    n = len(data)
    
    if n < 20:
        warnings.warn(
            f"Bootstrap with N={n} may have poor coverage. Consider using t-distribution CIs instead.",
            UserWarning
        )
        
    rng = np.random.default_rng(random_seed)
    
    # Check if scipy supports BCa (requires >= 1.7 or 1.8 typically)
    # Our environment has 1.16.3, so we are good.
    try:
        res = stats.bootstrap(
            (data,),
            np.mean,
            confidence_level=confidence,
            n_resamples=n_resamples,
            method='BCa',
            random_state=rng
        )
        return res.confidence_interval.low, res.confidence_interval.high
    except Exception as e:
        warnings.warn(f"Bootstrap BCa failed: {e}. Falling back to percentile method.")
        # Fallback to percentile if BCa fails (e.g. all values identical)
        res = stats.bootstrap(
            (data,),
            np.mean,
            confidence_level=confidence,
            n_resamples=n_resamples,
            method='percentile',
            random_state=rng
        )
        return res.confidence_interval.low, res.confidence_interval.high

def compute_cis(data, confidence=0.95):
    """
    Compute CIs using both methods.
    
    Returns:
        dict: { 't_dist': (low, high), 'bootstrap': (low, high) }
    """
    t_low, t_high = compute_t_ci(data, confidence)
    
    # Capture warnings for bootstrap to not spam stdout during this call if possible,
    # or just let it warn once.
    with warnings.catch_warnings():
        warnings.simplefilter("always") # Let the user see the warning at least once
        boot_low, boot_high = compute_bootstrap_ci(data, confidence)
        
    return {
        "t_dist": (t_low, t_high),
        "bootstrap": (boot_low, boot_high)
    }
