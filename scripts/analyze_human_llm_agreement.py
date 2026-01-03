#!/usr/bin/env python3
"""
Analyze agreement between human annotations and LLM scores.

Computes:
- Cohen's Kappa (inter-rater reliability)
- Pearson correlation
- Spearman correlation
- Confusion matrices
- Bland-Altman plots

Usage:
    python scripts/analyze_human_llm_agreement.py --output-dir experiments/exp1_adult/human_eval/analysis/
"""

import argparse
import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_annotations_with_llm(annotations_dir: Path) -> pd.DataFrame:
    """
    Load all annotations and merge with LLM scores.

    Returns DataFrame with columns:
    - sample_id, annotator_id
    - human_coherence, human_faithfulness, human_usefulness
    - llm_coherence, llm_faithfulness, llm_usefulness
    """
    # TODO: Implement after Phase 1 backend is deployed
    # Will use: GET /api/human-eval/admin/annotations
    pass

def compute_cohens_kappa(df: pd.DataFrame, dimension: str) -> float:
    """Compute Cohen's kappa for a dimension."""
    human_col = f"human_{dimension}"
    llm_col = f"llm_{dimension}"

    kappa = cohen_kappa_score(df[human_col], df[llm_col], weights='linear')
    return kappa

def compute_correlations(df: pd.DataFrame, dimension: str) -> Tuple[float, float, float, float]:
    """
    Compute Pearson and Spearman correlations.

    Returns: (pearson_r, pearson_p, spearman_rho, spearman_p)
    """
    human_col = f"human_{dimension}"
    llm_col = f"llm_{dimension}"

    pearson_r, pearson_p = pearsonr(df[human_col], df[llm_col])
    spearman_rho, spearman_p = spearmanr(df[human_col], df[llm_col])

    return pearson_r, pearson_p, spearman_rho, spearman_p

def plot_scatter(df: pd.DataFrame, dimension: str, output_path: Path):
    """Create scatter plot of human vs LLM scores."""
    plt.figure(figsize=(8, 6))

    human_col = f"human_{dimension}"
    llm_col = f"llm_{dimension}"

    sns.scatterplot(data=df, x=llm_col, y=human_col, alpha=0.6)

    # Add diagonal line
    plt.plot([1, 5], [1, 5], 'r--', alpha=0.5, label='Perfect agreement')

    plt.xlabel(f'LLM {dimension.capitalize()}')
    plt.ylabel(f'Human {dimension.capitalize()}')
    plt.title(f'Human vs LLM: {dimension.capitalize()}')
    plt.legend()
    plt.grid(alpha=0.3)

    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"Saved plot: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Analyze human-LLM agreement")
    parser.add_argument('--annotations-dir', type=Path,
                       default=Path("experiments/exp1_adult/human_eval/annotations"),
                       help="Directory with annotation JSON files")
    parser.add_argument('--output-dir', type=Path,
                       default=Path("experiments/exp1_adult/human_eval/analysis"),
                       help="Output directory for analysis results")

    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 70)
    logger.info("Human-LLM Agreement Analysis")
    logger.info("=" * 70)

    # Load data
    logger.info(f"\nLoading annotations from: {args.annotations_dir}")
    df = load_annotations_with_llm(args.annotations_dir)

    if df is None or df.empty:
        logger.error("No annotations found. Please ensure annotations have been submitted.")
        return

    logger.info(f"Loaded {len(df)} annotations")

    # Analyze each dimension
    dimensions = ['coherence', 'faithfulness', 'usefulness']
    results = {}

    for dim in dimensions:
        logger.info(f"\n--- {dim.upper()} ---")

        # Cohen's Kappa
        kappa = compute_cohens_kappa(df, dim)
        logger.info(f"Cohen's Kappa: {kappa:.3f}")

        # Correlations
        pearson_r, pearson_p, spearman_rho, spearman_p = compute_correlations(df, dim)
        logger.info(f"Pearson r: {pearson_r:.3f} (p={pearson_p:.4f})")
        logger.info(f"Spearman ρ: {spearman_rho:.3f} (p={spearman_p:.4f})")

        results[dim] = {
            "cohens_kappa": kappa,
            "pearson_r": pearson_r,
            "pearson_p": pearson_p,
            "spearman_rho": spearman_rho,
            "spearman_p": spearman_p
        }

        # Plot
        plot_path = args.output_dir / f"scatter_{dim}.png"
        plot_scatter(df, dim, plot_path)

    # Save results
    results_file = args.output_dir / "agreement_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    logger.info(f"\n✓ Results saved to: {results_file}")
    logger.info(f"✓ Plots saved to: {args.output_dir}")

if __name__ == "__main__":
    main()
