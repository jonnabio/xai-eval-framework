# Paper C plan: LLM judges as evaluators of explanations

**Dated:** 2026-10-04. **Status:** approved by the author on 2026-10-04, to be adjusted as
the work goes; every adjustment is dated here. Section 14 records two findings made after the
approval that change claims 3 and section 7.

**Basis:** ADR-0022 and its amendment of 2026-10-04; ADR-0017 (how cohort 2 is reported);
`docs/review/paper-c-resurrection-assessment_2026-10-04.md`; RCA-001 and RCA-002.

## 1. The paper

**Question.** Can LLM judges score post-hoc explanations reliably, and what do their scores
follow?

**Working title.** "Can LLM Judges Score Explanations Reliably? Agreement among Judges, across
Panels and with Human Raters". The last clause stays only if section 6 is completed.

**Claims the existing evidence supports**

1. On 192 explanations, three LLM judges do not reach an ICC(1,1) of 0.75 on any of seven
   rubric dimensions in the label-hidden condition. This holds in two judge panels.
2. The margin and the ranking of dimensions change between panels.
3. Rubric wording moves the scores. The comparison with and without the true label is
   **not** a test of label bias: see section 14.1.
4. Test-retest agreement at temperature 0 differs between judges.
5. Crossing 0.75 depends on the prompt condition and on pooling over replicates.

**Claims that need new work**

- Agreement between judges and people (section 6).
- What judge scores follow among the technical metrics (section 7).

**Not claimed.** Validity of LLM judges in general; any result for larger judge models; a
survey or a validated taxonomy. The taxonomy and the 44-paper corpus are framing, in about
one page.

## 2. Venue

*Tecnología en Marcha*, special issue on Artificial Intelligence, 2027 edition. Read on
2026-10-04 from the call and the instructions page.

| Item | Rule |
|---|---|
| Deadline | **2026-10-15**, by email to revistatm@tec.ac.cr |
| Language | Spanish or English. Planned: English, as Paper D |
| Length | 5 to 15 pages, letter size |
| File | Word, one column, 1.5 line spacing, 12 pt |
| Title, abstract, keywords | In Spanish and English; abstract of at most 250 words each |
| References | IEEE |
| Figures | In the document and as separate files (.jpg, .tiff, .eps), 300 ppi |
| Equations | Word equation editor |
| Authors | Full name, profession, telephone, email, workplace, country, ORCID |
| Review | Double-blind (Paper D README, checked 2026-10-03) |
| Originality | Original, unpublished, not in another process |
| AI policy | Assistance is disclosed |
| Fees | None stated |

At 12 pt and 1.5 spacing, 15 pages hold about 5,000 words with three tables, two figures and
25 references. The 9.5 journal pages of source material do not fit; section 4 sets the budget.

## 3. Evidence and its limits

| Source | Content | Limit |
|---|---|---|
| Original cohort, `outputs/analysis/exp4_llm_evaluation/` | Three judges, seven dimensions, 192 cases, ICC on 147 complete cases | Raw responses and prompt templates lost (RCA-002) |
| Cohort 2, `experiments/exp4_cohort2/`, `outputs/analysis/exp4_cohort2/` | Same 192 cases, a second panel, 3 conditions by 3 replicates, 5,180 of 5,184 responses parsed, raw data kept | A second panel with rebuilt templates; not a reproduction |
| Case records | Technical metrics of each explanation, 192 of 192 complete | Unbalanced inventory (below) |
| Corpus, `paper_c_review_corpus.csv` | 44 coded papers | One coder; audit of 16 papers; 28 disagreements open |

Case inventory by dataset and explainer: Adult has 25 Anchors, 32 DiCE, 32 LIME and 7 SHAP;
Breast Cancer 22 Anchors and 21 SHAP; German Credit 29 Anchors and 24 SHAP. LIME and DiCE
appear on Adult only.

Reporting rules that already bind (ADR-0017): the label-hidden ICC(1,1) is the primary
estimate; pooled and per-condition estimates are sensitivity analyses and are named as such;
147 is the complete-case subset of the original cohort, not the sample; a new judge run is a
new cohort and never overwrites the committed files.

## 4. Structure and page budget (15 Word pages)

| Section | Pages |
|---|---|
| Title, authors, abstract and keywords in two languages | 1.25 |
| Introduction | 1.0 |
| Related work and framing (taxonomy, corpus) | 1.25 |
| Materials and methods (cases, judges, rubric, conditions, statistics, human subset) | 2.5 |
| Results: reliability in two panels | 2.0 |
| Results: label, rubric, test-retest | 1.5 |
| Results: human subset; judge scores and technical metrics | 1.5 |
| Discussion and limitations | 1.5 |
| Conclusions, acknowledgments, data availability | 0.75 |
| References (about 25) | 1.75 |
| **Total** | **15.0** |

Planned floats: three tables (reliability by dimension and cohort; condition effects;
human-judge agreement) and two figures (ICC with intervals by dimension and cohort;
test-retest by judge). The rubric text and the full tables go to the archive, not the paper.

