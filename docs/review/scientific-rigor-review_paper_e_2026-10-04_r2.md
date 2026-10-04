# Scientific Rigor Review: Paper E, revised manuscript (second review)

**Date**: 2026-10-04 | **Reviewer role**: Scientific Advisor | **Grade**: Major revision (two findings; no new cohort needed)
**Mean score**: 3.6 | **Dimensions**: D1=3.5 D2=3.5 D3=3 D4=4 D5'=3.5 D6=4

**Scope reviewed**: `docs/reports/paper_e/paper_e.tex` at commit `5ad6433bb` (generated source; line numbers below refer to it), the six files in `tables/`, `README.md`, `ANALYSIS_PLAN.md`, `scripts/paper_e_ceiling.py`, `scripts/paper_e_review_analyses.py`, `scripts/paper_e_sign_contribution.py`, `src/xai/lime_tabular.py`, `src/xai/shap_tabular.py` (settings only), every CSV under `outputs/analysis/paper_e/analysis/` and `posthoc/`, the stored SHAP and LIME run files (read to compute a new reference), and `references.bib` (key audit only).
**Prior review**: `scientific-rigor-review_paper_e_2026-10-04.md` (major revision, F01 to F13). Status of each finding is in the table below: 10 fixed, 3 partly fixed and carried.
**Regression guards**: no Paper E file is under an RCA-001/002/003 path guard. `python scripts/pubs/verify_claims.py`: "OK: 917 claims re-derived from artifacts, 1136 manuscript sites checked, 48 retired-value guards clear, 13 cited artifacts present, 27 file(s) fully registered, 21 file(s) clear of unpublished results".
**Not read**: the two PDFs in `submission/` (the review is of the generated `.tex`; page count and blind-PDF metadata were not rechecked); the full texts of the cited papers; `ACTIVE_CONTEXT.md` beyond its first 736 lines.

**Evidence labels.** *Re-derived* = recomputed by me from the CSVs or the stored runs. *Code* = read in the code. *Probe* = a small experiment run outside the repository (scripts in the session scratch folder, nothing written to the repository); it shows a problem and its rough size and is not an estimate fit to publish. *Record* = stated in a project document, not re-derived.

## One-line summary

The revision answers the first review well and every number I recomputed matches, but two readings are still stronger than the evidence: the overlap is called instance-level while most of it on Breast Cancer, and about half of it on Adult, is reproduced by pairing the SHAP explanation of one instance with the LIME explanation of another; and "LIME" is one non-default configuration whose kernel gives the perturbed samples almost no weight on Adult.

## Strengths

- All re-derived values match the manuscript (list under "Verified, no finding").
- The self-agreement experiment is the right answer to the earlier F01, and its main claim holds at the finest level available: SHAP–LIME overlap is below both self-agreements in 32 of 32 runs (*re-derived* from `ceiling_instances.csv`).
- The majority-sign baseline is reported next to the converted sign agreement, and the claim is limited to a global direction per feature. This is an honest treatment of a result that weakens the paper's own earlier headline.
- The held-out correctness contrast keeps the two opposite signs (MLP negative, RF positive, five of five seeds each).
- Post hoc status is stated in the abstract, the contributions, Section 3.7, section titles and captions.

## Status of the findings of the first review

| First review | Status | Note |
|---|---|---|
| F01 no within-method ceiling | Fixed | Section 4.2, Table 2. The requested sentence on the stored LIME stability on Adult was not added: carried into F02 below. |
| F02 converted sign agreement matched by a fixed direction | Fixed | Baseline 0.951 / 0.978 / 0.990 reported. The first review's 0.962 / 0.970 came from a slightly different definition; the script's values are the ones printed. |
| F03 correctness contrast confounded with training rows | Fixed | See F06 for two small gaps. |
| F04 intervals are ranges of seed means | Fixed | Stated in Section 3.6. Captions still say "95% interval" (F07). |
| F05 LIME selection and sampling | Fixed | Section 3.2. The kernel is not discussed (F02). |
| F06 rank measure on the wrong scale | Fixed | |
| F07 untested cause of low rank concordance | Fixed | |
| F08 wording stronger than the estimates | Fixed | |
| F09 SVM coverage | Partly | 29.5% is stated in Section 3.4 and the limitations; the SVM rows of Tables 1, 3, 4 and 5 carry no note (F07). |
| F10 "registered"; unreported plan items | Partly | Wording, sign intervals, shared-feature counts and medians done. The plan commit hash is not in the full version; contribution (iii) is not labelled post hoc for its held-out part (F06). |
| F11 citation fit | Fixed in wording | Full texts still not read by a reviewer. |
| F12 seed-42 sentence | Fixed | 0.412 against 0.369 to 0.413 (*re-derived*). |
| F13 public PDFs | Partly | PDFs untracked. The earlier PDFs remain in git history and in Zenodo 0.6.0; this must go in the cover letter (author action). |

