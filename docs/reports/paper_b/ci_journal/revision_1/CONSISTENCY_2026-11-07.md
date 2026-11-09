# Paper B, revision 1: consistency of the manuscript, the ledger, the response and the proposal

Checked on 2026-11-08 against `manuscript/paper_b_ci_rev1.tex`, `CHANGELOG.md`,
`RESPONSE_TO_REVIEWERS.md` and `PROPOSAL_2026-11-06.md`. Regenerate before the final build.

## Result

| Check | Result |
|---|---|
| Every ledger change is in the manuscript at the place it names | yes (46 of 46) |
| Every ledger change appears in the response of each item it names | yes |
| Every change listed in a response names that item in the ledger | yes |
| Every answered item exists in the review analysis (ED-2, ED-3: no answer, by decision) | yes (51) |
| Proposal P-01 – P-24 match ledger C-001 – C-024 (items) | yes |
| Section, table and figure numbers quoted in the response match the manuscript | yes |

Fixed in this pass: later changes (C-029 – C-035) added to the 15 responses they serve; R1-8
and R2-8 added to the ledger and proposal rows that the responses already cited; R1-9 said
the recent work was cited in §3.3–3.4 (it is in §1–§2) and gave 52 references (53); R2-6 still
carried the open decision D-A, which was applied in §3.1 (C-025), and R1-M1 now discloses it
too; R1-m13 said it waited for the grouping fix, which is in the code (28ad03dc1); the abstract had the same CPU-time ambiguity as §1 (C-036); the proposal
gained Part E (implementation status and corrections: hypotheses renumbered, ED-2 and ED-3
not answered).

## Changes: ledger, manuscript, response, proposal

| Change | Proposal | Where in the manuscript | Items answered | State |
|---|---|---|---|---|
| C-000 | — | `manuscript/paper_b_ci_rev1.tex` | none | working copy |
| C-001 | P-01 | §1 | R1-1, R1-M1, R2-8, R1-8 | done |
| C-002 | P-02 | §2 | R1-9, R2-8 | done |
| C-003 | P-03 | old §4.1 | R2-6, R1-M1, R2-7, R1-8 | done |
| C-004 | P-04 | §3, everywhere | R2-7 | done |
| C-005 | P-05 | §3.1 | R1-m2, R2-4 | done |
| C-006 | P-06 | §3.1, Table 1 | R1-m3, R1-M2, R1-8 | done |
| C-007 | P-07 | §3.2 | R1-m4, R1-m5, R1-M2 | done |
| C-008 | P-08 | §3.3 | ED-1, R1-4, R1-M4, R2-3, R1-m12 | done |
| C-009 | P-09 | §3.4 | R1-m6, R1-m7, R1-3 | done |
| C-010 | P-10 | §3.6 | R2-1a, R1-5, R1-M8, R1-m14 | done |
| C-011 | P-11 | §3.5 | R1-2, R1-M2, R1-M3, R1-7, R1-M14 | done |
| C-012 | P-12 | §4.1, Table 2 | ED-1, R1-7, R1-M14, R2-6, R1-m8, R1-8 | frame; values [R] |
| C-013 | P-13 | old §4.3 | R1-m9 | done |
| C-014 | P-14 | §4.2, Table 3 | R2-1a, R2-1b, R1-5, R1-M8 | frame; values [R] |
| C-015 | P-15 | §4.2 | R1-M9 | frame; values [R] |
| C-016 | P-16 | §4.3, Fig. 1 | R2-2, R1-M5, R1-M11, R1-M12, R2-3, R1-M4, R1-8 | frame; values [R] |
| C-017 | P-17 | §4.5, Table 4 | R1-6, R1-M10, R2-5, R1-m11, R1-m12 | frame; values [R] |
| C-018 | P-18 | §4.4 | R1-3, R1-M6, R1-M7, R1-M13, R1-m13, R1-8 | frame; values [R] |
| C-019 | P-19 | §5, Table 5 | R1-M15, R1-10, R1-m15 | frame; values [R] |
| C-020 | P-20 | §5 | R1-1, R1-M1, R2-6 | frame; one sentence [R] |
| C-021 | P-21 | §6 | R1-10, R1-m15 | frame; values [R] |
| C-022 | P-22 | Abstract | R1-m1, R1-m15 | frame; values [R] |
| C-023 | P-23 | Figures | R1-m10 | old figures removed; Figure 1 [R] |
| C-024 | P-24 | Build | R2-7 | done |
| C-025 | D-A | §3.1 | R2-6, R1-M1 | done |
| C-026 | — | Keywords | none | done |
| C-027 | P-02 | §2, §3.2, References | R1-9 | done |
| C-028 | P-02 (D-6, option A) | §1, §2, §5 (limitations), References | R1-9 | done |
| C-029 | — | §3.1, §3.4, §3.5, §4.3 | R1-m2, R2-4, R1-3, R1-M3, R1-7, R1-M12, R2-2 | done |
| C-030 | — | §3.3 | R1-m12 | done |
| C-031 | — | §1 | R1-9 | done |
| C-032 | — | §1, References | R1-9, R2-1a | done |
| C-033 | — | §1 | R1-1, R1-M1, R1-8 | done |
| C-034 | — | §5.1, Table 5 | R1-M15 | done |
| C-035 | — | §6 | R1-10, R1-m15 | frame; values [R] |
| C-036 | — | Abstract | R1-m1 | done |
| C-037 | — | §4.2 | R1-M9 | done |
| C-038 | — | §1, §3.1, §3.4, §3.5, §3.6, Table 2, §4.2, Table 3, §6, Abstract, `scripts/paper_b_analyze.py` | R1-5, R1-M8, R2-1a | done |
| C-039 | — | §3.6 | R1-M8, R2-1a | done |
| C-040 | — | §3.2, §4.1, Table 2, §4.5, Table 4, §6, Abstract | ED-1, R1-6, R1-7, R1-10, R1-M1, R1-M10, R1-M14, R1-m1, R1-m5, R1-m8, R1-m11, R1-m15, R2-3, R2-5, R2-6 | filled from the quality pass |
| C-041 | — | Table 4 | R1-m11 | done |
| C-042 | — | §4.2, Table 2, Table 3, Table 5, §6, Abstract | ED-1, R1-5, R1-7, R1-M8, R1-m8, R2-1a, R2-1b, R2-6 | filled from the Adult timing cells; matched tree run [R] |
| C-043 | — | §4.1, Table 5, §5, §5.1 | R1-6, R1-10, R1-M3, R1-M7, R1-M10, R1-M15 | filled; sweep and control parts of §5 and §5.1 [R] |
| C-044 | — | §6 | none | done |
| C-045 | — | Supplement (S7–S13) | R1-M14 | built; S9 matched run, S10 and part of S11 [R] |
| C-046 | — | Supplement S9, results/ | R1-M14 | done |

