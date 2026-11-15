"""Paper G dashboard: read-only monitoring (no network, no real dataset, no computation).

The pilot fixture copies the pilot's operational metadata of 2026-11-14 (shard times, peak
memory, heartbeat, log formats). Its .done files and shard logs carry a SENTINEL test AUC so
that every output can be checked for leaked metric values.
"""
import csv
import gzip
import importlib.util
import json
import sys
import threading
import time
import urllib.request
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
dash = _load("paper_g_dashboard")

SENTINEL = "0.987654321"
NOW = datetime(2026, 11, 14, 18, 0, tzinfo=timezone.utc)
PILOT = {  # model: (seconds, peak MiB, finished) as recorded by the pilot of 2026-11-14
    "logreg": (2.5, 473.4, "2026-11-14T16:06:38Z"), "rf": (7.5, 619.8, "2026-11-14T16:06:43Z"),
    "xgb": (2.0, 378.4, "2026-11-14T16:06:38Z"), "mlp": (27.9, 486.6, "2026-11-14T16:07:04Z")}


class Env:
    """Paths and stubs of one isolated dashboard world."""

    def __init__(self, root: Path, cfg: dict):
        self.root, self.cfg = root, cfg
        self.work = run.work_dir(cfg)
        self.out = root / "outputs" / "analysis" / "paper_g"
        self.git_out: dict[str, str] = {}
        self.units: dict[str, dict] = {"paper-g-publish.timer": {"ActiveState": "active"},
                                       "paper-g-publish.service": {"ActiveState": "inactive", "Result": "success"}}
        self.alive = False

    def done(self, stage, dataset, model, seed, seconds, peak, finished, rows=80):
        sh = {"stage": stage, "dataset": dataset, "model": model, "seed": seed}
        p = run.shard_path(sh, self.cfg, ".done")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"stage": stage, "dataset": dataset, "model": model, "seed": seed,
                                 "host": "jonnabio-Latitude-5450", "commit": "a1677fe26d78",
                                 "auc": float(SENTINEL), "n_groups": 14, "n_columns": 108,
                                 "meta": {"note": f"SENTINEL {SENTINEL}"}, "rows": rows,
                                 "failed_rows": 0, "seconds": seconds, "finished": finished,
                                 "peak_rss_mib": peak}))
        log = self.work / "logs" / stage / f"{dataset}/{model}/seed_{seed}.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(f"2026-11-14 10:06:36,380 INFO start {stage} {dataset}/{model}/seed_{seed} on h\n"
                       f"2026-11-14 10:06:40,462 INFO prepared: 9 train, test AUC {SENTINEL}\n")
        return sh

    def beat(self, **kw):
        b = {"stage": "pilot", "jobs": 6, "host": "jonnabio-Latitude-5450", "commit": "a1677fe26d78",
             "started": "2026-11-14T16:06:36Z", "heartbeat": "2026-11-14T16:07:04Z", "todo": 0,
             "running": [], "done": 4, "failed": 0, "free_memory_gib": 8.2, "pid": 60596}
        b.update(kw)
        (self.work / "heartbeat.json").write_text(json.dumps(b))

    def log(self, name, lines):
        p = self.work / "logs" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\n".join(lines) + "\n")

    def manifest(self, paths):
        p = self.out / "raw" / "MANIFEST.csv"
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["path", "rows", "failed_rows", "sha256", "host", "commit", "finished"])
            w.writeheader()
            for x in paths:
                w.writerow({"path": x, "rows": 80, "failed_rows": 0, "sha256": "0" * 64,
                            "host": "h", "commit": "a1677fe26d78", "finished": "t"})


