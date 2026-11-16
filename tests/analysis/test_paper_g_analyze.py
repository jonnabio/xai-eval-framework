"""Paper G analysis (scripts/paper_g_analyze.py) on constructed data with known answers.

No test reads the frozen run: every input is built here. Expected values are worked out by hand
where practical and checked against independent implementations (scipy, statsmodels, full
enumeration) elsewhere.
"""
import copy
import hashlib
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
an = _load("paper_g_analyze")
gate = _load("paper_g_dataset_gate")

DATASETS = [f"d{i}" for i in range(8)]
SEEDS = [1, 2, 3, 4, 5]
EXPL = list(lib.EXPLAINERS)              # shap, lime, occlusion, random
QUALITY = {"shap": 3.0, "lime": 2.0, "occlusion": 1.0, "random": 0.0}
M6 = list(lib.INSTANCE_METRICS)
SUB = set(an.load_spec()["baseline2"]["substitute"])


def decided_spec(perms=2000):
    s = copy.deepcopy(an.load_spec())
    s["h1"].update(h1_decision_p="raw", circularity_variant="drop_m4_rater", permutations=perms)
    s["h2"]["bootstrap"] = 500
    return s


def value_for(metric, q):
    """A raw metric value whose orientation makes higher quality more faithful."""
    return q if lib.HIGHER_IS_BETTER[metric.removesuffix("_b2")] else -q


def make_full(n_inst=6, quality=None, noise=0.0, seed=0, degenerate=()):
    """Instance rows; every metric orders the explainers by `quality` (per dataset if a dict of dicts)."""
    rng = np.random.default_rng(seed)
    rows = []
    for d, m, s, e in itertools.product(DATASETS, lib.MODELS, SEEDS, EXPL):
        q = (quality or QUALITY)[e] if not callable(quality) else quality(d, m, s, e)
        for i in range(n_inst):
            r = {"stage": "full", "dataset": d, "model": m, "seed": s, "explainer": e, "instance": i,
                 "failed": 0, "pred_class": 1, "m4_degenerate": (d, m, s, e, i) in degenerate}
            for met in M6:
                # oriented value = quality + an instance trend shared by every metric
                r[met] = value_for(met, q + i * 0.01) + noise * rng.normal()
                if met in SUB:
                    r[f"{met}_b2"] = r[met]
            if r["m4_degenerate"]:
                r["m4_corr"] = 0.0
            rows.append(r)
    return pd.DataFrame(rows)


def make_roar(quality=None):
    rows = []
    for d, m, s, e in itertools.product(DATASETS, lib.MODELS, SEEDS, EXPL):
        q = (quality or QUALITY)[e] if not callable(quality) else quality(d, m, s, e)
        rows.append({"stage": "roar", "dataset": d, "model": m, "seed": s, "explainer": e,
                     "failed": 0, "m7_roar": q})
    return pd.DataFrame(rows)


def make_synth(n_inst=5, truth=None, metric_quality=None):
    rows = []
    conds = ["additive_rho00", "additive_rho50", "interaction_rho00", "interaction_rho50"]
    for c, s, e in itertools.product(conds, SEEDS, EXPL):
        for i in range(n_inst):
            r = {"stage": "synthetic", "dataset": c, "model": "known", "seed": s, "explainer": e,
                 "instance": i, "failed": 0, "pred_class": 1, "m4_degenerate": False,
                 "spearman_truth": (truth or QUALITY)[e] / 3}
            for met in M6:
                r[met] = value_for(met, (metric_quality or QUALITY)[e])
                if met in SUB:
                    r[f"{met}_b2"] = r[met]
            rows.append(r)
    return pd.DataFrame(rows)


# --- ranks, agreement and ties ----------------------------------------------------------------

def test_average_ranks_and_orientation():
    assert list(an.ranks_desc(np.array([1.0, 1.0, 0.0]))) == [1.5, 1.5, 3.0]
    assert np.isnan(an.ranks_desc(np.array([1.0, np.nan, 0.0]))).all()
    v = np.array([0.1, 0.3])
    assert list(an.oriented(v, "m1_deletion")) == [-0.1, -0.3]           # lower is better
    assert list(an.oriented(v, "m2_insertion")) == [0.1, 0.3]
    assert list(an.oriented(v, "m6_sufficiency_b2")) == [-0.1, -0.3]     # _b2 keeps the direction
    assert list(an.oriented(v, "m7_roar")) == [0.1, 0.3]


