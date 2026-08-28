"""Run EXP4 LLM judges or dry-run judges.

RECONSTRUCTED SOURCE -- see docs/rca/RCA-002-exp4-source-recovery.md.
Rebuilt from scripts/__pycache__/exp4_run_llm_judges.cpython-312.pyc.
Structurally verified only; see exp4_build_cases.py for why.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.exp4_runner import run_exp4_judges


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default="configs/experiments/exp4_llm_evaluation/manifest.yaml",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--replicates", type=int, default=None)
    parser.add_argument(
        "--condition",
        choices=(
            "hidden_label_primary",
            "label_visible_bias_probe",
            "rubric_alt_sensitivity",
        ),
        default=None,
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    summary = run_exp4_judges(
        manifest_path=args.manifest,
        dry_run=args.dry_run,
        limit=args.limit,
        replicates=args.replicates,
        condition=args.condition,
        force=args.force,
    )
    print(
        f"Wrote {summary['written_responses']} raw responses; "
        f"skipped {summary['skipped_existing']}"
    )
    print(f"Run manifest: {summary['run_manifest_path']}")


if __name__ == "__main__":
    main()
