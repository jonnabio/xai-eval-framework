#!/usr/bin/env python3
"""
Deterministic statistical analysis for Paper A (EXP2).

This script materializes all manuscript-facing inference tables from
`experiments/exp2_scaled/results` without manual spreadsheet work.

Outputs are written to:
    outputs/analysis/paper_a_exp2_stats/
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
import scikit_posthocs as sp
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parent.parent
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analysis.confidence import compute_cis


EXP2_RESULTS_DIR = PROJECT_ROOT / "experiments" / "exp2_scaled" / "results"
RECOVERY_BATCH_RESULTS = PROJECT_ROOT / "outputs" / "batch_results.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "analysis" / "paper_a_exp2_stats"

MODEL_ORDER = ["logreg", "rf", "xgb", "svm", "mlp"]
METHOD_ORDER = ["shap", "lime", "anchors", "dice"]
SEED_ORDER = [42, 123, 456, 789, 999]
N_ORDER = [50, 100, 200]
PRIMARY_METRICS = ["fidelity", "stability", "sparsity", "faithfulness_gap", "cost"]
PAIRWISE_METRICS = PRIMARY_METRICS
RECOVERY_NAME_RE = re.compile(r"rec_p1_exp2_([a-z0-9]+)_([a-z]+)_s(\d+)_n(\d+)")


@dataclass(frozen=True)
class RunKey:
    model: str
    method: str
    seed: int
    n: int


def holm_adjust(p_values: Iterable[float]) -> List[float]:
    """
    Holm-Bonferroni adjusted p-values (step-down), returned in original order.
    """
    p = np.asarray(list(p_values), dtype=float)
    m = len(p)
    if m == 0:
        return []
    order = np.argsort(p)
    p_sorted = p[order]
    adj_sorted = np.empty(m, dtype=float)
    running_max = 0.0
    for i in range(m):
        candidate = (m - i) * p_sorted[i]
        running_max = max(running_max, candidate)
        adj_sorted[i] = min(1.0, running_max)
    adjusted = np.empty(m, dtype=float)
    adjusted[order] = adj_sorted
    return adjusted.tolist()


def parse_result_file(path: Path) -> Tuple[Dict[str, float], str]:
    """
    Parse one EXP2 result artifact and return run-level metric means + status.
    """
    try:
        payload = json.loads(path.read_text())
    except Exception:
        return {}, "json_error"

    instances = payload.get("instance_evaluations", [])
    if not instances:
        return {}, "empty"

    metric_means: Dict[str, float] = {}
    for metric in ["fidelity", "stability", "sparsity", "faithfulness_gap"]:
        values = [row.get("metrics", {}).get(metric) for row in instances]
        values = [v for v in values if v is not None]
        if values:
            metric_means[metric] = float(np.mean(values))

    # Cost is defined as full run wall-clock normalized by analyzed instances.
    # This matches manuscript tables/figures generated for Paper A.
    duration_s = payload.get("experiment_metadata", {}).get("duration_seconds")
    if duration_s is not None and len(instances) > 0:
        metric_means["cost"] = float(duration_s) * 1000.0 / len(instances)
    else:
        values = [row.get("metrics", {}).get("cost") for row in instances]
        values = [v for v in values if v is not None]
        if values:
            metric_means["cost"] = float(np.mean(values))

    return metric_means, "ok_instance"


def load_exp2_runs() -> Tuple[pd.DataFrame, pd.DataFrame]:
    run_rows: List[Dict[str, object]] = []
    inventory_rows: List[Dict[str, object]] = []

    paths = sorted(EXP2_RESULTS_DIR.glob("*/*/n_*/results.json"))
    for path in paths:
        model, method = path.parts[-4].split("_", 1)
        seed = int(path.parts[-3].split("_")[1])
        n_value = int(path.parts[-2].split("_")[1])

        metrics, status = parse_result_file(path)
        inventory_rows.append(
            {
                "model": model,
                "method": method,
                "seed": seed,
                "n": n_value,
                "status": status,
                "path": str(path),
            }
        )
        if status != "ok_instance":
            continue

        row = {
            "model": model,
            "method": method,
            "seed": seed,
            "n": n_value,
            "path": str(path),
        }
        row.update(metrics)
        run_rows.append(row)

    return pd.DataFrame(run_rows), pd.DataFrame(inventory_rows)


def load_recovery_batch_overlay() -> pd.DataFrame:
    """
    Load optional recovery rows from outputs/batch_results.csv.

    These rows currently encode recovered EXP2 SHAP runs for the `mlp` and `svm`
    families. When present, they supersede same-key run-level metrics from the
    committed `exp2_scaled/results` tree and may also fill previously missing or
    malformed cells.
    """
    if not RECOVERY_BATCH_RESULTS.exists():
        return pd.DataFrame(
            columns=["model", "method", "seed", "n", "path"] + PRIMARY_METRICS
        )

    overlay_rows: List[Dict[str, object]] = []
    batch_df = pd.read_csv(RECOVERY_BATCH_RESULTS)
    for row in batch_df.to_dict(orient="records"):
        experiment_name = str(row.get("experiment_name", ""))
        match = RECOVERY_NAME_RE.fullmatch(experiment_name)
        if not match:
            continue

        model, method, seed, n_value = match.groups()
        overlay_rows.append(
            {
                "model": model,
                "method": method,
                "seed": int(seed),
                "n": int(n_value),
                "path": f"{RECOVERY_BATCH_RESULTS}::{experiment_name}",
                "fidelity": float(row["fidelity_mean"]),
                "stability": float(row["stability_mean"]),
                "sparsity": float(row["sparsity_mean"]),
                "faithfulness_gap": float(row["faithfulness_gap_mean"]),
                "cost": float(row["cost_mean"]),
            }
        )

    return pd.DataFrame(overlay_rows)


def apply_recovery_overlay(run_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """
    Overlay recovery batch rows onto committed EXP2 run-level metrics.
    """
    overlay_df = load_recovery_batch_overlay()
    if overlay_df.empty:
        return run_df.copy(), {"overlay_applied": False, "overlay_rows": 0, "overlay_replaced_existing_runs": 0}

    key_cols = ["model", "method", "seed", "n"]
    overlay_keys = set(tuple(row) for row in overlay_df[key_cols].itertuples(index=False, name=None))
    base_keys = set(tuple(row) for row in run_df[key_cols].itertuples(index=False, name=None))
    replaced_existing = len(base_keys & overlay_keys)

    base_without_overlay = run_df.loc[
        ~run_df[key_cols].apply(lambda row: tuple(row) in overlay_keys, axis=1)
    ].copy()
    merged = pd.concat([base_without_overlay, overlay_df], ignore_index=True)
    merged.sort_values(key_cols, inplace=True)
    return merged, {
        "overlay_applied": True,
        "overlay_rows": int(len(overlay_df)),
        "overlay_replaced_existing_runs": int(replaced_existing),
        "overlay_source": str(RECOVERY_BATCH_RESULTS),
    }


def find_complete_blocks(df: pd.DataFrame) -> List[Tuple[str, int]]:
    complete_blocks: List[Tuple[str, int]] = []
    for model in MODEL_ORDER:
        for n_value in N_ORDER:
            sub = df[(df["model"] == model) & (df["n"] == n_value)]
            if sub.empty:
                continue
            if not all((sub["method"] == m).any() for m in METHOD_ORDER):
                continue
            ok = True
            for method in METHOD_ORDER:
                method_sub = sub[sub["method"] == method]
                if any(method_sub[m].dropna().empty for m in PRIMARY_METRICS):
                    ok = False
                    break
            if ok:
                complete_blocks.append((model, n_value))
    return complete_blocks


def build_block_method_summary(
    df: pd.DataFrame, complete_blocks: List[Tuple[str, int]]
) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for model, n_value in complete_blocks:
        block = df[(df["model"] == model) & (df["n"] == n_value)]
        for method in METHOD_ORDER:
            sub = block[block["method"] == method]
            row: Dict[str, object] = {"model": model, "n": n_value, "method": method}
            for metric in PRIMARY_METRICS:
                row[metric] = float(sub[metric].mean())
            rows.append(row)
    return pd.DataFrame(rows)


def run_friedman_and_nemenyi(block_summary_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    friedman_rows: List[Dict[str, object]] = []
    nemenyi_tables: Dict[str, pd.DataFrame] = {}

    raw_p_values: List[float] = []
    tmp_rows: List[Dict[str, object]] = []
    for metric in PRIMARY_METRICS:
        mat = block_summary_df.pivot_table(
            index=["model", "n"], columns="method", values=metric
        ).reindex(columns=METHOD_ORDER)
        stat, p_value = stats.friedmanchisquare(*[mat[m].values for m in METHOD_ORDER])
        n_blocks = mat.shape[0]
        k_methods = mat.shape[1]
        kendall_w = float(stat / (n_blocks * (k_methods - 1))) if n_blocks > 0 else np.nan

        row = {
            "metric": metric,
            "n_blocks": n_blocks,
            "n_methods": k_methods,
            "friedman_statistic": float(stat),
            "p_value_raw": float(p_value),
            "kendall_w": kendall_w,
            "significant_raw_alpha_0_05": bool(p_value < 0.05),
        }
        tmp_rows.append(row)
        raw_p_values.append(float(p_value))

        mat_simple = mat.copy()
        mat_simple.index = np.arange(len(mat_simple))
        nemenyi = sp.posthoc_nemenyi_friedman(mat_simple)
        nemenyi = nemenyi.reindex(index=METHOD_ORDER, columns=METHOD_ORDER)
        nemenyi_tables[metric] = nemenyi

    adjusted = holm_adjust(raw_p_values)
    for row, p_adj in zip(tmp_rows, adjusted):
        row["p_value_holm"] = float(p_adj)
        row["significant_holm_alpha_0_05"] = bool(p_adj < 0.05)
        friedman_rows.append(row)

    friedman_df = pd.DataFrame(friedman_rows)
    return friedman_df, nemenyi_tables


def build_matched_pairs(df: pd.DataFrame, models: List[str]) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for model in models:
        for seed in SEED_ORDER:
            for n_value in N_ORDER:
                shap_row = df[
                    (df["model"] == model)
                    & (df["method"] == "shap")
                    & (df["seed"] == seed)
                    & (df["n"] == n_value)
                ]
                lime_row = df[
                    (df["model"] == model)
                    & (df["method"] == "lime")
                    & (df["seed"] == seed)
                    & (df["n"] == n_value)
                ]
                if len(shap_row) != 1 or len(lime_row) != 1:
                    continue
                record: Dict[str, object] = {
                    "model": model,
                    "seed": seed,
                    "n": n_value,
                }
                for metric in PAIRWISE_METRICS:
                    record[f"shap_{metric}"] = float(shap_row.iloc[0][metric])
                    record[f"lime_{metric}"] = float(lime_row.iloc[0][metric])
                    record[f"diff_{metric}"] = float(
                        shap_row.iloc[0][metric] - lime_row.iloc[0][metric]
                    )
                rows.append(record)
    return pd.DataFrame(rows)


def cohens_dz(diff_values: np.ndarray) -> float:
    if diff_values.size < 2:
        return float("nan")
    std = float(np.std(diff_values, ddof=1))
    if np.isclose(std, 0.0):
        return 0.0
    return float(np.mean(diff_values) / std)


def run_wilcoxon_suite(pair_df: pd.DataFrame, label: str) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    raw_p_values: List[float] = []
    tmp_rows: List[Dict[str, object]] = []

    for metric in PAIRWISE_METRICS:
        shap_vals = pair_df[f"shap_{metric}"].to_numpy(dtype=float)
        lime_vals = pair_df[f"lime_{metric}"].to_numpy(dtype=float)
        diff_vals = shap_vals - lime_vals
        stat, p_value = stats.wilcoxon(
            shap_vals,
            lime_vals,
            zero_method="wilcox",
            alternative="two-sided",
        )
        row = {
            "comparison_set": label,
            "metric": metric,
            "n_pairs": int(len(pair_df)),
            "wilcoxon_statistic": float(stat),
            "p_value_raw": float(p_value),
            "significant_raw_alpha_0_05": bool(p_value < 0.05),
            "shap_mean": float(np.mean(shap_vals)),
            "lime_mean": float(np.mean(lime_vals)),
            "shap_median": float(np.median(shap_vals)),
            "lime_median": float(np.median(lime_vals)),
            "median_diff": float(np.median(diff_vals)),
            "cohens_dz": cohens_dz(diff_vals),
        }
        tmp_rows.append(row)
        raw_p_values.append(float(p_value))

    adjusted = holm_adjust(raw_p_values)
    for row, p_adj in zip(tmp_rows, adjusted):
        row["p_value_holm"] = float(p_adj)
        row["significant_holm_alpha_0_05"] = bool(p_adj < 0.05)
        rows.append(row)

    return pd.DataFrame(rows)


def build_uncertainty_table(block_summary_df: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for method in METHOD_ORDER:
        sub = block_summary_df[block_summary_df["method"] == method]
        for metric in PRIMARY_METRICS:
            values = sub[metric].to_numpy(dtype=float)
            cis = compute_cis(values, confidence=0.95)
            mean_val = float(np.mean(values))
            std_val = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
            cv_val = float(std_val / mean_val) if not np.isclose(mean_val, 0.0) else float("nan")
            rows.append(
                {
                    "method": method,
                    "metric": metric,
                    "n_blocks": int(len(values)),
                    "mean": mean_val,
                    "std": std_val,
                    "cv": cv_val,
                    "ci_t_low": float(cis["t_dist"][0]),
                    "ci_t_high": float(cis["t_dist"][1]),
                    "ci_boot_low": float(cis["bootstrap"][0]),
                    "ci_boot_high": float(cis["bootstrap"][1]),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    run_df, inventory_df = load_exp2_runs()
    inventory_df.sort_values(["model", "method", "seed", "n"], inplace=True)
    run_df, overlay_meta = apply_recovery_overlay(run_df)
    run_df.sort_values(["model", "method", "seed", "n"], inplace=True)

    complete_blocks = find_complete_blocks(run_df)
    block_summary_df = build_block_method_summary(run_df, complete_blocks)
    block_summary_df.sort_values(["model", "n", "method"], inplace=True)

    friedman_df, nemenyi_tables = run_friedman_and_nemenyi(block_summary_df)
    friedman_df.sort_values("metric", inplace=True)

    pairs_primary = build_matched_pairs(run_df, ["logreg", "rf", "xgb"])
    pairs_all = build_matched_pairs(run_df, MODEL_ORDER)
    pairs_primary.sort_values(["model", "seed", "n"], inplace=True)
    pairs_all.sort_values(["model", "seed", "n"], inplace=True)

    wilcoxon_primary_df = run_wilcoxon_suite(pairs_primary, "logreg_rf_xgb")
    wilcoxon_all_df = run_wilcoxon_suite(pairs_all, "all_models")

    uncertainty_df = build_uncertainty_table(block_summary_df)
    uncertainty_df.sort_values(["method", "metric"], inplace=True)

    # Persist tabular outputs
    inventory_df.to_csv(OUTPUT_DIR / "exp2_run_inventory.csv", index=False)
    run_df.to_csv(OUTPUT_DIR / "exp2_run_level_metrics.csv", index=False)
    block_summary_df.to_csv(OUTPUT_DIR / "exp2_block_method_summary.csv", index=False)
    friedman_df.to_csv(OUTPUT_DIR / "friedman_results.csv", index=False)
    wilcoxon_primary_df.to_csv(OUTPUT_DIR / "wilcoxon_shap_lime_primary.csv", index=False)
    wilcoxon_all_df.to_csv(OUTPUT_DIR / "wilcoxon_shap_lime_all_models.csv", index=False)
    uncertainty_df.to_csv(OUTPUT_DIR / "method_uncertainty_over_blocks.csv", index=False)
    pairs_primary.to_csv(OUTPUT_DIR / "paired_cells_shap_lime_primary.csv", index=False)
    pairs_all.to_csv(OUTPUT_DIR / "paired_cells_shap_lime_all_models.csv", index=False)

    for metric, table in nemenyi_tables.items():
        table.to_csv(OUTPUT_DIR / f"nemenyi_{metric}.csv")

    status_counts = inventory_df["status"].value_counts().to_dict()
    summary = {
        "source_dir": str(EXP2_RESULTS_DIR),
        "overlay_batch_results_csv": overlay_meta.get("overlay_source"),
        "output_dir": str(OUTPUT_DIR),
        "present_files": int(len(inventory_df)),
        "status_counts": status_counts,
        "analyzable_runs": int(len(run_df)),
        "overlay_applied": bool(overlay_meta.get("overlay_applied", False)),
        "overlay_rows": int(overlay_meta.get("overlay_rows", 0)),
        "overlay_replaced_existing_runs": int(overlay_meta.get("overlay_replaced_existing_runs", 0)),
        "complete_blocks": [list(b) for b in complete_blocks],
        "n_complete_blocks": int(len(complete_blocks)),
        "n_pairs_primary_logreg_rf_xgb": int(len(pairs_primary)),
        "n_pairs_all_models": int(len(pairs_all)),
        "metrics": PRIMARY_METRICS,
        "methods": METHOD_ORDER,
        "models": MODEL_ORDER,
    }
    (OUTPUT_DIR / "analysis_summary.json").write_text(json.dumps(summary, indent=2))

    print(f"Analysis artifacts written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
