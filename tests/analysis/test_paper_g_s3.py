"""Paper G S3 (scripts/paper_g_s3_lime.py) on constructed inputs only; the frozen run is not read."""
import gzip
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
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
syn = _load("paper_g_synthetic")
s3 = _load("paper_g_s3_lime")


class LinearProb:
    """p1(x) = 0.5 + 0.04 * beta . (x - mu): exact contributions relative to mu are 0.04 * beta * (x - mu)."""

    def __init__(self, beta, mu):
        self.beta, self.mu = np.asarray(beta, float), np.asarray(mu, float)

    def predict_proba(self, X):
        p1 = np.clip(0.5 + 0.04 * (np.asarray(X, float) - self.mu) @ self.beta, 0, 1)
        return np.column_stack([1 - p1, p1])


def toy(seed=0):
    rng = np.random.default_rng(seed)
    sd = np.array([1.0, 2.0, 0.5, 1.0, 3.0, 1.0])
    X = rng.normal(0, 1, (1500, 6)) * sd + np.array([0, 1, -1, 0, 2, 0])
    beta = np.array([2.0, -1.5, 1.0, -0.5, 0.25, 0.8])
    model = LinearProb(beta, X.mean(axis=0))
    data = {"X_train": X, "names": [f"x{j}" for j in range(6)], "model": model}
    return data, model, beta


def cfg_lime():
    return {"explainers": {"lime": {"kernel_width": 3.0, "num_samples": 1000}}}


def test_contribution_formula_by_hand():
    w, x, m, s = np.array([0.2, -0.1]), np.array([3.0, 1.0]), np.array([1.0, 2.0]), np.array([2.0, 0.5])
    assert np.allclose(s3.to_contribution(w, x, m, s), [0.2 * 1.0, -0.1 * -2.0])


def test_contribution_recovers_exact_linear_contributions_with_fitted_scaler():
    data, model, beta = toy()
    lime = s3.LimeConfig(data, 7, cfg_lime(), False, 3.0)
    for i in range(5):
        x = data["X_train"][10 + i]
        w = lime.explain(x, 100 + i)
        mean, scale = lime.lime.scaler.mean_, lime.lime.scaler.scale_
        assert np.allclose(mean, data["X_train"].mean(axis=0)) and np.allclose(scale, data["X_train"].std(axis=0))
        c = s3.to_contribution(w, x, mean, scale)
        truth = 0.04 * beta * (x - model.mu)
        assert np.allclose(c, truth, atol=2e-3)
        assert s3.spearman_or_nan(c, truth) == pytest.approx(1.0)
        assert np.allclose(w, 0.04 * beta * scale, atol=2e-3)                  # the slope per s.d.


def test_orientation_commutes_with_the_transformation():
    w, x, m, s = np.array([0.3, -0.2, 0.1]), np.array([1.0, -1.0, 2.0]), np.zeros(3), np.ones(3)
    for c in (0, 1):
        assert np.allclose(lib.orient(s3.to_contribution(w, x, m, s), c),
                           s3.to_contribution(lib.orient(w, c), x, m, s))


def test_variant_class_reproduces_the_frozen_lime_exactly():
    data, model, _ = toy(1)
    data.update(groups=[np.array([j]) for j in range(6)])
    frozen = lib.make_explainer("lime", model, data, 42, {"explainers": {"lime": {"kernel_width": 3.0,
                                                                               "num_samples": 1000}}})
    variant = s3.LimeConfig(data, 42, cfg_lime(), False, 3.0)
    for i in range(3):
        x = data["X_train"][i]
        assert np.array_equal(frozen.explain(x, 5 + i), variant.explain(x, 5 + i))


def test_spearman_undefined_and_matches_scipy():
    assert math.isnan(s3.spearman_or_nan(np.ones(4), np.arange(4.0)))
    a, b = np.array([0.1, 0.5, 0.2, 0.9]), np.array([1.0, 3.0, 2.0, 2.5])
    assert s3.spearman_or_nan(a, b) == pytest.approx(stats.spearmanr(a, b).statistic)


