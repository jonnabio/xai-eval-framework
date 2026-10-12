"""Paper F registration: what is registered, and that it re-derives from the result files."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "pubs"))

import register_paper_f as rpf  # noqa: E402
from claim_sources import resolve  # noqa: E402


@pytest.mark.parametrize("value, fmt, expected", [
    (16, "d", None),                       # a bare count is outside the registry
    (0.19, "pct", None),                   # a whole percentage too
    (256000, "int", "256,000"),
    (20, "int", None),
    (0.00004, "p", None),                  # printed as "<0.001"
    (0.0056, "pct2", "0.56"),
    (0.048, "pct1", "4.8"),
    (-0.4, "u2", "0.40"),                  # the sign is printed apart from the digits
])
def test_literal(value, fmt, expected):
    assert rpf._literal(value, fmt)[0] == expected


def test_claims_resolve_to_their_printed_values():
    claims = rpf.collect(rpf._build_module())
    assert claims
    for cid, claim in claims.items():
        assert abs(resolve(claim["source"]) - float(claim["value"])) <= claim["tolerance"], cid


def test_every_site_is_in_a_registered_file():
    claims = rpf.collect(rpf._build_module())
    files = {file for claim in claims.values() for file, _ in claim["sites"]}
    assert files <= set(rpf.FILES)
    assert rpf.MANUSCRIPT in files and rpf.TAB_PRIMARY in files and rpf.TAB_DATASETS in files
