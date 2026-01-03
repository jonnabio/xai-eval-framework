
import numpy as np
import pandas as pd
from scipy import stats
import scikit_posthocs as sp

def perform_friedman_test(data_dict: dict):
    """
    Perform Friedman Test for global differences.
    
    Args:
        data_dict: Dictionary mapping method names to lists/arrays of scores (must be same length).
                   e.g., {'rf_lime': [0.1, 0.2], 'rf_shap': [0.15, 0.25]}
                   
    Returns:
        tuple: (statistic, p_value)
    """
    # Convert to matrix where cols are methods, rows are folds
    df = pd.DataFrame(data_dict)
    
    # Check assumptions
    if len(df) < 5:
        # Friedman test is not reliable for N < 5
        pass 
        
    stat, p = stats.friedmanchisquare(*[df[col] for col in df.columns])
    return stat, p

def perform_nemenyi_test(data_df: pd.DataFrame):
    """
    Perform Nemenyi Post-Hoc Test.
    
    Args:
        data_df: DataFrame where index=folds, columns=methods.
        
    Returns:
        pd.DataFrame: Pairwise p-values.
    """
    # scikit-posthocs expects data in a specific format
    # The 'melt' format is safer: val_col='score', group_col='method', block_col='fold'
    
    # Or simpler: sp.posthoc_nemenyi_friedman(a) where a is the matrix
    # But checking docs, if input is DataFrame, it treats columns as groups?
    # sp.posthoc_nemenyi_friedman(x) takes an array of arrays or DataFrame
    
    p_values = sp.posthoc_nemenyi_friedman(data_df)
    return p_values

def compute_cohens_dz(x, y):
    """
    Compute Cohen's d_z for paired samples.
    
    d_z = mean(d) / std(d)
    where d = x - y
    """
    x = np.array(x)
    y = np.array(y)
    d = x - y
    
    mean_d = np.mean(d)
    std_d = np.std(d, ddof=1) # Sample std dev
    
    if std_d == 0:
        return 0.0
        
    return mean_d / std_d

def estimate_power(n, effect_size, alpha=0.05):
    """
    Estimate power for a one-sample t-test (closest approx for paired difference)
    given sample size N and effect size.
    """
    from statsmodels.stats.power import TTestPower
    power_analysis = TTestPower()
    power = power_analysis.solve_power(effect_size=effect_size, nobs=n, alpha=alpha, alternative='two-sided')
    return power
