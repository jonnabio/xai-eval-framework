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
