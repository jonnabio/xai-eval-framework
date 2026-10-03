from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.analyze_paper_e import (
    _bootstrap_interval,
    _quality_summaries,
    _write_report,
    jaccard,
    kendall_top10,
    primary_agreement,
)
import numpy as np


class PaperEAgreementMetricTests(unittest.TestCase):
    def test_jaccard_distinguishes_empty_sets(self) -> None:
        self.assertIsNone(jaccard(set(), set()))
        self.assertEqual(jaccard(set(), {"age"}), 0.0)
        self.assertEqual(jaccard({"age", "income"}, {"age"}), 0.5)

    def test_kendall_uses_midrank_ties_and_absent_rank(self) -> None:
        self.assertEqual(
            kendall_top10({"a": 2.0, "b": -1.0}, {"a": 2.0, "b": -1.0}),
            1.0,
        )
        self.assertAlmostEqual(
            kendall_top10(
                {"a": 3.0, "b": -3.0, "c": 2.0},
                {"b": 3.0, "a": -3.0, "c": 2.0},
            ),
            1.0,
        )
        self.assertAlmostEqual(
            kendall_top10(
                {"a": 2.0, "b": 1.0},
                {"a": 2.0, "c": 1.0},
            ),
            1 / 3,
        )
        self.assertIsNone(kendall_top10({"a": 1.0}, {"a": 1.0}))

    def test_primary_agreement_reports_nonzero_sign_denominator(self) -> None:
        agreement = primary_agreement(
            {"a": 3.0, "b": -2.0, "c": 1.0},
            {"a": 4.0, "b": 2.0, "d": 1.0},
        )

        self.assertEqual(agreement["top5_jaccard"], 0.5)
        self.assertEqual(agreement["shared_top5_nonzero"], 2)
        self.assertEqual(agreement["sign_agreement"], 0.5)
        self.assertEqual(agreement["sign_coverage"], 1.0)

    def test_seed_cluster_bootstrap_is_deterministic_and_needs_two_seeds(self) -> None:
        rows = [
            {"seed": "42", "value": 0.1},
            {"seed": "42", "value": 0.3},
            {"seed": "123", "value": 0.5},
        ]
        first = _bootstrap_interval(
            rows, "value", np.random.default_rng(17)
        )
        second = _bootstrap_interval(
            rows, "value", np.random.default_rng(17)
        )
        self.assertEqual(first, second)
        self.assertIsNone(
            _bootstrap_interval(
                [{"seed": "42", "value": 0.5}],
                "value",
                np.random.default_rng(17),
            )[0]
        )

    def test_quality_associations_are_averaged_within_seed_first(self) -> None:
        rows = [
            {
                "dataset": "exp2_adult",
                "model": "rf",
                "seed": "42",
                "intensity": "n_50",
                "quality_metric": "shap_fidelity",
                "spearman_rho": 0.1,
            },
            {
                "dataset": "exp2_adult",
                "model": "rf",
                "seed": "42",
                "intensity": "n_100",
                "quality_metric": "shap_fidelity",
                "spearman_rho": 0.3,
            },
            {
                "dataset": "exp2_adult",
                "model": "rf",
                "seed": "123",
                "intensity": "n_50",
                "quality_metric": "shap_fidelity",
                "spearman_rho": 0.5,
            },
        ]

        by_seed, summary = _quality_summaries(rows)
        seed_42 = next(row for row in by_seed if row["seed"] == "42")
        self.assertEqual(seed_42["mean_run_spearman_rho"], 0.2)
        self.assertEqual(summary[0]["mean_seed_spearman_rho"], 0.35)
        self.assertEqual(summary[0]["n_seed_units"], 2)

    def test_report_scopes_pairing_and_mismatch_qc(self) -> None:
        diagnostics = [
            {
                "same_id_sets": True,
                "left_only_ids": 0,
                "right_only_ids": 0,
                "classification_mismatches": 0,
            },
            {
                "same_id_sets": False,
                "left_only_ids": 3,
                "right_only_ids": 4,
                "classification_mismatches": 0,
            },
        ]
        with TemporaryDirectory() as temp_dir:
            _write_report(Path(temp_dir), [], diagnostics, [])
            report = (Path(temp_dir) / "RESULTS.md").read_text(encoding="utf-8")

        self.assertIn(
            "Primary SHAP-LIME blocks with exact valid-ID sets: "
            "1/2; unpaired valid method-IDs: 7.",
            report,
        )
        self.assertIn(
            "Classification mismatches in primary SHAP-LIME pairs: 0.",
            report,
        )
        self.assertIn(
            "Secondary method-pair classification mismatches are excluded and",
            report,
        )


if __name__ == "__main__":
    unittest.main()
