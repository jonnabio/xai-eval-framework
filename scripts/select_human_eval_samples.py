import json
import os
import glob
import pandas as pd
import numpy as np
import argparse
from pathlib import Path
from typing import List, Dict, Any

def load_experiment_data(exp_dir: Path) -> List[Dict[str, Any]]:
    """Load instance evaluations from an experiment directory."""
    results_path = exp_dir / "results.json"
    if not results_path.exists():
        print(f"Warning: {results_path} not found.")
        return []
    
    with open(results_path, 'r') as f:
        data = json.load(f)
        
    instances = data.get("instance_evaluations", [])
    model_name = data.get("model_info", {}).get("name")
    explainer = data.get("model_info", {}).get("explainer_method")
    
    # Enrich with experiment meta
    for inst in instances:
        inst["experiment_id"] = exp_dir.name
        inst["model"] = model_name
        inst["explainer"] = explainer
        
    return instances

def load_llm_scores(llm_path: Path) -> Dict[str, Dict[str, Any]]:
    """Load LLM scores indexed by unique key (instance_id + model + explainer)."""
    if not llm_path.exists():
        print(f"Warning: {llm_path} not found. LLM scores will be missing.")
        return {}
        
    with open(llm_path, 'r') as f:
        llm_data = json.load(f)
        
    lookup = {}
    for record in llm_data:
        # Key needs to match how we identify instances in experiments
        # Experiment data: model="rf", explainer="lime"
        # LLM data: model="rf" (or "random_forest"?), explainer="lime"
        # We need to normalize.
        
        # In previous steps we saw LLM data uses 'xgboost' and 'rf'
        # Experiment data might use 'xgb' or 'rf'.
        # Let's clean the key generation.
        
        model = record['model']
        if model == 'xgboost': model = 'xgb' # normalize to match exp dir prefix usually
        
        key = f"{record['instance_id']}_{model}_{record['explainer']}"
        lookup[key] = record['eval_scores']
        lookup[key]['reasoning'] = record.get('reasoning', '')
        
    return lookup

