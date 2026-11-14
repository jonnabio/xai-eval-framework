"""Paper G: metrics, groups and exact Shapley values on cases with a known answer."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lib = _load("paper_g_lib")
syn = _load("paper_g_synthetic")
CFG = lib.config()


class Linear:
    """p1 = 0.5 + w . x (no clipping): every quantity has a closed form."""

    def __init__(self, w):
        self.w = np.asarray(w, dtype=float)

    def predict_proba(self, X):
        p1 = 0.5 + np.asarray(X) @ self.w
        return np.stack([1 - p1, p1], axis=-1)


GROUPS = [np.array([j]) for j in range(4)]
W = np.array([0.08, -0.04, 0.02, 0.01])
X = np.array([1.0, 1.0, 1.0, 1.0])
BASE = np.zeros(4)


def prob1(batch):
    return Linear(W).predict_proba(batch)[:, 1]


# --- configuration --------------------------------------------------------------------

def test_config_holds_the_plan():
    assert CFG["seeds"] == [42, 123, 456, 789, 101112]
    assert CFG["n_instances"] == 200
    assert [d["key"] for d in CFG["dataset"]] == [
        "phoneme", "qsar_biodeg", "magic_telescope", "electricity", "german_credit", "adult",
        "bank_marketing", "compas"]
    assert set(CFG["models"]) == set(lib.MODELS)
    assert set(CFG["explainers"]) == set(lib.EXPLAINERS)
    assert CFG["metrics"]["roar_levels"] == [0.1, 0.2, 0.3, 0.5]


# --- groups and baseline ------------------------------------------------------------------

def test_groups_join_the_one_hot_columns_of_a_feature():
    names = ["age", "hours", f"job{lib.SEP}a", f"job{lib.SEP}b", f"sex{lib.SEP}f", f"sex{lib.SEP}m"]
    groups, order, is_num = lib.make_groups(names, ["age", "hours"])
    assert order == ["age", "hours", "job", "sex"]
    assert [g.tolist() for g in groups] == [[0], [1], [2, 3], [4, 5]]
    assert is_num.tolist() == [True, True, False, False, False, False]


def test_baseline_is_mean_and_one_hot_mode():
    Xtr = np.array([[1.0, 1, 0], [3.0, 0, 1], [5.0, 0, 1]])
    groups = [np.array([0]), np.array([1, 2])]
    base = lib.baseline(Xtr, groups, np.array([True, False, False]))
    assert base.tolist() == [3.0, 0.0, 1.0]


def test_attributions_are_summed_per_group_and_oriented():
    w = np.array([0.5, 0.25, 0.25, -1.0])
    a = lib.group_attr(w, [np.array([0]), np.array([1, 2]), np.array([3])])
    assert a.tolist() == [0.5, 0.5, -1.0]
    assert lib.orient(a, 0).tolist() == [-0.5, -0.5, 1.0]


def test_order_breaks_ties_by_index():
    assert lib.order_of(np.array([1.0, 3.0, 3.0, -2.0])).tolist() == [1, 2, 0, 3]


# --- removal metrics -----------------------------------------------------------------------

def test_removal_metrics_closed_form():
    a = W * X                                          # the exact attribution of a linear model
    m = lib.removal_metrics(a, X, prob1, BASE, GROUPS, fraction=0.25)
    # order: 0 (0.08), 2 (0.02), 3 (0.01), 1 (-0.04)
    deletion = np.array([0.57, 0.49, 0.47, 0.46, 0.50])
    insertion = np.array([0.50, 0.58, 0.60, 0.61, 0.57])
    assert m["m1_deletion"] == pytest.approx(np.trapezoid(deletion, dx=0.25))
    assert m["m2_insertion"] == pytest.approx(np.trapezoid(insertion, dx=0.25))
    assert m["m3_gap"] == pytest.approx(0.08)          # top 1 of 4 groups masked
    assert m["m6_sufficiency"] == pytest.approx(0.57 - 0.58)


def test_correct_attribution_beats_reversed_on_every_removal_metric():
    good = lib.removal_metrics(W * X, X, prob1, BASE, GROUPS, 0.25)
    bad = lib.removal_metrics(-W * X, X, prob1, BASE, GROUPS, 0.25)
    assert good["m1_deletion"] < bad["m1_deletion"]
    assert good["m2_insertion"] > bad["m2_insertion"]
    assert good["m3_gap"] > bad["m3_gap"]
    assert good["m6_sufficiency"] < bad["m6_sufficiency"]


def test_correlation_is_one_for_occlusion_and_flags_constant_input():
    drops = W * X                                      # occlusion of a linear model
    r, degenerate = lib.correlation_metric(drops, X, prob1, BASE, GROUPS)
    assert r == pytest.approx(1.0) and not degenerate
    r, degenerate = lib.correlation_metric(np.ones(4), X, prob1, BASE, GROUPS)
    assert r == 0.0 and degenerate


def test_infidelity_is_zero_for_exact_additive_attribution_and_scale_free():
    rng = lambda: np.random.default_rng(0)  # noqa: E731
    exact = lib.infidelity_metric(W * X, X, prob1, BASE, GROUPS, 100, 0.5, rng())
    scaled = lib.infidelity_metric(3 * W * X, X, prob1, BASE, GROUPS, 100, 0.5, rng())
    wrong = lib.infidelity_metric(np.array([0.0, 1.0, 0.0, 0.0]), X, prob1, BASE, GROUPS, 100,
                                  0.5, rng())
    assert exact == pytest.approx(0.0, abs=1e-12)
    assert scaled == pytest.approx(0.0, abs=1e-12)
    assert 0.0 < wrong <= 1.0


def test_roar_removes_the_top_share():
    assert lib.n_top(8, 0.1) == 1 and lib.n_top(8, 0.5) == 4 and lib.n_top(3, 0.2) == 1


# --- explainers on a known model ------------------------------------------------------------

def _known_data(generator="additive", rho=0.0):
    cfg = {**CFG, "synthetic": {**CFG["synthetic"], "n_instances": 4}}
    return syn.make_condition(generator, rho, 42, cfg), cfg


def test_every_explainer_returns_a_row_with_all_metrics():
    data, cfg = _known_data()
    rows = list(lib.explain_and_score(data, lib.EXPLAINERS, 42, cfg, n_instances=2))
    assert len(rows) == 2 * len(lib.EXPLAINERS)
    for r in rows:
        assert r["failed"] == 0, r["fail_reason"]
        for k in lib.INSTANCE_METRICS:
            assert np.isfinite(r[k])
        assert len(r["attr"]) == 8


def test_occlusion_attribution_is_the_single_group_drop():
    data, cfg = _known_data()
    ex = lib.make_explainer("occlusion", data["model"], data, 42, cfg)
    x = data["X_test"][0]
    w = ex.explain(x, 1)
    z = x.copy()
    z[2] = data["base"][2]
    p = data["model"].predict_proba(np.vstack([x, z]))[:, 1]
    assert w[2] == pytest.approx(p[0] - p[1])


# --- exact Shapley ---------------------------------------------------------------------------

def test_exact_shapley_of_a_linear_function():
    rng = np.random.default_rng(1)
    bg = rng.standard_normal((50, 5))
    x = rng.standard_normal(5)
    beta = np.array([1.0, -2.0, 0.5, 0.0, 3.0])
    phi = syn.interventional_shapley(lambda z: z @ beta, x, bg)
    assert phi == pytest.approx(beta * (x - bg.mean(axis=0)))


def test_exact_shapley_is_efficient_for_the_interaction_model():
    data, _ = _known_data("interaction", 0.5)
    pos = int(data["instances"][0])
    phi = syn.true_attribution(data, pos)
    c = int(data["pred"][pos])
    f = lambda z: data["model"].predict_proba(z)[:, c]  # noqa: E731
    expected = f(data["X_test"][pos:pos + 1])[0] - f(data["truth_background"]).mean()
    assert phi.sum() == pytest.approx(expected)
    assert abs(phi[6]) < 1e-12 and abs(phi[7]) < 1e-12   # features with no effect


def test_correlated_sample_has_the_requested_correlation():
    X = syn.sample(20000, 8, 0.5, np.random.default_rng(0))
    c = np.corrcoef(X.T)
    assert c[0, 1] == pytest.approx(0.5, abs=0.03)
