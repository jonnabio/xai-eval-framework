import json
import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from collections import defaultdict

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def extract_quantitative_results(results_dir):
    """
    Aggregates metrics from individual experiment result files.
    Returns a dictionary keyed by 'model_explainer'.
    """
    aggregated_data = {}
    
    results_path = Path(results_dir)
    # Recursively find all results.json files
    for result_file in results_path.glob("**/results.json"):
        try:
            data = load_json(result_file)
            
            # Identify experiment key
            model = data.get('model_info', {}).get('name', 'unknown')
            explainer = data.get('model_info', {}).get('explainer_method', 'unknown')
            key = f"{model}_{explainer}"
            
            # Aggregate instance metrics
            instances = data.get('instance_evaluations', [])
            metrics_list = defaultdict(list)
            
            for inst in instances:
                metrics = inst.get('metrics', {})
                for m_name, m_val in metrics.items():
                    if isinstance(m_val, (int, float)):
                        metrics_list[m_name].append(m_val)
            
            # Compute means and stds
            summary_metrics = {}
            for m_name, values in metrics_list.items():
                summary_metrics[m_name] = {
                    'mean': float(np.mean(values)),
                    'std': float(np.std(values)),
                    'count': len(values)
                }
                
            # Extract Global Performance
            # Look for training_metrics_*.csv in the root results dir
            performance = {}
            # Assume results_dir is passed to function
            root_results_path = Path(results_dir)
            csv_files = list(root_results_path.glob("training_metrics_*.csv"))
            
            if csv_files:
                # Take the most recent one
                csv_files.sort()
                try:
                    df = pd.read_csv(csv_files[-1])
                    # Filter by model name if possible, or assume file structure
                    # The CSV likely has columns: model_name, accuracy, roc_auc
                    
                    # Normalize model name from JSON to match CSV (e.g. 'rf' vs 'random_forest')
                    # We check if our current 'model' is in any of the rows
                    row = None
                    if 'model' in df.columns: # CSV header says 'model', not 'model_name'
                         # Fuzzy match: is 'rf' in 'exp1_adult_mvp_rf'?
                         matches = df[df['model'].str.contains(model, case=False, na=False)]
                         if not matches.empty:
                             row = matches.iloc[0]
                         else:
                             # Try known aliases
                             aliases = {'xgboost': 'xgb', 'rf': 'random_forest'}
                             if model in aliases:
                                 matches = df[df['model'].str.contains(aliases[model], case=False, na=False)]
                                 if not matches.empty:
                                     row = matches.iloc[0]
                    elif len(df) > 0:
                        # Fallback: if there's no model_name column, maybe it's just a single row or we can't map
                        # But wait, we have multiple models (rf, xgb). The CSV must distinguish.
                        # Let's check CSV content later. For now, try simple matching
                        pass
                    
                    if row is not None:
                        if 'accuracy' in row: performance['accuracy'] = float(row['accuracy'])
                        if 'roc_auc' in row: performance['roc_auc'] = float(row['roc_auc'])
                        
                except Exception as e:
                    print(f"Warning: Could not read training metrics: {e}")

            aggregated_data[key] = {
                'model': model,
                'explainer': explainer,
                'xai_metrics': summary_metrics,
                'performance': performance
            }
            
        except Exception as e:
            print(f"Error processing {result_file}: {e}")
            
    return aggregated_data

def extract_qualitative_results(llm_results_path):
    """
    Aggregates LLM evaluation scores from the full results JSON.
    """
    aggregated_llm = {}
    
    try:
        data = load_json(llm_results_path)
        
        # Group by model + explainer
        grouped = defaultdict(lambda: defaultdict(list))
        
        for item in data:
            model = item.get('model', 'unknown')
            explainer = item.get('explainer', 'unknown')
            key = f"{model}_{explainer}"
            
            scores = item.get('eval_scores', {})
            for criteria, score in scores.items():
                # Handle cases where score might be a string or contain reasoning
                if isinstance(score, (int, float)):
                    grouped[key][criteria].append(score)
        
        # Compute stats
        for key, criteria_dict in grouped.items():
            model, explainer = key.split('_')
            aggregated_llm[key] = {
                'model': model,
                'explainer': explainer,
                'llm_metrics': {}
            }
            
            for criteria, values in criteria_dict.items():
                if values:
                    aggregated_llm[key]['llm_metrics'][criteria] = {
                        'mean': float(np.mean(values)),
                        'std': float(np.std(values)),
                        'count': len(values)
                    }
                    
    except Exception as e:
        print(f"Error processing LLM results {llm_results_path}: {e}")
        
    return aggregated_llm

def merge_results(quant, qual):
    """Merges quantitative and qualitative data."""
    merged = {}
    all_keys = set(quant.keys()) | set(qual.keys())
    
    for key in all_keys:
        merged[key] = {
            **quant.get(key, {'model': key.split('_')[0], 'explainer': key.split('_')[1]}),
            **qual.get(key, {})
        }
    return merged

def main():
    parser = argparse.ArgumentParser(description="Extract results metadata for LaTeX generation.")
    parser.add_argument("--results-dir", default="experiments/exp1_adult/results", help="Directory containing XAI results")
    parser.add_argument("--llm-file", default="experiments/exp1_adult/llm_eval/results_full.json", help="Path to LLM results JSON")
    parser.add_argument("--output", default="docs/thesis/results_metadata.json", help="Output JSON path")
    args = parser.parse_args()
    
    print("Extracting quantitative results...")
    quant_data = extract_quantitative_results(args.results_dir)
    
    print("Extracting qualitative LLM results...")
    qual_data = extract_qualitative_results(args.llm_file)
    
    print("Merging data...")
    final_metadata = merge_results(quant_data, qual_data)
    
    # Save
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_path, 'w') as f:
        json.dump(final_metadata, f, indent=4)
        
    print(f"Results metadata saved to {out_path}")

if __name__ == "__main__":
    main()
