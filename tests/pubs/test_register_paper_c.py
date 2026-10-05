"""Paper C registration (scripts/pubs/register_paper_c.py)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "pubs"))

import register_paper_c as reg  # noqa: E402
from claim_sources import MissingArtifact, resolve  # noqa: E402


@pytest.mark.parametrize("value, fmt, expected", [
    (0.7309, "s3", ("0.731", 3, 1.0)),
    (-0.1302, "s2", ("0.13", 2, 1.0)),
    (0.4567, "rs", ("0.46", 2, 1.0)),
    (0.8333, "pct1", ("83.3", 1, 100.0)),
    (5760, "int", ("5,760", 0, 1.0)),
    (192, "int", (None, 0, 1.0)),          # no thousands separator: not a registry literal
    (0.67, "pct", (None, 0, 1.0)),         # whole percentage: covered by --check only
    (0.0004, "p", (None, 3, 1.0)),
    (0.0312, "p", ("0.031", 3, 1.0)),
])
def test_literal(value, fmt, expected):
    assert reg._literal(value, fmt) == expected


def test_resolver_reads_a_cell_and_scales():
    icc = resolve("paper_c:rel:primary3|all|completeness:icc_1_1")
    assert 0 < icc < 1
    assert resolve("paper_c:rel:primary3|all|completeness:icc_1_1:x100") == pytest.approx(100 * icc)
    with pytest.raises(MissingArtifact):
        resolve("paper_c:rel:primary3|all|no_such_dimension:icc_1_1")


def test_a_quantity_registered_elsewhere_is_not_registered_twice():
    # The all-case coefficient of the second panel is the thesis claim exp4c2:...
    icc = resolve("exp4c2:hidden_label_primary:icc:completeness")
    source = reg._shared_source("rel", ("primary3", "all", "completeness"), "icc_1_1", icc)
    assert source == "exp4c2:hidden_label_primary:icc:completeness"
    assert reg._shared_source("rel", ("primary3", "shap", "completeness"), "icc_1_1", icc) is None
    assert reg._shared_source("rel", ("primary3", "all", "completeness"), "icc_1_1", icc + 0.01) is None


def test_add_sites_handles_both_layouts():
    multi = 'source = "x:y"\nvalue = "1"\nappears_in = [\n  { file = "a", text = "1" },\n]\n\n'
    single = 'source = "x:y"\nvalue = "1"\nappears_in = [{ file = "a", text = "1" }]\n\n'
    site = f'  {{ file = "{reg.MANUSCRIPT}", text = "0.5" }},\n'
    for text in (multi, single):
        out = reg._add_sites(text, "x:y", ["0.5"])
        assert out.count(site) == 1 and '{ file = "a", text = "1" },\n' in out
        assert reg.SITE_LINE.sub("", out).count(reg.MANUSCRIPT) == 0
    assert reg._add_sites(multi, "x:z", ["0.5"]) is None


def test_registration_is_current():
    assert reg.main(["--check"]) == 0
