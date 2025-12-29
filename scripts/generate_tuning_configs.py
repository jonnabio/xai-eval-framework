#!/usr/bin/env python3
"""
Generate tuning configurations for LIME parameters (EXP1-31).
User Story: EXP1-31
"""

import yaml
from pathlib import Path
import itertools
import numpy as np

def generate_configs():
    # Base config (template)
    # We'll hardcode the structure based on exp1_adult_xgb_lime.yaml
    base_config = {
        "name": "exp1_adult_xgb_lime_tuning",
        "description": "LIME Hyperparameter Tuning (EXP1-31)",
        "dataset": "adult",
        "version": "1.0.0",
        "random_seed": 42,
        "model": {
            "name": "xgboost",
            "path": "experiments/exp1_adult/models/xgboost/xgb_model.pkl"
        },
        "explainer": {
            "method": "lime",
            "num_features": 10,
            # params populated below
            "params": {}
        },
        "sampling": {
            "strategy": "stratified",
            "samples_per_class": 10,  # Reduced for tuning speed (total 40 instances)
            "random_seed": 42
        },
        "metrics": {
            "fidelity": True,
            "stability": True,  # Critical for valid comparison
            "sparsity": False,  # Not critical for tuning
            "cost": True,
            "stability_perturbations": 5,
            "stability_noise_level": 0.01
        }
    }

    # Parameter grid
    # "auto" for kernel_width means None (LIME default)
    # But user requested [0.25, 0.5, 0.75, 1.0, 2.0, "auto"]
    # We will map "auto" -> None in the yaml (or string "auto" if code handles it)
    
    # NOTE: LIME default kernel width is sqrt(num_features) * 0.75
    # For Adult, num_features after OHE is ~100? or 14? 
    # Current codebase uses preprocessed data.
    # We'll stick to the requested grid.
    
    kernel_widths = [0.25, 0.5, 0.75, 1.0, 2.0, "auto"]
    num_samples_list = [1000, 5000]
    feature_selection_list = ["auto", "none"]

    output_dir = Path("configs/experiments/tuning")
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for kw, ns, fs in itertools.product(kernel_widths, num_samples_list, feature_selection_list):
        # Create config copy
        config = base_config.copy()
        
        # Format filename params
        kw_str = str(kw) if kw != "auto" else "auto"
        
        # Config Name
        config_name = f"exp1_lime_k{kw_str}_n{ns}_fs{fs}"
        config["name"] = config_name
        
        # Output Dir
        config["output_dir"] = f"experiments/exp1_adult/results/tuning/{config_name}"
        
        # Explainer Params
        # We put everything in explainer.params (ExperimentRunner must handle this)
        # Note: num_samples is a first-class citizen in Schema but user wants to tune it.
        # We set top-level num_samples AND params for clarity
        config["explainer"]["num_samples"] = ns
        
        params = {
            "kernel_width": None if kw == "auto" else float(kw),
            "feature_selection": fs
        }
        config["explainer"]["params"] = params
        
        # Write File
        filename = f"{config_name}.yaml"
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            yaml.dump(config, f, sort_keys=False)
            
        count += 1
        print(f"Generated: {filepath}")

    print(f"Total configurations generated: {count}")

if __name__ == "__main__":
    generate_configs()
