# Analysis of cohort B2 (2026-11-08)

Output of `scripts/paper_b_analyze.py` on snapshot `992d20038` of `paper/b-rev1-runs`: quality
575 of 575 jobs, timing 33 of 115 cells (all 25 Adult cells; Breast Cancer 8 of 15). Run with the
pinned packages of `env/requirements-rev1-frozen.txt`. Source of the values filled in C-040
(quality, unchanged from snapshot `19a73baca`) and C-042 (cost; `p_holm` over the family of 12).
`cost.csv` lacks the FLOPs column: the prepared datasets are not on the documentation laptop, so
FLOPs were computed by hand in §4.2 (108 encoded features). Anchors' rows on XGBoost are 0
because its calls were not counted (see `../HANDOFF.md`). Regenerate from the final snapshot
before the final build.
