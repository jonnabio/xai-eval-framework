"""
Example script showing how to use the LIME tabular wrapper.

This script demonstrates:
1. Loading trained models
2. Initializing LIME wrapper
3. Generating explanations for test instances
4. Interpreting results
"""

import sys
from pathlib import Path
import time

# Add src to path
# Script is in experiments/exp1_adult/examples/
# We need to reach root/src
# Path(__file__).resolve().parents[3] should be root
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'src'))

import numpy as np
import joblib

from data_loading.adult import load_adult
from xai.lime_tabular import LIMETabularWrapper, generate_lime_explanations

def main():
    print("=" * 80)
    print("LIME Tabular Wrapper - Example Usage")
    print("=" * 80)
    
    # Define paths
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parents[2]
    data_dir = project_root / 'data'
    models_dir = script_dir.parent / 'models'
    
    # 1. Load data
    print("\n1. Loading Adult dataset...")
    # Using load_adult from src.data_loading
    data_dict = load_adult(data_dir=str(data_dir), random_state=42)
    X_train = data_dict['X_train']
    X_test = data_dict['X_test']
    feature_names = data_dict['feature_names']
    
    print(f"   Training samples: {X_train.shape[0]}")
    print(f"   Test samples: {X_test.shape[0]}")
    print(f"   Features: {len(feature_names)}")
    
    # 2. Load trained model
    print("\n2. Loading trained Random Forest model...")
    # Assuming standard model name from run_train_models.py
    # Checks for 'rf' folder or 'adult_rf' folder depending on trainer.
    # The previous code saved to `models_dir / model_key`
    # Let's check for 'exp1_adult_rf' or similar.
    # If not found, we print instruction.
    
    # Try probable paths
    probable_paths = [
        models_dir / 'rf' / 'random_forest_model.joblib',
        models_dir / 'dummy_rf_model.joblib' # For testing environments
    ]
    
    model_path = None
    for p in probable_paths:
        if p.exists():
            model_path = p
            break
            
    if not model_path:
        # Fallback to recursively finding any .joblib in models dir
        candidates = list(models_dir.rglob("*.joblib"))
        if candidates:
            model_path = candidates[0]
            
    if not model_path or not model_path.exists():
        print(f"   ERROR: Model not found in {models_dir}")
        print("   Run experiments/exp1_adult/run_train_models.py first")
        return
    
    print(f"   Found model at: {model_path}")
    model = joblib.load(model_path)
    print("   Model loaded successfully")
    
    # 3. Initialize LIME wrapper
    print("\n3. Initializing LIME wrapper...")
    # Note: LIME might take a moment to discretize if enabled (disabled here)
    lime_wrapper = LIMETabularWrapper(
        training_data=X_train,
        feature_names=feature_names,
        num_features=10,
        num_samples=5000,
        random_state=42
    )
    print("   LIME wrapper initialized")
    print(f"   Config: {lime_wrapper.get_config()}")
    
    # 4. Generate explanations for a few test instances
    print("\n4. Generating LIME explanations for 5 test instances...")
    n_explain = 5
    X_explain = X_test[:n_explain]
    
    explanations = lime_wrapper.generate_explanations(
        model=model,
        X_samples=X_explain
    )
    
    print("   Explanations generated!")
    print(f"   Feature importance shape: {explanations['feature_importance'].shape}")
    print(f"   Top features shape: {explanations['top_features'].shape}")
    print(f"   Total time: {explanations['metadata']['total_time_seconds']:.2f}s")
    print(f"   Avg time per instance: {explanations['metadata']['avg_time_per_instance']:.2f}s")
    
    # 5. Display top features for first instance
    print("\n5. Top 10 features for first test instance:")
    instance_idx = 0
    top_feat_indices = explanations['top_features'][instance_idx]
    importances = explanations['feature_importance'][instance_idx]
    
    # Get probability
    if hasattr(model, 'predict_proba'):
        prob = model.predict_proba(X_explain[instance_idx:instance_idx+1])[0, 1]
    else:
        prob = float(model.predict(X_explain[instance_idx:instance_idx+1])[0])
        
    print(f"\n   Instance prediction (p): {prob:.3f}")
    print(f"\n   {'Rank':<6} {'Feature Name':<40} {'Importance':>12}")
    print(f"   {'-'*60}")
    
    for rank, feat_idx in enumerate(top_feat_indices, 1):
        if feat_idx == -1: continue # Handle padding if any
        feat_name = feature_names[feat_idx]
        importance = importances[feat_idx]
        print(f"   {rank:<6} {feat_name:<40} {importance:>12.4f}")
    
    # 6. Demonstrate single instance explanation
    print("\n6. Single instance explanation (alternative interface):")
    single_importance = lime_wrapper.explain_instance(
        model=model,
        instance=X_test[0]
    )
    print(f"   Importance vector shape: {single_importance.shape}")
    print(f"   Non-zero features: {np.count_nonzero(single_importance)}")
    
    # 7. Demonstrate convenience function
    print("\n7. Using convenience function (no wrapper initialization):")
    # Using smaller samples to be quick
    quick_explanations = generate_lime_explanations(
        model=model,
        X_samples=X_test[:2],
        training_data=X_train,
        feature_names=feature_names,
        num_features=5,
        num_samples=100  # Faster
    )
    print(f"   Generated explanations for {quick_explanations['metadata']['n_instances']} instances")
    
    print("\n" + "=" * 80)
    print("Example completed successfully!")
    print("=" * 80)


if __name__ == '__main__':
    main()
