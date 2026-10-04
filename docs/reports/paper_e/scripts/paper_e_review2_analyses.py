#!/usr/bin/env python3
"""Paper E post hoc analyses added in response to the second rigor review of 2026-10-04.

ANALYSIS_PLAN.md section 9, second entry of 2026-10-04 (review findings F01 and F02). Both
are re-cuts of the stored explanations; no explainer is run.

  1. permutation   F01  Reference for the SHAP-LIME overlap: within each run, the SHAP list of
                        an instance is compared with the LIME list of another instance of the
                        same run, drawn at random (DRAWS draws per instance). The paired
                        overlap minus this value is the instance-specific part of the run.
  2. stability     F02  Median of the stored LIME stability by dataset and model, and the
                        smallest and largest model median per dataset. A dated deviation from
                        plan section 4, limited to this range.
  3. kernel        F02  Weight that LIME's kernel (width 3) gives to its perturbed samples.
                        LIME's sampling is reproduced from the package source: 999 samples
                        from a standard normal on the standardised scale (that is, around the
                        training mean), weight sqrt(exp(-d^2 / width^2)) with d the Euclidean
                        distance to the standardised instance. The instance itself has
                        weight 1. Needs the datasets (see paper_e_sign_contribution.py).

Aggregation is the plan's section 5: run means, mean of run means, seed-clustered percentile
bootstrap (2000 resamples, seed 20261003).

Writes outputs/analysis/paper_e/posthoc/review2_*.csv

    python docs/reports/paper_e/scripts/paper_e_review2_analyses.py
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_paper_e import primary_agreement  # noqa: E402
from paper_e_posthoc import ANALYSIS, BOOTSTRAP_SEED, OUT, bootstrap, run_path, write_csv  # noqa: E402
from paper_e_sign_contribution import split  # noqa: E402

DRAWS = 20                 # other instances drawn per instance
PERMUTATION_SEED = 20261004
KERNEL_WIDTH = 3.0         # the width of the stored LIME runs
LIME_SAMPLES = 999         # 1000 samples, the first of which is the instance itself
FIELDS = ("paired_top5_jaccard", "other_instance_top5_jaccard", "instance_specific_top5_jaccard")


def main() -> None:
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    draw = np.random.default_rng(PERMUTATION_SEED)
    with (ANALYSIS / "instance_agreement.csv").open(encoding="utf-8") as fh:
        instances = list(csv.DictReader(fh))
    blocks: dict[tuple, list[dict]] = defaultdict(list)
    for row in instances:
        blocks[(row["dataset"], row["model"], row["seed"], row["intensity"])].append(row)

    # --- 1. permutation reference -----------------------------------------------
    run_rows = []
    for block in sorted(blocks):
        dataset, model, seed, intensity = block
        stored = {m: {str(e["instance_id"]): e["explanation"]["raw_top"] for e in json.loads(
            run_path(dataset, model, seed, intensity, m).read_text(encoding="utf-8"))["instance_evaluations"]
            if e.get("explanation")} for m in ("shap", "lime")}
        ids = sorted((r["instance_id"] for r in blocks[block]), key=int)
        paired = [float(r["top5_jaccard"]) for r in blocks[block]]
        other = []
        for k, instance_id in enumerate(ids):
            for _ in range(DRAWS):
                j = int(draw.integers(len(ids) - 1))
                j += j >= k          # another instance of the run, uniformly
                other.append(primary_agreement(stored["shap"][instance_id], stored["lime"][ids[j]])["top5_jaccard"])
        run_rows.append({"dataset": dataset, "model": model, "seed": seed, "intensity": intensity,
                         "n_instances": len(ids), "paired_top5_jaccard": float(np.mean(paired)),
                         "other_instance_top5_jaccard": float(np.mean(other)),
                         "instance_specific_top5_jaccard": float(np.mean(paired) - np.mean(other))})
    write_csv(OUT / "review2_permutation_runs.csv", run_rows, list(run_rows[0]))

    summary = []
    for scope in ("model", "all"):
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for r in run_rows:
            groups[(r["dataset"], r["model"] if scope == "model" else "all")].append(r)
        for (dataset, model), rows in sorted(groups.items()):
            out = {"dataset": dataset, "model": model}
            for field in FIELDS:
                seed_values: dict[str, list[float]] = defaultdict(list)
                for r in rows:
                    seed_values[r["seed"]].append(r[field])
                low, high = bootstrap(seed_values, rng)
                out[f"{field}.estimate_mean_of_run_means"] = float(np.mean([r[field] for r in rows]))
                out[f"{field}.ci95_low"], out[f"{field}.ci95_high"] = low, high
            out["n_runs"], out["n_seeds"] = len(rows), len({r["seed"] for r in rows})
            summary.append(out)
    write_csv(OUT / "review2_permutation_summary.csv", summary, list(summary[0]))

    # --- 2. range of the stored LIME stability ----------------------------------
    values: dict[tuple, list[float]] = defaultdict(list)
    for row in instances:
        if row["lime_stability"] != "":
            values[(row["dataset"], row["model"])].append(float(row["lime_stability"]))
    by_model = [{"dataset": d, "model": m, "n_instances": len(v), "median_lime_stability": float(np.median(v))}
                for (d, m), v in sorted(values.items())]
    write_csv(OUT / "review2_lime_stability_by_model.csv", by_model, list(by_model[0]))
    ranges = []
    for dataset in sorted({r["dataset"] for r in by_model}):
        medians = [r["median_lime_stability"] for r in by_model if r["dataset"] == dataset]
        ranges.append({"dataset": dataset, "n_models": len(medians),
                       "min_model_median_lime_stability": min(medians),
                       "max_model_median_lime_stability": max(medians)})
    write_csv(OUT / "review2_lime_stability_range.csv", ranges, list(ranges[0]))

    # --- 3. weight of LIME's perturbed samples -----------------------------------
    explained: dict[tuple, set[int]] = defaultdict(set)
    for row in instances:
        explained[(row["dataset"], row["seed"])].add(int(row["instance_id"]))
    sums: dict[str, list[float]] = defaultdict(list)
    for (dataset, seed), ids in sorted(explained.items()):
        x_train, x_test, _, _ = split(dataset, seed)
        mean, scale = x_train.mean(axis=0), x_train.std(axis=0)
        scale[scale == 0] = 1.0
        for instance_id in sorted(ids):
            z = (x_test[instance_id] - mean) / scale
            samples = draw.normal(size=(LIME_SAMPLES, len(z)))
            distance2 = ((samples - z) ** 2).sum(axis=1)
            sums[dataset].append(float(np.sqrt(np.exp(-distance2 / KERNEL_WIDTH ** 2)).sum()))
    kernel = [{"dataset": d, "n_features": len(split(d, sorted(s for dd, s in explained if dd == d)[0])[3]),
               "n_instances": len(v), "kernel_width": KERNEL_WIDTH,
               "default_kernel_width": 0.75 * np.sqrt(len(split(d, sorted(s for dd, s in explained if dd == d)[0])[3])),
               "median_weight_of_perturbed_samples": float(np.median(v)),
               "q05_weight_of_perturbed_samples": float(np.quantile(v, 0.05)),
               "q95_weight_of_perturbed_samples": float(np.quantile(v, 0.95))}
              for d, v in sorted(sums.items())]
    write_csv(OUT / "review2_lime_kernel_weight.csv", kernel, list(kernel[0]))
    print(f"wrote {OUT.relative_to(ROOT)}/review2_*.csv")


if __name__ == "__main__":
    main()
