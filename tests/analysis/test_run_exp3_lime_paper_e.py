from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.run_exp3_lime import (
    serialize_attributions,
    target_instance_ids,
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


if __name__ == "__main__":
    unittest.main()
