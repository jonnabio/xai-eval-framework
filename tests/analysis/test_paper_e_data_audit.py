import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.paper_e_data_audit import audit_sources


def write_run(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"instance_evaluations": rows}),
        encoding="utf-8",
    )


def valid_row(instance_id: int, target: int = 1, prediction: int = 1) -> dict:
    return {
        "instance_id": instance_id,
        "true_label": target,
        "prediction": prediction,
        "prediction_correct": target == prediction,
        "explanation": {"raw_top": {"age": 0.5}},
    }


class PaperEDataAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_audit_pairs_only_unique_valid_ids(self) -> None:
        base = self.root / "experiments/exp2_scaled/results"
        block = ("rf_shap", "seed_42", "n_50")
        write_run(base.joinpath(*block, "results.json"), [
            valid_row(1),
            valid_row(2),
            valid_row(2),
            {"instance_id": 3, "error": "failed", "metrics": {}},
        ])
        lime_block = ("rf_lime", "seed_42", "n_50")
        write_run(base.joinpath(*lime_block, "results.json"), [
            valid_row(1),
            valid_row(2),
            valid_row(3),
        ])

        audit = audit_sources(self.root)
        shap_lime = audit["exp2"]["blocks"][0]["pairwise"]["shap_lime"]

        self.assertEqual(shap_lime["matched_ids"], 1)
        self.assertFalse(shap_lime["same_id_sets"])
        self.assertEqual(audit["exp2"]["method_counts"]["shap"]["invalid_rows"], 1)
        self.assertEqual(audit["exp2"]["method_counts"]["shap"]["duplicate_ids"], 1)

    def test_exp3_audit_reports_exact_ids_and_label_mismatch(self) -> None:
        base = self.root / "experiments/exp3_cross_dataset/results/german_credit"
        shap = base / "rf_shap/seed_42/n_100/results.json"
        anchors = base / "rf_anchors/seed_42/n_100/results.json"
        write_run(shap, [valid_row(4), valid_row(5)])
        write_run(anchors, [valid_row(4), valid_row(5, target=0, prediction=0)])

        audit = audit_sources(self.root)
        run = next(item for item in audit["exp3"]["runs"] if item["seed"] == 42)

        self.assertEqual(run["shap_anchors"]["matched_ids"], 2)
        self.assertTrue(run["shap_anchors"]["same_id_sets"])
        self.assertEqual(run["shap_anchors"]["classification_mismatches"], 1)
        self.assertEqual(audit["exp3"]["counts"]["exact_shap_anchor_blocks"], 1)


if __name__ == "__main__":
    unittest.main()
