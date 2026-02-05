#!/usr/bin/env python3
"""
Script to train missing models (SVM, MLP, LogisticRegression) for Experiment 1.
"""
import sys
import yaml
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.data_loading.adult import load_adult
from src.models.sklearn_trainers import SVMTrainer, MLPTrainer, LogisticRegressionTrainer
from src.models.xgboost_trainer import XGBoostTrainer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    # Load Data Once
    logger.info("Loading Adult Dataset...")
    try:
        # load_adult returns (X_train, X_test, y_train, y_test, feature_names, preprocessor)
        data = load_adult(verbose=True)
        X_train, X_test, y_train, y_test, feature_names, preprocessor = data
        
        # SAVE PREPROCESSOR
        # This is critical for ensuring the experiment runner uses the exact same feature transformation
        preprocessor_path = project_root / "experiments/exp1_adult/models/preprocessor.joblib"
        import joblib
        joblib.dump(preprocessor, preprocessor_path)
        logger.info(f"Saved preprocessor to {preprocessor_path}")
        
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        return 1

    models_to_train = [
        {
            "name": "SVM",
            "config": "experiments/exp1_adult/configs/models/svm_adult_config.yaml",
            "class": SVMTrainer
        },
        {
            "name": "MLP",
            "config": "experiments/exp1_adult/configs/models/mlp_adult_config.yaml",
            "class": MLPTrainer
        },
        {
            "name": "LogisticRegression",
            "config": "experiments/exp1_adult/configs/models/logreg_adult_config.yaml",
            "class": LogisticRegressionTrainer
        },
        {
            "name": "XGBoost",
            "config": "experiments/exp1_adult/configs/models/xgb_adult_config.yaml",
            "class": XGBoostTrainer
        }
    ]
    
    for item in models_to_train:
        try:
            name = item['name']
            logger.info(f"Starting {name} pipeline...")
            
            # Load config
            config_path = project_root / item['config']
            config = load_config(config_path)
            
            # Init
            trainer = item['class'](config['model']['params'])
            
            # Train
            trainer.train(X_train, y_train)
            
            # Evaluate
            metrics = trainer.evaluate(X_test, y_test)
            logger.info(f"{name} Results: accuracy={metrics.get('accuracy'):.4f}, roc_auc={metrics.get('roc_auc')}")
            
            # Save
            output_conf = config['output']
            save_dir = project_root / output_conf['models_dir']
            filename = output_conf['model_filename']
            
            # BaseTrainer.save takes dir and filename
            saved_path = trainer.save(save_dir, filename)
            logger.info(f"Saved {name} to {saved_path}")
            
        except Exception as e:
            logger.error(f"Failed to train {item['name']}: {e}", exc_info=True)
            # Continue to next model? Yes.
            
    logger.info("Training sequence completed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
