#!/usr/bin/env python3
"""Resolvers that re-derive manuscript numbers from committed analysis artifacts.

Each resolver maps a short source expression (used in pub/claim_registry.toml)
to a value computed from the artifact tree. Adding a new kind of claim means
adding a resolver here, not a new query language.
"""
from __future__ import annotations

import csv
import json
import statistics
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXP2_STATS = ROOT / "outputs" / "analysis" / "paper_a_exp2_stats"
EXP3_RESULTS = ROOT / "experiments" / "exp3_cross_dataset" / "results"
EXP3_LIME = ROOT / "outputs" / "analysis" / "exp3_lime_results.csv"
EXP4_DIR = ROOT / "outputs" / "analysis" / "exp4_llm_evaluation"
EXP6_PAIRED = ROOT / "outputs" / "analysis" / "exp6_masking_sensitivity" / "exp6_paired_shap_lime.csv"
LIME_KW = ROOT / "outputs" / "analysis" / "lime_kernel_width_sensitivity.csv"
ADULT = ROOT / "data" / "adult.csv"


class MissingArtifact(Exception):
    """Raised when a claim's backing artifact is not present in the tree."""


def _rows(path: Path) -> list[dict]:
    if not path.exists():
        raise MissingArtifact(f"artifact not found: {path.relative_to(ROOT).as_posix()}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


@lru_cache(maxsize=None)
def _exp2_run_level() -> list[dict]:
    return _rows(EXP2_STATS / "exp2_run_level_metrics.csv")


def _exp2_values(method: str, metric: str, model: str | None = None) -> list[float]:
    out = []
    for row in _exp2_run_level():
        if row["method"] != method:
            continue
        if model is not None and row["model"] != model:
            continue
        raw = row[metric]
        if raw not in ("", "nan"):
            out.append(float(raw))
    if not out:
        raise MissingArtifact(f"no EXP2 rows for method={method} metric={metric} model={model}")
    return out


@lru_cache(maxsize=None)
def _exp3_shap() -> dict:
    """3-seed means per (dataset, model) for the committed EXP3 SHAP cohort."""
    buckets: dict[tuple[str, str], list[dict]] = {}
    for path in sorted(EXP3_RESULTS.glob("*/*_shap/*/*/results.json")):
        parts = path.relative_to(EXP3_RESULTS).as_posix().split("/")
        dataset, cell = parts[0], parts[1]
        model = cell.rsplit("_", 1)[0]
        payload = json.loads(path.read_text(encoding="utf-8"))
        buckets.setdefault((dataset, model), []).append(payload["aggregated_metrics"])
    if not buckets:
        raise MissingArtifact("no EXP3 SHAP results under experiments/exp3_cross_dataset/results/")
    return buckets


@lru_cache(maxsize=None)
def _exp3_anchors() -> dict:
    buckets: dict[tuple[str, str], list[dict]] = {}
    for path in sorted(EXP3_RESULTS.glob("*/*_anchors/*/*/results.json")):
        parts = path.relative_to(EXP3_RESULTS).as_posix().split("/")
        dataset, cell = parts[0], parts[1]
        model = cell.rsplit("_", 1)[0]
        payload = json.loads(path.read_text(encoding="utf-8"))
        buckets.setdefault((dataset, model), []).append(payload["aggregated_metrics"])
    if not buckets:
        raise MissingArtifact(
            "no EXP3 Anchors results committed -- see RCA-001; these live on the "
            "results/exp3-* branches unless imported"
        )
    return buckets


@lru_cache(maxsize=None)
def _adult() -> list[dict]:
    return _rows(ADULT)


def _cramers_v(col_a: str, col_b: str) -> float:
    """Cramer's V over pairwise-complete cases of the Adult dataset (Table S3).

    Rows missing either value are dropped. `workclass` and `occupation` are
    missing on the same records, so admitting missingness as its own category
    would manufacture a spurious association between them (V rises from 0.216
    to 0.400) -- see F03 in the 2026-08-28 supplementary verification.

    Implemented over the chi-square statistic directly so the verifier stays
    stdlib-only; no p-value is needed, so scipy is not required.
    """
    rows = _adult()
    table: dict[str, dict[str, int]] = {}
    row_tot: dict[str, int] = {}
    col_tot: dict[str, int] = {}
    n = 0
    for row in rows:
        a, b = row[col_a], row[col_b]
        if a == "" or b == "":
            continue
        table.setdefault(a, {})[b] = table.setdefault(a, {}).get(b, 0) + 1
        row_tot[a] = row_tot.get(a, 0) + 1
        col_tot[b] = col_tot.get(b, 0) + 1
        n += 1
    chi2 = 0.0
    for a, arow in table.items():
        for b, expected_b in col_tot.items():
            expected = row_tot[a] * expected_b / n
            observed = arow.get(b, 0)
            chi2 += (observed - expected) ** 2 / expected
    denom = n * (min(len(row_tot), len(col_tot)) - 1)
    return (chi2 / denom) ** 0.5


def _pearson_r(col_a: str, col_b: str) -> float:
    """Pearson r between two numeric Adult columns (Supplementary Table S3)."""
    xs, ys = [], []
    for row in _adult():
        try:
            xs.append(float(row[col_a]))
            ys.append(float(row[col_b]))
        except (TypeError, ValueError):
            continue
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = (
        sum((x - mx) ** 2 for x in xs) ** 0.5 * sum((y - my) ** 2 for y in ys) ** 0.5
    )
    return num / den


def resolve(expr: str) -> float:
    """Resolve one source expression to a number derived from the artifacts."""
    kind, *args = expr.split(":")

    if kind == "exp2_mean":
        method, metric = args
        return statistics.mean(_exp2_values(method, metric))

    if kind == "exp2_median":
        method, metric = args
        return statistics.median(_exp2_values(method, metric))

    if kind == "exp2_model_mean":
        method, metric, model = args
        return statistics.mean(_exp2_values(method, metric, model))

    if kind == "exp2_runs":
        (method,) = args
        return float(len(_exp2_values(method, "fidelity")))

    if kind == "exp2_block_mean":
        # Block-level means differ from run-level means for Anchors and DiCE,
        # whose (g,s,N) coverage is incomplete. Paper A's global table is
        # block-level; the thesis per-method profile is run-level.
        method, metric = args
        values = [
            float(row[metric])
            for row in _rows(EXP2_STATS / "exp2_block_method_summary.csv")
            if row["method"] == method and row[metric] not in ("", "nan")
        ]
        if not values:
            raise MissingArtifact(f"no EXP2 blocks for method={method} metric={metric}")
        return statistics.mean(values)

    if kind == "friedman":
        metric, field = args
        for row in _rows(EXP2_STATS / "friedman_results.csv"):
            if row["metric"] == metric:
                return float(row[field])
        raise MissingArtifact(f"friedman metric not found: {metric}")

    if kind == "wilcoxon":
        comparison_set, metric, field = args
        name = "primary" if comparison_set == "primary" else "all_models"
        for row in _rows(EXP2_STATS / f"wilcoxon_shap_lime_{name}.csv"):
            if row["metric"] == metric:
                return float(row[field])
        raise MissingArtifact(f"wilcoxon row not found: {comparison_set}/{metric}")

    if kind in ("exp3_shap", "exp3_anchors"):
        dataset, model, metric = args
        buckets = _exp3_shap() if kind == "exp3_shap" else _exp3_anchors()
        key = (dataset, model)
        if key not in buckets:
            raise MissingArtifact(f"EXP3 cell not found: {kind} {dataset}/{model}")
        return statistics.mean(agg[metric]["mean"] for agg in buckets[key])

    if kind == "exp3_lime":
        dataset, model, metric = args
        values = [
            float(row[f"{metric}_mean"])
            for row in _rows(EXP3_LIME)
            if row["dataset"] == dataset and row["model"] == model
        ]
        if not values:
            raise MissingArtifact(f"EXP3 LIME cell not found: {dataset}/{model}")
        return statistics.mean(values)

    if kind == "exp4":
        stat, dimension = args
        filename = "icc_analysis.csv" if stat == "icc" else "krippendorff_alpha.csv"
        column = "icc_2_1" if stat == "icc" else "krippendorff_alpha"
        for row in _rows(EXP4_DIR / filename):
            if row["dimension"] == dimension:
                return float(row[column])
        raise MissingArtifact(f"EXP4 {stat} not found for dimension {dimension}")

    if kind == "exp6_paired":
        # Supplementary Table S6. The two endpoints diverge: the top-k gap
        # attenuates monotonically under correlation-aware masking, the
        # drop-correlation delta does not (F03).
        scheme, metric = args
        for row in _rows(EXP6_PAIRED):
            if row["masking_scheme"] == scheme and row["metric"] == metric:
                return float(row["mean_delta_shap_minus_lime"])
        raise MissingArtifact(f"EXP6 pair not found: {scheme}/{metric}")

    if kind == "lime_kernel_width":
        # Supplementary Table S2.
        width, field = args
        for row in _rows(LIME_KW):
            if float(row["kernel_width"]) == float(width):
                return float(row[field])
        raise MissingArtifact(f"kernel_width not probed: {width}")

    if kind == "adult_cramers_v":
        return _cramers_v(*args)

    if kind == "adult_pearson_r":
        return _pearson_r(*args)

    if kind == "review_corpus_rows":
        paper = args[0] if args else "paper_c"
        path = {
            "paper_c": ROOT / "docs" / "reports" / "paper_c" / "paper_c_review_corpus.csv",
            "paper_bc": ROOT / "docs" / "reports" / "paper_bc" / "paper_bc_review_corpus.csv",
        }[paper]
        return float(len(_rows(path)))

    if kind == "exp4_n":
        (stat,) = args
        filename = "icc_analysis.csv" if stat == "icc" else "krippendorff_alpha.csv"
        rows = _rows(EXP4_DIR / filename)
        return float(rows[0]["n_cases"])

    raise MissingArtifact(f"unknown source expression: {expr}")
