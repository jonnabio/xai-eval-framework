
import json
import logging
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from scipy import stats
import scikit_posthocs as sp

# Add project root to path
sys.path.append(str(Path.cwd()))

from src.analysis.stats import perform_friedman_test, perform_nemenyi_test, compute_cohens_dz
from src.analysis.visualization import plot_critical_difference_diagram, plot_metric_boxplots

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        if isinstance(obj, np.bool_): return bool(obj)
        return super(NpEncoder, self).default(obj)

def load_cv_data(experiments, base_dir="outputs/cv"):
    """
    Load fold-level metrics for all experiments.
    Returns a dict: metric -> DataFrame(folds x methods)
    """
    data = {}
    metrics_of_interest = ["faithfulness_gap", "stability", "sparsity", "cost", "fidelity"]
    
    # Initialize data structure
    # {metric: {method: [score_fold1, ...]}}
    metric_data = {m: {} for m in metrics_of_interest}
    
    for exp_name in experiments:
        path = Path(base_dir) / exp_name / "cv_summary.json"
        
        if not path.exists():
            logger.warning(f"Results not found for {exp_name} at {path}")
            continue
            
        with open(path, 'r') as f:
            summary = json.load(f)
            
        folds = summary.get('folds', [])
        if len(folds) != 5:
            logger.warning(f"Expected 5 folds for {exp_name}, found {len(folds)}")
            
        # Sort by fold to ensure alignment
        folds.sort(key=lambda x: x['fold'])
        
        for m in metrics_of_interest:
            scores = []
            for fold in folds:
                # Handle nested structure if needed, but summary usually has flat metrics or aggregated
                # Based on previous `cat`, it's fold['metrics'][metric]['mean'] 
                # Wait, fold['metrics'][metric] is a dict with mean, std etc. for that fold?
                # No, fold['metrics'] in cv_runner output was:
                # "metrics": { "cost": { "mean": X, ...} }
                # Actually, the fold-level metric should be the MEAN of instances in that fold.
                # Yes, we use the fold mean as the single observation for that fold.
                
                val = fold['metrics'].get(m, {}).get('mean')
                if val is not None:
                    scores.append(val)
                else:
                    logger.warning(f"Metric {m} missing in fold {fold['fold']} for {exp_name}")
                    scores.append(np.nan)
            
            metric_data[m][exp_name] = scores
            
    # Convert to DataFrames
    dfs = {}
    for m, d in metric_data.items():
        if not d: continue
        df = pd.DataFrame(d)
        # Check for NaNs
        if df.isnull().values.any():
            logger.warning(f"NaNs found in data for {m}, dropping incomplete rows/cols or imputing?")
            # For now just warn
        dfs[m] = df
        
    return dfs

