#!/usr/bin/env python3
"""Paper F: the primary analysis with the software-defect family counted once.

    python scripts/paper_f_posthoc_family.py [--results DIR]

A CHECK MADE AFTER THE RESULTS WERE SEEN (ANALYSIS_PLAN.md, section 12, 2026-10-12). It is
not part of the planned analysis and is reported as such.

JM1, KC1, PC3 and PC4 are software-defect datasets of one family, so the sixteen datasets
of the study are less independent than their number suggests. This script repeats the
primary analysis of scripts/paper_f_analyze.py (the same functions, the same numbers of
resamples and permutations, the same Holm correction over the four measures and the same
decision rule) on thirteen datasets: the twelve others and one of the four. It does so
four times, once for each dataset of the family that is kept, so that no choice among
them has to be defended.

Reads outputs/analysis/paper_f/results/cells.csv, the run means of the planned analysis.
No explanation is computed and no file of the planned analysis is written. Writes

    results/posthoc_defect_family.csv   one row per kept dataset and measure

The random generator is seeded here, apart from the planned analysis, and started again
for each of the four runs, so the order of the runs does not change a number.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_f_analyze as an  # noqa: E402
import paper_f_lib as lib  # noqa: E402

FAMILY = ("jm1", "kc1", "pc3", "pc4")
SEED = 20261012
COLUMNS = ["kept", "measure", "datasets", "mean_rank_corr", "ci_low", "ci_high", "p_perm",
           "p_holm", "decision"]


def family_once(cells: pd.DataFrame, seed: int = SEED) -> pd.DataFrame:
    """The primary analysis with one dataset of the family, for each of its datasets."""
    missing = set(FAMILY) - set(cells["dataset"])
    if missing:
        raise ValueError(f"datasets of the family not in the data: {sorted(missing)}")
    parts = []
    for i, kept in enumerate(FAMILY):
        dropped = [d for d in FAMILY if d != kept]
        table, _ = an.primary(cells[~cells["dataset"].isin(dropped)],
                              np.random.default_rng([seed, i]))
        parts.append(table.assign(kept=kept)[COLUMNS])
    return pd.concat(parts, ignore_index=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", default=str(lib.OUT / "results"))
    args = ap.parse_args()
    results = Path(args.results)
    out = family_once(pd.read_csv(results / "cells.csv"))
    out.to_csv(results / "posthoc_defect_family.csv", index=False)
    print(out.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
