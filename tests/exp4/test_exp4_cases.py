import json
from pathlib import Path

from src.evaluation.exp4_cases import load_candidate_cases, load_manifest, sample_cases, write_case_inventory


def test_load_candidate_cases_from_result_structure(tmp_path):
    root = tmp_path / "results" / "rf_shap" / "seed_42" / "n_100"
    root.mkdir(parents=True)
    result_path = root / "results.json"
    result_path.write_text(
        json.dumps(
            {
                "experiment_metadata": {"dataset": "adult", "random_seed": 42},
                "model_info": {"name": "adult_rf", "explainer_method": "shap"},
                "instance_evaluations": [
                    {
                        "instance_id": 7,
                        "quadrant": "TP",
                        "true_label": 1,
                        "prediction": 1,
                        "metrics": {"fidelity": 0.9, "stability": 0.8, "sparsity": 0.2},
                        "explanation": {"top_features": [{"feature": "age", "value": 0.42}]},
                    }
                ],
            }
        ),
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
      results_root: {tmp_path / "results"}
judges:
  - provider: dummy
    model_name: dummy
prompt_conditions:
  - hidden_label_primary
replicates: 1
""",
        encoding="utf-8",
    )

    cases = load_candidate_cases(load_manifest(manifest_path))

    assert len(cases) == 1
    assert cases[0].dataset == "adult"
    assert cases[0].model_family == "rf"
    assert "age" in cases[0].normalized_explanation


def test_sample_cases_is_deterministic():
    cases = []
    for idx in range(10):
        cases.append(
            {
                "case_id": f"case-{idx}",
                "source_experiment": "exp2_scaled",
                "source_artifact_path": "results.json",
                "dataset": "adult",
                "model_family": "rf",
                "explainer": "shap",
                "instance_id": str(idx),
                "normalized_explanation": f"Feature explanation {idx}",
                "explanation_length_tokens": 3,
                "technical_metrics": {"fidelity": idx / 10, "stability": idx / 20},
            }
        )
    from src.evaluation.exp4_schema import Exp4Case

    model_cases = [Exp4Case(**case) for case in cases]
    first = [case.case_id for case in sample_cases(model_cases, 4, 42)]
    second = [case.case_id for case in sample_cases(model_cases, 4, 42)]

    assert first == second
    assert len(first) == 4