def test_perfect_agreement_and_complete_reversal():
    R = np.array([[1, 2, 3]] * 7, float)
    assert an.kendall_w(R) == pytest.approx(1.0)
    assert an.mean_pairwise_spearman(R) == (pytest.approx(1.0), 21, 0)
    rev = np.array([[1, 2, 3], [3, 2, 1]], float)
    assert an.spearman_of_ranks(*rev) == pytest.approx(-1.0)
    assert an.kendall_w(rev) == pytest.approx(0.0)


def test_spearman_matches_scipy():
    rng = np.random.default_rng(3)
    for _ in range(50):
        x, y = rng.normal(size=9), rng.normal(size=9)
        x[2] = x[5]                                                          # with a tie
        ours = an.spearman_of_ranks(stats.rankdata(x), stats.rankdata(y))
        assert ours == pytest.approx(stats.spearmanr(x, y).statistic)


def test_tie_corrected_w_matches_friedman():
    """W = chi2_Friedman / (m (n - 1)); scipy's Friedman statistic is tie-corrected."""
    rng = np.random.default_rng(4)
    for _ in range(40):
        R = np.vstack([stats.rankdata(rng.integers(0, 3, size=4)) for _ in range(6)])
        if any(len(set(r)) == 1 for r in R):
            continue
        chi2 = stats.friedmanchisquare(*R.T).statistic
        assert an.kendall_w(R) == pytest.approx(chi2 / (R.shape[0] * (R.shape[1] - 1)))


def test_undefined_correlations_are_never_zero():
    R = np.array([[1, 2, 3], [2, 2, 2], [1, 2, 3]], float)                 # rater 2 all tied
    mean, defined, undefined = an.mean_pairwise_spearman(R)
    assert (mean, defined, undefined) == (pytest.approx(1.0), 1, 2)
    assert math.isnan(an.spearman_of_ranks(np.array([2, 2, 2.]), np.array([1, 2, 3.])))
    assert math.isnan(an.mean_pairwise_spearman(np.array([[2, 2, 2.], [1, 1, 1.]]))[0])
    assert math.isnan(an.kendall_w(np.array([[2, 2, 2.], [2, 2, 2.]])))  # denominator 0
    assert math.isnan(an.kendall_w(np.array([[1, 2, 3.]])))               # one rater


# --- aggregation, M7 and explainer populations ---------------------------------------------------

def test_system_table_m7_is_system_level_and_aligned():
    full, roar = make_full(), make_roar()
    sys_tab = an.system_table(an.block_means(full, M6), roar)
    assert len(sys_tab) == 8 * 4 * 5 * 4 and sys_tab["m7_roar"].notna().all()
    with pytest.raises(an.ValidationError):
        an.system_table(an.block_means(full, M6), roar.iloc[1:])
    assert "m7_roar" not in an.load_spec()["h2"]["metrics"]


def test_three_versus_four_explainers():
    sys_tab = an.system_table(an.block_means(make_full(), M6), make_roar())
    g = next(iter(sys_tab.groupby(an.BLOCK)))[1]
    spec = an.load_spec()
    assert an.rank_matrix(g, spec["h1"]["studied"], spec["h1"]["metrics"]).shape == (7, 3)
    assert an.rank_matrix(g, EXPL, spec["h1"]["metrics"]).shape == (7, 4)
    assert spec["h1"]["control"] == "random" and "random" not in spec["h1"]["studied"]


def test_h1_is_eight_dataset_means_of_twenty_blocks():
    spec = decided_spec()
    sys_tab = an.system_table(an.block_means(make_full(), M6), make_roar())
    res = an.h1_analysis(sys_tab, spec["h1"]["studied"], spec["h1"]["metrics"], spec)
    assert len(res["datasets_spearman"]) == 8 and (res["datasets_spearman"]["blocks"] == 20).all()
    assert res["spearman"]["n"] == 8 and res["spearman"]["df"] == 7
    assert res["spearman"]["mean"] == pytest.approx(1.0) and res["w"]["mean"] == pytest.approx(1.0)


