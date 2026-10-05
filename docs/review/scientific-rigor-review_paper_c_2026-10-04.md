# Scientific Rigor Review: Paper C, first draft

**Date**: 2026-10-04 | **Reviewer role**: Scientific Advisor (read-only) | **Grade**: Major revision
**Mean score**: 3.1 | **Dimensions**: D1=2.5 D2=3.5 D3=3 D4=3.5 D5'=3.5 D6=2.5

**Question from the author**: is this study enough to stand alone?

**Scope reviewed**: `docs/reports/paper_c/paper_c.tex` at commit `c42ab9f7d` (generated source;
line numbers refer to it), `paper_c_template.tex`, `PLAN.md`, `references.bib` (key audit
only), `results/*.csv`, `scripts/paper_c_posthoc.py`, `scripts/paper_c_summary.py`,
`scripts/build_paper_c.py`; `experiments/exp4_cohort2/` (case inventory, all 576 rendered
prompts, the 5,180 parsed scores and rationales); `outputs/analysis/exp4_cohort2/*.csv`;
`outputs/analysis/exp4_llm_evaluation/icc_analysis.csv` and `krippendorff_alpha.csv`;
`src/evaluation/exp4_reliability_metrics.py`; the three prompt templates; ADR-0017 and
ADR-0022.
**Prior review**: none of this manuscript. The assessment
`paper-c-resurrection-assessment_2026-10-04.md` judged viability before a draft existed; its
limits F05.1 to F05.5 are all stated in the draft.
**Regression guards**: no Paper C file is under an RCA path guard yet. RCA-002 binds the EXP4
aggregates and the ICC(1,1) wording; both are respected. `python scripts/pubs/verify_claims.py`:
"OK: 985 claims re-derived from artifacts, 1297 manuscript sites checked, 60 retired-value
guards clear, 13 cited artifacts present, 28 file(s) fully registered, 21 file(s) clear of
unpublished results". **None of those claims is a Paper C site**: `paper_c.tex` is not under
`[coverage]` (F12).
**Not read**: the full texts of the cited papers; the Word files (the PDF and the `.tex` were
read); the raw responses of the first panel, which do not exist.

**Independence.** This review was written in the session that drafted the manuscript. It is
not an independent review. A second reader who did not write the draft is still needed.

**Evidence labels.** *Re-derived* = recomputed by me from the stored scores or tables.
*Probe* = a calculation run for this review from the stored scores (scripts in the session
scratch folder, nothing written to the repository). A probe shows a problem and its size; it
is not a result fit to publish until it is planned, dated and run in the lane. *Code* = read
in the code. *Record* = stated in a project document.

## One-line summary

The study can stand alone, but not as drafted: its headline coefficient mostly measures
whether the judges agree on which **explainer** they prefer, not on which **explanation** is
better, and what the judges rated was a feature-weight rendering with the technical metrics
attached, which for Anchors and DiCE is not the explanation those methods produce.

## Answer to the author's question

**Yes, conditionally.** The material is enough for one paper with one question. It is not
enough for the paper the present title and abstract describe.

| What the draft has | Verdict |
|---|---|
| Two panels of three judges on the same 192 cases, 5,184 calls, three prompt conditions, three replicates, raw responses kept | Enough data for a reliability paper. This is more than most LLM-judge reports give |
| One coefficient per dimension on the pooled sample | Not enough: it does not separate agreement on the method from agreement on the case (F01) |
| "Quality of explanations" as the object | Not supported: the object is a serialised record with metrics (F02, F04) |
| Human reference | Absent. The paper can stand without it as a reliability study if the title and claims stay there |

Three levels, in order of cost:

1. **Minimum to submit honestly (no new data, about two days).** Report agreement within
   explainer, single-call and panel-mean coefficients, and raw agreement; describe the
   rendering with examples; rewrite the abstract and conclusions around what those show
   (F01, F02, F03, F06).
2. **Strongly recommended (576 calls, a few dollars, one day).** A condition without
   metrics, quadrant and label (PLAN.md 14.4), and, if Anchors and DiCE are to stay, their
   explanations rendered as a rule and as a counterfactual (F02, F04).
3. **Desirable, not required for a reliability paper.** The 56-case human subset.

