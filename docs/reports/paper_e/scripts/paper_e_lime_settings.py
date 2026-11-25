#!/usr/bin/env python3
"""Paper E, AAIR revision 1 (reviewers 2 and 3; author decision D-1 of 2026-11-24):
how much do the reported SHAP-LIME agreement levels depend on the LIME configuration?

Post hoc (ANALYSIS_PLAN.md section 9, second entry of 2026-11-24). On the instances of the
self-agreement experiment (outputs/analysis/paper_e/posthoc/ceiling_lists.json: same
instances, same model binaries, same two SHAP repetitions), LIME is run again under each
setting below, twice (random states 1001 and 2002, as in that experiment):

    w3_1k          kernel width 3, no discretisation, 1,000 samples: the configuration of the
                   study. Not re-run: the lists lime_a / lime_b of ceiling_lists.json.
    w3_5k          kernel width 3, no discretisation, 5,000 samples
    w3_10k         kernel width 3, no discretisation, 10,000 samples
    wd_5k          default width (0.75 * sqrt(d)), no discretisation, 5,000 samples
    package        the package defaults: default width, quartile discretisation, 5,000 samples

Every other setting is that of the study (ten features, the repository wrapper). For each
setting: LIME self-agreement (repetition a vs b), SHAP-LIME agreement (mean of the four pairs
of a SHAP and a LIME repetition), and agreement with the stored LIME list of the study.
Measures: scripts/analyze_paper_e.py::primary_agreement. Aggregation: run means, mean of run
means, seed-clustered percentile bootstrap (2000 resamples, seed 20261003).

German Credit and Breast Cancer need the EXP3 binaries (not tracked):
    python scripts/train_exp3_models.py --model-root <dir> --data-cache-dir data

Writes outputs/analysis/paper_e/posthoc/
    lime_settings_lists.json     top-10 lists of every setting and repetition, per instance
    lime_settings_runs.csv       run means
    lime_settings_summary.csv    group estimates
    lime_settings_timing.csv     seconds per run and setting

    .venv/Scripts/python.exe docs/reports/paper_e/scripts/paper_e_lime_settings.py --exp3-model-root <dir>
        [--only exp2_adult:rf] [--limit 5] [--settings w3_10k] [--summarise-only]
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
import warnings
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_paper_e import primary_agreement  # noqa: E402
from paper_e_ceiling import RANDOM_STATES, load_model, top10  # noqa: E402
from paper_e_posthoc import BOOTSTRAP_SEED, OUT, bootstrap, write_csv  # noqa: E402
from paper_e_sign_contribution import split  # noqa: E402

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

SETTINGS = {   # name: (kernel_width, discretize_continuous, num_samples)
    "w3_5k": (3.0, False, 5000),
    "w3_10k": (3.0, False, 10000),
    "wd_5k": (None, False, 5000),
    "package": (None, True, 5000),
}
ALL = ("w3_1k",) + tuple(SETTINGS)
METRICS = ("top5_jaccard", "top10_jaccard", "kendall_tau_b")
LISTS = OUT / "lime_settings_lists.json"


def lists_of(entry: dict, setting: str) -> tuple[dict, dict]:
    if setting == "w3_1k":
        return entry["lime_a"], entry["lime_b"]
    return entry["settings"][setting]["a"], entry["settings"][setting]["b"]


def measures(entry: dict, setting: str) -> dict[str, float | str]:
    a, b = lists_of(entry, setting)
    out: dict[str, float | str] = {}
    pairs = {"self": [(a, b)],
             "shap_lime": [(s, l) for s in (entry["shap_a"], entry["shap_b"]) for l in (a, b)],
             "vs_study": [(a, entry["stored_lime"]), (b, entry["stored_lime"])]}
    for name, items in pairs.items():
        for metric in METRICS:
            values = [r[metric] for r in (primary_agreement(x, y) for x, y in items) if r[metric] is not None]
            out[f"{setting}.{name}.{metric}"] = float(np.mean(values)) if values else ""
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp3-model-root", type=Path)
    ap.add_argument("--only", nargs="*", help="dataset:model pairs")
    ap.add_argument("--settings", nargs="*", choices=list(SETTINGS), default=list(SETTINGS))
    ap.add_argument("--limit", type=int, help="instances per run (timing pilot; nothing is saved)")
    ap.add_argument("--summarise-only", action="store_true")
    args = ap.parse_args()
    from src.xai.lime_tabular import LIMETabularWrapper

    base = json.loads((OUT / "ceiling_lists.json").read_text(encoding="utf-8"))
    done = {}
    if LISTS.exists():
        done = {(e["dataset"], e["model"], e["seed"], e["instance_id"]): e
                for e in json.loads(LISTS.read_text(encoding="utf-8"))}
    entries = [done.get((e["dataset"], e["model"], e["seed"], e["instance_id"]), {**e, "settings": {}})
               for e in base]
    if args.summarise_only:
        summarise(entries)
        return

    by_run: dict[tuple, list[dict]] = defaultdict(list)
    for e in entries:
        by_run[(e["dataset"], e["model"], e["seed"])].append(e)
    timing = []
    timing_path = OUT / "lime_settings_timing.csv"
    if timing_path.exists() and not args.limit:
        with timing_path.open(encoding="utf-8") as fh:
            timing = list(csv.DictReader(fh))
    for (dataset, model, seed), items in sorted(by_run.items()):
        if args.only and f"{dataset}:{model}" not in args.only:
            continue
        if dataset != "exp2_adult" and args.exp3_model_root is None:
            continue
        x_train, x_test, _, names = split(dataset, seed)
        clf = load_model(dataset, model, seed, args.exp3_model_root)
        work = items[:args.limit] if args.limit else items
        for setting in args.settings:
            todo = [e for e in work if setting not in e["settings"]]
            if not todo:
                continue
            width, discretize, samples = SETTINGS[setting]
            wrappers = [LIMETabularWrapper(training_data=x_train, feature_names=names, num_features=10,
                                           num_samples=samples, kernel_width=width,
                                           discretize_continuous=discretize, random_state=state)
                        for state in RANDOM_STATES]
            started = time.time()
            for e in todo:
                x = x_test[int(e["instance_id"])]
                if int(clf.predict(x.reshape(1, -1))[0]) != int(float(e["prediction"])):
                    sys.exit(f"{dataset} {model} {seed} {e['instance_id']}: stored prediction not reproduced")
                a, b = (top10(w.explain_instance(clf, x, return_full=False), names) for w in wrappers)
                e["settings"][setting] = {"a": a, "b": b}
            seconds = time.time() - started
            row = {"dataset": dataset, "model": model, "seed": seed, "setting": setting,
                   "n_instances": len(todo), "seconds": round(seconds, 1),
                   "seconds_per_instance": round(seconds / len(todo), 3)}
            print(row, flush=True)
            if args.limit:
                continue
            timing.append(row)
            LISTS.write_text(json.dumps(entries, indent=0), encoding="utf-8", newline="\n")
            write_csv(timing_path, timing, list(row))
    if not args.limit:
        summarise(entries)


def summarise(entries: list[dict]) -> None:
    complete = [e for e in entries if all(s in e["settings"] for s in SETTINGS)]
    if not complete:
        print("no instance has every setting yet")
        return
    rows = []
    for e in complete:
        out = {k: e[k] for k in ("dataset", "model", "seed", "instance_id")}
        for setting in ALL:
            out.update(measures(e, setting))
        rows.append(out)
    fields = [k for k in rows[0] if "." in k]
    by_run: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        by_run[(r["dataset"], r["model"], r["seed"])].append(r)
    run_rows = []
    for (dataset, model, seed), items in sorted(by_run.items()):
        out = {"dataset": dataset, "model": model, "seed": seed, "n_instances": len(items)}
        for f in fields:
            values = [float(r[f]) for r in items if r[f] != ""]
            out[f] = float(np.mean(values)) if values else ""
        run_rows.append(out)
    write_csv(OUT / "lime_settings_runs.csv", run_rows, list(run_rows[0]))

    rng = np.random.default_rng(BOOTSTRAP_SEED)
    summary = []
    for scope in ("model", "all"):
        groups: dict[tuple, list[dict]] = defaultdict(list)
        for r in run_rows:
            groups[(r["dataset"], r["model"] if scope == "model" else "all")].append(r)
        for (dataset, model), items in sorted(groups.items()):
            for f in fields:
                setting, pair, metric = f.split(".")
                seeds: dict[str, list[float]] = defaultdict(list)
                for r in items:
                    if r[f] != "":
                        seeds[r["seed"]].append(r[f])
                values = [v for vs in seeds.values() for v in vs]
                if not values:
                    continue
                low, high = bootstrap(seeds, rng)
                summary.append({"dataset": dataset, "model": model, "setting": setting, "pair": pair,
                                "metric": metric, "estimate_mean_of_run_means": float(np.mean(values)),
                                "ci95_low": low, "ci95_high": high, "n_runs": len(values),
                                "n_seeds": len(seeds), "n_instances": sum(int(r["n_instances"]) for r in items)})
    write_csv(OUT / "lime_settings_summary.csv", summary, list(summary[0]))
    print(f"summarised {len(complete)} instances into lime_settings_*.csv")


if __name__ == "__main__":
    main()
