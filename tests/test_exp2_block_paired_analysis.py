"""Regression tests for the review-motivated EXP2 block contrast."""

from __future__ import annotations

from hashlib import sha256
import math
from pathlib import Path

import pandas as pd
import pytest

from scripts.run_exp2_block_paired_analysis import (
    DEFAULT_INPUT,
    OUTPUT_FILENAMES,
    build_paired_blocks,
    build_sign_test_results,
    build_wilcoxon_results,
    load_block_summary,
    write_outputs,
)


EXPECTED_P = 6.103515625e-05
EXPECTED_HOLM_P = 3.0517578125e-04
EXPECTED_MEAN_DIFFERENCE = 0.2478901309699892


def _hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def test_fidelity_result_matches_review_targets() -> None:
    paired = build_paired_blocks(load_block_summary(DEFAULT_INPUT))
    wilcoxon = build_wilcoxon_results(paired).set_index("metric")
    sign_test = build_sign_test_results(paired).set_index("metric")

    fidelity = wilcoxon.loc["fidelity"]
    signs = sign_test.loc["fidelity"]
    assert len(paired) == 15
    assert fidelity["n_blocks"] == 15
    assert fidelity["wilcoxon_statistic"] == 0
    assert math.isclose(fidelity["p_value_raw"], EXPECTED_P, abs_tol=1e-15)
    assert math.isclose(fidelity["p_value_holm"], EXPECTED_HOLM_P, abs_tol=1e-15)
    assert math.isclose(
        fidelity["mean_difference"], EXPECTED_MEAN_DIFFERENCE, abs_tol=1e-15
    )
    assert (signs["n_positive"], signs["n_negative"], signs["n_ties"]) == (15, 0, 0)
    assert math.isclose(signs["p_value_two_sided"], EXPECTED_P, abs_tol=1e-15)


def test_seed_level_rows_are_rejected(tmp_path: Path) -> None:
    frame = pd.read_csv(DEFAULT_INPUT)
    frame["seed"] = 42
    input_path = tmp_path / "seed_level.csv"
    frame.to_csv(input_path, index=False)

    with pytest.raises(ValueError, match="seed-level input"):
        load_block_summary(input_path)


def test_incomplete_and_duplicate_blocks_are_rejected(tmp_path: Path) -> None:
    frame = pd.read_csv(DEFAULT_INPUT)
    incomplete_path = tmp_path / "incomplete.csv"
    frame.drop(frame[(frame["method"] == "shap")].index[0]).to_csv(
        incomplete_path, index=False
    )
    with pytest.raises(ValueError, match="block mismatch"):
        load_block_summary(incomplete_path)

    duplicate_path = tmp_path / "duplicate.csv"
    shap_row = frame[frame["method"] == "shap"].iloc[[0]]
    pd.concat([frame, shap_row], ignore_index=True).to_csv(duplicate_path, index=False)
    with pytest.raises(ValueError, match="duplicate"):
        load_block_summary(duplicate_path)


def test_repeated_execution_is_byte_identical(tmp_path: Path) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"

    first_paths = write_outputs(DEFAULT_INPUT, first_dir)
    second_paths = write_outputs(DEFAULT_INPUT, second_dir)

    assert tuple(path.name for path in first_paths) == OUTPUT_FILENAMES
    assert [_hash(path) for path in first_paths] == [
        _hash(path) for path in second_paths
    ]


def test_custom_output_does_not_touch_existing_exp2_artifacts(tmp_path: Path) -> None:
    existing = {
        path: _hash(path)
        for path in DEFAULT_INPUT.parent.glob("*")
        if path.is_file() and path.name not in OUTPUT_FILENAMES
    }

    write_outputs(DEFAULT_INPUT, tmp_path)

    assert {path: _hash(path) for path in existing} == existing