With level 1 the paper is defensible and its finding is sharper than the present one. With
level 2 it is a solid paper. Submitting the draft as it is would expose it to a referee who
computes the within-explainer coefficient, as I did in ten minutes.

## Strengths

- Every number I recomputed matches the draft (list under "Verified, no finding").
- The negative result is tested on a second panel, and the draft reports that the margin
  does not replicate instead of hiding it.
- The two prompt defects found on 2026-10-04 (the quadrant reveals the label; the metrics are
  printed) are stated in the methods, the results and the limitations, and the claim about
  label bias was withdrawn.
- The pooling effect is identified and explained; most LLM-judge reports average silently.
- The post hoc analysis was fixed and dated before it was run, and is labelled as such.
- The limitations paragraph names the judge tier, the lost first panel, the unbalanced
  inventory and the floor effect.

## Findings

### F01 [major] — D1 / D6. The pooled ICC measures agreement on the explainer, not on the explanation

- **Where**: lines 70, 270 ("No dimension reached 0.75 in either panel"), Table 1, Figure 1,
  line 468.
- **Evidence** (*probe*, primary condition, replicates averaged):
  - Share of the variance of the case-level mean score that lies between explainers: overall
    quality 0.64, completeness 0.67, concision 0.65, audit usefulness 0.63, semantic
    plausibility 0.43, clarity 0.36, actionability 0.07.
  - ICC(1,1) computed inside each explainer:

    | Explainer (cases) | Completeness | Sem. plausibility | Overall | Audit usefulness | Concision |
    |---|---|---|---|---|---|
    | SHAP (52) | 0.06 | 0.19 | -0.19 | 0.15 | -0.24 |
    | Anchors (76) | 0.17 | 0.38 | 0.46 | 0.12 | -0.20 |
    | DiCE (32) | -0.04 | 0.12 | 0.28 | 0.24 | -0.01 |
    | LIME (32) | 0.71 | 0.69 | 0.63 | 0.75 | 0.69 |

  - Pooled values in the draft for the same dimensions: 0.731, 0.604, 0.660, 0.699, 0.373.
- **Reasoning**: an ICC is the share of score variance that is between cases. When the cases
  come from four methods whose renderings differ visibly, the judges agree that SHAP records
  score higher than Anchors or DiCE records, and that agreement fills the coefficient. Inside
  SHAP, the largest group with real attributions, three judges do not agree at all on which
  explanation is more complete or better overall.
- **Consequence**: the headline understates the problem and misnames it. "Close to the
  threshold" (0.73) is the method-level reading; at the level a user of a judge cares about,
  ranking explanations of one method, agreement is near zero for three of four explainers.
  The comparison between panels (line 308) may also reflect how each panel separates the
  explainers. The first panel cannot be decomposed: only its aggregates exist.
- **Fix**: add the within-explainer coefficients (dated in PLAN.md before they are run in the
  lane), report the between-explainer share, and state the finding in the abstract: the
  judges agree on the method more than on the instance. Explain why LIME differs (its cases
  are all Adult, and its fidelity and sparsity vary visibly in the record) or say that it is
  not explained.

### F02 [major] — D1 / D3. For Anchors and DiCE the judges did not see the explanation the method produces

- **Where**: line 195 ("the explanation in the normalised text form of the benchmark"); the
  title and abstract ("quality of explanations").
- **Evidence** (*re-derived* from `exp4_cases.jsonl`): every explanation is rendered by one
  template, "top local factors: feature: weight; ...", with ten items.
  - Anchors: `ANCHORS top local factors: education-num: 1.0000; capital-gain: 1.0000;
    hours-per-week: 1.0000; age: 0.0000; fnlwgt: 0.0000; ...`. An anchor is a rule with a
    precision and a coverage; here it is a 0/1 list without thresholds. Median of 7 items
    with weight zero; 69 distinct texts in 76 cases.
  - DiCE: `DICE top local factors: age: 1.6182; education_9th: 0.4000; fnlwgt: 0.0000; ...`.
    A counterfactual is a changed instance with a new outcome; here it is a list of
    magnitudes without direction, target value or outcome. Median of 8 zero items.
  - `prediction_confidence` is empty in all 192 records, while the prompt says the record
    states "the model's prediction and confidence".
