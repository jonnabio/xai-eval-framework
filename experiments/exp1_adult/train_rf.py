#!/usr/bin/env python
# User Story: EXP1-08
"""
Train Random Forest model for Experiment 1.
Executable script to run training with configuration.
"""

import sys
import os
import argparse
import logging
import json
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

# Import training function
try:
    from src.models.tabular_models import train_random_forest_adult
except ImportError as e:
    print(f"Error importing model module: {e}")
    sys.exit(1)

def setup_logging(verbose: bool):
    """Configure logging with timestamp."""
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Train Random Forest for Experiment 1")
    parser.add_argument(
        "--config", 
        type=str, 
        default="experiments/exp1_adult/configs/models/rf_adult_config.yaml",
        help="Path to config file"
    )
    parser.add_argument(
        "--force", 
        action="store_true", 
        help="Force retraining"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        default=True, 
        help="Enable detailed logging"
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("EXP1: Random Forest Training Started")
    logger.info("=" * 60)
    
    start_time = time.time()
    
    try:
        # Check config existence
        if not os.path.exists(args.config):
            logger.error(f"Config file not found: {args.config}")
            logger.info(f"Current working directory: {os.getcwd()}")
            sys.exit(1)
            
        # Run training
        logger.info(f"Using config: {args.config}")
        model, metrics = train_random_forest_adult(
            config_path=args.config,
            force_retrain=args.force_retrain,
            verbose=args.verbose
        )
        
        # Report results
        execution_time = time.time() - start_time
        
        logger.info("-" * 60)
        logger.info("Training Completed Successfully")
        logger.info(f"Total Execution Time: {execution_time:.2f} seconds")
        
        if metrics:
            logger.info("Key Metrics:")
            logger.info(f"  Accuracy:  {metrics.get('test_accuracy', 'N/A')}")
            logger.info(f"  ROC AUC:   {metrics.get('test_roc_auc', 'N/A')}")
            logger.info(f"  F1 Macro:  {metrics.get('test_f1_macro', 'N/A')}")
            
            # Print full metrics to console for debug/pipe
            if args.verbose:
                logger.info("Full Metrics JSON:")
                print(json.dumps(metrics, indent=2,  default=str))
                
    except Exception as e:
        logger.error(f"Training Failed: {str(e)}", exc_info=True)
        sys.exit(1)
        
if __name__ == "__main__":
    main()
