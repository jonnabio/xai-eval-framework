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
        # Exclude tuning directory
        if "tuning" in str(result_file):
            continue
            
        try:
            data = load_json(result_file)
            
            # Identify experiment key
            model = data.get('model_info', {}).get('name', 'unknown')
            explainer = data.get('model_info', {}).get('explainer_method', 'unknown')
            key = f"{model}_{explainer}"
            
            # Aggregate instance metrics
            instances = data.get('instance_evaluations', [])
            metrics_list = defaultdict(list)
            
            # Compute Accuracy from instances if available
            correct_count = 0
            total_count = 0
            
            for inst in instances:
                # Performance tracking
                if 'prediction_correct' in inst:
                    total_count += 1
                    if inst['prediction_correct']:
                        correct_count += 1
                
                # Metric tracking
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
            # Priority 1: From global CSV (training_metrics_*.csv)
            # Priority 2: Compute from instance evaluations
            performance = {}
            row = None
            
            # Try CSV first
            root_results_path = Path(results_dir)
            csv_files = list(root_results_path.glob("training_metrics_*.csv"))
            if csv_files:
                csv_files.sort()
                try:
                    df = pd.read_csv(csv_files[-1])
                    if 'model' in df.columns:
                         matches = df[df['model'].str.contains(model, case=False, na=False)]
                         if not matches.empty:
                             row = matches.iloc[0]
                         else:
                             aliases = {'xgboost': 'xgb', 'rf': 'random_forest'}
                             if model in aliases:
                                 matches = df[df['model'].str.contains(aliases[model], case=False, na=False)]
                                 if not matches.empty:
                                     row = matches.iloc[0]
                    
                    if row is not None:
                        if 'accuracy' in row: performance['accuracy'] = float(row['accuracy'])
                        if 'roc_auc' in row: performance['roc_auc'] = float(row['roc_auc'])
                        
                except Exception as e:
                    print(f"Warning: Could not read training metrics from CSV: {e}")

            # Fallback to instance computation if CSV failed or missing
            if 'accuracy' not in performance and total_count > 0:
                performance['accuracy'] = correct_count / total_count
                performance['source'] = 'computed_from_instances'

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

def extract_cv_results(cv_dir):
    """
    Extracts cross-validation summary statistics.
    Returns a dictionary keyed by experiment name (e.g. 'exp1_cv_rf_lime').
    """
    cv_data = {}
    cv_path = Path(cv_dir)
    
    if not cv_path.exists():
        print(f"Warning: CV directory {cv_dir} does not exist.")
        return {}

    for exp_dir in cv_path.iterdir():
        if not exp_dir.is_dir():
            continue

        summary_file = exp_dir / "cv_summary.json"
        if summary_file.exists():
            try:
                cv_summary = load_json(summary_file)
                exp_name = exp_dir.name
                
                # Simplified structure for metadata
                cv_data[exp_name] = {
                    'n_folds': len(cv_summary.get('fold_results', [])), # Fallback if n_folds not top-level
                    'aggregated_metrics': cv_summary.get('aggregated_metrics', {}),
                    # We might want validation scores too if available
                }
            except Exception as e:
                print(f"Error reading CV summary {summary_file}: {e}")

    return cv_data

def load_significance_results(stats_file):
    """Loads statistical significance test results."""
    if not Path(stats_file).exists():
        print(f"Warning: Significance results file {stats_file} not found.")
        return {}
    
    try:
        return load_json(stats_file)
    except Exception as e:
        print(f"Error reading significance results: {e}")
        return {}

def main():
    parser = argparse.ArgumentParser(description="Extract results metadata for LaTeX generation.")
    parser.add_argument("--results-dir", default="experiments/exp1_adult/results", help="Directory containing XAI results")
    parser.add_argument("--llm-file", default="experiments/exp1_adult/llm_eval/results_full.json", help="Path to LLM results JSON")
    parser.add_argument("--cv-dir", default="outputs/cv", help="Directory containing CV results")
    parser.add_argument("--stats-file", default="outputs/analysis/significance_results.json", help="Path to significance results JSON")
    parser.add_argument("--output", default="docs/thesis/results_metadata.json", help="Output JSON path")
    args = parser.parse_args()
    
    print("Extracting quantitative results...")
    quant_data = extract_quantitative_results(args.results_dir)
    
    print("Extracting qualitative LLM results...")
    qual_data = extract_qualitative_results(args.llm_file)
    
    print("Extracting cross-validation results...")
    cv_data = extract_cv_results(args.cv_dir)
    
    print("Loading statistical significance results...")
    stats_data = load_significance_results(args.stats_file)
    
    print("Merging data...")
    final_metadata = merge_results(quant_data, qual_data)
    
    # Add new sections to metadata
    final_metadata['cross_validation'] = cv_data
    final_metadata['statistical_tests'] = stats_data
    
    # Save
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_path, 'w') as f:
        json.dump(final_metadata, f, indent=4)
        
    print(f"Results metadata saved to {out_path}")

if __name__ == "__main__":
    main()
