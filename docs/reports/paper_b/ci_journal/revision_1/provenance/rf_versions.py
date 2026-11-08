"""Scratch: which historical rf.joblib reproduces the Jan-Feb EXP2 RF instance sets,
and how the forest sizes compare. Blobs are extracted with `git show` into a temp dir."""
import json
import logging
import subprocess
import sys
import tempfile
from pathlib import Path

import joblib
import numpy as np

logging.disable(logging.WARNING)
REPO = Path(sys.argv[1])
sys.path.insert(0, str(REPO))
from src.experiment.config import load_config  # noqa: E402
from src.experiment.runner import ExperimentRunner  # noqa: E402

path = "experiments/exp1_adult/models/rf.joblib"
log = subprocess.run(["git", "log", "--format=%h %ad", "--date=short", "--", path], cwd=REPO,
                     capture_output=True, text=True).stdout.split("\n")
commits = [l.split() for l in log if l.strip()]
jan = json.load(open(REPO / "experiments/exp2_scaled/results/rf_lime/seed_123/n_50/results.json"))
jan_ids = {(e["quadrant"], int(e["instance_id"])) for e in jan["instance_evaluations"] if "quadrant" in e}

tmp = Path(tempfile.mkdtemp())
cfg = load_config(REPO / "configs/experiments/exp2_scaled/rf_lime_s123_n50.yaml")
cfg.output_dir = Path(tempfile.mkdtemp())
runner = ExperimentRunner(cfg)
runner.setup()  # loads data with today's preprocessor; model swapped below
seen = {}
for c, date in commits:
    blob = subprocess.run(["git", "rev-parse", f"{c}:{path}"], cwd=REPO, capture_output=True,
                          text=True).stdout.strip()
    if not blob or blob in seen:
        print(f"{c} {date}: blob {blob[:9]} (seen)")
        continue
    f = tmp / f"{blob}.joblib"
    f.write_bytes(subprocess.run(["git", "show", f"{c}:{path}"], cwd=REPO,
                                 capture_output=True).stdout)
    try:
        m = joblib.load(f)
        m = getattr(m, "model", m)
        runner.model = m
        inst = runner.generate_instances()
        ids = {(q, int(i)) for q, i in zip(inst["quadrant"], inst["original_index"])}
        leaves = int(sum(e.tree_.n_leaves for e in m.estimators_))
        depth = max(e.tree_.max_depth for e in m.estimators_)
        info = (f"n_estimators={m.n_estimators} max_depth_param={m.max_depth} "
                f"realized_max_depth={depth} total_leaves={leaves}")
        seen[blob] = True
        print(f"{c} {date}: blob {blob[:9]} reproduces Jan run: {ids == jan_ids} "
              f"(shared {len(ids & jan_ids)}/{len(jan_ids)}); {info}")
    except Exception as exc:
        print(f"{c} {date}: blob {blob[:9]} load/sample failed: {type(exc).__name__}: {exc}")
