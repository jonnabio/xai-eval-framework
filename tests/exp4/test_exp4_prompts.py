from src.evaluation.exp4_prompts import prompt_version_hash, render_exp4_prompt
from src.evaluation.exp4_schema import Exp4Case


def test_hidden_label_prompt_masks_true_label():
    case = Exp4Case(
        case_id="case-1",
        source_experiment="exp2_scaled",
        source_artifact_path="results.json",
        dataset="adult",
        model_family="rf",
        explainer="shap",
        instance_id="1",
        prediction=1,
        true_label=0,
        normalized_explanation="SHAP top local factors: age: 0.4",
        explanation_length_tokens=7,
    )

    prompt = render_exp4_prompt(case, "hidden_label_primary")

    assert '"true_label": null' in prompt
    assert '"case_id": "case-1"' in prompt
    assert prompt_version_hash(prompt) == prompt_version_hash(prompt)


def test_label_visible_prompt_includes_true_label():
    case = Exp4Case(
        case_id="case-1",
        source_experiment="exp2_scaled",
        source_artifact_path="results.json",
        dataset="adult",
        model_family="rf",
        explainer="shap",
        instance_id="1",
        prediction=1,
        true_label=0,
        normalized_explanation="SHAP top local factors: age: 0.4",
        explanation_length_tokens=7,
    )

    prompt = render_exp4_prompt(case, "label_visible_bias_probe")

    assert '"true_label": 0' in prompt
