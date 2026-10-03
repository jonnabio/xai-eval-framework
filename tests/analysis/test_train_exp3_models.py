import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts import train_exp3_models


class _FakeTrainer:
    def __init__(self) -> None:
        self.feature_names = None

    def train(self, X_train, y_train) -> None:
        self.X_train = X_train
        self.y_train = y_train

    def evaluate(self, X_test, y_test) -> dict:
        return {"accuracy": 1.0}

    def save(self, directory: Path, filename: str) -> None:
        (Path(directory) / filename).write_text("model", encoding="utf-8")
        metadata = {
            "model_class": "FakeTrainer",
            "config": {"seed": 7},
            "feature_names": self.feature_names,
        }
        (Path(directory) / "metadata.json").write_text(
            json.dumps(metadata), encoding="utf-8"
        )


class TrainExp3ModelsTests(unittest.TestCase):
    def test_artifact_and_cache_roots_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            model_root = root / "models"
            cache_dir = root / "cache"
            trainer = _FakeTrainer()
            with (
                patch.object(
                    train_exp3_models,
                    "load_tabular_dataset",
                    return_value=(
                        [[0.0]],
                        [[1.0]],
                        [0],
                        [1],
                        ["feature"],
                        object(),
                    ),
                ) as load_dataset,
                patch.object(
                    train_exp3_models.ModelTrainerFactory,
                    "get_trainer",
                    return_value=trainer,
                ),
            ):
                output = train_exp3_models.train_one(
                    "breast_cancer",
                    "rf",
                    7,
                    model_root=model_root,
                    cache_dir=cache_dir,
                )

            self.assertEqual(output, model_root / "breast_cancer/rf/seed_7/rf.joblib")
            self.assertTrue(output.is_file())
            self.assertTrue((output.parent / "exp3_training_summary.json").is_file())
            self.assertEqual(load_dataset.call_args.kwargs["cache_dir"], str(cache_dir))


if __name__ == "__main__":
    unittest.main()
