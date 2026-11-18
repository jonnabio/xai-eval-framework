"""Paper G S1 (scripts/paper_g_s1_lime.py) on constructed data only; the frozen run is not read.

Toy data go through the frozen preprocessing (paper_g_lib.split), so the one-hot encoding, the
feature groups and the masking baseline are exactly those of the real pipeline.
"""
import importlib.util
import itertools
import json
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
sem = _load("paper_g_semantics")
s1 = _load("paper_g_s1_lime")
CFG = lib.config()


def frame(n=900, seed=0, constant=False):
    rng = np.random.default_rng(seed)
    X = pd.DataFrame({"num_a": rng.normal(2, 3, n), "num_b": rng.normal(-1, 0.5, n),
                      "colour": rng.choice(["red", "green", "blue"], n, p=[0.5, 0.3, 0.2]),
                      "flag": rng.choice(["yes", "no"], n, p=[0.7, 0.3])})
    if constant:
        X["num_c"] = 4.0
    y = pd.Series((X["num_a"] + (X["colour"] == "blue") * 2 + rng.normal(0, 1, n) > 2.5).astype(int))
    return X, y


class LinearEncoded:
    """p1 = 0.5 + k * beta . (x - b): exact contributions relative to the baseline b are k * beta_j (x_j - b_j)."""

    def __init__(self, beta, b, k=0.02):
        self.beta, self.b, self.k = np.asarray(beta, float), np.asarray(b, float), k

    def predict_proba(self, Z):
        p1 = np.clip(0.5 + self.k * (np.asarray(Z, float) - self.b) @ self.beta, 0, 1)
        return np.column_stack([1 - p1, p1])

    def predict(self, Z):
        return (self.predict_proba(Z)[:, 1] >= 0.5).astype(int)


def toy_data(model="linear", seed=0, constant=False, n_inst=6):
    X, y = frame(seed=seed, constant=constant)
    data = lib.split(X, y, seed, CFG)
    data["base"] = lib.baseline(data["X_train"], data["groups"], data["is_numeric"])
    p = data["X_train"].shape[1]
    if model == "linear":
        beta = np.linspace(-2, 2, p) + 0.3
        data["model"] = LinearEncoded(beta, data["base"])
        data["beta"] = beta
    else:
        data["model"] = lib.fit(lib.make_model("logreg", seed, CFG), data["X_train"], data["y_train"])
        data["auc"] = 0.8
    data["pred"] = data["model"].predict(data["X_test"]).astype(int)
    data["instances"] = lib.pick_instances(data["pred"], n_inst, seed)
    return data


def lime_for(data, seed=1):
    return lib.make_explainer("lime", data["model"], data, seed, CFG)


# --- conversion ------------------------------------------------------------------------------------

def test_surrogate_identity():
    rng = np.random.default_rng(1)
    w, x, r, s, mu, b0 = (rng.normal(size=6), rng.normal(size=6), rng.normal(size=6),
                          rng.uniform(0.2, 3, 6), rng.normal(size=6), 0.4)

    def g(v):                                   # LIME's surrogate on its standardised coordinates
        return b0 + w @ ((v - mu) / s)
    assert s1.contributions(w, x, r, s).sum() == pytest.approx(g(x) - g(r))


def test_invalid_scales_and_shapes_are_refused():
    with pytest.raises(ValueError, match="finite and positive"):
        s1.contributions(np.ones(2), np.ones(2), np.zeros(2), np.array([1.0, 0.0]))
    with pytest.raises(ValueError, match="finite and positive"):
        s1.contributions(np.ones(2), np.ones(2), np.zeros(2), np.array([1.0, np.nan]))
    with pytest.raises(ValueError, match="shape"):
        s1.contributions(np.ones(2), np.ones(3), np.zeros(3), np.ones(3))


def test_encoded_alignment_and_groups_from_the_frozen_preprocessing():
    data = toy_data()
    names, groups = np.array(data["names"]), data["groups"]
    assert data["group_names"] == ["num_a", "num_b", "colour", "flag"]
    assert [len(g) for g in groups] == [1, 1, 3, 2]
    for gname, g in zip(data["group_names"], groups):           # every column of a group is that feature
        assert all(n == gname or n.split(lib.SEP)[0] == gname for n in names[g])
    assert sorted(j for g in groups for j in g) == list(range(len(names)))      # a partition of the columns
    x = data["X_test"][0]
    assert np.allclose(lib.group_attr(x, groups), [x[g].sum() for g in groups])
    assert not data["is_numeric"][groups[2][0]] and data["is_numeric"][groups[0][0]]