def test_t_interval_has_seven_degrees_of_freedom():
    v = np.array([0.2, 0.4, 0.1, 0.5, 0.3, 0.6, 0.2, 0.45])
    ti = an.t_interval(v)
    lo, hi = stats.t.interval(0.95, 7, loc=v.mean(), scale=stats.sem(v))
    assert (ti["df"], ti["lo"], ti["hi"]) == (7, pytest.approx(lo), pytest.approx(hi))
    assert an.t_test_greater(v) == pytest.approx(stats.ttest_1samp(v, 0, alternative="greater").pvalue)


# --- the H1 permutation test --------------------------------------------------------------------

def _brute_statistic(R_by, draw, perms):
    """Direct recomputation: relabel each dataset's rater rows, then average as the plan does."""
    ds_means = []
    for d, (name, R) in enumerate(R_by.items()):
        P = np.stack([R[:, j, :][:, perms[draw[d, j]]] for j in range(R.shape[1])], axis=1)
        vals = [an.mean_pairwise_spearman(b)[0] for b in P]
        ds_means.append(np.nanmean(vals))
    return float(np.mean(ds_means))


def test_permutation_statistic_equals_direct_recomputation():
    rng = np.random.default_rng(5)
    R_by = {f"d{i}": np.stack([np.vstack([rng.permutation(3) + 1.0 for _ in range(4)]) for _ in range(5)])
            for i in range(3)}
    R_by["d0"][0, 2] = [2.0, 2.0, 2.0]                                     # an undefined rater in one block
    contribs, perms = an.permutation_contributions(R_by)
    for _ in range(20):
        draw = rng.integers(0, 6, size=(3, 4))
        fast = an.permutation_statistic(contribs, perms, draw[None])[0]
        assert fast == pytest.approx(_brute_statistic(R_by, draw, perms))


def test_permutation_shares_one_relabelling_across_a_datasets_blocks():
    """Identical blocks within a dataset stay identical after relabelling (dependence preserved)."""
    R = np.array([[[1, 2, 3], [1, 3, 2]]] * 20, float)                     # 20 identical blocks
    contribs, perms = an.permutation_contributions({"d": R})
    stats_ = an.permutation_statistic(contribs, perms, np.array(list(itertools.product(range(6), repeat=2)))[:, None, :])
    assert set(np.round(stats_, 9)) <= {1.0, 0.5, -0.5, -1.0}              # never an average of mixed blocks


def test_exact_enumeration_and_monte_carlo_agree():
    R_by = {"a": np.array([[[1, 2, 3], [1, 2, 3]]], float), "b": np.array([[[1, 2, 3], [2, 1, 3]]], float)}
    exact = an.exact_permutation_p(R_by)
    # by hand: per dataset the pair correlation under 6 relative relabellings is
    # a: {1, .5, .5, -.5, -.5, -1}, b: {.5, 1, -.5, -1, .5, -.5}; observed mean (1 + .5)/2 = .75;
    # pairs (x, y) with (x + y)/2 >= .75: x=1,y=1 (1*1 ways x 1) + x=1,y=.5 (2) + x=.5,y=1 (2*1) = 5 of 36
    assert exact == pytest.approx(5 / 36)
    mc = an.h1_permutation_test(R_by, 40000, 1)
    assert mc["p"] == pytest.approx(exact, abs=0.01)
    assert mc["p"] > 0


def test_permutation_reproducible_and_never_zero():
    R_by = {f"d{i}": np.array([[[1, 2, 3]] * 7] * 20, float) for i in range(8)}
    a = an.h1_permutation_test(R_by, 3000, 7)
    assert a == an.h1_permutation_test(R_by, 3000, 7)
    assert a["p"] == pytest.approx(1 / 3001)                                  # perfect agreement: smallest p


def test_permutation_null_calibration_with_dataset_level_disagreement():
    """Null with strong dataset-level structure: each dataset has its own random rater orders shared
    by its blocks (h = 1). A block-level permutation would be anti-conservative; this one is not."""
    rng = np.random.default_rng(11)
    ps = []
    for sim in range(150):
        R_by = {}
        for d in range(8):
            base = np.vstack([rng.permutation(3) + 1.0 for _ in range(7)])
            R_by[f"d{d}"] = np.repeat(base[None], 20, axis=0)
        ps.append(an.h1_permutation_test(R_by, 400, sim)["p"])
    assert np.mean(np.array(ps) <= 0.05) <= 0.10


