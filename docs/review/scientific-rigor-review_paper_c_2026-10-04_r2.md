# Scientific Rigor Review: Paper C, revised draft (second review)

**Date**: 2026-10-04 | **Reviewer role**: Scientific Advisor (read-only) | **Grade**: Major revision (small: two analyses of committed files, then wording)
**Mean score**: 3.5 | **Dimensions**: D1=3 D2=4 D3=3.5 D4=3.5 D5'=4 D6=3

**Scope reviewed**: `docs/reports/paper_c/paper_c.tex` as on `main` at `08ef806f8` (generated
source; line numbers refer to it), `paper_c_template.tex` (placeholders of the abstract and
Table 1), `references.bib`, `README.md`, `results/review_summary.csv`,
`results/clean_fidelity.csv`, `results/judge_behaviour.csv`,
`scripts/paper_c_reliability.py`; `experiments/exp4_cohort2/cases/exp4_cases.jsonl` (192
records), `experiments/exp4_cohort2/parsed_scores/exp4_llm_scores.csv` (5,180 rows),
`clean_condition/parsed_scores/clean_llm_scores.csv` (576 rows);
`outputs/analysis/exp4_cohort2/icc_analysis.csv` and `krippendorff_alpha.csv`.
**Prior review**: `scientific-rigor-review_paper_c_2026-10-04.md` (F01 to F14). Status of
each finding is in the table below.
**Regression guards**: no Paper C file is under an RCA path guard. RCA-002 (ICC named as
ICC(1,1); a new judge run is a new cohort in its own directory) is respected.
`python scripts/pubs/verify_claims.py`: "OK: 985 claims re-derived from artifacts, 1297
manuscript sites checked, 60 retired-value guards clear, 13 cited artifacts present, 28
file(s) fully registered, 21 file(s) clear of unpublished results". None of these is a Paper
C site (F12, carried).
**Not read**: the Word and PDF files (the `.tex` was read); `PLAN.md`; the rendered prompts;
the raw responses; the full texts of the cited papers. The Krippendorff differences, the
test-retest shares, Table 3 and Table 4 were not recomputed.

**Independence.** This review was written by a session that did not write the draft or the
first review. It read the first review before the probes, so it is independent of the
drafting, not blind to the earlier findings. It is still a review by an AI session; it does
not replace a human reader.

**Evidence labels.** *Re-derived* = recomputed here from the stored scores with code written
for this review, not with the lane's scripts. *Probe* = a new calculation from the stored
scores, run for this review and written nowhere in the repository. A probe shows a problem
and its size. It is not a result to print until it is planned, dated and run in the lane.

## One-line summary

The revision answers the first review and its numbers reproduce, but its two findings about
single methods need restating: the agreement among LIME explanations comes from five records
whose ten weights are all zero, and the near-zero coefficients among SHAP explanations go
with judges that gave almost every SHAP explanation the same score.

## Strengths

- Every value recomputed here equals the draft: the seven ICC(1,1) of the primary condition
  with three calls and with one call, their F-based intervals, the 28 within-explainer
  coefficients of Table 2, the 42 cells of Table 5, the ICC(1,k) column, the shares of
  variance between explainers, the shares of rationales naming a metric (80%, 36%, 13%),
  the shifts of the clean condition (0.30, 0.52, 0.01, 0.01), the eight fidelity
  correlations of section 3.5, the case counts by explainer and the 174 distinct instances.
- The decomposition by explainer is the right analysis, and the draft is organised around it.
- The clean condition is a real repair of the design defect, and it is specified as a new
  cohort.
- The two effects of the clean condition that the paper leans on are robust (*probe*,
  bootstrap over cases, 4,000 resamples): the fall of agreement on audit usefulness, -0.23
  (95% interval -0.32 to -0.15), and the loss of the fidelity correlation for SHAP (change
  -0.81 to -0.23) and for DiCE (-0.87 to -0.11). The rise of the Claude Haiku 4.5 scores
  (0.30 for overall quality) is far above the difference between two calls of the same
  prompt (0.01).
- The limitations are stated where the claims are made.

## Status of the first review

