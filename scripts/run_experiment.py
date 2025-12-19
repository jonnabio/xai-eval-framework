#!/usr/bin/env python3
"""
CLI script to run XAI evaluation experiments.

Usage:
    python scripts/run_experiment.py --config configs/experiments/exp1_adult_rf_shap.yaml
    python scripts/run_experiment.py --config configs/experiments/exp1_adult_xgb_lime.yaml --verbose
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
# Assuming script is in scripts/ and project root is parent
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.experiment.config import load_config
from src.experiment.runner import ExperimentRunner

def setup_logging(verbose: bool = False) -> None:
    """Configure logging for experiment execution."""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Ensure logs dir exists
    log_dir = project_root / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / 'experiment_runner.log', mode='a', encoding='utf-8')
        ]
    )

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run XAI evaluation experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--config',
        type=Path,
        required=True,
        help='Path to experiment configuration YAML'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        # Verify config existence (done inside load_config too, but informative)
        if not args.config.exists():
            logger.error(f"Config file not found: {args.config}")
            return 1
            
        logger.info(f"Loading configuration from: {args.config}")
        config = load_config(args.config)
        
        # Initialize runner
        runner = ExperimentRunner(config)
        
        # Execute experiment
        results = runner.run()
        
        # Print summary
        print("\n" + "="*80)
        print(f"EXPERIMENT COMPLETE: {config.name}")
        print("="*80)
        print(f"Results saved to: {config.output_dir}")
        print("\nAggregated Metrics:")
        
        aggs = results.get('aggregated_metrics', {})
        if not aggs:
            print("  No metrics computed.")
        else:
            for metric, stats in aggs.items():
                print(f"  {metric.upper()}: {stats['mean']:.4f} \u00b1 {stats['std']:.4f}")
        print("="*80 + "\n")
        
        return 0
        
    except Exception as e:
        logger.error(f"Experiment failed: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
