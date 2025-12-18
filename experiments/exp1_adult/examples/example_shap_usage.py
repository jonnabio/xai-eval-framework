"""
Example script showing how to use the SHAP Tabular Wrapper.

This script demonstrates:
1. Loading trained models (XGBoost/RF)
2. Sampling background data
3. Initializing SHAP wrapper
4. Generating explanations
5. Validating additivity
"""

import sys
from pathlib import Path
import numpy as np
import joblib

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'src'))

from data_loading.adult import load_adult
from xai.shap_tabular import (
    SHAPTabularWrapper, 
    generate_shap_explanations,
    validate_shap_additivity
)

def main():
    print("=" * 80)
    print("SHAP Tabular Wrapper - Usage Example")
    print("=" * 80)
    
    # Paths
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parents[2]
    data_dir = project_root / 'data'
    models_dir = script_dir.parent / 'models'
    
    # 1. Load Data
    print("\n1. Loading Adult dataset...")
    data_dict = load_adult(data_dir=str(data_dir), random_state=42)
    X_train = data_dict['X_train']
    X_test = data_dict['X_test']
    feature_names = data_dict['feature_names']
    
    # 2. Load Model
    print("\n2. Loading trained model...")
    # Prefer XGBoost for SHAP demo if available, else RF
    xgb_path = models_dir / 'xgboost' / 'xgboost_model.joblib'
    rf_path = models_dir / 'rf' / 'random_forest_model.joblib'
    
    if xgb_path.exists():
        model_path = xgb_path
        model_type = "tree"
        print(f"   Using XGBoost model at {model_path}")
    elif rf_path.exists():
        model_path = rf_path
        model_type = "tree"
        print(f"   Using RF model at {model_path}")
    else:
        print("   No model found. Please run training first.")
        return

    model = joblib.load(model_path)
    
    # 3. Initialize Wrapper
    print("\n3. Initializing SHAP wrapper...")
    # Note: We pass X_train to be sampled for background
    wrapper = SHAPTabularWrapper(
        model=model,
        training_data=X_train,
        feature_names=feature_names,
        model_type=model_type,
        n_background_samples=100,
        random_state=42
    )
    print(f"   Initialized with background shape: {wrapper.background_data.shape}")
    print(f"   Expected Value (Base Rate): {wrapper.expected_value:.4f}")
    
    # 4. Explain
    print("\n4. Explaining 5 test instances...")
    X_explain = X_test[:5]
    
    # Get predictions for validation
    if hasattr(model, 'predict_proba'):
        preds = model.predict_proba(X_explain)[:, 1]
    else:
        # Fallback if model just returns class
        preds = model.predict(X_explain)
        
    results = wrapper.generate_explanations(model, X_explain)
    
    shap_values = results['feature_importance']
    print(f"   SHAP Values Shape: {shap_values.shape}")
    
    # 5. Validate Additivity
    print("\n5. Validating Additivity Property...")
    is_valid, max_err = validate_shap_additivity(
        shap_values, 
        wrapper.expected_value, 
        preds
    )
    status = "PASSED" if is_valid else "FAILED"
    print(f"   Additivity Check: {status} (Max Error: {max_err:.2e})")
    
    # 6. Top Features
    print("\n6. Top Features for Instance 0:")
    top_indices = results['top_features'][0]
    instance_shap = shap_values[0]
    
    print(f"   Prediction: {preds[0]:.4f}")
    print(f"   Base Value: {wrapper.expected_value:.4f}")
    print(f"   Sum(SHAP):  {np.sum(instance_shap):.4f}")
    print("-" * 60)
    print(f"   {'Rank':<6} {'Feature':<30} {'SHAP Value':>12}")
    print("-" * 60)
    
    for rank, idx in enumerate(top_indices[:10], 1):
        print(f"   {rank:<6} {feature_names[idx]:<30} {instance_shap[idx]:>12.4f}")

    print("\n" + "=" * 80)

if __name__ == '__main__':
    main()
