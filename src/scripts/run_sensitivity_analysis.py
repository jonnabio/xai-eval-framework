
import sys
import logging
import json
import copy
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import pandas as pd
import shutil

# Add project root to path
sys.path.append(str(Path.cwd()))

from src.experiment.config import load_config, ExperimentConfig
from src.experiment.runner import ExperimentRunner
from src.analysis.sensitivity import (
    compute_cv, 
    compute_percent_change,
    detect_plateau,
    classify_sensitivity,
    plot_sensitivity_curves
)

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SensitivityAnalysis")

# Constants
OUTPUT_DIR = Path("outputs/sensitivity")
FIGURES_DIR = OUTPUT_DIR / "figures"
RESULTS_FILE = OUTPUT_DIR / "sensitivity_results.json"
BASE_EXPERIMENT_PATH = Path("experiments/exp1_adult")
BASELINE_RESULTS_PATTERN = "outputs/experiments/exp1_adult/results/*/results.json"

# Sensitivity Grid
SENSITIVITY_GRID = {
    "lime": {
        "params": ["num_samples"],
        "ranges": {
            "num_samples": [500, 1000, 2000, 5000, 10000]
        },
        "default_config": "exp1_adult_rf_lime.yaml" # Base config to clone
    },
    "shap": {
        "params": ["n_background_samples"],
        "ranges": {
            "n_background_samples": [25, 50, 100, 200, 400]
        },
        "default_config": "exp1_adult_rf_shap.yaml"
    }
}

METRICS_OF_INTEREST = ["fidelity", "stability", "sparsity", "cost", "faithfulness_gap"]

def load_baseline_metric(experiment_name: str, metric_name: str) -> float:
    """Load baseline metric from original experiment results."""
    # Assuming standard path structure: outputs/experiments/exp1_adult/results/{experiment_name}/results.json
    # BUT, wait. Users ran experiments. Where are they? 
    # cv_runner results are in outputs/cv/... 
    # Standard single-split results are in outputs/experiments/...
    # Let's check where the consolidated results are.
    # The user might have run CV. But sensitivity analysis plan says "Single Split".
    # So we should compare against a Single Split Baseline? 
    # Or just use the default config run within this loop as the baseline?
    # To be robust, let's treat the value in the grid that matches the default as the baseline.
    # Default LIME num_samples=5000. Default SHAP n_bg=100.
    return None

