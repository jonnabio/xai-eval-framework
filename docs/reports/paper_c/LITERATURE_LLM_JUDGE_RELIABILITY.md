# Paper C: literature on the reliability of LLM judges (review F11 / N09)

**Date:** 2026-10-04. **Status:** candidates for the author. Nothing here is in
`references.bib` or in the manuscript. The paper is at the 15-page limit, so every added
sentence and reference needs an equal cut.

**How far each entry was checked.** Title, authors, venue and identifier were read on the
publisher or arXiv page on 2026-10-04. Except for XAI-Arena, only the abstract was read.
The summaries below are what the abstracts say; a claim about any of these papers in the
manuscript needs the author to read the paper first. This was a targeted search of about
ten queries, not a systematic one.

## 1. A paper the manuscript must cite: LLM judges of XAI explanations

**Y. Hu Fleischhauer, A. Zharova, N. Klein and S. Feuerriegel, "XAI-Arena: Can LLMs Assess
the Quality of XAI Explanations?", arXiv:2609.09428, 8 September 2026.**
<https://arxiv.org/abs/2609.09428>. Pages 1 to 9 of the PDF were read.

- What it does: one LLM judge (GPT-5.4, temperature 0) rates explanations from SHAP, LIME,
  DiCE, partial dependence plots and permutation importance on eight dimensions with a 1 to
  7 scale, from four stakeholder personas, on synthetic data and three real tabular datasets
  (Breast Cancer Wisconsin, Telco Churn, California Housing), with logistic regression,
  random forest, XGBoost and a perceptron. It compares methods by their mean ratings and
  reports a correlation of 0.693 between LLM and human ratings.
- It states that it is, to its authors' knowledge, the first LLM-as-a-judge framework for
  the quality of XAI explanations.
- Relation to Paper C: same object, same methods, overlapping models and one dataset in
  common, opposite question. XAI-Arena uses a single judge to compare methods. Paper C asks
  whether several judges agree, and finds that they agree on the method and not on the
  explanations of one method. That is consistent with a judge that separates methods and it
  limits what such a framework can be used for.
- Not checked: its Appendix H ("cross-LLM robustness, broadly similar patterns") and whether
  it reports any agreement coefficient among judges or between repeated calls. **The author
  should read Appendix H before the sentence is written**, because it decides whether Paper
  C can say that agreement among judges of explanations had not been measured.
- Consequences for the manuscript:
  - the introduction says LLM judges are "the newest source and the least validated"; with
    this paper, a human-validated framework exists and the sentence needs to say what
    remains unmeasured (agreement among judges, inside a method);
  - the sentence on the scoping corpus ("only 4 concern LLM judges") was true of a corpus
    assembled before September 2026; either date the corpus or replace the sentence.

## 2. Reliability of LLM judges in general

| Work | Checked at | What the abstract says | Use in Paper C |
|---|---|---|---|
| R. Haldar and J. Hockenmaier, "Rating Roulette: Self-Inconsistency in LLM-As-A-Judge Frameworks", *Findings of EMNLP 2025*, pp. 24986-25004, doi:10.18653/v1/2025.findings-emnlp.1361 | ACL Anthology | LLM judges have low intra-rater reliability across runs | Section 3.3: repeated calls at temperature 0 did not return the same score |
| K. Schroeder and Z. Wood-Doughty, "Can You Trust LLM Judgments? Reliability of LLM-as-a-Judge", arXiv:2412.12509, 2024 | arXiv | A reliability framework (McDonald's omega over repeated judgments); single-shot evaluations are risky | Methods and discussion: reliability of one call against several |
| A. Bagaria, S. S. Sundaram, G. S. Krishnan and B. Ravindran, "Judging LLM-as-a-Judge: Concerning Rubric Artifacts in LLM-based Automated Text Generation Evaluation", arXiv:2609.02942, 2026 (the arXiv page gives EMNLP 2026 as venue) | arXiv | Judge outputs can be predicted from the rubric text alone; judges often do not change their decision when the response or the criteria are reversed | Section 3.3 (rubric wording) and the discussion of what the prompt contains |
| R. R. Bellibatlu, E. Raff and W. Zhang, "JudgeSense: A Benchmark for Prompt Sensitivity in LLM-as-a-Judge Systems", arXiv:2604.23478, 2026 | arXiv | Rewording the request lowers agreement on all four tasks, 25 models | Section 3.3, alternative to the previous row |
| P. Wang et al., "Large Language Models are not Fair Evaluators", *Proc. ACL 2024*, pp. 9440-9450, doi:10.18653/v1/2024.acl-long.511 | ACL Anthology | Rankings change with the order of the responses | Background; position bias is already covered by Zheng et al. |
| C.-H. Chiang and H.-y. Lee, "Can Large Language Models Be an Alternative to Human Evaluations?", *Proc. ACL 2023*, pp. 15607-15631, doi:10.18653/v1/2023.acl-long.870 | ACL Anthology | LLM ratings follow those of human experts on two text tasks | Background; the usual first citation for LLM evaluation |

Seen in the search results and not opened: arXiv:2603.28304 (temperature in LLM judges),
arXiv:2602.00521 (item response theory for judge reliability), arXiv:2606.13685 (reliability
and bias of judges), arXiv:2506.22316 (scoring bias).

## 3. Recommendation

Add three references and two sentences, and cut the same length.

1. XAI-Arena, in the introduction, replacing the corpus sentence (two lines for two lines).
2. Haldar and Hockenmaier, where the repeated calls are reported.
3. Schroeder and Wood-Doughty or Bagaria et al., one of the two, in the discussion.

Each reference is about two lines in the Word file, so three references cost about six
lines. Candidates for the cut: the sentence on the Krippendorff check in the methods (it is
"not tabulated" and can be one clause), and the rewording of the LIME passages that the
second review asks for, which shortens them.

Not recommended: more than three or four. The paper is a reliability study with a narrow
question; a referee needs to see that the author knows the judge-reliability literature
exists, not a survey of it.