# --- H2 -----------------------------------------------------------------------------------------

def test_h2_dataset_level_aggregation_and_orientation():
    spec = decided_spec()
    res = an.h2_analysis(make_full(n_inst=10), EXPL, M6, spec)
    assert len(res["datasets"]) == 8 and len(res["blocks"]) == 8 * 4 * 5 * 4
    assert res["omnibus"]["n"] == 8 and len(res["pairs"]) == 15
    # the shared instance trend is oriented consistently, so every oriented pair agrees perfectly
    assert res["omnibus"]["mean"] == pytest.approx(1.0)
    more = an.h2_analysis(make_full(n_inst=40), EXPL, M6, spec)
    assert more["omnibus"]["n"] == 8                                         # instances are not units


def test_sign_flip_exact_small_cases():
    assert an.sign_flip_p([1.0, 2.0, 3.0]) == pytest.approx(1 / 8)
    assert an.sign_flip_p([1.0, -1.0]) == pytest.approx(3 / 4)
    v = np.array([0.3, 0.1, -0.05, 0.2, 0.25, 0.15, 0.05, 0.4])
    assert len(list(itertools.product([1, -1], repeat=8))) == 256
    assert 1 / 256 <= an.sign_flip_p(v) <= 1


def test_holm_matches_statsmodels_and_families_are_separate():
    from statsmodels.stats.multitest import multipletests
    p = [0.01, 0.04, 0.03, 0.2, 0.002]
    assert an.holm(p) == pytest.approx(list(multipletests(p, method="holm")[1]))
    assert math.isnan(an.holm([0.03, math.nan, 0.01])[1])                          # NaN stays NaN
    res = an.h2_analysis(make_full(noise=0.5), EXPL, M6, decided_spec())
    assert res["pairs"]["p_holm15"].tolist() == pytest.approx(an.holm(res["pairs"]["p_t"].tolist()))


# --- degenerate M4 --------------------------------------------------------------------------------

def test_degenerate_m4_primary_retention_and_exploratory_exclusion():
    deg = {("d0", "rf", 1, "shap", i) for i in range(6)} | {("d1", "rf", 1, "lime", 0)}
    full = make_full(degenerate=deg)
    prim = an.block_means(full, M6).set_index(an.BLOCK + ["explainer"])
    excl = an.block_means(full, M6, exclude_degenerate_m4=True).set_index(an.BLOCK + ["explainer"])
    assert prim.loc[("d0", "rf", 1, "shap"), "m4_corr"] == pytest.approx(0.0)    # retained as 0.0
    assert math.isnan(excl.loc[("d0", "rf", 1, "shap"), "m4_corr"])              # missing, not 0
    assert excl.loc[("d0", "rf", 1, "shap"), "m1_deletion"] == prim.loc[("d0", "rf", 1, "shap"), "m1_deletion"]
    assert excl.loc[("d1", "rf", 1, "lime"), "m4_corr"] == pytest.approx(
        full.query("dataset=='d1' and model=='rf' and seed==1 and explainer=='lime' and instance>0")["m4_corr"].mean())
    sys_x = an.system_table(an.block_means(full, M6, exclude_degenerate_m4=True), make_roar())
    blocks, _ = an.h1_blocks(sys_x, ["shap", "lime", "occlusion"], an.load_spec()["h1"]["metrics"])
    hit = blocks.query("dataset=='d0' and model=='rf' and seed==1").iloc[0]
    assert hit["raters_missing"] == 1 and hit["pairs_defined"] == 15
    h2 = an.h2_blocks(full, EXPL, M6, exclude_degenerate_m4=True)
    row = h2.query("dataset=='d1' and model=='rf' and seed==1 and explainer=='lime'").iloc[0]
    assert row["n|m1_deletion|m4_corr"] == 5 and row["n|m1_deletion|m2_insertion"] == 6
    counts = an.degenerate_counts(full)
    assert counts["explainer"].set_index("explainer").loc["shap", "degenerate"] == 6


