import sys
import numpy as np
import pandas as pd
from pathlib import Path
import json

project_root = Path("/home/jonnabio/Documents/GitHub/xai-eval-framework")
sys.path.insert(0, str(project_root))

def analyze_stability():
    from src.api.services.data_loader import find_result_files, load_json_file, get_experiments_dir
    
    base_dir = get_experiments_dir()
    all_files = find_result_files(base_dir)
    
    data = []
    
    for f in all_files:
        res = load_json_file(f)
        if not res: continue
        
        aggs = res.get("aggregated_metrics", {})
        model_info = res.get("model_info", {})
        meta = res.get("experiment_metadata", {})
        
        # Normalize aggs keys to lowercase for robust lookup
        aggs_lower = {k.lower(): v for k, v in aggs.items()}
        
        if not aggs_lower or 'stability' not in aggs_lower: continue
        
        stability_val = aggs_lower.get('stability')
        if isinstance(stability_val, dict):
            stability_val = stability_val.get('mean')
            
        if stability_val is None: continue
        
        data.append({
            'path': str(f),
            'model': model_info.get('name'),
            'method': model_info.get('explainer_method'),
            'stability': stability_val,
            'is_recovery': 'recovery' in str(f) or 'exp_recov_p1' in str(f),
            'seed': meta.get('random_seed')
        })
        
    df = pd.DataFrame(data)
    if df.empty:
        print("No stability data found.")
        return

    # Focus on SHAP Stability
    shap_df = df[df['method'] == 'shap']
    
    print("=== SHAP Stability Analysis ===")
    print("\nBy Model Type (All):")
    stats = shap_df.groupby('model')['stability'].agg(['mean', 'std', 'count']).sort_values('mean', ascending=False)
    print(stats)
    
    print("\nLegacy vs Recovery (SHAP):")
    print(shap_df.groupby('is_recovery')['stability'].agg(['mean', 'std', 'count']))

    # Check SVM Specifically
    svm_shap = shap_df[shap_df['model'] == 'adult_svm']
    if not svm_shap.empty:
        print("\nSVM SHAP Stability Breakdown:")
        print(svm_shap.groupby('is_recovery')['stability'].agg(['mean', 'std', 'count']))
        
        # Print top/bottom seeds for SVM if count > 1
        if len(svm_shap) > 1:
            print("\nDetailed SVM SHAP Stability (Sample):")
            print(svm_shap[['stability', 'seed', 'is_recovery']].sort_values('stability', ascending=False).head(10))

if __name__ == "__main__":
    analyze_stability()
