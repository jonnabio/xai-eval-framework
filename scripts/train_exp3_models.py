"""
Train seed-specific EXP3 tabular model artifacts.

This script prepares the model/preprocessor artifacts required by the EXP3
cross-dataset validation configs. It does not run explanation experiments.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Iterable

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.data_loading.cross_dataset import load_tabular_dataset
from src.models.factory import ModelTrainerFactory

logger = logging.getLogger(__name__)

DEFAULT_DATASETS = ["breast_cancer", "german_credit"]
DEFAULT_MODELS = ["rf", "xgb"]
DEFAULT_SEEDS = [42, 123, 456]
MODEL_ROOT = Path("experiments/exp3_cross_dataset/models")


def _trainer_config(model: str, seed: int) -> dict:
    if model == "rf":
        return {
            "n_estimators": 100,
            "random_state": seed,
            "n_jobs": 1,
        }
    if model == "xgb":
        return {
            "n_estimators": 100,
            "max_depth": 4,
            "learning_rate": 0.1,
            "random_state": seed,
            "n_jobs": 1,
        }
    raise ValueError(f"Unsupported EXP3 model: {model}")


def train_one(dataset: str, model: str, seed: int, force: bool = False) -> Path:
    """Train and persist one EXP3 model artifact."""
    model_dir = MODEL_ROOT / dataset / model / f"seed_{seed}"
    model_path = model_dir / f"{model}.joblib"
    preprocessor_path = model_dir / "preprocessor.joblib"

    if model_path.exists() and preprocessor_path.exists() and not force:
        logger.info("Skipping existing EXP3 artifact: %s", model_path)
        return model_path

    model_dir.mkdir(parents=True, exist_ok=True)
    X_train, X_test, y_train, y_test, feature_names, _ = load_tabular_dataset(
        dataset,
        random_state=seed,
        preprocessor_path=str(preprocessor_path),
        verbose=True,
    )

    trainer = ModelTrainerFactory.get_trainer(model, _trainer_config(model, seed))
    trainer.feature_names = feature_names
    trainer.train(X_train, y_train)
    metrics = trainer.evaluate(X_test, y_test)
    trainer.save(model_dir, model_path.name)

    summary_path = model_dir / "exp3_training_summary.json"
    summary = {
        "dataset": dataset,
        "model": model,
        "seed": seed,
        "model_path": str(model_path),
        "preprocessor_path": str(preprocessor_path),
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "n_features": int(len(feature_names)),
        "metrics": metrics,
    }
    summary_path.write_text(json.dumps(summary, indent=2))
    logger.info("Trained EXP3 artifact: %s", model_path)
    return model_path


def train_many(
    datasets: Iterable[str],
    models: Iterable[str],
    seeds: Iterable[int],
    force: bool = False,
) -> list[Path]:
    """Train the selected EXP3 model grid."""
    outputs: list[Path] = []
    for dataset in datasets:
        for model in models:
            for seed in seeds:
                outputs.append(train_one(dataset, model, int(seed), force=force))
    return outputs


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(description="Train EXP3 cross-dataset model artifacts")
    parser.add_argument("--datasets", nargs="+", default=DEFAULT_DATASETS)
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--seeds", nargs="+", type=int, default=DEFAULT_SEEDS)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    outputs = train_many(args.datasets, args.models, args.seeds, force=args.force)
    print(f"Prepared {len(outputs)} EXP3 model artifacts")


if __name__ == "__main__":
    main()
