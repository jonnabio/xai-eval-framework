import json
from pathlib import Path

from src.evaluation.exp4_cases import (
    load_candidate_cases,
    load_manifest,
    sample_cases,
    write_case_inventory,
)


def test_load_candidate_cases_from_result_structure(tmp_path):
    results_root = tmp_path / "results"
    run_dir = results_root / "rf_shap" / "seed_42" / "n_100"
    run_dir.mkdir(parents=True)
    (run_dir / "results.json").write_text(
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
                        "explanation": {
                            "top_features": [{"feature": "age", "value": 0.42}]
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        "\nexperiment_family: exp4_llm_evaluation\n"
        "case_inventory:\n  target_cases: 1\n  random_seed: 42\n  sources:\n"
        "    - name: exp2_scaled\n      results_root: " + str(results_root) +
        "\njudges:\n  - provider: dummy\n    model_name: dummy\n"
        "prompt_conditions:\n  - hidden_label_primary\nreplicates: 1\n",
        encoding="utf-8",
    )

    manifest = load_manifest(manifest_path)
    cases = load_candidate_cases(manifest)
    assert len(cases) == 1
    assert cases[0].dataset == "adult"
    assert cases[0].model_family == "rf"
    assert "age" in cases[0].normalized_explanation


def test_sample_cases_is_deterministic():
    cases = []
    for index in range(10):
        cases.append(
            _case(
                case_id=f"case-{index}",
                explanation=f"Feature explanation {index}",
            )
        )

    first = [case.case_id for case in sample_cases(cases, 4, 42)]
    second = [case.case_id for case in sample_cases(cases, 4, 42)]
    assert first == second
    assert len(first) == 4


def _case(case_id: str, explanation: str):
    from src.evaluation.exp4_schema import Exp4Case

    return Exp4Case(
        case_id=case_id,
        source_experiment="exp2_scaled",
        source_artifact_path="results.json",
        dataset="adult",
        model_family="rf",
        explainer="shap",
        instance_id=str(case_id),
        normalized_explanation=explanation,
        explanation_length_tokens=3,
        technical_metrics={"fidelity": 0.5, "stability": 0.5},
    )
