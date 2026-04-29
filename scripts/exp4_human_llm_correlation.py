"""Correlate human validation ratings with LLM scores."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, kendalltau


def compute_human_llm_correlation(
    human_responses_path: Path,
    parsed_scores_path: Path,
    case_manifest_path: Path,
    output_path: Path,
) -> pd.DataFrame:
    """
    Correlate human validation ratings with LLM scores.
    
    Maps human questions (5 simple) to LLM dimensions (7 semantic),
    computes Spearman correlation to validate LLM proxy reliability.
    
    Args:
        human_responses_path: Path to aggregated human responses CSV
        parsed_scores_path: Path to exp4_llm_scores.csv
        case_manifest_path: Path to human validation case manifest
        output_path: Where to write correlation results
    
    Returns:
        DataFrame with human→LLM correlations
    """
    # Load data
    human_df = pd.read_csv(human_responses_path)
    llm_df = pd.read_csv(parsed_scores_path)
    case_manifest = pd.read_csv(case_manifest_path)
    
    # Filter to cases in human validation set
    human_case_ids = case_manifest['case_id'].unique()
    llm_filtered = llm_df[llm_df['case_id'].isin(human_case_ids)]
    
    # Aggregate LLM scores to case level (mean across judges and replicates, primary condition)
    primary_condition = 'hidden_label_primary'
    llm_case_level = llm_filtered[llm_filtered['prompt_condition'] == primary_condition].groupby('case_id').agg({
        'clarity': 'mean',
        'completeness': 'mean',
        'concision': 'mean',
        'semantic_plausibility': 'mean',
        'audit_usefulness': 'mean',
        'actionability': 'mean',
        'overall_quality': 'mean',
    }).reset_index()
    
    # Human question → LLM dimension mapping (as per design)
    mapping = {
        'q1_clarity': 'clarity',
        'q2_completeness': 'completeness',
        'q3_concision': 'concision',
        'q4_plausibility': 'semantic_plausibility',
        'q5_audit_usefulness': 'audit_usefulness',
    }
    
    # Compute correlations
    results = []
    
    for human_q, llm_dim in mapping.items():
        # Merge human and LLM on case_id
        if human_q not in human_df.columns:
            continue
        
        merged = human_df[['case_id', human_q]].merge(
            llm_case_level[['case_id', llm_dim]],
            on='case_id',
            how='inner'
        )
        
        if len(merged) < 3:  # Need at least 3 points for correlation
            continue
        
        # Compute Spearman correlation
        rho, p_val = spearmanr(merged[human_q], merged[llm_dim])
        
        # Compute Kendall tau as secondary metric
        tau, tau_p = kendalltau(merged[human_q], merged[llm_dim])
        
        results.append({
            'human_question': human_q,
            'llm_dimension': llm_dim,
            'spearman_rho': rho,
            'spearman_p_value': p_val,
            'kendall_tau': tau,
            'kendall_p_value': tau_p,
            'n_cases': len(merged),
            'human_mean': merged[human_q].mean(),
            'human_std': merged[human_q].std(),
            'llm_mean': merged[llm_dim].mean(),
            'llm_std': merged[llm_dim].std(),
        })
    
    # Convert to DataFrame
    corr_df = pd.DataFrame(results)
    
    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    corr_df.to_csv(output_path, index=False)
    
    print(f"✅ Computed human-LLM correlations")
    print(f"   Output: {output_path}")
    print("\nCorrelation Summary:")
    print(corr_df[['human_question', 'llm_dimension', 'spearman_rho', 'spearman_p_value', 'n_cases']].to_string(index=False))
    
    return corr_df


def compute_inter_rater_reliability(
    human_responses_path: Path,
    overlap_cases: Optional[List[str]] = None,
    output_path: Optional[Path] = None,
) -> pd.DataFrame:
    """
    Compute inter-rater reliability (ICC) on human responses.
    
    Uses overlapping cases (rated by multiple annotators) to assess
    non-expert human inter-rater agreement.
    
    Args:
        human_responses_path: Path to human responses
        overlap_cases: List of case_ids rated by multiple annotators
        output_path: Where to write ICC results
    
    Returns:
        DataFrame with ICC values per question
    """
    from src.evaluation.exp4_reliability_metrics import ICC
    
    human_df = pd.read_csv(human_responses_path)
    
    # Filter to overlap cases (if specified)
    if overlap_cases:
        human_df = human_df[human_df['case_id'].isin(overlap_cases)]
    
    # Questions to analyze
    questions = ['q1_clarity', 'q2_completeness', 'q3_concision', 'q4_plausibility', 'q5_audit_usefulness']
    
    results = []
    
    for q in questions:
        if q not in human_df.columns:
            continue
        
        # Compute ICC(2,1) if we have annotator info
        icc_dict = ICC.icc_2_1(
            human_df,
            judge_col='annotator_id',  # Assumes 'annotator_id' column
            case_col='case_id',
            score_col=q
        )
        
        results.append({
            'question': q,
            **icc_dict,
        })
    
    icc_df = pd.DataFrame(results)
    
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        icc_df.to_csv(output_path, index=False)
        print(f"\n✅ Inter-rater reliability (ICC):")
        print(icc_df.to_string(index=False))
    
    return icc_df


def generate_human_validation_report(
    correlation_df: pd.DataFrame,
    icc_df: Optional[pd.DataFrame] = None,
    output_path: Path = Path("outputs/analysis/exp4_llm_evaluation/human_validation_report.md"),
) -> str:
    """Generate markdown report of human validation findings."""
    
    report_lines = [
        "# EXP4 Human Validation Study: Results & Analysis",
        "",
        "## Executive Summary",
        f"Human validation study correlating {len(correlation_df)} annotated cases with LLM proxy scores.",
        "",
        "## Human-LLM Correlation Analysis",
        "",
        "### Key Findings",
        "",
    ]
    
    # Identify strong correlations (ρ ≥ 0.50)
    strong_corr = correlation_df[correlation_df['spearman_rho'] >= 0.50]
    if len(strong_corr) > 0:
        report_lines.append("**Strong Agreement (ρ ≥ 0.50):**")
        for _, row in strong_corr.iterrows():
            report_lines.append(
                f"- {row['human_question']} ↔ {row['llm_dimension']}: "
                f"ρ = {row['spearman_rho']:.3f}, p = {row['spearman_p_value']:.4f}"
            )
        report_lines.append("")
    
    # Identify weak correlations (ρ < 0.30)
    weak_corr = correlation_df[correlation_df['spearman_rho'] < 0.30]
    if len(weak_corr) > 0:
        report_lines.append("**Weak or No Agreement (ρ < 0.30):**")
        for _, row in weak_corr.iterrows():
            report_lines.append(
                f"- {row['human_question']} ↔ {row['llm_dimension']}: "
                f"ρ = {row['spearman_rho']:.3f}, p = {row['spearman_p_value']:.4f}"
            )
        report_lines.append("")
    
    # Inter-rater reliability section
    if icc_df is not None and len(icc_df) > 0:
        report_lines.extend([
            "## Inter-Rater Reliability (Human Annotators)",
            "",
            "Intraclass Correlation Coefficient (ICC) on overlapping cases:",
            "",
        ])
        
        for _, row in icc_df.iterrows():
            icc_val = row['icc_2_1']
            if icc_val >= 0.75:
                agreement_level = "Excellent"
            elif icc_val >= 0.60:
                agreement_level = "Good"
            elif icc_val >= 0.40:
                agreement_level = "Fair"
            else:
                agreement_level = "Poor"
            
            report_lines.append(
                f"- {row['question']}: ICC = {icc_val:.3f} ({agreement_level})"
            )
        report_lines.append("")
    
    # Interpretation
    report_lines.extend([
        "## Interpretation",
        "",
        "### LLM Proxy Validity",
        f"- Mean Spearman ρ: {correlation_df['spearman_rho'].mean():.3f}",
        f"- Median Spearman ρ: {correlation_df['spearman_rho'].median():.3f}",
        "",
        "**Conclusion**: LLM proxy scores align with human judgments at level ",
        f"{'strong' if correlation_df['spearman_rho'].mean() >= 0.50 else 'moderate' if correlation_df['spearman_rho'].mean() >= 0.40 else 'weak'} ",
        "(ρ interpretation: ≥0.50 strong, 0.40-0.49 moderate, <0.30 weak).",
        "",
        "### Implications for Thesis",
        "1. LLM proxy can serve as reproducible semantic evaluation layer",
        "2. Dimensions with high human-LLM agreement validate proxy reliability",
        "3. Weak agreement dimensions suggest LLM limitations or human-LLM conceptual mismatch",
        "",
    ])
    
    report_text = "\n".join(report_lines)
    
    # Write report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text)
    
    print(f"\n✅ Report generated: {output_path}")
    
    return report_text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--human-responses",
        type=Path,
        default=Path("experiments/exp4_llm_evaluation/human_validation_responses.csv"),
        help="Path to aggregated human responses",
    )
    parser.add_argument(
        "--parsed-scores",
        type=Path,
        default=Path("experiments/exp4_llm_evaluation/parsed_scores/exp4_llm_scores.csv"),
        help="Path to parsed LLM scores",
    )
    parser.add_argument(
        "--case-manifest",
        type=Path,
        default=Path("experiments/exp4_llm_evaluation/human_validation/case_manifest.csv"),
        help="Path to human validation case manifest",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/analysis/exp4_llm_evaluation/human_llm_alignment.csv"),
        help="Output correlation results CSV",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("outputs/analysis/exp4_llm_evaluation/human_validation_report.md"),
        help="Output report markdown file",
    )
    args = parser.parse_args()
    
    # Compute correlations
    corr_df = compute_human_llm_correlation(
        human_responses_path=args.human_responses,
        parsed_scores_path=args.parsed_scores,
        case_manifest_path=args.case_manifest,
        output_path=args.output,
    )
    
    # Generate report
    generate_human_validation_report(
        correlation_df=corr_df,
        output_path=args.report,
    )


if __name__ == "__main__":
    main()
