import pandas as pd
import numpy as np
import scipy.stats as stats
import json
import os
import glob
import sys

def run_analysis():
    print("=== Starting Metric Correlation Analysis ===")
    
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # experiments/exp1_adult
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(base_dir))) # root
    
    llm_results_path = os.path.join(base_dir, "llm_eval", "results_full.json")
    results_dir = os.path.join(base_dir, "results")
    
    # 1. Load LLM Data
    print(f"Loading LLM results from: {llm_results_path}")
    if not os.path.exists(llm_results_path):
        print(f"ERROR: File not found: {llm_results_path}")
        return

    with open(llm_results_path, 'r') as f:
        llm_data = json.load(f)

    flat_llm_data = []
    for record in llm_data:
        flat_record = {
            'instance_id': record['instance_id'],
            'model': record['model'],
            'explainer': record['explainer'],
            'quadrant': record['quadrant'],
            'llm_coherence': record['eval_scores']['coherence'],
            'llm_faithfulness': record['eval_scores']['faithfulness'],
            'llm_usefulness': record['eval_scores']['usefulness']
        }
        flat_llm_data.append(flat_record)
    
    df_llm = pd.DataFrame(flat_llm_data)
    print(f"Loaded {len(df_llm)} LLM records.")

    # 2. Load Classical Metrics
    print(f"Loading Classical metrics from: {results_dir}")
    metrics_files = glob.glob(os.path.join(results_dir, "*", "metrics.csv"))
    
    df_metrics_list = []
    for file_path in metrics_files:
        dir_name = os.path.basename(os.path.dirname(file_path))
        if '_' in dir_name and 'tuning' not in dir_name: # Avoid tuning directory
            parts = dir_name.split('_', 1)
            model_prefix = parts[0]
            explainer_suffix = parts[1]
            
            # Map shorthand to full names if necessary, matching LLM data
            # LLM data uses 'xgboost' and 'lime'/'shap'
            model = 'xgboost' if model_prefix == 'xgb' else model_prefix # rf stays rf? or random_forest?
            
            # Check LLM data model names
            # Expected: 'xgboost', 'rf' (based on previous head output)
            
            explainer = explainer_suffix
            
            df_temp = pd.read_csv(file_path)
            df_temp['model'] = model
            df_temp['explainer'] = explainer
            
            # Ensure instance_id is int
            if 'instance_id' in df_temp.columns:
                df_temp['instance_id'] = df_temp['instance_id'].astype(int)
                df_metrics_list.append(df_temp)
    
    if not df_metrics_list:
        print("ERROR: No suitable metrics.csv files found.")
        return

    df_classical = pd.concat(df_metrics_list, ignore_index=True)
    print(f"Loaded {len(df_classical)} classical metric records.")

    # 3. Merge
    # We need to ensure model names match.
    # LLM data has: 'xgboost', and likely 'rf' or 'random_forest'.
    # Classical loader produced: 'xgboost' (from xgb), 'rf' (from rf).
    # Let's verify unique values.
    print(f"LLM Data Models: {df_llm['model'].unique()}")
    print(f"Classical Data Models: {df_classical['model'].unique()}")
    
    df_merged = pd.merge(
        df_classical, 
        df_llm, 
        on=['instance_id', 'model', 'explainer', 'quadrant'], 
        how='inner'
    )
    print(f"Merged Record Count: {len(df_merged)}")
    
    if len(df_merged) == 0:
        print("ERROR: Merge resulted in 0 records. Check join keys.")
        return

    # 4. Correlation Analysis
    print("\n=== Correlation Analysis (Spearman) ===")
    classical_cols = [c for c in df_merged.columns if c.startswith('metric_') and c != 'metric_cost'] 
    # Exclude cost if constant or irrelevant, but keeping others.
    # previous head showed: metric_cost, metric_sparsity, metric_fidelity, metric_faithfulness_gap, metric_domain_precision, metric_domain_recall, metric_stability
    
    llm_cols = ['llm_coherence', 'llm_faithfulness', 'llm_usefulness']
    
    results = []
    
    for c_metric in classical_cols:
        for l_score in llm_cols:
            if df_merged[c_metric].nunique() <= 1:
                continue # Skip constant metrics
                
            r, p = stats.spearmanr(df_merged[c_metric], df_merged[l_score])
            is_sig = p < 0.05
            results.append({
                'Classical': c_metric,
                'LLM': l_score,
                'Spearman_R': r,
                'P_Value': p,
                'Significant': '*' if is_sig else ''
            })
            
    df_results = pd.DataFrame(results)
    
    # Sort by absolute correlation strength
    df_results['Abs_R'] = df_results['Spearman_R'].abs()
    df_results = df_results.sort_values('Abs_R', ascending=False).drop(columns=['Abs_R'])
    
    print(df_results.to_string(index=False))
    
    # 5. Key Highlights
    print("\n=== Key Findings ===")
    sig_results = df_results[df_results['P_Value'] < 0.05]
    if not sig_results.empty:
        print("Significant Correlations found:")
        for _, row in sig_results.iterrows():
            print(f"- {row['Classical']} vs {row['LLM']}: R={row['Spearman_R']:.3f} (p={row['P_Value']:.4f})")
    else:
        print("No statistically significant correlations found (p < 0.05).")

    # 6. Stratified Analysis Snapshot (Top Correlation only)
    if not df_results.empty:
        top_pair = df_results.iloc[0]
        c_top, l_top = top_pair['Classical'], top_pair['LLM']
        print(f"\nStratified Breakdown for Top Pair: {c_top} vs {l_top}")
        
        for explainer in df_merged['explainer'].unique():
            subset = df_merged[df_merged['explainer'] == explainer]
            if len(subset) > 1:
                r, p = stats.spearmanr(subset[c_top], subset[l_top])
                print(f"  [{explainer}] R={r:.3f} (p={p:.4f})")

if __name__ == "__main__":
    run_analysis()
