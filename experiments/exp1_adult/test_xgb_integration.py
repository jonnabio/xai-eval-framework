#!/usr/bin/env python
"""
Integration test for XGBoost training pipeline.
Verifies end-to-end functionality: Data Load -> Train -> Save -> Load -> Predict.
"""

import sys
import shutil
import logging
from pathlib import Path
import yaml
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.models.xgboost_trainer import XGBoostTrainer
from src.data_loading.adult import load_adult

# Configure simple logging
logging.basicConfig(level=logging.INFO, format='[TEST] %(message)s')
logger = logging.getLogger(__name__)

def run_integration_test():
    """
    Execute the full end-to-end integration test for XGBoost.

    Context:
        Verifies that all components of the pipeline (loading, training, evaluating, 
        saving, loading, prediction) work together in the runtime environment.
        Crucial for preventing regression before deployment.

    Test Cases:
        1. Data Loading: Load Adult dataset.
        2. Training: Train XGBoost with valid config.
        3. Evaluation: Compute metrics.
        4. Persistence: Save artifacts to disk.
        5. Verification: Load back and confirm predictions match.
        6. Cleanup: Remove temporary files.

    Expected Behavior:
        - Script runs to completion without errors.
        - "Integration Test PASSED Successfully" is logged.
        - Temporary files are cleaned up.

    Related Tasks:
        EXP1-09
    """
    logger.info("Starting XGBoost Integration Test...")
    
    # Setup temporary directory
    temp_dir = Path("temp_test_xgb_integration")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # 1. Load Data
        logger.info("1. Loading Adult dataset...")
        X_train, X_test, y_train, y_test = load_adult()
        
        # Use subset for speed
        X_train_sub = X_train.iloc[:500]
        y_train_sub = y_train.iloc[:500]
        X_test_sub = X_test.iloc[:100]
        y_test_sub = y_test.iloc[:100]

        # 2. Train XGBoost
        logger.info("2. Training XGBoost model...")
        config = {
            'n_estimators': 10,  # Fast training
            'max_depth': 3,
            'learning_rate': 0.1,
            'output': {'model_dir': str(temp_dir)}
        }
        
        trainer = XGBoostTrainer(config)
        trainer.train(X_train_sub, y_train_sub, X_val=X_test_sub, y_val=y_test_sub)
        
        # 3. Evaluate
        logger.info("3. Evaluating model...")
        metrics = trainer.evaluate(X_test_sub, y_test_sub)
        logger.info(f"Metrics: accuracy={metrics['accuracy']:.4f}")
        
        # Get predictions before saving
        preds_orig = trainer.predict(X_test_sub)

        # 4. Save Artifacts
        logger.info("4. Saving artifacts...")
        trainer.save(temp_dir)
        
        # 5. Load and Verify
        logger.info("5. Loading model and verifying predictions...")
        loaded_trainer = XGBoostTrainer.load(temp_dir)
        preds_loaded = loaded_trainer.predict(X_test_sub)
        
        if not np.array_equal(preds_orig, preds_loaded):
            raise ValueError("Predictions do not match after loading!")
        logger.info("Predictions match confirmed.")
        
        # 6. Check Files
        logger.info("6. Verifying artifact existence...")
        expected_files = [
            "xgb_model.pkl",
            "xgb_model_metadata.json",
            "xgb_metrics.json",
            "xgb_feature_importance.csv"
        ]
        
        for fname in expected_files:
            if not (temp_dir / fname).exists():
                raise FileNotFoundError(f"Missing artifact: {fname}")
        logger.info("All artifacts found.")
        
        logger.info("Integration Test PASSED Successfully.")
        
    except Exception as e:
        logger.error(f"Integration Test FAILED: {e}")
        raise e
        
    finally:
        # 7. Cleanup
        if temp_dir.exists():
            logger.info("7. Cleaning up temporary files...")
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    run_integration_test()
