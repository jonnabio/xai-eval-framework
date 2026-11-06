#!/usr/bin/env python3
"""Paper B revision 1: save the live results to git and push them, without touching
the checked-out branch.

    python scripts/paper_b_sync.py            one snapshot: commit + push if anything changed
    python scripts/paper_b_sync.py --loop     every [sync].every_minutes (Ctrl+C to leave)
    python scripts/paper_b_sync.py --no-push  commit locally only

    Stop a loop started in the background: create outputs/paper_b_rev1_live/_STOP_SYNC
    (it makes one last snapshot within a minute, then exits).

The loop also pushes the committed state of the lane branches in [sync].also_push
(default paper/b-ci-revision-1), never forced, so committed work reaches GitHub within
every_minutes. Uncommitted files are never touched.

The live files (outputs/paper_b_rev1_live/, git-ignored) are copied into a commit on the
runs branch ([sync].branch, default paper/b-rev1-runs) under [sync].results_prefix, with
git plumbing: a temporary index, `hash-object`, `update-index`, `write-tree`, `commit-tree`
and a compare-and-swap `update-ref`. The working tree, HEAD and the real index are never
changed, so the run and the author's work on the revision branch go on undisturbed.

Safety: the push is never forced. If the remote branch has moved (another machine
pushed), the push is refused and reported; nothing is overwritten. A file larger than
[sync].max_file_mb is skipped and reported (GitHub refuses files over 100 MB).
Heartbeats and temporary files are not copied.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_b_lib as lib  # noqa: E402

SKIP_SUFFIXES = (".heartbeat", ".tmp")


def git(*args: str, env: dict | None = None, input_text: str | None = None,
        cwd: Path | None = None, check: bool = True) -> str:
    # Bytes, not text mode: on Windows text-mode stdin turns "\n" into "\r\n", which
    # corrupts --stdin-paths and --index-info records.
    r = subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "core.safecrlf=false", *args],
                       cwd=cwd or lib.ROOT, env=env,
                       input=None if input_text is None else input_text.encode("utf-8"),
                       capture_output=True, timeout=600)
    out = r.stdout.decode("utf-8", "replace").strip()
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: "
                           f"{r.stderr.decode('utf-8', 'replace').strip()}")
    return out


def ref_exists(ref: str, cwd: Path | None = None) -> bool:
    return subprocess.run(["git", "rev-parse", "--verify", "--quiet", ref], cwd=cwd or lib.ROOT,
                          capture_output=True).returncode == 0


def collect(live: Path, max_mb: float) -> tuple[list[tuple[Path, str]], list[str]]:
    """(file, path in the commit) for every live file to save; and the skipped ones."""
    files, skipped = [], []
    for base, prefix in ((live / "results", "results"), (live / "pilot", "pilot"),
                         (live / "_state", "_state")):
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or p.name.startswith(".") or p.suffix in SKIP_SUFFIXES:
                continue
            if p.stat().st_size > max_mb * 2**20:
                skipped.append(f"{p} ({p.stat().st_size / 2**20:.0f} MB)")
                continue
            files.append((p, f"{prefix}/{p.relative_to(base).as_posix()}"))
    status = live / "STATUS.md"
    if status.exists():
        files.append((status, "STATUS.md"))
    return files, skipped


def snapshot(branch: str, prefix: str, live: Path, max_mb: float, base_ref: str,
             cwd: Path | None = None) -> str | None:
    """Commit the live files on `branch`; return the new commit, or None if unchanged."""
    ref = f"refs/heads/{branch}"
    parent = git("rev-parse", ref, cwd=cwd) if ref_exists(ref, cwd) else git("rev-parse", base_ref, cwd=cwd)
    files, skipped = collect(live, max_mb)
    for s in skipped:
        print(f"SKIPPED (too large): {s}", flush=True)
    with tempfile.TemporaryDirectory() as td:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(td) / "index"))
        git("read-tree", parent, env=env, cwd=cwd)
        if files:
            blobs = git("hash-object", "-w", "--no-filters", "--stdin-paths",
                        input_text="\n".join(str(f) for f, _ in files) + "\n", cwd=cwd).split()
            if len(blobs) != len(files):
                raise RuntimeError(f"hash-object returned {len(blobs)} ids for {len(files)} files")
            info = "".join(f"100644 {b}\t{prefix}/{dest}\0" for b, (_, dest) in zip(blobs, files))
            git("update-index", "-z", "--index-info", env=env, input_text=info, cwd=cwd)
            staged = git("ls-files", "--", f"{prefix}/", env=env, cwd=cwd).splitlines()
            missing = {f"{prefix}/{d}" for _, d in files} - set(staged)
            if missing:                                   # never commit a partial snapshot
                raise RuntimeError(f"{len(missing)} files did not reach the index, "
                                   f"e.g. {sorted(missing)[0]}")
        tree = git("write-tree", env=env, cwd=cwd)
    if tree == git("rev-parse", f"{parent}^{{tree}}", cwd=cwd):
        return None
    msg = (f"data(paper-b): B2 results snapshot {time.strftime('%Y-%m-%d %H:%M')}\n\n"
           f"{len(files)} files from outputs/paper_b_rev1_live/ (automatic, paper_b_sync.py).\n")
    commit = git("commit-tree", tree, "-p", parent, "-m", msg, cwd=cwd)
    # Compare-and-swap: refuses if the branch moved since `parent` was read.
    if ref_exists(ref, cwd):
        git("update-ref", ref, commit, parent, cwd=cwd)
    else:
        git("update-ref", ref, commit, "", cwd=cwd)
    return commit


def push(branch: str, remote: str, cwd: Path | None = None) -> tuple[bool, str]:
    r = subprocess.run(["git", "push", remote, f"refs/heads/{branch}:refs/heads/{branch}"],
                       cwd=cwd or lib.ROOT, capture_output=True, text=True, timeout=600)
    return r.returncode == 0, (r.stderr or r.stdout).strip()[-400:]


def write_state(**kw) -> None:
    state = lib.read_json(lib.STATE / "sync.json", {}) or {}
    state.update(kw)
    lib.atomic_write_json(lib.STATE / "sync.json", state)


def once(cfg: dict, do_push: bool) -> int:
    sc = cfg["sync"]
    try:
        import paper_b_dashboard as dash
        dash.write_status_md()
    except Exception as exc:      # the dashboard must never block a save
        print(f"status page not written: {exc}", flush=True)
    try:
        base = git("rev-parse", "HEAD")
        commit = snapshot(sc["branch"], sc["results_prefix"], lib.LIVE, sc["max_file_mb"], base)
    except Exception as exc:
        write_state(last_error=str(exc)[-400:], last_error_time=time.time())
        print(f"snapshot FAILED: {exc}", flush=True)
        return 1
    if commit:
        write_state(last_commit=commit, last_commit_time=time.time())
        print(f"committed {commit[:10]} on {sc['branch']}", flush=True)
    else:
        print("no change since the last snapshot", flush=True)
    if not do_push:
        return 0
    rc = push_lanes(sc)
    head = git("rev-parse", f"refs/heads/{sc['branch']}")
    last = (lib.read_json(lib.STATE / "sync.json", {}) or {}).get("last_pushed")
    if head == last:
        return rc
    for attempt in range(4):
        ok, out = push(sc["branch"], sc["remote"])
        if ok:
            write_state(last_pushed=head, last_push_time=time.time(), last_error=None)
            print(f"pushed {head[:10]} to {sc['remote']}/{sc['branch']}", flush=True)
            return rc
        if "non-fast-forward" in out or "rejected" in out:
            write_state(last_error=f"push rejected (remote moved; nothing overwritten): {out}",
                        last_error_time=time.time())
            print(f"push REFUSED, the remote branch moved; resolve by hand: {out}", flush=True)
            return 1
        time.sleep(30 * (attempt + 1))                     # network: back off and retry
    write_state(last_error=f"push failed: {out}", last_error_time=time.time())
    print(f"push FAILED after retries: {out}", flush=True)
    return 1


def push_lanes(sc: dict) -> int:
    """Push the committed state of each lane branch in [sync].also_push (never forced).
    Uncommitted work is not touched: only commits travel."""
    rc = 0
    for br in sc.get("also_push", []):
        if not ref_exists(f"refs/heads/{br}"):
            continue
        local = git("rev-parse", f"refs/heads/{br}")
        remote_ref = f"refs/remotes/{sc['remote']}/{br}"
        if ref_exists(remote_ref) and git("rev-parse", remote_ref) == local:
            continue                                   # nothing new
        ok, out = push(br, sc["remote"])
        if ok:
            write_state(**{f"lane_{br}": {"pushed": local, "time": time.time()}})
            print(f"pushed lane {br} at {local[:10]}", flush=True)
        else:
            rc = 1
            write_state(last_error=f"lane push {br} refused (nothing overwritten): {out}",
                        last_error_time=time.time())
            print(f"lane push REFUSED for {br}: {out}", flush=True)
    return rc


STOP_SYNC = lib.LIVE / "_STOP_SYNC"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--loop", action="store_true")
    ap.add_argument("--no-push", dest="push", action="store_false")
    args = ap.parse_args(argv)
    cfg = lib.config()
    lib.STATE.mkdir(parents=True, exist_ok=True)
    if not args.loop:
        return once(cfg, args.push)
    every = 60 * float(cfg["sync"]["every_minutes"])
    write_state(loop_pid=os.getpid(), loop_started=time.time())
    try:
        while True:
            print(time.strftime("%Y-%m-%d %H:%M:%S"), "snapshot", flush=True)
            once(lib.config(), args.push)
            write_state(loop_heartbeat=time.time(), loop_pid=os.getpid())
            t_next = time.time() + every
            while time.time() < t_next:              # wake each minute: stop file, heartbeat
                if STOP_SYNC.exists():
                    print(f"{STOP_SYNC} found: one last snapshot, then leaving", flush=True)
                    STOP_SYNC.unlink(missing_ok=True)
                    rc = once(lib.config(), args.push)
                    write_state(loop_pid=None, loop_stopped=time.time())
                    return rc
                time.sleep(60)
                write_state(loop_heartbeat=time.time())
    except KeyboardInterrupt:
        print("leaving; one last snapshot", flush=True)
        rc = once(lib.config(), args.push)
        write_state(loop_pid=None, loop_stopped=time.time())
        return rc


if __name__ == "__main__":
    raise SystemExit(main())
