# Review analysis: Paper E, AAIR revision 1

Every comment of `DECISION_LETTER.md` is one item. The letter will answer every item
(none left unattended). Verdict: **REMEDIATE** (the manuscript changes) or
**EXPLAIN** (answered in the letter, with a sentence in the manuscript where useful).
**AMBIGUOUS** marks a comment whose request is open; the best reading taken is stated and
will be stated in the letter as well, so the reviewer can correct it.

Table numbers are those of the submitted manuscript: 1 agreement, 2 self-agreement,
3 sign, 4 correct vs misclassified, 5 quality, 6 secondary feature sets.

## Editor

| ID | Comment | Verdict | WP |
|---|---|---|---|
| ED-1 | Decision: major revision | Answered by the cover letter and the revision as a whole | WP7 |

## Reviewer 1 (minor revision)

| ID | Comment | Verdict | What will be done | WP |
|---|---|---|---|---|
| R1-0 | (Comments to editor and summary) held-out sensitivity, bound conclusions to configuration, SVM caution | Covered by R1-1, R1-2, R1-5 | Cross-referenced in the letter | — |
| R1-1 | Held-out-only sensitivity for the principal top-k agreement on Adult, or justify why training membership does not matter | REMEDIATE | Recompute Table 1 measures (top-5, top-10 Jaccard, Kendall) on held-out Adult instances only, from the stored instance-level rows; report it in text (and supplement); no new runs | WP2 |
| R1-2 | State in Abstract and Conclusion that agreement levels are conditional on the LIME configuration (width 3; W3-vs-default overlap 0.370) | REMEDIATE | Abstract, Conclusion and the RQ answers say "under the evaluated configuration"; the 0.370 figure cited where the conclusion is drawn | WP4 |
| R1-3 | Describe self-agreement as a sensitivity/reference analysis, not a general property | REMEDIATE | Rewording in Abstract, Results, Conclusion: "reference analysis on a 100-instance subsample, one pair of random states" | WP4 |
| R1-4 | Make the pre-specified sign analysis vs the post-hoc contribution-corrected interpretation visible in the Discussion | REMEDIATE | Discussion paragraph split into "pre-specified (not like for like)" and "post-hoc, corrected"; Table 3 header labels both blocks | WP4 |
| R1-5 | Qualify SVM (2,064 of 7,000; 29.5%; unbalanced classes) wherever model families are compared; no model-family ranking | REMEDIATE | Sweep every family comparison; SVM flagged in each; sentence that no family ranking is claimed | WP4 |

## Reviewer 2 (major revision)

| ID | Comment | Verdict | What will be done | WP |
|---|---|---|---|---|
| R2-0 | (Comments to editor) numbers in Tables 1, 4, 5; overlap; LIME; generalizability | Covered by R2-1 … R2-6 | Cross-referenced | — |
| R2-1 | Signs of values and interval bounds inconsistent in Tables 1, 4, 5 (e.g., Table 4 positive differences with means that imply negative); verify all numbers against outputs | REMEDIATE — **reviewer is right; defect confirmed** | Cause found 2026-11-24: the Word build dropped every LaTeX minus (`$-$`): 29 in the source, 0 in the submitted `.docx`. The analysis and the LaTeX tables are correct (e.g., Table 4, MLP: −0.059 [−0.069, −0.049]). Fix the converter, add a check that compares every number of the Word tables and text with the generated source and the CSVs, rebuild; RCA with a regression guard. Thank the reviewer explicitly | WP1 |
| R2-2 | Extend held-out sensitivity to the main agreement results | REMEDIATE | Same as R1-1 | WP2 |
| R2-3 | Sensitivity to standard LIME settings and different sampling budgets | REMEDIATE (new computation, bounded) | On the self-agreement subsample: LIME with package defaults (default width **and** discretisation on) and with sampling budgets (e.g., 1,000 / 5,000 / 10,000) vs SHAP; report the overlap per setting. Needs a run (decision D-1) | WP3 |
| R2-4 | Permutation reference with instances of the same predicted class | REMEDIATE | Recompute "Other" pairing SHAP of i with LIME of j restricted to j of the same predicted class, from stored lists; report beside the current reference; no new runs | WP2 |
| R2-5 | Limited seeds and fitted models restrict generalizability; strengthen validation where feasible; cautious interpretation | REMEDIATE + EXPLAIN. **AMBIGUOUS:** "strengthen validation" is not specified. Best reading: show that the conclusions do not rest on one seed or one model, with what exists | Leave-one-seed-out ranges for the main estimates; state the unit of inference (5 seeds, one fitted model per family) in Methods and Limitations; refitting per seed discussed as future design (see R3-3) | WP2, WP4 |
| R2-6 | Correct numerical inconsistencies; document agreement measures and configurations for independent verification | REMEDIATE | WP1 for the numbers; a configuration table (each explainer, each parameter, per dataset) and the measure definitions in a supplementary file (the paper is at the 10 figures+tables limit); Zenodo release updated with the revision | WP1, WP5 |

## Reviewer 3 (major revision)

| ID | Comment | Verdict | What will be done | WP |
|---|---|---|---|---|
| R3-0 | (Strengths; comments to editor; closing thanks) | Acknowledged in the letter | — | WP7 |
| R3-1 | LIME configuration (width 3, no discretisation) is non-standard; more extensive sensitivity and stronger justification | REMEDIATE + EXPLAIN. **AMBIGUOUS on "stronger justification":** the width was inherited from the protocol of the cohort and has no technical rationale; a rationale cannot honestly be invented afterwards. Best reading: state its origin plainly and replace the missing justification with evidence (WP3) | Same computation as R2-3; Method states where width 3 and no discretisation come from and why discretisation was off (continuous slopes comparable with SHAP values); conclusions bounded (R1-2) | WP3, WP4 |
| R3-2 | Three tabular datasets limit generalization; discuss dataset characteristics; separate evidence-supported conclusions from broader implications | REMEDIATE (text) | Limitations: dimensionality, encoding, domain of the three datasets; Conclusion split into "supported by the evidence" and "implications to test" | WP4 |
| R3-3 | Adult: one fitted model per family, many seeds → training-row overlap; discuss per-seed retraining as an alternative design | REMEDIATE (text + WP2) | Paragraph in Method/Limitations naming per-seed retraining as the cleaner design and why it was not used (the cohort is reused, not rerun); held-out analysis of WP2 bounds the effect | WP2, WP4 |
| R3-4 | Separate pre-specified from exploratory findings more consistently (self-agreement, permutation references, sign conversion) | REMEDIATE | A labelled paragraph in Method listing pre-specified vs exploratory analyses; "(exploratory)" marked consistently in headings, captions, Abstract and Conclusion | WP4 |
| R3-5 | Condense Discussion and Limitations; avoid repeated caveats | REMEDIATE | Each caveat stated once (Limitations) and referenced elsewhere; target net shortening of these two sections, which also pays for the new text of WP2–WP4 | WP6 |
| R3-6 | Overall: LIME configuration, scope, exploratory presentation | Covered by R3-1, R3-2, R3-4 | Cross-referenced | — |

**Count:** 1 editor item + 6 (R1) + 7 (R2) + 7 (R3) = 21 items; 3 marked AMBIGUOUS
(R2-5, R3-1 "justification", and R2-3 for the budgets chosen, see plan D-1).
