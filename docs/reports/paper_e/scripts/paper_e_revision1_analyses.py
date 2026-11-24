#!/usr/bin/env python3
"""Paper E analyses for AAIR revision 1 (decision of 2026-11-24). Re-cuts of the stored
explanations; no explainer is run. Post hoc (ANALYSIS_PLAN.md section 9, entry of 2026-11-24).

  1. heldout      R1-1, R2-2, R3-3  Adult: the primary agreement measures (top-5 and top-10
                                    Jaccard, Kendall tau-b) on held-out instances only, that
                                    is, instances that are not rows of the model's training
                                    data (seed-42 partition), beside the training instances
                                    and all instances.
  2. same_class   R2-4              Permutation reference restricted to the same predicted
                                    class: the SHAP list of an instance against the LIME list
                                    of another instance of the same run AND the same predicted
                                    class (DRAWS draws). Beside it, the unrestricted reference
                                    recomputed with the same draws, for a like-for-like
                                    comparison.
  3. loso         R2-5              Leave one seed out: the mean of run means of the primary
                                    measures with each seed left out in turn; smallest and
                                    largest value over the seeds left out.

Aggregation is the plan's section 5: run means, mean of run means, seed-clustered percentile
bootstrap (2000 resamples, seed 20261003).

Writes outputs/analysis/paper_e/posthoc/rev1_*.csv

    .venv/Scripts/python.exe docs/reports/paper_e/scripts/paper_e_revision1_analyses.py
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

MEASURES = ("top5_jaccard", "top10_jaccard", "kendall_tau_b")
DRAWS = 20
PERMUTATION_SEED = 20261124
MIN_INSTANCES = 10   # a run enters a held-out or training cell only with at least 10 instances


def summarise(run_rows: list[dict], fields: tuple[str, ...], keys: tuple[str, ...], rng) -> list[dict]:
    """Mean of run means and seed-clustered interval, per model and over models."""
    out = []
    for scope in ("model", "all"):
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for r in run_rows:
            groups[(r["dataset"], r["model"] if scope == "model" else "all")
                   + tuple(r[k] for k in keys)].append(r)
        for group, rows in sorted(groups.items()):
            row = {"dataset": group[0], "model": group[1], **dict(zip(keys, group[2:]))}
            for field in fields:
                seeds: dict[str, list[float]] = defaultdict(list)
                for r in rows:
                    if r[field] != "":
                        seeds[r["seed"]].append(float(r[field]))
                values = [v for vs in seeds.values() for v in vs]
                low, high = bootstrap(seeds, rng) if values else ("", "")
                row[f"{field}.estimate_mean_of_run_means"] = float(np.mean(values)) if values else ""
                row[f"{field}.ci95_low"], row[f"{field}.ci95_high"] = low, high
            row["n_runs"] = len([r for r in rows if r[fields[0]] != ""])
            row["n_seeds"] = len({r["seed"] for r in rows if r[fields[0]] != ""})
            row["n_instances"] = int(sum(int(r.get("n_instances", 0) or 0) for r in rows))
            out.append(row)
    return out


def run_mean(rows: list[dict], measure: str) -> float | str:
    values = [float(r[measure]) for r in rows if r[measure] not in ("", "nan", "None")]
    return float(np.mean(values)) if len(values) >= 1 else ""


def main() -> None:
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    draw = np.random.default_rng(PERMUTATION_SEED)
    with (ANALYSIS / "instance_agreement.csv").open(encoding="utf-8") as fh:
        instances = list(csv.DictReader(fh))
    blocks: dict[tuple, list[dict]] = defaultdict(list)
    for row in instances:
        blocks[(row["dataset"], row["model"], row["seed"], row["intensity"])].append(row)

    # --- 1. held-out instances (Adult) ------------------------------------------------
    adult_train_rows = {r.tobytes() for r in np.ascontiguousarray(split("exp2_adult", "42")[0])}
    held_runs = []
    for block in sorted(b for b in blocks if b[0] == "exp2_adult"):
        dataset, model, seed, intensity = block
        x_test = split(dataset, seed)[1]
        part = {"train": [], "heldout": []}
        for r in blocks[block]:
            x = np.ascontiguousarray(x_test[int(r["instance_id"])])
            part["train" if x.tobytes() in adult_train_rows else "heldout"].append(r)
        part["all"] = blocks[block]
        for subset, rows in part.items():
            entry = {"dataset": dataset, "model": model, "seed": seed, "intensity": intensity,
                     "subset": subset, "n_instances": len(rows)}
            for m in MEASURES:
                entry[m] = run_mean(rows, m) if len(rows) >= MIN_INSTANCES else ""
            held_runs.append(entry)
    write_csv(OUT / "rev1_heldout_runs.csv", held_runs, list(held_runs[0]))
    held = summarise(held_runs, MEASURES, ("subset",), rng)
    write_csv(OUT / "rev1_heldout_summary.csv", held, list(held[0]))

    # --- 2. same-predicted-class permutation reference --------------------------------
    perm_runs = []
    for block in sorted(blocks):
        dataset, model, seed, intensity = block
        stored = {m: {str(e["instance_id"]): e["explanation"]["raw_top"] for e in json.loads(
            run_path(dataset, model, seed, intensity, m).read_text(encoding="utf-8"))["instance_evaluations"]
            if e.get("explanation")} for m in ("shap", "lime")}
        rows = sorted(blocks[block], key=lambda r: int(r["instance_id"]))
        ids = [r["instance_id"] for r in rows]
        by_class: dict[str, list[int]] = defaultdict(list)
        for k, r in enumerate(rows):
            by_class[r["prediction"]].append(k)
        other, same = [], []
        for k, r in enumerate(rows):
            shap = stored["shap"][ids[k]]
            for _ in range(DRAWS):
                j = int(draw.integers(len(ids) - 1))
                j += j >= k
                other.append(primary_agreement(shap, stored["lime"][ids[j]])["top5_jaccard"])
            pool = [j for j in by_class[r["prediction"]] if j != k]
            if pool:
                for j in draw.choice(pool, size=DRAWS):
                    same.append(primary_agreement(shap, stored["lime"][ids[int(j)]])["top5_jaccard"])
        paired = float(np.mean([float(r["top5_jaccard"]) for r in rows]))
        perm_runs.append({"dataset": dataset, "model": model, "seed": seed, "intensity": intensity,
                          "n_instances": len(rows), "paired_top5_jaccard": paired,
                          "other_any_class_top5_jaccard": float(np.mean(other)),
                          "other_same_class_top5_jaccard": float(np.mean(same)),
                          "specific_vs_any_class": paired - float(np.mean(other)),
                          "specific_vs_same_class": paired - float(np.mean(same))})
    fields = ("paired_top5_jaccard", "other_any_class_top5_jaccard", "other_same_class_top5_jaccard",
              "specific_vs_any_class", "specific_vs_same_class")
    write_csv(OUT / "rev1_same_class_permutation_runs.csv", perm_runs, list(perm_runs[0]))
    perm = summarise(perm_runs, fields, (), rng)
    write_csv(OUT / "rev1_same_class_permutation_summary.csv", perm, list(perm[0]))

    # --- 3. leave one seed out ---------------------------------------------------------
    run_means = []
    for block, rows in sorted(blocks.items()):
        run_means.append({"dataset": block[0], "model": block[1], "seed": block[2],
                          **{m: run_mean(rows, m) for m in MEASURES}})
    loso = []
    for scope in ("model", "all"):
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for r in run_means:
            groups[(r["dataset"], r["model"] if scope == "model" else "all")].append(r)
        for (dataset, model), rows in sorted(groups.items()):
            seeds = sorted({r["seed"] for r in rows})
            out = {"dataset": dataset, "model": model, "n_seeds": len(seeds)}
            for m in MEASURES:
                full = [float(r[m]) for r in rows if r[m] != ""]
                left = [float(np.mean([float(r[m]) for r in rows if r["seed"] != s and r[m] != ""]))
                        for s in seeds if len(seeds) > 1]
                out[f"{m}.all_seeds"] = float(np.mean(full))
                out[f"{m}.loso_min"], out[f"{m}.loso_max"] = (min(left), max(left)) if left else ("", "")
            loso.append(out)
    write_csv(OUT / "rev1_leave_one_seed_out.csv", loso, list(loso[0]))

    manifest = OUT / "manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {}
    data["revision1_2026-11-24"] = {
        "script": "docs/reports/paper_e/scripts/paper_e_revision1_analyses.py",
        "outputs": ["rev1_heldout_runs.csv", "rev1_heldout_summary.csv",
                    "rev1_same_class_permutation_runs.csv", "rev1_same_class_permutation_summary.csv",
                    "rev1_leave_one_seed_out.csv"],
        "bootstrap_seed": BOOTSTRAP_SEED, "permutation_seed": PERMUTATION_SEED, "draws": DRAWS,
        "min_instances_per_cell": MIN_INSTANCES}
    manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
