#!/usr/bin/env python
"""
Training Runner for Experiment 1 - Adult MVP.

Purpose:
    Orchestrates the end-to-end training pipeline for the Adult dataset.
    - Loads the dataset (cached).
    - Trains baseline models (Random Forest, XGBoost).
    - Evaluates performance.
    - Persists trained models and metrics.

Usage:
    python run_train_models.py [--config path/to/config.yaml]
    python run_train_models.py --help

Outputs:
    - Trained Models: saved to `models_dir` (e.g., experiments/exp1_adult/models/)
    - Metrics: saved to `metrics_dir` (CSV and Parquet)
    - Logs: saved to `log_dir`

Example:
    $ python run_train_models.py --config config/training_config.yaml
    INFO - Starting Experiment: exp1_adult_mvp
    INFO - Loaded Adult dataset: (32561, 108)
    INFO - Training RF...
    INFO - RF Accuracy: 0.8523, ROC-AUC: 0.9012
    INFO - Training XGBoost...
    INFO - XGBoost Accuracy: 0.8650, ROC-AUC: 0.9150
    INFO - Saved metrics to experiments/exp1_adult/results/

Author: Google Deepmind (Antigravity)
Date: 2025-12-17
Version: 1.0.0
"""

import argparse
import logging
import sys
import yaml
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import pandas as pd
import numpy as np

# Adjust path to include project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Internal Imports
from src.data_loading.adult import load_adult
from src.models.tabular_models import AdultRandomForestTrainer
from src.models.xgboost_trainer import XGBoostTrainer

