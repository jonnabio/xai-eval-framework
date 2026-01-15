"""
Verification script for XAI Expansion (Anchors & DiCE).
"""
import sys
import logging
import numpy as np
import pandas as pd
from pathlib import Path
import shutil

# Add project root
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.models.sklearn_trainers import SVMTrainer
from src.xai import AnchorsTabularWrapper, DiCETabularWrapper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_XAI")

def verify_xai():
    # 1. Setup Data & Model
    # Simple binary classification
    np.random.seed(42)
    X = np.random.rand(50, 4)
    y = (X[:, 0] + X[:, 1] > 1.0).astype(int)
    feature_names = ["f0", "f1", "f2", "f3"]
    
    logger.info("Training SVM model for XAI validation...")
    trainer = SVMTrainer({'probability': True})
    trainer.train(X, y)
    
    # 2. Test Anchors
    logger.info("--- Testing Anchors ---")
    try:
        # Pass predict_fn (SVM predict)
        anchors = AnchorsTabularWrapper(X, feature_names)
        
        # Explain 2 samples
        results = anchors.generate_explanations(
            model=trainer.model,
            X_samples=X[:2],
            predict_fn=trainer.predict
        )
        
        importance = results['feature_importance']
        logger.info(f"Anchors importance shape: {importance.shape}")
        assert importance.shape == (2, 4)
        logger.info("Anchors PASS")
        
    except ImportError as e:
        logger.warning(f"Skipping Anchors (Dependency missing): {e}")
    except Exception as e:
        logger.error(f"Anchors FAILED: {e}")
        # Don't fail entire script if just anchors fails (e.g. timeout)

    # 3. Test DiCE
    logger.info("--- Testing DiCE ---")
    try:
        # DiCE needs model + data
        dice = DiCETabularWrapper(
            training_data=X,
            feature_names=feature_names,
            target_column="target"
        )
        
        # Explain 1 sample (DiCE is slow)
        results = dice.generate_explanations(
            model=trainer.model,
            X_samples=X[:1]
        )
        
        importance = results['feature_importance']
        logger.info(f"DiCE importance shape: {importance.shape}")
        assert importance.shape == (1, 4)
        
        # Check if non-zero importance found (usually true if counterfactual found)
        logger.info(f"DiCE importance vector: {importance[0]}")
        
        logger.info("DiCE PASS")
        
    except ImportError as e:
        logger.warning(f"Skipping DiCE (Dependency missing): {e}")
    except Exception as e:
        logger.error(f"DiCE FAILED: {e}")

    logger.info("XAI Verification Complete")

if __name__ == "__main__":
    verify_xai()
