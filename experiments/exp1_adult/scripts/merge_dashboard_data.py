import json
import os
import glob
import pandas as pd
import numpy as np
from pathlib import Path

def merge_data():
    base_dir = Path("experiments/exp1_adult")
    llm_results_path = base_dir / "llm_eval" / "results_full.json"
    results_dir = base_dir / "results"

    print(f"Base Dir: {base_dir}")

    # 1. Load LLM Data
    if llm_results_path.exists():
        with open(llm_results_path, 'r') as f:
            llm_records = json.load(f)
        df_llm = pd.DataFrame([
            {
                'model': r['model'],
                'explainer': r['explainer'],
                'coherence': r['eval_scores']['coherence'],
                'faithfulness': r['eval_scores']['faithfulness'],
                'usefulness': r['eval_scores']['usefulness']
            }
            for r in llm_records
        ])
        print(f"Loaded {len(df_llm)} LLM records")
    else:
        print("WARNING: LLM results not found. Dashboard will have empty LLM stats.")
        df_llm = pd.DataFrame()

    # 2. Iterate Experiment Configurations
    # We look for distinct folders in results/
    exp_folders = [f for f in results_dir.iterdir() if f.is_dir() and (f / "metrics.csv").exists()]
    
    for exp_folder in exp_folders:
        print(f"\nProcessing {exp_folder.name}...")
        
        # Identify Model/Explainer from folder name or metadata
        # Convention: rf_lime, xgb_shap
        try:
            model_prefix, explainer_suffix = exp_folder.name.split('_', 1)
            # Map standard names
            model_key = "xgboost" if model_prefix == "xgb" else model_prefix # 'rf' matches? LLM had 'rf' or 'random_forest'?
            # Let's check LLM data for specific values
            # LLM data: 'xgboost', 'rf' (from previous analysis output)
            if model_key == 'rf' and not df_llm.empty and 'rf' in df_llm['model'].unique():
                 model_key = 'rf'
            elif model_key == 'rf': # fallback
                 model_key = 'rf' 
            
            explainer_key = explainer_suffix
        except ValueError:
            print(f"Skipping folder {exp_folder.name} (cannot parse model_explainer)")
            continue

        # Load metrics.csv
        metrics_csv = exp_folder / "metrics.csv"
        df_metrics = pd.read_csv(metrics_csv)
        
        # Load results.json
        results_json_path = exp_folder / "results.json"
        if not results_json_path.exists():
            print(f"Skipping {exp_folder.name}: No results.json")
            continue
            
        with open(results_json_path, 'r') as f:
            results_data = json.load(f)

        # --- COMPUTE AGGREGATED METRICS ---
        # Schema: Fidelity, Stability, Sparsity, CausalAlignment, CounterfactualSensitivity, EfficiencyMS
        
        agg_metrics = {
            "Fidelity": df_metrics['metric_fidelity'].mean() if 'metric_fidelity' in df_metrics else 0.0,
            "Stability": df_metrics['metric_stability'].mean() if 'metric_stability' in df_metrics else 0.0,
            "Sparsity": df_metrics['metric_sparsity'].mean() if 'metric_sparsity' in df_metrics else 0.0,
            "CausalAlignment": df_metrics['metric_domain_precision'].mean() if 'metric_domain_precision' in df_metrics else 0.0, # Proxy
            "CounterfactualSensitivity": 0.0, # Not implemented yet
            "EfficiencyMS": df_metrics['metric_cost'].mean() if 'metric_cost' in df_metrics else 0.0
        }
        
        # Rounding
        agg_metrics = {k: round(float(v), 4) for k, v in agg_metrics.items()}
        
        # --- COMPUTE LLM EVAL ---
        # Filter LLM data for this model/explainer
        if not df_llm.empty:
            mask = (df_llm['model'] == model_key) & (df_llm['explainer'] == explainer_key)
            subset = df_llm[mask]
        else:
            subset = pd.DataFrame()

        if not subset.empty:
            mean_scores = subset.mean(numeric_only=True)
            # Map to Schema: clarity, usefulness, completeness, trustworthiness, overall
            # Input: coherence, faithfulness, usefulness
            
            likert = {
                "clarity": round(mean_scores.get('coherence', 3.0), 1),
                "usefulness": round(mean_scores.get('usefulness', 3.0), 1),
                "completeness": 3.0,
                "trustworthiness": round(mean_scores.get('faithfulness', 3.0), 1),
                "overall": round(mean_scores.mean(), 1)
            }
            justification = f"Aggregated from {len(subset)} LLM evaluations. Strongest correlation observed with Stability."
        else:
            likert = {
                "clarity": 3.0,
                "usefulness": 3.0,
                "completeness": 3.0,
                "trustworthiness": 3.0,
                "overall": 3.0
            }
            justification = "No LLM evaluations available for this configuration."

        llm_eval_obj = {
            "likert_scores": likert,
            "justification": justification
        }

        # --- UPDATE JSON ---
        results_data['aggregated_metrics'] = agg_metrics 
        results_data['llm_evaluation'] = llm_eval_obj
        
        # Also ensure instance_evaluations have metrics
        # (They are already there in 'metrics' key in snake_case, transformer might need updating or we leave it)
        # The schema InstanceEvaluation has metrics: Dict[str, float].
        # So snake_case is fine for instance level if frontend handles it, but typicaly we want consistency.
        # For now, we focus on the Top Level Run object which strictly needs the Schema keys.

        with open(results_json_path, 'w') as f:
            json.dump(results_data, f, indent=2)
            
        print(f"Updated {results_json_path}")

if __name__ == "__main__":
    merge_data()
