import json
import os
import glob
import pandas as pd
import numpy as np
from pathlib import Path

def merge_data():
    base_dir = Path("experiments/exp2_comparative")
    results_dir = base_dir / "results"
    
    # Optional: Load LLM results if they exist (skipping for now as we haven't run LLM eval for Exp2 yet)
    # llm_results_path = base_dir / "llm_eval" / "results_full.json"
    
    print(f"Scanning results in: {results_dir}")
    
    # Iterate Experiment Configurations
    exp_folders = [f for f in results_dir.iterdir() if f.is_dir()]
    
    count = 0
    for exp_folder in exp_folders:
        metrics_csv = exp_folder / "metrics.csv"
        results_json_path = exp_folder / "results.json"
        
        if not metrics_csv.exists() or not results_json_path.exists():
            print(f"Skipping {exp_folder.name}: Missing metrics.csv or results.json")
            continue
            
        print(f"Processing {exp_folder.name}...")
        
        try:
            # Load Data
            df_metrics = pd.read_csv(metrics_csv)
            with open(results_json_path, 'r') as f:
                results_data = json.load(f)
                
            # Compute Aggregated Metrics
            # Mapping generic metric names from CSV to Dashboard Schema
            # CSV usually has keys like: metric_fidelity, metric_stability, etc.
            
            agg_metrics = {
                "Fidelity": df_metrics['metric_fidelity'].mean() if 'metric_fidelity' in df_metrics else 0.0,
                "Stability": df_metrics['metric_stability'].mean() if 'metric_stability' in df_metrics else 0.0,
                "Sparsity": df_metrics['metric_sparsity'].mean() if 'metric_sparsity' in df_metrics else 0.0,
                "CausalAlignment": df_metrics['metric_domain_precision'].mean() if 'metric_domain_precision' in df_metrics else 0.0,
                "CounterfactualSensitivity": 0.0, # Placeholder
                "EfficiencyMS": df_metrics['metric_cost'].mean() if 'metric_cost' in df_metrics else 0.0
            }
            
            # Rounding
            agg_metrics = {k: round(float(v), 4) for k, v in agg_metrics.items()}
            
            # Placeholder LLM Data (To avoid Dashboard errors until we do Phase J)
            llm_eval_obj = {
                "likert_scores": {
                    "clarity": 3.0,
                    "usefulness": 3.0,
                    "completeness": 3.0,
                    "trustworthiness": 3.0,
                    "overall": 3.0
                },
                "justification": "Pending LLM Evaluation (Phase J)"
            }
            
            # Update JSON
            results_data['aggregated_metrics'] = agg_metrics
            results_data['llm_evaluation'] = llm_eval_obj
            
            # Write back
            with open(results_json_path, 'w') as f:
                json.dump(results_data, f, indent=2)
                
            count += 1
            
        except Exception as e:
            print(f"Error processing {exp_folder.name}: {e}")
            
    print(f"\nSuccessfully merged {count} experiments for Dashboard.")

if __name__ == "__main__":
    merge_data()
