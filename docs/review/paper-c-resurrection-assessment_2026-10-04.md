# Assessment: reducing Paper B+C to 13 pages and resurrecting Paper C

**Date**: 2026-10-04 | **Reviewer role**: Scientific Advisor (read-only) | **Requested by**: the author

**Verdict**: Paper C can be resurrected, in one form only: an LLM-judge reliability paper
that uses the taxonomy as its framing. The survey-only Paper C of April 2026 is not viable on
its own. The robustness-scaling Paper C is a new project, not a resurrection.

**Scope reviewed**: `docs/reports/paper_bc/paper_bc_iberamia.tex` and its appendix (32 pages
as built); the earlier prototypes in `docs/reports/paper_b/` and `docs/reports/paper_c/`;
`docs/planning/publication_strategy.md`; `docs/reports/paper_c_robustness_scaling_plan.md`;
`experiments/exp4_cohort2/` (cases, parsed scores, `RESULTS.md`);
`docs/reports/paper_bc/second_reviewer_audit_summary.md`; the rigor review of 2026-09-28.

**Not changed**: no manuscript, registry or result file. One exploratory calculation was run
(section 4); its numbers are a feasibility check and are not results.

## 1. Background

Paper B+C was rejected at the desk by TMLR (2026-10-02) and by *Inteligencia Artificial*
(reported 2026-10-04). Neither notice names a defect. The manuscript joins three bodies of
work: a paired SHAP-LIME benchmark (the former Paper B), a taxonomy with a 44-paper scoping
corpus (the former Paper C), and an LLM-judge reliability study (EXP4), which was added
after the merge. The author has decided to reduce the paper to 13 pages and asks whether the
removed material can become Paper C again.

## 2. Three things have been called "Paper C"

| Candidate | Source | Content |
|---|---|---|
| C-survey | `docs/reports/paper_c/` (April 2026, 14 pages) | Taxonomy and survey of XAI evaluation metrics, 24-paper corpus at the time |
| C-judge | `docs/planning/publication_strategy.md` | LLM-based semantic assessment validated against human annotation |
| C-scaling | `docs/reports/paper_c_robustness_scaling_plan.md` (February 2026) | Cost of stabilising LIME and Anchors by averaging repeated runs |

## 3. Where the 32 pages are now

Approximate, from the built PDF. Section boundaries fall inside pages, so the figures are
rounded to a quarter page.

| Block | Pages | Belongs to |
|---|---|---|
| Title, abstract, Resumen, keywords | 1.0 | shared |
| Introduction | 1.25 | shared |
| Background (distinctions, LIME, SHAP) | 1.75 | benchmark |
| Scoping review protocol and corpus profile | 2.25 | taxonomy |
| Paired benchmark design | 3.0 | benchmark |
| EXP4 method | 0.5 | LLM judges |
| Taxonomy (four axes, two tables) | 1.5 | taxonomy |
| Paired benchmark results | 2.75 | benchmark |
| Cross-dataset results (EXP3) | 2.0 | benchmark |
| EXP4 results | 1.25 | LLM judges |
| Gaps, formalization-aware criteria, layered architecture | 1.5 | taxonomy |
| Practical recommendations | 1.5 | benchmark |
| Validity and limitations | 4.0 | mostly benchmark; about 0.75 taxonomy |
| Broader impact, conclusions, acknowledgments, availability | 1.75 | shared |
| References (57 entries) | 3.75 | shared |
| Appendix A, Tables S1 to S6 | 4.5 | S1, S4: LLM judges and taxonomy; S2, S5, S6: benchmark; S3: neither |

Benchmark material: about 17 pages. Taxonomy and LLM-judge material: about 9.5 pages. Shared
front and back matter: about 8 pages.

## 4. Findings

### F01 - A 13-page benchmark paper is feasible, and it is the April Paper B again

- **Evidence**: the Paper B prototype (`paper_b_prototype_jmlr.pdf`) has 14 pages with the
  same structure: paired inference, runtime, recommendations, validity. The benchmark
  material in the current manuscript is 17 pages before cutting.
- **Budget that reaches 13 pages** (journal format unchanged):

  | Block | Now | Target |
  |---|---|---|
  | Front matter | 1.0 | 0.75 |
  | Introduction (two contributions, no optimisation problem) | 1.25 | 1.0 |
  | Background | 1.75 | 0.75 |
  | Benchmark design | 3.0 | 2.25 |
  | Paired results | 2.75 | 2.5 |
  | Cross-dataset results | 2.0 | 1.25 |
  | Recommendations and discussion | 1.5 | 1.0 |
  | Validity and limitations | 4.0 | 1.25 |
  | Conclusions, acknowledgments, availability | 1.75 | 0.75 |
  | References (about 30) | 3.75 | 1.5 |
  | **Total** | | **13.0** |

