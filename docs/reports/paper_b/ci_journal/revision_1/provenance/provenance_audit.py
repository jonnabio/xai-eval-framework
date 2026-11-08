"""Scratch audit of the EXP2 cohort (all 300 runs):
- per run: date, cost floor (min cost >= 990 ms => guard artifact suspected),
  share of its instance set reproduced by today's model for that cell;
- per cell: whether SHAP and LIME (and Anchors, DiCE) saw the same instance set.
Writes a CSV next to this script and prints a summary."""
import collections
import csv
import glob
import json
import logging
import sys
import tempfile
import traceback
from pathlib import Path

logging.disable(logging.WARNING)
REPO = Path(sys.argv[1])
OUT = Path(sys.argv[2])
sys.path.insert(0, str(REPO))
from src.experiment.config import load_config  # noqa: E402
from src.experiment.runner import ExperimentRunner  # noqa: E402

runs = {}
for f in glob.glob(str(REPO / "experiments/exp2_scaled/results/*/*/*/results.json")):
    p = Path(f)
    try:
        d = json.load(open(f))
    except Exception:
        continue
    model, expl = p.parts[-4].split("_", 1)
    seed = int(p.parts[-3].split("_")[1])
    n = int(p.parts[-2].split("_")[1])
    ev = d.get("instance_evaluations") or []
    cost = d.get("aggregated_metrics", {}).get("cost", {}) or {}
    runs[(model, expl, seed, n)] = {
        "date": d["experiment_metadata"]["timestamp"][:10],
        "ids": {(e["quadrant"], int(e["instance_id"])) for e in ev if "quadrant" in e},
        "cost_min": cost.get("min"),
        "cost_median_proxy": cost.get("mean"),
    }

today = {}
errors = {}
for model in ("logreg", "mlp", "rf", "svm", "xgb"):
    for seed in (42, 123, 456, 789, 999):
        for n in (50, 100, 200):
            cfgp = REPO / f"configs/experiments/exp2_scaled/{model}_lime_s{seed}_n{n}.yaml"
            try:
                cfg = load_config(cfgp)
                cfg.output_dir = Path(tempfile.mkdtemp())
                r = ExperimentRunner(cfg)
                r.setup()
                inst = r.generate_instances()
                today[(model, seed, n)] = {(q, int(i)) for q, i in
                                           zip(inst["quadrant"], inst["original_index"])}
            except Exception as exc:
                errors[(model, seed, n)] = f"{type(exc).__name__}: {exc}"
                traceback.print_exc(limit=1)

with open(OUT, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["model", "explainer", "seed", "n", "date", "n_instances", "share_today",
                "cost_min_ms", "guard_floor_suspected"])
    for (model, expl, seed, n), r in sorted(runs.items()):
        t = today.get((model, seed, n))
        share = (len(r["ids"] & t) / len(r["ids"])) if (t and r["ids"]) else None
        cm = r["cost_min"]
        w.writerow([model, expl, seed, n, r["date"], len(r["ids"]),
                    None if share is None else round(share, 4), cm,
                    None if cm is None else cm >= 990])

print("errors building today's instance sets:", {k: v[:80] for k, v in errors.items()} or "none")
print("== share of each run's instances reproduced by today's model (by model, by month)")
agg = collections.defaultdict(list)
for (model, expl, seed, n), r in runs.items():
    t = today.get((model, seed, n))
    if t and r["ids"]:
        agg[(model, r["date"][:7])].append(len(r["ids"] & t) / len(r["ids"]))
for k in sorted(agg):
    v = agg[k]
    print(f"{k[0]:6} {k[1]}: runs {len(v):3}  identical {sum(x == 1 for x in v):3}  "
          f"median share {sorted(v)[len(v)//2]:.3f}")

print("== SHAP vs LIME instance sets per cell")
same = diff = 0
diffs = []
for model in ("logreg", "mlp", "rf", "svm", "xgb"):
    for seed in (42, 123, 456, 789, 999):
        for n in (50, 100, 200):
            a, b = runs.get((model, "shap", seed, n)), runs.get((model, "lime", seed, n))
            if not a or not b or not a["ids"] or not b["ids"]:
                continue
            if a["ids"] == b["ids"]:
                same += 1
            else:
                diff += 1
                diffs.append(f"{model} s{seed} n{n}: shared {len(a['ids'] & b['ids'])}/"
                             f"{len(b['ids'])} (shap {a['date']}, lime {b['date']})")
print(f"identical {same}, different {diff}")
for line in diffs:
    print("  ", line)

print("== guard floor (min cost >= 990 ms) among SHAP/LIME runs, by month")
gf = collections.Counter()
tot = collections.Counter()
for (model, expl, seed, n), r in runs.items():
    if expl in ("shap", "lime") and r["cost_min"] is not None:
        tot[(expl, r["date"][:7])] += 1
        gf[(expl, r["date"][:7])] += r["cost_min"] >= 990
for k in sorted(tot):
    print(f"{k[0]:5} {k[1]}: {gf[k]} of {tot[k]}")
