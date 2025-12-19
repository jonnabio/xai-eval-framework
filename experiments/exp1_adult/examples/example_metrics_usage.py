"""
Example script showing how to use the XAI Metrics Framework.

This script demonstrates:
1. Loading the Evaluation Dataset (created by Sampler)
2. Generating explanations for a subset of samples (LIME)
3. Calculating Fidelity, Stability, Sparsity, and Cost
4. Reporting results
"""
import sys
import time
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from tqdm import tqdm

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'src'))

from xai.lime_tabular import LIMETabularWrapper
from metrics import (
    FidelityMetric, 
    StabilityMetric, 
    SparsityMetric, 
    CostMetric
)

def main():
    print("=" * 80)
    print("XAI Metrics Evaluation - Example Usage")
    print("=" * 80)
    
    # Paths
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parents[2]
    data_dir = project_root / 'data'
    models_dir = script_dir.parent / 'models'
    
    eval_path = data_dir / 'processed/eval_instances.csv'
    model_path = models_dir / 'xgboost/xgboost_model.joblib'
    
    # 1. Load Data & Model
    print("\n1. Loading Resources...")
    if not eval_path.exists():
        print(f"Error: {eval_path} not found. Run scripts/generate_eval_instances.py first.")
        return
        
    eval_df = pd.read_csv(eval_path)
    print(f"   Loaded {len(eval_df)} evaluation instances.")
    
    if not model_path.exists():
        # Try RF
        model_path = models_dir / 'rf/random_forest_model.joblib'
    
    if not model_path.exists():
        print("Error: No trained model found.")
        return
        
    print(f"   Loading model from {model_path}...")
    model = joblib.load(model_path)
    
    # Needs training data for LIME initialization (load small subset or expect user handled it)
    # For this example, we'll try to load the training data again via the loader OR
    # just warn. The wrapper usually needs training data stats.
    # Let's import the loader to be safe.
    from data_loading.adult import load_adult
    data_dict = load_adult(data_dir=str(data_dir), random_state=42)
    X_train = data_dict['X_train']
    feature_names = data_dict['feature_names']
    
    # 2. Initialize Wrapper & Metrics
    print("\n2. Initializing Components...")
    lime_wrapper = LIMETabularWrapper(
        model=model,
        training_data=X_train,
        feature_names=feature_names,
        random_state=42
    )
    
    metrics = {
        'Fidelity': FidelityMetric(n_samples=1000), # Lower samples for speed in demo
        'Stability': StabilityMetric(n_iterations=5),
        'Sparsity': SparsityMetric(threshold=0.05),
        'Cost': CostMetric()
    }
    
    # 3. Run Evaluation Loop
    # Select 3 samples: 1 TP, 1 TN, 1 FP (if available)
    quadrants = ['TP', 'TN', 'FP', 'FN']
    samples_to_run = []
    
    for q in quadrants:
        subset = eval_df[eval_df['quadrant'] == q]
        if not subset.empty:
            samples_to_run.append(subset.iloc[0])
            
    print(f"\n3. Evaluating {len(samples_to_run)} representative instances...")
    
    results = []
    
    # Helper for stability re-generation
    def explainer_func(m, d):
        # explain_instance returns (weights, metadata)
        # Stability expects dict with 'feature_importance'
        w = lime_wrapper.explain_instance(m, d, return_full=False)
        return {'feature_importance': w}

    for i, row in enumerate(tqdm(samples_to_run)):
        # Prep data
        meta_cols = ['original_index', 'target', 'prediction', 'quadrant']
        instance_data = row.drop(labels=meta_cols).values.astype(float)
        
        row_res = {
            'id': row['original_index'], 
            'quadrant': row['quadrant']
        }
        
        # A. Generate Explanation & Cost
        start_t = time.perf_counter()
        weights, meta = lime_wrapper.explain_instance(model, instance_data, return_full=True)
        end_t = time.perf_counter()
        
        # B. Calculate Metrics
        
        # Cost (Time)
        row_res['Time(ms)'] = (end_t - start_t) * 1000
        
        # Sparsity
        s_res = metrics['Sparsity'].compute(weights)
        row_res['Sparsity(%)'] = s_res['nonzero_percentage'] * 100
        row_res['Gini'] = s_res['gini_index']
        
        # Fidelity
        f_res = metrics['Fidelity'].compute(weights, model=model, data=instance_data)
        row_res['Fidelity(R2)'] = f_res['r2_score']
        
        # Stability
        stab_res = metrics['Stability'].compute(
            None, model=model, data=instance_data, explainer_func=explainer_func
        )
        row_res['Stability(Cos)'] = stab_res['cosine_similarity_mean']
        
        results.append(row_res)
        
    # 4. Report
    print("\n4. Evaluation Results:")
    res_df = pd.DataFrame(results)
    
    # Format for display
    print(res_df.to_string(index=False, float_format=lambda x: "{:.4f}".format(x)))
    
    print("\nDone.")

if __name__ == '__main__':
    main()
