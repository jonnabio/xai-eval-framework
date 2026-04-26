#!/usr/bin/env python3
"""Email progress reports for XAI experiment runs.

Defaults target EXP3, but the paths are configurable so the script can still be
used for older experiment families. The report is project-root aware and works
from Linux, WSL, Windows PowerShell, cron, and Windows Task Scheduler.
"""

from __future__ import annotations

import argparse
import json
import os
import smtplib
import subprocess
import tempfile
from datetime import datetime
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_DIR = "configs/experiments/exp3_cross_dataset"
DEFAULT_RESULTS_DIR = "experiments/exp3_cross_dataset/results"
DEFAULT_LOG_FILE = "logs/managed_runner_exp3.log"
DEFAULT_TO_EMAIL = "jonnabio@gmail.com"
RESULT_BRANCH_REFSPEC = "+refs/heads/results/*:refs/remotes/origin/results/*"


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def normalize_path(path: str | Path) -> str:
    return str(path).replace("\\", "/").strip("/")


def read_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def get_target_instances(config: dict) -> int:
    sampling = config.get("sampling") or {}
    samples_per_class = int(sampling.get("samples_per_class") or 0)
    if samples_per_class:
        return samples_per_class * 4
    sample_size = sampling.get("sample_size") or sampling.get("n_samples")
    return int(sample_size or 0)


def build_config_index(config_dir: Path) -> tuple[list[Path], dict[str, dict]]:
    config_paths = sorted(p for p in config_dir.rglob("*.yaml") if p.name != "manifest.yaml")
    index: dict[str, dict] = {}
    for path in config_paths:
        config = read_yaml(path)
        output_dir = config.get("output_dir")
        if not output_dir:
            continue
        index[normalize_path(output_dir)] = {
            "path": path,
            "name": config.get("name") or path.stem,
            "dataset": config.get("dataset", "?"),
            "target": get_target_instances(config),
        }
    return config_paths, index


def fetch_remote_state(enabled: bool) -> str:
    if not enabled:
        return "remote fetch disabled"

    messages: list[str] = []
    main_fetch = run_git(["fetch", "--no-progress", "--prune", "origin"])
    messages.append("origin fetch ok" if main_fetch.returncode == 0 else "origin fetch failed")

    result_fetch = run_git(["fetch", "--no-progress", "--prune", "origin", RESULT_BRANCH_REFSPEC])
    messages.append("result branches fetch ok" if result_fetch.returncode == 0 else "result branches fetch failed")
    return "; ".join(messages)


