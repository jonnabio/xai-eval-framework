#!/usr/bin/env python3
"""Generate the review-motivated EXP2 SHAP-LIME block-level contrasts.

The input is the committed method summary over 15 ``(model, n)`` blocks. Each
method value in that summary is already the mean over its qualified seeds; this
script never treats seed-level runs as independent inferential blocks.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = (
    PROJECT_ROOT
    / "outputs"
    / "analysis"
    / "paper_a_exp2_stats"
    / "exp2_block_method_summary.csv"
)
DEFAULT_OUTPUT_DIR = DEFAULT_INPUT.parent
SOURCE_PATH = "outputs/analysis/paper_a_exp2_stats/exp2_block_method_summary.csv"

MODELS = ("logreg", "rf", "xgb", "svm", "mlp")
SAMPLE_SIZES = (50, 100, 200)
METHODS = ("shap", "lime")
PRIMARY_METRICS = (
    "fidelity",
    "stability",
    "sparsity",
    "faithfulness_gap",
    "cost",
)
OUTPUT_FILENAMES = (
    "paired_blocks_shap_lime.csv",
    "wilcoxon_shap_lime_blocks.csv",
    "sign_test_shap_lime_blocks.csv",
)


def holm_adjust(p_values: Iterable[float]) -> list[float]:
    """Return Holm-adjusted p-values in their original order."""
    values = np.asarray(list(p_values), dtype=float)
    order = np.argsort(values, kind="stable")
    adjusted_sorted = np.empty(len(values), dtype=float)
    running_max = 0.0
    for rank, index in enumerate(order):
        candidate = (len(values) - rank) * values[index]
        running_max = max(running_max, candidate)
        adjusted_sorted[rank] = min(1.0, running_max)

    adjusted = np.empty(len(values), dtype=float)
    adjusted[order] = adjusted_sorted
    return adjusted.tolist()


def load_block_summary(input_path: Path) -> pd.DataFrame:
    """Load and validate the committed block-level method summary."""
    if not input_path.is_file():
        raise FileNotFoundError(f"EXP2 block summary not found: {input_path}")

    frame = pd.read_csv(input_path)
    required = {"model", "n", "method", *PRIMARY_METRICS}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"block summary is missing columns: {', '.join(missing)}")
    if "seed" in frame.columns:
        raise ValueError(
            "seed-level input is invalid; expected aggregated (model, n) blocks"
        )

    normalized = frame["method"].astype(str).str.lower()
    mislabeled = normalized.isin(METHODS) & frame["method"].ne(normalized)
    if mislabeled.any():
        raise ValueError("SHAP/LIME method labels must be lowercase canonical names")

    paired_rows = frame[frame["method"].isin(METHODS)].copy()
    _validate_block_rows(paired_rows)
    return paired_rows


def _validate_block_rows(frame: pd.DataFrame) -> None:
    """Fail loudly when the SHAP-LIME block grid is not the declared 15 pairs."""
    if frame.duplicated(["model", "n", "method"]).any():
        raise ValueError("duplicate SHAP/LIME row for a (model, n) block")

    expected = {(model, n) for model in MODELS for n in SAMPLE_SIZES}
    for method in METHODS:
        method_rows = frame[frame["method"] == method]
        actual = set(zip(method_rows["model"], method_rows["n"], strict=True))
        if actual != expected:
            missing = sorted(expected.difference(actual))
            extra = sorted(actual.difference(expected))
            raise ValueError(
                f"{method} block mismatch; missing={missing}, extra={extra}"
            )

    if frame[list(PRIMARY_METRICS)].isna().any().any():
        raise ValueError("SHAP/LIME block metrics contain missing values")
    try:
        frame.loc[:, list(PRIMARY_METRICS)] = frame[list(PRIMARY_METRICS)].apply(
            pd.to_numeric, errors="raise"
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("SHAP/LIME block metrics must be numeric") from exc


def build_paired_blocks(frame: pd.DataFrame) -> pd.DataFrame:
    """Create one deterministic row per matched ``(model, n)`` block."""
    shap = frame[frame["method"] == "shap"].set_index(["model", "n"])
    lime = frame[frame["method"] == "lime"].set_index(["model", "n"])
    rows: list[dict[str, object]] = []
    for model in MODELS:
        for sample_size in SAMPLE_SIZES:
            row: dict[str, object] = {
                "model": model,
                "n": sample_size,
                "source": SOURCE_PATH,
            }
            for metric in PRIMARY_METRICS:
                shap_value = float(shap.loc[(model, sample_size), metric])
                lime_value = float(lime.loc[(model, sample_size), metric])
                row[f"shap_{metric}"] = shap_value
                row[f"lime_{metric}"] = lime_value
                row[f"difference_{metric}"] = shap_value - lime_value
            rows.append(row)
    return pd.DataFrame(rows)


def build_wilcoxon_results(paired: pd.DataFrame) -> pd.DataFrame:
    """Compute the five-test two-sided Wilcoxon family over 15 blocks."""
    rows: list[dict[str, object]] = []
    for metric in PRIMARY_METRICS:
        differences = paired[f"difference_{metric}"].to_numpy(dtype=float)
        result = stats.wilcoxon(
            differences,
            alternative="two-sided",
            zero_method="wilcox",
            method="exact",
        )
        rows.append(
            {
                "metric": metric,
                "n_blocks": len(differences),
                "shap_mean": paired[f"shap_{metric}"].mean(),
                "lime_mean": paired[f"lime_{metric}"].mean(),
                "mean_difference": differences.mean(),
                "median_difference": np.median(differences),
                "wilcoxon_statistic": float(result.statistic),
                "p_value_raw": float(result.pvalue),
                "alternative": "two-sided",
                "zero_method": "wilcox",
                "calculation_method": "exact",
                "multiplicity_family": "five_primary_metrics",
            }
        )

    result_frame = pd.DataFrame(rows)
    result_frame["p_value_holm"] = holm_adjust(result_frame["p_value_raw"])
    result_frame["reject_holm_0_05"] = result_frame["p_value_holm"] < 0.05
    return result_frame


def build_sign_test_results(paired: pd.DataFrame) -> pd.DataFrame:
    """Compute exact two-sided sign tests and direction counts for every metric."""
    rows: list[dict[str, object]] = []
    for metric in PRIMARY_METRICS:
        differences = paired[f"difference_{metric}"].to_numpy(dtype=float)
        n_positive = int(np.count_nonzero(differences > 0))
        n_negative = int(np.count_nonzero(differences < 0))
        n_ties = int(np.count_nonzero(differences == 0))
        n_nonzero = n_positive + n_negative
        p_value = 1.0
        if n_nonzero:
            p_value = stats.binomtest(
                n_positive, n_nonzero, p=0.5, alternative="two-sided"
            ).pvalue
        rows.append(
            {
                "metric": metric,
                "n_blocks": len(differences),
                "n_positive": n_positive,
                "n_negative": n_negative,
                "n_ties": n_ties,
                "n_nonzero": n_nonzero,
                "proportion_positive": n_positive / n_nonzero if n_nonzero else np.nan,
                "p_value_two_sided": float(p_value),
                "alternative": "two-sided",
            }
        )
    return pd.DataFrame(rows)


def write_outputs(input_path: Path, output_dir: Path) -> tuple[Path, ...]:
    """Generate and write the three deterministic review artifacts."""
    frame = load_block_summary(input_path)
    paired = build_paired_blocks(frame)
    outputs = (
        paired,
        build_wilcoxon_results(paired),
        build_sign_test_results(paired),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for output_frame, filename in zip(outputs, OUTPUT_FILENAMES, strict=True):
        path = output_dir / filename
        output_frame.to_csv(
            path, index=False, float_format="%.17g", lineterminator="\n"
        )
        paths.append(path)
    return tuple(paths)


def parse_args() -> argparse.Namespace:
    """Parse command-line paths for reproducible local or CI execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    """Run the block-level paired analysis and report written paths."""
    args = parse_args()
    for path in write_outputs(args.input, args.output_dir):
        print(
            path.relative_to(PROJECT_ROOT)
            if path.is_relative_to(PROJECT_ROOT)
            else path
        )


if __name__ == "__main__":
    main()
