# Scientific Rigor Review: Paper F

**Date**: 2026-10-12 | **Reviewer role**: Scientific Advisor | **Grade**: Minor revision
**Mean score**: 3.9 | **Dimensions**: D1=4 D2=5 D3=3.5 D4=3 D5'=3.5 D6=4.5

**Scope reviewed**: `docs/reports/paper_f/paper_f_template.tex` and the rendered
`paper_f.tex` at `8130db825` (whole text); `generated/tab_datasets.tex`,
`generated/tab_primary.tex`, `generated/tab_adult.tex`; `figures/fig1.png`;
`ANALYSIS_PLAN.md` (version 2 and its section 12); `scripts/paper_f_analyze.py`,
`scripts/paper_f_report.py`, `docs/reports/paper_f/scripts/build_paper_f.py`; the result
files of `outputs/analysis/paper_f/results/` (commit `b7b8d576b`).
**Prior review**: none for Paper F. This is the first.
**Regression guards**: RCA-001 applies (manuscript numbers re-derive from artifacts);
Paper F files are under `[coverage]` and `[exclusivity]` since `3057490f4`. RCA-002 and
RCA-003 guard no Paper F file. `verify_claims.py`: "OK: 1287 claims re-derived from
artifacts, 1626 manuscript sites checked, 60 retired-value guards clear, 13 cited
artifacts present, 33 file(s) fully registered, 25 file(s) clear of unpublished results".
**Limit of this review**: it was written in the session that wrote the text under review,
at the author's request. It is not independent.

## One-line summary

The design, the test and the numbers hold; one conclusion and the last sentence of the
abstract say more than the paper's own rankings support, and two departures from the
registered plan are not named in a paper that rests its credibility on that plan.

## Strengths

- The hypothesis, the measures, the dataset rule and the decision rule were fixed and
  committed before any explanation was computed, and the analysis was run once.
- The unit of analysis is the dataset. Instances, classifiers and seeds are not counted
  as independent evidence.
- The decision rule is applied as written, including where it gives the weaker outcome
  (faithfulness gap, lower end 0.4875 against 0.5).
- Every printed number is a placeholder read from a result file and is registered.
- Re-derived here from `cells.csv`, independently of the analysis script: the rankings
  of all four measures equal `ranks.csv`, and the mean pairwise Spearman correlations are
  0.6683, 0.8783, 0.7894 and 0.8683, equal to `primary.csv`.

## Findings

### F01 [major] — D4 (Argument coherence) / D3 (Scope calibration)

**Where**: Abstract, last sentence; Discussion, second paragraph; Conclusion 2.
**Text**: "the order below it transfers less"; "Below the first place the order moves";
"the exceptions are found in the middle of the order"; "What transfers best is the first
place on a measure."
**Evidence**: counted from `ranks.csv`, the method most often ranked first and the method
most often ranked last hold their place on this many of the 16 datasets:

| Measure | Most frequent first | Most frequent last |
|---|---|---|
| Faithfulness gap | 13 (SHAP) | 10 (DiCE) |
| Stability | 14 (SHAP) | 16 (DiCE) |
| Sparsity | 11 (DiCE) | 14 (SHAP; tied last on one more) |
| Cost | 15 (LIME) | 8 (Anchors and DiCE, 8 each) |

The first place is the more regular one on the faithfulness gap and on cost. On
stability and sparsity the last place is at least as regular as the first. The paper's
own Discussion says so two lines earlier (DiCE is the least stable on every dataset).
The general statement is therefore contradicted by two of the four measures.
**Fix**: state what the counts support. The first place is the same on most datasets
(11 to 15 of 16). The irregular part is specific: LIME against Anchors on faithfulness
and stability, and Anchors against DiCE on cost, faithfulness and sparsity (Table 3).
Drop "transfers best" and "the middle of the order".

### F02 [minor] — D5' (Reporting honesty)