def test_numeric_baseline_equals_lime_mean():
    data = toy_data()
    sc = lime_for(data).lime.scaler
    num = data["is_numeric"]
    assert np.max(np.abs(data["base"][num] - sc.mean_[num])) <= s1.TOL_REF
    cat = ~num
    assert not np.allclose(data["base"][cat], sc.mean_[cat])            # mode one-hot vs category shares


def test_s1b_recovers_exact_model_contributions_numeric_and_one_hot():
    """Linear model in the encoded columns: LIME's slope is exact, so S1-B equals the model's own
    contribution relative to the masking baseline for numeric and categorical groups."""
    data = toy_data()
    lime = lime_for(data)
    sc = lime.lime.scaler
    for pos in data["instances"]:
        x, c = data["X_test"][pos], int(data["pred"][pos])
        v = s1.s1_vectors(lime.explain(x, 10 + int(pos)), x, c, data, sc)
        truth = lib.orient(lib.group_attr(0.02 * data["beta"] * (x - data["base"]), data["groups"]), c)
        assert np.allclose(v["S1-B"], truth, atol=2e-3)
        num_groups = [i for i, g in enumerate(data["groups"]) if data["is_numeric"][g[0]]]
        assert np.allclose(v["S1-B"][num_groups], v["S1-M"][num_groups])     # same reference for numerics


def test_mode_value_gives_exactly_zero_s1b_and_nonzero_s1m():
    data = toy_data()
    lime = lime_for(data)
    for pos in data["instances"]:
        x = data["X_test"][pos]
        v = s1.s1_vectors(lime.explain(x, 3), x, 1, data, lime.lime.scaler)
        for gi, g in enumerate(data["groups"]):
            if not data["is_numeric"][g[0]] and np.array_equal(x[g], data["base"][g]):
                assert v["S1-B"][gi] == 0.0 and v["S1-M"][gi] != 0.0


def test_orientation_and_zero_variance_column():
    data = toy_data(constant=True)
    lime = lime_for(data)
    sc = lime.lime.scaler
    const = [j for j, n in enumerate(data["names"]) if n == "num_c"][0]
    assert sc.scale_[const] == 1.0 and np.all(np.isfinite(sc.scale_))            # sklearn: zero variance -> 1
    x = data["X_test"][data["instances"][0]]
    w = lime.explain(x, 2)
    v1, v0 = s1.s1_vectors(w, x, 1, data, sc), s1.s1_vectors(w, x, 0, data, sc)
    assert all(np.allclose(v0[k], -v1[k]) for k in v1) and all(np.all(np.isfinite(v1[k])) for k in v1)


def _baseline_shapley(data, x, c):
    """Exact Shapley over groups with masking to the baseline b (the M1-M6 reference)."""
    G = len(data["groups"])
    prob = lib.class_prob(data["model"], c)

    def v(S):
        return float(prob(lib._masked(x, data["base"], data["groups"], [i for i in range(G) if i not in S])[None])[0])
    phi = np.zeros(G)
    for i in range(G):
        for k in range(G):
            for S in itertools.combinations([j for j in range(G) if j != i], k):
                wgt = math.factorial(k) * math.factorial(G - k - 1) / math.factorial(G)
                phi[i] += wgt * (v(set(S) | {i}) - v(set(S)))
    return phi


def test_nonlinear_model_s1b_tracks_baseline_shapley_better_than_slopes():
    """Not an identity: for a fitted logistic model S1-B is a surrogate contribution. It should still be
    closer to the model's exact baseline-Shapley values than the frozen slopes are (documented property)."""
    data = toy_data("logreg", n_inst=12)
    lime = lime_for(data)
    rb, rs = [], []
    for pos in data["instances"]:
        x, c = data["X_test"][pos], int(data["pred"][pos])
        w = lime.explain(x, 7 + int(pos))
        truth = _baseline_shapley(data, x, c)
        rb.append(stats.spearmanr(s1.s1_vectors(w, x, c, data, lime.lime.scaler)["S1-B"], truth).statistic)
        rs.append(stats.spearmanr(lib.orient(lib.group_attr(w, data["groups"]), c), truth).statistic)
    assert np.nanmean(rb) > np.nanmean(rs), (np.nanmean(rb), np.nanmean(rs))
    assert np.nanmean(rb) > 0.5, np.nanmean(rb)


# --- gate, metrics, M7, contract -------------------------------------------------------------------

