"""Paper F: the analysis on synthetic rows (scripts/paper_f_analyze.py)."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("paper_f_analyze", SCRIPTS / "paper_f_analyze.py")
an = importlib.util.module_from_spec(spec)
spec.loader.exec_module(an)

EXPL = an.EXPL


def synthetic(shared: bool, n_datasets: int = 8, seed: int = 0) -> pd.DataFrame:
    """Rows where the explainer order is the same in every dataset, or random in each."""
    rng = np.random.default_rng(seed)
    rows = []
    for d in range(n_datasets):
        level = np.arange(4.0) if shared else rng.permutation(4).astype(float)
        for model in ("logreg", "rf"):
            for s in (1, 2, 3):
                for e, name in enumerate(EXPL):
                    for i in range(6):
                        v = level[e] + rng.normal(0, 0.3)
                        rows.append({"dataset": "adult" if d == 0 else f"d{d}", "model": model,
                                     "seed": s, "explainer": name, "instance": i, "failed": 0,
                                     "gap": v, "stability": v, "sparsity": v, "cost_ms": -v})
    return pd.DataFrame(rows)


@pytest.fixture(autouse=True)
def small(monkeypatch):
    monkeypatch.setattr(an, "N_BOOT", 300)
    monkeypatch.setattr(an, "N_PERM", 2000)
    monkeypatch.setattr(an, "N_PERM_VAR", 100)


def test_mean_corr_equals_the_mean_of_pairwise_spearman():
    ranks = np.array([[1, 2, 3, 4], [1, 2, 4, 3], [4, 3, 2, 1.0]])
    z = an.standardise(ranks)
    pair = [np.corrcoef(ranks[i], ranks[j])[0, 1] for i, j in ((0, 1), (0, 2), (1, 2))]
    assert an.mean_corr(z) == pytest.approx(np.mean(pair))
    assert an.mean_corr(an.standardise(np.tile([1, 2, 3, 4.0], (5, 1)))) == pytest.approx(1.0)


def test_holm_is_monotone_and_bounded():
    assert an.holm([0.01, 0.04, 0.03, 0.5]) == pytest.approx([0.04, 0.09, 0.09, 0.5])


def test_shared_order_is_detected():
    cells = an.cell_means(an.impute_failures(synthetic(shared=True)))
    table, ranks = an.primary(cells, np.random.default_rng(1))
    assert (table["mean_rank_corr"] > 0.95).all() and (table["p_holm"] < 0.05).all()
    assert (table["decision"] == "the order generalises").all()
    pairs = an.pairs_vs_adult(ranks)
    assert (pairs["share"] == 1.0).all() and len(pairs) == 4 * 6


def test_unrelated_orders_are_not_called_shared():
    cells = an.cell_means(an.impute_failures(synthetic(shared=False, n_datasets=10, seed=3)))
    table, _ = an.primary(cells, np.random.default_rng(1))
    assert (table["mean_rank_corr"].abs() < 0.5).all()
    assert (table["decision"] != "the order generalises").all()


def test_failures_take_the_worst_value():
    df = synthetic(shared=True, n_datasets=2)
    df.loc[0, "failed"] = 1
    df.loc[0, ["gap", "stability", "sparsity", "cost_ms"]] = np.nan
    out = an.impute_failures(df)
    same = df[(df["dataset"] == df.loc[0, "dataset"]) & (df["model"] == df.loc[0, "model"])
              & (df["failed"] == 0)]
    assert out.loc[0, "gap"] == same["gap"].min()
    assert out.loc[0, "cost_ms"] == same["cost_ms"].max()


def test_variance_shares_sum_to_one_and_find_the_interaction():
    shared = an.variance(an.cell_means(synthetic(shared=True)), np.random.default_rng(2))
    part = shared[(shared["measure"] == "gap") & (shared["analysis"] == "mixed model (balanced)")]
    assert part["share"].sum() == pytest.approx(1.0)
    assert part.set_index("term").loc["explainer", "share"] > 0.9
    mixed = an.variance(an.cell_means(synthetic(shared=False)), np.random.default_rng(2))
    row = mixed[(mixed["measure"] == "gap") & (mixed["term"] == "explainer x dataset")
                & (mixed["analysis"] == "mixed model (balanced)")].iloc[0]
    assert row["share"] > 0.5 and row["p_perm"] < 0.05
