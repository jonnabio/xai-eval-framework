"""Paper F: the order of the methods by the type of features, on synthetic ranks."""
import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("paper_f_posthoc_type",
                                              SCRIPTS / "paper_f_posthoc_type.py")
ph = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ph)

SAME = {"lime": 2.0, "shap": 1.0, "anchors": 3.0, "dice": 4.0}
SWAP = {"lime": 3.0, "shap": 1.0, "anchors": 2.0, "dice": 4.0}


def frames(mixed_order=SWAP):
    data = pd.DataFrame({"key": ["n1", "n2", "m1", "m2", "c1"],
                         "stratum": ["numeric-small", "numeric-large", "mixed-small",
                                     "mixed-large", "categorical-large"]})
    rows = []
    for m in ph.MEASURES:
        for d in ("n1", "n2", "c1"):
            rows.append({"dataset": d, "measure": m, **SAME})
        for d in ("m1", "m2"):
            rows.append({"dataset": d, "measure": m, **mixed_order})
    return pd.DataFrame(rows), data


def value(out, metric, key):
    return out.set_index(["metric", "key"]).loc[(metric, key), "value"]


def test_counts_by_type():
    out = ph.describe(*frames())
    assert value(out, "datasets", "numeric") == 2
    assert value(out, "shap_first_gap", "mixed") == 2
    assert value(out, "lime_above_anchors_stability", "numeric") == 2
    assert value(out, "lime_above_anchors_stability", "mixed") == 0
    assert value(out, "modal_order_sparsity", "mixed") == 2


def test_agreement_inside_and_between_types():
    out = ph.describe(*frames())
    assert value(out, "within", "numeric_gap") == pytest.approx(1.0)
    assert value(out, "between_types", "gap") == pytest.approx(0.8)  # one swap of adjacent ranks
    same = ph.describe(*frames(SAME))
    assert value(same, "between_types", "gap") == pytest.approx(1.0)


def test_a_dataset_without_stratum_stops():
    ranks, data = frames()
    with pytest.raises(ValueError):
        ph.describe(ranks, data[data["key"] != "m1"])
