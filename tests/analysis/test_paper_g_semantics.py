"""RCA-005 guard: the explainer-metric semantic contract (scripts/paper_g_semantics.py)."""
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
sem = _load("paper_g_semantics")
SIGNED = ["m1_deletion", "m2_insertion", "m3_gap", "m4_corr", "m5_infidelity", "m6_sufficiency"]


def test_compatible_pairs_pass():
    for e in ("shap", "occlusion", "random"):
        for m in [*SIGNED, "m7_roar"]:
            assert sem.check(e, m, multi_column_groups=True).status == "compatible"


@pytest.mark.parametrize("metric", SIGNED)
def test_lime_slopes_into_signed_metrics_are_refused(metric):
    with pytest.raises(sem.IncompatibleSemantics, match="LOCAL_SURROGATE_COEFFICIENT"):
        sem.check("lime", metric, multi_column_groups=False)


def test_lime_into_m7_depends_on_grouping():
    assert sem.check("lime", "m7_roar", multi_column_groups=False).status == "compatible"
    with pytest.raises(sem.IncompatibleSemantics, match="multi-column group"):
        sem.check("lime", "m7_roar", multi_column_groups=True)


def test_declared_conversion_and_declared_estimand_are_explicit():
    v = sem.check("lime", "m1_deletion", multi_column_groups=True, conversion=True)
    assert v.status == "converted" and "training mean" in v.note
    v = sem.check("lime", "m4_corr", multi_column_groups=True, declared=sem.PAPER_G_FROZEN_DECLARATIONS)
    assert v.status == "declared alternative estimand" and "LIME as configured" in v.note
    with pytest.raises(sem.IncompatibleSemantics):                      # a declaration for another pair does not help
        sem.check("lime", "m7_roar", multi_column_groups=True, declared=sem.PAPER_G_FROZEN_DECLARATIONS)


def test_frozen_paper_g_run_passes_only_with_its_declarations():
    with pytest.raises(sem.IncompatibleSemantics):
        sem.audit(lib.EXPLAINERS, SIGNED, multi_column_groups=True)
    rows = sem.audit(lib.EXPLAINERS, SIGNED, multi_column_groups=True, declared=sem.PAPER_G_FROZEN_DECLARATIONS)
    lime = [r["status"] for r in rows if r["explainer"] == "lime"]
    assert lime == ["declared alternative estimand"] * 6
    assert all(r["status"] == "compatible" for r in rows if r["explainer"] != "lime")


def test_declaration_is_bound_to_the_live_lime_configuration():
    """If someone changes paper_g_lib.Lime (e.g. turns discretisation on), this test fails until the
    contract is updated: the declaration cannot drift from the code."""
    rng = np.random.default_rng(0)
    X = rng.normal(size=(200, 4))

    class M:
        def predict_proba(self, Z):
            p = 1 / (1 + np.exp(-Z[:, 0]))
            return np.column_stack([1 - p, p])
    data = {"X_train": X, "names": ["a", "b", "c", "d"], "groups": [np.array([j]) for j in range(4)]}
    lime = lib.make_explainer("lime", M(), data, 1, lib.config())
    assert sem.lime_kind_of(lime.lime) is sem.EXPLAINERS["lime"].kind
    from lime.lime_tabular import LimeTabularExplainer
    discretised = LimeTabularExplainer(X, mode="classification", discretize_continuous=True, random_state=1)
    assert sem.lime_kind_of(discretised) is sem.Kind.DISCRETISED_INDICATOR_WEIGHT


def test_every_paper_g_explainer_and_metric_is_declared():
    assert set(sem.EXPLAINERS) == set(lib.EXPLAINERS)
    assert set(sem.METRICS) == set(lib.HIGHER_IS_BETTER)
