
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

def load_metrics(path):
    with open(path, 'r') as f:
        data = json.load(f)
    
    rows = []
    for item in data['instance_evaluations']:
        metrics = item.get('metrics', {})
        metrics['instance_id'] = item.get('instance_id')
        rows.append(metrics)
    return pd.DataFrame(rows)

def main():
    base_results = Path("experiments/exp1_adult/results")
    output_dir = base_results / "figures"
    output_dir.mkdir(exist_ok=True)

    # Load data
    try:
        df_rf = load_metrics(base_results / "rf_shap/results.json")
        df_rf['Method'] = 'RF + SHAP'
    except FileNotFoundError:
        print("Warning: RF+SHAP results not found")
        df_rf = pd.DataFrame()

    try:
        df_xgb = load_metrics(base_results / "xgb_lime/results.json")
        df_xgb['Method'] = 'XGB + LIME'
    except FileNotFoundError:
        print("Warning: XGB+LIME results not found")
        df_xgb = pd.DataFrame()

    if df_rf.empty and df_xgb.empty:
        print("No data found to plot.")
        return

    df_all = pd.concat([df_rf, df_xgb], ignore_index=True)

    # Metrics to plot
    metrics = ['stability', 'fidelity', 'sparsity', 'cost']
    friendly_names = {
        'stability': 'Stability (Cosine)',
        'fidelity': 'Fidelity (R2)',
        'sparsity': 'Sparsity (Zero-Ratio)',
        'cost': 'Cost (Seconds)'
    }

    # Plot
    plt.figure(figsize=(12, 10))
    for i, metric in enumerate(metrics):
        if metric not in df_all.columns:
            continue
            
        plt.subplot(2, 2, i+1)
        sns.barplot(x='Method', y=metric, data=df_all, capsize=.1, errorbar='sd')
        plt.title(friendly_names.get(metric, metric))
        plt.ylabel("Score")
        plt.xlabel("")
    
    plt.tight_layout()
    save_path = output_dir / "xai_metrics_comparison.png"
    plt.savefig(save_path)
    print(f"Saved comparison plot to {save_path}")

if __name__ == "__main__":
    main()
