# Handoff between the two laptops (Paper B, revision 1)

## 2026-11-07, from the documentation laptop to the experiment laptop

**The only thing pending is the results of cohort B2.** All text work is done and consistent
(`CONSISTENCY_2026-11-07.md`): manuscript, ledger (C-000 – C-037), response letter and proposal
agree; 17 of 51 items are closed, and 33 of the 34 open items wait only for results. The
remaining one (R1-9) waits for the author's reading of the 15 recent abstracts, not for this
laptop.

Merged to `main` through pull requests; `paper/b-ci-revision-1` stays open. Pull it with
`--no-rebase` (a rebase drops the merge commit from `main` and the lane guard then refuses
commits).

What the documentation laptop needs from the runs, in this order:

| Study | Fills | Open items |
|---|---|---|
| Main quality pass (finishing) | Table 2 (Adult), Table 4 (other datasets), §5.2 | 12 |
| Timing pass | Table 3 | 4 (+ R1-M9 with the matched run) |
| Configuration sweep | §4.3, Figure 1 | 7 (+ R1-M7 with the controls) |
| Validity controls: no noise, valid one-hot | §4.4 | 2 |
| Grouped masking (after the grouping fix 28ad03dc1) | §4.4 | 2 |
| Matched random forest vs XGBoost | §4.2 | 1 |
| All of the above | Table 5, abstract, §6 | 4 |

Two checks for the experiment laptop before the final analysis:

1. In the partial analysis of the 18:21 snapshot, `quality_checks.csv` reports
   `stability_zero_vectors_mean` of 0.88 (LIME) and 0.95 (LIME full) on Adult, and 0 for every
   other explainer. Confirm in the raw rows whether most perturbed LIME explanations on Adult
   are all-zero vectors, and why, before the stability comparison is used.
2. `status.json` of the same analysis reports `jobs_finished: 0` of 575 while 115 cells have
   results. Confirm that the analysis counts finished jobs the way the orchestrator does.

When the results are final, push them on `paper/b-rev1-runs` and say so here; the
documentation laptop then fills every [R] marker and runs `check_revision.py --final`.

## 2026-11-07, answer from the experiment laptop (2fd1cb7f9)

Both checks are closed. (1) `stability_zero_vectors_mean` is a count per stability instance
out of 15 perturbed explanations, not a share: 2.7% (LIME) and 3.0% (LIME full) of the
perturbed vectors on Adult are all-zero; `quality_checks.csv` now has
`stability_zero_vector_share`. (2) The analysis counted finished jobs in the local live
folder instead of `--root`; it now counts in the analysed root (test added). Still pending:
the cohort B2 results only.

## 2026-11-07 (late), from the documentation laptop: cost tested in wall time (C-038)

The first timing cells show Windows CPU time moving in 15.6 ms steps (SHAP 31.25 ms, LIME 0 or
15.6 ms on logistic regression). Author's decision: H2 is tested in **wall-clock time**; CPU time
and rows stay descriptive. Changed: the manuscript (§3.1, §3.4–3.6, Tables 2–3, §6, abstract) and
`scripts/paper_b_analyze.py` (tests `wall_ms`; `cpu_ms` descriptive). **Nothing changes for the
running timing pass**: it already records wall time for every repetition. Do not restart it.
Pull `paper/b-ci-revision-1` (no rebase) before the final analysis.

## 2026-11-07 (late), correction and quality results

Correction to the answer above: with `stability_T` = 15, a mean of 0.877 and 0.950 all-zero
vectors per stability instance is **5.8% (LIME) and 6.3% (LIME full)**, not 2.7% and 3.0%; the
`stability_zero_vector_share` column of the final analysis gives these values. The manuscript
states 5.8% and 6.3% (§4.1).

The quality results (575 of 575 jobs) are filled in the manuscript (C-040): Table 2 except
p_Holm and the cost rows, Table 4, §4.1, §4.5, §3.2 (overlap), §6 and the abstract. p_Holm waits
for the cost tests, which complete the family of 12. Still needed from this laptop's runs: the
timing pass, then the sweep, the validity controls, the grouped masking and the matched run.

## 2026-11-08, from the documentation laptop: cost results filled (C-042)

The 25 Adult timing cells (snapshot 992d20038) are analysed and filled: Table 2 cost rows and the
Holm-adjusted p of the family of 12, Table 3, §4.2, the Table 5 cost row, §6 and the abstract.
The timing pass need not stop; the other datasets are exploratory and go to the supplement.

One check for this laptop: Anchors on XGBoost records 0 rows and 0 model calls in every cell.
`counted_methods` includes `XGBClassifier.predict_proba` but not `XGBClassifier.predict`, which
Anchors probably calls. Do not restart the run for it; confirm the cause, and say whether a
short rerun of Anchors on XGBoost with the counter fixed is feasible (rows only, not time).
Until then Table 3 excludes Anchors' rows on XGBoost and says so.

## 2026-11-09, from the documentation laptop: every result filled

All cohort B2 runs are complete and in the manuscript: validity controls (C-048), sweep quality
and Figure 1 (C-049), sweep timing and the matched tree-ensemble run (C-050). No [R] marker is
left in the manuscript, the abstract or the supplement (52 pages, S9-S11 complete). Response
letter: 49 remediated, 1 explained, 1 pending (R1-9, the author's reading of the recent
abstracts). Length: the author decided to submit at 15 pages and let the editor decide; options
to shorten are in `LENGTH_OPTIONS_2026-11-09.md`. The Anchors-on-XGBoost counter question is
answered by the counter fix (f64db3236); the main runs keep "not counted" for those rows.
The run laptop has no further runs queued.
