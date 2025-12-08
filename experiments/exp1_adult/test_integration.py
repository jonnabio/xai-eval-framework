import sys
import os
import logging
import numpy as np
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.data_loading.adult import load_adult, _fetch_adult_data, _clean_data, TARGET_COLUMN
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import shap
import lime
import lime.lime_tabular

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_integration():
    logger.info("Starting Integration Test...")

    # 1. Load Data
    logger.info("1. Loading Adult Dataset...")
    X_train, X_test, y_train, y_test, feature_names, preprocessor = load_adult(
        test_size=0.01, # Small test split for speed
        random_state=42,
        verbose=False
    )
    logger.info(f"   Data loaded. X_train: {X_train.shape}, features: {len(feature_names)}")

    # 2. Sklearn Model Compatibility
    logger.info("2. Testing Sklearn LogisticRegression...")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train[:1000], y_train[:1000]) # Train on subset for speed
    
    preds = model.predict(X_test[:100])
    acc = accuracy_score(y_test[:100], preds)
    logger.info(f"   Model trained. Test Accuracy (subset): {acc:.4f}")
    assert acc > 0.5, "Model accuracy should be better than random"

    # 3. Preprocessor Single Sample Transformation
    logger.info("3. Testing Preprocessor on new data...")
    # Fetch a raw sample manually to simulate new data
    raw_df = _fetch_adult_data()
    clean_df = _clean_data(raw_df)
    raw_sample = clean_df.drop(columns=[TARGET_COLUMN]).iloc[[0]]
    
    # Transform
    transformed_sample = preprocessor.transform(raw_sample)
    assert transformed_sample.shape == (1, X_train.shape[1])
    logger.info("   Preprocessor transformed raw sample successfully.")

    # 4. Feature Name Alignment
    logger.info("4. Checking Feature Names...")
    assert len(feature_names) == X_train.shape[1]
    # Check if coefficients align (just dimension check)
    assert len(model.coef_[0]) == len(feature_names)
    logger.info("   Feature names align with model coefficients.")

    # 5. XAI Library Compatibility
    logger.info("5. Testing XAI Libraries...")
    
    # SHAP (KernelExplainer as it's model agnostic)
    logger.info("   Testing SHAP...")
    # Summarize background to 5 samples
    background = shap.kmeans(X_train[:50], 5) 
    explainer_shap = shap.KernelExplainer(model.predict_proba, background)
    shap_values = explainer_shap.shap_values(X_test[:2], nsamples=100)
    assert np.array(shap_values).shape[0] == 2 or np.array(shap_values).shape[1] == 2 # Depends on return type (list of arrays or array)
    logger.info("   SHAP KernelExplainer ran successfully.")

    # LIME
    logger.info("   Testing LIME...")
    explainer_lime = lime.lime_tabular.LimeTabularExplainer(
        X_train[:100], 
        feature_names=feature_names, 
        class_names=['<=50K', '>50K'], 
        discretize_continuous=True
    )
    exp = explainer_lime.explain_instance(X_test[0], model.predict_proba, num_features=5)
    assert exp is not None
    logger.info("   LIME explainer ran successfully.")

    logger.info("\nSUCCESS: All integration tests passed!")

if __name__ == "__main__":
    try:
        test_integration()
    except Exception as e:
        logger.error(f"Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
