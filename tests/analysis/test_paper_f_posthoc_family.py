"""Paper F: the check with the software-defect family counted once, on synthetic rows."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("paper_f_posthoc_family",
                                              SCRIPTS / "paper_f_posthoc_family.py")
ph = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ph)
an = ph.an


def cells(n_others: int = 6, seed: int = 0) -> pd.DataFrame:
    """Run means with one order of the methods in every dataset, the family included."""
    rng = np.random.default_rng(seed)
    rows = []
    for dataset in [*ph.FAMILY, "adult", *[f"d{i}" for i in range(n_others - 1)]]:
        for model in ("logreg", "rf"):
            for s in (1, 2, 3):
                for e, name in enumerate(an.EXPL):
                    v = e + rng.normal(0, 0.2)
                    rows.append({"dataset": dataset, "model": model, "explainer": name, "seed": s,
                                 "gap": v, "stability": v, "sparsity": v, "cost_ms": -v})
    return pd.DataFrame(rows)


@pytest.fixture(autouse=True)
def small(monkeypatch):
    monkeypatch.setattr(an, "N_BOOT", 200)
    monkeypatch.setattr(an, "N_PERM", 1000)


def test_one_row_per_kept_dataset_and_measure_on_the_reduced_set():
    out = ph.family_once(cells())
    assert len(out) == len(ph.FAMILY) * len(an.MEASURES)
    assert set(out["kept"]) == set(ph.FAMILY)
    assert (out["datasets"] == 6 + 1).all()          # the six others and one of the family


def test_a_shared_order_stays_shared():
    out = ph.family_once(cells())
    assert (out["mean_rank_corr"] > 0.9).all() and (out["p_holm"] < 0.05).all()


def test_the_order_of_the_runs_does_not_change_a_number():
    a = ph.family_once(cells())
    b = ph.family_once(cells())
    pd.testing.assert_frame_equal(a, b)


def test_a_missing_family_dataset_is_an_error():
    data = cells()
    with pytest.raises(ValueError):
        ph.family_once(data[data["dataset"] != "kc1"])