@pytest.fixture
def env(tmp_path, monkeypatch):
    c = lib.config()
    cfg = {**c, "run": {**c["run"], "work_dir": str(tmp_path / "work")}}
    e = Env(tmp_path, cfg)
    (tmp_path / "experiments" / "exp_g").mkdir(parents=True)
    (tmp_path / "experiments" / "exp_g" / "host.json").write_text(json.dumps(
        {"hostname": "jonnabio-Latitude-5450", "cpu": "13th Gen Intel(R) Core(TM) i5-1335U", "ram_gib": 14.8}))
    monkeypatch.setattr(lib, "ROOT", tmp_path)
    monkeypatch.setattr(lib, "OUT", e.out)
    monkeypatch.setattr(lib, "config", lambda: cfg)
    monkeypatch.setattr(dash, "git", lambda *a: e.git_out.get(" ".join(a)))
    monkeypatch.setattr(dash, "systemd", lambda unit: e.units.get(unit, {}))
    monkeypatch.setattr(dash, "runner_alive", lambda pid: e.alive)
    monkeypatch.setattr(dash, "pool_memory", lambda pid: {"processes": 3, "rss_mib": 1500.0, "largest_mib": 600.0})
    e.git_out.update({"rev-parse --short=12 HEAD": "a1677fe26d78", "rev-parse --abbrev-ref HEAD": "paper/g-runs",
                      "rev-list --count refs/remotes/origin/paper/g-runs..HEAD": "0"})
    return e


def pilot(e: Env):
    """The pilot as it stood after 2026-11-14 16:21 UTC: 4 shards done and published."""
    for m, (sec, peak, fin) in PILOT.items():
        e.done("pilot", "adult", m, 42, sec, peak, fin)
    e.beat()
    e.log("pilot_main.log", [
        "pilot: 0 of 4 shards done; 4 to run with 6 jobs (commit a1677fe26d78)",
        "2026-11-14T16:06:38Z done adult/xgb/seed_42 (1/4, 2.0 s)",
        "2026-11-14T16:06:38Z done adult/logreg/seed_42 (2/4, 2.5 s)",
        "2026-11-14T16:06:43Z done adult/rf/seed_42 (3/4, 7.5 s)",
        "2026-11-14T16:07:04Z done adult/mlp/seed_42 (4/4, 27.9 s)",
        "pilot: finished; 4 done, 0 failed"])
    e.log("publish.log", [
        "2026-11-14T16:06:11.529569+00:00 published: 0 new shard(s); 0 event(s)",
        "2026-11-14T16:21:17.489565+00:00 published: 4 new shard(s); 2 event(s)",
        "2026-11-14T17:52:34.152629+00:00 published: 0 new shard(s); 0 event(s)"])
    (e.work / "events.json").write_text(json.dumps({"start:pilot": 1, "end:pilot": 1}))
    e.manifest([f"pilot/adult/{m}/seed_42.jsonl.gz" for m in PILOT])
    e.git_out["ls-files outputs/analysis/paper_g/logs"] = "\n".join(
        f"outputs/analysis/paper_g/logs/pilot/adult/{m}/seed_42.log" for m in PILOT)
    e.git_out["log -1 --format=%h %cI %s refs/remotes/origin/paper/g-runs"] = \
        "0f6939204 2026-11-14T17:52:35+00:00 data(paper-g): pilot snapshot 2026-11-14 17:52 (4/344)"


def outputs(s):
    return [dash.render_text(s), dash.render_html(s), json.dumps(s, default=str)]


# --- pilot acceptance ----------------------------------------------------------------------

def test_pilot_fixture_reports_the_completed_pilot(env):
    pilot(env)
    s = dash.gather(NOW)
    st = s["stages"]
    assert (st["pilot"]["done"], st["pilot"]["total"], st["pilot"]["failed"]) == (4, 4, 0)
    assert st["pilot"]["label"] == "completed"
    assert [(st[k]["done"], st[k]["total"], st[k]["label"]) for k in ("full", "roar", "synthetic")] == \
        [(0, 160, "not started"), (0, 160, "not started"), (0, 20, "not started")]
    shards = {sh["shard"]: sh for sh in st["pilot"]["shards"]}
    assert len(shards) == 4
    for m, (sec, peak, fin) in PILOT.items():
        sh = shards[f"adult/{m}/seed_42"]
        assert (sh["seconds"], sh["peak_rss_mib"], sh["finished"], sh["rows"]) == (sec, peak, fin, 80)
    assert st["pilot"]["peak_rss_mib"] == 619.8
    assert s["workers"] == [] and s["overall"]["running"] == 0
    assert s["runner"]["state"] == "idle"            # finished pilot: not stalled, not complete
    assert not any("STALLED" in w or "late" in w for w in s["warnings"])
    assert s["overall"]["done"] == 4 and s["overall"]["total"] == 344
    assert s["overall"]["elapsed_s"] == pytest.approx(29.0, abs=1)   # first shard start 16:06:35 -> 16:07:04, not to NOW
    assert "experiment complete" not in dash.render_html(s)
    assert s["warnings"] == []


