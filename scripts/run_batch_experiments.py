#!/usr/bin/env python3
"""
CLI entry point for batch experiment execution.

Usage:
    python scripts/run_batch_experiments.py --config-dir configs/experiments --output outputs/batch_results.csv --parallel
"""

import argparse
import logging
import sys
import json
import git
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

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
            logging.FileHandler(log_dir / 'batch_runner.log', mode='a')
        ]
    )

def check_git_status(require_clean: bool = True) -> str:
    """Check if git repo is clean."""
    try:
        repo = git.Repo(project_root, search_parent_directories=True)
        if repo.is_dirty(untracked_files=True):
            status = "DIRTY"
            msg = "Repository has uncommitted changes."
            if require_clean:
                logging.warning(f"{msg} Reproducibility not guaranteed.")
                # We warn but don't hard stop unless strictly enforced, 
                # to allow rapid dev iterations. 
                # For strict mode, we could raise.
        else:
            status = "CLEAN"
            
        return f"{status} ({repo.head.object.hexsha[:7]})"
    except Exception as e:
        logging.warning(f"Could not determine git status: {e}")
        return "UNKNOWN"

def main():
    parser = argparse.ArgumentParser(description="Run batch experiments")
    
    parser.add_argument(
        '--config-dir', 
        type=Path, 
        required=True,
        help="Directory containing YAML configuration files"
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=Path("outputs/batch_results.csv"),
        help="Path to save aggregated CSV results"
    )
    
    parser.add_argument(
        '--pattern',
        type=str,
        default="*.yaml",
        help="Glob pattern for config files (default: *.yaml)"
    )
    
    parser.add_argument(
        '--parallel',
        action='store_true',
        help="Run experiments in parallel"
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=2,
        help="Number of worker processes (default: 2)"
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    print("="*80)
    print("BATCH EXPERIMENT RUNNER")
    print("="*80)
    
    # Git Check
    git_status = check_git_status()
    logger.info(f"Git Status: {git_status}")
    
    # Discovery
    if not args.config_dir.exists():
        logger.error(f"Config directory not found: {args.config_dir}")
        return 1
        
    config_files = list(args.config_dir.glob(args.pattern))
    if not config_files:
        logger.error(f"No config files found in {args.config_dir} matching {args.pattern}")
        return 1
        
    # Initialize Runner
    runner = BatchExperimentRunner(config_files)
    
    # Run
    try:
        df, manifest = runner.run(parallel=args.parallel, max_workers=args.workers)
        
        # Save Results
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output, index=False)
        logger.info(f"Saved results to satisfy {args.output}")
        
        # Save Manifest
        manifest_path = args.output.parent / "batch_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        logger.info(f"Saved manifest to {manifest_path}")
        
        # Summary
        total = len(manifest["executions"])
        passed = sum(1 for e in manifest["executions"] if e["status"] == "success")
        skipped = sum(1 for e in manifest["executions"] if e["status"] == "skipped")
        failed = total - passed - skipped
        
        print("\n" + "="*80)
        print(f"BATCH COMPLETE")
        print(f"Total: {total} | Passed: {passed} | Skipped: {skipped} | Failed: {failed}")
        print(f"Results: {args.output}")
        print("="*80 + "\n")
        
        if failed > 0:
            print("WARNING: Some experiments failed. Check logs.")
            return 1
            
        return 0
        
    except Exception as e:
        logger.error(f"Critical Batch Error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
