#!/usr/bin/env python
# User Story: EXP1-08
"""
Integration test for Random Forest training pipeline.
Verifies end-to-end functionality: Data Load -> Train -> Save -> Load -> Predict.
"""

import sys
import os
import json
import yaml
import shutil
import logging
from pathlib import Path
import traceback

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.models.tabular_models import train_random_forest_adult, load_trained_model
from src.data_loading.adult import load_adult

# Configure simple logging
logging.basicConfig(level=logging.INFO, format='[TEST] %(message)s')
logger = logging.getLogger(__name__)

def run_integration_test():
    """Execute the full integration test."""
    logger.info("Starting Integration Test...")
    
    # Setup temporary directory
    temp_dir = Path("temp_test_integration")
    temp_dir.mkdir(exist_ok=True)
    
    model_dir = temp_dir / "models"
    results_dir = temp_dir / "results"
    
    config_path = temp_dir / "test_config.yaml"
    
    try:
        # 1. Create Test Config
        logger.info("1. Creating temporary configuration...")
        default_config_path = PROJECT_ROOT / "experiments/exp1_adult/configs/models/rf_adult_config.yaml"
        
        with open(default_config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Update paths
        config['output']['model_dir'] = str(model_dir)
        config['output']['results_dir'] = str(results_dir)
        # Use faster training parameters for test
        config['model']['params']['n_estimators'] = 5
        
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
            
        # 2. Run Training
        logger.info("2. Running training pipeline...")
        model, metrics = train_random_forest_adult(
            config_path=str(config_path),
            force_retrain=True,
            verbose=False # Keep it cleaner
        )
        
        if model is None or not metrics:
            raise RuntimeError("Training returned None or empty metrics")
        logger.info("   Training successful.")
            
        # 3. Verify Files Exist
        logger.info("3. Verifying output files...")
        expected_files = [
            model_dir / config['output']['model_filename'],
            model_dir / f"{Path(config['output']['model_filename']).stem}_metadata.json",
            results_dir / config['output']['metrics_filename'],
            results_dir / "rf_feature_importance.csv"
        ]
        
        for p in expected_files:
            if not p.exists():
                raise FileNotFoundError(f"Expected output file missing: {p}")
            logger.info(f"   Found: {p.name}")
            
        # 4. Load Model & Predict
        logger.info("4. Testing model loading and inference...")
        loaded_model = load_trained_model(str(expected_files[0]))
        
        # Load small sample of data
        data = load_adult()
        X_test = data[1][:5] # First 5 samples
        
        # Predict
        preds = loaded_model.predict(X_test)
        logger.info(f"   Made {len(preds)} predictions: {preds}")
        
        # 5. Verify Feature Importance
        logger.info("5. Verifying feature importance...")
        import pandas as pd
        fi_df = pd.read_csv(expected_files[3])
        if len(fi_df) == 0:
            raise ValueError("Feature importance CSV is empty")
        if 'feature' not in fi_df.columns or 'importance' not in fi_df.columns:
            raise ValueError("Feature importance CSV missing columns")
        logger.info(f"   Verified feature importance for {len(fi_df)} features.")

        logger.info("-" * 40)
        logger.info("SUCCESS: Integration Test Passed!")
        logger.info("-" * 40)
        
    except Exception as e:
        logger.error(f"FAILURE: Integration Test Failed - {str(e)}")
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        # Cleanup
        logger.info("Cleaning up temporary test files...")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    run_integration_test()
