"""Paper F: the counts and the audit asked for by the Codex review, on rows written by hand."""
import importlib.util
import os
import sys
import time
from pathlib import Path

import pandas as pd

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("paper_f_posthoc_protocol",
                                              SCRIPTS / "paper_f_posthoc_protocol.py")
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)

D = 20          # m = ceil(0.2 * 20) = 4


def rows() -> tuple[pd.DataFrame, pd.DataFrame]:
    inst = []
    used = {"lime": [10] * 4, "shap": [20] * 4, "anchors": [2, 3, 5, 7], "dice": [3] * 4}
    cost = {"lime": [1] * 4, "shap": [4] * 4, "anchors": [10] * 4, "dice": [8] * 4}
    for e in pp.METHODS:
        for i in range(4):
            inst.append({"dataset": "a", "model": "rf", "seed": 1, "explainer": e, "instance": i,
                         "failed": 0, "n_used": used[e][i], "sparsity": 1 - used[e][i] / D,
                         "cost_ms": cost[e][i], "total_s": 2.0})
    inst = pd.DataFrame(inst)
    cells = pd.DataFrame([
        {"dataset": "a", "model": "rf", "explainer": e, "seed": 1, "gap": g, "stability": s,
         "sparsity": p, "cost_ms": c}
        for e, g, s, p, c in (("lime", 0.20, 0.6, 0.5, 1.0), ("shap", 0.30, 0.8, 0.0, 4.0),
                              ("anchors", 0.12, 0.5, 0.8, 10.0), ("dice", 0.10, 0.2, 0.85, 40.0))])
    return inst, cells


def value(out: pd.DataFrame, metric: str, key: str) -> float:
    return float(out[(out["metric"] == metric) & (out["key"] == key)]["value"].iloc[0])


def test_anchors_rules_over_the_budgets():
    out = pp.counts(*rows())
    assert value(out, "anchors_over_budget", "mask") == 0.5     # 5 and 7 are above m = 4
    assert value(out, "anchors_over_budget", "top5") == 0.25    # only 7 is above 5


def test_cost_of_successes_and_planned_cost_can_differ():
    out = pp.counts(*rows())
    assert value(out, "mean_success_cost_faster", "dice") == 1  # 8 ms against 10 ms
    assert round(value(out, "cost_ratio_median", "anchors-dice"), 6) == 4.0   # planned: 40 / 10
    assert round(value(out, "cost_ratio_median", "range"), 6) == 40.0


def test_differences_between_pairs():
    out = pp.counts(*rows())
    assert round(value(out, "absdiff_median", "gap_anchors-dice"), 6) == 0.02
    assert round(value(out, "range_median", "gap"), 6) == 0.20
    assert round(value(out, "absdiff_median", "sparsity_anchors-dice"), 6) == 0.05


def test_a_job_with_a_long_pause_is_flagged(tmp_path):
    inst, _ = rows()
    now = time.time()
    for e, pause in (("lime", 0.0), ("dice", 4000.0)):
        folder = tmp_path / "a" / "rf" / "seed_1"
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{e}.jsonl"
        path.write_text("{}\n", encoding="utf-8")
        os.utime(path, (now + pause, now + pause))           # the last write, later
    table = pp.audit(tmp_path, inst).set_index("explainer")
    assert table.loc["lime", "flagged"] == 0
    assert table.loc["dice", "flagged"] == 1
