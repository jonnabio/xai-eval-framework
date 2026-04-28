#!/usr/bin/env python3
"""Analyze parsed EXP4 LLM scores."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.exp4_analysis import analyze_exp4


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("configs/experiments/exp4_llm_evaluation/manifest.yaml"))
    args = parser.parse_args()

    summary = analyze_exp4(args.manifest)
    print(
        f"Analyzed {summary['score_rows']} score rows from "
        f"{summary['scored_cases']} scored cases "
        f"({summary['case_inventory_rows']} inventory cases)"
    )
    print(f"Analysis directory: {summary['analysis_dir']}")


if __name__ == "__main__":
    main()