# --- sensitivity analyses -----------------------------------------------------------------------------

def test_baseline_sensitivity_substitutes_only_m1_m3_m6():
    spec = an.load_spec()
    full = make_full()
    full["m1_deletion_b2"] = 99.0
    full["m4_corr"] = 7.0
    sub = spec["baseline2"]["substitute"]
    assert set(sub) == {"m1_deletion", "m2_insertion", "m3_gap", "m6_sufficiency"}
    cols = [sub.get(m, m) for m in M6]
    b2 = an.block_means(full, cols).rename(columns={v: k for k, v in sub.items()})
    assert (b2["m1_deletion"] == 99.0).all() and (b2["m4_corr"] == 7.0).all()
    assert "m5_infidelity" in b2 and not any(c.endswith("_b2") for c in b2.columns)


def test_occlusion_m4_variants():
    spec = an.load_spec()
    m7, studied = spec["h1"]["metrics"], spec["h1"]["studied"]
    items = an.circularity_pair_items(m7, studied)
    j4 = m7.index("m4_corr")
    assert len(items) == 6 and all(j4 in k for k in items) and all(v == [0, 1] for v in items.values())
    sys_tab = an.system_table(an.block_means(make_full(), M6), make_roar())
    pw = an.h1_analysis(sys_tab, studied, m7, decided_spec(), test=False, pair_items=items)
    assert pw["spearman"]["mean"] == pytest.approx(1.0) and pw["blocks"]["kendall_w"].isna().all()
    drop = an.h1_analysis(sys_tab, studied, [m for m in m7 if m != "m4_corr"], decided_spec())
    assert drop["blocks"]["pairs_defined"].eq(15).all()


def test_winner_flips_and_shap_lime_reversals_with_ties():
    spec = an.load_spec()
    q = lambda d, m, s, e: {"shap": 2.0, "lime": 2.0, "occlusion": 1.0, "random": 0.0}[e]  # noqa: E731
    sys_tie = an.system_table(an.block_means(make_full(quality=q), M6), make_roar(quality=q))
    wf = an.winner_flips(sys_tie, spec["h1"]["studied"], spec["h1"]["metrics"])
    assert (wf["ties"] == 160).all() and (wf["flips"] == 0).all()
    sl, any_ = an.shap_lime_reversals(sys_tie, spec["h1"]["metrics"])
    assert (sl["tie_involved"] == 160).all() and (sl["strict_reversals"] == 0).all()
    def q2(d, m, s, e):
        return {"shap": 3.0, "lime": 2.0, "occlusion": 1.0, "random": 0.0}[e]
    full = make_full(quality=q2)
    full.loc[full["explainer"] == "lime", "m2_insertion"] = 10.0                   # LIME wins under M2 only
    sys_rev = an.system_table(an.block_means(full, M6), make_roar(quality=q2))
    sl, any_ = an.shap_lime_reversals(sys_rev, spec["h1"]["metrics"])
    pair = sl.query("metric_a=='m1_deletion' and metric_b=='m2_insertion'").iloc[0]
    assert pair["strict_reversals"] == 160 and any_["blocks_with_any_strict_reversal"] == 160
    wf = an.winner_flips(sys_rev, spec["h1"]["studied"], spec["h1"]["metrics"])
    assert wf.query("metric_a=='m1_deletion' and metric_b=='m2_insertion'").iloc[0]["flips"] == 160


def test_stability_benchmark_ten_seed_pairs():
    spec = an.load_spec()
    sys_tab = an.system_table(an.block_means(make_full(), M6), make_roar())
    st = an.stability_benchmark(sys_tab, spec["h1"]["studied"], spec["h1"]["metrics"])
    assert (st["cells"]["seed_pairs"] == 10).all() and len(st["datasets"]) == 8
    assert st["summary"]["mean"] == pytest.approx(1.0)


def test_decision_table_four_outcomes():
    assert an.decision(0.2, 0.6, 0.9, 0.05, 0.5) == "no evidence that the metrics share an order"
    assert an.decision(0.01, 0.6, 0.9, 0.05, 0.5) == "the metrics broadly agree"
    assert an.decision(0.01, 0.1, 0.4, 0.05, 0.5) == "the metrics agree only weakly"
    assert an.decision(0.01, 0.4, 0.6, 0.05, 0.5) == "agreement present, strength not determined"


