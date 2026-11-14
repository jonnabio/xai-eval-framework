#!/usr/bin/env python3
"""Paper G: send the run's progress, raw rows and logs to GitHub (run host only).

    python scripts/paper_g_publish.py              one cycle (the timer calls this every 15 min)
    python scripts/paper_g_publish.py --no-push    copy and commit, do not push or notify

Each cycle (docs/reports/paper_g/RUN_PROTOCOL.md, section 5):
1. copies newly finished shards to outputs/analysis/paper_g/raw/<stage>/<shard>.jsonl.gz,
   unchanged, and lists them in raw/MANIFEST.csv (rows, failed rows, SHA-256);
2. copies the shard logs and the main logs to outputs/analysis/paper_g/logs/;
3. rewrites outputs/analysis/paper_g/STATUS.md;
4. stages only the lane's output paths, runs the lane guard, commits and pushes;
5. comments on the GitHub issue "Paper G run" on events only (section 6).

It refuses to run on any branch but paper/g-runs. A push that fails is retried next cycle.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_g_lib as lib  # noqa: E402
import paper_g_run as run  # noqa: E402
import paper_g_status as status  # noqa: E402

RUN_BRANCH = "paper/g-runs"
ISSUE_TITLE = "Paper G run"
RAW = lib.OUT / "raw"
LOGS = lib.OUT / "logs"
LOG_GZIP_BYTES = 1_000_000
PUSH_ALERT_HOURS = 2
STAGE_PATHS = ["outputs/analysis/paper_g", "experiments/exp_g/host.json",
               "experiments/exp_g/ENVIRONMENT.md"]


def git(*args, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=lib.ROOT, capture_output=True, text=True, check=check)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_shards(cfg: dict) -> list[str]:
    """Copy finished shards that are not yet in raw/. Returns the new published paths."""
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = RAW / "MANIFEST.csv"
    known = set()
    if manifest.exists():
        with manifest.open(encoding="utf-8") as fh:
            known = {r["path"] for r in csv.DictReader(fh)}
    new_rows, added = [], []
    for stage in run.STAGES:
        for sh in run.shards(stage, cfg):
            if run.state(sh, cfg) != "done":
                continue
            rel = f"{stage}/{run.shard_name(sh)}.jsonl.gz"
            if rel in known:
                continue
            src = run.shard_path(sh, cfg, ".jsonl.gz")
            dst = RAW / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            info = json.loads(run.shard_path(sh, cfg, ".done").read_text(encoding="utf-8"))
            new_rows.append({"path": rel, "rows": info.get("rows"),
                             "failed_rows": info.get("failed_rows"), "sha256": sha256(dst),
                             "host": info.get("host"), "commit": info.get("commit"),
                             "finished": info.get("finished")})
            added.append(rel)
    if new_rows:
        write_header = not manifest.exists()
        with manifest.open("a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(new_rows[0]))
            if write_header:
                w.writeheader()
            w.writerows(new_rows)
    return added


def copy_logs(cfg: dict) -> list[Path]:
    """Copy every log to logs/. Returns the published paths (all of them, every cycle)."""
    src_root = run.work_dir(cfg) / "logs"
    published: list[Path] = []
    if not src_root.exists():
        return published
    for src in src_root.rglob("*.log"):
        rel = src.relative_to(src_root)
        if src.stat().st_size > LOG_GZIP_BYTES:
            dst = LOGS / (str(rel) + ".gz")
            dst.parent.mkdir(parents=True, exist_ok=True)
            with src.open("rb") as fi, gzip.open(dst, "wb", mtime=0) as fo:
                shutil.copyfileobj(fi, fo)
        else:
            dst = LOGS / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        published.append(dst)
    return published


def ignored(paths: list[Path]) -> list[str]:
    """Published files git would silently skip on `git add` (RCA-004: `logs/` and `*.log` in .gitignore)."""
    if not paths:
        return []
    rel = [p.resolve().relative_to(lib.ROOT.resolve()).as_posix() for p in paths]
    out = git("check-ignore", "--", *rel, check=False)
    return [line for line in out.stdout.splitlines() if line.strip()]


# --- events -------------------------------------------------------------------------

def events_due(cfg: dict, seen: dict, now: datetime) -> list[str]:
    """Messages for events not reported yet; updates `seen` in place."""
    msgs = []
    state = status.collect(cfg)
    beat = status._read(run.work_dir(cfg) / "heartbeat.json") or {}
    for stage, rows in state.items():
        n_done = sum(r["state"] == "done" for r in rows)
        key_start, key_end = f"start:{stage}", f"end:{stage}"
        if (n_done or beat.get("stage") == stage) and key_start not in seen:
            seen[key_start] = 1
            msgs.append(f"Stage **{stage}** started ({len(rows)} shards).")
        for s in sorted({r["seed"] for r in rows}):
            rs = [r for r in rows if r["seed"] == s]
            if stage != "pilot" and all(r["state"] == "done" for r in rs) and f"seed:{stage}:{s}" not in seen:
                seen[f"seed:{stage}:{s}"] = 1
                msgs.append(f"Stage **{stage}**: seed {s} finished ({len(rs)} shards).")
        if rows and n_done == len(rows) and key_end not in seen:
            seen[key_end] = 1
            msgs.append(f"Stage **{stage}** finished: all {len(rows)} shards done.")
        for r in rows:
            k = f"fail:{stage}:{r['shard']}:{r['info'].get('at', '')}"
            if r["state"] == "failed" and k not in seen:
                seen[k] = 1
                msgs.append(f"Shard **{stage} {r['shard']}** failed: "
                            f"`{(r['info'].get('error') or '')[:300]}`. "
                            f"Log: `outputs/analysis/paper_g/logs/{stage}/{r['shard']}.log`.")
    age = status._age_min(beat.get("heartbeat"), now)
    active = bool(beat.get("running")) or bool(beat.get("todo"))
    if active and age is not None and age > status.STALL_MINUTES:
        k = f"stall:{beat.get('heartbeat')}"
        if k not in seen:
            seen[k] = 1
            msgs.append(f"Run looks **stalled**: no heartbeat for {age:.0f} min "
                        f"(stage {beat.get('stage')}). Check the run host.")
    return msgs


def notify(messages: list[str]) -> bool:
    if not messages:
        return True
    body = "\n".join(f"- {m}" for m in messages)
    try:
        found = subprocess.run(["gh", "issue", "list", "--state", "open", "--search",
                                f'"{ISSUE_TITLE}" in:title', "--json", "number,title"],
                               cwd=lib.ROOT, capture_output=True, text=True, check=True)
        issues = [i for i in json.loads(found.stdout) if i["title"] == ISSUE_TITLE]
        if issues:
            subprocess.run(["gh", "issue", "comment", str(issues[0]["number"]), "--body", body],
                           cwd=lib.ROOT, capture_output=True, text=True, check=True)
        else:
            subprocess.run(["gh", "issue", "create", "--title", ISSUE_TITLE, "--body",
                            "Events of the Paper G run (scripts/paper_g_publish.py).\n\n" + body],
                           cwd=lib.ROOT, capture_output=True, text=True, check=True)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


# --- one cycle -------------------------------------------------------------------------

def cycle(push: bool = True, now: datetime | None = None) -> int:
    now = now or datetime.now(timezone.utc)
    cfg = lib.config()
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if branch != RUN_BRANCH:
        print(f"refused: on branch {branch!r}, publishing only on {RUN_BRANCH}", file=sys.stderr)
        return 2
    seen_path = run.work_dir(cfg) / "events.json"
    seen = status._read(seen_path) or {}
    added = copy_shards(cfg)
    logs = copy_logs(cfg)
    lib.OUT.mkdir(parents=True, exist_ok=True)
    (lib.OUT / "STATUS.md").write_text(status.build(cfg, now), encoding="utf-8")
    git("add", "--", *[p for p in STAGE_PATHS if (lib.ROOT / p).exists()])
    msgs, rc = [], 0
    skipped = ignored(logs)
    if skipped:
        # Never report a snapshot as published while git silently leaves its logs out (RCA-004).
        git("reset", "-q", check=False)
        rc = 3
        msgs.append(f"Publisher refused a commit: {len(skipped)} log file(s) are ignored by .gitignore and "
                    f"would not be published (RCA-004), e.g. `{skipped[0]}`.")
        print(f"refused: {len(skipped)} log file(s) ignored by git, e.g. {skipped[0]}", file=sys.stderr)
    elif (guard := subprocess.run([sys.executable, "scripts/pubs/check_lane.py", "--staged"],
                                  cwd=lib.ROOT, capture_output=True, text=True)).returncode != 0:
        git("reset", "-q", check=False)
        msgs.append(f"Publisher refused a commit: the lane guard failed.\n```\n{guard.stdout[-800:]}{guard.stderr[-800:]}\n```")
    elif git("diff", "--cached", "--quiet", check=False).returncode != 0:
        state = status.collect(cfg)
        done = sum(r["state"] == "done" for rows in state.values() for r in rows)
        total = sum(len(rows) for rows in state.values())
        stage = (status._read(run.work_dir(cfg) / "heartbeat.json") or {}).get("stage", "run")
        git("commit", "-q", "-m",
            f"data(paper-g): {stage} snapshot {now.strftime('%Y-%m-%d %H:%M')} ({done}/{total})",
            "-m", f"{len(added)} new shard file(s). Published by scripts/paper_g_publish.py.")
    if push:
        pushed = git("push", "-q", "origin", RUN_BRANCH, check=False).returncode == 0
        if pushed:
            seen.pop("push_failing_since", None)
        else:
            since = seen.setdefault("push_failing_since", now.strftime("%Y-%m-%dT%H:%M:%SZ"))
            hours = (status._age_min(since, now) or 0) / 60
            if hours > PUSH_ALERT_HOURS and not seen.get("push_alerted"):
                seen["push_alerted"] = 1
                msgs.append(f"Pushing has failed for {hours:.1f} h on the run host.")
        msgs += events_due(cfg, seen, now)
        if notify(msgs):
            seen_path.parent.mkdir(parents=True, exist_ok=True)
            seen_path.write_text(json.dumps(seen, indent=1), encoding="utf-8")
    if rc:
        print(f"{now.isoformat()} NOT published: logs would be omitted; {len(msgs)} event(s)")
        return rc
    print(f"{now.isoformat()} published: {len(added)} new shard(s), {len(logs)} log(s); {len(msgs)} event(s)")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-push", action="store_true")
    args = ap.parse_args(argv)
    return cycle(push=not args.no_push)


if __name__ == "__main__":
    sys.exit(main())
