#!/usr/bin/env python3
"""Resolvers that re-derive manuscript numbers from committed analysis artifacts.

Each resolver maps a short source expression (used in pub/claim_registry.toml)
to a value computed from the artifact tree. Adding a new kind of claim means
adding a resolver here, not a new query language.
"""
from __future__ import annotations

import csv
import json
import math
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
EXP1_MODELS = ROOT / "experiments" / "exp1_adult" / "models"
EXP1_REPRO = ROOT / "experiments" / "exp1_adult" / "reproducibility" / "reproducibility_report.csv"
EXP2_INVENTORY = EXP2_STATS / "exp2_run_inventory.csv"


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


# ---------------------------------------------------------------------------
# EXP1 calibration cohort (Chapter 3 design tables)
# ---------------------------------------------------------------------------

# The thesis labels the gradient-boosting model "xgb" but its artifact
# directory is "xgboost". The manuscript cites the glob models/*/metrics.json,
# which resolves either way; the mapping only matters here.
_EXP1_DIRS = {"logreg": "logreg", "rf": "rf", "xgb": "xgboost", "svm": "svm", "mlp": "mlp"}


@lru_cache(maxsize=None)
def _exp1_metrics(model: str) -> dict:
    name = _EXP1_DIRS.get(model, model)
    path = EXP1_MODELS / name / "metrics.json"
    if not path.exists():
        raise MissingArtifact(f"artifact not found: {path.relative_to(ROOT).as_posix()}")
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def _exp1_confusion_totals() -> tuple[int, int]:
    """(test-set size, positive count) from any EXP1 model's confusion matrix.

    All five models are scored on the same held-out split, so the matrix
    totals are a property of the partition rather than of the model.
    """
    cm = _exp1_metrics("logreg")["confusion_matrix"]
    return sum(sum(row) for row in cm), sum(cm[1])


