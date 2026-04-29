"""Analysis exports for EXP4 LLM-as-evaluator results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from src.evaluation.exp4_cases import load_manifest, read_cases_jsonl
from src.evaluation.exp4_schema import SCORE_FIELDS
from src.evaluation.exp4_reliability_metrics import ICC, KrippendorffAlpha, MultiJudgeComparison


def analyze_exp4(manifest_path: Path) -> Dict[str, Any]:
    manifest = load_manifest(manifest_path)
    scores_path = manifest.paths.parsed_scores_dir / "exp4_llm_scores.csv"
    cases_path = manifest.paths.cases_dir / "exp4_cases.jsonl"
    output_dir = manifest.paths.analysis_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    scores = pd.read_csv(scores_path)
    analysis_scores = _analysis_scope(scores)
    cases = pd.DataFrame([case.model_dump(mode="json") for case in read_cases_jsonl(cases_path)])
    metrics = pd.json_normalize(cases["technical_metrics"]).add_prefix("metric_")
    cases_flat = pd.concat([cases.drop(columns=["technical_metrics"]), metrics], axis=1)
    data = analysis_scores.merge(cases_flat, on="case_id", how="left")

    outputs = {
        "score_summary": _score_summary(data),
        "reliability": _reliability(data),
        "interjudge_agreement": _interjudge_agreement(data),
        "metric_alignment": _metric_alignment(data),
        "bias_diagnostics": _bias_diagnostics(data),
    }
    
    # Add multi-judge metrics if 2+ judges present
    if data["judge_model"].nunique() >= 2:
        outputs["icc_analysis"] = _icc_per_dimension(data)
        outputs["krippendorff_alpha"] = _krippendorff_per_dimension(data)
        outputs["judge_disagreement"] = _judge_disagreement_matrix(data)
        outputs["judge_comparison_summary"] = _judge_comparison_summary(data)

    for name, frame in outputs.items():
        frame.to_csv(output_dir / f"{name}.csv", index=False)

    summary_md = _summary_markdown(data, outputs)
    (output_dir / "exp4_analysis_summary.md").write_text(summary_md, encoding="utf-8")
    (output_dir / "thesis_fragment_es.qmd").write_text(_thesis_fragment_es(data, outputs), encoding="utf-8")

    summary = {
        "parsed_score_rows": len(scores),
        "score_rows": len(analysis_scores),
        "excluded_non_real_rows": len(scores) - len(analysis_scores),
        "case_inventory_rows": len(cases),
        "scored_cases": analysis_scores["case_id"].nunique(),
        "analysis_dir": str(output_dir),
        "outputs": {name: str(output_dir / f"{name}.csv") for name in outputs},
    }
    (output_dir / "exp4_analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def _analysis_scope(scores: pd.DataFrame) -> pd.DataFrame:
    """Use real LLM judgments when present, preserving dry-run-only workflows."""
    judge_model = scores["judge_model"].fillna("").astype(str).str.lower()
    dry_run_like = judge_model.str.contains("dummy|dry-run|dry_run", regex=True)
    real_scores = scores[~dry_run_like].copy()
    return real_scores if not real_scores.empty else scores.copy()


def _score_summary(data: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["source_experiment", "dataset", "model_family", "explainer", "prompt_condition", "judge_model"]
    rows: List[Dict[str, Any]] = []
    for keys, group in data.groupby(group_cols, dropna=False):
        row = dict(zip(group_cols, keys))
        row["n_judgments"] = len(group)
        row["n_cases"] = group["case_id"].nunique()
        for field in SCORE_FIELDS:
            row[f"{field}_mean"] = group[f"{field}_score"].mean()
            row[f"{field}_std"] = group[f"{field}_score"].std()
        rows.append(row)
    return pd.DataFrame(rows)


def _reliability(data: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["case_id", "judge_model", "prompt_condition"]
    rows: List[Dict[str, Any]] = []
    for keys, group in data.groupby(group_cols, dropna=False):
        row = dict(zip(group_cols, keys))
        row["n_replicates"] = group["replicate"].nunique()
        for field in SCORE_FIELDS:
            row[f"{field}_std_across_replicates"] = group[f"{field}_score"].std(ddof=0)
            row[f"{field}_range_across_replicates"] = group[f"{field}_score"].max() - group[f"{field}_score"].min()
        rows.append(row)
    return pd.DataFrame(rows)


def _interjudge_agreement(data: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    if data["judge_model"].nunique() < 2:
        return pd.DataFrame([{"note": "inter-judge agreement requires at least two judge models"}])
    group_cols = ["case_id", "prompt_condition", "replicate"]
    for keys, group in data.groupby(group_cols, dropna=False):
        row = dict(zip(group_cols, keys))
        row["n_judges"] = group["judge_model"].nunique()
        for field in SCORE_FIELDS:
            row[f"{field}_judge_std"] = group[f"{field}_score"].std(ddof=0)
            row[f"{field}_exact_agreement"] = int(group[f"{field}_score"].nunique() == 1)
        rows.append(row)
    return pd.DataFrame(rows)


def _metric_alignment(data: pd.DataFrame) -> pd.DataFrame:
    metric_cols = [col for col in data.columns if col.startswith("metric_")]
    rows = []
    for score_field in SCORE_FIELDS:
        score_col = f"{score_field}_score"
        for metric_col in metric_cols:
            subset = data[[score_col, metric_col]].dropna()
            if (
                len(subset) < 3
                or subset[metric_col].nunique() < 2
                or subset[score_col].nunique() < 2
            ):
                corr = None
            else:
                corr = subset[score_col].corr(subset[metric_col], method="spearman")
            rows.append(
                {
                    "score_dimension": score_field,
                    "technical_metric": metric_col.replace("metric_", ""),
                    "spearman_correlation": corr,
                    "n": len(subset),
                }
            )
    return pd.DataFrame(rows)


def _bias_diagnostics(data: pd.DataFrame) -> pd.DataFrame:
    primary = data[data["prompt_condition"] == "hidden_label_primary"]
    visible = data[data["prompt_condition"] == "label_visible_bias_probe"]
    keys = ["case_id", "judge_model", "replicate"]
    rows = []
    if primary.empty or visible.empty:
        return pd.DataFrame([{"note": "bias diagnostics require hidden-label and label-visible conditions"}])
    merged = primary.merge(visible, on=keys, suffixes=("_hidden", "_visible"))
    for field in SCORE_FIELDS:
        delta = merged[f"{field}_score_visible"] - merged[f"{field}_score_hidden"]
        rows.append(
            {
                "score_dimension": field,
                "mean_visible_minus_hidden": delta.mean(),
                "median_visible_minus_hidden": delta.median(),
                "n_pairs": int(delta.count()),
            }
        )
    return pd.DataFrame(rows)


def _icc_per_dimension(data: pd.DataFrame) -> pd.DataFrame:
    """Compute ICC(2,1) per score dimension for inter-judge reliability."""
    # Map score column names to dimension names
    dimension_mapping = {
        "clarity_score": "clarity",
        "completeness_score": "completeness",
        "concision_score": "concision",
        "semantic_plausibility_score": "semantic_plausibility",
        "audit_usefulness_score": "audit_usefulness",
        "actionability_score": "actionability",
        "overall_quality_score": "overall_quality",
    }
    
    results = []
    for score_col, dim_name in dimension_mapping.items():
        if score_col not in data.columns:
            continue
        
        # Rename for ICC function
        temp_data = data[["case_id", "judge_model", score_col]].copy()
        temp_data.columns = ["case_id", "judge_model", "score"]
        
        icc_dict = ICC.icc_2_1(temp_data, judge_col="judge_model", case_col="case_id", score_col="score")
        results.append({
            "dimension": dim_name,
            **icc_dict,
        })
    
    return pd.DataFrame(results)


def _krippendorff_per_dimension(data: pd.DataFrame) -> pd.DataFrame:
    """Compute Krippendorff's alpha per score dimension for ordinal agreement."""
    dimension_mapping = {
        "clarity_score": "clarity",
        "completeness_score": "completeness",
        "concision_score": "concision",
        "semantic_plausibility_score": "semantic_plausibility",
        "audit_usefulness_score": "audit_usefulness",
        "actionability_score": "actionability",
        "overall_quality_score": "overall_quality",
    }
    
    results = []
    for score_col, dim_name in dimension_mapping.items():
        if score_col not in data.columns:
            continue
        
        # Rename for Krippendorff function
        temp_data = data[["case_id", "judge_model", score_col]].copy()
        temp_data.columns = ["case_id", "judge_model", "score"]
        
        alpha_dict = KrippendorffAlpha.alpha_ordinal(
            temp_data, judge_col="judge_model", case_col="case_id", score_col="score",
            min_val=1, max_val=5
        )
        results.append({
            "dimension": dim_name,
            **alpha_dict,
        })
    
    return pd.DataFrame(results)