def test_instance_seed_matches_frozen_formula():
    assert s3.instance_seed(42, 7) == (42 * 100003 + 7) % (2**31)
    assert s3.instance_seed(101112, 399) == (101112 * 100003 + 399) % (2**31)


def _small_cfg(n=3):
    c = lib.config()
    return {**c, "synthetic": {**c["synthetic"], "n_instances": n}}


def _stored_for(generator, rho, seed, cfg, tamper=False):
    """Records as the frozen run writes them, built by the frozen code for a tiny condition."""
    data = syn.make_condition(generator, rho, seed, cfg)
    lime = lib.make_explainer("lime", data["model"], data, seed, cfg)
    out = {}
    for pos in data["instances"]:
        pos = int(pos)
        c = int(data["pred"][pos])
        a = lib.orient(lib.group_attr(lime.explain(data["X_test"][pos], s3.instance_seed(seed, pos)),
                                      data["groups"]), c)
        attr = [round(float(v), 8) for v in a]
        if tamper and not out:
            attr[0] += 1e-3
        out[(pos, "lime")] = {"instance": pos, "explainer": "lime", "pred_class": c, "attr": attr,
                              "true_attr": [round(float(v), 8) for v in syn.true_attribution(data, pos)]}
    return out


def test_block_gate_reproduces_and_detects_tampering():
    cfg = _small_cfg()
    repro, rows, ref = s3.run_block("interaction", 0.5, 123, cfg, _stored_for("interaction", 0.5, 123, cfg))
    assert len(repro) == 3 and all(r["reproduced"] == 1 for r in repro)
    assert len(rows) == 3 * len(s3.REPRESENTATIONS)
    assert {r["representation"] for r in rows} == set(s3.REPRESENTATIONS)
    assert ref["truth_recomputed_first_instance_max_abs_diff"] <= s3.TRUTH_TOL
    repro, _, _ = s3.run_block("interaction", 0.5, 123, cfg, _stored_for("interaction", 0.5, 123, cfg, tamper=True))
    assert sum(r["reproduced"] for r in repro) == 2


def test_summaries_count_and_keep_undefined():
    rows = [{"condition": "c", "seed": 1, "instance": i, "pred_class": i % 2, "representation": "S3-A",
             "config": "F3", "kind": "slope", "spearman_truth": v} for i, v in enumerate([0.5, math.nan, 0.1])]
    cs, cond, cls = s3.summarise(rows)
    assert cs[0]["instances"] == 3 and cs[0]["undefined"] == 1 and cs[0]["mean_spearman_truth"] == pytest.approx(0.3)
    assert cond[0]["seeds"] == 1 and {r["pred_class"] for r in cls} == {0, 1}


def test_outputs_are_byte_deterministic(tmp_path):
    rows = [{"a": 1, "b": 0.123456789}, {"a": 2, "b": math.nan}]
    for name in ("x.csv.gz", "y.csv.gz"):
        s3.write_csv(tmp_path / name, rows, gz=True)
    assert (tmp_path / "x.csv.gz").read_bytes() == (tmp_path / "y.csv.gz").read_bytes()
    assert gzip.decompress((tmp_path / "x.csv.gz").read_bytes()).decode().splitlines()[1] == "1,0.12345679"


def test_refuses_without_authorization(capsys):
    assert s3.main([]) == 2
    assert s3.main(["--run"]) == 2
    assert "refused" in capsys.readouterr().err


def test_representations_are_declared_and_isolated():
    kinds = {k: v[2] for k, v in s3.REPRESENTATIONS.items()}
    assert kinds == {"S3-A": "slope", "S3-A-kd": "slope", "S3-B": "contribution", "S3-B-kd": "contribution",
                     "S3-C": "discretised", "S3-C-kd": "discretised"}
    assert s3.CONFIGS == {"F3": (False, 3.0), "FD": (False, None), "T3": (True, 3.0), "TD": (True, None)}
    json.dumps(s3.REPRESENTATIONS)
