"""Analysis exports for EXP4 LLM-as-evaluator results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from src.evaluation.exp4_cases import load_manifest, read_cases_jsonl
from src.evaluation.exp4_schema import SCORE_FIELDS


def analyze_exp4(manifest_path: Path) -> Dict[str, Any]:
    manifest = load_manifest(manifest_path)
    scores_path = manifest.paths.parsed_scores_dir / "exp4_llm_scores.csv"
    cases_path = manifest.paths.cases_dir / "exp4_cases.jsonl"
    output_dir = manifest.paths.analysis_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    scores = pd.read_csv(scores_path)
    cases = pd.DataFrame([case.model_dump(mode="json") for case in read_cases_jsonl(cases_path)])
    metrics = pd.json_normalize(cases["technical_metrics"]).add_prefix("metric_")
    cases_flat = pd.concat([cases.drop(columns=["technical_metrics"]), metrics], axis=1)
    data = scores.merge(cases_flat, on="case_id", how="left")

    outputs = {
        "score_summary": _score_summary(data),
        "reliability": _reliability(data),
        "interjudge_agreement": _interjudge_agreement(data),
        "metric_alignment": _metric_alignment(data),
        "bias_diagnostics": _bias_diagnostics(data),
    }

    for name, frame in outputs.items():
        frame.to_csv(output_dir / f"{name}.csv", index=False)

    summary_md = _summary_markdown(data, outputs)
    (output_dir / "exp4_analysis_summary.md").write_text(summary_md, encoding="utf-8")
    (output_dir / "thesis_fragment_es.qmd").write_text(_thesis_fragment_es(data, outputs), encoding="utf-8")

    summary = {
        "score_rows": len(scores),
        "case_rows": len(cases),
        "analysis_dir": str(output_dir),
        "outputs": {name: str(output_dir / f"{name}.csv") for name in outputs},
    }
    (output_dir / "exp4_analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


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
            if len(subset) < 3 or subset[metric_col].nunique() < 2:
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


def _summary_markdown(data: pd.DataFrame, outputs: Dict[str, pd.DataFrame]) -> str:
    lines = [
        "# EXP4 LLM Evaluation Analysis Summary",
        "",
        f"- Parsed judgments: {len(data)}",
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
