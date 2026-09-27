"""Rebuild the original 192-case EXP4 inventory from tracked EXP2/EXP3 results.

NEW 2026-09-27 (not a reconstruction). The original case inventory was lost
with the raw judge data (RCA-002), but its 192 case IDs survive in the
committed outputs/analysis/exp4_llm_evaluation/judge_disagreement.csv. A case
ID is a hash of the case's provenance fields and its results.json path
(src/evaluation/exp4_cases.py::_stable_case_id); the original run rendered that
path Windows-style and relative to the repository root. This script recomputes
the ID of every candidate instance under the two source experiments, keeps the
ones whose ID is in the committed set, and writes them with the standard
inventory writer.

It selects by ID, not by re-sampling: sample_cases(pool, 192, seed=42) over
today's results reproduces only 121 of the 192, because the candidate pool has
changed since the original run. It refuses to write anything unless all 192
IDs are recovered exactly once.
"""
from __future__ import annotations

import argparse
import csv
import io
import subprocess
import sys
from pathlib import Path, PureWindowsPath

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.exp4_cases import (  # noqa: E402
    _cases_from_results_file,
    _stable_case_id,
    write_case_inventory,
)

SOURCES = {
    "exp2_scaled": "experiments/exp2_scaled/results",
    "exp3_cross_dataset": "experiments/exp3_cross_dataset/results",
}
ORIGINAL_IDS = "outputs/analysis/exp4_llm_evaluation/judge_disagreement.csv"
ORIGINAL_SEED = 42


def original_case_ids() -> list[str]:
    """The 192 case IDs of the original cohort, read from the committed blob."""
    blob = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"HEAD:{ORIGINAL_IDS}"],
        capture_output=True, text=True, check=True,
    ).stdout
    return [row["case_id"] for row in csv.DictReader(io.StringIO(blob))]


def recover(target_ids: set[str]):
    found, candidates = {}, []
    for source, root in SOURCES.items():
        for path in sorted((ROOT / root).rglob("results.json")):
            original_path = str(PureWindowsPath(path.relative_to(ROOT)))
            for case in _cases_from_results_file(path, source):
                case_id = _stable_case_id(
                    case.source_experiment, case.dataset, case.model_family,
                    case.explainer, str(case.random_seed), str(case.sample_size),
                    case.instance_id, original_path,
                )
                case = case.model_copy(
                    update={"case_id": case_id, "source_artifact_path": original_path}
                )
                candidates.append(case)
                if case_id in target_ids:
                    if case_id in found:
                        raise SystemExit(f"case id {case_id} recovered twice")
                    found[case_id] = case
    return found, candidates


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    ordered_ids = original_case_ids()
    found, candidates = recover(set(ordered_ids))
    missing = [cid for cid in ordered_ids if cid not in found]
    if missing or len(found) != 192:
        print(f"FAILED: recovered {len(found)}/192; missing {missing[:5]}")
        return 1

    cases = [found[cid] for cid in ordered_ids]
    report = write_case_inventory(
        cases, candidates, args.output_dir, target_cases=192, seed=ORIGINAL_SEED
    )
    print(
        f"OK: recovered {report['selected_cases']}/192 original EXP4 cases from "
        f"{report['candidate_cases']} candidates -> {args.output_dir.as_posix()}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