## Items not yet closed

Sources of the missing values:

- **Q**: main quality pass: complete (575/575) and filled (C-040)
- **T**: timing pass: Adult complete and filled (C-042); other datasets running, exploratory
- **S**: configuration sweep (§4.3, Figure 1): not started
- **V**: validity controls, no-noise and valid one-hot (§4.4): not started
- **M**: grouped masking (§4.4): not started; grouping fix in 28ad03dc1
- **X**: matched RF vs XGBoost run (§4.2): not started
- **A**: author action

| Item | Status | Waits for | What is missing |
|---|---|---|---|
| R1-1 | pending | Q | §5.2: which earlier statements are confirmed, qualified or reversed (author's reading of the filled results) |
| R1-3 | pending | V | §4.4 results of the stability controls |
| R1-6 | pending | S, T | Table 5 scope column; §4.5 is filled |
| R1-9 | pending | A | the author reads the 15 recent abstracts (REFERENCE_AUDIT.md); text and list are done |
| R1-10 | pending | Q, S, V, T | Table 5 scope column and §6 |
| R1-M1 | pending | Q | §5.2 paragraph on earlier work (results available; text to write) |
| R1-M4 | pending | S | §4.3: whether the differences hold across LIME budgets and SHAP estimators |
| R1-M5 | pending | S | §4.3 sweep results |
| R1-M6 | pending | V | §4.4: stability under valid one-hot perturbations |
| R1-M7 | pending | V, S | §4.4 and §4.3: LIME stability against noise and kernel width |
| R1-M9 | pending | X, T | §4.2: whether the reversal follows tree size or implementation |
| R1-M10 | pending | S, T | Table 5 scope column; Table 4 and §4.5 are filled |
| R1-M11 | pending | S | §4.3 over seeds and models |
| R1-M12 | pending | S | §4.3 on the common valid instances |
| R1-M13 | pending | M | §4.4 masking schemes on all models |
| R1-M15 | pending | Q, S, V, T | Table 5 scope column and the recommendations in §5.1 |
| R1-m1 | pending | Q, S, V, T | abstract values |
| R1-m10 | pending | S | Figure 1 is generated from the sweep |
| R1-m13 | pending | M | §4.4 masking results; rule stated |
| R1-m15 | pending | Q, S, V, T | labelled findings in §5, §6 and the abstract |
| R2-2 | pending | S | §4.3 Pareto fronts, Figure 1 |
| R2-3 | pending | S | §4.3 kernel-width results |

Closed: ED-1, R1-2, R1-4, R1-5, R1-7, R1-8, R1-11, R1-M2, R1-M3, R1-M8, R1-M14, R1-m2, R1-m3, R1-m4, R1-m5, R1-m6, R1-m7, R1-m8, R1-m9, R1-m11, R1-m12, R1-m14, R2-1a, R2-1b, R2-4, R2-5, R2-6, R2-7, R2-8 (29 items).

Count of pending items by source: Q 6, T 7, S 14, V 7, M 2, X 1, A 1.

## Mandatory before submission

- Length review by the author once every result is in (13 pages after C-042; only references spill onto page 13). Do not trim before then; do not submit without it (author, 2026-11-08).
