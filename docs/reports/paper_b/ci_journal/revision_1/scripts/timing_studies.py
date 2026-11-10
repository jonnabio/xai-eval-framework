"""Paper B rev. 1: timing of the configuration sweep and of the matched tree-ensemble run.

    python timing_studies.py <sweep results/timing> <matched results/timing> <out dir>

Per instance, the median of its three repeats; per model and configuration, the median over
instances (all seeds). Writes sweep_timing.csv and matched_timing.csv.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def load(root):
    rows = []
    for f in Path(root).rglob("timing.jsonl"):
        model, seed = f.parts[-3], int(f.parts[-2].split("_")[1])
        for line in f.read_text().splitlines():
            r = json.loads(line)
            reps = [x for x in r.get("reps", []) if not x.get("error")]
            if not reps:
                continue
            rows.append(dict(model=model, seed=seed, config=r["explainer"], instance_id=r["instance_id"],
                             wall_ms=float(np.median([x["wall_ms"] for x in reps])),
                             cpu_ms=float(np.median([x["cpu_ms"] for x in reps])),
                             rows=float(np.median([x["rows"] for x in reps]))))
    return pd.DataFrame(rows)


sweep, matched, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
for name, root in (("sweep", sweep), ("matched", matched)):
    d = load(root)
    t = d.groupby(["model", "config"]).agg(wall_ms=("wall_ms", "median"), cpu_ms=("cpu_ms", "median"),
                                           rows=("rows", "median"), n=("wall_ms", "size")).reset_index()
    t.to_csv(out / f"{name}_timing.csv", index=False)
    print(f"== {name}: {len(d)} instance timings")
    print(t.pivot(index="config", columns="model", values="wall_ms").round(1).to_string())
    if name == "matched":
        # per seed: SHAP / LIME ratio, to show the spread
        p = d.groupby(["model", "seed", "config"]).wall_ms.median().unstack("config")
        p["ratio"] = p["shap"] / p["lime_full"]
        print(p.round(2).to_string())
