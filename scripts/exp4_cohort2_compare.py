"""Analyse EXP4 cohort 2 and compare it with the original cohort.

NEW 2026-09-27 (not a reconstruction). Runs the standard parse and analysis
(src/evaluation/exp4_parser.py, exp4_analysis.py) on cohort 2, then adds the
views the standard analysis does not produce:

- reliability per prompt condition: the standard ICC/alpha pool every
  condition and replicate into one case x judge mean; Supplementary Table S1
  says the primary ICC comes from hidden_label only. Both are reported.
- label bias: label_visible_bias_probe minus hidden_label_primary, per judge
  and dimension, paired on case and replicate.
- rubric sensitivity: rubric_alt_sensitivity minus label_visible_bias_probe
  (the two conditions that both show the true label).
- test-retest: share of case x judge cells with the same score in every
  replicate.
- coverage: responses, parse failures and repairs per judge and condition.

The original cohort's committed aggregates are read from Git and never
written. Outputs go to outputs/analysis/exp4_cohort2/.
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd  # noqa: E402

from src.evaluation import exp4_analysis as ea  # noqa: E402
from src.evaluation.exp4_cases import load_manifest  # noqa: E402
from src.evaluation.exp4_parser import parse_manifest_responses  # noqa: E402
from src.evaluation.exp4_schema import SCORE_FIELDS  # noqa: E402

ORIGINAL = "outputs/analysis/exp4_llm_evaluation"
CONDITIONS = ["hidden_label_primary", "label_visible_bias_probe", "rubric_alt_sensitivity"]


def original(name: str) -> pd.DataFrame:
    blob = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"HEAD:{ORIGINAL}/{name}"],
        capture_output=True, text=True, check=True,
    ).stdout
    return pd.read_csv(io.StringIO(blob))


def reliability(scores: pd.DataFrame, view: str) -> pd.DataFrame:
    icc = ea._icc_per_dimension(scores).set_index("dimension")
    alpha = ea._krippendorff_per_dimension(scores).set_index("dimension")
    out = icc.rename(columns={"icc_2_1": "icc_1_1"})[["icc_1_1", "ci_lower", "ci_upper", "n_cases"]]
    out["krippendorff_alpha"] = alpha["krippendorff_alpha"]
    out["alpha_n_cases"] = alpha["n_cases"]
    out.insert(0, "view", view)
    return out.reset_index()


def paired_shift(scores: pd.DataFrame, cond: str, base: str) -> pd.DataFrame:
    keys = ["judge_model", "case_id", "replicate"]
    cols = [f"{f}_score" for f in SCORE_FIELDS]
    a = scores[scores.prompt_condition == cond].set_index(keys)[cols]
    b = scores[scores.prompt_condition == base].set_index(keys)[cols]
    diff = (a - b).dropna(how="all")
    rows = []
    for judge, g in diff.groupby(level="judge_model"):
        for f in SCORE_FIELDS:
            d = g[f"{f}_score"].dropna()
            rows.append({"judge_model": judge, "dimension": f, "n_pairs": len(d),
                         "mean_shift": d.mean(), "share_changed": (d != 0).mean()})
    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", type=Path, default=Path("configs/experiments/exp4_cohort2/manifest.yaml"))
    args = parser.parse_args()
    manifest = load_manifest(args.manifest)
    out_dir = manifest.paths.analysis_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    parse_summary = parse_manifest_responses(args.manifest)
    try:  # standard pooled analysis; its CLI's KeyError is avoided by calling it directly
        ea.analyze_exp4(args.manifest)
    except Exception as exc:  # noqa: BLE001 -- report and continue with the added views
        print(f"standard analysis failed: {type(exc).__name__}: {exc}")

    scores = pd.read_csv(manifest.paths.parsed_scores_dir / "exp4_llm_scores.csv")
    failures = pd.read_csv(manifest.paths.parsed_scores_dir / "exp4_parse_failures.csv")

    views = [reliability(scores, "pooled_all_conditions")]
    views += [reliability(scores[scores.prompt_condition == c], c) for c in CONDITIONS
              if (scores.prompt_condition == c).any()]
    rel = pd.concat(views, ignore_index=True)
    rel.to_csv(out_dir / "cohort2_reliability_by_view.csv", index=False)

    o_icc, o_alpha = original("icc_analysis.csv"), original("krippendorff_alpha.csv")
    comp = o_icc[["dimension", "icc_2_1", "ci_upper", "n_cases"]].rename(
        columns={"icc_2_1": "orig_icc_1_1", "ci_upper": "orig_ci_upper", "n_cases": "orig_icc_n"})
    comp = comp.merge(o_alpha[["dimension", "krippendorff_alpha", "n_cases"]].rename(
        columns={"krippendorff_alpha": "orig_alpha", "n_cases": "orig_alpha_n"}), on="dimension")
    for view in ["hidden_label_primary", "pooled_all_conditions"]:
        v = rel[rel.view == view].set_index("dimension")
        comp[f"{view}_icc"] = comp.dimension.map(v["icc_1_1"])
        comp[f"{view}_ci_upper"] = comp.dimension.map(v["ci_upper"])
        comp[f"{view}_alpha"] = comp.dimension.map(v["krippendorff_alpha"])
    comp.to_csv(out_dir / "cohort2_vs_original.csv", index=False)

    paired_shift(scores, "label_visible_bias_probe", "hidden_label_primary").to_csv(
        out_dir / "cohort2_label_bias.csv", index=False)
    paired_shift(scores, "rubric_alt_sensitivity", "label_visible_bias_probe").to_csv(
        out_dir / "cohort2_rubric_sensitivity.csv", index=False)

    cols = [f"{f}_score" for f in SCORE_FIELDS]
    retest = (scores.groupby(["prompt_condition", "judge_model", "case_id"])[cols].nunique() == 1)
    retest.groupby(level=["prompt_condition", "judge_model"]).mean().reset_index().to_csv(
        out_dir / "cohort2_test_retest.csv", index=False)

    raw = [json.loads(p.read_text(encoding="utf-8")) for p in manifest.paths.raw_responses_dir.rglob("*.json")]
    cov = pd.DataFrame([{"judge_model": e["judge_model"], "prompt_condition": e["prompt_condition"],
                         "cost": ((e.get("response_meta") or {}).get("usage") or {}).get("cost") or 0.0}
                        for e in raw])
    coverage = cov.groupby(["judge_model", "prompt_condition"]).agg(responses=("cost", "size"), cost_usd=("cost", "sum"))
    coverage["parsed"] = scores.groupby(["judge_model", "prompt_condition"]).size()
    coverage["repaired"] = scores[scores.parse_status != "parsed"].groupby(["judge_model", "prompt_condition"]).size()
    coverage["failed"] = failures.groupby(["judge_model", "prompt_condition"]).size() if len(failures) else 0
    coverage = coverage.fillna(0).astype({"parsed": int, "repaired": int, "failed": int})
    coverage.reset_index().to_csv(out_dir / "cohort2_coverage.csv", index=False)

    print(json.dumps(parse_summary, indent=2))
    print(coverage.to_string())
    print(f"Outputs in {out_dir.as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
