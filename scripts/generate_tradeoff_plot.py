#!/usr/bin/env python3
"""
Generate Stability vs. Computation Time Trade-off Plot for Paper B.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def load_data(experiments_dir: Path):
    data = []
    json_files = list(experiments_dir.rglob("results.json"))
    
    for p in json_files:
        try:
            with open(p, 'r') as f:
                res = json.load(f)
            
            aggs = res.get("aggregated_metrics", {})
            meta = res.get("experiment_metadata", {})
            model_info = res.get("model_info", {})
            
            if not aggs:
                continue
                
            entry = {
                'Experiment': meta.get('name'),
                'Model': model_info.get('name', 'Unknown'),
                'Method': model_info.get('explainer_method', 'Unknown').upper(),
                'Stability': aggs.get('Stability', {}).get('mean') if isinstance(aggs.get('Stability'), dict) else aggs.get('Stability'),
                'Latency': aggs.get('EfficiencyMS', {}).get('mean') if isinstance(aggs.get('EfficiencyMS'), dict) else aggs.get('EfficiencyMS', aggs.get('cost'))
            }
            
            # Fallback for flat metrics
            if entry['Stability'] is None: entry['Stability'] = aggs.get('Stability')
            if entry['Latency'] is None: entry['Latency'] = aggs.get('EfficiencyMS', aggs.get('cost'))
            
            if entry['Stability'] is not None and entry['Latency'] is not None:
                data.append(entry)
        except:
            continue
            
    return pd.DataFrame(data)

def main():
    exp_dir = Path("experiments")
    df = load_data(exp_dir)
    
    if df.empty:
        print("No data found.")
        return

    plt.figure(figsize=(12, 8))
    sns.set_theme(style="whitegrid")
    
    # Filter out outliers if necessary (e.g. extreme latency from corrupt runs or svm_shap)
    # Latency > 2000ms might squish the plot. Let's cap for visibility or use log scale.
    
    g = sns.scatterplot(
        data=df,
        x='Latency',
        y='Stability',
        hue='Method',
        style='Model',
        s=100,
        alpha=0.7
    )
    
    plt.xscale('log') # Use log scale for latency as SHAP can be much slower
    plt.title("XAI Trade-off: Stability vs. Computation Time (Paper B)", fontsize=16, fontweight='bold')
    plt.xlabel("Average Latency per Instance (ms) - Log Scale", fontsize=12)
    plt.ylabel("Average Stability (AOC / Feature Agreement)", fontsize=12)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    output_path = Path("outputs/paper_analysis")
    output_path.mkdir(parents=True, exist_ok=True)
    
    plot_file = output_path / "stability_vs_latency_tradeoff.png"
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Trade-off plot saved to {plot_file}")
    
    # Print summary statistics
    summary = df.groupby('Method')[['Stability', 'Latency']].agg(['mean', 'std'])
    print("\nMethod comparison summary:")
    print(summary)

if __name__ == "__main__":
    main()
