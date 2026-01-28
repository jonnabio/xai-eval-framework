
import json
import os
from collections import defaultdict
import glob
import numpy as np

def load_all_metrics():
    # Structure: experiment_group -> method -> model -> list of metrics
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    
    # Scan all experiment directories
    files = glob.glob("experiments/*/results/**/results.json", recursive=True)
    print(f"Found {len(files)} result files")
    
    for f in files:
        try:
            with open(f) as res_file:
                res = json.load(res_file)
            
            # Identify group (exp1 or exp2)
            path_parts = f.split('/')
            exp_group = path_parts[1] # experiments/exp1_adult/...
            
            # Identify model and method
            # Usually in model_info, or infer from directory names
            # directory structure varies: 
            # exp1: results/rf/rf_lime/results.json OR results/rf/lime/results.json
            # exp2: results/rf_shap/seed_X/n_Y/results.json
            
            model_name = res.get('model_info', {}).get('name', 'unknown')
            method_name = res.get('model_info', {}).get('explainer_method', res.get('xai_method', 'unknown'))
            
            # Fallback if metadata missing (common in old runs)
            if method_name == 'unknown':
                if 'lime' in f: method_name = 'lime'
                elif 'shap' in f: method_name = 'shap'
            
            instances = res.get('instance_evaluations', [])
            if not instances:
                continue
                
            fidelities = [i.get('metrics', {}).get('fidelity', i.get('metrics', {}).get('faithfulness', 0)) for i in instances]
            stabilities = [i.get('metrics', {}).get('stability', 0) for i in instances]
            sparsities = [i.get('metrics', {}).get('sparsity', 0) for i in instances]
            
            # Duration
            duration = res.get('experiment_metadata', {}).get('duration_seconds', 0)
            avg_time = (duration * 1000) / len(instances) if len(instances) > 0 else 0
            
            data[exp_group][method_name][model_name]['fidelity'].extend(fidelities)
            data[exp_group][method_name][model_name]['stability'].extend(stabilities)
            data[exp_group][method_name][model_name]['sparsity'].extend(sparsities)
            data[exp_group][method_name][model_name]['time_ms'].append(avg_time)
            # count is derived from length of lists
            
        except Exception as e:
            # print(f"Skipping {f}: {e}")
            pass
            
    return data

def print_summary(data):
    print("\nXXX FULL EXPERIMENT SUMMARY XXX\n")
    print(f"{'Exp':<15} | {'Method':<10} | {'Model':<12} | {'Count':<6} | {'Fidelity':<8} | {'Stability':<8} | {'Sparsity':<8} | {'Time(ms)':<8}")
    print("-" * 105)
    
    for exp in sorted(data.keys()):
        for method in sorted(data[exp].keys()):
            for model in sorted(data[exp][method].keys()):
                m = data[exp][method][model]
                if not m['fidelity']: continue
                
                fid = np.mean(m['fidelity'])
                stab = np.mean(m['stability'])
                spar = np.mean(m['sparsity'])
                time = np.mean(m['time_ms']) # Average of experiment averages
                count = len(m['fidelity'])
                
                print(f"{exp:<15} | {method:<10} | {model:<12} | {count:<6} | {fid:.4f}   | {stab:.4f}   | {spar:.4f}   | {time:.1f}")

if __name__ == "__main__":
    d = load_all_metrics()
    print_summary(d)
