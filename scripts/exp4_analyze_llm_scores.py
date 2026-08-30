"""Analyze parsed EXP4 LLM scores.

RECONSTRUCTED SOURCE -- see docs/rca/RCA-002-exp4-source-recovery.md.
Rebuilt from scripts/__pycache__/exp4_analyze_llm_scores.cpython-312.pyc.
Structurally verified only; see exp4_build_cases.py for why.

KNOWN DEFECT, preserved from the original: the second print reads
summary["case_rows"], but analyze_exp4() returns "case_inventory_rows". Running
this CLI raises KeyError *after* every analysis CSV has been written, so the
committed EXP4 outputs are unaffected. Left as-is so the file matches the
bytecode; see RCA-002 before changing it.
"""
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
    parser.add_argument(
        "--manifest",
        type=Path,
        default="configs/experiments/exp4_llm_evaluation/manifest.yaml",
    )
    args = parser.parse_args()

    summary = analyze_exp4(args.manifest)
    print(
        f"Analyzed {summary['score_rows']} score rows from "
        f"{summary['case_rows']} cases"
    )
    print(f"Analysis directory: {summary['analysis_dir']}")


if __name__ == "__main__":
    main()