- **Reasoning**: 108 of the 192 cases (56%) are Anchors or DiCE. Their low scores, the 86% of
  actionability scores equal to 1, and a large part of the between-explainer variance of F01
  can come from the rendering. DiCE is the method built for actionability, and its recourse
  content was removed before the judges saw it.
- **Consequence**: the paper cannot say what the judges think of Anchors or DiCE
  explanations, and the floor effect is at least partly an artefact. The object of the study
  is "explanations as serialised by the benchmark", which the draft does not say.
- **Fix**: show one rendered example per explainer in the methods; limit the claims to the
  rendered records; attribute the actionability floor to the rendering as a candidate cause.
  Better: report SHAP and LIME (84 cases, real attributions) as the main analysis and the
  other two as a stated limitation, or re-render Anchors and DiCE in the clean condition.

### F03 [major] — D4 / D6. The primary coefficient is not single-call, and the panel mean is not reported

- **Where**: line 69 ("single-rater intraclass correlation"), line 244 ("with the three
  replicates of a judge averaged per case"), line 447 ("should report the reliability of a
  single call"), line 79 and line 468.
- **Evidence** (*probe*, primary condition):

  | Dimension | ICC(1,1), 3 replicates averaged (draft) | ICC(1,1), one call | ICC(1,k), mean of 3 judges |
  |---|---|---|---|
  | Completeness | 0.731 | 0.675 | 0.891 |
  | Audit usefulness | 0.699 | 0.656 | 0.875 |
  | Overall quality | 0.660 | 0.626 | 0.853 |
  | Semantic plausibility | 0.604 | 0.557 | 0.821 |
  | Concision | 0.373 | 0.325 | 0.641 |

- **Reasoning**: the draft criticises averaging over nine scores for raising the coefficient,
  and its own primary estimate averages three. It recommends reporting single-call
  reliability and does not report it. In the other direction, the reliability of the mean of
  the three judges, which is how a panel is used, exceeds 0.75 on four dimensions by the
  draft's own threshold.
- **Consequence**: "Three LLM judges did not agree well enough ... to be used as a
  confirmatory measure" (line 468) does not follow. What follows is that one judge is not
  enough. The abstract's last sentence says "a single LLM judge" and is correct; the
  conclusions and the discussion are broader than the evidence. All of this is subject to
  F01: the panel-mean values are also pooled over explainers.
- **Fix**: report the three columns above; call the primary estimate what it is; make the
  conclusion about a single judge, and say that a panel mean is reliable for separating
  methods and unverified for separating instances.

### F04 [major] — D1 / D3. The judges read the metrics, to different degrees, and this is measurable

- **Where**: lines 395 to 411 and the fourth paragraph of the discussion.
- **Evidence** (*probe*, rationale text of the primary condition): a metric name (fidelity,
  stability, sparsity, faithfulness) appears in the rationales of 80% of the responses of
  Claude Haiku 4.5, 40% of GPT-5.4 mini and 15% of Gemini 3.8 Flash. In the rationale for
  overall quality alone: 73%, 32% and 8%.
- **Reasoning**: the draft infers from a correlation that the scores follow the printed
  fidelity. The rationales show it directly, and they show that the three judges use the
  metrics unequally. That is a source of disagreement the draft does not name, and it means
  the scores are not a semantic reading of the explanation.
- **Also** (*probe*): inside explainer-by-dataset cells the fidelity correlation is absent
  on Breast Cancer (Anchors -0.09, SHAP +0.11) and strong elsewhere (0.51 to 0.72). "Within
  every explainer" (line 77) is true and hides this.
- **Fix**: report the share of rationales that cite a metric, per judge, as a planned
  addition; state the dataset heterogeneity. The clean condition is the only repair of the
  design; without it the title should not say "quality of explanations" without
  qualification.

### F05 [major] — D3. Differences between the panels cannot be attributed to the panel

- **Where**: line 308 ("The order of the dimensions was not the same in the two panels"),
  line 437 ("Agreement is a property of a panel and a rubric together").
- **Evidence** (*record*): the panels differ in the models, in the templates (rebuilt for the
  second), in the output limit (512 against 4,000 tokens), in the cases used for the ICC (147
  complete against 192) and possibly in the condition and aggregation, which are unknown for
  the first (line 242). Which 45 cases were incomplete in the first panel is not known.
- **Consequence**: "changes with the panel" is one of five confounded explanations. The
  rubric claim is supported inside the second panel; the panel claim is not separable.
- **Fix**: say "between the two runs" and list the differences where the comparison is made,
  not only in the limitations.

### F06 [minor] — D6. Raw agreement and the restricted range are reported for one dimension only

- **Evidence** (*probe*, primary condition, one call): overall quality takes the value 2 in
  59% of the scores and never 5; pairs of judges give the same score in 71% of the cases and
  differ by at most one point in 99%. Completeness: 72% and 99%. Concision: 35% and 78%.
- **Reasoning**: a low ICC with high raw agreement is the usual effect of a narrow range. The
  draft explains it for actionability only (line 313). A reader will otherwise take 0.66 as
  "the judges often disagree", which is not what happened.
- **Fix**: add exact and within-one agreement to Table 1 or to the text.

### F07 [minor] — D6. The confidence interval is not the interval of an ICC

- **Where**: line 236 ("a 95% confidence interval from Fisher's transformation").
- **Evidence** (*code*; *probe*): the code applies Fisher's z with standard error
  1/sqrt(n-3), which is the interval of a Pearson correlation. The exact F-based interval of
  ICC(1,1) is narrower: completeness 0.674 to 0.782 (draft 0.657 to 0.791), audit usefulness
  0.637 to 0.755 (draft 0.619 to 0.765).
- **Consequence**: the statement that two upper bounds exceed 0.75 survives, for audit
  usefulness by 0.005. The method as described is not the standard one.
- **Fix**: report the F-based interval in the paper (computed in the lane; the registered
  values of the earlier documents do not change), or keep the present one and name it an
  approximation.

### F08 [minor] — D6. The one-way model is stated, not justified, and the alternative changes two cells

- **Evidence** (*probe*): ICC(2,1), absolute agreement, is within 0.01 of ICC(1,1) on five
  dimensions (0.733, 0.613, 0.667, 0.702; concision 0.431 against 0.373). ICC(3,1),
  consistency, gives completeness 0.750 and concision 0.596.
- **Reasoning**: the same three judges scored every case, which is the crossed design of the
  two-way models; ICC(1,1) is the model for raters that differ by case. The conclusion holds
  under absolute agreement. Under consistency completeness sits on the threshold, so "the
  threshold was crossed only under an alternative rubric wording or when replicates and
  conditions were averaged" (line 74) is true for one coefficient only.
- **Fix**: one sentence with the two-way values as a sensitivity analysis; drop "only".

### F09 [minor] — D6. Two of the post hoc correlations rest on almost no variation

- **Evidence** (*re-derived*): LIME sparsity has four distinct values and 24 of 32 cases
  share one; DiCE sparsity has two values. The LIME sparsity correlation (0.73, starred in
  Table 4) rests on eight cases that differ. Runtime and cost are the same column.
- **Fix**: note the ties under Table 4 or leave the cell without a test, as the plan allows
  for cells without variation.

### F10 [minor] — D4. Three sentences say more than their numbers

- Line 76: "returned the same score in 33% to 99% of the cases, depending on the judge". The
  range is over judges and dimensions.
- Line 324: "Stating the label left agreement almost unchanged". True, but since both
  conditions reveal the label the sentence carries no information; the caveat comes four
  sentences later.
- A better test exists and is not used (*probe*): in the primary condition the mean overall
  score is 2.32 for correct predictions and 2.29 for wrong ones (difference 0.03, p = 0.70),
  and GPT-5.4 mini mentions the outcome in 24% of its rationales. The label is available to
  the judges and does not move the score.

### F11 [minor] — D1. The background does not position the paper in the LLM-judge literature

- **Evidence**: 25 references, 4 on LLM judges, one of them a survey. The corpus section
  (line 146) describes 44 papers on the evaluation of explanations, of which 4 concern LLM
  judges.
- **Reasoning**: a referee of a standalone LLM-judge reliability paper will ask what is known
  about the reliability, self-consistency and prompt sensitivity of LLM evaluators outside
  XAI. The draft does not say, so its novelty is asserted by absence. The corpus adds little
  to this paper: half a page for one number (4 of 44).
- **Fix**: a targeted search on LLM-judge reliability (author task; I did not verify what
  exists and name no paper). Cut the corpus paragraph to three sentences and use the space
  for F01 and F03.

### F12 [minor] — RCA-001. No number of the draft is registered

- **Evidence**: `paper_c.tex` is not under `[coverage]` or `[exclusivity]`; `verify_sync.py`
  does not check it; `pub/claims.toml` holds a placeholder abstract.
- **Invariant**: "Every published number is registered in pub/claim_registry.toml with the
  resolver that re-derives it". The build generates every number from a result file, which
  removes typing errors; it does not give the cross-document checks.
- **Fix**: the registry work of PLAN.md section 9, before submission.

### F13 [suggestion]. Cases are not all independent

192 cases come from 174 distinct dataset-instance pairs (*re-derived*). The dependence is
small; say it in the methods.

### F14 [suggestion]. State the decision rule before the results

The 0.75 threshold is applied to point estimates in some sentences and to upper bounds in
others. State once, in the methods, which is used for the conclusion.

## Verified, no finding

*Re-derived* from the stored scores or tables and equal to the draft: the seven ICC(1,1) and
alpha values of the primary condition; the three other views of Table 2; the test-retest
shares of Table 3; the largest mean shifts (0.14 and 0.50); 86% of actionability scores equal
to 1; the clarity offset (SD 0.38, 0.64 points); the case counts by dataset, explainer and
outcome; 5,184 calls and 5,180 parsed; the 20 correlations of Table 4 and their Holm
adjustment; the corpus counts and the four audit agreement shares. The first-panel values
equal the committed aggregates. Abstract 244 words, resumen 248. The blind PDF and Word file
contain no author identity apart from the citation of the RIMI article.

## Dimension rationale

- **D1 Evidence relevance, 2.5.** The central coefficient does not measure what the claim
  says (F01), and the object rated is not the explanation for more than half the cases (F02).
- **D2 Falsifiability, 3.5.** Four clear questions and a stated threshold; the decision rule
  moves between point estimate and bound (F14).
- **D3 Scope calibration, 3.** Judge tier and datasets are limited correctly; "quality of
  explanations" and "changes with the panel" exceed the design (F02, F04, F05).
- **D4 Argument coherence, 3.5.** The draft criticises averaging and averages; recommends
  single-call reporting and omits it (F03, F10).
- **D5' Reporting honesty, 3.5.** Good on the prompt defects, the lost panel and the post hoc
  status. The rendering of Anchors and DiCE is not disclosed (F02).
- **D6 Methodological rigor, 2.5.** No stratified coefficient, interval of the wrong
  statistic, model not justified, raw agreement missing (F01, F03, F06, F07, F08).

## Readiness assessment

Not ready to submit. No finding needs the first panel, a human rater or a new judge run to be
answered at the minimum level; F01, F03, F06, F07, F08, F09 and F10 are analyses of files
already committed and text changes. F02 and F04 are answered fully only by a new condition.

The revised paper would say something more useful than the draft: small LLM judges agree on
which explanation method they prefer and on little else; inside one method their agreement is
near zero except where the record varies visibly; a panel mean is reliable for the first
purpose and unverified for the second; and the scores of at least one judge are largely a
reading of the metrics it was shown.

Outside the science, and unchanged from the plan: the deadline is 2026-10-15; Paper D is in
the same special issue; the reliability tables are public in the 32-page edition and the
thesis; the review above is not independent.

## Questions for the author

1. Should Anchors and DiCE stay in the main analysis as rendered, move to a limitation, or be
   re-rendered and re-judged?
2. Is the clean condition (PLAN.md 14.4) approved? It decides whether F02 and F04 are
   repaired or only disclosed.
3. Is the within-explainer analysis accepted as a dated post hoc addition to the plan?
4. Is the corpus paragraph kept at its present length, given F11?
5. If the deadline cannot hold a new condition, is a later venue preferable to submitting the
   minimum version on 2026-10-15?
