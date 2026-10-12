"""Paper F: the descriptive counts made after the results, on rows written by hand."""
import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("paper_f_posthoc_descriptives",
                                              SCRIPTS / "paper_f_posthoc_descriptives.py")
pd_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pd_mod)

D = 20                      # encoded features of the one dataset: m = ceil(0.2 * 20) = 4
USED = {"lime": 10, "shap": 20, "anchors": 2, "dice": 3}
COST = {"lime": [1, 1, 1, 1], "shap": [5, 5, 5, 5], "anchors": [10, 10, 10, 10],
        "dice": [2, 2, 2, 100]}          # DiCE: the lower median and the higher mean


def rows() -> tuple[pd.DataFrame, pd.DataFrame]:
    inst = []
    for e, used in USED.items():
        for i, cost in enumerate(COST[e]):
            inst.append({"dataset": "a", "model": "rf", "seed": 1, "explainer": e, "instance": i,
                         "failed": 0, "fail_reason": "", "n_used": used,
                         "sparsity": 1 - used / D, "cost_ms": cost})
    inst.append({"dataset": "a", "model": "rf", "seed": 1, "explainer": "dice", "instance": 9,
                 "failed": 1, "fail_reason": "time limit of 1200 s", "n_used": None,
                 "sparsity": None, "cost_ms": None})
    inst.append({"dataset": "a", "model": "rf", "seed": 1, "explainer": "dice", "instance": 10,
                 "failed": 1, "fail_reason": "Failure: no counterfactual", "n_used": None,
                 "sparsity": None, "cost_ms": None})
    inst = pd.DataFrame(inst)
    cells = (inst[inst["failed"] == 0].groupby(["dataset", "model", "explainer", "seed"])["cost_ms"]
             .mean().reset_index())
    return inst, cells


def value(out: pd.DataFrame, metric: str, key: str) -> float:
    return float(out[(out["metric"] == metric) & (out["key"] == key)]["value"].iloc[0])


def test_features_used_and_masked():
    out = pd_mod.describe(*rows())
    assert value(out, "features_used", "shap") == 20 and value(out, "features_used", "anchors") == 2
    assert value(out, "features_masked", "shap") == 4       # capped at m
    assert value(out, "features_masked", "lime") == 4
    assert value(out, "features_masked", "anchors") == 2     # fewer than m are named
    assert value(out, "features_masked", "dice") == 3
    assert value(out, "encoded_features", "min") == D == value(out, "encoded_features", "max")


def test_median_and_mean_cost_can_order_the_pair_differently():
    out = pd_mod.describe(*rows())
    assert value(out, "median_cost_faster", "dice") == 1 and value(out, "median_cost_faster", "anchors") == 0
    assert value(out, "mean_cost_faster", "anchors") == 1 and value(out, "mean_cost_faster", "dice") == 0


def test_failures_by_reason():
    out = pd_mod.describe(*rows())
    assert value(out, "failures_time_limit", "dice") == 1 and value(out, "failures_other", "dice") == 1
    assert value(out, "failures_time_limit", "lime") == 0


def test_a_changing_number_of_features_is_an_error():
    inst, cells = rows()
    inst.loc[0, "sparsity"] = 0.9                       # 10 named of 100: another d
    with pytest.raises(ValueError):
        pd_mod.describe(inst, cells)
