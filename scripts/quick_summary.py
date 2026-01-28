
import json
import os
from collections import defaultdict
import glob
import numpy as np

RESULTS_DIR = "experiments/exp2_scaled/results"

def load_metrics():
    # Structure: method -> model -> set_size -> list of metrics
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    
    # We want to aggregate by: Method, Model, N (sample size)
    # The path structure is: .../results/{model}_{method}/seed_{seed}/n_{n}/results.json
    
    files = glob.glob(f"{RESULTS_DIR}/*/*/n_*/results.json")
    print(f"Found {len(files)} result files")
    
    for f in files:
        try:
            with open(f) as res_file:
                res = json.load(res_file)
                
            # Parse path to get meta
            parts = f.split('/')
            # parts[-4] is '{model}_{method}' e.g., 'rf_shap'
            # parts[-3] is 'seed_{seed}'
            # parts[-2] is 'n_{n}'
            
            model_method = parts[-4]
            model_name = model_method.split('_')[0]
            method_name = '_'.join(model_method.split('_')[1:]) # handle 'integrated_gradients'
            
            n_val = int(parts[-2].split('_')[1])
            
            # Extract metrics
            # We need average fidelity, stability per file
            # If 'aggregated_metrics' exists (it should, but we can compute from instances)
            
            instances = res.get('instance_evaluations', [])
            if not instances:
                continue
                
            fidelities = [i['metrics'].get('fidelity', 0) for i in instances]
            stabilities = [i['metrics'].get('stability', 0) for i in instances]
            sparsities = [i['metrics'].get('sparsity', 0) for i in instances]
            times = [res.get('experiment_metadata', {}).get('duration_seconds', 0) * 1000 / len(instances)] # ms per instance roughly
            
            # Store averages
            data[method_name][model_name][n_val]['fidelity'].append(np.mean(fidelities))
            data[method_name][model_name][n_val]['stability'].append(np.mean(stabilities))
            data[method_name][model_name][n_val]['sparsity'].append(np.mean(sparsities))
            data[method_name][model_name][n_val]['time_ms'].append(np.mean(times))
            
        except Exception as e:
            print(f"Error reading {f}: {e}")
            
    return data

def print_summary(data):
    print("\nXXX EXPERIMENT SUMMARY TABLE XXX\n")
    print(f"{'Method':<15} | {'Model':<10} | {'N':<5} | {'Fidelity':<10} | {'Stability':<10} | {'Sparsity':<10} | {'Time(ms)':<10}")
    print("-" * 90)
    
    for method in sorted(data.keys()):
        for model in sorted(data[method].keys()):
            for n in sorted(data[method][model].keys()):
                metrics = data[method][model][n]
                
                fid = np.mean(metrics['fidelity'])
                stab = np.mean(metrics['stability'])
                spar = np.mean(metrics['sparsity'])
                time = np.mean(metrics['time_ms'])
                
                print(f"{method:<15} | {model:<10} | {n:<5} | {fid:.4f}     | {stab:.4f}     | {spar:.4f}     | {time:.2f}")

if __name__ == "__main__":
    d = load_metrics()
    print_summary(d)