# Custom Exception
class ConfigurationError(Exception):
    """Raised when configuration validation fails."""
    pass

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load and validate the training configuration.

    Args:
        config_path: Path to the YAML configuration file. 
                     If None, defaults to 'experiments/exp1_adult/config/training_config.yaml'.

    Returns:
        Dict containing the parsed configuration.

    Raises:
        ConfigurationError: If the file is missing, invalid YAML, or missing required sections.
    """
    # 1. Determine config path
    if config_path is None:
        # Default relative to project root. We use PROJECT_ROOT constant to be robust 
        # against where the script is invoked from (e.g. root vs experiment dir).
        config_path_obj = PROJECT_ROOT / "experiments/exp1_adult/config/training_config.yaml"
    else:
        config_path_obj = Path(config_path)

    # 2. Check existence
    if not config_path_obj.exists():
        raise ConfigurationError(f"Configuration file not found at: {config_path_obj}")

    # 3. Load YAML
    try:
        with open(config_path_obj, 'r') as f:
            # safe_load is used to prevent code execution vulnerabilities in YAML parsing
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Error parsing YAML configuration: {e}")
    except Exception as e:
        raise ConfigurationError(f"Unexpected error loading config: {e}")

    # 4. Validate Schema (Basic)
    required_sections = ['data', 'models', 'output']
    missing = [sec for sec in required_sections if sec not in config]
    
    if missing:
        raise ConfigurationError(f"Invalid configuration. Missing required sections: {missing}")
    
    # 5. Validate subsections (optional but recommended)
    if 'rf' not in config['models'] or 'xgboost' not in config['models']:
         raise ConfigurationError("Missing model configurations for 'rf' or 'xgboost'.")

    return config

def setup_logging(log_dir: str, experiment_name: str, verbose: bool = False) -> logging.Logger:
    """
    Configure logging to both console and file.

    Args:
        log_dir: Directory to store log files.
        experiment_name: Name of the experiment (prefix for log file).

    Returns:
        Configured logger instance.
    """
    # 1. Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # 2. Setup Logger
    logger = logging.getLogger(experiment_name)
    logger.setLevel(logging.DEBUG)  # Capture everything at the root level so file handler gets all details

    # Remove existing handlers if any (to avoid duplicates in interactive runs)
    if logger.hasHandlers():
        logger.handlers.clear()

    # 3. File Handler ( Detailed, DEBUG level)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file = log_path / f"{experiment_name}_{timestamp}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # 4. Console Handler (Concise, INFO level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    # 5. Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.debug(f"Logging initialized. Log file: {log_file}")
    
    return logger

def train_and_evaluate_model(
    trainer: Union[AdultRandomForestTrainer, XGBoostTrainer], 
    X_train: pd.DataFrame, 
    y_train: pd.Series, 
    X_test: pd.DataFrame, 
    y_test: pd.Series, 
    model_name: str, 
    logger: logging.Logger
) -> Dict[str, Any]:
    """
    Train a single model and evaluate its performance.

    Args:
        trainer: Instance of a trainer class (RF or XGBoost).
        X_train, y_train: Training data.
        X_test, y_test: Evaluation data.
        model_name: Identifier for the model (for logging).
        logger: Logger instance.

    Returns:
        Dictionary containing metrics and metadata:
        {
            'model': model_name,
            'training_time_sec': float,
            'accuracy': float,
            'roc_auc': float,
            'f1_score': float,
            ...other metrics
        }

    Raises:
        Exception: Re-raises any exception occurring during training.
    """
    logger.info(f"Starting training for model: {model_name}")
    start_time = time.time()

    try:
        # Train
        # Note: XGBoostTrainer supports validation set for early stopping, 
        # but for baseline consistency with RF, we use the standard interface here.
        trainer.train(X_train, y_train)
        
        # Evaluate
        metrics = trainer.evaluate(X_test, y_test)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Combine info
        result = {
            "model": model_name,
            "training_time_sec": round(duration, 4),
            **metrics
        }
        
        logger.info(f"Completed {model_name} in {duration:.2f}s")
        logger.info(f"{model_name} Metrics: Accuracy={metrics.get('accuracy', 0):.4f}, ROC-AUC={metrics.get('roc_auc', 0):.4f}")
        
        return result

    except Exception as e:
        logger.error(f"Failed to train {model_name}: {e}", exc_info=True)
        raise e

def save_metrics(metrics: List[Dict[str, Any]], output_path: str, logger: logging.Logger) -> None:
    """
    Save aggregated metrics to disk in multiple formats.

    Args:
        metrics: List of metric dictionaries from `train_and_evaluate_model`.
        output_path: Directory to save the metrics files.
        logger: Logger instance.

    Returns:
        None (saves files to disk).
    """
    if not metrics:
        logger.warning("No metrics to save.")
        return

    # 1. Prepare Directory
    out_dir = Path(output_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 2. Convert to DataFrame
    df = pd.DataFrame(metrics)
    
    # 3. Add Metadata
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    df['timestamp'] = timestamp
    # Note: version could be passed in, simpler to just rely on config log for deep details
    
    # 4. Define Filenames
    file_timestamp = time.strftime("%Y%m%d_%H%M%S")
    csv_path = out_dir / f"training_metrics_{file_timestamp}.csv"
    parquet_path = out_dir / f"training_metrics_{file_timestamp}.parquet"

    # 5. Save CSV (Human Readable)
    # CSV is preferred for quick manual inspection and Excel compatibility
    try:
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved metrics CSV to: {csv_path}")
    except Exception as e:
        logger.error(f"Failed to save metrics CSV: {e}")

    # 6. Save Parquet (Efficient / Type-safe)
    # Parquet preserves data types better than CSV and is faster for downstream loading
    try:
        df.to_parquet(parquet_path, index=False)
        logger.info(f"Saved metrics Parquet to: {parquet_path}")
    except Exception as e:
        logger.error(f"Failed to save metrics Parquet: {e}")

def main(config_path: Optional[str] = None, models_filter: str = "rf,xgboost", dry_run: bool = False, verbose: bool = False) -> None:
    """
    Main execution flow for the training runner.

    Args:
        config_path: Path to configuration file.

    Returns:
        None. Exits with code 0 on success, 1 on failure.
    """
    try:
        # 1. Load Configuration
        config = load_config(config_path)
        
        # 2. Setup Logging
        experiment_name = config['experiment'].get('name', 'exp1_adult')
        log_dir = config['output']['log_dir']
        logger = setup_logging(log_dir, experiment_name, verbose=verbose)
        
        logger.info(f"Starting Experiment: {experiment_name}")
        logger.debug(f"Configuration loaded: {config}")

        # 3. Load Data
        logger.info("Loading Adult dataset...")
        data_config = config['data']
        
        X_train, X_test, y_train, y_test, feature_names, preprocessor = load_adult(
            test_size=data_config['test_size'],
            random_state=data_config['random_state'],
            cache_dir=data_config['cache_dir'],
            preprocessor_path=data_config.get('preprocessor_output')
        )
        logger.info(f"Loaded Data: Train shape={X_train.shape}, Test shape={X_test.shape}")
        
        if dry_run:
            logger.info("Dry run mode enabled. Skipping training.")
            return

        # 4. Initialize Models
        trainers = {}
        allowed_models = [m.strip().lower() for m in models_filter.split(',')]
        
        # Random Forest
        if 'rf' in allowed_models:
            rf_config = config['models']['rf']
            logger.info("Initializing Random Forest...")
            trainers['rf'] = AdultRandomForestTrainer(rf_config)

        # XGBoost
        if 'xgboost' in allowed_models:
            xgb_config = config['models']['xgboost']
            logger.info("Initializing XGBoost...")
            trainers['xgboost'] = XGBoostTrainer(xgb_config)

        if not trainers:
            logger.warning(f"No valid models selected from {models_filter}. Available: rf, xgboost")
            return

        # 5. Train and Evaluate Loop
        metrics_list = []
        models_dir = Path(config['output']['models_dir'])
        models_dir.mkdir(parents=True, exist_ok=True)

        # Global list of models to run could be filtered here if we passed it as an arg
        # For now, we iterate over initialized trainers
        
        for model_key, trainer in trainers.items():
            try:
                # Train & Evaluate
                result = train_and_evaluate_model(
                    trainer, X_train, y_train, X_test, y_test, f"{experiment_name}_{model_key}", logger
                )
                metrics_list.append(result)
                
                # Save Model
                save_path = models_dir / f"{model_key}_model.pkl" # Simplified name for clarity
                # Or use the save() method if available on trainer specific to directory
                if hasattr(trainer, 'save'):
                     # The trainers save method usually takes a directory and handles filenames/metadata
                     # Let's create a specific subdir for each model to store full artifacts (json, feature importance etc)
                     model_subdir = models_dir / model_key
                     model_subdir.mkdir(exist_ok=True)
                     trainer.save(model_subdir)
                     logger.info(f"Saved {model_key} artifacts to {model_subdir}")
                else:
                     logger.warning(f"Trainer for {model_key} does not have a save() method.")

            except Exception as e:
                logger.error(f"Skipping {model_key} due to error: {e}")
                continue

        # 6. Save Aggregated Metrics
        logger.info("Saving aggregated metrics...")
        save_metrics(metrics_list, config['output']['metrics_dir'], logger)

        # 7. Summary
        if metrics_list:
             best_model = max(metrics_list, key=lambda x: x.get('roc_auc', 0))
             logger.info("-" * 40)
             logger.info(f"Experiment Completed Successfully.")
             logger.info(f"Models Trained: {len(metrics_list)}")
             logger.info(f"Best Model (ROC-AUC): {best_model['model']} ({best_model.get('roc_auc', 0):.4f})")
             logger.info("-" * 40)
        else:
             logger.warning("No models were successfully trained.")
             sys.exit(1)

    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal Error: {e}")
        # If logger exists, log it too
        if 'logger' in locals():
            logger.critical(f"Fatal unhandled exception: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run Experiment 1 (Adult MVP) Training Pipeline",
        epilog="Example: python run_train_models.py --config config/my_config.yaml"
    )
    
    parser.add_argument(
        "--config", 
        type=str, 
        help="Path to YAML configuration file. Default: config/training_config.yaml"
    )
    
    parser.add_argument(
        "--models", 
        type=str, 
        default="rf,xgboost",
        help="Comma-separated list of models to train. Default: 'rf,xgboost'"
    )
    
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Validate validation and data loading without training."
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose (DEBUG) logging to console."
    )

    args = parser.parse_args()
    
    try:
        main(
            config_path=args.config,
            models_filter=args.models,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
        sys.exit(130)