def _chi2_sf_df3(x: float) -> float:
    """P(chi^2_3 > x), closed form so the verifier stays stdlib-only.

    For df=3 the CDF is erf(sqrt(x/2)) - sqrt(2x/pi) e^{-x/2}; the survival
    function below is its complement. CI installs no packages, so scipy is
    not available to any resolver.
    """
    return math.erfc(math.sqrt(x / 2.0)) + math.sqrt(2.0 * x / math.pi) * math.exp(-x / 2.0)


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

    if kind in ("exp2_subset_mean", "exp2_subset_sd", "exp2_subset_cv"):
        # A single (model, N) stratum across its five seeds. This is the P1
        # reproducibility cell: the thesis reports it as "CV sobre EXP1" and
        # cites the EXP1 reproducibility report, but the printed values
        # re-derive exactly from the EXP2 run-level table and not from that
        # artifact (n_runs=9, different means). See review finding F14.
        method, metric, model, n = args
        values = [
            float(row[metric])
            for row in _exp2_run_level()
            if row["method"] == method
            and row["model"] == model
            and row["n"] == n
            and row[metric] not in ("", "nan")
        ]
        if not values:
            raise MissingArtifact(
                f"no EXP2 runs for {method}/{model}/N={n}/{metric}"
            )
        mean = statistics.mean(values)
        if kind == "exp2_subset_mean":
            return mean
        sd = statistics.stdev(values)  # sample SD: the printed values match it
        return sd if kind == "exp2_subset_sd" else 100.0 * sd / mean

    if kind in ("exp2_block_sd", "friedman_rank"):
        # Block-level dispersion and the Friedman mean ranks, both computed from
        # exp2_block_method_summary.csv over the 15 complete (g, N) blocks.
        metric = args[1] if kind == "exp2_block_sd" else args[0]
        rows = [
            row
            for row in _rows(EXP2_STATS / "exp2_block_method_summary.csv")
            if row[metric] not in ("", "nan")
        ]
        if kind == "exp2_block_sd":
            method = args[0]
            values = [float(r[metric]) for r in rows if r["method"] == method]
            if not values:
                raise MissingArtifact(f"no EXP2 blocks for {method}/{metric}")
            return statistics.stdev(values)

        target = args[1]
        blocks: dict[tuple[str, str], dict[str, float]] = {}
        for r in rows:
            blocks.setdefault((r["model"], r["n"]), {})[r["method"]] = float(r[metric])
        ranks: list[int] = []
        for cell in blocks.values():
            if len(cell) < 4:  # Friedman uses complete blocks only
                continue
            order = sorted(cell, key=lambda m: -cell[m])  # rank 1 = best
            ranks.append(order.index(target) + 1)
        if not ranks:
            raise MissingArtifact(f"no complete blocks for {metric}")
        return statistics.mean(ranks)

    if kind == "exp2_sd":
        method, metric = args
        values = [
            float(row[metric])
            for row in _exp2_run_level()
            if row["method"] == method and row[metric] not in ("", "nan")
        ]
        if not values:
            raise MissingArtifact(f"no EXP2 runs for {method}/{metric}")
        return statistics.stdev(values)

    if kind == "exp2_pooled_cv":
        # CV over every qualified run of a method, as a percentage. Distinct
        # from the per-stratum CV of the P1 cell; the thesis reports both and
        # had them the wrong way round for SHAP (F15).
        method, metric = args
        values = [
            float(row[metric])
            for row in _exp2_run_level()
            if row["method"] == method and row[metric] not in ("", "nan")
        ]
        if not values:
            raise MissingArtifact(f"no EXP2 runs for {method}/{metric}")
        return 100.0 * statistics.stdev(values) / statistics.mean(values)

    if kind == "exp2_n_mean":
        method, metric, n = args
        values = [
            float(row[metric])
            for row in _exp2_run_level()
            if row["method"] == method and row["n"] == n and row[metric] not in ("", "nan")
        ]
        if not values:
            raise MissingArtifact(f"no EXP2 runs for {method}/N={n}/{metric}")
        return statistics.mean(values)

    if kind in ("wilcoxon_meandiff", "wilcoxon_sd"):
        # The thesis reports the paired mean difference and its SD; the exported
        # table carries the two group means and d_z, from which both follow.
        comparison_set, metric = args
        name = "primary" if comparison_set == "primary" else "all_models"
        for row in _rows(EXP2_STATS / f"wilcoxon_shap_lime_{name}.csv"):
            if row["metric"] == metric:
                diff = float(row["shap_mean"]) - float(row["lime_mean"])
                if kind == "wilcoxon_meandiff":
                    return diff
                return diff / float(row["cohens_dz"])
        raise MissingArtifact(f"wilcoxon row not found: {comparison_set}/{metric}")

    if kind == "exp1_model_metric":
        model, metric = args
        return float(_exp1_metrics(model)[metric])

    if kind == "exp1_split":
        # "test" and "train" sizes of the canonical seed-42 partition, and the
        # positive-class rate as a percentage. The test size comes from the
        # confusion-matrix total; the training size from the dataset_shape
        # recorded when the model was fitted.
        (what,) = args
        n_test, n_pos = _exp1_confusion_totals()
        if what == "test":
            return float(n_test)
        if what == "positive_rate":
            return 100.0 * n_pos / n_test
        if what == "train":
            meta = json.loads(
                (EXP1_MODELS / "xgboost" / "xgb_metrics.json").read_text(encoding="utf-8")
            )
            return float(meta["training_metadata"]["dataset_shape"][0])
        raise ValueError(f"unknown exp1_split argument: {what}")

    if kind == "exp1_repro_cv_max":
        # Chapter 3 reports the EXP1 reproducibility profile as upper bounds
        # over the four cohort rows, so the resolver returns the maximum of the
        # column. The manuscript states each bound rounded up, so these claims
        # carry a tolerance rather than matching to the last digit.
        (metric,) = args
        rows = _rows(EXP1_REPRO)
        return max(float(row[f"{metric}_cv"]) for row in rows)

    if kind == "exp2_artifacts_present":
        # Rows in the run inventory: artifacts physically present, which is the
        # planned grid minus the one cell that was never written.
        return float(len(_rows(EXP2_INVENTORY)))

    if kind == "exp2_coverage_pct":
        # Analysable share of the planned grid. The complement of
        # exp2_missing_pct, stated directly because Chapter 3 tabulates it.
        planned = float(args[0]) if args else 300.0
        qualified = sum(
            len(_exp2_values(method, "fidelity"))
            for method in ("shap", "lime", "anchors", "dice")
        )
        return 100.0 * qualified / planned

    if kind == "exp2_method_coverage_pct":
        method, planned = args[0], float(args[1]) if len(args) > 1 else 75.0
        return 100.0 * len(_exp2_values(method, "fidelity")) / planned

    if kind == "exp2_block_replication":
        # Mean number of qualified seeds per (model, N) block for one method,
        # restricted to the |-separated models named. Chapter 3 uses the
        # worst-case models to bound the variance inflation of Anchors.
        method, models = args[0], args[1].split("|")
        counts: dict[tuple[str, str], int] = {}
        for row in _rows(EXP2_INVENTORY):
            if row["method"] != method or row["status"] != "ok_instance":
                continue
            if row["model"] not in models:
                continue
            counts[(row["model"], row["n"])] = counts.get((row["model"], row["n"]), 0) + 1
        grid = {(m, n) for m in models for n in {r["n"] for r in _rows(EXP2_INVENTORY)}}
        if not grid:
            raise MissingArtifact(f"no inventory rows for method={method}")
        return statistics.mean(counts.get(cell, 0) for cell in grid)

    if kind == "linear":
        # Composing resolver: "linear:<a>|<b>|<expr>" -> a * resolve(expr) + b.
        # Chapter 3's stress test is arithmetic performed inline on a registered
        # Friedman statistic; registering the results this way means they go red
        # if that statistic ever moves, which a structural declaration would not.
        rest = expr.split(":", 1)[1]
        a, b, sub = rest.split("|", 2)
        return float(a) * resolve(sub) + float(b)

    if kind == "chi2_sf3":
        # "chi2_sf3:<expr>" -> P(chi^2_3 > resolve(expr)).
        return _chi2_sf_df3(resolve(expr.split(":", 1)[1]))

    if kind == "diff":
        # Composing resolver: "diff:<exprA>|<exprB>" -> resolve(A) - resolve(B).
        # The operands are themselves colon-delimited, so they are separated by
        # "|" rather than ":". Chapters state gaps and ranges as differences of
        # quantities that are individually registered; without this they could
        # only be recorded as unbacked, which would be untrue -- they are
        # derivable, just not by a single lookup.
        left, sep, right = expr.split(":", 1)[1].partition("|")
        if not sep:
            raise ValueError(f"diff expects two |-separated expressions: {expr}")
        return resolve(left) - resolve(right)

    if kind == "exp2_missing_pct":
        # Share of the planned EXP2 grid with no analysable artifact, the
        # complement of the coverage percentage reported in Chapter 3.
        planned = float(args[0]) if args else 300.0
        qualified = sum(
            len(_exp2_values(method, "fidelity"))
            for method in ("shap", "lime", "anchors", "dice")
        )
        return 100.0 * (1.0 - qualified / planned)

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
