"""Paper G S1 supplementary analysis (scripts/paper_g_s1_analyze.py) on constructed data only."""
import importlib.util
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd
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
an = _load("paper_g_analyze")
sa = _load("paper_g_s1_analyze")
M6 = list(lib.INSTANCE_METRICS)
DS = [f"d{i}" for i in range(8)]
Q = {"shap": 3.0, "lime": 1.0, "occlusion": 2.0, "random": 0.0}


def val(m, q):
    return q if lib.HIGHER_IS_BETTER[m.removesuffix("_b2")] else -q


def frozen(n=6, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for d, m, s, e in itertools.product(DS, lib.MODELS, [1, 2, 3, 4, 5], Q):
        for i in range(n):
            r = {"dataset": d, "model": m, "seed": s, "explainer": e, "instance": i, "m4_degenerate": False,
                 "f_x": 0.6 + 0.01 * i}
            for k in (*M6, *sa.B2.values()):
                r[k] = val(k, Q[e] + 0.01 * i + 0.3 * rng.normal())
            rows.append(r)
    full = pd.DataFrame(rows)
    roar = pd.DataFrame([{"dataset": d, "model": m, "seed": s, "explainer": e, "m7_roar": Q[e] + 0.1 * rng.normal()}
                         for d, m, s, e in itertools.product(DS, lib.MODELS, [1, 2, 3, 4, 5], Q)])
    return full, roar


def s1_from(full, roar, shift=0.0):
    lime = full[full["explainer"] == "lime"]
    rows = []
    for rep in ("S1-B", "S1-M"):
        for _, r in lime.iterrows():
            rows.append({"dataset": r["dataset"], "model": r["model"], "seed": r["seed"], "instance": r["instance"],
                         "representation": rep, "m4_degenerate": 0,
                         **{k: r[k] + val(k, shift) for k in (*M6, *sa.B2.values())}})
    m7 = roar[roar["explainer"] == "lime"][an.BLOCK + ["m7_roar"]]
    m7 = pd.concat([m7.assign(representation=rep, m7_roar=m7["m7_roar"] + shift) for rep in ("S1-B", "S1-M")])
    checks = pd.DataFrame([{"dataset": d, "categorical_groups": int(d in DS[4:]), "seed": 1} for d in DS])
    return {"rows": rows, "m7": m7, "checks": checks, "blocks": 160}


def spec():
    s = an.load_spec()
    return {**s, "h1": {**s["h1"], "permutations": 100}, "h2": {**s["h2"], "bootstrap": 100}}


def test_identical_s1_rows_reproduce_the_original_condition():
    full, roar = frozen()
    s1 = s1_from(full, roar)
    res = {c: sa.analyse_condition(*sa.condition(full, roar, s1, c), spec()) for c in sa.CONDITIONS}
    for c in ("S1-B", "S1-M"):
        assert res[c]["h1"]["spearman"] == pytest.approx(res["original"]["h1"]["spearman"])
        assert res[c]["h2"] == pytest.approx(res["original"]["h2"])
        assert res[c]["positions"]["summary"]["value"].tolist() == res["original"]["positions"]["summary"]["value"].tolist()


def test_substitution_changes_only_lime_rows_and_no_p_values(tmp_path):
    full, roar = frozen(seed=1)
    s1 = s1_from(full, roar, shift=5.0)                       # LIME now ranked first everywhere
    f, r = sa.condition(full, roar, s1, "S1-B")
    keep = ["dataset", "model", "seed", "explainer", "instance"]
    a = full[full["explainer"] != "lime"].sort_values(keep).reset_index(drop=True)
    b = f[f["explainer"] != "lime"].sort_values(keep).reset_index(drop=True)
    pd.testing.assert_frame_equal(a[b.columns], b)
    assert (r[r["explainer"] != "lime"]["m7_roar"].to_numpy() == roar[roar["explainer"] != "lime"]["m7_roar"].to_numpy()).all()
    res = {c: sa.analyse_condition(*sa.condition(full, roar, s1, c), spec()) for c in sa.CONDITIONS}
    pos = res["S1-B"]["positions"]["positions_by_metric"].set_index(["metric", "explainer"])
    assert pos.loc[("m1_deletion", "lime"), "r1"] == 160
    comp = sa.write_all(res, s1, tmp_path / "out", tmp_path / "R.md", {"fixture": 1})
    assert set(comp["condition"]) == set(sa.CONDITIONS)
    for p in (tmp_path / "out").rglob("*.csv"):
        assert not any(c.startswith("p_") or c == "p" for c in pd.read_csv(p).columns), p
    assert "no test" in (tmp_path / "R.md").read_text()


def test_original_check_detects_a_mismatch(tmp_path):
    full, roar = frozen()
    res = sa.analyse_condition(full, roar, spec())
    pd.DataFrame([{"analysis": "mean pairwise Spearman", **res["h1"]["spearman"]},
                  {"analysis": "Kendall W", **res["h1"]["w"]}]).to_csv(tmp_path / "h1_summary.csv", index=False)
    pd.DataFrame([res["h2"]]).to_csv(tmp_path / "h2_omnibus.csv", index=False)
    assert sa.check_original(res, tmp_path) < 1e-12
    pd.DataFrame([res["h2"] | {"mean": res["h2"]["mean"] + 0.01}]).to_csv(tmp_path / "h2_omnibus.csv", index=False)
    assert sa.check_original(res, tmp_path) == pytest.approx(0.01)


def test_refusal():
    assert sa.main([]) == 2 and sa.main(["--run"]) == 2
