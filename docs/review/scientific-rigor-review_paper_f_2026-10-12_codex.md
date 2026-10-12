# Paper F: scientific and editorial review for the author

Date: 2026-10-12. Role: Scientific Advisor, using ACE scientific-rigor-review and manuscript-editing, with the scientific-book-editor technical and narrative criteria adapted to an English journal article.

**Recommendation: major revision of the argument and interpretation.** The existing experiment can support a useful, narrower paper about the reproducibility of rankings under a specified evaluation protocol. It does not establish a general ranking of explanation quality. Additional experiments are necessary only if the author wants to retain that stronger interpretation.

**Dimensions:** evidence relevance 3; falsifiability 3.5; scope calibration 3; argument coherence 3.5; reporting honesty 4; methodological rigor 3. Mean: 3.3/5. These are editorial judgments, not measured research outcomes.

## Scope and verification

Reviewed the complete current manuscript (`paper_f_template.tex`, generated `paper_f.tex`), all three generated tables, and Figure 1 visually; the analysis plan and amendment log; current results report; the two earlier reviews and their editor dispositions; relevant venue/README guidance; references supporting the central motivation; and implementation of preprocessing, explanation adapters, measures, ranks, inference, failures and resume behavior in `scripts/paper_f_lib.py`, `scripts/paper_f_analyze.py`, `scripts/paper_f_run.py` and `scripts/paper_f_posthoc_descriptives.py`. Reference point: HEAD `7d8652cfcd3d1f616518c834b7b15e4b7d0a320d`.

Inspected `primary.csv`, `cells.csv`, `posthoc_descriptives.csv`, and secondary results. Independently recomputed the four mean pairwise Spearman correlations from `cells.csv`: gap 0.6683333333, stability 0.8783333333, sparsity 0.7893505364, cost 0.8683333333. They match the stored primary estimates. No experiment or planned analysis pipeline was rerun.

Claim verifier passed: **1,303 claims re-derived, 1,642 manuscript sites checked, 60 retired-value guards clear, 13 cited artifacts present, 33 files fully registered, 25 files clear of unpublished results.** RCA-001 applies through publication coverage: registered numbers must match their artifacts, with correct aggregation and evidence attribution. Passing this check establishes traceability, not validity of a metric or conclusion. RCA-002/003 list no Paper F manuscript path directly; no guarded manuscript, registry, fragment or experimental artifact was edited.

Limits: this is a scientific argument and implementation review, not a full raw-data audit, comprehensive reference audit, rerender of the submission Word/PDF, or replication of bootstrap/permutation uncertainty. Archived metadata and DOI contents were not audited. Source checks below distinguish full-text inspection from abstracts/documentation.

## What is worth preserving

- The question matters: a method selected using one benchmark may behave differently on another.
- The blocked comparison uses the same fitted classifier and instances for the four methods, with dataset-level inference rather than treating instances as independent datasets.
- The fixed plan, explicit deviations, failure accounting and generated numeric claims make the experiment unusually inspectable.
- The paper reports the weaker faithfulness-gap decision and labels the descriptive additions made after seeing results.
- The revised text already acknowledges configuration effects, unequal masking budgets, stochastic stability, invalid categorical counterfactuals and the heavy tail of runtime. These are real improvements over the versions reviewed earlier.

## Findings and actionable author questions

### F01 — Major: decide what the common comparison actually means

**Where:** `paper_f_template.tex:244` (Measures), Introduction and Conclusions. **Dimensions:** D1, D3, D6.

**Text:** “each explanation ... is first reduced to a vector of non-negative weights”.

Converting outputs to vectors makes a common score computable; it does not establish that the score measures each explanation's intended success. An Anchors rule offers sufficient conditions for a prediction, whereas deleting its conditions tests a different question. DiCE proposes changes toward another outcome; ranking absolute changes and replacing them with means does not evaluate those proposed changes. LIME/SHAP concern contributions to an output, with signed information discarded here.

