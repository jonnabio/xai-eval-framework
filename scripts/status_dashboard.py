#!/usr/bin/env python3
"""
Cross-platform terminal dashboard for XAI experiment progress.

Usage:
  python scripts/status_dashboard.py
  python scripts/status_dashboard.py --interval 5
  python scripts/status_dashboard.py --config-dir configs/experiments/exp2_scaled
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import psutil
import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG_FILE = PROJECT_ROOT / "logs" / "managed_runner.log"
DEFAULT_CONFIG_DIR = PROJECT_ROOT / "configs" / "experiments" / "exp2_scaled"
DEFAULT_RESULTS_DIR = PROJECT_ROOT / "experiments" / "exp2_scaled" / "results"
REMOTE_WORKER_PREFIX = "origin/results/"
REMOTE_WORKER_FETCH_REFSPEC = "+refs/heads/results/*:refs/remotes/origin/results/*"
_LAST_REMOTE_WORKER_FETCH: datetime | None = None


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def get_load_average() -> str:
    if hasattr(os, "getloadavg"):
        try:
            return f"{os.getloadavg()[0]:.2f}"
        except OSError:
            pass
    return "N/A"


def get_branch_status(project_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "status", "--short", "--branch"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        first_line = result.stdout.splitlines()[0] if result.stdout else "unknown"
        return first_line.strip()
    except Exception:
        return "unknown"


def get_last_commit(project_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%h (%cr) %s"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip() or "Unknown"
    except Exception:
        return "Unknown"


def run_git(project_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )


def parse_git_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    try:
        return datetime.fromisoformat(normalized).replace(tzinfo=None)
    except ValueError:
        # PowerShell/.NET timestamps can contain 7 fractional digits; Python
        # accepts 6, so truncate only the fractional part before parsing.
        if "." in normalized:
            head, tail = normalized.split(".", 1)
            offset = ""
            for marker in ("+", "-"):
                idx = tail.rfind(marker)
                if idx > 0:
                    tail, offset = tail[:idx], tail[idx:]
                    break
            try:
                return datetime.fromisoformat(f"{head}.{tail[:6]}{offset}").replace(tzinfo=None)
            except ValueError:
                return None
    return None


def normalize_remote_worker_branch(ref: str) -> str:
    return ref.removeprefix(REMOTE_WORKER_PREFIX)


def maybe_fetch_remote_worker_branches(
    project_root: Path, enabled: bool, fetch_interval: int
) -> tuple[bool, str]:
    global _LAST_REMOTE_WORKER_FETCH

    if not enabled:
        return False, "disabled"

    now = datetime.now()
    if (
        _LAST_REMOTE_WORKER_FETCH
        and fetch_interval > 0
        and (now - _LAST_REMOTE_WORKER_FETCH).total_seconds() < fetch_interval
    ):
        return False, "cached"

    result = run_git(
        project_root,
        ["fetch", "--no-progress", "--prune", "origin", REMOTE_WORKER_FETCH_REFSPEC],
    )
    if result.returncode == 0:
        _LAST_REMOTE_WORKER_FETCH = now
        return True, "ok"

    message = (result.stderr or result.stdout or "fetch failed").strip().splitlines()
    return False, message[-1] if message else "fetch failed"


def get_remote_worker_refs(project_root: Path) -> list[str]:
    result = run_git(
        project_root,
        [
            "for-each-ref",
            "--format=%(refname:short)",
            "refs/remotes/origin/results",
        ],
    )
    if result.returncode != 0:
        return []
    return sorted(
        ref.strip()
        for ref in result.stdout.splitlines()
        if ref.strip().startswith(REMOTE_WORKER_PREFIX)
    )


def git_show_text(project_root: Path, ref: str, path: str) -> str | None:
    result = run_git(project_root, ["show", f"{ref}:{path}"])
    if result.returncode != 0:
        return None
    return result.stdout


def git_tree_paths(project_root: Path, ref: str, path: str) -> list[str]:
    result = run_git(project_root, ["ls-tree", "-r", "--name-only", ref, path])
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def get_main_sync_status(project_root: Path) -> dict:
    status = {
        "main_head": "Unknown",
        "main_results_last_commit": "Unknown",
        "pending_to_main_files": "?",
        "pending_from_main_files": "?",
    }

    try:
        main_head = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%h (%cr) %s", "origin/main"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if main_head.stdout.strip():
            status["main_head"] = main_head.stdout.strip()

        main_results_commit = subprocess.run(
            [
                "git",
                "log",
                "-1",
                "--pretty=format:%h (%cr) %s",
                "origin/main",
                "--",
                "experiments/exp2_scaled/results",
            ],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if main_results_commit.stdout.strip():
            status["main_results_last_commit"] = main_results_commit.stdout.strip()

        to_main = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                "origin/main..HEAD",
                "--",
                "experiments/exp2_scaled/results",
            ],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        from_main = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                "HEAD..origin/main",
                "--",
                "experiments/exp2_scaled/results",
            ],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )

        status["pending_to_main_files"] = len([line for line in to_main.stdout.splitlines() if line.strip()])
        status["pending_from_main_files"] = len([line for line in from_main.stdout.splitlines() if line.strip()])
    except Exception:
        return status

    return status


def get_live_runner_process() -> dict | None:
    try:
        script = r"""
