"""Select cases for human validation based on LLM judge disagreement."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.exp4_reliability_metrics import MultiJudgeComparison


def select_human_validation_cases(
    parsed_scores_path: Path,
    cases_manifest_path: Path,
    output_path: Path,
    n_cases: int = 80,
    per_explainer: bool = True,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Select cases for human validation based on maximum LLM disagreement.
    
    Strategy: Identify cases where multiple LLM judges disagree most.
    This tests whether LLM disagreement is justified (true ambiguity) or
    due to inherent LLM unreliability.
    
    Args:
        parsed_scores_path: Path to exp4_llm_scores.csv (multi-judge output)
        cases_manifest_path: Path to exp4_cases.jsonl or exp4_cases.csv
        output_path: Where to write human_validation_case_manifest.csv
        n_cases: Number of cases to select (default 80)
        per_explainer: If True, balance selection across explainers
        seed: Random seed for reproducibility
    
    Returns:
        DataFrame of selected cases with LLM scores and disagreement metadata
    """
    # Load parsed scores
    scores_df = pd.read_csv(parsed_scores_path)
    
    # Load case manifest
    if str(cases_manifest_path).endswith('.jsonl'):
        cases_df = pd.read_json(cases_manifest_path, lines=True)
    else:
        cases_df = pd.read_csv(cases_manifest_path)
    
    # Define score dimensions (use actual column names with _score suffix)
    score_dims = ['clarity_score', 'completeness_score', 'concision_score', 'semantic_plausibility_score',
                  'audit_usefulness_score', 'actionability_score', 'overall_quality_score']
    
    # Compute disagreement per case using primary condition
    primary_condition = 'hidden_label_primary'
    primary_scores = scores_df[scores_df['prompt_condition'] == primary_condition]
    
    # Aggregate to case-level means (across judges and replicates)
    case_means = primary_scores.groupby('case_id')[score_dims].mean().reset_index()
    
    # Compute per-case disagreement (std dev across judges)
    disagreement = MultiJudgeComparison.judge_disagreement_matrix(
        primary_scores,
        dimensions=score_dims,
        case_col='case_id',
        judge_col='judge_model'
    )
    
    # Merge disagreement with case metadata
    selected = disagreement.merge(cases_df, on='case_id', how='left')
    selected = selected.merge(case_means, on='case_id', how='left')
    
    # Sort by disagreement (highest first)
    selected = selected.sort_values('avg_disagreement_std', ascending=False)
    
    # Selection strategy: balanced by explainer if requested
    if per_explainer:
        explainers = cases_df['explainer'].unique()
        n_per_explainer = n_cases // len(explainers)
        remainder = n_cases % len(explainers)
        
        selected_cases = []
        for i, explainer in enumerate(sorted(explainers)):
            explainer_cases = selected[selected['explainer'] == explainer]
            n_to_select = n_per_explainer + (1 if i < remainder else 0)
            selected_cases.append(explainer_cases.head(n_to_select))
        
        selected = pd.concat(selected_cases, ignore_index=True)
    else:
        selected = selected.head(n_cases)
    
    # Ensure reproducibility
    selected = selected.sort_values('case_id').reset_index(drop=True)
    
    # Add human validation metadata
    selected['human_validation_assigned'] = False
    selected['human_validation_annotators'] = ''
    
    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    selected.to_csv(output_path, index=False)
    
    print(f"✅ Selected {len(selected)} cases for human validation")
    print(f"   Disagreement range: {selected['avg_disagreement_std'].min():.3f} - {selected['avg_disagreement_std'].max():.3f}")
    print(f"   Output: {output_path}")
    
    # Summary by explainer
    print("\nCases by explainer:")
    for explainer in sorted(selected['explainer'].unique()):
        count = len(selected[selected['explainer'] == explainer])
        mean_disagreement = selected[selected['explainer'] == explainer]['avg_disagreement_std'].mean()
        print(f"  {explainer}: {count} cases (mean disagreement: {mean_disagreement:.3f})")
    
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--parsed-scores",
        type=Path,
        default=Path("experiments/exp4_llm_evaluation/parsed_scores/exp4_llm_scores.csv"),
        help="Path to parsed LLM scores (multi-judge output)",
    )
    parser.add_argument(
        "--cases-manifest",
        type=Path,
        default=Path("experiments/exp4_llm_evaluation/cases/exp4_cases.csv"),
        help="Path to case inventory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/exp4_llm_evaluation/human_validation/case_manifest.csv"),
        help="Output path for human validation case manifest",
    )
    parser.add_argument(
        "--n-cases",
        type=int,
        default=80,
        help="Number of cases to select (default 80)",
    )
    parser.add_argument(
        "--per-explainer",
        action="store_true",
        default=True,
        help="Balance selection across explainers",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility",
    )
    args = parser.parse_args()
    
    select_human_validation_cases(
        parsed_scores_path=args.parsed_scores,
        cases_manifest_path=args.cases_manifest,
        output_path=args.output,
        n_cases=args.n_cases,
        per_explainer=args.per_explainer,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