- **What this requires**: remove the scoping review, the taxonomy, EXP4, the three gaps,
  the layered architecture and the broader-impact section; move Tables S2, S5 and S6 to the
  archive instead of the PDF; drop Table S3. The largest single cut is in the validity
  section (4 pages to 1.25).
- **No result changes.** Every number that stays is already registered.

### F02 - Reduction fixes the focus problem, not the novelty problem

- **Evidence**: the introduction states that the protocol, the cohort and the four-method
  omnibus result are already published in the RIMI article. Paper E, now under review,
  compares SHAP and LIME on the same runs at instance level. After reduction, the paper's
  own contribution is the paired contrast with effect sizes on 75 Adult cells, the
  per-model cost reversal (XGBoost against Random Forest), and the LIME cross-dataset
  extension.
- **Reasoning**: an editor who rejected the 32-page version for scope would see a tighter
  paper. An editor who rejected it as incremental would see the same benchmark with less
  around it. The notices do not say which applies.
- **Recommendation**: lead the 13-page paper with the result that has no counterpart
  elsewhere, which is the conditional deployment finding (the latency ordering depends on
  the model family, and LIME's near-zero stability on Adult depends on kernel width and
  feature space). Do not lead with "SHAP beats LIME".

### F03 - C-survey alone is not viable

- **Evidence**:
  - 44 coded papers, coded by one reviewer.
  - The second-reviewer audit covers 16 papers. Exact agreement is 25.0% on the
    quality-property axis and 56.2% on evidence source; 12 of 16 records needed
    adjudication, and no adjudication record is in the folder.
  - The original screening record is not released, and four coded papers were lost.
  - The taxonomy section presents four axes by argument; nothing tests them.
- **Reasoning**: a survey paper is judged on coverage and on the reliability of its coding.
  Published reviews in this area code several hundred papers. On both criteria this corpus
  is weaker than the work it would be compared with, and the paper itself says so.
- **Conclusion**: the corpus supports a framing section of about two pages. It does not
  support a standalone taxonomy or survey paper.

### F04 - C-judge is viable, and it has unused evidence

- **Evidence already in the repository**:
  - Two cohorts on the same 192 cases, each with three judges and seven dimensions.
  - Cohort 2: 5,184 calls (3 conditions by 3 replicates), 5,180 parsed, raw responses
    released.
  - `experiments/exp4_cohort2/RESULTS.md` reports three findings that the manuscript does
    not use: showing the explainer label barely moves the scores (largest mean shift 0.14
    points); rubric wording moves them more (up to 0.50 points); and test-retest agreement
    at temperature 0 differs by judge (0.96 to 0.98, 0.82 to 0.88, 0.59 to 0.68).
  - Every case record carries the technical metrics of its explanation (fidelity,
    stability, sparsity, faithfulness gap, cost): 192 of 192 complete.
- **Feasibility check (exploratory, not a result)**: in the label-hidden condition, the mean
  judge score for overall quality has a Spearman correlation of about 0.5 with fidelity,
  0.5 with stability and 0.7 with sparsity across the 192 cases. This shows that the
  analysis the title promises, from fidelity to semantics, can be run on existing data. The
  values cannot be reported as they stand: see F05.
- **Reasoning**: this is the only part of Paper B+C whose data is not the EXP2 runs already
  used by Papers A, D and E. It gives a paper with one question (can LLM judges score
  explanations reliably, and what do their scores track?), a negative primary result that
  replicates, and three secondary analyses. The taxonomy and the three gaps become its
  motivation, where the small corpus is adequate.
- **Size**: about 9.5 pages of existing material, plus the unused findings and references.
  A paper of 12 to 14 pages is realistic.

### F05 - Limits that C-judge must state or repair

1. **No human reference.** The study measures agreement among LLM judges, which is
   reliability. It does not measure validity. The annotation tool, guidelines and analysis
   script exist (`tools/human_annotation_viewer.html`, `tools/annotation_guidelines.md`,
   `scripts/analyze_human_llm_agreement.py`); no human ratings were collected. Two human
   raters on a stratified subset of 50 to 60 cases would change the paper from "judges
   disagree with each other" to "judges disagree with each other and with people", which is
   the stronger and more publishable claim. Without it the title and abstract must say
   inter-judge reliability only.