def select_samples(args):
    base_dir = Path("experiments/exp1_adult")
    results_dir = base_dir / "results"
    llm_path = base_dir / "llm_eval" / "results_full.json"
    output_path = Path(args.output)
    
    # 1. Load LLM Scores
    llm_lookup = load_llm_scores(llm_path)
    print(f"Loaded {len(llm_lookup)} LLM records.")

    # 2. Load All Experiments
    # We specifically want the 4 main ones
    target_experiments = ["rf_lime", "rf_shap", "xgb_lime", "xgb_shap"]
    
    all_selected_samples = []
    
    for exp_name in target_experiments:
        exp_dir = results_dir / exp_name
        if not exp_dir.exists():
            print(f"Skipping {exp_name} (not found)")
            continue
            
        print(f"\nProcessing {exp_name}...")
        instances = load_experiment_data(exp_dir)
        df = pd.DataFrame(instances)
        
        if df.empty:
            print("  No instances found.")
            continue
            
        # FILTER: Only keep instances that have LLM scores
        # We need to constructing the key column to match llm_lookup keys
        # Normalization logic
        def get_lookup_key(row):
            m = row['model']
            if m == 'random_forest': m = 'rf'
            if m == 'xgboost': m = 'xgb'
            e = row['explainer']
            return f"{row['instance_id']}_{m}_{e}"
            
        df['lookup_key'] = df.apply(get_lookup_key, axis=1)
        
        # Check intersection
        valid_keys = set(llm_lookup.keys())
        original_count = len(df)
        df = df[df['lookup_key'].isin(valid_keys)]
        print(f"  Filtered to {len(df)}/{original_count} instances with LLM scores.")
        
        if df.empty:
            print("  No instances with LLM scores found for this experiment.")
            continue

        # Extract Fidelity
        # Metric structure: metrics dict inside instance
        # We need to extract 'fidelity' from the metrics dict
        df['fidelity'] = df['metrics'].apply(lambda m: m.get('fidelity', 0.0))
        df['quadrant'] = df['quadrant']
        
        # Define Strata: Quadrant x Fidelity
        df['fidelity_level'] = df['fidelity'].apply(lambda x: 'High' if x >= args.fidelity_threshold else 'Low')
        df['stratum'] = df['quadrant'] + "_" + df['fidelity_level']
        
        # We want 5 samples from this experiment
        # Ideally covering different quadrants.
        # Unique quadrants: TP, TN, FP, FN. 
        # Strategy: Pick 1 from each Quadrant (prioritizing diverse Fidelity), then 1 random.
        
        selected_indices = []
        quadrants = ['TP', 'TN', 'FP', 'FN']
        
        temp_df = df.copy()
        
        # Pass 1: One from each quadrant
        for q in quadrants:
            q_subset = temp_df[temp_df['quadrant'] == q]
            if not q_subset.empty:
                # Try to alternate High/Low fidelity if possible, or just pick random/highest fidelity?
                # Let's pick the one with highest fidelity for 'High' and lowest for 'Low' to get range?
                # User asked for diverse.
                # Let's just sample random to avoid bias, or pick one High and one Low across the set.
                
                # Simple approach: Sample 1
                sample = q_subset.sample(n=1, random_state=42)
                selected_indices.extend(sample.index.tolist())
                # Remove from pool
                temp_df = temp_df.drop(sample.index)
        
        # Pass 2: Fill remaining slots (target 5)
        current_count = len(selected_indices)
        needed = 5 - current_count
        
        if needed > 0 and not temp_df.empty:
            if len(temp_df) >= needed:
                extra_samples = temp_df.sample(n=needed, random_state=42)
                selected_indices.extend(extra_samples.index.tolist())
            else:
                selected_indices.extend(temp_df.index.tolist())
                
        # Retrieve Data
        selected_df = df.loc[selected_indices]
        print(f"  Selected {len(selected_df)} samples. Breakdown:")
        print(selected_df['stratum'].value_counts())
        
        for _, row in selected_df.iterrows():
            # Construct Final Record
            # Key for LLM lookup
            # model in row is 'rf' or 'xgb' (from JSON model_info)
            # llm_lookup keys use that too (normalized above)
            
            # Note: JSON model_info might be 'random_forest' or 'rf'.
            # let's check what load_experiment_data put in 'model'
            # it's from model_info.name.
            
            # Normalization for lookup
            model_key = row['model']
            if model_key == 'random_forest': model_key = 'rf'
            if model_key == 'xgboost': model_key = 'xgb'
            
            # Also explainer
            explainer_key = row['explainer']    
            
            lookup_key = f"{row['instance_id']}_{model_key}_{explainer_key}"
            llm_score = llm_lookup.get(lookup_key, {})
            
            if not llm_score:
                print(f"    Warning: No LLM score for {lookup_key}")
            
            sample_record = {
                "sample_id": f"{exp_name}_{row['instance_id']}",
                "experiment": exp_name,
                "instance_id": row['instance_id'],
                "quadrant": row['quadrant'],
                "true_label": row['true_label'],
                "prediction": row['prediction'],
                "prediction_correct": row['prediction_correct'],
                "explanation": row['explanation'],
                "classical_metrics": row['metrics'],
                "llm_scores": llm_score, # Can be empty if missing
                "stratification": {
                    "quadrant": row['quadrant'],
                    "fidelity_level": row['fidelity_level']
                }
            }
            all_selected_samples.append(sample_record)

    # 3. Save Output
    print(f"\nTotal samples selected: {len(all_selected_samples)}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(all_selected_samples, f, indent=2)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Select human evaluation samples")
    parser.add_argument("--num-samples", type=int, default=20, help="Total samples target")
    parser.add_argument("--fidelity-threshold", type=float, default=0.7, help="Threshold for High/Low fidelity")
    parser.add_argument("--output", type=str, default="experiments/exp1_adult/human_eval/samples.json")
    
    args = parser.parse_args()
    select_samples(args)
