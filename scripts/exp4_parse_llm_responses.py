"""Parse and validate EXP4 raw LLM responses.

RECONSTRUCTED SOURCE -- see docs/rca/RCA-002-exp4-source-recovery.md.
Rebuilt from scripts/__pycache__/exp4_parse_llm_responses.cpython-312.pyc.
Structurally verified only; see exp4_build_cases.py for why.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.exp4_parser import parse_manifest_responses


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default="configs/experiments/exp4_llm_evaluation/manifest.yaml",
    )
    args = parser.parse_args()

    summary = parse_manifest_responses(args.manifest)
    print(
        f"Parsed {summary['parsed_count']} responses; "
        f"failures: {summary['failure_count']}"
    )
    print(f"Scores: {summary['scores_path']}")


if __name__ == "__main__":
    main()
