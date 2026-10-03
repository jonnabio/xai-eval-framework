from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.run_exp3_lime import (
    run_paper_e,
    serialize_attributions,
    target_instance_ids,
    validate_training_reproduction,
    validate_source_predictions,
)


class PaperELimePreparationTests(unittest.TestCase):
    def test_target_ids_are_sorted_and_range_checked(self) -> None:
        rows = [{"instance_id": 3}, {"instance_id": 1}]

        self.assertEqual(target_instance_ids(rows, test_size=4), [1, 3])

    def test_target_ids_reject_duplicates_and_out_of_range(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate"):
            target_instance_ids(
                [{"instance_id": 2}, {"instance_id": 2}], test_size=4
            )
        with self.assertRaisesRegex(ValueError, "outside X_test range"):
            target_instance_ids([{"instance_id": 4}], test_size=4)

    def test_source_prediction_mismatch_fails(self) -> None:
        rows = [{
            "instance_id": 0,
            "true_label": 1,
            "prediction": 1,
            "prediction_correct": True,
        }]

        with self.assertRaisesRegex(ValueError, "Prediction mismatch"):
            validate_source_predictions(
                rows, np.array([1]), np.array([0])
            )

    def test_serialized_top_is_ranked_by_absolute_signed_value(self) -> None:
        result = serialize_attributions(
            np.array([-0.7, 0.3, 0.1]),
            ["a", "b", "c"],
            top_k=2,
        )

        self.assertEqual(list(result["raw_top"]), ["a", "b"])
        self.assertEqual(result["raw_top"]["a"], -0.7)
        self.assertEqual(
            result["raw_attributions"],
            {"a": -0.7, "b": 0.3, "c": 0.1},
        )

    def test_reproduced_training_summary_must_match_source(self) -> None:
        summary = {
            "dataset": "breast_cancer",
            "model": "rf",
            "seed": 42,
            "n_train": 455,
            "n_test": 114,
            "n_features": 30,
            "metrics": {
                "accuracy": 0.95,
                "confusion_matrix": [[39, 3], [2, 70]],
            },
        }
        validate_training_reproduction(summary, summary.copy())

        mismatched = {**summary, "metrics": {**summary["metrics"], "accuracy": 0.9}}
        with self.assertRaisesRegex(ValueError, "accuracy"):
            validate_training_reproduction(mismatched, summary)

    def test_existing_paper_e_output_directory_is_not_overwritten(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as temporary:
            output_root = Path(temporary)
            sentinel = output_root / "keep.txt"
            sentinel.write_text("existing", encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "already exists"):
                run_paper_e(output_root)

            self.assertEqual(sentinel.read_text(encoding="utf-8"), "existing")

    def test_failed_cohort_run_leaves_no_partial_output(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as temporary:
            output_root = Path(temporary) / "cohort"
            with patch(
                "scripts.run_exp3_lime.run_one_paper_e",
                side_effect=ValueError("source mismatch"),
            ):
                with self.assertRaisesRegex(ValueError, "source mismatch"):
                    run_paper_e(output_root)

            self.assertFalse(output_root.exists())
            self.assertEqual(list(Path(temporary).glob(".cohort.*")), [])


if __name__ == "__main__":
    unittest.main()
