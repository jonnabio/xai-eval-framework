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
