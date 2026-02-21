import sys
import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Add project root to sys.path
project_root = Path("/home/jonnabio/Documents/GitHub/xai-eval-framework")
sys.path.insert(0, str(project_root))

from src.data_loading.adult import load_adult, load_preprocessor
from src.xai.shap_tabular import SHAPTabularWrapper

def generate_visuals():
    print("Loading preprocessor and data...")
    preprocessor_path = project_root / "experiments/exp1_adult/models/preprocessor.joblib"
    preprocessor = load_preprocessor(str(preprocessor_path))
    
    # Load and preprocess using the existing preprocessor
    X_train, X_test, y_train, y_test, feature_names, _ = load_adult(
        preprocessor=preprocessor,
        verbose=False
    )
    
    print("Loading models...")
    svm_path = project_root / "experiments/exp1_adult/models/svm.joblib"
    mlp_path = project_root / "experiments/exp1_adult/models/mlp.joblib"
    
    svm = joblib.load(svm_path)
    mlp = joblib.load(mlp_path)
    
    # Select a sample
    sample_idx = 92 # We know this from earlier jq inspection
    sample = X_test[sample_idx:sample_idx+1]
    
    # Perturbation parameters
    # Use a moderate epsilon to demonstrate meaningful shifts
    eps = 0.08 
    n_perturbations = 3
    
    # Generate perturbations
    np.random.seed(42) # For consistent paper-ready visuals
    perturbations = [sample]
    for i in range(n_perturbations):
        # Only perturb numeric features to avoid invalid OHE states in this simple visual
        # Numeric are the first 6 features in our pipeline
        noise = np.zeros(sample.shape)
        noise[:, :6] = np.random.normal(0, eps, (1, 6))
        perturbations.append(sample + noise)
    
    X_viz = np.vstack(perturbations)
    
    # SVM SHAP (Stable)
    print("Generating SHAP for SVM (Status: Stable)...")
    svm_wrapper = SHAPTabularWrapper(
        model=svm, 
        training_data=X_train[:100], 
        feature_names=feature_names,
        model_type="kernel",
        n_background_samples=20,
        use_kmeans=True
    )
    svm_res = svm_wrapper.generate_explanations(svm, X_viz)
    
    # MLP SHAP (Unstable)
    print("Generating SHAP for MLP (Status: Unstable)...")
    mlp_wrapper = SHAPTabularWrapper(
        model=mlp,
        training_data=X_train[:100],
        feature_names=feature_names,
        model_type="kernel",
        n_background_samples=20,
        use_kmeans=True
    )
    mlp_res = mlp_wrapper.generate_explanations(mlp, X_viz)
    
    # Setup Plotting Style
    plt.rcParams['font.family'] = 'sans-serif'
    sns.set_theme(style="whitegrid", palette="tab10")
    fig, axes = plt.subplots(2, 1, figsize=(15, 12), sharex=True)
    
    # Features to show: Top 6 of the original SVM explanation
    top_k = 6
    top_features_idx = svm_res['top_features'][0][:top_k]
    
    def plot_stb(ax, res, title, is_svm=True):
        plot_data = []
        labels = ['Target Instance', 'Perturbation A', 'Perturbation B', 'Perturbation C']
        for i in range(len(X_viz)):
            for j, f_idx in enumerate(top_features_idx):
                plot_data.append({
                    'State': labels[i],
                    'Feature': feature_names[f_idx],
                    'Importance': res['feature_importance'][i, f_idx]
                })
        
        df = pd.DataFrame(plot_data)
        sns.barplot(data=df, x='Feature', y='Importance', hue='State', ax=ax, edgecolor='0.3', alpha=0.9)
        
        main_color = "#1B5E20" if is_svm else "#B71C1C"
        bg_color = "#E8F5E9" if is_svm else "#FFEBEE"
        
        ax.set_facecolor(bg_color)
        ax.set_title(title, fontsize=18, fontweight='bold', color=main_color, pad=25)
        ax.set_ylabel("SHAP Value (Attribution)", fontsize=13, fontweight='bold')
        ax.set_xlabel("")
        ax.legend(title="Local Neighborhood", loc='upper right', frameon=True, fontsize=11)
        ax.tick_params(axis='x', labelsize=12)
        
        # Add stability annotation
        stability_score = np.mean([np.corrcoef(res['feature_importance'][0], res['feature_importance'][i+1])[0,1] for i in range(n_perturbations)])
        ax.text(0.98, 0.02, f"Estimated Local Stability: {stability_score:.3f}", 
                transform=ax.transAxes, ha='right', va='bottom', 
                bbox=dict(boxstyle="round", facecolor='white', alpha=0.8),
                fontsize=12, fontweight='bold')

    plot_stb(axes[0], svm_res, "Fig 1a: SVM + SHAP (Robust Decision Surface)", is_svm=True)
    plot_stb(axes[1], mlp_res, "Fig 1b: MLP + SHAP (Sensitive/Noisy Decision Surface)", is_svm=False)
    
    plt.xticks(rotation=20, ha='right')
    plt.suptitle("Local Stability Analysis: Feature Attribution Variance across Neighboring Samples", 
                 fontsize=22, y=1.03, fontweight='bold')
    
    plt.tight_layout()
    
    out_dir = project_root / "outputs/paper_analysis"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "explanation_stability_comparison.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    
    print(f"\nSUCCESS: Visualization generated at {out_path}")
    print(f"Output Directory: {out_dir}")

if __name__ == "__main__":
    generate_visuals()
