#!/usr/bin/env python3
"""Live console dashboard for EXP4 LLM judge execution progress.

Usage:
  python scripts/exp4_judge_dashboard.py
  python scripts/exp4_judge_dashboard.py --interval 10
  python scripts/exp4_judge_dashboard.py --once
  python scripts/exp4_judge_dashboard.py --judges openai_gpt41,openrouter_gpt41_mini
"""

from __future__ import annotations

import argparse
import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.exp4_cases import load_manifest


@dataclass
class JudgeStatus:
    judge_id: str
    done: int
    total: int
    by_condition: Dict[str, int]
    latest_write: Optional[datetime]


def _clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _progress_bar(done: int, total: int, width: int = 24) -> str:
    if total <= 0:
        return "-" * width
    ratio = max(0.0, min(done / total, 1.0))
    filled = int(round(ratio * width))
    return "#" * filled + "." * (width - filled)


def _fmt_tdelta(delta: Optional[timedelta]) -> str:
    if delta is None:
        return "n/a"
    secs = int(delta.total_seconds())
    if secs < 0:
        secs = 0
    return str(timedelta(seconds=secs))


def _count_case_rows(cases_jsonl: Path) -> int:
    if not cases_jsonl.exists():
        return 0
    count = 0
    with cases_jsonl.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                count += 1
    return count


def _collect_judge_status(raw_root: Path, judge_id: str, conditions: List[str], target: int) -> JudgeStatus:
    judge_root = raw_root / judge_id
    by_condition: Dict[str, int] = {}
    latest_mtime = 0.0

    for cond in conditions:
        cond_dir = judge_root / cond
        if not cond_dir.exists():
            by_condition[cond] = 0
            continue
        files = list(cond_dir.rglob("*.json"))
        by_condition[cond] = len(files)
        for file_path in files:
            try:
                latest_mtime = max(latest_mtime, file_path.stat().st_mtime)
            except OSError:
                continue

    done = sum(by_condition.values())
    latest_write = datetime.fromtimestamp(latest_mtime) if latest_mtime else None
    return JudgeStatus(judge_id=judge_id, done=done, total=target, by_condition=by_condition, latest_write=latest_write)


def _render(
    manifest_path: Path,
    statuses: List[JudgeStatus],
    conditions: List[str],
    replicates: int,
    case_count: int,
    interval: int,
    rates_per_sec: Dict[str, float],
) -> None:
    _clear_screen()
    now = datetime.now()

    total_target = sum(item.total for item in statuses)
    total_done = sum(item.done for item in statuses)
    total_pct = (100.0 * total_done / total_target) if total_target else 0.0

    print("=" * 108)
    print("EXP4 JUDGE PROGRESS DASHBOARD".center(108))
    print("=" * 108)
    print(f"Updated: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Manifest: {manifest_path}")
    print(
        "Scope: "
        f"cases={case_count}, conditions={len(conditions)} ({', '.join(conditions)}), replicates={replicates}"
    )
    print("-" * 108)
    print(f"Overall: {total_done:,}/{total_target:,} ({total_pct:.1f}%)")
    print("-" * 108)

    header = (
        f"{'Judge':<26} {'Progress':<38} {'Done/Total':<14} {'Rate':<11} "
        f"{'ETA':<12} {'Last Write'}"
    )
    print(header)
    print("-" * 108)

    for status in statuses:
        pct = (100.0 * status.done / status.total) if status.total else 0.0
        rate = rates_per_sec.get(status.judge_id, 0.0)
        remaining = max(status.total - status.done, 0)
        eta = timedelta(seconds=int(remaining / rate)) if rate > 0 else None
        age = (now - status.latest_write) if status.latest_write else None
        last_write_text = (
            f"{status.latest_write.strftime('%H:%M:%S')} ({_fmt_tdelta(age)} ago)"
            if status.latest_write
            else "n/a"
        )
        rate_text = f"{rate * 60:.1f}/min" if rate > 0 else "n/a"

        print(
            f"{status.judge_id:<26} "
            f"[{_progress_bar(status.done, status.total, 24)}] {pct:5.1f}% "
            f"{status.done:>5}/{status.total:<7} "
            f"{rate_text:<11} {_fmt_tdelta(eta):<12} {last_write_text}"
        )

        cond_parts = [f"{cond}: {status.by_condition.get(cond, 0)}" for cond in conditions]
        print(f"  by condition -> {' | '.join(cond_parts)}")

    print("=" * 108)
    print(f"Refresh: {interval}s | Ctrl+C to exit")


def main() -> int:
    parser = argparse.ArgumentParser(description="Live EXP4 judge progress dashboard")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("configs/experiments/exp4_llm_evaluation/manifest.yaml"),
        help="Path to EXP4 manifest",
    )
    parser.add_argument("--interval", type=int, default=5, help="Refresh interval in seconds")
    parser.add_argument(
        "--judges",
        type=str,
        default="",
        help="Comma-separated judge_ids to display (default: all judges in manifest)",
    )
    parser.add_argument("--once", action="store_true", help="Print one snapshot and exit")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    raw_root = manifest.paths.raw_responses_dir
    conditions = list(manifest.prompt_conditions)
    replicates = int(manifest.replicates)

    case_count = _count_case_rows(manifest.paths.cases_dir / "exp4_cases.jsonl")
    if case_count <= 0:
        case_count = int(manifest.case_inventory.target_cases)

    all_judges = [judge.judge_id for judge in manifest.judges]
    wanted = [item.strip() for item in args.judges.split(",") if item.strip()]
    judge_ids = wanted if wanted else all_judges

    unknown = sorted(set(judge_ids) - set(all_judges))
    if unknown:
        raise ValueError(f"Unknown judge_id(s): {unknown}. Known judges: {all_judges}")

    target_per_judge = case_count * len(conditions) * replicates

    prev_snapshot: Dict[str, tuple[datetime, int]] = {}
    rates_per_sec: Dict[str, float] = {}

    while True:
        statuses = [
            _collect_judge_status(raw_root, judge_id, conditions, target_per_judge)
            for judge_id in judge_ids
        ]

        now = datetime.now()
        for status in statuses:
            prev = prev_snapshot.get(status.judge_id)
            if prev:
                prev_time, prev_done = prev
                dt = (now - prev_time).total_seconds()
                dd = status.done - prev_done
                if dt > 0 and dd >= 0:
                    rates_per_sec[status.judge_id] = dd / dt
            prev_snapshot[status.judge_id] = (now, status.done)

        _render(args.manifest, statuses, conditions, replicates, case_count, args.interval, rates_per_sec)

        if args.once:
            return 0

        time.sleep(max(1, args.interval))


if __name__ == "__main__":
    raise SystemExit(main())