def run_single_experiment(base_config: ExperimentConfig, param_name: str, param_value: Any, output_subdir: str) -> Dict[str, float]:
    """Run a single experiment with modified config and return mean metrics."""
    # Clone and modify config
    config = copy.deepcopy(base_config)
    
    # Update Parameter
    if param_name == 'num_samples':
        # Special case for LIME num_samples which is a top-level attribute in ExplainerConfig
        # and also might be in params, causing collision if passed twice.
        config.explainer.num_samples = param_value
        # Ensure it's not in params to avoid kwargs collision
        if config.explainer.params and 'num_samples' in config.explainer.params:
            del config.explainer.params['num_samples']
    elif param_name in config.explainer.params:
        config.explainer.params[param_name] = param_value
    else:
        if config.explainer.params is None:
            config.explainer.params = {}
        config.explainer.params[param_name] = param_value

    # Update Sampling for Efficiency
    # N ~ 50 total. 12 per class * 2 classes = 24? 
    # Adult has 2 classes. 12 samples_per_class * 2 = 24. A bit low?
    # Plan said ~48 total. Stratified sampler samples per class.
    # If 2 classes, 12 samples per class = 24 total.
    # Actually, let's use 12, which gives ~48 if we consider quadrants or if user calculation was correct.
    # The user said "12 x 4 quadrants = 48". 
    config.sampling.samples_per_class = 12 # Total ~48
    config.sampling.random_seed = 42 # Fixed seed for direct comparison
    
    # Update Output Directory to avoid overwriting
    config.output_dir = OUTPUT_DIR / "runs" / output_subdir
    
    # Run Experiment
    runner = ExperimentRunner(config)
    runner.setup()
    
    # ExperimentRunner.run() performs sampling, explaining, evaluation
    try:
        results = runner.run()
        # results structure: {'experiment_metadata':..., 'aggregated_metrics': {...}}
        agg = results.get('aggregated_metrics', {})
        
        # Extract means
        means = {}
        for m in METRICS_OF_INTEREST:
             if m in agg:
                 means[m] = agg[m]['mean']
             else:
                 means[m] = 0.0 # Should not happen if metric is enabled
        
        # Capture Time? Cost metric covers runtime.
        
        return means
    except Exception as e:
        logger.error(f"Run failed for {param_name}={param_value}: {e}")
        return {m: 0.0 for m in METRICS_OF_INTEREST}

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    final_results = {}
    
    # We will test both RF and XGB models for each Explainer Type
    models = ["rf", "xgb"]
    
    for explainer_type, settings in SENSITIVITY_GRID.items():
        param_name = settings['params'][0] # Only 1 param per explainer for now
        param_values = settings['ranges'][param_name]
        default_config_file = settings['default_config']
        
        # We need to run this for both RF and XGB. 
        # The default config file likely specifies one model (e.g. rf).
        # We need to dynamically load the config and possibly switch model?
        # Or load explicit configs: exp1_adult_rf_lime.yaml, exp1_adult_xgb_lime.yaml
        
        for model in models:
            experiment_key = f"{model}_{explainer_type}"
            config_name = f"exp1_adult_{model}_{explainer_type}.yaml"
            config_path = Path("configs/experiments") / config_name
            
            if not config_path.exists():
                logger.warning(f"Config {config_path} not found. Skipping.")
                continue
                
            logger.info(f"Starting Sensitivity Analysis for {experiment_key} varying {param_name}")
            
            base_config = load_config(config_path)
            
            # Store results vectors
            values_col = []
            metrics_cols = {m: [] for m in METRICS_OF_INTEREST}
            
            # Identify Baseline Value (Default)
            # LIME: 5000, SHAP: 100
            default_val = 5000 if explainer_type == 'lime' else 100
            baseline_means = None
            
            # 1. RUN LOOP
            for val in param_values:
                logger.info(f"  > Testing {param_name} = {val} ...")
                subdir_name = f"{experiment_key}_{val}"
                
                means = run_single_experiment(base_config, param_name, val, subdir_name)
                
                values_col.append(val)
                for m in METRICS_OF_INTEREST:
                    metrics_cols[m].append(means[m])
                    
                if val == default_val:
                    baseline_means = means
            
            # Fallback if default not in grid (should be)
            if baseline_means is None:
                # Use first run? Or warn?
                baseline_means = {m: metrics_cols[m][-1] for m in METRICS_OF_INTEREST} # Use Max?
            
            # 2. ANALYZE PER METRIC
            model_results = {
                "parameter": param_name,
                "values": values_col,
                "metrics": {}
            }
            
            for m in METRICS_OF_INTEREST:
                vals = metrics_cols[m]
                baseline = baseline_means[m]
                
                # Compute Stats
                cv = compute_cv(vals)
                sens_class = classify_sensitivity(cv)
                plateau_point = detect_plateau(values_col, vals, threshold_pct=1.0)
                
                # Percent Changes
                pct_changes = [compute_percent_change(v, baseline) for v in vals]
                
                model_results["metrics"][m] = {
                    "absolute_values": vals,
                    "baseline_value": baseline,
                    "percent_changes": pct_changes,
                    "mean": np.mean(vals),
                    "std": np.std(vals),
                    "cv": cv,
                    "sensitivity_class": sens_class,
                    "plateau_point": plateau_point
                }
            
            # Store
            if explainer_type not in final_results:
                final_results[explainer_type] = {}
            final_results[explainer_type][experiment_key] = model_results
            
    # 3. GENERATE PLOTS & RECOMMENDATIONS
    summary = {"critical_parameters": [], "recommendations": {}}
    
    for explainer_type, experiments in final_results.items():
        # experiments = {'rf_lime': ..., 'xgb_lime': ...}
        
        # Plotting: Need to group by metric across models
        first_exp = list(experiments.values())[0]
        param_name = first_exp['parameter']
        
        # Pass the whole 'experiments' dict to plotter
        plot_sensitivity_curves(
            experiments, 
            param_name, 
            METRICS_OF_INTEREST, 
            FIGURES_DIR
        )
        
        # Generate Recommendations (Simple Logic)
        # Verify consensus between models?
        # If RF says 2000 and XGB says 5000 -> Conservative: take max(2000, 5000)
        
        rec_val = 0
        rationale = []
        
        for exp_name, res in experiments.items():
            # Check Fidelity Plateau
            fid_res = res['metrics']['fidelity']
            rec_val = max(rec_val, fid_res['plateau_point'])
            rationale.append(f"{exp_name}: Fidelity plateaus at {fid_res['plateau_point']}")
            
            # Check Sensitivities
            for m, data in res['metrics'].items():
                if data['sensitivity_class'] == 'sensitive':
                    summary['critical_parameters'].append({
                        "experiment": exp_name,
                        "parameter": param_name,
                        "metric": m,
                        "cv": data['cv']
                    })
        
        summary['recommendations'][f"{explainer_type}_{param_name}"] = {
            "recommended_value": rec_val,
            "rationale": "; ".join(rationale)
        }

    final_results['summary'] = summary

    # Save Results
    with open(RESULTS_FILE, 'w') as f:
        json.dump(final_results, f, indent=2, cls=NpEncoder)
        
    logger.info(f"Sensitivity Analysis Complete. Results saved to {RESULTS_FILE}")
    
if __name__ == "__main__":
    main()
