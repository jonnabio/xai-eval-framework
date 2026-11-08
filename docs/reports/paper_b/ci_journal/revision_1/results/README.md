# Analysis of cohort B2 (2026-11-08, 12:17 snapshot)

Output of `scripts/paper_b_analyze.py` on snapshot `4869537b5` of `paper/b-rev1-runs`: quality
575 of 575 jobs; timing 73 of 115 cells (Adult, Breast Cancer, Diabetes and German Credit
complete; Spambase 3 of 15; Phishing and Connect-4 not started). Pinned packages of
`env/requirements-rev1-frozen.txt`, with the prepared datasets rebuilt on this laptop (their
hashes match `models/MANIFEST.csv`), so `cost.csv` now has FLOPs. Adult values are identical to
the snapshot `992d20038` used for C-042.

Derived for the supplement by `scripts/supplement_results.py` (from `rows.csv`, not committed):
`instances.csv`, `overlap.csv`, `paired_differences.csv`, `zero_vector_exclusion.csv`,
`timing_cells.csv` and `fig_s1_paired_differences.png`. Anchors' rows on XGBoost are 0 because
its calls were not counted (see `../HANDOFF.md`). Regenerate from the final snapshot before the
final build.
