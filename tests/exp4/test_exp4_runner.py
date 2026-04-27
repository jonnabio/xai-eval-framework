import json

from src.evaluation.exp4_runner import run_exp4_judges


def test_runner_dry_run_writes_raw_response(tmp_path):
    cases_dir = tmp_path / "cases"
    cases_dir.mkdir()
    (cases_dir / "exp4_cases.jsonl").write_text(
        json.dumps(
            {
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
        )
        + "\n",
        encoding="utf-8",
    )
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        f"""
experiment_family: exp4_llm_evaluation
case_inventory:
  target_cases: 1
  random_seed: 42
  sources:
    - name: exp2_scaled
      results_root: {tmp_path / "missing"}
judges:
  - provider: dummy
    model_name: dummy
prompt_conditions:
  - hidden_label_primary
replicates: 1
paths:
  cases_dir: {cases_dir}
  prompts_dir: {tmp_path / "prompts"}
  raw_responses_dir: {tmp_path / "raw"}
  parsed_scores_dir: {tmp_path / "parsed"}
  run_manifests_dir: {tmp_path / "runs"}
  analysis_dir: {tmp_path / "analysis"}
""",
        encoding="utf-8",
    )

    summary = run_exp4_judges(manifest_path, dry_run=True)

    assert summary["written_responses"] == 1
    assert len(list((tmp_path / "raw").rglob("*.json"))) == 1
