

import matplotlib.pyplot as plt
import seaborn as sns
import scikit_posthocs as sp
import pandas as pd
import numpy as np
from pathlib import Path
from math import pi

# --- PUBLICATION STYLE CONSTANTS ---
PUBLICATION_STYLE = {
    'single_column_width': 3.5,
    'double_column_width': 7.16,
    'max_height': 9.0,
    'font_family': 'serif',
    'font_size': 9,
    'dpi': 300,
}

# Okabe-Ito Colorblind-Safe Palette
OKABE_ITO_PALETTE = {
    'orange': '#E69F00',
    'sky_blue': '#56B4E9',
    'bluish_green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'vermillion': '#D55E00',
    'reddish_purple': '#CC79A7',
    'black': '#000000'
}

METHOD_COLORS = {
    'RF+LIME': OKABE_ITO_PALETTE['blue'],
    'RF+SHAP': OKABE_ITO_PALETTE['orange'],
    'XGB+LIME': OKABE_ITO_PALETTE['bluish_green'],
    'XGB+SHAP': OKABE_ITO_PALETTE['vermillion'],
    # Fallbacks or generic
    'RF': OKABE_ITO_PALETTE['blue'],
    'XGB': OKABE_ITO_PALETTE['bluish_green'],
    'LIME': OKABE_ITO_PALETTE['sky_blue'],
    'SHAP': OKABE_ITO_PALETTE['vermillion']
}

def setup_publication_style():
    """Apply publication-quality matplotlib settings."""
    plt.rcParams.update({
        'font.size': PUBLICATION_STYLE['font_size'],
        'axes.labelsize': PUBLICATION_STYLE['font_size'],
        'axes.titlesize': PUBLICATION_STYLE['font_size'] + 1,
        'xtick.labelsize': PUBLICATION_STYLE['font_size'] - 1,
        'ytick.labelsize': PUBLICATION_STYLE['font_size'] - 1,
        'legend.fontsize': PUBLICATION_STYLE['font_size'] - 1,
        'font.family': PUBLICATION_STYLE['font_family'],
        'lines.linewidth': 1.5,
        'figure.dpi': PUBLICATION_STYLE['dpi'],
        'savefig.dpi': PUBLICATION_STYLE['dpi'],
        'savefig.bbox': 'tight',
        'pdf.fonttype': 42 # TrueType
    })


def plot_critical_difference_diagram(ranks: dict, cd: float, method_names: list, save_path: str = None):
    """
    Generate CD diagram using scikit-posthocs.
    """
    # Create figure with simplified size
    plt.figure(figsize=(6, 3))
    
    # sp.critical_difference_diagram expects a Series of ranks and the CD value
    # Ensure ranks are properly formatted
    if isinstance(ranks, dict):
        ranks_series = pd.Series(ranks)
    else:
        ranks_series = ranks
        
    # Plot
    sp.critical_difference_diagram(ranks_series, cd)
        
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()

def plot_radar_chart(data: dict, metric_names: list, methods: list, save_path: str = None, ax=None):
    """
    Plot Radar Chart comparing methods across metrics.
    Normalization logic: 
    - Fidelity, Stability: [0, 1] Higher is better (Metric)
    - Sparsity: [0, 1] Lower is better (Metric). Inverted -> 1 - val
    - Cost: Lower is better. Normalized [0,1] then inverted.
    """
    setup_publication_style()
    
    # 1. Prepare Data & Normalize
    # We need a dataframe of absolute values first to normalize Cost
    raw_df = pd.DataFrame(index=methods, columns=metric_names)
    for m in methods:
        for met in metric_names:
            # Assuming data structure: data[method][metric] = value
            # Handle potential missing keys gracefully
            val = data.get(m, {}).get(met, 0)
            raw_df.loc[m, met] = val
            
    norm_df = raw_df.copy()
    
    # Cost Normalization (Min-Max then Invert)
    if 'cost' in metric_names:
        costs = raw_df['cost'].astype(float)
        c_min, c_max = costs.min(), costs.max()
        if c_max > c_min:
            norm_df['cost'] = 1 - ((costs - c_min) / (c_max - c_min))
        else:
            norm_df['cost'] = 1.0 # If all same, perfect score? Or relative?
            
    # Sparsity (Invert: 1 - sparsity)
    if 'sparsity' in metric_names:
        norm_df['sparsity'] = 1 - raw_df['sparsity'].astype(float)
        
    # Fidelity & Stability (Keep as is, assume 0-1)
    # Ensure float
    norm_df = norm_df.astype(float)
    
    # 2. Plot Setup
    N = len(metric_names)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1] # Close the loop
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    
    # 3. Plot Each Method
    for method in methods:
        values = norm_df.loc[method].tolist()
        values += values[:1] # Close loop
        
        color = METHOD_COLORS.get(method, 'gray')
        ax.plot(angles, values, linewidth=1.5, linestyle='solid', label=method, color=color)
        ax.fill(angles, values, color=color, alpha=0.1)
        
    # Labels
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    plt.xticks(angles[:-1], [m.capitalize() for m in metric_names])
    
    # Y-labels
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=7)
    plt.ylim(0, 1)
    
    if save_path:
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        plt.close()

