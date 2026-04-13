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


def discover_active_experiments(results_dir: Path, config_index: dict[str, dict], main_paths: set = None) -> tuple[int, list[dict]]:
    if main_paths is None:
        main_paths = set()
        
    active_instances = 0
    active_experiments: list[dict] = []

    instance_dirs = list(results_dir.glob("**/instances"))
    for inst_dir in sorted(instance_dirs):
        parent = inst_dir.parent
        parent_norm = str(parent.relative_to(results_dir.parent)).replace(os.sep, "/")
        
        # Skip if this experiment is already finished on origin/main
        if any(p.startswith(f"{parent_norm}/results.json") for p in main_paths):
            continue

        # Union of local files and files already on origin/main for this directory
        local_files = {f.name for f in inst_dir.glob("*.json")}
        main_files_here = {
            os.path.basename(p) for p in main_paths
            if p.startswith(f"{parent_norm}/instances/") and p.endswith(".json")
        }
        count = len(local_files | main_files_here)
        if count == 0:
            continue
            
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


def collect_status(project_root: Path, config_dir: Path, results_dir: Path, log_file: Path) -> dict:
    import subprocess
    
    config_paths = sorted(config_dir.glob("*.yaml"))
    config_index = build_config_index(config_paths)

    # Fetch origin/main to get cross-workstation global progress
    subprocess.run(
        ["git", "fetch", "origin", "--prune", "--quiet"],
        cwd=str(project_root),
        check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    # Get finished configs and completed instances from origin/main
    try:
        main_tree_raw = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", "origin/main", "--",
             "experiments/exp2_scaled/results"],
            text=True, cwd=str(project_root)
        )
        main_paths = set(main_tree_raw.strip().splitlines())
    except subprocess.CalledProcessError:
        main_paths = set()
    
    # Finished configs = dirs with results.json on origin/main
    finished_dirs_main = {os.path.dirname(p) for p in main_paths if p.endswith("/results.json")}
    
    # Completed instances = instance JSON count in finished dirs on origin/main
    completed_instances = sum(
        1 for p in main_paths
        if '/instances/' in p and p.endswith('.json')
        and p.split('/instances/')[0] in finished_dirs_main
    )
    
    # Also load local result files for recent_completed_runs display
    result_files = sorted(results_dir.glob("**/results.json"))
    
    total_target_instances = 0
    for config_path in config_paths:
        cfg = load_yaml(config_path)
        if cfg:
            total_target_instances += get_target_instances(cfg)

    active_instances, active_experiments = discover_active_experiments(results_dir, config_index, main_paths)

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
        "finished_configs": len(finished_dirs_main),
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
    args = parser.parse_args()

    project_root = PROJECT_ROOT
    config_dir = Path(args.config_dir).resolve()
    results_dir = Path(args.results_dir).resolve()
    log_file = Path(args.log_file).resolve()

    try:
        while True:
            status = collect_status(project_root, config_dir, results_dir, log_file)
            draw(status, args.interval)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nDashboard exited. Background experiments continue running.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