def _stored(data, seed, n, tamper=None):
    rows = {}
    for r in lib.explain_and_score(data, ["lime"], seed, CFG, n):
        r = {**r, "attr": list(r["attr"]), "pred_class": r["pred_class"]}
        rows[r["instance"]] = r
    if tamper:
        first = next(iter(rows))
        if tamper == "attr":
            rows[first]["attr"][0] += 1e-6
        else:
            rows[first]["m3_gap"] += 1e-6
    return rows


def test_block_gate_metrics_and_m7():
    data = toy_data("logreg", n_inst=5)
    res = s1.run_block("toy", "logreg", 11, CFG, 4, _stored(data, 11, 4), data=data)
    rec = res["reconstruction"]
    assert len(rec) == 4 and all(r["passed"] for r in rec)
    assert max(r["metric_max_diff"] for r in rec) <= s1.TOL_METRIC and max(r["fx_diff"] for r in rec) <= s1.TOL_FX
    assert len(res["rows"]) == 8 and {r["representation"] for r in res["rows"]} == {"S1-B", "S1-M"}
    for r in res["rows"]:
        assert all(math.isfinite(r[k]) for k in (*s1.SIGNED, *s1.B2)) and r["failed"] == 0
    for m in res["m7"]:                                                       # M7 ranking = order of mean |c|
        vecs = np.array([json.loads(r["group_vector"]) for r in res["rows"] if r["representation"] == m["representation"]])
        assert json.loads(m["global_rank"]) == [int(i) for i in lib.order_of(np.abs(vecs).mean(axis=0))]
        assert math.isfinite(m["m7_roar"])
    assert res["checks"][0]["s1b_nonzero_at_mode"] == 0 and res["checks"][0]["categorical_groups"] == 1
    statuses = {(r["representation"], r["status"]) for r in res["contract"]}
    assert ("S1-B", "compatible") in statuses and ("S1-M", "declared alternative estimand") in statuses


@pytest.mark.parametrize("tamper", ["attr", "metric"])
def test_gate_stops_on_tampered_stored_rows(tamper):
    data = toy_data("logreg", n_inst=3)
    with pytest.raises(s1.GateFailure, match="reconstruction gate failed"):
        s1.run_block("toy", "logreg", 11, CFG, 2, _stored(data, 11, 2, tamper=tamper), data=data)


def test_contract_is_enforced(monkeypatch):
    data = toy_data("logreg", n_inst=3)

    def refuse(*a, **k):
        raise sem.IncompatibleSemantics("refused")
    monkeypatch.setattr(s1.sem, "check", refuse)
    with pytest.raises(sem.IncompatibleSemantics):
        s1.run_block("toy", "logreg", 11, CFG, 2, _stored(data, 11, 2), data=data)


def test_substitute_lime_replaces_only_lime_rows():
    full = pd.DataFrame([{"dataset": "d", "model": "m", "seed": 1, "explainer": e, "instance": i,
                          **{k: 0.0 for k in (*s1.SIGNED, *s1.B2)}, "m4_degenerate": False}
                         for e in ("shap", "lime") for i in range(2)])
    rows = [{"dataset": "d", "model": "m", "seed": 1, "instance": i, "representation": "S1-B",
             **{k: 1.0 for k in (*s1.SIGNED, *s1.B2)}, "m4_degenerate": 0} for i in range(2)]
    out = s1.substitute_lime(full, rows, "S1-B")
    assert (out[out.explainer == "lime"]["m1_deletion"] == 1.0).all()
    assert (out[out.explainer == "shap"]["m1_deletion"] == 0.0).all() and len(out) == 4
    with pytest.raises(s1.GateFailure):
        s1.substitute_lime(full, rows[:1], "S1-B")


# --- governance --------------------------------------------------------------------------------------

def test_refusals_and_output_paths(capsys):
    assert s1.main([]) == 2 and s1.main(["--pilot"]) == 2
    assert s1.main(["--full"]) == 2 and s1.main(["--full", "--authorized", "  "]) == 2
    assert "refused" in capsys.readouterr().err
    frozen = [lib.OUT / "raw", lib.OUT / "analysis", lib.OUT / "supplementary" / "s3"]
    assert not any(s1.PILOT_OUT.is_relative_to(f) for f in frozen)
    assert s1.PILOT_OUT.is_relative_to(lib.OUT / "supplementary")


def test_csv_output_is_deterministic(tmp_path):
    rows = [{"a": 1, "b": 0.1 + 0.2, "c": "x"}]
    s1.write_csv(tmp_path / "x.csv", rows)
    s1.write_csv(tmp_path / "y.csv", rows)
    assert (tmp_path / "x.csv").read_bytes() == (tmp_path / "y.csv").read_bytes()
    assert "0.30000000000000004" in (tmp_path / "x.csv").read_text()     # full precision kept