## Findings

### F01 [major] — D1 / D3. The overlap is compared with uniformly random sets; a large part of it does not depend on the instance

**Passages.** Title: "Instance-Level Agreement". l.289–293 (chance reference 0.026 / 0.047 / 0.099). l.390–391: "In all three datasets the overlap was several times the expected overlap of random sets." l.493–496: "The dataset mattered most … Breast Cancer … gave much higher agreement". l.734: "The high agreement on Breast Cancer indicates that low agreement is not inevitable."

**Evidence (*re-derived* from the stored runs; one random draw, generator seed 20261004).** For every paired instance I kept its SHAP top-10 list and replaced its LIME list by the LIME list of another instance of the same run, then applied the prespecified `primary_agreement`. Mean of run means of the top-5 overlap:

| Dataset | Model | Same instance | Another instance | Another instance, same predicted class |
|---|---|---|---|---|
| Adult | LR | 0.485 | 0.263 | 0.266 |
| | SVM | 0.395 | 0.203 | 0.204 |
| | MLP | 0.335 | 0.128 | 0.130 |
| | RF | 0.389 | 0.199 | 0.202 |
| | XGB | 0.363 | 0.219 | 0.225 |
| | All | 0.393 | 0.202 | 0.206 |
| German Credit | All | 0.387 | 0.286 | 0.291 |
| Breast Cancer | RF | 0.738 | 0.661 | 0.648 |
| | XGB | 0.690 | 0.643 | 0.647 |
| | All | 0.714 | 0.652 | 0.647 |

**What is wrong.** Two uniformly random sets are not the right lower reference. Both methods draw their top features from a small group of globally important features, so two explanations of different instances already overlap far above 0.026 to 0.099. The part of the overlap that depends on the instance is about 0.19 on Adult, 0.10 on German Credit and 0.06 on Breast Cancer. On Breast Cancer, nine tenths of the reported agreement is agreement on a ranking that is nearly the same for every instance. This is the same structure the paper already reports for signs (a global direction per feature), and it was not checked for the overlap.

Consequences: (a) the dataset comparison reverses on the instance-specific part, so "the dataset mattered most" and the sentence at l.734 do not hold as written; (b) "several times the expected overlap of random sets" is true and uninformative; (c) the title promises instance-level agreement, and the evidence for it is the difference between the first two columns, not the first column.

Limit: I could not compute the same reference for the self-agreement experiment, because `ceiling_instances.csv` stores measures, not the lists. The reruns would have to save their top-10 lists.

**Fix.** Add this permutation reference as a dated deviation (a re-cut of stored runs, no explainer is run), with the plan's aggregation and several draws. Report it beside the chance reference in Section 3.3 and in Table 1 or the text of Section 4.1. Rewrite the dataset paragraph of Section 4.3 and the second Discussion paragraph: Breast Cancer shows high agreement on a global ranking and little instance-specific agreement. Save the top-10 lists in `paper_e_ceiling.py` so the same reference can be given for Table 2 when the experiment is next run.

### F02 [major] — D3 / D5'. "LIME" is one non-default configuration in which the perturbed samples carry almost no weight on Adult; the stored LIME stability on Adult is near zero and is not reported

**Passages.** l.236–246 (LIME settings). l.725–726: "For LIME, more perturbed samples would raise the repeatability; the 1000 used here are fewer than the default of the package." l.767–769: "one configuration of each explainer; other kernel widths, sample sizes or discretisation settings of LIME may change the estimates." l.780–781: "so its slopes are only loosely local." Table 5, columns LIME Stab.