The distinction is supported by the [original Anchors paper](https://ojs.aaai.org/index.php/AAAI/article/view/11491) and [DiCE documentation](https://interpret.ml/DiCE/notebooks/DiCE_getting_started.html). My methodological inference is that the shared representation supports a comparison of feature-set proxies, rather than a validated common measure of native explanation quality.

**Question:** What exactly is transferred across datasets: quality of explanations for a user task, or rankings produced by these feature-vector reductions?

**Request:** Add a short justification for the reduction and explicitly name what it discards. State that this study evaluates rankings under the common proxy protocol. Remove any implication that the four outputs have thereby become interchangeable or equally well evaluated. If native explanation quality is the intended claim, report suitable native checks and justify their relationship to the common scores; a caveat alone cannot establish that relationship.

### F02 — Major: make the research gap and contribution specific

**Where:** `paper_f_template.tex:69`, `:115`, `:148`, `:167`. **Dimensions:** D1, D2, D3.

**Text:** “Explanation methods are usually compared on one dataset”; “The product of a comparative study is an order”.

These claims simplify the literature and practitioner decision process. The cited Klein benchmark already examines dataset/model dependence and ranking behavior in computer vision. Its full text supports the broad concern about evaluation, but cannot establish that most tabular studies use a single dataset. Gevaert's abstract supports the claim that image metric results need not transfer; this review did not inspect its entire paper.

Sources: [Klein et al., full text](https://arxiv.org/html/2409.16756v1); [Gevaert et al., abstract](https://arxiv.org/abs/2202.12270).

**Questions:** Which closest tabular studies already test ranking transfer? What does this study add beyond repeating that question in another domain? Is the contribution the fixed dataset-selection rule, the cross-format comparison, the estimated transfer strength, or the exceptions to the Adult ordering?

**Request:** Replace the broad opening with an evidenced, bounded statement. Add a compact comparison of the nearest studies and identify the precise missing analysis. Do not claim that ranking-transfer research is new in XAI. Reduce general lists of SHAP/LIME weaknesses unless they help explain the present design.

### F03 — Major: the gap is a masking response, with several unresolved validity limits

**Where:** Measures, `paper_f_template.tex:244` onward; Discussion and Conclusion 2. **Dimensions:** D1, D6.

**Text:** “Higher is better for G”.

The unequal masking budgets are now disclosed, but other limits remain. A larger absolute probability change can result from masking more features, from an unrealistic masked input, or from the model's response away from the observed data distribution. It does not by itself demonstrate a better explanation. The baseline in `paper_f_lib.py:332` replaces one-hot columns separately with their marginal modes, so the resulting category group need not be a valid one-hot representation. Numeric means can also break feature dependencies. The paper acknowledges invalid DiCE outputs but does not clearly acknowledge invalid inputs created by its evaluator.

**Questions:** Does the masking preserve valid categories and plausible feature combinations? Why should a larger absolute change establish better faithfulness for all four output types? What evidence separates feature selection from the number of features masked?

**Request:** Call G a deletion/masking-based faithfulness proxy and say that larger values mean greater sensitivity to the specified masking operation. Disclose possible off-distribution inputs and broken categorical groups. Keep “SHAP has the largest measured gap” as a descriptive result; remove any inference that it is therefore the most faithful method. Equal-budget, category-preserving or conditional masking would be additional, explicitly post hoc work if undertaken; do not silently substitute it for the planned result.

### F04 — Major: soften the claim that the data “decide” certain orders

**Where:** Discussion `paper_f_template.tex:452` onward and Conclusion 2 (`:508`). **Dimensions:** D1, D3, D4.

**Text:** “Where the data decide the order”.

The study does not separate effects caused by dataset properties from effects caused by representation, settings, model behavior, or metric construction. Even the faithfulness-gap order remains confounded by masking budget. The new admission of these confounds is inconsistent with presenting the remaining rankings as cleanly data-determined.

**Questions:** Which comparisons are shown to respond to dataset changes rather than merely being less structurally constrained? What useful decision should the reader make from an observed ranking reversal?

**Request:** Replace this wording with “Among the comparisons whose order varies across the evaluated datasets...” or equivalent. Avoid causal claims about why an order holds. Describe the study as measuring observed cross-dataset agreement under fixed settings. Keep the preplanned verdict label, but define “generalises” locally as the study's threshold classification, not demonstrated transfer to an arbitrary deployment.

### F05 — Minor: the hypothesis is testable but scientifically weak

**Where:** Purpose/hypothesis (`paper_f_template.tex:167`); Statistical analysis and first Discussion paragraph. **Dimensions:** D2, D1.

**Text:** “agrees across tabular datasets more than chance”.

The revised Discussion correctly says rejection was expected. Widely different computational procedures and fixed output budgets make uniformly unrelated ranks an undemanding null. Rejection cannot tell how much agreement follows from dataset-independent configuration. Conversely, a nonsignificant test would not prove unrelatedness or refute the hypothesis conclusively.

**Question:** What magnitude or particular ranking reversal would change the author's scientific or practical belief?

**Request:** Preserve the hypothesis and decision rule as planned; do not rewrite them as if a stronger hypothesis had been registered. Lead the contribution with the estimated agreement, its uncertainty, and named exceptions. Explain that 0.5 is a prespecified descriptive convention, not a validated threshold for safe method selection. Put small p-values in a supporting role.

### F06 — Minor: distinguish a fixed selection procedure from a representative sample

**Where:** Datasets (`paper_f_template.tex:176`); Statistical analysis (`:273`); limitations. **Dimensions:** D3, D6.

**Text:** “chosen by a rule and not by hand, so that the choice could not favour one outcome”; “the only independent units”.

The candidate pool, ordering, inclusion cutoffs and AUC gate were choices. Fixing them before explanation results reduces outcome-driven selection; it does not eliminate selection effects or yield a random sample of tabular problems. Acknowledging the software-defect family later does not make the earlier unconditional independence statement true.

**Questions:** What population of tasks does the author intend to describe? What is excluded by the AUC and feature-count rules? Why should the chosen collection represent that population?

**Request:** Say the deterministic procedure was fixed before explanation outcomes were inspected. Describe datasets as the units of analysis, with independence assumed for resampling and imperfect because of related datasets. Keep the family sensitivity check and the feature-composition limitations. State that intervals characterize uncertainty under this resampling assumption, not guaranteed performance on new domains.

### F07 — Minor: show score differences as well as ranks

**Where:** Table 2, Figure 1, Selected results, and method-selection motivation. **Dimensions:** D1, D6.

All figures and main tables emphasize order. A rank change can reflect a negligible score difference, whereas unchanged rank can hide a large change in magnitude. Dataset bootstrap intervals on average agreement do not express uncertainty of a particular method pair's score difference on one dataset. Averaging four classifiers also describes an equally weighted mixture, not necessarily a practitioner's chosen model.

**Questions:** Are the important reversals large enough to matter? Are they consistent across seeds and classifiers? Why is equal weighting of these four classifier families the intended target?

**Request:** For the main changing pairs, provide score differences or ratios from existing cell means, with the seed/model variation made visible. Label any new descriptive summary as post hoc. Explain the classifier weighting and that SHAP pools two implementations. If page space prevents this, give an explicit archive table reference and remove deployment advice that depends on unshown practical effect sizes.

### F08 — Minor: disclose arbitrary selection among tied Anchors features

**Where:** Measures; `scripts/paper_f_lib.py:319`. **Dimensions:** D6, D5'.

Anchors assigns weight 1 to every rule feature. `top_set` breaks equal weights by encoded column index. For a rule larger than the masking or top-five budget, selected features are therefore determined by column order, not importance. This affects both the gap and stability. The manuscript defines the “largest weights” without describing this ambiguity.

**Questions:** How often does an Anchors rule exceed the relevant budgets? Would reordering encoded columns change the evaluation?

**Request:** State the deterministic tie-breaking rule and its limitation. A frequency count from stored rule lengths would quantify exposure if desired, and must be labeled post hoc. Do not describe the resulting subset as the most important rule conditions. A different tie-handling analysis would be additional work, not an editorial correction to the frozen results.

### F09 — Minor: correct deterministic and universal assertions

**Where:** Discussion `paper_f_template.tex:452`; absolute-score interpretation near `:475`. **Dimensions:** D1, D4.

**Text:** “SHAP cannot be the sparser of the two”; “which places [DiCE] last”; “a value of the gap cannot be carried from one dataset to another”.

The SHAP claim is stronger than the code: sparsity counts nonzero weights, and TreeSHAP can produce zero contributions. Random search does not logically force DiCE to rank last; last place is an observation under this protocol. A variance decomposition shows score variation, not the impossibility of transferring any score to any other dataset.

**Request:** Use “SHAP was generally less sparse under these settings”; “DiCE ranked last on measured stability, which combines input and algorithmic variation”; and “absolute gap values varied substantially across datasets and should not be assumed to transfer”. Keep causal explanations tentative unless independently tested.

### F10 — Minor: the runtime sensitivity comparison changes two things

**Where:** Selected results, median-versus-mean paragraph; `scripts/paper_f_posthoc_descriptives.py:76` onward. **Dimensions:** D6, D5'.

The median uses successful instances only. The planned mean in `cells.csv` includes worst-observed-value imputations for failures. Thus the reported 14-versus-8 comparison changes both the summary statistic and failure treatment. It suggests sensitivity to runtime definition, but alone does not isolate the heavy tail as the cause.

**Questions:** Does the comparison hold when both mean and median use the same successful instances? Is the practical target typical latency, expected compute expenditure, or failure-aware service cost?

**Request:** Explicitly say “run medians among successful instances” and explain the difference from the planned failure-penalized mean. Soften “a small share ... decides” to a sensitivity statement unless a matched comparison is supplied. Define whether explainer setup time is excluded; add machine, software and concurrency information or an exact archive pointer. Do not claim runtime ranking is hardware-independent.

### F11 — Minor: check restart-dependent LIME reproducibility and failure labels

**Where:** Research scenario; `scripts/paper_f_run.py:53`; `scripts/paper_f_lib.py:297`. **Dimensions:** D5', D6.

The current paper discloses LIME's advancing random generator, but not the implication of resuming a partly finished job: `run_job` creates a fresh explainer and skips completed instances without restoring its generator state. Reproduction from an uninterrupted job can therefore differ if a recorded LIME job resumed. This is a conditional concern; this review has not established that a LIME job actually resumed. Separately, DiCE's broad exception wrapper records the exception class but discards the original message, so “no explanation returned” is safer than attributing every non-time-limit failure to inability to find a counterfactual.

**Questions:** Did any LIME job restart after it had saved instances? Are logs sufficient to establish this? Are DiCE failure causes known beyond their exception classes?

**Request:** Audit available run logs and state any reproducibility limitation. Do not repair code and regenerate frozen results silently. Keep failure descriptions at the level established by recorded evidence. Also replace “seeds are run one after another” with the actual scheduling description: ordered seeds with overlap at their ends, as logged in the plan.

### F12 — Minor: finish the editorial alignment and useful presentation

**Where:** Abstract, Introduction, Figure 1, archive README and RESULTS_REPORT.

**Requests:**

- Make the abstract explicitly say these are fixed configurations and operational measures. Its broad statement about single-dataset practice needs support or narrowing.
- Replace repeated four-number lists with measure-labeled text or a compact table; make “strength not determined” mean uncertainty relative to the prespecified threshold, not absence of an estimated effect.
- In Figure 1, explain that connecting lines join unordered dataset categories and carry no trend meaning; a rank heatmap is an alternative. Use readable dataset labels and explain tied ranks. The figure is visually legible and distinguishes methods through both markers and line styles.
- Update the results report and README so the archive tells the same scoped story as the revised paper; older design scaffolding should be visibly marked superseded.
- Verify the latest rendered submission matches the revised source. This review did not inspect or rebuild Word/PDF and does not certify layout or page count.

## Previous findings: current disposition

First review (`scientific-rigor-review_paper_f_2026-10-12.md`): F01–F04 and F06–F07 are addressed in the current text, with the additional qualifications above; F05's feature counts are now printed; F08's central Klein/Gevaert statements are supported by the source checks at the stated depth, while a comprehensive literature audit remains open; F09's numeric prose improved but presentation can still be simplified.

Independent review (`..._independent.md`): F01 and F02 are substantially addressed as disclosures, but carried forward here as questions of construct validity and conclusion scope (F01, F03, F04). F03 is addressed except the newly identified tie handling (F08). F04 is addressed in direction, but carried forward because the median comparison also changes failure treatment (F10). F05–F07 are addressed, with remaining precision/reproducibility issues in F10–F11. F08 is acknowledged in the Discussion and carried forward as contribution framing (F02, F05). F09 is mostly addressed but “data decide” remains too strong (F04). F10 is disclosed, with evaluator-created invalid categories additionally identified here (F03). F11 is optional, not a required experiment. No prior reviewer numerical calculation is treated as newly verified merely because the editor marked it fixed.

## Claim map and readiness

| Top-level claim | Evidence | What it supports |
|---|---|---|
| Rankings agree more than chance | `primary.csv`, rank/permutation implementation | Rejection of unrelated label rankings under this protocol; not validation of the measures |
| Agreement exceeds the study's threshold on three measures | Registered bootstrap intervals and fixed decision rule | A threshold-based classification for this selected collection and resampling scheme |
| SHAP most often has the largest gap | `ranks.csv`, generated figure and registered counts | Largest response to this masking procedure; not native quality superiority |
| Anchors–DiCE ordering changes | `pairs_vs_adult.csv`, runtime descriptives | Metric- and aggregation-specific exceptions; not that all other pairs are invariant |
| Sparsity and gap are opposed | Rankings plus features-used/masked descriptives | Observed opposition with definition coupling; not an independent quality trade-off |

**Author's first decision:** retain the current experiment as a study of protocol-dependent ranking agreement, or seek a broader explanation-quality claim that needs metric validation and additional controls.

For the narrower paper, the immediate work is editorial: clarify the contribution, describe the proxies and their limits, remove deterministic/causal overstatements, and align abstract and conclusions. Small archive-based checks can then answer the tied-feature, runtime and restart questions. No full benchmark rerun is requested by this review. Stronger claims about native explanation quality or fair cross-format superiority would require further evidence.

**Suggested scoped takeaway:** “Under fixed configurations and a common feature-based evaluation protocol, rankings were largely consistent across the selected tabular tasks. Some agreement reflects output constraints and metric construction; observed exceptions show why a ranking should be interpreted together with its evaluation protocol rather than treated as a universal ordering of explanation quality.”

## Editor's disposition (2026-10-12, not by the reviewer)

Added by the session that edits the manuscript, at the author's instruction to implement
the suggestions. The text above is the reviewer's and is unchanged. The author's first
decision is taken as the narrower paper: agreement of rankings under fixed settings and
one evaluation protocol. New figures come from `scripts/paper_f_posthoc_protocol.py`,
logged in the plan (section 12) before it was run.

| Finding | Action in `paper_f_template.tex` |
|---|---|
| F01 | Done. The Measures say what the reduction to weights discards and that the measures are proxies on the features named; the Introduction, the abstract and Conclusion 1 say the object is the rankings this protocol produces, not explanation quality. Native checks are named as further work, not computed |
| F02 | Done in part. The opening is bounded ("often compared on one or a few datasets"; "typically yields"; "not always tested"); the two unsupported sentences on tabular practice and the uncited sentence are removed or reworded; the Purpose says the question is not new and names what the study adds. Klein et al. is described from its abstract as a benchmark of saliency methods. **Not done:** a comparison with the nearest tabular studies; no new reference was added, since none was searched and verified |
| F03 | Done. G is called a masking-based proxy; the Measures disclose inputs outside the data and one-hot groups that no category has; a larger G is said not to be evidence of a better explanation; "largest measured gap" |
| F04 | Done. "Where the data decide" is replaced by "the comparisons whose order varies across the evaluated datasets"; a sentence says the study does not separate the contribution of the dataset from that of representation, settings, classifier and measure; "generalises" is defined as a class of the rule, in the Methods and in the sentences of the outcomes |
| F05 | Done. The hypothesis and the rule stay as registered; the Methods call 0.5 a convention fixed in advance and not a validated threshold; the Discussion already led with the size of the agreement |
| F06 | Done. The datasets are said to be chosen by a rule fixed before any explanation was computed and not to be a random sample; independence is said to be assumed for resampling and approximate; the intervals are said not to describe a new domain |
| F07 | Done with medians. The Results give the median difference of Anchors and DiCE in gap and sparsity beside the median range of the four methods, and the median cost ratio beside the range; the Methods say the four classifiers are weighted equally and that SHAP pools two variants. Per-seed and per-classifier variation of the pairs is not shown |
| F08 | Done. Ties broken by column index are stated in the Measures; the share of Anchors rules above each budget is printed (18% above the masking budget, 10% above five) |
| F09 | Done. The three statements are softened as proposed |
| F10 | Done. The planned mean with failures, the mean of successes and the median of successes are given side by side (DiCE faster on 8, 9 and 14 of 16 datasets), and the conclusion is stated as a dependence on how slow searches are counted |
| F11 | Done. By the file times of the run's working directory, the time on disk of every one of the 320 LIME jobs exceeds the time of its rows by 0.4 s at most: none was restarted (`results/audit_resume.csv`, a dated record that cannot be repeated from the archive). "One after another" is corrected to the overlapping schedule. The failure wording was already "returned no explanation" |
| F12 | Done in part. Abstract: fixed settings and operational measures; Figure 1: the caption explains the lines and the ties, and the figure is slightly lower; RESULTS_REPORT carries a note on the scope. Not done: a table in place of the four-number lists; readable dataset labels in Figure 1 |
