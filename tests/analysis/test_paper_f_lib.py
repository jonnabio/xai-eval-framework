"""Paper F: measures and instance selection (scripts/paper_f_lib.py)."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "paper_f_lib.py"
spec = importlib.util.spec_from_file_location("paper_f_lib", SCRIPT)
lib = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lib)

CFG = lib.config()


def test_config_holds_the_plan():
    assert CFG["seeds"] == [42, 123, 456, 789, 101112]
    assert CFG["n_instances"] == 200 and CFG["target_datasets"] == 16
    assert set(CFG["models"]) == set(lib.MODELS)
    assert set(CFG["explainers"]) == set(lib.EXPLAINERS)
    keys = [d["key"] for d in CFG["dataset"]]
    assert len(keys) == len(set(keys)) == 17 and "adult" in keys


def test_top_set_takes_the_largest_used_features():
    w = np.array([0.0, -3.0, 1.0, 2.0, 0.0, 0.5])
    assert lib.top_set(w, 2, 1e-8) == frozenset({1, 3})
    assert lib.top_set(w, 10, 1e-8) == frozenset({1, 2, 3, 5})
    assert lib.top_set(np.zeros(4), 5, 1e-8) == frozenset()


def test_top_set_breaks_ties_by_position():
    assert lib.top_set(np.ones(8), 3, 1e-8) == frozenset({0, 1, 2})


def test_jaccard():
    assert lib.jaccard(frozenset(), frozenset()) == 1.0
    assert lib.jaccard(frozenset({1}), frozenset()) == 0.0
    assert lib.jaccard(frozenset({1, 2}), frozenset({2, 3})) == pytest.approx(1 / 3)


def test_pick_instances_is_stratified_and_repeatable():
    pred = np.array([0] * 900 + [1] * 100)
    a = lib.pick_instances(pred, 200, 42)
    assert len(a) == 200 and pred[a].sum() == 20
    assert np.array_equal(a, lib.pick_instances(pred, 200, 42))
    assert len(lib.pick_instances(pred[:150], 200, 42)) == 150


def _toy():
    rng = np.random.default_rng(0)
    X = pd.DataFrame({"a": rng.normal(size=400), "b": rng.normal(size=400),
                      "c": rng.choice(["x", "y", "z"], size=400)})
    y = pd.Series((X["a"] + (X["c"] == "x") > 0.5).astype(int))
    return X, y


def test_split_puts_numeric_columns_first():
    X, y = _toy()
    data = lib.split(X, y, 42, CFG)
    assert data["names"][:2] == ["a", "b"] and data["is_numeric"].tolist() == [True, True, False, False, False]
    assert data["X_train"].shape == (320, 5) and data["X_test"].shape == (80, 5)
    assert set(np.unique(data["X_train"][:, 2:])) == {0.0, 1.0}


def test_faithfulness_gap_is_larger_for_the_feature_the_model_uses():
    X, y = _toy()
    data = lib.split(X, y, 42, CFG)
    model = lib.make_model("logreg", 42, CFG).fit(data["X_train"], data["y_train"])
    base = lib.baseline(data)
    x = data["X_test"][np.argmax(np.abs(data["X_test"][:, 0]))]
    used = lib.faithfulness(np.array([1.0, 0, 0, 0, 0]), x, model, base, CFG)
    unused = lib.faithfulness(np.array([0, 1.0, 0, 0, 0]), x, model, base, CFG)
    assert used["gap"] > unused["gap"]
    assert lib.faithfulness(np.zeros(5), x, model, base, CFG)["gap"] == 0.0


class _Fixed(lib.Explainer):
    name = "lime"

    def explain(self, x, seed):
        if x[0] > 90:
            raise lib.Failure("none")
        w = np.zeros(self.d)
        w[0] = 1.0
        return w, {}


def test_evaluate_records_measures_and_failures():
    X, y = _toy()
    data = lib.split(X, y, 42, CFG)
    model = lib.make_model("logreg", 42, CFG).fit(data["X_train"], data["y_train"])
    explainer = _Fixed(model, data, 42, CFG)
    row = lib.evaluate(explainer, data["X_test"][0], 0, lib.baseline(data), CFG)
    assert row["failed"] == 0 and row["stability"] == 1.0 and row["n_used"] == 1
    assert row["sparsity"] == pytest.approx(0.8) and row["top"] == [0]
    bad = data["X_test"][0].copy()
    bad[0] = 100.0
    row = lib.evaluate(explainer, bad, 0, lib.baseline(data), CFG)
    assert row["failed"] == 1 and "Failure" in row["fail_reason"]