| Finding | Status |
|---|---|
| F01 pooled ICC | Fixed. See N01 and N02 for what the within-explainer values mean |
| F02 rendering of Anchors and DiCE | Disclosed with examples; not repaired (author decision) |
| F03 unit of the estimate | Fixed; N04 is a labelling point |
| F04 metrics in the prompt | Fixed by the clean condition |
| F05 panels confounded | Fixed |
| F06 raw agreement | Fixed for all cases; **reopened inside the explainers** (N02) |
| F07 interval | Fixed; intervals re-derived |
| F08 model | Fixed for all cases; **reopened inside the explainers** (N03) |
| F09, F10, F13, F14 | Fixed |
| F11 literature | Carried: four works on LLM judges |
| F12 registry | Carried: no Paper C number is registered |

## Findings

### N01 [major] — D1 / D3. The agreement among LIME explanations comes from five records with all weights zero

- **Where**: line 76 ("among the LIME cases five dimensions stayed above 0.6"), lines 340 to
  342, Table 2 column LIME, Table 5 columns LIME, lines 503 to 509, lines 541 to 543 ("LIME
  is the exception, and it is not explained by the metrics; its cases come from one dataset,
  and why its explanations draw agreement is not established here"), and the same sentence
  of the resumen.
- **Evidence** (*re-derived* from `exp4_cases.jsonl`): in 5 of the 32 LIME records every one
  of the ten weights is printed as 0.0000 or -0.0000, for example "native-country_India:
  -0.0000; occupation_Tech-support: -0.0000; ...". (*Probe*): the three judges gave each of
  these five records the score 1 for overall quality and for completeness in every call.
  The other 27 LIME records have a mean overall-quality score of 2.51 with a standard
  deviation of 0.31.
- ICC(1,1) among the LIME cases (*probe*; completeness, semantic plausibility, overall
  quality, audit usefulness, concision):

  | Cases | Primary, three calls | Primary, one call | Clean |
  |---|---|---|---|
  | All 32 (as in the draft) | 0.71, 0.69, 0.63, 0.75, 0.69 | 0.61, 0.68, 0.61, 0.68, 0.68 | 0.63, 0.69, 0.64, 0.66, 0.52 |
  | The 27 with a non-zero weight | 0.29, 0.14, 0.07, 0.33, -0.13 | 0.13, 0.16, 0.11, 0.29, -0.14 | -0.05, 0.13, 0.02, -0.18, -0.21 |

- **Reasoning**: an ICC is high when the cases differ and the judges agree on the
  difference. Here the difference is between a list of zeros and a list of numbers. Among
  the LIME explanations that say something, the three judges agree as little as among the
  SHAP explanations.
- **Consequence**: the "exception" is explained, and the explanation removes it. The
  sentence that the cause "is not established here" can be replaced by the cause. The
  abstract's contrast between SHAP and LIME does not stand as written. The paper's main
  message becomes simpler and stronger: inside every explainer, agreement on which
  explanation is better was low; what the judges agreed on was the method and the empty
  explanation. The sentence at line 492 ("for LIME and Anchors something visible in the
  rendered explanation goes with fidelity") can also be made concrete for LIME: among its
  cases fidelity rises with the size of the printed weights (Spearman 0.55) and the
  overall-quality score rises with the largest weight (0.78 primary, 0.75 clean).
- **Fix**: add to `PLAN.md` a dated analysis (LIME with and without the records whose
  weights are all zero), run it in the lane, and report both rows. Rewrite the LIME
  sentences of the abstract, resumen, results, discussion and conclusions. Say in the
  methods how many records have no non-zero weight. Check the same for the other explainers
  (none of the SHAP records has a zero weight; Anchors and DiCE are covered by the rendering
  caveat). No new judge call is needed.

### N02 [major] — D1 / D6. Among SHAP explanations the judges gave almost the same score to every case, and the draft reads the low coefficient as disagreement

- **Where**: lines 337 to 340 ("the three judges did not agree on which SHAP explanation was
  better"), lines 540 to 541 ("the agreement of three judges was near zero"), line 583
  ("among SHAP explanations agreement was near zero on every dimension").
- **Evidence** (*probe*, SHAP cases, primary condition):
  - Standard deviation of the case-level mean score: completeness 0.15, overall quality
    0.21, concision 0.18, audit usefulness 0.30. Among LIME cases: 0.69, 0.62, 0.79, 0.81.
  - Share of pairs of judges with the same score, one call: completeness 83% (within one
    point 100%), overall quality 54% (97%), audit usefulness 56% (100%), concision 45%
    (100%). For completeness the three judges gave the same score in 75% of the SHAP cases.
  - In the clean condition one judge gave completeness 3 to all 52 SHAP cases.
- **Reasoning**: this is the argument the draft makes for actionability at lines 322 to 325
  ("the judges almost always agreed and the coefficient, which needs differences between
  cases, is near zero"), and it applies to the SHAP result, which is now the headline. A
  coefficient near zero with scores that hardly vary does not show that the judges disagree
  about which SHAP explanation is better. It shows that they did not separate the SHAP
  explanations at all, and that what little they separated they did not separate alike.
  Whether the 52 explanations differ in quality is not known without a reference.
- **Consequence**: the practical conclusion survives and can be said more exactly: a judge
  of this class did not tell one SHAP explanation from another. "Did not agree on which was
  better" and "agreement was near zero" say more than the data show.
- **Fix**: report the spread of the scores and the raw agreement inside SHAP and LIME beside
  the coefficients (they are already in `reliability_long.csv` for one call), and reword the
  three sentences. In the limitations, say that low variance among the cases of a method and
  disagreement among the judges are not separated by the ICC.

### N03 [minor] — D6. Inside SHAP the one-way coefficient is pulled down by constant differences between judges

- **Where**: line 76 and line 338 ("no dimension exceeded 0.19"), the coefficient of overall
  quality ($-$0.19).
- **Evidence** (*probe*, SHAP cases, three calls averaged): the mean overall-quality scores
  of the three judges are 2.67, 2.92 and 3.40. ICC(3,1), consistency: semantic plausibility
  0.45, audit usefulness 0.24, clarity 0.16, overall quality 0.05. ICC(2,1): 0.29, 0.20,
  0.05, 0.03. The interval of the one-way value of overall quality lies below zero (-0.29 to
  -0.05), which a one-way model produces when judges differ by a constant.
- **Consequence**: "no dimension exceeded 0.19" is true for ICC(1,1) only. No value is near
  0.75 under any model, so the conclusion holds. The draft gives the two-way check for all
  cases (lines 311 to 316) and not where it changes a number the abstract prints.
- **Fix**: one clause: under consistency the highest value among the SHAP cases was 0.45.

### N04 [minor] — D4. Three numbers of the abstract and Table 1 are not labelled as what they are

- Line 76 and line 102: "no dimension exceeded 0.19, with or without the metrics". The
  value without the metrics is 0.198, printed as 0.20 at line 504; with one call of the
  primary condition it is 0.22 (Table 5, audit usefulness). Print the largest of the values
  the sentence covers.
- Table 1, column ICC(1,$k$): the values (0.862 for completeness) are computed from one
  call per judge. From three calls averaged the value is 0.891. The caption does not say
  which; the count of "four dimensions" at line 311 is the same either way.
- "One call" is the first of the three calls. The other two give 0.698 and 0.665 for
  completeness and 0.569 and 0.597 for overall quality (*probe*). State that the first call
  is used.

### N05 [minor] — D6. The changes of the clean condition are given without an interval, and one is inside the noise

- **Where**: lines 495 to 500.
- **Evidence** (*probe*, bootstrap over cases): audit usefulness -0.23 (-0.32 to -0.15);
  completeness -0.10 (-0.17 to -0.03); overall quality -0.06 (-0.14 to +0.02). The three
  calls of the primary condition give 0.626, 0.569 and 0.597 for overall quality, so 0.57
  in the clean condition is inside the range of the primary condition itself.
- **Fix**: drop overall quality from the list of falls, or give the intervals. The headline
  (audit usefulness) is safe.
- **Also**: the cells of Table 5 inside SHAP move between calls by as much as they move
  between conditions (audit usefulness inside SHAP: 0.22, -0.04 and 0.12 in the three
  calls). The text does not interpret single cells; the caption could say so.

### N06 [minor] — D3. The clean condition removes three things, and the abstract names one

- **Where**: line 81 ("Without them that judge scored higher"), line 22 of the README.
- **Evidence**: the clean record has no metrics, no outcome of the prediction and no label
  (line 221). The body says so each time; the abstract and the first sentence of the
  discussion's fourth paragraph attribute the change to the metrics.
- **Reasoning**: the attribution is plausible, since the judge that changed is the one that
  named a metric in 80% of its responses, and correct and wrong predictions received the
  same score. It is still an inference.
- **Fix**: "without the metrics and the outcome" once in the abstract, or a clause in the
  limitations.

### N07 [minor] — D3. The share of variance "between explainers" is also between datasets and model families

- **Evidence** (*re-derived*): 45 of the 52 SHAP cases are from Breast Cancer or German
  Credit and 45 are from tree models; all LIME and DiCE cases are from Adult, on logistic
  regression and the perceptron. (*Probe*): with the dataset held fixed, among the 96 Adult
  cases, the share between explainers is 40% for completeness and 38% for overall quality
  (67% and 64% over all cases), with 7 SHAP cases.
- **Consequence**: the reading that the judges separate methods holds inside one dataset,
  smaller. The draft says the inventory is unbalanced (line 572) and does not connect it to
  the 67%.
- **Fix**: one clause where the 67% is given, or in the limitations.

### N08 [suggestion]. Agreement among Anchors cases is on Adult only

(*Probe*) ICC(1,1) of overall quality among Anchors cases: Adult 0.58 (25 cases), German
Credit 0.36 (29), Breast Cancer 0.01 (22). Not needed in the paper; it bears on any later
claim about datasets.

### N09 [carried, F11]. Four works on LLM judges

Unchanged. A referee of a reliability paper will ask what is known about the consistency of
LLM evaluators and their sensitivity to the prompt. See the literature note of the same
date in `docs/reports/paper_c/`.

### N10 [carried, F12]. No number of the draft is registered

Unchanged. RCA-001 invariant: "Every published number is registered in
pub/claim_registry.toml with the resolver that re-derives it". If N01 to N05 change numbers
in the text, the registry work is better done after them.

## Dimension rationale

- **D1 Evidence relevance, 3.** The coefficients are correct. Two of them are read as
  evidence of something they do not show (N01, N02).
- **D2 Falsifiability, 4.** Four questions, a stated threshold and a stated decision rule.
- **D3 Scope calibration, 3.5.** Judge class, datasets and rendering are limited correctly.
  The LIME contrast and the attribution to the metrics go past the design (N01, N06, N07).
- **D4 Argument coherence, 3.5.** The restricted-range argument is made for actionability
  and not for SHAP (N02); three numbers are loosely labelled (N04).
- **D5' Reporting honesty, 4.** Defects, lost material and post hoc status are disclosed.
  The zero-weight LIME records are not, because they were not noticed.
- **D6 Methodological rigor, 3.** Sound over all cases. Inside the explainers the model
  check, the raw agreement and the intervals of the differences are missing (N02, N03, N05).

## Readiness assessment

Not ready to submit as it is; close. No finding needs a judge call, a human rater or a new
dataset. N01 and N02 need a dated addition to the plan, a run of an extended
`paper_c_reliability.py`, and new wording in the abstract, the resumen, sections 3.2 and
3.5, the discussion and the conclusions. N03 to N07 are clauses. The paper is at the page
limit, and the rewording of the LIME passages frees about as much as N01 and N02 add.

The corrected paper says: three small LLM judges agreed on which method they preferred and
on which explanations were empty; among the explanations of one method that carried
content, they did not separate one from another alike, with or without the metrics in the
prompt.

A change to the analysis code or to the result files needs a new Zenodo version.

## Questions for the author

1. Is the analysis of N01 (LIME with and without the all-zero records) accepted as a dated
   addition to the plan?
2. Should the five all-zero LIME records stay among the 192 cases with the finding stated,
   or be reported as a separate group? The recommendation is to keep them and state it:
   they are real outputs of the benchmark.
3. One of the five has a printed fidelity of 0.84 with all weights at zero. Is that a
   rounding of very small weights or a defect of the stored run? It concerns the benchmark,
   not this paper's conclusions.
