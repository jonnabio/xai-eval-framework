#!/usr/bin/env python3
"""Lane guard: keep one session's work out of another lane (ADR-0021).

The lanes, their folders and the paths they own are in scripts/pubs/lanes.toml.

  check_lane.py claim --owner NAME    start of a session: check the folder and take its lock
  check_lane.py release --owner NAME  end of a session: give the lock back
  check_lane.py status                show the lane, the lock and whether `main` was taken
  check_lane.py --staged              pre-commit: check the staged files (.githooks/pre-commit)
  check_lane.py --range A..B          CI: check every commit in a range

A commit passes when
  1. the branch is a registered lane and is checked out in that lane's folder;
  2. the lane has taken `main` (local `main` is an ancestor of HEAD);
  3. it touches no path another lane owns;
  4. it does not mix the lane's own paths with shared paths;
  5. the folder holds a live session lock (and, if LANE_OWNER is set, that owner's).
Merge commits are skipped: taking `main` brings every lane's files.

Standard library only, so the hook runs without the project environment.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

REGISTRY = Path(__file__).with_name("lanes.toml")
LOCK_NAME = "lane-session.lock"


def git(*args: str, check: bool = True) -> str:
    out = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8")
    if check and out.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout.strip()


def load_registry(path: Path = REGISTRY) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def matches(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        return path.startswith(pattern[:-2])
    return fnmatch.fnmatchcase(path, pattern)


def owner_of(path: str, registry: dict) -> str | None:
    """Name of the lane that owns `path`, or None when the path is shared."""
    for lane in registry["lane"]:
        if any(matches(path, pat) for pat in lane["owns"]):
            return lane["name"]
    return None


def lane_of(branch: str, registry: dict) -> dict | None:
    for lane in registry["lane"]:
        if any(fnmatch.fnmatchcase(branch, pat) for pat in lane["branches"]):
            return lane
    return None


def commit_problems(paths: list[str], lane: dict | None, registry: dict) -> list[str]:
    """Rules 3 and 4. With lane=None (CI on `main`) only the mixing rules apply."""
    owned: dict[str, list[str]] = {}
    shared: list[str] = []
    for p in paths:
        o = owner_of(p, registry)
        if o is None:
            shared.append(p)
        else:
            owned.setdefault(o, []).append(p)
    problems = []
    if lane is not None:
        for o, ps in owned.items():
            if o != lane["name"]:
                problems.append(
                    f"lane '{lane['name']}' may not change paths owned by lane '{o}': "
                    + ", ".join(ps[:5]) + (" ..." if len(ps) > 5 else "")
                )
    elif len(owned) > 1:
        problems.append("one commit changes paths of several lanes: " + ", ".join(sorted(owned)))
    if owned and shared:
        problems.append(
            "the commit mixes lane paths with shared paths; commit the shared files "
            "separately and send that commit through main: " + ", ".join(shared[:5])
            + (" ..." if len(shared) > 5 else "")
        )
    return problems


# --- the folder and its lock -------------------------------------------------

def lock_path() -> Path:
    return Path(git("rev-parse", "--absolute-git-dir")) / LOCK_NAME


def read_lock(registry: dict) -> dict | None:
    """The live lock of this folder, or None when there is none or it is stale."""
    p = lock_path()
    if not p.exists():
        return None
    try:
        lock = json.loads(p.read_text(encoding="utf-8"))
        seen = dt.datetime.fromisoformat(lock["heartbeat"])
    except (ValueError, KeyError):
        return None
    age = dt.datetime.now(dt.timezone.utc) - seen
    if age > dt.timedelta(hours=registry.get("lock_stale_hours", 12)):
        return None
    return lock


def write_lock(owner: str, branch: str, claimed_at: str | None = None) -> None:
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    lock_path().write_text(
        json.dumps({"owner": owner, "branch": branch,
                    "claimed_at": claimed_at or now, "heartbeat": now}, indent=2),
        encoding="utf-8",
    )


def folder_problems(registry: dict) -> tuple[dict | None, list[str]]:
    """Rules 1 and 2 for the current folder."""
    branch = git("branch", "--show-current")
    folder = Path(git("rev-parse", "--show-toplevel")).name
    if not branch:
        return None, ["detached HEAD: check out a lane branch before working"]
    if branch == "main":
        return None, ["`main` is checked out; it is never worked on directly (ADR-0013)"]
    lane = lane_of(branch, registry)
    if lane is None:
        return None, [f"branch '{branch}' is not a lane in scripts/pubs/lanes.toml"]
    problems = []
    if folder != lane["folder"]:
        problems.append(
            f"lane '{lane['name']}' ({branch}) belongs in folder '{lane['folder']}', "
            f"not '{folder}'"
        )
    if git("rev-parse", "--verify", "--quiet", "main", check=False):
        if subprocess.run(["git", "merge-base", "--is-ancestor", "main", "HEAD"]).returncode:
            problems.append("this lane has not taken `main`: run `git merge main` first")
    return lane, problems


# --- commands ----------------------------------------------------------------

def cmd_status(registry: dict) -> int:
    lane, problems = folder_problems(registry)
    lock = read_lock(registry)
    dirty = git("status", "--porcelain")
    print(f"folder : {Path(git('rev-parse', '--show-toplevel')).name}")
    print(f"branch : {git('branch', '--show-current') or '(detached)'}")
    print(f"lane   : {lane['name'] if lane else '(none)'}")
    print(f"lock   : {lock['owner'] + ' since ' + lock['claimed_at'] if lock else 'free'}")
    print(f"tree   : {'uncommitted files present' if dirty else 'clean'}")
    for p in problems:
        print(f"PROBLEM: {p}")
    return 1 if problems else 0


def cmd_claim(registry: dict, owner: str) -> int:
    lane, problems = folder_problems(registry)
    lock = read_lock(registry)
    if lock and lock["owner"] != owner:
        problems.append(
            f"this folder is in use by '{lock['owner']}' (branch {lock['branch']}, "
            f"last active {lock['heartbeat']}). Do not work here; pick another lane, "
            "or have the author release the lock."
        )
    if problems:
        for p in problems:
            print(f"FAIL: {p}", file=sys.stderr)
        return 1
    if git("status", "--porcelain"):
        print("WARNING: uncommitted files are present; another session may have left "
              "work here. Read `git status` before editing.")
    write_lock(owner, git("branch", "--show-current"), lock["claimed_at"] if lock else None)
    print(f"OK: lane '{lane['name']}' claimed by '{owner}'")
    return 0


def cmd_release(registry: dict, owner: str) -> int:
    lock = read_lock(registry)
    if lock and lock["owner"] != owner:
        print(f"FAIL: the lock belongs to '{lock['owner']}', not '{owner}'", file=sys.stderr)
        return 1
    lock_path().unlink(missing_ok=True)
    print("OK: lock released")
    return 0


def cmd_staged(registry: dict) -> int:
    git_dir = Path(git("rev-parse", "--absolute-git-dir"))
    if (git_dir / "MERGE_HEAD").exists():
        return 0
    lane, problems = folder_problems(registry)
    paths = [p for p in git("diff", "--cached", "--name-only").splitlines() if p]
    if lane is not None:
        problems += commit_problems(paths, lane, registry)
    lock = read_lock(registry)
    env_owner = os.environ.get("LANE_OWNER")
    if lock is None:
        problems.append(
            "no session holds this folder: run "
            "`python scripts/pubs/check_lane.py claim --owner <name>` first"
        )
    elif env_owner and env_owner != lock["owner"]:
        problems.append(f"this folder is claimed by '{lock['owner']}', not '{env_owner}'")
    if problems:
        print("lane guard (ADR-0021) refused this commit:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    write_lock(lock["owner"], lock["branch"], lock["claimed_at"])
    return 0


def cmd_range(registry: dict, rev_range: str) -> int:
    failed = 0
    for sha in git("rev-list", "--no-merges", rev_range).splitlines():
        paths = git("diff-tree", "--no-commit-id", "--name-only", "-r", sha).splitlines()
        for p in commit_problems(paths, None, registry):
            print(f"FAIL {sha[:9]}: {p}", file=sys.stderr)
            failed = 1
    if not failed:
        print(f"OK: every commit in {rev_range} keeps to one lane")
    return failed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", nargs="?", choices=["claim", "release", "status"])
    ap.add_argument("--owner")
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--range", dest="rev_range")
    args = ap.parse_args(argv)
    registry = load_registry()
    if args.staged:
        return cmd_staged(registry)
    if args.rev_range:
        return cmd_range(registry, args.rev_range)
    if args.command == "status":
        return cmd_status(registry)
    if args.command in ("claim", "release"):
        if not args.owner:
            ap.error(f"{args.command} needs --owner")
        return (cmd_claim if args.command == "claim" else cmd_release)(registry, args.owner)
    ap.error("give a command, --staged or --range")
    return 2


if __name__ == "__main__":
    sys.exit(main())
