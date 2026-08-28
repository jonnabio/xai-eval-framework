import json
from pathlib import Path

import pytest

from src.evaluation.exp4_prompts import TEMPLATE_BY_CONDITION
from src.evaluation.exp4_runner import run_exp4_judges

# See tests/exp4/test_exp4_prompts.py: the EXP4 Jinja templates were not
# retained, and the runner renders a real prompt per case (RCA-002).
_TEMPLATES = Path(__file__).resolve().parents[2] / "src" / "prompts" / "templates"
pytestmark = pytest.mark.skipif(
    not all((_TEMPLATES / name).exists() for name in TEMPLATE_BY_CONDITION.values()),
    reason="EXP4 prompt templates were not retained in the repository (RCA-002)",
)

CASE = {
    "case_id": "case-1",
    "source_experiment": "exp2_scaled",
    "source_artifact_path": "results.json",
    "dataset": "adult",
    "model_family": "rf",
    "explainer": "shap",
    "instance_id": "1",
    "normalized_explanation": "SHAP top local factors: age: 0.4",
    "explanation_length_tokens": 7,
    "technical_metrics": {"fidelity": 0.9},
}

MANIFEST = """
experiment_family: exp4_llm_evaluation
case_inventory:
  target_cases: 1
  random_seed: 42
  sources:
    - name: exp2_scaled
      results_root: {missing}
judges:
  - provider: dummy
    model_name: dummy
prompt_conditions:
  - hidden_label_primary
replicates: 1
paths:
  cases_dir: {cases}
  prompts_dir: {prompts}
  raw_responses_dir: {raw}
  parsed_scores_dir: {parsed}
  run_manifests_dir: {runs}
  analysis_dir: {analysis}
"""


def _setup(tmp_path):
    cases_dir = tmp_path / "cases"
    cases_dir.mkdir(parents=True)
    (cases_dir / "exp4_cases.jsonl").write_text(json.dumps(CASE) + "\n", encoding="utf-8")
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        MANIFEST.format(
            missing=tmp_path / "missing",
            cases=cases_dir,
            prompts=tmp_path / "prompts",
            raw=tmp_path / "raw",
            parsed=tmp_path / "parsed",
            runs=tmp_path / "runs",
            analysis=tmp_path / "analysis",
        ),
        encoding="utf-8",
    )
    return manifest_path


def test_runner_dry_run_writes_raw_response(tmp_path):
    manifest_path = _setup(tmp_path)
    summary = run_exp4_judges(manifest_path, dry_run=True)
    assert summary["written_responses"] == 1
    assert len(list((tmp_path / "raw").rglob("*.json"))) == 1


def test_runner_filters_judge_id_in_dry_run(tmp_path):
    manifest_path = _setup(tmp_path)
    summary = run_exp4_judges(manifest_path, dry_run=True, judge_id="dummy_exp4")
    assert summary["written_responses"] == 1
