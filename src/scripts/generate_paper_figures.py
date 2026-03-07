
import sys
import json
import logging
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Add project root to path
sys.path.append(str(Path.cwd()))

from src.analysis.visualization import (
    setup_publication_style,
    plot_radar_chart,
    plot_metric_heatmap,
    plot_multipanel_summary,
    PUBLICATION_STYLE,
    METHOD_COLORS
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PaperFigures")

OUTPUT_DIR = Path("outputs/paper_figures")
FIGURES_DIR = OUTPUT_DIR / "figures"

# Data Paths
DATA_SOURCES = {
    'cv_results': {
        'rf_lime': "outputs/cv/exp1_cv_rf_lime/cv_summary.json",
        'rf_shap': "outputs/cv/exp1_cv_rf_shap/cv_summary.json",
        'xgb_lime': "outputs/cv/exp1_cv_xgb_lime/cv_summary.json",
        'xgb_shap': "outputs/cv/exp1_cv_xgb_shap/cv_summary.json"
    },
    'sensitivity': "outputs/sensitivity/sensitivity_results.json",
    # Add other paths if needed (e.g. stats results)
}

def check_data_availability():
    """Check availability of required data files."""
    available = {}
    
    # Check CV
    cv_available = True
    for key, path in DATA_SOURCES['cv_results'].items():
        if not Path(path).exists():
            logger.warning(f"Missing CV result for {key}: {path}")
            cv_available = False
    available['cv'] = cv_available
    
    # Check Sensitivity
    sens_path = Path(DATA_SOURCES['sensitivity'])
    if not sens_path.exists():
        logger.warning(f"Missing Sensitivity results: {sens_path}")
        available['sensitivity'] = False
    else:
        available['sensitivity'] = True
        
    return available

def load_cv_data():
    """Load CV summary results."""
    data = {}
    for key, path in DATA_SOURCES['cv_results'].items():
        p = Path(path)
        if p.exists():
            with open(p, 'r') as f:
                data[key] = json.load(f)
    return data

def prepare_radar_data(cv_data):
    """Extract mean metrics for radar chart."""
    radar_data = {}
    # Structure needed: {method: {metric: value}}
    for method, content in cv_data.items():
        # content has 'aggregated_metrics'
        agg = content.get('aggregated_metrics', {})
        metrics = {}
        for m, stats in agg.items():
            metrics[m] = stats['mean']
        radar_data[method] = metrics
    return radar_data

def prepare_heatmap_data(cv_data):
    """Create DataFrame for heatmap (Method x Metric)."""
    rows = []
    for method, content in cv_data.items():
        agg = content.get('aggregated_metrics', {})
        row = {'Method': method}
        for m, stats in agg.items():
            row[m] = stats['mean']
        rows.append(row)
    
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.set_index('Method')
    return df

def generate_figure_latex(figures_meta):
    """Generate LaTeX include file."""
    content = ""
    for fig in figures_meta:
        content += f"""
\\begin{{figure}}[htbp]
    \\centering
    \\includegraphics[width={fig['width']}]{{figures/{fig['filename']}}}
    \\caption{{{fig['caption']}}}
    \\label{{{fig['label']}}}
\\end{{figure}}
"""
    with open(OUTPUT_DIR / "figures_include.tex", "w") as f:
        f.write(content)

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    setup_publication_style()
    
    availability = check_data_availability()
    figures_meta = []
    
    if availability['cv']:
        logger.info("Generating Main Result Figures (CV)...")
        cv_data = load_cv_data()
        
        # 1. Radar Chart
        radar_data = prepare_radar_data(cv_data)
        metrics = ['fidelity', 'stability', 'sparsity', 'cost']
        methods = list(radar_data.keys())
        
        plot_radar_chart(
            radar_data, 
            metrics, 
            methods, 
            save_path=str(FIGURES_DIR / "fig1_radar_comparison.pdf")
        )
        figures_meta.append({
            'filename': "fig1_radar_comparison.pdf",
            'caption': "Comparison of XAI methods across evaluation metrics (normalized).",
            'label': "fig:radar",
            'width': "0.5\\textwidth"
        })
        
        # 2. Heatmap
        heatmap_df = prepare_heatmap_data(cv_data)
        plot_metric_heatmap(
            heatmap_df,
            save_path=str(FIGURES_DIR / "fig2_metric_heatmap.pdf")
        )
        figures_meta.append({
            'filename': "fig2_metric_heatmap.pdf",
            'caption': "Heatmap of metric performance by method.",
            'label': "fig:heatmap",
            'width': "0.6\\textwidth"
        })
        
        # 3. Multipanel Summary
        # Note: Multipanel needs specific data structures. 
        # For now, we reuse radar_data for panel A.
        # We need to implement proper data passing for other panels in plot_multipanel_summary
        # Passing 'radar_data' as a placeholder dict
        plot_multipanel_summary(
            {'aggregated_means': radar_data},
            save_path=str(FIGURES_DIR / "fig3_multipanel_summary.pdf")
        )
        figures_meta.append({
            'filename': "fig3_multipanel_summary.pdf",
            'caption': "Summary of experimental results.",
            'label': "fig:summary",
            'width': "\\textwidth"
        })
        
    if availability['sensitivity']:
        logger.info("Generating Sensitivity Figures...")
        with open(DATA_SOURCES['sensitivity'], 'r') as f:
            sens_data = json.load(f)
            
        # Plot Logic for Sensitivity
        # We process 'lime' and 'shap' keys
        for method_type, content in sens_data.items():
            if method_type == 'summary':
                continue
            
            for config_name, details in content.items():
                param = details['parameter']
                values = details['values']
                metrics_data = details['metrics']
                
                # Plot each metric
                for metric_name, m_stats in metrics_data.items():
                    plt.figure(figsize=(PUBLICATION_STYLE['single_column_width'], PUBLICATION_STYLE['single_column_width']*0.75))
                    
                    xs = values
                    ys = m_stats['absolute_values']
                    base = m_stats['baseline_value']
                    
                    plt.plot(xs, ys, marker='o', markersize=4, label='Value', color=METHOD_COLORS.get(config_name.upper(), 'black'))
                    plt.axhline(base, linestyle='--', color='gray', alpha=0.7, label='Baseline')
                    plt.fill_between(xs, [base*0.95]*len(xs), [base*1.05]*len(xs), color='gray', alpha=0.1, label='±5% Region')
                    
                    plt.xscale('log')
                    plt.xlabel(param)
                    plt.ylabel(metric_name.capitalize())
                    plt.title(f"{config_name}: {metric_name} vs {param}")
                    # plt.legend() # Legend might clutter small plots
                    
                    safe_name = f"fig_sens_{config_name}_{metric_name}_{param}.pdf"
                    plt.tight_layout()
                    plt.savefig(FIGURES_DIR / safe_name)
                    plt.close()
                    
                    figures_meta.append({
                        'filename': safe_name,
                        'caption': f"Sensitivity of {metric_name} to {param} for {config_name}.",
                        'label': f"fig:sens_{config_name}_{metric_name}",
                        'width': "0.45\\textwidth"
                    })
        
    generate_figure_latex(figures_meta)
    logger.info(f"Figures generated in {FIGURES_DIR}")

if __name__ == "__main__":
    main()