def test_no_metric_value_reaches_any_output(env):
    pilot(env)
    s = dash.gather(NOW)
    for text in outputs(s) + [json.dumps(dash.heartbeat())]:
        assert SENTINEL not in text and "SENTINEL" not in text
        assert '"auc"' not in text and "n_groups" not in text and "AUC" not in text


# --- operational states (synthetic fixtures) ---------------------------------------------

def test_stage_not_started_is_not_inferred_from_finished_predecessors(env):
    pilot(env)
    s = dash.gather(NOW)
    assert s["stages"]["full"]["label"] == "not started"
    assert "<h3>full</h3>" not in dash.render_html(s)


def test_running_stage_with_pending_shards(env):
    pilot(env)
    env.alive = True
    env.done("full", "phoneme", "rf", 42, 300.0, 700.0, "2026-11-14T17:58:00Z")
    env.beat(stage="full", started="2026-11-14T17:50:00Z", heartbeat="2026-11-14T17:59:40Z",
             todo=150, running=["phoneme/logreg/seed_42", "phoneme/xgb/seed_42"], done=1)
    log = env.work / "logs" / "full" / "phoneme" / "logreg" / "seed_42.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("2026-11-14 11:55:00,000 INFO start full phoneme/logreg/seed_42 on h\n")
    s = dash.gather(NOW)
    assert s["runner"]["state"] == "running"
    assert s["stages"]["full"]["label"] == "running" and s["stages"]["full"]["done"] == 1
    assert [w["shard"] for w in s["workers"]] == ["phoneme/logreg/seed_42", "phoneme/xgb/seed_42"]
    assert s["workers"][1]["elapsed_s"] is None      # no log yet: not invented
    assert s["runner"]["jobs"] == 6 and len(s["runner"]["running"]) == 2
    assert s["stages"]["full"]["eta_h"] is not None
    cell = next(c for c in s["cells"]["full"] if (c["dataset"], c["model"]) == ("phoneme", "rf"))
    assert (cell["done_seeds"], cell["seeds"], cell["avg_s"], cell["left_s"]) == (1, 5, 300.0, 1200.0)
    assert s["overall"]["eta_h"] is None              # full has its own evidence; roar/synthetic not


def test_overall_eta_needs_evidence_from_every_unfinished_stage(env):
    pilot(env)
    env.done("full", "phoneme", "rf", 42, 300.0, 700.0, "2026-11-14T17:58:00Z")
    env.done("roar", "phoneme", "rf", 42, 100.0, 700.0, "2026-11-14T17:59:00Z")
    s = dash.gather(NOW)
    assert s["overall"]["eta_h"] is None              # synthetic has no finished shard yet
    env.done("synthetic", "additive_rho00", "known", 42, 60.0, 300.0, "2026-11-14T17:59:30Z")
    s = dash.gather(NOW)
    assert s["overall"]["eta_h"] == pytest.approx(sum(s["stages"][k]["eta_h"] for k in ("full", "roar", "synthetic")))


def test_shard_transition_is_seen_on_the_next_refresh(env):
    pilot(env)
    env.alive = True
    env.beat(stage="full", heartbeat="2026-11-14T17:59:50Z", todo=159, running=["phoneme/rf/seed_42"], done=0)
    assert dash.gather(NOW)["stages"]["full"]["done"] == 0
    env.done("full", "phoneme", "rf", 42, 300.0, 700.0, "2026-11-14T17:59:55Z")
    env.beat(stage="full", heartbeat="2026-11-14T17:59:56Z", todo=158, running=["phoneme/xgb/seed_42"], done=1)
    s = dash.gather(NOW)
    assert s["stages"]["full"]["done"] == 1 and s["workers"][0]["shard"] == "phoneme/xgb/seed_42"