# --- synthetic ground truth ---------------------------------------------------------------------------

def test_synthetic_reference_agreement():
    res = an.synthetic_agreement(make_synth(), EXPL, M6)
    assert len(res["blocks"]) == 20 * 6 and np.allclose(res["blocks"]["spearman_with_reference"], 1.0)
    ref = res["reference"].iloc[0]
    assert (ref["rank_shap"], ref["rank_random"]) == (1.0, 4.0)
    rev = {"shap": 0.0, "lime": 1.0, "occlusion": 2.0, "random": 3.0}
    res = an.synthetic_agreement(make_synth(metric_quality=rev), EXPL, M6)
    assert np.allclose(res["blocks"]["spearman_with_reference"], -1.0)
    three = an.synthetic_agreement(make_synth(), ["shap", "lime", "occlusion"], M6)
    assert "rank_random" not in three["reference"]


# --- validation, manifest, report and the run guard --------------------------------------------------

def test_manifest_validation_detects_missing_and_altered(tmp_path):
    raw = tmp_path / "raw"
    (raw / "full").mkdir(parents=True)
    rows = []
    for name in ("a", "b"):
        p = raw / "full" / f"{name}.jsonl.gz"
        p.write_bytes(name.encode())
        rows.append({"path": f"full/{name}.jsonl.gz", "sha256": hashlib.sha256(name.encode()).hexdigest()})
    assert an.check_manifest(rows, raw)["manifest_rows"] == 2
    (raw / "full" / "a.jsonl.gz").write_bytes(b"x")
    with pytest.raises(an.ValidationError, match="hash mismatch"):
        an.check_manifest(rows, raw)
    (raw / "full" / "b.jsonl.gz").unlink()
    with pytest.raises(an.ValidationError, match="missing"):
        an.check_manifest(rows, raw)
    with pytest.raises(an.ValidationError, match="duplicate"):
        an.check_manifest(rows + rows[:1], raw)
    with pytest.raises(an.ValidationError, match="1 missing"):
        an.check_manifest([], raw, expected={"full": {"full/a.jsonl.gz"}})


def test_structural_validation():
    cfg = {"dataset": [{"key": d} for d in DATASETS], "seeds": SEEDS, "n_instances": 6,
           "synthetic": {"generators": ["additive", "interaction"], "correlation": [0.0, 0.5], "n_instances": 5}}
    full, roar, synth = make_full(), make_roar(), make_synth()
    counts = an.validate(full, roar, synth, cfg, an.load_spec())
    assert counts["full_blocks"] == 160 and counts["m4_degenerate_rows"] == 0
    bad = full.copy()
    bad.loc[bad.index[0], "instance"] = 99                                         # misaligned instances
    with pytest.raises(an.ValidationError, match="do not share"):
        an.validate(bad, roar, synth, cfg, an.load_spec())
    with pytest.raises(an.ValidationError, match="roar"):
        an.validate(full, roar.iloc[:-1], synth, cfg, an.load_spec())


def test_report_and_outputs_are_deterministic(tmp_path):
    full, roar, synth = make_full(noise=0.3, seed=2), make_roar(), make_synth()
    outs = []
    for k in ("a", "b"):
        an.run_analysis(full, roar, synth, decided_spec(perms=1000), tmp_path / k, tmp_path / k / "R.md", {"fixture": "yes"})
        outs.append({p.relative_to(tmp_path / k): p.read_bytes() for p in sorted((tmp_path / k).rglob("*")) if p.is_file()})
    assert outs[0] == outs[1]
    names = {str(p) for p in outs[0]}
    for want in ("confirmatory/h1_summary.csv", "confirmatory/h2_pairs.csv", "confirmatory/multiplicity_h1_h2.csv",
                 "sensitivity/winner_flips.csv", "exploratory/h1_m4_excluded.csv", "synthetic/four_by_metric.csv",
                 "figures/fig_g1_h1_datasets.svg", "R.md"):
        assert want in names
    report = outs[0][Path("R.md")].decode()
    assert "Table R1." in report and "Table R11." in report and "Figure R3" in report


