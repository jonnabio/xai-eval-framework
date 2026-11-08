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
