#!/usr/bin/env python
# User Story: EXP1-08
"""
Visualize Random Forest training results for Experiment 1.
Generates plots and a markdown report.
"""

import sys
import os
import json
import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.models.tabular_models import load_trained_model
from src.data_loading.adult import load_adult

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def plot_confusion_matrix(metrics, save_dir):
    """Plot confusion matrix from metrics."""
    if "test_confusion_counts" not in metrics:
        return
        
    counts = metrics["test_confusion_counts"]
    cm = np.array([
        [counts["tn"], counts["fp"]],
        [counts["fn"], counts["tp"]]
    ])
    
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.title("Confusion Matrix")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    
    save_path = save_dir / "rf_confusion_matrix.png"
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved confusion matrix to {save_path}")

def plot_feature_importance(results_dir, save_dir):
    """Plot feature importance from CSV."""
    csv_path = results_dir / "rf_feature_importance.csv"
    if not csv_path.exists():
        logger.warning(f"Feature importance, CSV not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    top_20 = df.head(20)
    
    plt.figure(figsize=(10, 8))
    sns.barplot(x="importance", y="feature", data=top_20, palette="viridis")
    plt.title("Top 20 Feature Importance (Random Forest)")
    plt.xlabel("Gini Importance")
    plt.tight_layout()
    
    save_path = save_dir / "rf_feature_importance.png"
    plt.savefig(save_path)
    plt.close()
    logger.info(f"Saved feature importance plot to {save_path}")

def plot_roc_curve(model_path, save_dir):
    """Generate and plot ROC curve by reloading model/data."""
    model_path = Path(model_path)
    if not model_path.exists():
        logger.warning("Model file not found, skipping ROC curve.")
        return

    try:
        # Load model and data
        model = load_trained_model(str(model_path))
        data = load_adult()
        _, X_test, _, y_test = data[0], data[1], data[2], data[3]
        
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            roc_auc = auc(fpr, tpr)
            
            plt.figure(figsize=(7, 7))
            plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('Receiver Operating Characteristic')
            plt.legend(loc="lower right")
            
            save_path = save_dir / "rf_roc_curve.png"
            plt.savefig(save_path)
            plt.close()
            logger.info(f"Saved ROC curve to {save_path}")
            
    except Exception as e:
        logger.warning(f"Failed to plot ROC curve: {e}")

def create_report(metrics, save_dir):
    """Create markdown report."""
    md_path = save_dir.parent / "rf_training_report.md"
    
    metadata = metrics.get("training_metadata", {})
    acc = metrics.get("test_accuracy", "N/A")
    auc = metrics.get("test_roc_auc", "N/A")
    
    content = f"""# Random Forest Training Report (Experiment 1)

**Date**: {metadata.get("timestamp", "Unknown")}

## Performance Summary
- **Accuracy**: {acc}
- **ROC AUC**: {auc}
- **Execution Time**: {metadata.get("training_time_seconds", "?")}s

## Visualizations

### Confusion Matrix
![Confusion Matrix](figures/rf_confusion_matrix.png)

### Feature Importance
![Feature Importance](figures/rf_feature_importance.png)

### ROC Curve
![ROC Curve](figures/rf_roc_curve.png)

## Model Parameters
```json
{json.dumps(metadata.get("model_params", {}), indent=2)}
```
"""
    with open(md_path, 'w') as f:
        f.write(content)
    logger.info(f"Saved report to {md_path}")

def main():
    parser = argparse.ArgumentParser(description="Visualize RF Results")
    parser.add_argument("--results-dir", type=str, default="experiments/exp1_adult/results")
    parser.add_argument("--model-dir", type=str, default="experiments/exp1_adult/models")
    args = parser.parse_args()
    
    results_dir = Path(args.results_dir)
    model_dir = Path(args.model_dir)
    
    # Create figures dir
    figures_dir = results_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    # Load metrics
    metrics_path = results_dir / "rf_metrics.json"
    if not metrics_path.exists():
        logger.error(f"Metrics file not found: {metrics_path}")
        return
        
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
        
    # Generate plots
    plot_confusion_matrix(metrics, figures_dir)
    plot_feature_importance(results_dir, figures_dir)
    
    # Attempt ROC curve (needs model path)
    model_path = model_dir / "rf_model.pkl"
    plot_roc_curve(model_path, figures_dir)
    
    # Create report
    create_report(metrics, figures_dir)

if __name__ == "__main__":
    main()