def run_analysis():
    experiments = [
        "exp1_cv_rf_lime", 
        "exp1_cv_rf_shap", 
        "exp1_cv_xgb_lime", 
        "exp1_cv_xgb_shap"
    ]
    
    # Short names for plotting
    aliases = {
        "exp1_cv_rf_lime": "RF+LIME",
        "exp1_cv_rf_shap": "RF+SHAP",
        "exp1_cv_xgb_lime": "XGB+LIME",
        "exp1_cv_xgb_shap": "XGB+SHAP"
    }
    
    logger.info("Loading CV data...")
    dfs = load_cv_data(experiments)
    
    results = {
        "data_source": "cv_fold_aggregates",
        "n_observations": 5,
        "metrics": {}
    }
    
    output_dir = Path("outputs/analysis")
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(exist_ok=True)
    
    for metric, df in dfs.items():
        logger.info(f"Analyzing {metric}...")
        
        # Rename columns for better display
        df_display = df.rename(columns=aliases)
        
        # 1. Boxplots
        plot_metric_boxplots(df_display, metric, str(figures_dir / f"boxplot_{metric}.png"))
        
        metric_res = {}
        
        # 2. Friedman Test
        try:
            stat, p = perform_friedman_test(df_display.to_dict(orient='list'))
            metric_res["friedman"] = {
                "statistic": stat,
                "p_value": p,
                "significant": p < 0.05
            }
            logger.info(f"  Friedman p={p:.4f}")
        except Exception as e:
            logger.error(f"  Friedman test failed: {e}")
            metric_res["friedman"] = {"error": str(e)}
            p = 1.0
            
        # 3. Post-Hoc (if significant)
        if p < 0.05:
            logger.info("  Significant! Running Nemenyi...")
            try:
                p_values = perform_nemenyi_test(df_display)
                
                # Convert to dict for JSON
                # p_values is a DataFrame
                pairwise_dict = {}
                for c1 in p_values.columns:
                    for c2 in p_values.columns:
                        if c1 < c2: # Avoid duplicates
                            pairwise_dict[f"{c1}_vs_{c2}"] = p_values.loc[c1, c2]
                            
                metric_res["post_hoc"] = {
                    "test": "nemenyi",
                    "pairwise_p_values": pairwise_dict
                }
                
                # Plot CD Diagram
                # For CD Diagram using scikit-posthocs, typically we need ranks and N
                # But sp.critical_difference_diagram takes ranks and computes CD
                # Let's compute ranks manually
                ranks = df_display.rank(axis=1, ascending=False).mean()
                # Determine q_alpha for Nemenyi at alpha=0.05
                # k = len(df_display.columns)
                # n = len(df_display)
                # We can let the library handle it if we find the right function, 
                # but currently plot_critical_difference_diagram calls sp.critical_difference_diagram(ranks, cd)
                
                # NOTE: Nemenyi CD = q * sqrt(k(k+1)/6N)
                # We will approximate or try to extract from library if possible, 
                # else we skip CD plotting to avoid error if complex to calculate manually
                # Actually, let's use a simpler approach for now: skip CD plot if library usage is ambiguous
                # verifying the args for sp.critical_difference_diagram
                
                # Try plotting
                # Note: sp.critical_difference_diagram(ranks, sig_matrix) 
                # Pass the p_values dataframe as sig_matrix
                try:
                    import matplotlib.pyplot as plt
                    plt.figure(figsize=(10, 2))
                    sp.critical_difference_diagram(ranks, p_values)
                    plt.savefig(str(figures_dir / f"cd_diagram_{metric}.png"), bbox_inches='tight')
                    plt.close()
                except Exception as ex:
                    logger.warning(f"Could not plot CD diagram: {ex}")
                
            except Exception as e:
                logger.error(f"  Nemenyi failed: {e}")
                
        # 4. Effect Sizes (Cohen's dz)
        effect_sizes = {}
        cols = df_display.columns
        for i in range(len(cols)):
            for j in range(i+1, len(cols)):
                c1, c2 = cols[i], cols[j]
                dz = compute_cohens_dz(df_display[c1], df_display[c2])
                effect_sizes[f"{c1}_vs_{c2}"] = dz
        
        metric_res["effect_sizes"] = effect_sizes
        results["metrics"][metric] = metric_res

    # Save Results
    with open(output_dir / "significance_results.json", 'w') as f:
        json.dump(results, f, indent=2, cls=NpEncoder)
        
    logger.info(f"Analysis complete. Results saved to {output_dir}")
    
    # Print Summary Table
    print("\n\n=== Statistical Analysis Summary ===")
    print(f"{'Metric':<20} | {'Friedman p':<12} | {'Significant?':<12}")
    print("-" * 50)
    for m, res in results['metrics'].items():
        fp = res.get('friedman', {}).get('p_value', 1.0)
        sig = "YES" if fp < 0.05 else "NO"
        print(f"{m:<20} | {fp:.4f}       | {sig:<12}")

if __name__ == "__main__":
    run_analysis()
