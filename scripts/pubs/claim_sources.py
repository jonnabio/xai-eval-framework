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