def list_remote_refs() -> list[str]:
    result = run_git(
        [
            "for-each-ref",
            "--format=%(refname:short)",
            "refs/remotes/origin/main",
            "refs/remotes/origin/results",
        ]
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def list_paths_at_ref(ref: str, root: str) -> set[str]:
    result = run_git(["ls-tree", "-r", "--name-only", ref, "--", root])
    if result.returncode != 0:
        return set()
    return {normalize_path(line) for line in result.stdout.splitlines() if line.strip()}


def collect_remote_paths(results_dir: str) -> tuple[set[str], dict[str, int]]:
    paths: set[str] = set()
    branch_counts: dict[str, int] = {}
    for ref in list_remote_refs():
        ref_paths = list_paths_at_ref(ref, results_dir)
        if not ref_paths:
            continue
        result_count = sum(1 for path in ref_paths if path.endswith("/results.json"))
        if result_count:
            branch_counts[ref] = result_count
        paths.update(ref_paths)
    return paths, branch_counts


def local_result_paths(results_dir: Path) -> set[str]:
    if not results_dir.exists():
        return set()
    return {normalize_path(path.relative_to(PROJECT_ROOT)) for path in results_dir.rglob("*") if path.is_file()}


def read_result_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def local_completed_instances(result_files: list[Path]) -> int:
    total = 0
    for path in result_files:
        payload = read_result_json(path)
        evaluations = payload.get("instance_evaluations")
        if isinstance(evaluations, list):
            total += len(evaluations)
    return total


def result_name_from_path(path: Path) -> str:
    payload = read_result_json(path)
    metadata = payload.get("experiment_metadata") or {}
    if metadata.get("name"):
        return str(metadata["name"])
    return normalize_path(path.parent.relative_to(PROJECT_ROOT))


def summarize_active_runs(results_dir: Path, config_index: dict[str, dict]) -> tuple[int, list[str]]:
    active_instances = 0
    lines: list[str] = []
    if not results_dir.exists():
        return active_instances, lines

    for instances_dir in sorted(results_dir.rglob("instances")):
        run_dir = instances_dir.parent
        if (run_dir / "results.json").exists():
            continue

        instance_count = len(list(instances_dir.glob("*.json")))
        active_instances += instance_count
        output_key = normalize_path(run_dir.relative_to(PROJECT_ROOT))
        config = config_index.get(output_key, {})
        target = int(config.get("target") or 0)
        name = config.get("name") or output_key
        pct = (instance_count / target * 100) if target else 0.0
        lines.append(f"- {name}: {instance_count}/{target or '?'} ({pct:.1f}%)")

    return active_instances, lines


def recent_log_lines(log_file: Path, limit: int = 12) -> list[str]:
    if not log_file.exists():
        return ["No log file found."]
    try:
        lines = log_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as exc:
        return [f"Could not read log file: {exc}"]
    return lines[-limit:] if lines else ["Log file is empty."]


def git_summary() -> list[str]:
    lines: list[str] = []
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    lines.append(f"Current branch: {branch.stdout.strip() if branch.returncode == 0 else 'unknown'}")

    status = run_git(["status", "--short", "--branch", "--untracked-files=no"])
    if status.stdout.strip():
        lines.append(status.stdout.strip())

    log = run_git(["log", "-n", "8", "--pretty=format:%h %ai %s"])
    if log.stdout.strip():
        lines.append("")
        lines.append("Recent local commits:")
        lines.append(log.stdout.strip())
    return lines


def generate_report(
    *,
    title: str,
    config_dir: Path,
    results_dir: Path,
    log_file: Path,
    fetch_remote: bool,
) -> str:
    config_paths, config_index = build_config_index(config_dir)
    results_root = normalize_path(results_dir.relative_to(PROJECT_ROOT))
    remote_status = fetch_remote_state(fetch_remote)
    remote_paths, branch_counts = collect_remote_paths(results_root) if fetch_remote else (set(), {})
    local_paths = local_result_paths(results_dir)
    all_paths = local_paths | remote_paths

    local_result_files = sorted(results_dir.rglob("results.json")) if results_dir.exists() else []
    result_dirs_all = {path.removesuffix("/results.json") for path in all_paths if path.endswith("/results.json")}
    completed_configs = len(result_dirs_all)

    total_target_instances = sum(int(item.get("target") or 0) for item in config_index.values())
    completed_instances_local = local_completed_instances(local_result_files)
    remote_instance_count = sum(1 for path in remote_paths if "/instances/" in path and path.endswith(".json"))
    local_instance_count = sum(1 for path in local_paths if "/instances/" in path and path.endswith(".json"))
    active_instances, active_lines = summarize_active_runs(results_dir, config_index)
    known_instances = max(completed_instances_local + active_instances, local_instance_count, remote_instance_count)
    progress_pct = (known_instances / total_target_instances * 100) if total_target_instances else 0.0

    lines: list[str] = []
    lines.append(f"{title} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 72)
    lines.append(f"Project root: {PROJECT_ROOT}")
    lines.append(f"Config dir: {normalize_path(config_dir.relative_to(PROJECT_ROOT))}")
    lines.append(f"Results dir: {results_root}")
    lines.append(f"Remote status: {remote_status}")
    lines.append("")
    lines.append("### Run Progress")
    lines.append(f"Configs finished: {completed_configs} / {len(config_paths)}")
    lines.append(f"Known instance files/evaluations: {known_instances} / {total_target_instances} ({progress_pct:.2f}%)")
    lines.append(f"Local completed result files: {len(local_result_files)}")
    lines.append(f"Local active checkpoint instances: {active_instances}")
    lines.append("")

    lines.append("### Active Local Runs")
    if active_lines:
        lines.extend(active_lines)
    else:
        lines.append("No active local checkpoint folders found.")
    lines.append("")

    lines.append("### Recent Local Completed Runs")
    if local_result_files:
        for path in sorted(local_result_files, key=lambda p: p.stat().st_mtime, reverse=True)[:8]:
            rel_path = normalize_path(path.relative_to(PROJECT_ROOT))
            payload = read_result_json(path)
            count = len(payload.get("instance_evaluations") or [])
            lines.append(f"- {result_name_from_path(path)}: {count} instances ({rel_path})")
    else:
        lines.append("No local results.json files found.")
    lines.append("")

    lines.append("### Remote Result Branches")
    if branch_counts:
        for branch, count in sorted(branch_counts.items()):
            lines.append(f"- {branch}: {count} completed result file(s)")
    else:
        lines.append("No pushed result branch completions found.")
    lines.append("")

    lines.append("### Recent Log Tail")
    lines.extend(recent_log_lines(log_file))
    lines.append("")

    lines.append("### Git")
    lines.extend(git_summary())
    return "\n".join(lines)


def send_email(subject: str, body: str, to_email: str) -> None:
    gmail_user = os.environ.get("GMAIL_USER", DEFAULT_TO_EMAIL)
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD")

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = f"{subject} [{datetime.now().strftime('%H:%M:%S')}]"
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()

    if not gmail_password:
        output_path = Path(tempfile.gettempdir()) / "latest_xai_report.txt"
        output_path.write_text(f"To: {to_email}\nSubject: {subject}\n\n{body}", encoding="utf-8")
        print("WARNING: GMAIL_APP_PASSWORD environment variable not set.")
        print(f"Saved report locally to {output_path} instead of emailing.")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        print(f"Successfully sent automated email report to {to_email} via Gmail SMTP.")
    except Exception as exc:
        output_path = Path(tempfile.gettempdir()) / "latest_xai_report.txt"
        output_path.write_text(f"To: {to_email}\nSubject: {subject}\n\n{body}", encoding="utf-8")
        print(f"Failed to send email. Ensure your App Password is correct. Error: {exc}")
        print(f"Saved report locally to {output_path}.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send an XAI experiment progress email.")
    parser.add_argument("--experiment", default="EXP3 Cross-Dataset", help="Experiment label for report headings.")
    parser.add_argument("--config-dir", default=DEFAULT_CONFIG_DIR, help="Directory containing experiment YAML configs.")
    parser.add_argument("--results-dir", default=DEFAULT_RESULTS_DIR, help="Directory containing experiment results.")
    parser.add_argument("--log-file", default=DEFAULT_LOG_FILE, help="Runner log file to include in the report.")
    parser.add_argument("--to-email", default=os.environ.get("XAI_REPORT_TO", DEFAULT_TO_EMAIL))
    parser.add_argument("--subject", default=None, help="Email subject. Also used by watchdog alert mode.")
    parser.add_argument("--message", default=None, help="Send a direct message instead of generating a progress report.")
    parser.add_argument("--no-fetch", action="store_true", help="Do not fetch origin/main or origin/results/* before reporting.")
    parser.add_argument("--print-only", action="store_true", help="Print the report instead of sending email.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    os.chdir(PROJECT_ROOT)

    subject = args.subject or f"XAI Framework {args.experiment} Progress Report"
    if args.message is not None:
        body = args.message
    else:
        body = generate_report(
            title=f"XAI Eval Framework {args.experiment} Status Report",
            config_dir=(PROJECT_ROOT / args.config_dir).resolve(),
            results_dir=(PROJECT_ROOT / args.results_dir).resolve(),
            log_file=(PROJECT_ROOT / args.log_file).resolve(),
            fetch_remote=not args.no_fetch,
        )

    if args.print_only:
        print(body)
    else:
        send_email(subject, body, args.to_email)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
