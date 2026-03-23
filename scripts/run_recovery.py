#!/usr/bin/env python3
"""
Recovery script for skipped XAI experiments.

Target specific configurations that were skipped in the main batch run:
- MLP + SHAP
- SVM + SHAP
- Anchors (All)
- DiCE (All)

Usage:
    python scripts/run_recovery.py --config-dir configs/experiments/exp2_scaled --workers 1
"""

import argparse
import logging
import sys
from pathlib import Path
import pandas as pd

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.experiment.utils import get_default_workers

from src.experiment.batch_runner import BatchExperimentRunner

def setup_logging(verbose: bool = False) -> None:
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    
    log_dir = project_root / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / 'recovery_runner.log', mode='a')
        ]
    )

def main():  # noqa: C901
    parser = argparse.ArgumentParser(description="Run recovery experiments")
    
    parser.add_argument(
        '--config-dir', 
        type=Path, 
        required=True,
        help="Directory containing YAML configuration files"
    )
    
    parser.add_argument(
        '--pattern',
        type=str,
        default="*.yaml",
        help="Glob pattern for config files (default: *.yaml)"
    )
    
    parser.add_argument(
        '--target',
        type=str,
        default="all",
        choices=["all", "shap", "anchors", "dice"],
        help="Specific recovery target (shap=MLP/SVM SHAP)"
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=None,
        help='Number of worker processes (default: based on RESERVED_CORES)'
    )
    
    args = parser.parse_args()
    
    # Determine number of workers
    workers = args.workers if args.workers is not None else get_default_workers()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("="*80)
    print("RECOVERY EXPERIMENT RUNNER")
    print("="*80)
    
    if not args.config_dir.exists():
        logger.error(f"Config directory not found: {args.config_dir}")
        return 1
        
    all_files = list(args.config_dir.glob(args.pattern))
    recovery_files = []
    
    logger.info(f"Scanning {len(all_files)} files in {args.config_dir} for recovery candidates...")
    
    for f in all_files:
        name = f.name
        # logic to identify skipped items
        is_skipped = False
        
        if "anchors" in name:
            if args.target in ["all", "anchors"]: is_skipped = True
        elif "dice" in name:
            if args.target in ["all", "dice"]: is_skipped = True
        elif "mlp_shap" in name or "svm_shap" in name:
             if args.target in ["all", "shap"]: is_skipped = True
             
        if is_skipped:
            recovery_files.append(f)
            
    if not recovery_files:
        logger.warning(f"No recovery candidates found matching target='{args.target}'.")
        return 0
        
    logger.info(f"Found {len(recovery_files)} experiments to recover.")
    
    # Initialize Runner
    runner = BatchExperimentRunner(recovery_files)
    
    # Run
    try:
        df, _ = runner.run(parallel=(workers > 1), max_workers=workers)
        
        # Save Results 
        output_dir = project_root / "outputs"
        output_dir.mkdir(exist_ok=True)
        output_csv = output_dir / "recovery_results.csv"
        
        df.to_csv(output_csv, index=False)
        logger.info(f"Saved recovery summary to {output_csv}")
        
    except Exception as e:
        logger.error(f"Recovery failed: {e}", exc_info=True)
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
