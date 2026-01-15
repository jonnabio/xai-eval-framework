"""
Verification script for Generic Model Trainers.
Tests:
1. Factory registration/retrieval.
2. Training/Prediction for all generic types (RF, XGB, SVM, MLP, LogReg).
3. Standardized metrics output.
"""
import sys
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import shutil

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.models.factory import ModelTrainerFactory
from src.models.base import BaseTrainer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY")

def verify_trainers():
    # 1. Verify Registry
    supported = ModelTrainerFactory.list_supported_models()
    logger.info(f"Supported Models: {supported}")
    expected = ['svm', 'mlp', 'logreg', 'rf', 'random_forest', 'xgb', 'xgboost']
    assert all(m in supported for m in expected), f"Missing models! Found: {supported}"
    
    # 2. Synthetic Data
    X = pd.DataFrame(np.random.rand(100, 5), columns=[f"feat_{i}" for i in range(5)])
    y = np.random.randint(0, 2, 100)
    
    # 3. Test Each Trainer
    models_to_test = ['rf', 'xgb', 'svm', 'mlp', 'logreg']
    
    for model_type in models_to_test:
        logger.info(f"--- Testing {model_type.upper()} ---")
        try:
            # Instantiate
            config = {}
            if model_type == 'mlp':
                config['max_iter'] = 200 # speed up test
                
            trainer = ModelTrainerFactory.get_trainer(model_type, config)
            assert isinstance(trainer, BaseTrainer)
            
            # Train
            trainer.train(X, y)
            
            # Evaluate
            metrics = trainer.evaluate(X, y)
            logger.info(f"{model_type} metrics: {metrics}")
            
            # Check essential metrics exist
            assert 'accuracy' in metrics
            assert 'f1' in metrics
            
            # Save/Load Roundtrip
            tmp_dir = Path("tmp_verification") / model_type
            save_path = trainer.save(tmp_dir)
            
            loaded_trainer = trainer.load(tmp_dir)
            assert loaded_trainer.model is not None
            
            logger.info(f"{model_type} PASS")
            
        except Exception as e:
            logger.error(f"{model_type} FAILED: {e}")
            raise e

    # Cleanup
    if Path("tmp_verification").exists():
        shutil.rmtree("tmp_verification")
        
    logger.info("ALL CHECKS PASSED")

if __name__ == "__main__":
    verify_trainers()
