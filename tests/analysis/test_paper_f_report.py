"""Paper F: tables and figure from synthetic analysis files (scripts/paper_f_report.py)."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


an = _load("paper_f_analyze")
rep = _load("paper_f_report")
from test_paper_f_analyze import synthetic  # noqa: E402


@pytest.fixture()
def results(tmp_path, monkeypatch):
    monkeypatch.setattr(an, "N_BOOT", 200)
    monkeypatch.setattr(an, "N_PERM", 1000)
    cells = an.cell_means(an.impute_failures(synthetic(shared=True)))
    table, ranks = an.primary(cells, np.random.default_rng(0))
    table.to_csv(tmp_path / "primary.csv", index=False)
    ranks.to_csv(tmp_path / "ranks.csv", index=False)
    an.pairs_vs_adult(ranks).to_csv(tmp_path / "pairs_vs_adult.csv", index=False)
    return tmp_path


def test_primary_table_has_one_row_per_measure(results):
    tex = rep.primary_table(results)
    body = [l for l in tex.splitlines() if l.endswith("\\\\") and not l.startswith("Measure")]
    assert len(body) == 4
    assert all(l.count("&") == 8 for l in body)
    assert "<<" not in tex and "nan" not in tex


def test_adult_table_has_the_six_pairs(results):
    tex = rep.adult_table(results)
    body = [l for l in tex.splitlines() if "--" in l and l.endswith("\\\\")]
    assert len(body) == 6
    assert "LIME--SHAP & 7 & 7 & 7 & 7" in tex  # the same order in the 7 other datasets


def test_figure_is_written(results, tmp_path):
    rep.figure(results, tmp_path / "figures")
    assert (tmp_path / "figures" / "fig1.pdf").stat().st_size > 1000
    assert (tmp_path / "figures" / "fig1.png").stat().st_size > 1000