**Evidence.**
- *Code.* The kernel width is fixed at 3 for all datasets. The package default is 0.75·√p: 7.8 on Adult, 5.9 on German Credit, 4.1 on Breast Cancer. The manuscript says that 1000 samples are fewer than the default and does not say that the kernel is narrower than the default.
- *Probe* (200 paired instances per dataset, seed 42, LIME's sampling and kernel reproduced from the package source). Sum of the kernel weights of the 999 perturbed samples, against weight 1 for the instance itself, median (5th to 95th percentile): Adult 0.26 (0.00 to 1.26); German Credit 2.2 (0.06 to 9.0); Breast Cancer 86 (12 to 149). The nearest perturbed sample is about 10, 8 and 4.5 standardised units from the instance. On Adult the local fit is decided by a few distant samples and the ridge penalty. This repeats on 200 instances what the first review saw on six (its F02, item 4).
- *Re-derived* from `instance_agreement.csv`. Stored LIME stability on Adult: median 0.001 to 0.009 by model, 95th percentile at most 0.10. On German Credit the median is 0.79 to 0.87 and on Breast Cancer 0.94 to 0.96. SHAP stability on Adult has medians 0.23 to 0.98.
- *Record.* The thesis review of 2026-08-28 (`ACTIVE_CONTEXT.md`) notes that Appendix C of the thesis gives LIME stability 0.664 at kernel width 10 against 0.000 at width 3 on Adult. The author's own earlier work shows that this width is the cause.
- *Probe* (Adult, seed 42, `n_100`, 40 instances per model, LIME rerun with width 3 and with the default width). Top-5 overlap between LIME at the default width and the stored LIME: 0.47 (LR), 0.34 (XGB), 0.25 (MLP). Stored SHAP against new LIME, width 3 then default: LR 0.56 and 0.52; XGB 0.43 and 0.56; MLP 0.31 and 0.21. LIME self-agreement, width 3 then default: 0.72 and 0.91; 0.59 and 0.65; 0.50 and 0.47.

**What is wrong.** (a) Two LIME configurations share as few top-5 features with each other as SHAP and LIME do. The title and the abstract say "SHAP and LIME"; the estimates are for LIME with width 3, 1000 samples and no discretisation, and the general limitation sentence does not tell the reader how much this matters. (b) The probe does not show that the default width would raise agreement with SHAP: the direction differs by model. So the kernel is not shown to explain the low overlap, and I do not claim it does; it is an uncontrolled factor of the same size as the effect studied. (c) The Adult LIME-stability column of Table 5 correlates disagreement with a variable confined to about −0.02 to 0.10; the values 0.10 to 0.12 there cannot be read as an association with stability. (d) The dataset ordering of agreement (Adult and German Credit low, Breast Cancer high) coincides with the ordering of the kernel weights, which is a concrete competing explanation next to "many one-hot features"; with F01 it leaves little of the dataset conclusion. (e) "Only loosely local" understates what the probe shows.

**Fix.** State in Section 3.2 that the kernel width is 3 against a default of 0.75·√p, and in the limitations what this implies for 108 and 61 features. Report the range of the stored LIME stability on Adult (a logged deviation from plan section 4, which forbids pooled quality means; one sentence about the range is enough) and remove or footnote the Adult LIME-stability column of Table 5. Either add a sensitivity run with the default width on the self-agreement subsample (LIME only; minutes for LR, MLP, RF and XGB) or name the configuration in the abstract ("LIME with a fixed kernel width of 3 and without discretisation"). Add the kernel to the candidate explanations of the dataset difference.

### F03 [minor] — D5' / D4. The random-forest row of Table 2 mixes two forests, and a limitation sentence contradicts it

**Passages.** l.297: "An instance entered only if the loaded model reproduced its stored prediction." l.786–788: "the stored binary does not reproduce all the predictions recorded in the runs; the analysis uses only the recorded outputs". Abstract l.78: "for every model tested".

**Evidence.** *Probe*: `rf.joblib` reproduces 0.745 to 0.815 of the stored predictions in each of the 15 paired random-forest blocks (0.750 to 0.797 at `n_100`, the blocks used for Table 2). *Re-derived*: for the random forest a new SHAP run shares 0.640 of its top-5 with the stored SHAP run against 0.887 with another new run; no other model shows this (LR 0.797 against 0.759, MLP 0.672 against 0.728, XGB 0.788 against 0.754).

**What is wrong.** For this row, self-agreement is measured on the present binary, on the roughly four fifths of the candidates whose prediction it reproduces, while SHAP–LIME agreement is that of the stored explanations of another forest. The gap is large (0.356 against 0.783 and 0.887), so the conclusion probably holds, but the manuscript does not say it and the sentence "the analysis uses only the recorded outputs" is false for Table 2. The plan's "(none was skipped)" cannot be true for the random forest at these rates; I could not see the run log. The plan also says "760 instances in 26 runs"; the file has 760 instances in 32 runs.

**Fix.** Footnote the row; correct the limitation sentence and the two plan statements; give the number of skipped candidates per model.

### F04 [minor] — D4. One sentence of the stability paragraph reports the wrong column

**Passage.** l.659–660: "On Breast Cancer the correlation was negative for the random forest and near zero for gradient boosting."

**Evidence (Table 5).** Breast Cancer, gradient boosting, stability: −0.34 (SHAP) and −0.27 (LIME). The sentence fits the LIME-fidelity column (−0.28 and 0.01).

**Fix.** Move the sentence to the fidelity paragraph and name the measure, or delete it.

### F05 [minor] — D1. "Differences between models follow in part the differences in self-agreement" rests on one model

**Passages.** l.433–435; l.481–484; l.731–733.

**Evidence (*re-derived* from `ceiling_instances.csv`).** Over the four Adult models the correlation between SHAP–LIME overlap and LIME self-agreement is 0.57 and with SHAP self-agreement −0.20 (four points). The random forest has the highest self-agreement of both methods and the second-lowest SHAP–LIME overlap. Within runs, the instance-level Spearman correlation between SHAP–LIME overlap and self-agreement is 0.08 (LIME) and 0.01 (SHAP).

**What is wrong.** Only the multilayer perceptron supports the sentence. At instance level, low self-agreement does not go with low agreement between methods.

**Fix.** Say that the multilayer perceptron is lowest on both and that the other three models show no such relation; drop "supported by Table 2" as a general reading.

### F06 [minor] — D5'. Held-out contrast: one model and one label missing

- l.614–616 gives the held-out difference for LR and XGB and not for the SVM (*re-derived* from `review_heldout_contrast_summary.csv`: +0.028, two seeds of each sign, 5 of 14 runs included). State it with its coverage.
- Table 4 gives only the full-sample contrast; the held-out values are in the text only. A column or a note would let the reader compare.
- Contribution (iii), l.142–145, "also when training instances are excluded", is post hoc and not labelled.

### F07 [minor] — D5'. Carried from the first review (F04, F09, F10)

- Tables 1, 2, 4 and 6 and Figs. 2 and 3 give a "95% interval" or "seed-clustered interval" for groups with three seeds. Section 3.6 explains it; a reader of a table alone is not told. Add "spread of seed means" to the captions.
- No note on the SVM rows (29.5% coverage; three of four seeds in Table 4).
- The full version does not give the hash of the plan commit (`7726bb0a9`).

### F08 [minor] — D4. Project documents cited by the paper still state claims the manuscript withdrew

**Evidence.** `README.md` l.62–71: "Agreement depends on model family and dataset", "Disagreement is higher where LIME's local fidelity is lower", "The two explainers differ in which features they rank first, not in the direction they assign." Open item 4 asks for the conversion that was done. l.128 says five table files; there are six. `ANALYSIS_PLAN.md`, entry of 2026-10-04: "The explanation of 2026-10-03 is confirmed." The Data Availability statement sends the reader to this README and plan, and both go into the Zenodo archive.

**Fix.** Update the README summary; add a line under the plan entry pointing to the later entry that qualifies it. This changes text only, so no new Zenodo version is required by the README's own rule, but the archive cited in the full PDF (0.7.0) will keep the old README.

### F09 [suggestion] — D6. The comparison in Table 2 uses new runs for self-agreement and stored runs for SHAP–LIME

The script already has both new SHAP and new LIME lists for each instance. Computing SHAP–LIME overlap between the new runs (four pairs) would put the three columns of Table 2 on the same runs and remove the random-forest problem of F03. "So it is real" (l.724) would then rest on like-for-like evidence.

### F10 [suggestion] — D3. Title

If F01 is accepted, "Instance-Level Agreement" needs either the permutation reference in the abstract or a title without "Instance-Level" (for example "Agreement between SHAP and LIME on the Same Instances").

## Verified, no finding

- *Re-derived* from `instance_agreement.csv`: 31,411 pairs, 86 runs; top-5 0.393 / 0.387 / 0.714; top-10 0.507 / 0.480 / 0.669; Kendall 0.126 / 0.122 / 0.517; sign 0.717 / 0.511 / 0.374; medians of run means 0.393 / 0.416 / 0.712; all per-model values of Table 1; intensity 0.395 / 0.394 / 0.390; LR above MLP in five of five seeds; seed means Adult 0.369 to 0.413 with seed 42 at 0.412; German Credit seed means 0.343, 0.391, 0.426 and Breast Cancer 0.671, 0.679, 0.792, equal to the printed interval limits as Section 3.6 says.
- *Re-derived* from `ceiling_instances.csv`: 760 instances; all values of Table 2 (LIME 0.690 / 0.642 / 0.836; SHAP 0.782 / 0.708 / 0.939; SHAP–LIME 0.393 / 0.382 / 0.724 and the eight model rows); SHAP–LIME below both self-agreements in 32 of 32 runs.
- Matched against the summary CSVs: converted sign agreement and majority-sign baseline (0.945 / 0.960 / 0.990 and 0.951 / 0.978 / 0.990), shared features 2.70 / 2.67 / 4.05, re-ranked overlap 0.416 / 0.393 / 0.633, shared-only Kendall 0.193 / 0.243 / 0.613, held-out contrasts (MLP −0.042, RF +0.049, LR 0.000, XGB −0.004, seed signs), training shares 0.707 / 0.840 / 0.006, SVM coverage 29.5%, chance values.
- *Code*: `paper_e_review_analyses.py` implements the baseline, the re-ranking, the shared-only Kendall and the held-out contrast as the plan describes them; `paper_e_ceiling.py` varies only the random state and uses the prespecified agreement function.
- SVM SHAP: all 15 configuration files are identical (KernelSHAP, 50 background instances); the runs are partial files from several machines, which matches "incomplete" in Section 3.4.
- References: 25 cited keys, 25 entries, no orphan, no unused entry, no duplicate key.
- The lane tree was clean before and after the review; no manuscript, registry or result file was changed.

## Could not verify

- The run log of the self-agreement experiment (number of skipped candidates).
- Self-agreement on German Credit and Breast Cancer by rerun (model binaries are not tracked).
- The permutation reference for self-agreement (lists not stored).
- The two PDFs: page count, layout, metadata.
- Full texts of the cited papers.

## Dimension rationale

- **D1 = 3.5.** Numbers sound; the lower reference for the overlap does not address what the title asserts (F01); one model carries a general sentence (F05).
- **D2 = 3.5.** Descriptive questions; the self-agreement comparison could have failed and did not. No refutation criterion for "instance-level".
- **D3 = 3.** Instance-level framing (F01) and one LIME configuration presented as LIME (F02).
- **D4 = 4.** One sentence on the wrong column (F04), one false limitation sentence (F03), stale project documents (F08).
- **D5' = 3.5.** Post hoc labelling is good; the kernel, the near-zero LIME stability on Adult and the random-forest binary in Table 2 are not disclosed (F02, F03).
- **D6 = 4.** Units, aggregation and the absence of tests are right; Table 2 mixes new and stored runs (F09).

## Readiness assessment

Not ready to submit, and close. F01 needs one re-cut of stored runs and three rewritten passages; F02 needs two sentences, a note on Table 5 and, preferably, a short LIME-only sensitivity run. F03 to F08 are text. The new analyses change result files, so a new Zenodo version is needed afterwards (the README's rule).

## Questions for the author

1. Why was the kernel width fixed at 3 for all three datasets?
2. Do you want the paper to be about agreement on the same instances (then the permutation reference goes in the abstract), or to keep "instance-level" and make the instance-specific part the headline?
3. Is the run log of `paper_e_ceiling.py` available, to give the number of skipped random-forest candidates?
4. Would you accept a default-width LIME rerun on the 400 Adult instances of the self-agreement subsample as a sensitivity analysis?
