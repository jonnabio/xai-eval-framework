#!/usr/bin/env python3
"""
Generate Metric Independence Heatmap (Pearson Correlation) for Paper A.
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def load_all_metrics(experiments_dir: Path):
    data = []
    json_files = list(experiments_dir.rglob("results.json"))
    print(f"Scanning {len(json_files)} files...")
    
    for p in json_files:
        try:
            with open(p, 'r') as f:
                res = json.load(f)
            
            aggs = res.get("aggregated_metrics", {})
            if not aggs:
                continue
                
            entry = {}
            # Flatten metrics
            for k, v in aggs.items():
                if isinstance(v, dict) and "mean" in v:
                    entry[k] = v["mean"]
                else:
                    entry[k] = v
            
            if entry:
                data.append(entry)
        except:
            continue
            
    return pd.DataFrame(data)

def main():
    exp_dir = Path("experiments")
    df = load_all_metrics(exp_dir)
    
    if df.empty:
        print("No metrics found.")
        return

    # Clean up column names for the paper
    column_mapping = {
        'Fidelity': 'Fidelity',
        'Stability': 'Stability',
        'Sparsity': 'Sparsity',
        'CausalAlignment': 'Causal Alignment',
        'CounterfactualSensitivity': 'CF Sensitivity',
        'EfficiencyMS': 'Latency (ms)',
        'cost': 'Latency (ms)' # Handle both naming conventions
    }
    
    # Merge Latency columns if both exist
    if 'cost' in df.columns and 'EfficiencyMS' in df.columns:
         df['Latency (ms)'] = df['EfficiencyMS'].fillna(df['cost'])
    elif 'EfficiencyMS' in df.columns:
         df['Latency (ms)'] = df['EfficiencyMS']
    elif 'cost' in df.columns:
         df['Latency (ms)'] = df['cost']

    cols_to_keep = ['Fidelity', 'Stability', 'Sparsity', 'CausalAlignment', 'CounterfactualSensitivity', 'Latency (ms)']
    existing_cols = [c for c in cols_to_keep if c in df.columns]
    
    analysis_df = df[existing_cols].rename(columns=column_mapping)
    
    # Compute Pearson Correlation
    corr = analysis_df.corr(method='pearson')
    
    # Plot
    plt.figure(figsize=(10, 8))
    sns.set_theme(style="white")
    
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    header_font = {'weight': 'bold', 'size': 14}
    
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1.0, vmin=-1.0, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, fmt=".2f")
    
    plt.title("Metric Independence Analysis (Pearson Correlation)", fontdict=header_font, pad=20)
    
    output_path = Path("outputs/paper_analysis")
    output_path.mkdir(parents=True, exist_ok=True)
    
    plot_file = output_path / "metric_correlation_heatmap.png"
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Heatmap saved to {plot_file}")
    print("\nPearson Correlation Matrix:")
    print(corr)

if __name__ == "__main__":
    main()
