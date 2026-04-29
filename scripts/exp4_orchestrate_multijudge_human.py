#!/usr/bin/env python3
"""Orchestration script for EXP4 Phase 1→Phase 2 transition.

Automates: parse responses → analyze multi-judge → select human validation cases
Runs after both GPT-4 and GPT-4-mini judges complete execution.
"""

from __future__ import annotations

import argparse
import sys
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def run_command(cmd: list[str], description: str) -> bool:
    """Execute shell command with logging."""
    print(f"\n{'='*70}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {description}")
    print(f"{'='*70}")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=ROOT)
    
    if result.returncode == 0:
        print(f"✅ Success: {description}")
        return True
    else:
        print(f"❌ Failed: {description} (exit code: {result.returncode})")
        return False


def phase_1_completion(
    manifest_path: Path,
    parsed_scores_dir: Path,
    analysis_dir: Path,
) -> bool:
    """Execute Phase 1 post-judge workflows."""
    
    print("\n" + "="*70)
    print("EXP4 PHASE 1: Multi-Judge Analysis Completion")
    print("="*70)
    
    # Step 1: Re-parse all responses (openai_gpt41 + openrouter_gpt41_mini + existing openrouter_gpt41)
    step1 = run_command(
        [
            "python", "scripts/exp4_parse_llm_responses.py",
            "--manifest", str(manifest_path),
        ],
        "Step 1: Re-parse all judge responses (combining 3 judges)"
    )
    
    if not step1:
        return False
    
    # Step 2: Run full multi-judge analysis
    step2 = run_command(
        [
            "python", "scripts/exp4_analyze_llm_scores.py",
            "--manifest", str(manifest_path),
        ],
        "Step 2: Compute multi-judge metrics (ICC, Krippendorff, disagreement)"
    )
    
    if not step2:
        return False
    
    # Step 3: Summarize multi-judge results
    print("\n" + "-"*70)
    print("PHASE 1 COMPLETION SUMMARY")
    print("-"*70)
    
    # Check generated files
    analysis_dir_path = Path(analysis_dir)
    expected_files = [
        "icc_analysis.csv",
        "krippendorff_alpha.csv",
        "judge_comparison_summary.csv",
        "judge_disagreement.csv",
        "multijudge_summary_report.md",
    ]
    
    print("\nGenerated outputs:")
    for f in expected_files:
        fpath = analysis_dir_path / f
        if fpath.exists():
            size = fpath.stat().st_size / 1024  # KB
            print(f"  ✅ {f} ({size:.1f} KB)")
        else:
            print(f"  ❌ {f} (NOT FOUND)")
    
    print("\n✅ Phase 1 Complete. Ready for Phase 2 (human validation).")
    return True


def phase_2_case_selection(
    parsed_scores_path: Path,
    cases_manifest_path: Path,
    output_path: Path,
    n_cases: int = 80,
) -> bool:
    """Execute Phase 2 case selection (disagreement-based)."""
    
    print("\n" + "="*70)
    print("EXP4 PHASE 2: Human Validation Case Selection")
    print("="*70)
    
    step = run_command(
        [
            "python", "scripts/exp4_select_human_validation_cases.py",
            "--parsed-scores", str(parsed_scores_path),
            "--cases-manifest", str(cases_manifest_path),
            "--output", str(output_path),
            "--n-cases", str(n_cases),
        ],
        f"Select {n_cases} high-disagreement cases for human annotation"
    )
    
    if step:
        print("\n" + "-"*70)
        print("PHASE 2 CASE SELECTION COMPLETE")
        print("-"*70)
        print(f"\n✅ Selected {n_cases} cases:")
        print(f"   Location: {output_path}")
        print(f"   Strategy: Highest LLM judge disagreement")
        print(f"   Stratification: Balanced by explainer (~20 per type)")
        print("\n🎯 Next: Recruit & onboard 5-10 annotators for human annotation")
        return True
    else:
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phase",
        choices=["1", "2", "all"],
        default="all",
        help="Which phase(s) to execute: 1 (parse+analyze), 2 (case selection), or all",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("configs/experiments/exp4_llm_evaluation/manifest.yaml"),
        help="Path to EXP4 manifest",
    )
    parser.add_argument(
        "--n-cases",
        type=int,
        default=80,
        help="Number of cases for human validation (default 80)",
    )
    args = parser.parse_args()
    
    manifest_path = args.manifest
    parsed_scores_dir = Path("experiments/exp4_llm_evaluation/parsed_scores")
    analysis_dir = Path("outputs/analysis/exp4_llm_evaluation")
    parsed_scores_path = parsed_scores_dir / "exp4_llm_scores.csv"
    cases_manifest_path = Path("experiments/exp4_llm_evaluation/cases/exp4_cases.csv")
    human_validation_output = Path("experiments/exp4_llm_evaluation/human_validation/case_manifest.csv")
    
    print("\n" + "="*70)
    print("EXP4 MULTI-JUDGE & HUMAN VALIDATION ORCHESTRATION")
    print("="*70)
    print(f"Manifest: {manifest_path}")
    print(f"Parsed scores: {parsed_scores_path}")
    print(f"Analysis output: {analysis_dir}")
    print(f"Human validation cases: {n_cases}")
    
    if args.phase in ["1", "all"]:
        success = phase_1_completion(manifest_path, parsed_scores_dir, analysis_dir)
        if not success and args.phase == "1":
            sys.exit(1)
    
    if args.phase in ["2", "all"]:
        success = phase_2_case_selection(
            parsed_scores_path, cases_manifest_path, human_validation_output, args.n_cases
        )
        if not success:
            sys.exit(1)
    
    print("\n" + "="*70)
    print("✅ ORCHESTRATION COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("1. Review multi-judge metrics (Phase 1):")
    print(f"   - {analysis_dir / 'multijudge_summary_report.md'}")
    print("2. Recruit annotators (Phase 2):")
    print(f"   - Guide: experiments/exp4_llm_evaluation/human_validation_annotator_guide.md")
    print(f"   - Cases: {human_validation_output}")
    print("3. Deploy web UI and start human annotation")


if __name__ == "__main__":
    main()
