"""Paper G exploratory diagnostics (scripts/paper_g_diagnostics.py) on constructed data only."""
import importlib.util
import itertools
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import stats

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lib = _load("paper_g_lib")
an = _load("paper_g_analyze")
dg = _load("paper_g_diagnostics")

DS, MODELS, SEEDS, EXPL = ["d0", "d1"], ["rf", "mlp"], [1, 2], ["shap", "lime", "occlusion", "random"]
Q = {"shap": 3.0, "lime": 1.0, "occlusion": 2.0, "random": 0.0}       # LIME last among the studied
M6 = list(lib.INSTANCE_METRICS)


def value(metric, q):
    return q if lib.HIGHER_IS_BETTER[metric] else -q


def make_full(n=30, seed=0, noise=0.0, shared_f=False):
    rng = np.random.default_rng(seed)
    rows = []
    for d, m, s, e in itertools.product(DS, MODELS, SEEDS, EXPL):
        f = rng.uniform(0.5, 1.0, n)
        for i in range(n):
            r = {"dataset": d, "model": m, "seed": s, "explainer": e, "instance": i, "m4_degenerate": False,
                 "f_x": f[i]}
            for met in M6:
                trend = 5 * f[i] if shared_f else 0.01 * i
                r[met] = value(met, Q[e] + trend + noise * rng.normal())
            rows.append(r)
    return pd.DataFrame(rows)


def make_roar(rank_of=None, m7=None, G=5):
    rows = []
    for d, m, s, e in itertools.product(DS, MODELS, SEEDS, EXPL):
        gr = (rank_of or {}).get(e, list(range(G)))
        rows.append({"dataset": d, "model": m, "seed": s, "explainer": e,
                     "m7_roar": (m7 or Q)[e], "global_rank": gr})
    return pd.DataFrame(rows)


def system(full, roar):
    return an.system_table(an.block_means(full, M6), roar[an.BLOCK + ["explainer", "m7_roar"]])


def test_r3_detects_a_consistently_last_explainer_and_shap_occlusion_order():
    res = dg.r3(system(make_full(), make_roar()))
    b = res["blocks"]
    assert len(b) == 8 and (b["consistently_last"] == "lime").all()
    assert (b["extreme_explainer"] == "shap").all() and (b["extreme_position"] == 1).all()
    pos = res["positions_by_metric"].set_index(["metric", "explainer"])
    assert pos.loc[("m1_deletion", "lime"), "r3"] == 8 and pos.loc[("m1_deletion", "shap"), "r1"] == 8
    so = res["shap_occlusion"]
    assert (so["pair_agreement_share"] == 1.0).all() and (so["all_seven_same_order"] == 1).all()


def test_r3_ties_are_counted_not_ranked():
    q = {"shap": 2.0, "lime": 2.0, "occlusion": 1.0, "random": 0.0}
    full = make_full()
    for met in M6:
        full.loc[full["explainer"] == "lime", met] = full.loc[full["explainer"] == "shap", met].to_numpy()
    res = dg.r3(system(full, make_roar(m7=q)))
    pos = res["positions_by_metric"].set_index(["metric", "explainer"])
    assert pos.loc[("m1_deletion", "lime"), "tied"] == 8 and pos.loc[("m1_deletion", "lime"), "r1"] == 0
    assert (res["blocks"]["consistently_last"] == "occlusion").all()


def test_partial_spearman_matches_the_correlation_formula():
    rng = np.random.default_rng(3)
    f = rng.normal(size=50)
    a, b = f + rng.normal(size=50), f + rng.normal(size=50)
    ra, rb, rf = stats.rankdata(a), stats.rankdata(b), stats.rankdata(f)
    r_ab, r_af, r_bf = (np.corrcoef(u, v)[0, 1] for u, v in ((ra, rb), (ra, rf), (rb, rf)))
    expected = (r_ab - r_af * r_bf) / math.sqrt((1 - r_af ** 2) * (1 - r_bf ** 2))
    assert dg.partial_spearman(a, b, f) == pytest.approx(expected)
    assert math.isnan(dg.partial_spearman(f, a, f))                          # residual of f on f is constant


def test_r6_adjustment_removes_a_shared_prediction_level_trend():
    res = dg.r6(make_full(shared_f=True, noise=0.5, seed=4))
    s = res["summary"].set_index("pair")
    assert s.loc["omnibus", "unadjusted_mean"] > 0.5
    assert abs(s.loc["omnibus", "adjusted_mean"]) < 0.15
    assert len(res["datasets"]) == 2 and len(res["blocks"]) == 2 * 2 * 2 * 4


def test_r6_unadjusted_path_equals_frozen_h2_code(tmp_path):
    full = make_full(noise=0.4, seed=5)
    spec = an.load_spec()
    h2 = an.h2_analysis(full, EXPL, M6, {**spec, "h2": {**spec["h2"], "bootstrap": 200}})
    an._csv(an._summary_frame(h2["omnibus"], "H2 omnibus"), tmp_path / "h2_omnibus.csv")
    an._csv(h2["pairs"], tmp_path / "h2_pairs.csv")
    assert dg.validate_r6_against_frozen(dg.r6(full)["summary"], tmp_path) <= dg.H2_TOL


def test_r7_identical_removal_sets_and_ties():
    roar = make_roar(rank_of={"shap": [0, 1, 2, 3, 4], "lime": [0, 1, 2, 3, 4], "occlusion": [1, 0, 2, 3, 4]},
                     m7={"shap": 0.5, "lime": 0.5, "occlusion": 0.1, "random": 0.0})
    res = dg.r7(roar, [0.1, 0.2, 0.3, 0.5])
    g = res["groups"].set_index("dataset")
    assert g.loc["d0", "G"] == 5 and [g.loc["d0", f"k_{lv}"] for lv in (0.1, 0.2, 0.3, 0.5)] == [1, 1, 2, 3]
    rs = res["removal_sets"]
    assert (rs.query("k == 1")["identical_pairs"] == 1).all()                # occlusion's top differs
    assert (rs.query("k >= 2")["all_three_identical"] == 1).all()            # {0, 1} = {1, 0}
    assert (res["ties"]["any_equal_pair"] == 1).all() and (res["ties"]["top_tied"] == 1).all()


def test_r11_random_last_with_denominator_and_ties():
    res = dg.r11(system(make_full(), make_roar()))
    s = res["summary"].iloc[0]
    assert (s["denominator_blocks"], s["untied_last_all7"], s["last_or_tied_all7"]) == (8, 8, 8)
    full = make_full()
    full.loc[full["explainer"] == "random", M6] = full.loc[full["explainer"] == "lime", M6].to_numpy()
    q = {**Q, "random": Q["lime"]}
    s = dg.r11(system(full, make_roar(m7=q)))["summary"].iloc[0]
    assert (s["untied_last_all7"], s["last_or_tied_all7"]) == (0, 8)          # tied last is not untied last


def test_outputs_deterministic_and_refusal(tmp_path, capsys):
    full, roar = make_full(noise=0.3, seed=6), make_roar()
    for k in ("a", "b"):
        dg.run_all(full, roar, tmp_path / k, tmp_path / k / "R.md", {"fixture": 1}, [0.1, 0.2, 0.3, 0.5], frozen=None)
    a = {p.name: p.read_bytes() for p in (tmp_path / "a").glob("*")}
    b = {p.name: p.read_bytes() for p in (tmp_path / "b").glob("*")}
    assert a == b and "r3_summary.csv" in a and "r6_summary.csv" in a and "r11_summary.csv" in a
    assert dg.main([]) == 2 and dg.main(["--run"]) == 2 and "refused" in capsys.readouterr().err