If section 6 is not completed, its half page goes to the discussion.

## 5. Work package A: adjudication of the corpus coding

- File: `corpus_audit/second_reviewer_adjudication_sheet.csv`, 28 disagreements in 12 records;
  the columns `final_labels`, `rule_applied`, `decided_by` and `decided_on` are empty.
- The author and the second reviewer decide each row and record the rule.
- A rule that changes the codebook is applied to the 28 papers outside the audit. The corpus
  file is then updated and its counts recomputed by a script in `scripts/`.
- **Fallback.** If adjudication is not complete by 2026-10-08, the paper prints the corpus
  size and the cluster counts only, states the audit agreement, and prints no count on the
  four audited axes.

## 6. Work package B: human-rated subset

**Purpose.** To compare judge scores with people. Without it the paper reports agreement
among judges only, and the title and abstract say so.

**Sample.** 56 of the 192 cases: 7 from each of the 8 dataset-by-explainer cells, drawn
without replacement with a fixed seed by a script in `scripts/`. Adult SHAP has 7 cases, so
all are taken. Equal allocation is chosen so that no cell is empty; results are reported by
cell and are not weighted back to the 192.

**Material.** Each rater sees what the judges saw in the label-hidden condition (the rendered
prompt content of that case, without the instruction to answer in JSON) and scores the same
seven dimensions on the same 1 to 5 scale.

**Instrument.** A new rating sheet is needed. `tools/human_annotation_viewer.html` and
`tools/annotation_guidelines.md` were made for EXP1: three dimensions, 20 Adult cases, bar
charts. They do not fit the seven-dimension rubric. The sheet is built in this folder.

**Blinding.** Raters do not see judge scores, the explainer name beyond what the judges saw,
or each other's ratings. Case order is randomised per rater.

**Analysis, fixed before the ratings exist**

- Human-human agreement per dimension: ICC(1,1) with the same code as the judges, and the
  share of exact and adjacent agreement.
- Human-judge agreement per dimension and judge: Spearman correlation and mean signed
  difference between the judge score (cohort 2, label-hidden, first replicate) and the mean of
  the two raters, with percentile bootstrap intervals over cases.
- The three judges and two raters together: ICC(1,1) on the 56 cases, beside the judges-only
  value on the same 56.
- With 56 cases the intervals will be wide. The paper reports them and makes no claim from a
  point estimate alone.

**Cut-off.** If both raters' files are not received by 2026-10-10, the paper is submitted
without this section and the subset is named as future work.

## 7. Work package C: judge scores and technical metrics (post hoc)

**Declared post hoc.** This analysis was not planned when EXP4 was designed. One pooled
calculation has already been seen (assessment of 2026-10-04, F04): in the label-hidden
condition the mean judge score for overall quality had a Spearman correlation of about 0.5
with fidelity, 0.5 with stability and 0.7 with sparsity over the 192 cases. Those values mix
explainers and datasets and are not reported.

**Added 2026-10-04, before the analysis was run.** The judges were shown the technical
metrics of each explanation (section 14.2). An association between scores and metrics can
therefore come from the judges reading the numbers. The analysis is run as fixed below and is
reported as "how closely the scores follow the metrics shown in the prompt", not as evidence
that the judges recover technical quality from the explanation.

**Analysis, fixed here before it is run**

- Data: cohort 2, label-hidden, mean of the three judges and three replicates per case.
- Outcome: overall quality (primary); the other six dimensions (secondary).
- Metrics: fidelity, stability, sparsity, faithfulness gap, cost, as stored in the case
  records.
- Method: Spearman correlation **within each explainer**, with percentile bootstrap intervals
  over cases; then a rank regression of the score on the metric with explainer and dataset as
  strata.
- Multiplicity: Holm correction over the five metrics for the primary outcome; the secondary
  outcomes are descriptive.
- A cell with fewer than 20 cases is reported descriptively, without a test.
- Any further analysis is added to this section with its date before it is run.

## 8. Work package D: manuscript and build

- Source in LaTeX with placeholders filled from result files, as Papers D and E; Word and PDF
  made by a build script in `scripts/`, in a blind and a full version.
- Every printed number comes from a result file through the build. The build stops on an
  unresolved placeholder and above 15 pages measured in Word.
- Text taken from the 32-page edition is rewritten for the new question; no Paper B result is
  printed (ADR-0022, decision 5).
- The sentence that the earlier article left the SHAP-LIME contrast unresolved is not carried
  over; it is wrong.

## 9. Work package E: registry and checks (shared files, through `main`)

- The manuscript goes under `[coverage]`; `docs/reports/paper_c/` joins the protected side of
  `[exclusivity]`; `verify_sync.py` checks its abstract and keywords fragments; the
  placeholder abstract in `pub/claims.toml` is replaced.
- The registered `exp4` and `exp4c2` claims gain a site in the new file. New values (human
  subset, section 7, adjudicated corpus counts) need a `paper_c` resolver in
  `scripts/pubs/claim_sources.py`.