def plot_metric_heatmap(df: pd.DataFrame, save_path: str = None, ax=None):
    """
    Plot heatmap of Method vs Metric.
    """
    setup_publication_style()
    if ax is None:
        plt.figure(figsize=(6, 4))
        ax = plt.gca()
        
    sns.heatmap(df, annot=True, cmap="YlGnBu", fmt=".3f", linewidths=.5, ax=ax, cbar_kws={'label': 'Score'})
    ax.set_title("Method Performance Summary")
    ax.set_ylabel("Method")
    ax.set_xlabel("Metric")
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        plt.close()

def plot_multipanel_summary(data_dict: dict, save_path: str = None):
    """
    Generate 4-panel summary figure (Radar, Boxplot, CD, Heatmap).
    """
    setup_publication_style()
    fig = plt.figure(figsize=(PUBLICATION_STYLE['double_column_width'], PUBLICATION_STYLE['max_height'] * 0.8))
    
    # GridSpec for complex layout
    gs = fig.add_gridspec(2, 2)
    
    # A. Radar Chart
    ax1 = fig.add_subplot(gs[0, 0], projection='polar')
    # Extract aggregated means for radar
    # Assuming data_dict['aggregated_means'] exists or similar
    # Need to construct it from the input data structure
    # For now, placeholder call (requires proper data prep in caller)
    ax1.set_title("A. Method Comparison", loc='left', fontsize=10, fontweight='bold')
    
    # B. Fidelity Boxplot
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title("B. Fidelity Distribution", loc='left', fontsize=10, fontweight='bold')
    
    # C. CD Diagram 
    # Note: CD diagram in sp plots to current axis or new figure? 
    # sp.critical_difference_diagram usually makes a new figure or uses generic plot.
    # It might be tricky to embed. Let's start with a placeholder or use rank bar chart.
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_title("C. Critical Differences", loc='left', fontsize=10, fontweight='bold')
    ax3.axis('off') # CD diagram drawing is custom
    
    # D. Heatmap
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_title("D. Metric Summary", loc='left', fontsize=10, fontweight='bold')

    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
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

def plot_metric_comparison_with_cis(data_dict: dict, metric_name: str, save_path: str = None):
    """
    Plot bar chart of means with error bars (CIs).
    
    Args:
        data_dict: Dict of structure {method: {'mean': X, 'ci_t': {'lower': L, 'upper': U}, ...}}
    """
    means = []
    lowers = []
    uppers = []
    methods = list(data_dict.keys())
    
    for m in methods:
        stats = data_dict[m]
        means.append(stats['mean'])
        lowers.append(stats['ci_t']['lower'])
        uppers.append(stats['ci_t']['upper'])
        
    yerr = [
        np.array(means) - np.array(lowers),
        np.array(uppers) - np.array(means)
    ]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(methods, means, yerr=yerr, capsize=10, alpha=0.7, color='skyblue', edgecolor='black')
    
    plt.title(f"Mean {metric_name} with 95% t-Distribution CIs")
    plt.ylabel(metric_name)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        plt.close()
