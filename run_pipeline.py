#!/usr/bin/env python3
"""
Master pipeline execution script for XAI Evaluation Framework.
This script orchestrates the steps:
1. Environment verification
2. Data preparation
3. Model training (skipped if exists)
4. Experiment execution (skipped if exists)

It is used by start.sh during deployment.
"""

import argparse
import subprocess
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("pipeline")

def run_command(command, description):
    """Run a shell command with error handling."""
    logger.info(f"Step: {description}")
    try:
        # Use shell=True for complex commands or ensure args are list
        # Here we split simple commands for security/best practice if possible, 
        # but shell scripts need shell=True or direct invocation.
        subprocess.run(command, shell=True, check=True)
        logger.info(f"✅ {description} completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed with exit code {e.returncode}")
        # We might want to suppress error if we want to proceed to API start
        # But for the pipeline, failure usually means we should stop or warn.
        # propagate error to caller
        raise e

def main():
    parser = argparse.ArgumentParser(description="Run XAI Evaluation Pipeline")
    parser.add_argument("--mode", type=str, default="minimal", help="Pipeline mode (minimal, complete)")
    args = parser.parse_args()

    pipeline_script = Path("experiments/exp1_adult/reproducibility_package/run_full_pipeline.sh")
    
    if not pipeline_script.exists():
        logger.error(f"Pipeline script not found at {pipeline_script}")
        sys.exit(1)

    # Ensure executable
    pipeline_script.chmod(pipeline_script.stat().st_mode | 0o111)

    logger.info(f"Starting pipeline in {args.mode} mode...")
    
    try:
        # Execute the existing shell orchestration script
        # This preserves all the logic (Step 1..7) defined there.
        run_command(f"bash {pipeline_script} --mode {args.mode}", "Full Pipeline Execution")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        # Exit with error so start.sh knows
        sys.exit(1)

if __name__ == "__main__":
    main()
