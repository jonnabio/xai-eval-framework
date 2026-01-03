
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Union, Any, Optional
from pathlib import Path
import json

def compute_cv(values: List[float]) -> float:
    """
    Compute Coefficient of Variation (sigma / mu).
    
    Args:
        values: List of numerical values.
        
    Returns:
        CV value (0.0 if mean is 0).
    """
    values = np.array(values)
    mean_val = np.mean(values)
    if mean_val == 0:
        return 0.0
    return np.std(values) / mean_val

def compute_percent_change(current: float, baseline: float) -> float:
    """
    Compute percentage change from baseline.
    
    Args:
        current: Current value.
        baseline: Baseline value.
        
    Returns:
        Percentage change (e.g., 5.0 for 5% increase).
    """
    if baseline == 0:
        return 0.0 if current == 0 else float('inf')
    return ((current - baseline) / baseline) * 100.0

def detect_plateau(params: List[Union[int, float]], metrics: List[float], threshold_pct: float = 1.0) -> Union[int, float]:
    """
    Detect the parameter value where increasing it yields diminishing returns (< 1% improvement).
    Assumes params are sorted ascending.
    
    Args:
        params: List of parameter values (e.g. [500, 1000, ...]).
        metrics: List of corresponding metric values.
        threshold_pct: Percentage threshold for "significant improvement".
        
    Returns:
        The parameter value where the plateau effectively starts (or is reached).
    """
    if len(params) < 2:
        return params[0]
        
    # We look for the first point i where the change to i+1 is negligible
    # Or rather, we want the point where we CAN STOP.
    # If metric[i+1] vs metric[i] is small, then i might be enough? 
    # Or do we look for when the curve flattens?
    # Let's say: The plateau is the value P where moving to any P' > P yields < threshold change.
    
    # Simple greedy approach: 
    # Iterate from left. If (next - current)/current < threshold, then current is sufficient?
    # BUT, we might have noise.
    # Let's check improvement relative to the *previous* step.
    
    # Recommendation logic:
    # "Use 2000" means 2000 is the start of the plateau. 
    # So moving from 1000 to 2000 gave a boost, but 2000 to 5000 did not.
    
    best_param = params[-1] # Default to max acting as strict 
    
    for i in range(len(params) - 1):
        current_val = metrics[i]
        next_val = metrics[i+1]
        
        # Handle zero division or small values
        denom = abs(current_val) if abs(current_val) > 1e-9 else 1.0
        
        # Calculate relative change
        # Improvement could be positive or negative depending on metric direction (cost vs fidelity)
        # We take absolute change magnitude
        rel_change = abs(next_val - current_val) / denom * 100.0
        
        if rel_change < threshold_pct:
            # Found a step with little change. 
            # If this persists? 
            # Let's simplify: return the first param where the NEXT step is negligible.
            return params[i]
            
    return params[-1]

def classify_sensitivity(cv: float) -> str:
    """
    Classify sensitivity based on CV.
    
    Args:
        cv: Coefficient of variation.
        
    Returns:
        'robust' (<0.05), 'moderate' (0.05-0.10), or 'sensitive' (>0.10).
    """
    if cv < 0.05:
        return "robust"
    elif cv < 0.10:
        return "moderate"
    else:
        return "sensitive"

def generate_recommendations(sensitivity_data: Dict) -> Dict:
    """
    Generate recommendations based on sensitivity analysis results.
    
    Args:
        sensitivity_data: Dictionary containing results for a specific parameter/setup.
                          Structure: {'values': [], 'metrics': {'fidelity': {'absolute_values': []}}}
    
    Returns:
        Dict of recommendation strings/rationales.
    """
    # This acts as a helper to extract simple recommendations
    # Implementation depends on the exact JSON structure passed
    pass 

def plot_sensitivity_curves(
    results: Dict[str, Any], 
    param_name: str, 
    metric_names: List[str],
    output_dir: Union[str, Path]
):
    """
    Plot sensitivity curves for multiple metrics vs a parameter.
    
    Args:
        results: Dictionary containing 'rf_lime', 'xgb_lime' etc.
        param_name: Name of the parameter (X-axis).
        metric_names: List of metrics to plot (Y-axis).
        output_dir: Directory to save plots.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # We likely want one plot per metric, showing lines for different models
    
    for metric in metric_names:
        plt.figure(figsize=(10, 6))
        
        # Collect data for this metric from all available models in results
        # Keys in results like 'rf_lime', 'xgb_lime'
        
        models_plotted = False
        
        for model_key, data in results.items():
            if metric not in data['metrics']:
                continue
                
            xs = data['values']
            ys = data['metrics'][metric]['absolute_values']
            baseline = data['metrics'][metric]['baseline_value']
            
            # Plot Curve
            plt.plot(xs, ys, marker='o', label=f"{model_key} (Curve)")
            
            # Plot Baseline (Horizontal Line)
            # Use color cycle or specific style
            color = plt.gca().lines[-1].get_color()
            plt.axhline(y=baseline, linestyle='--', alpha=0.5, color=color, label=f"{model_key} (Baseline)")
            
            # Add shaded region +/- 5% around baseline
            plt.fill_between(
                xs, 
                [baseline * 0.95] * len(xs), 
                [baseline * 1.05] * len(xs), 
                color=color, alpha=0.1
            )
            
            models_plotted = True
            
        if models_plotted:
            plt.title(f"Sensitivity of {metric} to {param_name}")
            plt.xlabel(param_name)
            plt.ylabel(metric)
            plt.xscale('log') # Params are log-scale
            plt.grid(True, which="both", ls="-", alpha=0.2)
            plt.legend()
            
            safe_metric = metric.replace(" ", "_").lower()
            plt.savefig(output_dir / f"sensitivity_{param_name}_{safe_metric}.png", dpi=300)
            plt.close()