- When the paper replaces the 32-page edition under `[coverage]`, the guarded-file lists of
  RCA-001 and RCA-002 are updated in the same change.
- Checks before submission: `verify_claims.py`, `verify_sync.py`,
  `scan_shared_literals.py --strict`, `verify_exp4_reconstruction.py`, the lane tests, and an
  identity scan of the blind files.

## 10. Work package F: review, archive, submission

- Rigor review by the Scientific Advisor role in a separate session; findings to
  `docs/review/`.
- A new Zenodo version before submission, cited in the full version only.
- The author sends the files by email and the submission is recorded in the README here and
  in `ACTIVE_CONTEXT.md`.

## 11. Schedule

| Date | Work |
|---|---|
| 4 Oct | Lane, folder, this plan |
| 5 Oct | Author approves the plan. Sample drawn, rating sheet built and sent to the raters. Adjudication starts |
| 5 to 7 Oct | Build script; methods and reliability results written from registered values; section 7 analysis |
| 8 Oct | Adjudication cut-off. Framing section written |
| 10 Oct | Rating cut-off. Human-subset analysis or its removal |
| 11 Oct | Full draft in Word; length check; registry changes through `main` |
| 12 Oct | Independent rigor review |
| 13 Oct | Fixes; author's read |
| 14 Oct | Zenodo version; final build; blind check |
| 15 Oct | Author submits |

## 12. Risks

- **Time.** Eleven days, with two tasks that depend on other people (sections 5 and 6). Both
  have a dated fallback.
- **Two submissions to one issue.** Paper D was sent to the same special issue on 2026-10-03.
  The call states no limit per author; the editor may still prefer one.
- **Prior availability.** The 32-page edition is public (repository, Zenodo) and carries the
  reliability tables; the thesis chapter 5 carries the same values. The email to the editor
  states it.
- **Double-blind.** The repository and archive identify the author; the blind file cites them
  anonymised.
- **Length.** The Word limit is tight for two cohorts, three conditions and a human subset.
- **Judge tier.** Both panels use small, low-cost models; the conclusions are limited to them.
- **Floor effect.** 86% of actionability scores are 1 in the primary condition; its ICC is
  not informative.

## 13. Author decisions (2026-10-04)

1. The plan is approved and is adjusted as the work goes.
2. The paper is written in English.
3. The human sample has 56 cases, 7 per dataset-by-explainer cell.
4. The two raters are not the second reviewer of the corpus; they are different people.
5. Single author: Jonathan Herrera-Vásquez.
6. The AI-use statement is the one used in Paper D.
7. The editor is not asked about a second submission to the same issue, for now.

## 14. Findings after approval

### 14.1 The label-hidden prompts reveal the label (2026-10-04)

- **Evidence.** All 192 rendered prompts of `hidden_label_primary` in
  `experiments/exp4_cohort2/prompts/` set `true_label` to null and also print the field
  `quadrant` (TP, FN, TN or FP) next to `prediction`. The two together give the true label.
  The other two conditions print the true label and the quadrant.
- **Consequence.** In cohort 2 no condition withholds the true label. The contrast between
  `label_visible_bias_probe` and `hidden_label_primary` compares a label stated outright with
  a label that can be derived. That its effect is small (largest mean shift 0.14 points) does
  not show that the judges ignore the label.
- **Original cohort.** Its prompts are lost; whether they printed the quadrant is not known.
- **In the paper.** The primary condition is named by what it does (true-label field
  withheld, error quadrant shown). Claim 3 of section 1 is limited to rubric wording. The
  finding is stated in the methods and in the limitations.
- **Outside this lane.** The 32-page edition and the thesis chapter 5 describe the condition
  as label-hidden. They are not changed from this lane; the thesis lane must check its text.

### 14.2 The judges were shown the technical metrics (2026-10-04)

- **Evidence.** All 576 rendered prompts print `technical_metrics` (fidelity, stability,
  sparsity, faithfulness gap, runtime, cost) inside the case record, and the prompt text says
  so.
- **Consequence.** The judges scored an explanation together with its metrics. Section 7
  cannot separate what the judges infer from the explanation from what they read in the
  numbers. The title phrase "what do their scores follow" is answered only in that limited
  sense.

### 14.3 Human raters see the same record (2026-10-04)

The rating sheets show the case record of the primary condition as the judges received it,
including the quadrant and the technical metrics, so that people and judges rate the same
material. Seven fields without content for a reader (identifiers, file path, seed, sample
size, token count) are left out of the sheet; they are listed in
`scripts/draw_human_sample.py`.

### 14.4 Option for the author: a clean condition

A fourth prompt condition that shows the explanation without the quadrant, the true label and
the technical metrics would repair 14.1 and 14.2: 192 cases by 3 judges by 1 replicate is 576
calls, about a ninth of the cost of cohort 2 (US$20.24). It is a new cohort under RCA-002, it
is run on the `exp4-cohort2` lane, and it needs the API key. It is not run unless the author
decides so.