2. **Unbalanced case inventory.** Adult has 7 SHAP cases against 32 LIME, 32 DiCE and 25
   Anchors; LIME and DiCE appear on Adult only. Any association between judge scores and
   technical metrics is confounded with explainer and dataset. It must be analysed within
   explainer, or with explainer as a stratum, and declared as post hoc with a dated plan
   before it is run.
3. **Original cohort.** Raw responses and prompt templates are lost; the ICC rests on 147
   complete cases. The replication is a second panel, not a reproduction. The manuscript
   already says this and must keep saying it.
4. **Floor effect.** 86% of actionability scores are 1 in the primary condition, so its ICC
   near zero is not informative about agreement.
5. **Judge tier.** Both panels use small, low-cost models. The conclusion applies to them.

### F06 - C-scaling is not a resurrection

- It needs a new experiment (averaging K LIME runs and measuring stability against K).
  Nothing removed from Paper B+C supplies it; Tables S2 and S5 vary configuration, not
  repetition.
- It overlaps Paper E's self-agreement experiment (LIME against LIME, 0.690 / 0.642 / 0.836).
- Keep it as a possible later paper. It is outside this decision.

### F07 - The split must not create redundant publication

- **Evidence**: Papers A, B, D and E analyse the same EXP2 and EXP3 executions. Paper E's
  submitted text names Paper B+C as a companion manuscript.
- **Requirements**:
  - No number appears in both B and C. The `[exclusivity]` mechanism in
    `pub/claim_registry.toml` can enforce it once each paper is a registered document.
  - Each paper cites the other and the RIMI article, and tells the editor about both.
  - C states that its cases are drawn from the executions of the earlier studies.
  - If Paper E is revised, its companion statement is updated to the new titles.

## 5. Verdict by candidate

| Candidate | Resurrectable after the reduction? | Condition |
|---|---|---|
| C-survey (taxonomy and corpus alone) | No | Corpus size and coding agreement do not carry a survey paper |
| C-judge (EXP4, taxonomy as framing) | **Yes** | Scope the claim to inter-judge reliability, or add a small human-rated subset |
| C-scaling (stabilisation cost) | No, new project | Needs a new experiment |

Of the two papers, C-judge has the more distinctive evidence. The 13-page benchmark paper
carries the larger risk of a third rejection (F02).

## 6. What the split would cost in this repository

- New ADR: Paper B+C is split; it supersedes ADR-0020 (venue) and amends ADR-0019.
- `pub/claim_registry.toml`: 321 claims at 487 sites point at the two IBERAMIA files. Each
  claim moves to the file that keeps it; both new files go under `[coverage]` and
  `[exclusivity]`. RCA-001 and RCA-002 guard these files.
- `scripts/pubs/lanes.toml` has no Paper C lane. `docs/reports/paper_c/` holds the April
  prototype.
- ADR-0018 (the CIFIE chapter prints no unpublished Paper B+C result) must cover both papers.
- The thesis sync matrix names Paper B+C in its rows.
- A new Zenodo version before either paper is submitted.

## 7. Questions for the author

1. Where does the 13-page limit come from, and does it include references and appendices?
   The budget in F01 assumes it includes references and that there is no appendix.
2. Were the 12 audit records that needed adjudication ever adjudicated, and is there a
   record of it?
3. Can two people rate 50 to 60 explanations with the existing annotation tool? This decides
   which claim C-judge can make (F05, item 1).
4. Which paper goes first? The answer decides where the taxonomy text lives, since it can
   appear in only one.

## 8. Author's answers (2026-10-04)

1. **13 pages**: the author's own target, on the hypothesis that long articles are harder to
   review and publish. It is not a journal rule. Treated as a target that includes
   references.
2. **Adjudication**: none was done so far. The author decided that the disagreements must
   be considered: each one is adjudicated and the decision recorded, in
   `docs/reports/paper_bc/second_reviewer_adjudication_sheet.csv` (28 disagreements in 12
   records: 12 on quality property, 7 on evidence source, 6 on evaluation target, 3 on task
   context). In 19 of the 28 the primary coder assigned a label that the second reviewer
   did not assign and the second reviewer added none. A rule adopted in adjudication changes
   the codebook, so it must also be applied to the 28 papers outside the audit, and the
   corpus counts recomputed and re-registered.
3. **Human raters**: available. Two raters on a stratified subset of 50 to 60 cases.
4. **Order**: "taxonomy goes first". Reviewer's reading, not yet confirmed by the author: the
   first paper to write is Paper C (taxonomy as framing, LLM-judge study as evidence); the
   13-page benchmark paper follows without the taxonomy.
