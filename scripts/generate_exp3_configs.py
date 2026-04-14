"""
Generate EXP3 cross-dataset validation configs.

EXP3 is intentionally compact:
- datasets: breast_cancer, german_credit
- models: rf, xgb
- explainers: shap, anchors
- seeds: 42, 123, 456
- sample size: 100 per TP/TN/FP/FN quadrant
"""

from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path
from typing import Iterable

import yaml

DEFAULT_DATASETS = ["breast_cancer", "german_credit"]
DEFAULT_MODELS = ["rf", "xgb"]
DEFAULT_EXPLAINERS = ["shap", "anchors"]
DEFAULT_SEEDS = [42, 123, 456]
DEFAULT_SAMPLE_SIZE = 100
DEFAULT_STABILITY_PERTURBATIONS = 15

CONFIG_ROOT = Path("configs/experiments/exp3_cross_dataset")
MODEL_ROOT = Path("experiments/exp3_cross_dataset/models")
RESULT_ROOT = Path("experiments/exp3_cross_dataset/results")


def _model_path(dataset: str, model: str, seed: int) -> Path:
    return MODEL_ROOT / dataset / model / f"seed_{seed}" / f"{model}.joblib"


def _output_dir(dataset: str, model: str, explainer: str, seed: int) -> Path:
    return RESULT_ROOT / dataset / f"{model}_{explainer}" / f"seed_{seed}" / "n_100"


def _config_path(root: Path, dataset: str, model: str, explainer: str, seed: int) -> Path:
    return root / dataset / f"{model}_{explainer}_s{seed}_n100.yaml"


def build_config(dataset: str, model: str, explainer: str, seed: int) -> dict:
    """Build one EXP3 experiment config dictionary."""
    config = {
        "name": f"exp3_{dataset}_{model}_{explainer}_s{seed}_n100",
        "version": "3.0",
        "dataset": dataset,
        "random_seed": seed,
        "model": {
            "name": f"{dataset}_{model}",
            "path": _model_path(dataset, model, seed).as_posix(),
            "type": model,
        },
        "explainer": {
            "method": explainer,
            "params": {},
        },
        "sampling": {
            "strategy": "stratified",
            "samples_per_class": DEFAULT_SAMPLE_SIZE,
            "random_seed": seed,
        },
        "metrics": {
            "fidelity": True,
            "stability": True,
            "sparsity": True,
            "cost": True,
            "domain": False,
            "counterfactual": False,
            "stability_perturbations": DEFAULT_STABILITY_PERTURBATIONS,
        },
        "max_workers": 1,
        "output_dir": _output_dir(dataset, model, explainer, seed).as_posix(),
    }

    if explainer == "shap":
        config["explainer"]["params"] = {"n_background_samples": 50}
        config["explainer"]["explainer_type"] = "tree"
    elif explainer == "anchors":
        config["explainer"]["params"] = {"threshold": 0.95}
    else:
        raise ValueError(f"Unsupported EXP3 explainer: {explainer}")

    return config


def generate_configs(
    datasets: Iterable[str] = DEFAULT_DATASETS,
    models: Iterable[str] = DEFAULT_MODELS,
    explainers: Iterable[str] = DEFAULT_EXPLAINERS,
    seeds: Iterable[int] = DEFAULT_SEEDS,
    output_dir: Path = CONFIG_ROOT,
) -> int:
    """Generate EXP3 YAML configs and manifest."""
    datasets = list(datasets)
    models = list(models)
    explainers = list(explainers)
    seeds = [int(seed) for seed in seeds]

    count = 0
    for dataset, model, explainer, seed in product(datasets, models, explainers, seeds):
        config = build_config(dataset, model, explainer, seed)
        path = _config_path(output_dir, dataset, model, explainer, seed)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(config, sort_keys=False))
        count += 1

    manifest = {
        "experiment_set": "exp3_cross_dataset",
        "status": "prepared",
        "thesis_role": "external_validation",
        "total_configs": count,
        "dimensions": {
            "datasets": datasets,
            "models": models,
            "explainers": explainers,
            "seeds": seeds,
            "sample_sizes": [DEFAULT_SAMPLE_SIZE],
        },
        "estimated_instances": count * DEFAULT_SAMPLE_SIZE * 4,
        "stability_perturbations": DEFAULT_STABILITY_PERTURBATIONS,
        "metrics": {
            "fidelity": True,
            "stability": True,
            "sparsity": True,
            "cost": True,
            "domain": False,
            "counterfactual": False,
        },
        "naming_pattern": "exp3_<dataset>_<model>_<explainer>_s<seed>_n100",
        "config_root": output_dir.as_posix(),
        "model_root": MODEL_ROOT.as_posix(),
        "result_root": RESULT_ROOT.as_posix(),
    }
    (output_dir / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False))
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate EXP3 cross-dataset configs")
    parser.add_argument("--datasets", nargs="+", default=DEFAULT_DATASETS)
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--explainers", nargs="+", default=DEFAULT_EXPLAINERS)
    parser.add_argument("--seeds", nargs="+", type=int, default=DEFAULT_SEEDS)
    args = parser.parse_args()

    count = generate_configs(
        datasets=args.datasets,
        models=args.models,
        explainers=args.explainers,
        seeds=args.seeds,
    )
    print(f"Generated {count} EXP3 configs under {CONFIG_ROOT}")


if __name__ == "__main__":
    main()
