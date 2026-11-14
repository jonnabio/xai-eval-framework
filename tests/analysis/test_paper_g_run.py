"""Paper G: shards, resume, status page and publisher (no network, no real dataset)."""
import gzip
import importlib.util
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

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
run = _load("paper_g_run")
status = _load("paper_g_status")
publish = _load("paper_g_publish")


@pytest.fixture
def cfg(tmp_path):
    c = lib.config()
    c = {**c, "run": {**c["run"], "work_dir": str(tmp_path / "work")},
         "synthetic": {**c["synthetic"], "n_instances": 3}}
    return c


def _synthetic_shard(cfg):
    return run.shards("synthetic", cfg)[0]


def test_shard_counts_follow_the_plan(cfg):
    assert len(run.shards("full", cfg)) == 8 * 4 * 5
    assert len(run.shards("roar", cfg)) == 8 * 4 * 5
    assert len(run.shards("synthetic", cfg)) == 2 * 2 * 5
    assert len(run.shards("pilot", cfg)) == 4


def test_a_shard_writes_rows_then_its_done_marker(cfg):
    sh = _synthetic_shard(cfg)
    assert run.state(sh, cfg) == "todo"
    summary = run.run_shard(sh, cfg, "abc123")
    assert run.state(sh, cfg) == "done"
    assert summary["rows"] == 3 * len(lib.EXPLAINERS) and summary["failed_rows"] == 0
    with gzip.open(run.shard_path(sh, cfg, ".jsonl.gz"), "rt", encoding="utf-8") as fh:
        rows = [json.loads(line) for line in fh]
    assert {r["commit"] for r in rows} == {"abc123"}
    assert all("true_attr" in r and "spearman_truth" in r for r in rows)
    assert (run.work_dir(cfg) / "logs" / "synthetic" / f"{run.shard_name(sh)}.log").exists()


def test_a_shard_that_raises_is_marked_failed_and_retried(cfg, monkeypatch):
    sh = _synthetic_shard(cfg)
    monkeypatch.setattr(run, "_rows_synthetic", lambda *a: (_ for _ in ()).throw(ValueError("boom")))
    result = run.run_shard(sh, cfg, "x")
    assert result["failed"] and run.state(sh, cfg) == "failed"
    assert not run.shard_path(sh, cfg, ".jsonl.gz.part").exists()
    monkeypatch.undo()
    run.run_shard(sh, cfg, "x")
    assert run.state(sh, cfg) == "done"
    assert not run.shard_path(sh, cfg, ".failed").exists()


def test_status_page_shows_progress_and_failures_but_no_metric(cfg):
    sh = _synthetic_shard(cfg)
    run.run_shard(sh, cfg, "x")
    bad = run.shards("synthetic", cfg)[1]
    p = run.shard_path(bad, cfg, ".failed")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"error": "ValueError: boom", "at": "2026-11-14T00:00:00Z"}))
    page = status.build(cfg)
    assert "| synthetic | 1 | 1 | 18 | 20 |" in page
    assert "ValueError: boom" in page
    for metric in list(lib.INSTANCE_METRICS) + ["m7_roar", "spearman_truth"]:
        assert metric not in page


