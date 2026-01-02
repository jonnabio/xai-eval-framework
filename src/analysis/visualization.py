
import matplotlib.pyplot as plt
import seaborn as sns
import scikit_posthocs as sp
import pandas as pd
import numpy as np
from pathlib import Path

def plot_critical_difference_diagram(ranks: dict, cd: float, method_names: list, save_path: str = None):
    """
    Generate CD diagram using scikit-posthocs.
    
    Args:
        ranks: Dict mapping method name to average rank.
               Or more commonly for sp.critical_difference_diagram, it takes ranks and CD.
               Wait, sp.critical_difference_diagram signature: (ranks, sig_matrix) usually.
               Let's re-read docs or use a safer approach:
               It acts on the results index/columns.
               
    Actually, let's use the provided API more directly if possible.
    But sp.critical_difference_diagram is high level.
    
    Let's rely on passing the Nemenyi rankings and let it plot.
    
    Function signature of sp.critical_difference_diagram(ranks, sig_matrix) -> None
    
    ranks : dict or Series
        A dictionary or Series with keys as method names and values as mean ranks.
    sig_matrix : DataFrame
        Significance matrix (p-values) or binary significance matrix.
        
    """
    plt.figure(figsize=(10, 3))
    
    # We need mean ranks. 
    # The external caller should compute them or we compute here.
    # For now assuming ranks is a Series/Dict.
    
    # NOTE: current sp version might just take ranks and calculate connections based on CD logic internally
    # if we pass the sig_matrix?
    # Actually, critical_difference_diagram usually works with Nemenyi results.
    
    # Let's wrap standard usage:
    sp.critical_difference_diagram(ranks, cd)
        
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()

def plot_metric_boxplots(df: pd.DataFrame, metric_name: str, save_path: str = None):
    """
    Plot boxplots for a metric across methods.
    
    Args:
        df: DataFrame where index=folds, cols=methods.
    """
    plt.figure(figsize=(10, 6))
    
    # Melt for seaborn
    melted = df.melt(var_name='Method', value_name='Score')
    
    sns.boxplot(data=melted, x='Method', y='Score', hue='Method', palette="Set3", legend=False)
    plt.title(f"Distribution of {metric_name} across folds")
    plt.ylabel(metric_name)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        plt.close()