def test_no_premature_analysis(monkeypatch, capsys):
    repo_spec = an.load_spec()
    assert an.check_spec_decided(repo_spec) == []                                    # O1-O3 decided (11.11)
    assert (repo_spec["h1"]["h1_decision_p"], repo_spec["h1"]["circularity_variant"],
            repo_spec["variance"]["status"]) == ("raw", "drop_m4_rater", "OMITTED")
    monkeypatch.setattr(an, "read_manifest", lambda *a, **k: pytest.fail("frozen data read"))
    assert an.main(["--run"]) == 2                                                   # no authorization
    assert an.main(["--run", "--authorized", "   "]) == 2                            # blank authorization
    assert "refused" in capsys.readouterr().err
    undecided = copy.deepcopy(repo_spec)
    undecided["h1"]["h1_decision_p"] = an.UNDECIDED
    undecided["variance"]["status"] = "STOPPED"
    monkeypatch.setattr(an, "load_spec", lambda: undecided)
    assert an.main(["--run", "--authorized", "someone"]) == 2                        # spec not decided
    assert set(an.check_spec_decided(undecided)) == {"h1_decision_p", "variance.status must be OMITTED (11.11)"}


def test_dataset_gate_rule():
    rule = {"auc_low": 0.65, "auc_high": 0.98, "min_models_in_range": 2}
    ok = gate.gate_row("x", {"logreg": 0.65, "rf": 0.98, "xgb": 0.99, "mlp": 0.60}, rule)
    assert (ok["models_in_range"], ok["passes"], ok["retained"]) == (2, 1, 1)       # bounds inclusive
    bad = gate.gate_row("y", {"logreg": 0.99, "rf": 0.99, "xgb": 0.99, "mlp": 0.64}, rule)
    assert (bad["passes"], bad["retained"]) == (0, 1) and "retained" in bad["note"]


def test_planned_claims_resolve_to_one_number(tmp_path):
    """RCA-001: every planned claim of CLAIMS_PLAN.toml reads exactly one numeric cell of the outputs."""
    import tomllib
    plan = tomllib.loads((SCRIPTS.parent / "docs/reports/paper_g/CLAIMS_PLAN.toml").read_text(encoding="utf-8"))
    assert plan["meta"]["status"].startswith("planned; not verified")
    an.run_analysis(make_full(noise=0.3), make_roar(), make_synth(), decided_spec(perms=500),
                    tmp_path / "analysis", tmp_path / "R.md", {})
    gate_csv = tmp_path / "diagnostics" / "dataset_gate.csv"
    gate_csv.parent.mkdir()
    pd.DataFrame([gate.gate_row(d, {m: 0.8 for m in lib.MODELS}, {"auc_low": 0.65, "auc_high": 0.98,
                                                                 "min_models_in_range": 2})
                  for d in ["phoneme", "compas"]]).rename(columns={}).to_csv(gate_csv, index=False)
    ids = [c["id"] for c in plan["planned"]]
    assert len(ids) == len(set(ids)) and all(i.startswith("paper_g.") for i in ids)
    for c in plan["planned"]:
        df = pd.read_csv(tmp_path / c["artifact"])
        rows = df if c["value"] == "*" else df[df[c["key"]].astype(str) == c["value"]]
        assert len(rows) == 1, c["id"]
        assert math.isfinite(float(rows.iloc[0][c["column"]])), c["id"]


# --- O1-O3 (ANALYSIS_PLAN.md 11.11) ----------------------------------------------------------------

def test_o1_raw_classification_and_holm_conclusion_can_differ():
    # H1 raw p 0.03 and H2 p 0.04: Holm gives 0.06 for H1, so the adjusted conclusion is "no evidence"
    adj = an.holm([0.03, 0.04])
    assert adj == pytest.approx([0.06, 0.06])
    both = an.h1_conclusions(0.03, adj[0], 0.6, 0.9, 0.05, 0.5)
    assert both == {"classification_raw_p": "the metrics broadly agree",
                    "conclusion_holm_p": "no evidence that the metrics share an order", "differ": True}
    same = an.h1_conclusions(0.001, 0.002, 0.1, 0.4, 0.05, 0.5)
    assert same["differ"] is False and same["classification_raw_p"] == "the metrics agree only weakly"


