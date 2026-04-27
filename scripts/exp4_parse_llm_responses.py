#!/usr/bin/env python3
"""Parse and validate EXP4 raw LLM responses."""

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
    parser.add_argument("--manifest", type=Path, default=Path("configs/experiments/exp4_llm_evaluation/manifest.yaml"))
    args = parser.parse_args()

    summary = parse_manifest_responses(args.manifest)
    print(f"Parsed {summary['parsed_count']} responses; failures: {summary['failure_count']}")
    print(f"Scores: {summary['scores_path']}")


if __name__ == "__main__":
    main()