**Where**: Introduction, end ("fixed in a plan committed to a public repository before
any explanation was computed"); Materials and methods, Statistical analysis.
**Evidence**: `ANALYSIS_PLAN.md`, section 12, entry of 2026-10-11: the variance shares
are a balanced decomposition of sums of squares, not the linear mixed model the plan
names, and the cost as a ratio to the prediction time (plan section 3) was not computed.
Section 10 of the plan requires a deviation to be "named in the paper if it touches a
reported result". The paper describes what was computed and does not say that it departs
from the plan.
**Fix**: one sentence in the last section naming the two departures and pointing to the
plan's log.

### F03 [minor] — D5' / D4

**Where**: Table 2, column "Seeds", row Sparsity; Results, "The agreement between seeds
inside a dataset is 0.95, 0.97, 1.00 and 0.98".
**Evidence**: `primary.csv`, `ceiling_seeds` for sparsity is 0.9950. At two decimals it
prints as 1.00, which reads as identical rankings in every seed; they are not.
**Fix**: print this quantity with three decimals in the table and in the text.

### F04 [minor] — D3 (Scope calibration)

**Where**: Conclusion 1: "is largely a property of the methods".
**Evidence**: each method has one configuration (stated under sources of error). DiCE
runs with random search, and its last place on stability on all 16 datasets may follow
from that choice as much as from the method. The order is a property of the methods as
configured and as measured here.
**Fix**: "of the methods as configured here"; name the random search of DiCE where the
single configuration is discussed.

### F05 [minor] — D1 (Evidence relevance)

**Where**: Sources of error: "they name few features ... so part of their low gap
reflects a short explanation".
**Evidence**: `secondary.csv` supports the premise (mean features used, over the 64
dataset-and-classifier cells: Anchors 3.0, DiCE 3.0, LIME 9.5, SHAP 21.3). The paper
prints no figure for it, so the reader cannot check the premise, and the inference
("part of their low gap") is not tested.
**Fix**: print the four means (they would need registering), or keep the sentence as a
stated possibility ("may reflect").

### F06 [minor] — D6 (Methodological rigor)

**Where**: Statistical analysis.
**Evidence**: `paper_f_analyze.py`. (a) `bootstrap_interval` leaves out the pairs formed
by a dataset drawn twice, which would otherwise count as perfect agreement; the paper
says "percentile bootstrap interval over datasets". (b) `_interaction_p` removes the
method means and the method-by-classifier means before permuting; the paper says only
that method labels are permuted inside blocks. (c) The identity with Kendall's W holds
with the correction for ties; one tie exists (sparsity, Phoneme: 0.7894 with it, 0.7837
without). All three choices are sound; none is described.
**Fix**: half a sentence for each of (a) and (b). (c) needs no change unless the editor
wants the word "tie-corrected".

### F07 [minor] — D6 / D3

**Where**: Statistical analysis ("the 16 datasets are the only independent units of the
design"); Sources of error.
**Evidence**: JM1, KC1, PC3 and PC4 are one family. The bootstrap and the permutation
test treat the sixteen as independent. The paper discloses the family and, for the
faithfulness gap, that the four agree more with each other than the other pairs do. It
reports no analysis with the family counted once.
**Fix**: the author's decision. A check with one defect dataset in place of four (13
datasets) would be a post hoc analysis and must be labelled as such; the alternative is
to leave the disclosure as it is. See the questions.

### F08 [minor] — D1

**Where**: Introduction ("yield unreliable rankings"); Related work and Discussion (the
image study whose metric results "did not necessarily hold on others").
**Evidence**: `ACTIVE_CONTEXT.md` records that the references added on 2026-10-11 were
checked on their records and abstracts, not on full texts. The Discussion now builds a
contrast on one of them. The sentence "Comparative studies, which score the methods on
properties such as faithfulness, stability, sparsity and cost, are therefore the usual
guide to a choice" still has no citation (noted in the handoff of 2026-10-11).
**Fix**: read the two papers before submission; cite or soften the uncited sentence.

### F09 [suggestion] — wording

"1,326 of DiCE, 99 of Anchors, 0 of LIME and 0 of SHAP" and "The decision differs from
the one above for zero of the four measures" are correct and read as machine output.
Dataset names in the Results are OpenML identifiers ("Amazon_employee_access",
"ozone-level-8hr", "qsar-biodeg").

## Dimension rationale

- **D1 = 4.** Evidence is of the right type for the claims: a permutation test for
  "more than chance", an interval for strength, counts for the descriptive statements.
  F05 and F08 are the gaps.
- **D2 = 5.** One hypothesis per measure with a decision rule fixed in advance; a p of
  0.05 or more would have refuted it, and the rule separates three strengths.
- **D3 = 3.5.** Scope is stated (binary tabular tasks, one repository, one
  configuration). F01 generalises beyond the paper's own counts and F04 attributes to
  the methods what belongs to methods and settings.
- **D4 = 3.** F01 is an internal contradiction between a conclusion and the rankings the
  paper prints. Numbers agree between abstract, text and tables.
- **D5' = 3.5.** Failures, the post hoc comparison and the weaker outcome are disclosed.
  F02 and F03 are omissions at the place where the claim is made.
- **D6 = 4.5.** Unit of analysis, test, multiplicity control and the reference between
  seeds are appropriate and correctly described, apart from F06 and F07.

## Readiness assessment

Ready for submission after F01, F02 and F03 are fixed in the text; none of them changes
a number of the primary analysis or a decision of the rule. F04 to F06 are short edits.
F07 and F08 need the author.

## Questions for the author

1. F07: run the primary analysis once more with one software-defect dataset in place of
   four, labelled post hoc, or leave the disclosure as it stands?
2. F05: print the mean number of features each method uses, or keep the sentence
   qualitative?
3. F08: have the two cited papers been read in full?

## Editor's disposition (2026-10-12, same session, at the author's instruction)

| Finding | Action |
|---|---|
| F01 | Fixed in the abstract, the Discussion and Conclusion 2 |
| F02 | Fixed: a sentence in the last section names the two departures |
| F03 | Fixed: three decimals for the agreement between seeds, table and text |
| F04 | Fixed: "as configured here"; the random search of DiCE is named |
| F05 | Softened to "may reflect"; printing the means is left to the author |
| F06 | Fixed: (a) and (b) described |
| F07 | Closed on the author's decision of 2026-10-12: the check was run (scripts/paper_f_posthoc_family.py, logged in the plan before it was run). With one software-defect dataset in place of four, for each of the four, the agreement is 0.64 to 0.67 (faithfulness gap), 0.85 to 0.88 (stability), 0.76 to 0.77 (sparsity) and 0.86 to 0.87 (cost); the decision of the rule is unchanged in 16 of 16 cases. Reported in the Results, labelled as made after the results |
| F08 | Open, question 3 |
| F09 | The two sentences reworded; dataset names left as they are |
