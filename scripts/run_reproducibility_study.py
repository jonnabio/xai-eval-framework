#!/usr/bin/env python3
"""
Reproducibility Study Runner for EXP1.

Executes experiments multiple times with different random seeds to measure
metric stability and calculate Coefficient of Variation (CV).
"""

import argparse
import logging
import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path
from copy import deepcopy

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.experiment.config import load_config
from src.experiment.runner import ExperimentRunner

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Run reproducibility study")
    parser.add_argument(
        '--config-dir',
        type=Path,
        default=Path("configs/experiments"),
        help="Directory containing experiment configs"
    )
    parser.add_argument(
        '--seeds',
        type=int,
        default=10,
        help="Number of seeds to run (default: 10)"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path("experiments/exp1_adult/reproducibility"),
        help="Output directory for study results"
    )
    parser.add_argument(
        '--pattern',
        type=str,
        default="exp1_adult_*.yaml",
        help="Config file pattern"
    )
    
    args = parser.parse_args()
    
    # Setup output
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Discover configs
    if not args.config_dir.exists():
        logger.error(f"Config dir not found: {args.config_dir}")
        return 1
        
    config_files = list(args.config_dir.glob(args.pattern))
    if not config_files:
        logger.error(f"No configs found matching {args.pattern}")
        return 1
        
    logger.info(f"Found {len(config_files)} configurations to test.")
    
    combined_results = []
    
    # 2. Execution Loop
    for config_path in config_files:
        logger.info(f"=== Starting Study for {config_path.stem} ===")
        
        # Base config
        base_config = load_config(config_path)
        metric_samples = []
        
        # Specific output dir for this experiment's study
        exp_study_dir = args.output_dir / base_config.name
        exp_study_dir.mkdir(exist_ok=True)
        
        for i in range(args.seeds):
            seed = 42 + i
            logger.info(f"  Run {i+1}/{args.seeds} (Seed {seed})")
            
            # Create seeded config
            # We modify the object in place but rely on Runner to use it
            # Deepcopy to avoid pollution between runs
            # Actually, reusing the object might be tricky if Runner modifies it.
            # Best to reload or deepcopy.
            # config objects are pydantic models, .copy() is shallow.
            
            # Re-loading is safest
            current_config = load_config(config_path)
            current_config.random_seed = seed
            current_config.sampling.random_seed = seed # Ensure data sampling also varies? 
            # Ideally we want to test stability of EXPLANATION given same model/data?
            # Or stability of entire pipeline? 
            # Usually reproducibility means: same seed -> same result.
            # Stability means: different seed -> similar result (robustness).
            # We are testing STABILITY/ROBUSTNESS here by varying seed.
            
            # Modifying output dir to avoid overwrite/conflict
            current_config.output_dir = exp_study_dir / f"seed_{seed}"
            
            try:
                runner = ExperimentRunner(current_config)
                # Suppress runner logs if possible?
                result = runner.run()
                
                # Extract aggregated metrics
                aggs = result.get('aggregated_metrics', {})
                flat_metrics = {'seed': seed}
                
                for m, stats in aggs.items():
                    if 'mean' in stats:
                        flat_metrics[m] = stats['mean']
                
                metric_samples.append(flat_metrics)
                
            except Exception as e:
                logger.error(f"Failed run {i} for {base_config.name}: {e}")
                
        # 3. Analyze Results for this Config
        if not metric_samples:
            logger.warning(f"No successful runs for {base_config.name}")
            continue
            
        df = pd.DataFrame(metric_samples)
        
        # Calculate CV
        stats = {
            'experiment': base_config.name,
            'n_runs': len(df)
        }
        
        # Metrics columns (exclude seed)
        metric_cols = [c for c in df.columns if c != 'seed']
        
        for m in metric_cols:
            mean = df[m].mean()
            std = df[m].std()
            cv = std / mean if mean != 0 else 0.0
            
            stats[f"{m}_mean"] = mean
            stats[f"{m}_std"] = std
            stats[f"{m}_cv"] = cv
            
        combined_results.append(stats)
        
        # Save raw samples
        df.to_csv(exp_study_dir / "samples.csv", index=False)
        logger.info(f"Saved samples to {exp_study_dir}/samples.csv")

    # 4. Final Report
    if combined_results:
        report_df = pd.DataFrame(combined_results)
        report_path = args.output_dir / "reproducibility_report.csv"
        report_df.to_csv(report_path, index=False)
        
        logger.info("="*50)
        logger.info(f"Study Complete. Report saved to: {report_path}")
        logger.info("="*50)
        
        # Print summary of CVs
        print("\nCoefficient of Variation (CV) Summary:")
        # Filter for CV columns
        cv_cols = [c for c in report_df.columns if c.endswith('_cv')]
        print(report_df[['experiment'] + cv_cols].to_string())
            
    else:
        logger.error("No results generated.")
        return 1
        
    return 0

if __name__ == "__main__":
    main()