def test_stall_is_reported_once(cfg):
    now = datetime(2026, 11, 14, 12, 0, tzinfo=timezone.utc)
    old = (now - timedelta(minutes=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
    beat = run.work_dir(cfg) / "heartbeat.json"
    beat.parent.mkdir(parents=True, exist_ok=True)
    beat.write_text(json.dumps({"stage": "full", "heartbeat": old, "todo": 5, "running": ["a"]}))
    seen = {}
    first = publish.events_due(cfg, seen, now)
    assert any("stalled" in m for m in first)
    assert not any("stalled" in m for m in publish.events_due(cfg, seen, now))


def test_failure_and_seed_events(cfg):
    for sh in [s for s in run.shards("synthetic", cfg) if s["seed"] == 42]:
        run.run_shard(sh, cfg, "x")
    seen = {}
    msgs = publish.events_due(cfg, seen, datetime.now(timezone.utc))
    assert any("seed 42 finished" in m for m in msgs)
    assert any("Stage **synthetic** started" in m for m in msgs)
    assert publish.events_due(cfg, seen, datetime.now(timezone.utc)) == []


def test_copy_shards_writes_manifest_with_checksums(cfg, tmp_path, monkeypatch):
    monkeypatch.setattr(publish, "RAW", tmp_path / "raw")
    sh = _synthetic_shard(cfg)
    run.run_shard(sh, cfg, "x")
    added = publish.copy_shards(cfg)
    assert added == [f"synthetic/{run.shard_name(sh)}.jsonl.gz"]
    manifest = (tmp_path / "raw" / "MANIFEST.csv").read_text(encoding="utf-8").splitlines()
    assert manifest[0].startswith("path,rows,failed_rows,sha256")
    assert publish.sha256(tmp_path / "raw" / added[0]) in manifest[1]
    assert publish.copy_shards(cfg) == []          # copied once only


def test_publisher_refuses_other_branches(monkeypatch, capsys):
    class R:
        stdout = "paper/g-metric-agreement\n"
        returncode = 0
    monkeypatch.setattr(publish, "git", lambda *a, **k: R())
    assert publish.cycle(push=False) == 2
    assert "refused" in capsys.readouterr().err


# --- RCA-004: published logs must reach git ------------------------------------------------

import shutil  # noqa: E402
import subprocess  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
UNRELATED_LOGS = ["logs/app.log", "outputs/analysis/other/logs/a.log", "experiments/exp_g/work/logs/x.log",
                  "docs/build.log"]


def _git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path, cfg, monkeypatch):
    """An isolated git repo on paper/g-runs with the real .gitignore and a pass-through lane guard."""
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q", "-b", publish.RUN_BRANCH)
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "user.name", "test")
    shutil.copy(REPO / ".gitignore", root / ".gitignore")
    guard = root / "scripts" / "pubs" / "check_lane.py"
    guard.parent.mkdir(parents=True)
    guard.write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "init")
    out = root / "outputs" / "analysis" / "paper_g"
    monkeypatch.setattr(lib, "ROOT", root)
    monkeypatch.setattr(lib, "OUT", out)
    monkeypatch.setattr(publish, "RAW", out / "raw")
    monkeypatch.setattr(publish, "LOGS", out / "logs")
    monkeypatch.setattr(lib, "config", lambda: cfg)
    # Logs as the run writes them: a pilot shard, a synthetic shard (real run) and the main log.
    work_logs = run.work_dir(cfg) / "logs"
    pilot = run.shards("pilot", cfg)[0]
    (work_logs / "pilot" / f"{run.shard_name(pilot)}.log").parent.mkdir(parents=True, exist_ok=True)
    (work_logs / "pilot" / f"{run.shard_name(pilot)}.log").write_text("pilot ok\n", encoding="utf-8")
    run.run_shard(_synthetic_shard(cfg), cfg, "x")
    (work_logs / "full_main.log").write_text("main\n", encoding="utf-8")
    for rel in UNRELATED_LOGS + ["docs/notes.md", "scripts/other.py"]:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text("x\n", encoding="utf-8")
    return root


def _committed(root):
    return set(_git(root, "ls-files").splitlines())


def test_publisher_commits_pilot_shard_and_main_logs(repo, cfg):
    assert publish.cycle(push=False) == 0
    files = _committed(repo)
    logs = {f for f in files if f.startswith("outputs/analysis/paper_g/logs/")}
    pilot = run.shard_name(run.shards("pilot", cfg)[0])
    synth = run.shard_name(_synthetic_shard(cfg))
    assert f"outputs/analysis/paper_g/logs/pilot/{pilot}.log" in logs
    assert f"outputs/analysis/paper_g/logs/synthetic/{synth}.log" in logs
    assert "outputs/analysis/paper_g/logs/full_main.log" in logs
    assert "outputs/analysis/paper_g/STATUS.md" in files


def test_unrelated_logs_stay_ignored_and_other_paths_unstaged(repo):
    assert publish.cycle(push=False) == 0
    files = _committed(repo)
    for rel in UNRELATED_LOGS:
        assert rel not in files
        assert subprocess.run(["git", "check-ignore", "-q", rel], cwd=repo).returncode == 0, rel
    new = files - {".gitignore", "scripts/pubs/check_lane.py"}
    assert new and all(f.startswith("outputs/analysis/paper_g/") for f in new)   # only the lane's output
    assert "docs/notes.md" not in files and "scripts/other.py" not in files


def test_published_paths_belong_to_the_paper_g_lane():
    lane = _load_lane_guard()
    registry = lane.load_registry()
    for rel in ["outputs/analysis/paper_g/logs/pilot/x/seed_1.log", "outputs/analysis/paper_g/logs/full_main.log",
                "outputs/analysis/paper_g/STATUS.md"]:
        assert lane.owner_of(rel, registry) == "paper-g", rel


def _load_lane_guard():
    spec = importlib.util.spec_from_file_location("check_lane", SCRIPTS / "pubs" / "check_lane.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_publisher_refuses_when_logs_would_be_silently_omitted(repo, capsys):
    gi = repo / ".gitignore"
    gi.write_text(gi.read_text(encoding="utf-8").split("# Paper G run logs (RCA-004)")[0], encoding="utf-8")
    head = _git(repo, "rev-parse", "HEAD")
    assert publish.cycle(push=False) == 3
    assert _git(repo, "rev-parse", "HEAD") == head                 # nothing committed
    assert _git(repo, "diff", "--cached", "--name-only") == ""      # nothing left staged
    captured = capsys.readouterr()
    assert "NOT published" in captured.out and "ignored by git" in captured.err