def test_o1_outputs_keep_raw_and_adjusted(tmp_path):
    res = an.run_analysis(make_full(noise=0.4, seed=5), make_roar(), make_synth(), decided_spec(perms=500),
                          tmp_path / "a", tmp_path / "R.md", {})
    dec = pd.read_csv(tmp_path / "a/confirmatory/h1_decision.csv")
    assert list(dec["basis"]) == ["decision table (section 4.4), raw permutation p",
                                  "multiplicity-adjusted (Holm over H1 and H2)"]
    mult = pd.read_csv(tmp_path / "a/confirmatory/multiplicity_h1_h2.csv")
    assert dec["p"].iloc[0] == pytest.approx(mult["p_raw"].iloc[0], rel=1e-5)
    assert dec["p"].iloc[1] == pytest.approx(mult["p_holm"].iloc[0], rel=1e-5)
    assert mult["p_raw"].notna().all()
    assert mult["p_holm"].tolist() == pytest.approx(an.holm(mult["p_raw"].tolist()), rel=1e-5)
    h1 = res["h1"]["spearman"]
    assert res["both"]["classification_raw_p"] == an.decision(res["mult"]["p_raw"].iloc[0], h1["lo"], h1["hi"], 0.05, 0.5)
    assert res["both"]["conclusion_holm_p"] == an.decision(res["mult"]["p_holm"].iloc[0], h1["lo"], h1["hi"], 0.05, 0.5)
    assert list(dec["wording"]) == [res["both"]["classification_raw_p"], res["both"]["conclusion_holm_p"]]
    report = (tmp_path / "R.md").read_text()
    assert "raw permutation p" in report and "Multiplicity-adjusted conclusion" in report


def test_o2_six_metric_circularity_with_its_own_permutation_test(tmp_path):
    spec = decided_spec(perms=800)
    full, roar = make_full(noise=0.4, seed=9), make_roar()
    res = an.run_analysis(full, roar, make_synth(), spec, tmp_path / "a", tmp_path / "R.md", {})
    six = [m for m in spec["h1"]["metrics"] if m != "m4_corr"]
    assert len(six) == 6 and "m4_corr" not in six
    sys_tab = an.system_table(an.block_means(full, M6), roar)
    blocks, R_by = an.h1_blocks(sys_tab, spec["h1"]["studied"], six)
    assert (blocks["pairs_defined"] + blocks["pairs_undefined"] == 15).all()             # 6 raters, complete
    direct = an.h1_permutation_test(R_by, spec["h1"]["permutations"], spec["h1"]["permutation_seed"])
    assert res["h1_circ"]["permutation"] == direct                                        # same dataset-unit test
    assert res["h1_circ"]["spearman"]["mean"] == pytest.approx(an.t_interval(an.dataset_means(blocks, "mean_pairwise_spearman")["mean"])["mean"])
    sens = pd.read_csv(tmp_path / "a/sensitivity/h1_sensitivity.csv").set_index("analysis")
    row = sens.loc["H1 circularity: M4 removed for all explainers (six metrics)"]
    assert (row["metrics"], row["explainers"]) == (6, 3) and not math.isnan(row["p_permutation"])
    assert sens.loc["H1 four explainers", "explainers"] == 4 and sens.loc["H1 second baseline", "metrics"] == 7
    assert (tmp_path / "a/sensitivity/h1_circularity_datasets.csv").exists()
    # the primary H1 keeps all seven metrics
    assert res["h1"]["blocks"]["pairs_defined"].add(res["h1"]["blocks"]["pairs_undefined"]).eq(21).all()


def test_o3_no_variance_share_output(tmp_path):
    an.run_analysis(make_full(), make_roar(), make_synth(), decided_spec(perms=300),
                    tmp_path / "a", tmp_path / "R.md", {})
    files = [str(p.relative_to(tmp_path)) for p in tmp_path.rglob("*") if p.is_file()]
    assert not any("variance" in f or "art" in Path(f).stem.split("_") for f in files)
    report = (tmp_path / "R.md").read_text()
    assert "omitted, a protocol deviation" in report and "No variance-share result exists" in report
    assert "stopped pending" not in report