def test_failed_shard(env):
    pilot(env)
    sh = {"stage": "full", "dataset": "phoneme", "model": "mlp", "seed": 42}
    p = run.shard_path(sh, env.cfg, ".failed")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({**sh, "host": "h", "commit": "c", "error": "MemoryError: x", "at": "2026-11-14T17:00:00Z"}))
    env.log("full_main.log", ["full: 0 of 160 shards done; 160 to run with 6 jobs (commit a1677fe26d78)",
                              "2026-11-14T17:00:00Z FAILED phoneme/mlp/seed_42: MemoryError: x"])
    s = dash.gather(NOW)
    assert s["stages"]["full"]["failed"] == 1 and s["overall"]["failed"] == 1
    assert any("1 failed shard" in w for w in s["warnings"])
    assert any(ev["bad"] and "FAILED phoneme/mlp/seed_42" in ev["event"] for ev in s["history"])
    assert "MemoryError" in dash.render_html(s)


def test_stale_heartbeat_of_a_live_runner_is_stalled(env):
    pilot(env)
    env.alive = True
    env.beat(stage="full", heartbeat="2026-11-14T16:00:00Z", todo=100, running=["phoneme/rf/seed_42"])
    s = dash.gather(NOW)
    assert s["runner"]["state"] == "stalled"
    assert any(w.startswith("STALLED") for w in s["warnings"])


def test_missing_or_malformed_data(env):
    (env.work / "pilot" / "adult" / "rf").mkdir(parents=True)
    (env.work / "pilot" / "adult" / "rf" / "seed_42.done").write_text("{not json")
    (env.work / "heartbeat.json").write_text("[]")
    (env.root / "experiments" / "exp_g" / "host.json").unlink()
    env.git_out.clear()
    env.units.clear()
    s = dash.gather(NOW)
    assert s["runner"]["state"] == "idle"
    assert s["stages"]["pilot"]["done"] == 1           # marker exists; its summary is unreadable
    for text in outputs(s):
        assert text


def test_unavailable_temperature_sensor(env, monkeypatch):
    pilot(env)
    monkeypatch.setattr(dash, "SENSOR_GLOB", "/nonexistent/thermal_zone*")
    s = dash.gather(NOW)
    assert s["host"]["temp_c"] is None
    assert "temperature not available" in dash.render_html(s)
    assert "not available" in dash.render_text(s)


def test_publisher_failure(env):
    pilot(env)
    env.log("publish.log", [
        "2026-11-14T16:21:17.489565+00:00 published: 4 new shard(s); 2 event(s)",
        "refused: 2 log file(s) ignored by git, e.g. outputs/analysis/paper_g/logs/x.log",
        "2026-11-14T17:52:34.152629+00:00 NOT published: logs would be omitted; 1 event(s)"])
    (env.work / "events.json").write_text(json.dumps({"push_failing_since": "2026-11-14T15:00:00Z"}))
    env.git_out["rev-list --count refs/remotes/origin/paper/g-runs..HEAD"] = "2"
    s = dash.gather(NOW)
    w = " ".join(s["warnings"])
    assert "did not publish" in w and "Push to GitHub failing" in w and "2 local commit(s) not on origin" in w
    assert "No successful publish" in w               # last success 16:21, now 18:00
    assert any(ev["bad"] and ev["source"] == "publisher" for ev in s["history"])


def test_published_shard_without_log_in_git_is_flagged(env):
    pilot(env)
    env.git_out["ls-files outputs/analysis/paper_g/logs"] = ""
    s = dash.gather(NOW)
    assert any("no log in git (RCA-004)" in w for w in s["warnings"])
    assert len(s["publishing"]["published_without_log"]) == 4


