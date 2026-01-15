"""
Train a dummy SVM model for testing the runner integration.
"""
import sys
import logging
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

# Add project root
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.models.sklearn_trainers import SVMTrainer
from src.data_loading.adult import load_adult

logging.basicConfig(level=logging.INFO)

def train_dummy_svm():
    # Load data
    X_train, X_test, y_train, y_test, feature_names, _ = load_adult()
    
    # Train small SVM (on subset for speed)
    X_small = X_train[:500]
    y_small = y_train[:500]
    
    trainer = SVMTrainer({'probability': True})
    trainer.train(X_small, y_small)
    
    # Save to location expected by config
    save_dir = Path("experiments/exp1_adult/models")
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # BaseTrainer.save() usually saves to dir/model_name
    # But here we want to control the filename to match config
    # SVMTrainer.save() -> BaseTrainer.save() saves 'model.joblib' and 'metadata.json' ? 
    # Let's just manually save for this quick test to match 'test_svm.joblib'
    
    joblib.dump(trainer.model, save_dir / "test_svm.joblib")
    print(f"Saved dummy SVM to {save_dir / 'test_svm.joblib'}")

if __name__ == "__main__":
    train_dummy_svm()
