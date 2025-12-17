"""
Training script for XGBoost on Adult Dataset (Experiment 1).

This script orchestrates the training pipeline:
1. Loads processed Adult dataset.
2. Initializes XGBoostTrainer with specified (or default) hyperparameters.
3. Trains the model with early stopping.
4. Evaluates performance on the test set.
5. Saves the model and artifacts.

Usage:
    python train_xgb.py --n_estimators 100 --max_depth 6 --output_dir models/
"""

import sys
import argparse
import logging
from pathlib import Path
import json

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

import yaml

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.data_loading.adult import load_adult
from src.models.xgboost_trainer import XGBoostTrainer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Train XGBoost on Adult Dataset")
    parser.add_argument("--config", type=str, help="Path to YAML configuration file", 
                       default="configs/xgb_config.yaml")
    
    # CLI Overrides (optional, take precedence over config file if provided)
    parser.add_argument("--n_estimators", type=int, help="Number of boosting rounds")
    parser.add_argument("--max_depth", type=int, help="Maximum tree depth")
    parser.add_argument("--learning_rate", type=float, help="Step size shrinkage")
    parser.add_argument("--output_dir", type=str, help="Directory to save artifacts")
    
    args = parser.parse_args()
    
    # 1. Load Config
    config_path = Path(__file__).parent / args.config
    if config_path.exists():
        logger.info(f"Loading configuration from {config_path}")
        config = load_config(config_path)
    else:
        logger.warning(f"Config file not found at {config_path}. Using internal defaults.")
        config = {'model': {}}

    # 2. CLI Overrides
    if args.n_estimators:
        config['model']['n_estimators'] = args.n_estimators
        logger.info(f"Overriding n_estimators with CLI arg: {args.n_estimators}")
    if args.max_depth:
        config['model']['max_depth'] = args.max_depth
        logger.info(f"Overriding max_depth with CLI arg: {args.max_depth}")
    if args.learning_rate:
        config['model']['learning_rate'] = args.learning_rate
        logger.info(f"Overriding learning_rate with CLI arg: {args.learning_rate}")
    
    # Resolve Output Directory
    output_dir = args.output_dir if args.output_dir else config.get('output', {}).get('model_dir', 'models')
    
    # 3. Load Data
    logger.info("Loading Adult dataset...")
    X_train, X_test, y_train, y_test = load_adult()
    
    X_val, y_val = X_test, y_test

    # 4. Initialize Trainer (passing model config section)
    logger.info(f"Initializing XGBoostTrainer with model config: {config.get('model', {})}")
    trainer = XGBoostTrainer(config=config.get('model', {}))
    
    # 5. Train
    logger.info("Starting training...")
    trainer.train(X_train, y_train, X_val=X_val, y_val=y_val)
    
    # 6. Evaluate
    logger.info("Evaluating on test set...")
    metrics = trainer.evaluate(X_test, y_test)
    
    print("\nTraining Completed.")
    print("Test Metrics:")
    print(json.dumps(metrics, indent=2))
    
    # 7. Save
    save_path = Path(__file__).parent / output_dir
    logger.info(f"Saving artifacts to {save_path}...")
    trainer.save(save_path)
    print(f"\nModel saved to: {save_path}")

if __name__ == "__main__":
    main()