# --- full driver (Task 19) ------------------------------------------------------------------------

def _fake_block(dataset, model, seed, cfg, n, stored, data=None, audit_n=0):
    if dataset == "bad":
        raise s1.GateFailure("constructed failure")
    rows = [{"dataset": dataset, "model": model, "seed": seed, "instance": i, "pred_class": 1, "representation": r,
             **{k: 0.5 + 0.01 * i for k in (*s1.SIGNED, *s1.B2, "f_x")}, "m4_degenerate": 0, "failed": 0,
             "group_vector": "[0.1]"} for i in range(n) for r in ("S1-B", "S1-M")]
    rec = [{"instance": i, "passed": 1, "fx_diff": 0.0, "attr_max_diff": 0.0, "metric_max_diff": 0.0} for i in range(n)]
    return {"reconstruction": rec, "rows": rows, "contract": [],
            "m7": [{"representation": r, "m7_roar": 0.1} for r in ("S1-B", "S1-M")],
            "checks": [{"s1b_nonzero_at_mode": 0}], "audit": {"instances": []}}


# The driver runs blocks in a ProcessPoolExecutor. Under "spawn" (the only start method on
# Windows) workers re-import the module, so the monkeypatched run_block never reaches them and
# the real computation runs on fixture datasets that do not exist. These tests need "fork".
needs_fork = pytest.mark.skipif(sys.platform == "win32",
                                reason="worker processes do not inherit monkeypatch under spawn")


@pytest.fixture
def fake(monkeypatch):
    monkeypatch.setattr(s1, "run_block", _fake_block)
    monkeypatch.setattr(s1, "stored_rows", lambda *a, **k: {})


@needs_fork
def test_full_driver_publishes_atomically_and_resumes(tmp_path, fake, monkeypatch):
    blocks = [("d0", "rf", 1), ("d0", "rf", 2), ("d1", "mlp", 1)]
    assert s1.run_full("test", out=tmp_path, jobs=2, blocks=blocks, n=3) == 0
    man = pd.read_csv(tmp_path / "MANIFEST.csv")
    assert len(man) == 3 and not list(tmp_path.rglob("*.part"))
    for b in blocks:
        p = s1.block_paths(tmp_path, *b)
        assert s1.sha256(p["shard"]) == json.loads(p["done"].read_text())["sha256"] and p["log"].exists()
    before = {q: q.read_bytes() for q in tmp_path.rglob("*.json.gz")}
    monkeypatch.setattr(s1, "run_block", lambda *a, **k: pytest.fail("a finished block was recomputed"))
    assert s1.run_full("test", out=tmp_path, jobs=2, blocks=blocks, n=3) == 0
    assert {q: q.read_bytes() for q in tmp_path.rglob("*.json.gz")} == before


@needs_fork
def test_full_driver_stops_on_failure_and_writes_no_manifest(tmp_path, fake):
    rc = s1.run_full("test", out=tmp_path, jobs=1, blocks=[("bad", "rf", 1), ("d0", "rf", 1)], n=2)
    assert rc == 3 and not (tmp_path / "MANIFEST.csv").exists()
    assert "constructed failure" in s1.block_paths(tmp_path, "bad", "rf", 1)["failed"].read_text()
    assert not s1.block_paths(tmp_path, "d0", "rf", 1)["done"].exists()       # not admitted after the failure


@needs_fork
def test_tampered_shard_is_refused_not_overwritten(tmp_path, fake):
    assert s1.run_full("test", out=tmp_path, jobs=1, blocks=[("d0", "rf", 1)], n=2) == 0
    p = s1.block_paths(tmp_path, "d0", "rf", 1)["shard"]
    p.write_bytes(p.read_bytes() + b"x")
    with pytest.raises(s1.GateFailure, match="does not match"):
        s1.run_full("test", out=tmp_path, jobs=1, blocks=[("d0", "rf", 1)], n=2)


def test_deterministic_serialisation_and_block_list():
    a = s1.det_gzip_json({"b": [1.5, "x"], "a": {"z": 1, "y": 2}})
    b = s1.det_gzip_json({"a": {"y": 2, "z": 1}, "b": [1.5, "x"]})
    assert a == b
    blocks = s1.full_blocks(CFG)
    assert len(blocks) == 160 == len(set(blocks))
    assert {m for _, m, _ in blocks} == set(lib.MODELS) and {s for *_, s in blocks} == set(CFG["seeds"])