def test_successful_publication(env):
    pilot(env)
    s = dash.gather(NOW)
    p = s["publishing"]
    assert p["last_ok"] == "2026-11-14T17:52:34+00:00" and p["remote_sha"] == "0f6939204"
    assert p["unpushed_commits"] == 0 and p["awaiting_copy"] == 0 and p["manifest_shards"] == 4
    events = [ev["event"] for ev in s["history"] if ev["source"] == "publisher"]
    assert events == ["publisher succeeded: 0 new shard(s); 0 event(s)",
                      "publisher succeeded: 4 new shard(s); 2 event(s)"]   # later quiet cycles dropped


def test_intentionally_stopped_service_vs_unexpected_termination(env):
    pilot(env)
    env.beat(stage="full", heartbeat="2026-11-14T17:00:00Z", todo=120, running=["phoneme/rf/seed_42"])
    env.units["paper-g-run@full.service"] = {"ActiveState": "inactive", "Result": "success"}
    s = dash.gather(NOW)
    assert s["runner"]["state"] == "stopped" and not any("unexpected" in w for w in s["warnings"])
    env.units["paper-g-run@full.service"] = {"ActiveState": "failed", "Result": "exit-code", "ExecMainStatus": "1"}
    s = dash.gather(NOW)
    assert s["runner"]["state"] == "interrupted" and any("unexpected termination" in w for w in s["warnings"])


def test_completed_experiment_only_when_all_four_stages_finish(env):
    pilot(env)
    for stage in ("full", "roar", "synthetic"):
        for sh in run.shards(stage, env.cfg):
            p = run.shard_path(sh, env.cfg, ".done")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps({"rows": 1, "seconds": 1.0, "finished": "2026-11-14T17:00:00Z"}))
    env.beat(stage="synthetic", todo=0, running=[], heartbeat="2026-11-14T17:00:00Z")
    s = dash.gather(NOW)
    assert s["runner"]["state"] == "completed" and "experiment complete" in dash.render_html(s)


def test_terminal_rendering(env):
    pilot(env)
    t = dash.render_text(dash.gather(NOW))
    assert "Runner: IDLE" in t and "pilot       4/4" in t and "full        0/160" in t
    assert "Overall: 4/344 shards, 0 failed" in t and "timer active" in t


def test_browser_refresh_and_endpoints_write_nothing(env):
    pilot(env)

    def tree():
        return {str(p): (p.stat().st_size, p.stat().st_mtime_ns) for p in env.root.rglob("*") if p.is_file()}

    before = tree()
    srv = dash.serve(0)
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    try:
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        assert srv.server_address[0] == "127.0.0.1"
        pages = [urllib.request.urlopen(base + "/", timeout=10).read().decode() for _ in range(2)]
        hb = json.loads(urllib.request.urlopen(base + "/api/heartbeat", timeout=10).read())
        st = json.loads(urllib.request.urlopen(base + "/api/state", timeout=10).read())
    finally:
        srv.shutdown()
        srv.server_close()
        th.join(timeout=5)
    assert all("Paper G — run monitor" in p for p in pages)
    assert hb["runner"]["alive"] is False and hb["publisher"]["ok"] is True
    assert st["stages"]["pilot"]["done"] == 4
    for text in pages + [json.dumps(hb), json.dumps(st)]:
        assert SENTINEL not in text
    assert tree() == before                           # opening the page changes no file
    assert not th.is_alive()


def test_progress_reads_markers_not_raw_results(env, monkeypatch):
    """344 finished shards: progress comes from .done markers; no raw file is opened."""
    pilot(env)
    for stage in ("full", "roar", "synthetic"):
        for sh in run.shards(stage, env.cfg):
            p = run.shard_path(sh, env.cfg, ".done")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps({"rows": 1600, "seconds": 300.0, "finished": "2026-11-14T17:00:00Z",
                                     "auc": float(SENTINEL)}))
    monkeypatch.setattr(gzip, "open", lambda *a, **k: (_ for _ in ()).throw(AssertionError("raw file read")))
    t0 = time.process_time()
    s = dash.gather(NOW)
    cpu = time.process_time() - t0
    assert s["overall"]["done"] == 344
    assert cpu < 1.0, f"one refresh took {cpu:.2f} s of CPU"
    assert SENTINEL not in json.dumps(s, default=str)
