"""Build the EXP4 case inventory from EXP2/EXP3 results.

RECONSTRUCTED SOURCE -- see docs/rca/RCA-002-exp4-source-recovery.md.
Rebuilt from scripts/__pycache__/exp4_build_cases.cpython-312.pyc. Structurally
verified (names, constants, docstrings); no CPython 3.12 interpreter is
available here, so the opcode-level check applied to src/evaluation/exp4_*.py
could not be run against this file.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.exp4_cases import build_case_inventory


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default="configs/experiments/exp4_llm_evaluation/manifest.yaml",
    )
    parser.add_argument("--target-cases", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    report = build_case_inventory(
        args.manifest, target_cases=args.target_cases, seed=args.seed
    )
    print(
        f"Selected {report['selected_cases']} EXP4 cases from "
        f"{report['candidate_cases']} candidates"
    )
    print(f"Wrote {report['jsonl_path']}")


if __name__ == "__main__":
    main()
