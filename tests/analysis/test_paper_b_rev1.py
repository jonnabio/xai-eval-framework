"""Tests of the defensive parts of the Paper B revision 1 runner (cohort B2).

Covered: the model-call counter, crash-safe JSONL I/O and resume, admission control,
the quiet-host gate, the model hash check, the git-plumbing sync (no change to HEAD,
the index or the working tree; never a forced push), and instance selection.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))
import paper_b_lib as lib  # noqa: E402
import paper_b_sync as sync  # noqa: E402


# ---------------------------------------------------------------- call counter
def test_counter_counts_outermost_calls_and_rows_for_inherited_methods():
    from sklearn.ensemble import RandomForestClassifier

    class RF(RandomForestClassifier):      # fresh subclass: no global side effects
        pass

    X = np.random.default_rng(0).standard_normal((60, 3))
    y = (X[:, 0] > 0).astype(int)
    m = RF(n_estimators=5, random_state=0).fit(X, y)
    c = lib.CallCounter()
    wrapped = lib.install_counter(c, [RF])
    assert "RF.predict_proba" in wrapped and "RF.predict" in wrapped
    m.predict(X[:7])                      # predict calls predict_proba inside: one call
    assert (c.calls, c.rows) == (1, 7)
    m.predict_proba(X[:3])
    assert (c.calls, c.rows) == (2, 10)
    assert lib.install_counter(c, [RF]) == []        # never wrapped twice


def test_counter_wraps_available_if_descriptor():
    from sklearn.svm import SVC

    class S(SVC):
        pass

    X = np.random.default_rng(1).standard_normal((40, 2))
    y = (X[:, 1] > 0).astype(int)
    c = lib.CallCounter()
    lib.install_counter(c, [S])
    m = S(probability=True, random_state=0).fit(X, y)
    c.reset()
    m.predict_proba(X[:5])
    assert c.calls >= 1 and c.rows >= 5


# ---------------------------------------------------------------- crash-safe I/O
def test_jsonl_append_resume_and_truncated_line(tmp_path):
    p = tmp_path / "job.jsonl"
    lib.append_jsonl(p, {"instance_id": 1, "v": 0.5})
    lib.append_jsonl(p, {"instance_id": 2, "v": 0.6})
    with open(p, "a", encoding="utf-8") as fh:         # a crash mid-write
        fh.write('{"instance_id": 3, "v"')
    assert lib.done_keys(p) == {1, 2}
    lib.append_jsonl(p, {"instance_id": 3, "v": 0.7})  # resume starts a fresh line
    assert lib.done_keys(p) == {1, 2, 3}
    assert [r["instance_id"] for r in lib.read_jsonl(p)] == [1, 2, 3]


def test_jsonl_damaged_line_ending_with_newline_is_isolated(tmp_path):
    p = tmp_path / "job.jsonl"
    lib.append_jsonl(p, {"instance_id": 1})
    with open(p, "a", encoding="utf-8") as fh:
        fh.write('{"instance_id": 2, "v"\n')
    lib.append_jsonl(p, {"instance_id": 3})
    assert lib.done_keys(p) == {1, 3}


def test_atomic_write_never_leaves_partial_file(tmp_path):
    p = tmp_path / "state.json"
    lib.atomic_write_json(p, {"a": 1})
    lib.atomic_write_json(p, {"a": 2})
    assert json.loads(p.read_text()) == {"a": 2}
    assert not list(tmp_path.glob(".*tmp"))


# ---------------------------------------------------------------- admission and gate
BASE = dict(max_workers=4, reserve_gb=6.0, pause_below_gb=3.0, ac_power=True,
            disk_free_gb=100.0, disk_pause_gb=5.0, stop_requested=False)


def test_admission_admits_when_room():
    ok, why = lib.admission_decision(20.0, 3.0, 1, **BASE)
    assert ok and why == "ok"


@pytest.mark.parametrize("over, expect", [
    (dict(available_gb=8.0, expected_peak_gb=3.0, running=1), "reserve"),
    (dict(available_gb=2.0, expected_peak_gb=0.5, running=0), "RAM available"),
    (dict(available_gb=30.0, expected_peak_gb=1.0, running=4), "workers running"),
])
def test_admission_refuses(over, expect):
    args = {**BASE, **over}
    ok, why = lib.admission_decision(args.pop("available_gb"), args.pop("expected_peak_gb"),
                                     args.pop("running"), **args)
    assert not ok and expect in why


def test_admission_refuses_on_battery_disk_and_stop():
    assert not lib.admission_decision(30, 1, 0, **{**BASE, "ac_power": False})[0]
    assert not lib.admission_decision(30, 1, 0, **{**BASE, "disk_free_gb": 2.0})[0]
    assert not lib.admission_decision(30, 1, 0, **{**BASE, "stop_requested": True})[0]


def test_expected_peak_uses_most_specific_record_with_margin():
    peaks = {"adult|svm|shap": [2.0, 2.5, 3.0], "svm|shap": [9.0, 9.0]}
    assert lib.expected_peak_gb(peaks, "svm", "shap", "adult", 3.0) == pytest.approx(3.6)
    assert lib.expected_peak_gb(peaks, "svm", "shap", "spambase", 3.0) == pytest.approx(10.8)
    assert lib.expected_peak_gb({}, "rf", "lime", "adult", 3.0) == 3.0


def test_quiet_gate():
    assert lib.quiet_gate(3.0, 600.0, True, 10.0, 300.0, 0) == (True, "quiet")
    assert not lib.quiet_gate(3.0, 600.0, True, 10.0, 300.0, 2)[0]       # quality running
    assert not lib.quiet_gate(25.0, 600.0, True, 10.0, 300.0, 0)[0]      # busy host
    assert not lib.quiet_gate(3.0, 20.0, True, 10.0, 300.0, 0)[0]        # user active
    assert lib.quiet_gate(3.0, 20.0, True, 10.0, None, 0)[0]             # idle not required
    assert not lib.quiet_gate(3.0, 600.0, False, 10.0, 300.0, 0)[0]      # battery


# ---------------------------------------------------------------- model hash check
def test_model_hash_mismatch_stops(tmp_path, monkeypatch):
    import joblib
    from sklearn.linear_model import LogisticRegression
    models = tmp_path / "models"
    (models / "toy").mkdir(parents=True)
    f = models / "toy" / "logreg.joblib"
    joblib.dump(LogisticRegression().fit([[0], [1]], [0, 1]), f)
    monkeypatch.setattr(lib, "ROOT", tmp_path)
    monkeypatch.setattr(lib, "MANIFEST", models / "MANIFEST.csv")
    lib.write_manifest({("toy", "logreg"): {"dataset": "toy", "model": "logreg",
                                            "file": "models/toy/logreg.joblib",
                                            "sha256": lib.sha256_file(f)}})
    lib.load_model_checked("toy", "logreg")                     # passes
    f.write_bytes(f.read_bytes() + b"x")                        # the file changes
    with pytest.raises(lib.ModelHashMismatch):
        lib.load_model_checked("toy", "logreg")


# ---------------------------------------------------------------- sync by plumbing
def _git(cwd, *a):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True,
                          text=True).stdout.strip()


@pytest.fixture()
def repo(tmp_path):
    origin = tmp_path / "origin.git"
    work = tmp_path / "work"
    _git(tmp_path, "init", "--bare", "-q", str(origin))
    _git(tmp_path, "init", "-q", str(work))
    _git(work, "config", "user.email", "t@example.com")
    _git(work, "config", "user.name", "t")
    (work / "a.txt").write_text("a\n")
    _git(work, "add", "a.txt")
    _git(work, "commit", "-q", "-m", "init")
    _git(work, "remote", "add", "origin", str(origin))
    _git(work, "branch", "-M", "lane")
    _git(work, "push", "-q", "origin", "lane")
    return work, origin


def test_sync_commits_without_touching_head_index_or_tree(repo, tmp_path):
    work, _ = repo
    live = tmp_path / "live"
    (live / "results" / "q").mkdir(parents=True)
    (live / "results" / "q" / "x.jsonl").write_text('{"instance_id": 1}\n')
    (live / "results" / "q" / "x.heartbeat").write_text("{}")         # never copied
    (work / "a.txt").write_text("edited, not staged\n")               # author's work
    head = _git(work, "rev-parse", "HEAD")
    status = _git(work, "status", "--porcelain")
    c1 = sync.snapshot("runs", "exp/results", live, 50, "HEAD", cwd=work)
    assert c1
    assert _git(work, "rev-parse", "HEAD") == head
    assert _git(work, "status", "--porcelain") == status
    files = _git(work, "ls-tree", "-r", "--name-only", "runs").split("\n")
    assert "exp/results/results/q/x.jsonl" in files
    assert not any(f.endswith(".heartbeat") for f in files)
    assert sync.snapshot("runs", "exp/results", live, 50, "HEAD", cwd=work) is None  # no change
    (live / "results" / "q" / "x.jsonl").write_text('{"instance_id": 1}\n{"instance_id": 2}\n')
    c2 = sync.snapshot("runs", "exp/results", live, 50, "HEAD", cwd=work)
    assert _git(work, "rev-parse", "runs^") == c1 and c2


def test_sync_push_never_forces(repo, tmp_path):
    work, origin = repo
    live = tmp_path / "live"
    (live / "results").mkdir(parents=True)
    (live / "results" / "r.jsonl").write_text("{}\n")
    sync.snapshot("runs", "p", live, 50, "HEAD", cwd=work)
    assert sync.push("runs", "origin", cwd=work)[0]
    # Another machine pushes a different history to the same branch.
    other = tmp_path / "other"
    _git(tmp_path, "clone", "-q", "-b", "lane", str(origin), str(other))
    _git(other, "config", "user.email", "o@example.com")
    _git(other, "config", "user.name", "o")
    (other / "b.txt").write_text("b\n")
    _git(other, "add", "b.txt")
    _git(other, "commit", "-q", "-m", "other")
    _git(other, "push", "-q", "-f", "origin", "HEAD:runs")
    remote_head = _git(other, "rev-parse", "HEAD")
    (live / "results" / "r.jsonl").write_text("{}\n{}\n")
    sync.snapshot("runs", "p", live, 50, "HEAD", cwd=work)
    ok, _out = sync.push("runs", "origin", cwd=work)
    assert not ok                                                   # refused, not forced
    assert _git(work, "ls-remote", "origin", "refs/heads/runs").split()[0] == remote_head


def test_sync_skips_oversized_files(tmp_path):
    live = tmp_path / "live"
    (live / "results").mkdir(parents=True)
    (live / "results" / "big.jsonl").write_bytes(b"x" * (2 * 2**20))
    (live / "results" / "ok.jsonl").write_text("{}\n")
    files, skipped = sync.collect(live, max_mb=1)
    assert [d for _, d in files] == ["results/ok.jsonl"]
    assert len(skipped) == 1


# ---------------------------------------------------------------- instance selection
def test_select_instances_is_stratified_and_deterministic():
    from sklearn.linear_model import LogisticRegression
    rng = np.random.default_rng(3)
    X = rng.standard_normal((800, 4))
    y = (X[:, 0] + 0.8 * rng.standard_normal(800) > 0).astype(int)
    m = LogisticRegression().fit(X[:400], y[:400])
    data = {"X_test": X[400:], "y_test": y[400:], "feature_names": list("abcd")}
    a = lib.select_instances(m, data, seed=11, per_stratum=10)
    b = lib.select_instances(m, data, seed=11, per_stratum=10)
    assert list(a["original_index"]) == list(b["original_index"])
    counts = a["quadrant"].value_counts().to_dict()
    assert all(counts.get(q, 0) <= 10 for q in lib.STRATA)
    first = lib.first_per_stratum(a, 2)
    assert len(first) == sum(min(2, counts.get(q, 0)) for q in lib.STRATA)


def test_instance_seed_is_stable_and_distinct():
    s1 = lib.instance_seed(11, "adult", "rf", "lime", 5)
    assert s1 == lib.instance_seed(11, "adult", "rf", "lime", 5)
    assert s1 != lib.instance_seed(11, "adult", "rf", "lime", 6)
    assert 0 <= s1 < 2**32


def test_cohort_config_is_complete():
    cfg = lib.config()
    assert set(cfg["datasets"]) == {"adult", "breast_cancer", "german_credit", "diabetes",
                                    "spambase", "phishing", "connect4"}
    assert set(cfg["explainers"]) >= {"shap", "lime", "lime_full", "anchors", "dice"}
    assert cfg["cohort"]["split_seed"] == 42
    assert cfg["resources"]["worker_cap_gb"] > cfg["resources"]["default_peak_gb"]


def test_config_hash_covers_design_only(tmp_path):
    a, b, c, d = (tmp_path / f"{n}.toml" for n in "abcd")
    a.write_bytes(b"[x]\ny = 1\n[sync]\nevery_minutes = 15\n")
    b.write_bytes(b"# comment\r\n[x]\r\ny = 1\r\n[sync]\r\nevery_minutes = 5\r\n")
    c.write_bytes(b"[x]\ny = 1\n[resources]\nmax_workers = 2\n")
    d.write_bytes(b"[x]\ny = 2\n")
    assert lib.config_hash(a) == lib.config_hash(b) == lib.config_hash(c)
    assert lib.config_hash(a) != lib.config_hash(d)


def test_stuck_at_startup_only_without_any_heartbeat():
    assert lib.stuck_at_startup(False, born=0, now=2000, limit_s=1800)
    assert not lib.stuck_at_startup(False, born=0, now=100, limit_s=1800)
    # A job that reported heartbeats and removed its file at the end is finishing, not stuck.
    assert not lib.stuck_at_startup(True, born=0, now=5000, limit_s=1800)


# ---------------------------------------------------------------- analysis (WP6)
import paper_b_analyze as an  # noqa: E402


def test_holm_matches_hand_computation_and_keeps_order():
    adj = an.holm([0.01, 0.04, 0.03, float("nan")])
    assert adj[0] == pytest.approx(0.03)
    assert adj[2] == pytest.approx(0.06)
    assert adj[1] == pytest.approx(0.06)          # monotone: max(0.04*1, 0.06)
    assert np.isnan(adj[3])


def test_hodges_lehmann_and_rank_biserial():
    assert an.hodges_lehmann(np.array([1.0, 2.0, 3.0])) == pytest.approx(2.0)
    assert an.rank_biserial(np.array([1.0, 2.0, 3.0])) == pytest.approx(1.0)
    assert an.rank_biserial(np.array([-1.0, -2.0])) == pytest.approx(-1.0)
    # ranks of |d| = 1,2,3,4 -> R+ = 2+4 = 6, R- = 1+3 = 4 -> (6-4)/10
    assert an.rank_biserial(np.array([-1.0, 2.0, -3.0, 4.0])) == pytest.approx(0.2)
    assert an.rank_biserial(np.array([0.0, 0.0])) != an.rank_biserial(np.array([0.0, 0.0]))


def test_nemenyi_cd_and_dz():
    assert an.nemenyi_cd(4, 25) == pytest.approx(2.569 * (4 * 5 / 150) ** 0.5)
    with pytest.raises(ValueError):
        an.nemenyi_cd(9, 10)
    assert an.d_z(np.array([1.0, 1.0])) != an.d_z(np.array([1.0, 1.0]))   # SD 0 -> NaN


def _synthetic(effect: float, seed: int = 0):
    import pandas as pd
    rng = np.random.default_rng(seed)
    recs = []
    for m in ["logreg", "rf", "xgb", "svm", "mlp"]:
        for s in [11, 22, 33, 44, 55]:
            for i in range(20):
                base = rng.normal(0.5, 0.1)
                for e in ["shap", "lime_full", "lime", "anchors", "dice"]:
                    shift = effect if e == "shap" else 0.0
                    recs.append({"dataset": "adult", "model": m, "seed": s, "explainer": e,
                                 "instance_id": i, "stability": base + shift + rng.normal(0, .05),
                                 "fidelity": base + shift + rng.normal(0, .05),
                                 "faithfulness_gap": base + shift + rng.normal(0, .05),
                                 "sparsity": rng.uniform(), "all_zero": False,
                                 "stability_zero_vectors": 0})
    return pd.DataFrame(recs)


def test_primary_effects_recover_a_known_effect_and_holm_family():
    import pandas as pd
    q = _synthetic(0.2)
    df = an.primary_effects(q, pd.DataFrame())
    conf = df[df.confirmatory]
    assert len(conf) == 9                          # 3 endpoints x 3 contrasts, no timing yet
    assert conf["estimate"].between(0.17, 0.23).all()
    assert (conf["ci_lo"] > 0).all() and (conf["p_holm"] < 1e-6).all()
    assert (conf["cells_positive"] == 25).all()
    assert (conf["method"] == "mixedlm").all()     # never a silent fallback
    assert conf["var_model"].notna().all()
    assert df[~df.confirmatory]["p_holm"].isna().all()
    fr = an.friedman(q)
    assert set(fr["endpoint"]) == {"stability", "fidelity", "faithfulness_gap"}
    assert (fr["rank_shap"] == 1.0).all()


def test_primary_effects_null_effect_is_not_significant():
    import pandas as pd
    df = an.primary_effects(_synthetic(0.0, seed=3), pd.DataFrame())
    conf = df[df.confirmatory]
    assert (conf["p_holm"] > 0.01).all()
    assert ((conf["ci_lo"] < 0) & (conf["ci_hi"] > 0)).mean() >= 0.8


def test_cluster_bootstrap_resamples_whole_clusters():
    import pandas as pd
    df = pd.DataFrame({"c": ["a"] * 10 + ["b"] * 10, "v": [0.0] * 10 + [1.0] * 10})
    lo, hi = an.cluster_bootstrap_ci(df, "v", "c", reps=2000)
    assert lo == pytest.approx(0.0) and hi == pytest.approx(1.0)


# ---------------------------------------------------------------- auxiliary studies (WP2b, WP4, WP5)
def test_onehot_groups_split_numeric_and_categorical():
    names = ["age", "hours-per-week", "sex_F", "sex_M", "race_A", "race_B", "race_C"]
    X = np.array([[0.3, -1.2, 1, 0, 1, 0, 0], [-0.5, 0.4, 0, 1, 0, 1, 0],
                  [1.1, 0.9, 1, 0, 0, 0, 1]], float)
    num, groups = lib.onehot_groups(names, X)
    assert num == [0, 1]
    assert groups == {"sex": [2, 3], "race": [4, 5, 6]}


def test_onehot_groups_underscores_and_shared_numeric_prefixes():
    """R1-m13: names and categories with underscores (Phishing, German Credit) and numeric
    columns sharing a prefix (Spambase) were mis-grouped by a first-underscore split."""
    names = ["word_freq_make", "word_freq_all",                       # numeric, shared prefix
             "having_IP_Address_-1", "having_IP_Address_1",           # underscores in the name
             "credit_amount",                                         # numeric, prefix 'credit'
             "credit_history_all_paid", "credit_history_critical",    # underscore in a category
             "a_x", "a_y", "a_b_x", "a_b_y"]                          # features 'a' and 'a_b'
    X = np.array([[0.2, -0.1, 1, 0, 0.7, 1, 0, 1, 0, 0, 1],
                  [-0.4, 1.3, 0, 1, -1.1, 0, 1, 0, 1, 1, 0],
                  [0.9, 0.0, 1, 0, 0.2, 1, 0, 1, 0, 1, 0]], float)
    num, groups = lib.onehot_groups(names, X)
    assert num == [0, 1, 4]
    assert groups == {"having_IP_Address": [2, 3], "credit_history": [5, 6],
                      "a": [7, 8], "a_b": [9, 10]}


def test_onehot_groups_on_the_cohort_datasets():
    """The frozen cohort encodings: groups equal the source categorical features."""
    expected = {"adult": 8, "breast_cancer": 0, "diabetes": 0, "spambase": 0, "connect4": 42,
                "german_credit": 13, "phishing": 30}
    for d, n in expected.items():
        try:
            data = lib.load_dataset(d)
        except FileNotFoundError:
            pytest.skip(f"{d} not prepared on this machine")
        num, groups = lib.onehot_groups(data["feature_names"], data["X_train"])
        assert len(groups) == n, (d, sorted(groups))
        X = data["X_train"]
        for idx in groups.values():
            assert np.all(X[:, idx].sum(axis=1) == 1)
        assert len(num) + sum(map(len, groups.values())) == X.shape[1]


def test_valid_perturbation_keeps_one_hot_rows_valid():
    names = ["age", "sex_F", "sex_M", "race_A", "race_B", "race_C"]
    X = np.array([[0.1, 1, 0, 1, 0, 0], [0.3, 0, 1, 0, 1, 0], [0.2, 0, 1, 0, 0, 1]], float)
    m = lib.ValidStabilityMetric(5, 0.1, X, names, p_resample=1.0)
    np.random.seed(0)
    for _ in range(50):
        z = m.perturb(X[0])
        assert z[1:3].sum() == 1 and z[3:6].sum() == 1          # exactly one category each
        assert set(np.unique(z[1:])) <= {0.0, 1.0}
    out = m.compute(None, model=None, data=X[0],
                    explainer_func=lambda _m, d: {"feature_importance": d[0]})
    assert 0 < out["cosine_similarity_mean"] <= 1 and out["n_iterations"] == 5


def test_explainer_model_restriction_and_main_job_count_unchanged():
    cfg = lib.config(lib.MAIN_CONFIG)
    assert len(lib.all_quality_jobs(cfg)) == 575
    c = {"datasets": {"adult": {}}, "seeds": {"adult": [1], "other": [1]},
         "models": {"rf": {}, "svm": {}},
         "explainers": {"a": {}, "t": {"models": ["rf"]}}}
    assert sorted(lib.all_quality_jobs(c)) == [("adult", "rf", 1, "a"), ("adult", "rf", 1, "t"),
                                               ("adult", "svm", 1, "a")]


def test_study_configs_are_isolated_from_the_main_cohort():
    code = ("import sys; sys.path.insert(0, 'scripts'); import paper_b_lib as l; "
            "print(l.VARIANT, l.LIVE.name, l.config_hash())")
    main = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True,
                          env={k: v for k, v in __import__("os").environ.items()
                               if k != "PAPER_B_CONFIG"}).stdout.split()
    env = dict(__import__("os").environ,
               PAPER_B_CONFIG=str(ROOT / "experiments/exp_b_rev1/studies/sweep.toml"))
    sweep = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True,
                           env=env).stdout.split()
    assert main[0] == "paper_b_rev1_live"            # VARIANT empty -> first token is LIVE
    assert sweep[:2] == ["sweep", "paper_b_rev1_sweep_live"]
    assert sweep[2] != main[1]


# ---------------------------------------------------------------- post-hoc controls (WP4)
import paper_b_posthoc as ph  # noqa: E402


def test_posthoc_measures():
    a, b = np.array([3.0, 2.0, 1.0, 0.0]), np.array([3.0, 1.0, 2.0, 0.0])
    assert ph.cosine(a, np.zeros(4)) == 0.0                     # main-protocol convention
    assert ph.topk_jaccard(a, a, k=2) == 1.0
    assert ph.topk_jaccard(a, b, k=2) == pytest.approx(1 / 3)
    assert ph.spearman_abs(a, a) == pytest.approx(1.0)
    top, ent = ph.concentration(np.array([1.0, 0, 0, 0]), k=1)
    assert top == 1.0 and ent == pytest.approx(0.0)
    top, ent = ph.concentration(np.ones(4), k=2)
    assert top == pytest.approx(0.5) and ent == pytest.approx(1.0)


def test_grouped_masking_masks_whole_groups():
    names = ["age", "education-num", "education_A", "education_B", "sex_F", "sex_M"]
    X = np.array([[1.0, 2.0, 1, 0, 1, 0], [3.0, 4.0, 0, 1, 0, 1]])
    groups = ph.mask_groups(names, "adult", X)
    assert sorted(map(sorted, groups)) == [[1, 2, 3], [4, 5]]   # education pair merged
    mean = X.mean(0)
    z = ph.masked(X[0], [1], "grouped_mean", X, mean, groups, np.random.default_rng(0))
    assert np.allclose(z[[1, 2, 3]], mean[[1, 2, 3]]) and z[0] == 1.0 and z[4] == 1.0
    z = ph.masked(X[0], [1], "mean", X, mean, groups, np.random.default_rng(0))
    assert z[2] == 1.0                                          # ungrouped: one column only


def test_compressed_logs_are_deterministic_and_collected(tmp_path):
    import gzip
    import os
    live = tmp_path
    (live / "_logs").mkdir()
    log = live / "_logs" / "a.log"
    log.write_text("warning\n" * 1000, encoding="utf-8")
    out = sync.compress_logs(live) / "a.log.gz"
    first = out.read_bytes()
    os.utime(log, (out.stat().st_mtime + 5, out.stat().st_mtime + 5))   # "changed" log
    sync.compress_logs(live)
    assert out.read_bytes() == first                                   # same bytes, same blob
    assert gzip.decompress(first) == log.read_bytes()
    files, _ = sync.collect(live, max_mb=50)
    assert ("_logs/a.log.gz" in {d for _, d in files})


# ---------------------------------------------------------------- dashboard throttling check
def test_throttling_check_uses_medians_not_single_readings():
    import paper_b_dashboard as dash
    noisy = [32.4, 36.4, 33.5, 36.8, 52.1, 34.5, 34.3, 32.0, 31.3, 42.3, 33.8, 43.8]  # 6 workers
    b = dash.bench_summary(noisy)
    assert b["n"] == 12 and b["last"] <= 1.15 * b["first"]       # noise alone: no alarm
    zero = {"total": {"rows": 0, "failed": 0}}
    s = {"orchestrator": {}, "sync": {}, "timing": {"state": {}}, "now": 0,
         "passes": {"pilot": zero, "quality": zero}, "bench": dict(b, workers=6)}
    assert not any("Throttling" in w for w in dash.warnings(s))
    slow = noisy[:6] + [v * 1.4 for v in noisy[6:]]               # a real 40% slowdown
    s["bench"] = dict(dash.bench_summary(slow), workers=6)
    assert any("Throttling" in w for w in dash.warnings(s))
    assert dash.bench_summary([])["first"] is None

# ---------------------------------------------------------------- admission backfill (2026-11-07)
def _plan(cands, avail, running=0, maxw=6, stop=False, ac=True, disk=300.0):
    return lib.plan_admissions(cands, avail, running, maxw, reserve_gb=6.0, pause_below_gb=3.0,
                               ac_power=ac, disk_free_gb=disk, disk_pause_gb=5.0,
                               stop_requested=stop)


def test_admission_passes_over_a_job_that_does_not_fit():
    big, s1, s2 = ("adult", "mlp", 33, "anchors"), ("a", "svm", 33, "shap"), ("b", "rf", 33, "dice")
    start, why = _plan([(big, 4.9, False), (s1, 0.4, False), (s2, 0.4, False)], 8.6, running=3)
    assert start == [s1, s2] and "smaller jobs go first" in why          # no head-of-line stall


def test_admission_starts_a_large_job_alone_when_nothing_runs():
    big, s1 = ("adult", "mlp", 33, "anchors"), ("a", "svm", 33, "shap")
    start, why = _plan([(big, 4.9, False), (s1, 0.4, False)], 8.6, running=0)
    assert start == [big] and "started alone" in why                     # nothing joins it
    start, _ = _plan([(big, 6.0, False)], 8.6, running=0)
    assert start == []                                                   # would leave < 3 GB


def test_admission_hard_refusals_still_stop_the_scan():
    s1, s2 = ("a", "svm", 33, "shap"), ("b", "rf", 33, "dice")
    assert _plan([(s1, 0.4, False)], 20.0, stop=True)[0] == []
    assert _plan([(s1, 0.4, False)], 20.0, ac=False)[0] == []
    assert _plan([(s1, 0.4, False)], 20.0, disk=1.0)[0] == []
    assert _plan([(s1, 0.4, False)], 2.0)[0] == []                       # below the pause floor
    assert _plan([(s1, 0.4, False), (s2, 0.4, False)], 20.0, running=5) == ([s1], "ok")
    start, _ = _plan([(s1, 0.4, False), (s2, 0.4, False)], 20.0, running=1, maxw=2)
    assert start == [s1]


def test_admission_job_that_must_run_alone():
    lone, s1 = ("connect4", "mlp", 22, "anchors"), ("a", "svm", 33, "shap")
    start, _ = _plan([(lone, 2.0, True), (s1, 0.4, False)], 20.0, running=2)
    assert start == [s1]                                                 # it waits, others go
    start, _ = _plan([(lone, 2.0, True), (s1, 0.4, False)], 20.0, running=0)
    assert start == [lone]                                               # nothing joins it