def _judge_disagreement_matrix(data: pd.DataFrame) -> pd.DataFrame:
    """Compute case-level disagreement for human validation case selection."""
    dimensions = [col.replace("_score", "") for col in data.columns if col.endswith("_score")]
    
    return MultiJudgeComparison.judge_disagreement_matrix(
        data,
        dimensions=dimensions,
        case_col="case_id",
        judge_col="judge_model"
    )


def _judge_comparison_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Generate per-judge summary (mean/std) for each dimension."""
    dimensions = [col.replace("_score", "") for col in data.columns if col.endswith("_score")]
    
    return MultiJudgeComparison.judge_comparison_summary(
        data,
        dimensions=dimensions,
        judge_col="judge_model",
        groupby_cols=["judge_model"]
    )


def _summary_markdown(data: pd.DataFrame, outputs: Dict[str, pd.DataFrame]) -> str:
    lines = [
        "# EXP4 LLM Evaluation Analysis Summary",
        "",
        f"- Analyzed judgments: {len(data)}",
        f"- Unique cases: {data['case_id'].nunique()}",
        f"- Judge models: {', '.join(sorted(map(str, data['judge_model'].dropna().unique())))}",
        f"- Prompt conditions: {', '.join(sorted(map(str, data['prompt_condition'].dropna().unique())))}",
        "",
        "EXP4 is analyzed as semantic proxy evaluation evidence. These outputs support claims about LLM-judge reliability, semantic profile differences, metric alignment, and label-visibility sensitivity; they do not replace human-subject validation.",
    ]
    if not outputs["score_summary"].empty:
        overall = data["overall_quality_score"].mean()
        lines.append(f"\nMean overall quality across parsed judgments: {overall:.3f}.")
    return "\n".join(lines) + "\n"


def _thesis_fragment_es(data: pd.DataFrame, outputs: Dict[str, pd.DataFrame]) -> str:
    return (
        "EXP4 incorpora evaluadores basados en LLM como una medida semantica proxy "
        "para examinar claridad, completitud, concision, plausibilidad semantica, "
        "utilidad de auditoria, accionabilidad y calidad global de las explicaciones. "
        f"El paquete analizado contiene {len(data)} juicios sobre {data['case_id'].nunique()} casos. "
        "La evidencia se interpreta como complemento metodologico de los experimentos tecnicos, "
        "no como sustituto de validacion con participantes humanos.\n"
    )