import json
import psutil

matches = []
for proc in psutil.process_iter(["pid", "ppid", "name", "cmdline", "create_time"]):
    try:
        cmd = proc.info.get("cmdline") or []
        if len(cmd) >= 3 and cmd[1] == "-m" and cmd[2] == "src.experiment.runner":
            matches.append({
                "pid": proc.info["pid"],
                "ppid": proc.info["ppid"],
                "name": proc.info["name"],
                "cmdline": cmd,
                "create_time": proc.info["create_time"],
            })
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

print(json.dumps(matches))
"""
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        payload = json.loads(result.stdout or "[]")
        if not payload:
            return None
        payload.sort(key=lambda item: item.get("create_time", 0), reverse=True)
        proc = payload[0]
        cmdline = proc.get("cmdline") or []
        config_path = None
        if "--config" in cmdline:
            idx = cmdline.index("--config")
            if idx + 1 < len(cmdline):
                config_path = cmdline[idx + 1]
        return {
            "pid": proc.get("pid"),
            "ppid": proc.get("ppid"),
            "name": proc.get("name"),
            "config": config_path,
            "started_at": datetime.fromtimestamp(proc["create_time"]) if proc.get("create_time") else None,
        }
    except Exception:
        return None


def get_recent_log_lines(log_file: Path, max_lines: int = 8) -> list[str]:
    if not log_file.exists():
        return [f"Log file not found: {log_file}"]

    try:
        with log_file.open("r", encoding="utf-8", errors="replace") as handle:
            handle.seek(0, os.SEEK_END)
            size = handle.tell()
            handle.seek(max(size - 12000, 0))
            lines = handle.readlines()
        return [line.rstrip() for line in lines[-max_lines:]]
    except Exception as exc:
        return [f"Error reading log: {exc}"]


def normalize_name(name: str) -> str:
    return name.replace("_", "").replace("-", "")


def load_yaml(path: Path) -> dict | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except Exception:
        return None


def build_config_index(config_paths: list[Path]) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for path in config_paths:
        cfg = load_yaml(path)
        if not cfg:
            continue

        name = path.stem
        normalized = normalize_name(name)
        index[normalized] = cfg
    return index


def get_target_instances(cfg: dict, default: int = 400) -> int:
    sampling = cfg.get("sampling", {}) if isinstance(cfg, dict) else {}
    return sampling.get("samples_per_class", 100) * 4 if sampling else default


def target_for_result_dir(output_dir: str, config_index: dict[str, dict]) -> int:
    parts = Path(output_dir.replace("\\", "/")).parts
    if len(parts) < 3:
        return 400

    method, seed, n_value = parts[-3], parts[-2], parts[-1]
    display_name = f"{method}_{seed}_{n_value}"
    res_norm = normalize_name(display_name)
    res_norm_short = res_norm.replace("seed", "s")
    cfg = config_index.get(res_norm_short) or config_index.get(res_norm)
    return get_target_instances(cfg) if cfg else 400


def get_remote_worker_manifest(project_root: Path, ref: str) -> dict | None:
    manifest_paths = [
        path
        for path in git_tree_paths(
            project_root,
            ref,
            "experiments/exp2_scaled/worker_manifests",
        )
        if path.endswith("/current.json")
    ]
    for manifest_path in manifest_paths:
        raw_manifest = git_show_text(project_root, ref, manifest_path)
        if not raw_manifest:
            continue
        try:
            return json.loads(raw_manifest.lstrip("\ufeffï»¿"))
        except json.JSONDecodeError:
            continue
    return None


def remote_worker_from_manifest(ref: str, manifest: dict, config_index: dict[str, dict]) -> dict:
    output_dir = manifest.get("output_dir") or ""
    target_instances = manifest.get("target_instances") or target_for_result_dir(output_dir, config_index)
    latest_checkpoint = parse_git_datetime(manifest.get("last_checkpoint_at"))
    latest_write = parse_git_datetime(manifest.get("latest_instance_write"))

    return {
        "worker_id": manifest.get("worker_id") or normalize_remote_worker_branch(ref),
        "branch": ref,
        "source": "manifest",
        "experiment": manifest.get("experiment_name") or "unknown",
        "status": manifest.get("status") or "unknown",
        "done": int(manifest.get("instances_done") or 0),
        "total": int(target_instances or 0),
        "latest_checkpoint": latest_checkpoint,
        "latest_write": latest_write,
        "results_json_exists": bool(manifest.get("results_json_exists")),
        "output_dir": output_dir or "unknown",
    }


def summarize_remote_worker_tree(project_root: Path, ref: str, config_index: dict[str, dict]) -> dict:
    result_root = "experiments/exp2_scaled/results"
    paths = git_tree_paths(project_root, ref, result_root)
    result_files = {path for path in paths if path.endswith("/results.json")}
    instance_counts: dict[str, int] = {}

    for path in paths:
        if "/instances/" not in path or not path.endswith(".json"):
            continue
        run_dir = path.split("/instances/", 1)[0]
        instance_counts[run_dir] = instance_counts.get(run_dir, 0) + 1

    active_runs = [
        (run_dir, count)
        for run_dir, count in instance_counts.items()
        if f"{run_dir}/results.json" not in result_files
    ]
    active_runs.sort(key=lambda item: item[1], reverse=True)

    if active_runs:
        output_dir, done = active_runs[0]
        experiment = "_".join(Path(output_dir).parts[-3:])
        total = target_for_result_dir(output_dir, config_index)
        status = "running-or-partial"
    else:
        output_dir = "unknown"
        experiment = "no active run detected"
        done = 0
        total = 0
        status = "idle-or-complete"

    return {
        "worker_id": normalize_remote_worker_branch(ref),
        "branch": ref,
        "source": "tree",
        "experiment": experiment,
        "status": status,
        "done": done,
        "total": total,
        "latest_checkpoint": None,
        "latest_write": None,
        "results_json_exists": False,
        "output_dir": output_dir,
    }


def collect_remote_workers(
    project_root: Path,
    config_index: dict[str, dict],
    fetch_remote_workers: bool,
    remote_fetch_interval: int,
) -> dict:
    fetched, fetch_status = maybe_fetch_remote_worker_branches(
        project_root, fetch_remote_workers, remote_fetch_interval
    )
    workers: list[dict] = []

    for ref in get_remote_worker_refs(project_root):
        manifest = get_remote_worker_manifest(project_root, ref)
        if manifest:
            workers.append(remote_worker_from_manifest(ref, manifest, config_index))
        else:
            workers.append(summarize_remote_worker_tree(project_root, ref, config_index))

    workers.sort(
        key=lambda item: (
            item.get("latest_checkpoint") or item.get("latest_write") or datetime.min,
            item.get("done") or 0,
        ),
        reverse=True,
    )

    return {
        "enabled": fetch_remote_workers,
        "fetched": fetched,
        "fetch_status": fetch_status,
        "workers": workers,
    }


def discover_active_experiments(results_dir: Path, config_index: dict[str, dict]) -> tuple[int, list[dict]]:
    active_instances = 0
    active_experiments: list[dict] = []

    instance_dirs = list(results_dir.glob("**/instances"))
    for inst_dir in sorted(instance_dirs):
        parent = inst_dir.parent
        if (parent / "results.json").exists():
            continue

        count = len(list(inst_dir.glob("*.json")))
        active_instances += count

        rel_path = parent.relative_to(results_dir)
        parts = rel_path.parts
        if len(parts) < 3:
            continue

        method, seed, n_value = parts[-3], parts[-2], parts[-1]
        display_name = f"{method}_{seed}_{n_value}"

        res_norm = normalize_name(display_name)
        res_norm_short = res_norm.replace("seed", "s")
        cfg = config_index.get(res_norm_short) or config_index.get(res_norm)
        target = get_target_instances(cfg) if cfg else 400
        latest_file = None
        latest_write = None
        if count:
            latest_file = max(inst_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, default=None)
            latest_write = datetime.fromtimestamp(latest_file.stat().st_mtime) if latest_file else None

        active_experiments.append(
            {
                "name": display_name,
                "done": count,
                "total": target,
                "output_dir": str(parent),
                "instances_dir": str(inst_dir),
                "latest_file": latest_file.name if latest_file else None,
                "latest_write": latest_write,
            }
        )

    active_experiments.sort(
        key=lambda item: (
            item["latest_write"] or datetime.min,
            item["done"],
        ),
        reverse=True,
    )
    return active_instances, active_experiments


def get_completed_instance_count(result_files: list[Path]) -> int:
    completed_instances = 0
    for path in result_files:
        try:
            with path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            completed_instances += len(payload.get("instance_evaluations", []))
        except Exception:
            continue
    return completed_instances


def get_recent_completed_runs(result_files: list[Path], limit: int = 5) -> list[dict]:
    recent: list[dict] = []
    for path in sorted(result_files, key=lambda p: p.stat().st_mtime, reverse=True)[:limit]:
        try:
            with path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            recent.append(
                {
                    "path": str(path.parent),
                    "name": path.parent.relative_to(path.parents[3]).as_posix(),
                    "completed_at": datetime.fromtimestamp(path.stat().st_mtime),
                    "instances": len(payload.get("instance_evaluations", [])),
                }
            )
        except Exception:
            recent.append(
                {
                    "path": str(path.parent),
                    "name": path.parent.name,
                    "completed_at": datetime.fromtimestamp(path.stat().st_mtime),
                    "instances": "?",
                }
            )
    return recent


def collect_status(
    project_root: Path,
    config_dir: Path,
    results_dir: Path,
    log_file: Path,
    fetch_remote_workers: bool,
    remote_fetch_interval: int,
) -> dict:
    config_paths = sorted(config_dir.glob("*.yaml"))
    result_files = sorted(results_dir.glob("**/results.json"))
    config_index = build_config_index(config_paths)

    total_target_instances = 0
    for config_path in config_paths:
        cfg = load_yaml(config_path)
        if cfg:
            total_target_instances += get_target_instances(cfg)

    completed_instances = get_completed_instance_count(result_files)
    active_instances, active_experiments = discover_active_experiments(results_dir, config_index)

    total_done = completed_instances + active_instances
    pct = (total_done / total_target_instances * 100) if total_target_instances else 0.0

    remaining = max(total_target_instances - total_done, 0)
    eta_seconds = remaining * 10

    mem = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=0.1)

    return {
        "timestamp": datetime.now(),
        "cpu_percent": cpu_percent,
        "mem_available_gb": mem.available / (1024**3),
        "mem_used_percent": mem.percent,
        "load": get_load_average(),
        "total_configs": len(config_paths),
        "finished_configs": len(result_files),
        "completed_instances": completed_instances,
        "active_instances": active_instances,
        "total_target_instances": total_target_instances,
        "progress_pct": pct,
        "active": active_experiments,
        "current_result": active_experiments[0] if active_experiments else None,
        "recent_completed": get_recent_completed_runs(result_files),
        "live_runner": get_live_runner_process(),
        "eta": timedelta(seconds=int(eta_seconds)),
        "last_git": get_last_commit(project_root),
        "branch_status": get_branch_status(project_root),
        "log_lines": get_recent_log_lines(log_file),
        "log_file": str(log_file),
        "config_dir": str(config_dir),
        "results_dir": str(results_dir),
        "main_sync": get_main_sync_status(project_root),
        "remote_workers": collect_remote_workers(
            project_root,
            config_index,
            fetch_remote_workers,
            remote_fetch_interval,
        ),
    }


def bar(done: int, total: int, width: int = 24) -> str:
    if total <= 0:
        return "-" * width
    pct = max(0.0, min(done / total, 1.0))
    filled = int(round(pct * width))
    return "#" * filled + "." * (width - filled)


def draw(status: dict, interval: int) -> None:
    clear_screen()

    print("=" * 88)
    print("XAI EXPERIMENT DASHBOARD".center(88))
    print("=" * 88)
    print(f"Updated: {status['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Git: {status['branch_status']}")
    print(f"Last Commit: {status['last_git']}")
    print("-" * 88)
    print("System")
    print(
        f"CPU: {status['cpu_percent']:.1f}%  |  RAM Free: {status['mem_available_gb']:.2f} GB"
        f"  |  RAM Used: {status['mem_used_percent']:.1f}%  |  Load: {status['load']}"
    )
    print("-" * 88)
    print("Overall Progress")
    print(f"Configs Finished: {status['finished_configs']} / {status['total_configs']}")
    print(
        "Instances: "
        f"{status['completed_instances'] + status['active_instances']:,} / "
        f"{status['total_target_instances']:,} ({status['progress_pct']:.2f}%)"
    )
    print(f"ETA: ~ {status['eta']} remaining")
    print("-" * 88)
    print("Active Experiments")

    if not status["active"]:
        print("Waiting for scheduler or no in-progress instance folders detected.")
    else:
        for exp in status["active"][:8]:
            pct = (exp["done"] / exp["total"] * 100) if exp["total"] else 0.0
            age_min = (
                f"{((status['timestamp'] - exp['latest_write']).total_seconds() / 60):.1f}m"
                if exp.get("latest_write")
                else "n/a"
            )
            print(
                f"{exp['name'][:36]:<36} "
                f"[{bar(exp['done'], exp['total'])}] "
                f"{exp['done']}/{exp['total']} ({pct:5.1f}%) last:{age_min}"
            )

    print("-" * 88)
    print("Live Worker")
    runner = status.get("live_runner")
    if not runner:
        print("No active src.experiment.runner process detected.")
    else:
        started_at = runner["started_at"].strftime("%Y-%m-%d %H:%M:%S") if runner.get("started_at") else "unknown"
        config = runner.get("config") or "unknown"
        print(f"PID: {runner['pid']}  |  Started: {started_at}")
        print(f"Config: {config}"[:88])

    print("-" * 88)
    print("Current Results")
    current = status.get("current_result")
    if not current:
        print("No active result directory detected.")
    else:
        latest_age = (
            f"{((status['timestamp'] - current['latest_write']).total_seconds() / 60):.1f} min ago"
            if current.get("latest_write")
            else "n/a"
        )
        print(f"Run: {current['name']}")
        print(f"Output: {current['output_dir']}"[:88])
        print(
            f"Instances Complete: {current['done']} / {current['total']}  |  "
            f"Latest Write: {latest_age}  |  Latest File: {current.get('latest_file') or 'n/a'}"
        )

    print("-" * 88)
    print("Recent Completed Runs")
    if not status["recent_completed"]:
        print("No completed results.json files found.")
    else:
        for item in status["recent_completed"]:
            completed_at = item["completed_at"].strftime("%Y-%m-%d %H:%M:%S")
            print(
                f"{completed_at}  {str(item['instances']).rjust(4)} inst  {item['name']}"[:88]
            )

    print("-" * 88)
    print("Main Branch Sync")
    main_sync = status.get("main_sync", {})
    print(f"origin/main HEAD: {main_sync.get('main_head', 'Unknown')}")
    print(
        "Latest main results commit: "
        f"{main_sync.get('main_results_last_commit', 'Unknown')}"
    )
    print(
        "Result files pending this branch -> main: "
        f"{main_sync.get('pending_to_main_files', '?')}  |  "
        "main-only result files not in this branch: "
        f"{main_sync.get('pending_from_main_files', '?')}"
    )
    print("-" * 88)
    print("Remote Worker Branches")
    remote_workers = status.get("remote_workers", {})
    fetch_label = remote_workers.get("fetch_status", "unknown")
    print(f"Remote refresh: {fetch_label}")
    workers = remote_workers.get("workers", [])
    if not workers:
        print("No origin/results/* worker branches detected.")
    else:
        for worker in workers[:8]:
            done = worker.get("done") or 0
            total = worker.get("total") or 0
            pct = (done / total * 100) if total else 0.0
            timestamp = worker.get("latest_checkpoint") or worker.get("latest_write")
            age = (
                f"{((status['timestamp'] - timestamp).total_seconds() / 60):.1f}m"
                if timestamp
                else "n/a"
            )
            print(
                f"{worker.get('worker_id', '?')[:16]:<16} "
                f"{worker.get('experiment', 'unknown')[:28]:<28} "
                f"[{bar(done, total, 14)}] {done}/{total} "
                f"({pct:5.1f}%) {worker.get('status', '?')[:10]:<10} "
                f"{worker.get('source', '?'):<8} age:{age}"
            )
            print(f"  {worker.get('branch', '?')} -> {worker.get('output_dir', '?')}"[:88])
    print("-" * 88)
    print(f"Recent Log Tail: {status['log_file']}")
    for line in status["log_lines"]:
        print(line[:88])
    print("=" * 88)
    print(f"Refresh: {interval}s | Press Ctrl+C to exit")


def main() -> int:
    parser = argparse.ArgumentParser(description="Cross-platform XAI experiment dashboard")
    parser.add_argument("--interval", type=int, default=5, help="Refresh interval in seconds")
    parser.add_argument("--config-dir", default=str(DEFAULT_CONFIG_DIR), help="Directory containing config YAMLs")
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR), help="Directory containing experiment results")
    parser.add_argument("--log-file", default=str(DEFAULT_LOG_FILE), help="Managed runner log file")
    parser.add_argument(
        "--no-remote-workers",
        action="store_true",
        help="Disable read-only origin/results/* worker branch summaries",
    )
    parser.add_argument(
        "--remote-fetch-interval",
        type=int,
        default=300,
        help="Seconds between read-only fetches of origin/results/* worker branches",
    )
    args = parser.parse_args()

    project_root = PROJECT_ROOT
    config_dir = Path(args.config_dir).resolve()
    results_dir = Path(args.results_dir).resolve()
    log_file = Path(args.log_file).resolve()

    try:
        while True:
            status = collect_status(
                project_root,
                config_dir,
                results_dir,
                log_file,
                fetch_remote_workers=not args.no_remote_workers,
                remote_fetch_interval=args.remote_fetch_interval,
            )
            draw(status, args.interval)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nDashboard exited. Background experiments continue running.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
