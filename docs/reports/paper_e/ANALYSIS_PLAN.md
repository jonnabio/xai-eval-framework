# Paper E — scientific analysis plan

**Question:** *Do explainers agree on which features matter?*
**Status:** Pre-analysis plan, 2026-10-03. No Paper E result has been computed.
**Scope:** Existing EXP2 Adult explanations plus a new, instance-aligned EXP3 LIME
cohort for German Credit and Breast Cancer. The plan must be committed before
calculating Paper E statistics or running the new LIME cohort.

## 1. Motivation and scope

The paper studies whether different explainers identify the same features for
the same model prediction, and whether this agreement varies with model,
sampling intensity or prediction correctness. Paper D asks whether explanation
quality differs between correct and incorrect predictions; Paper E will cite
that work and will not repeat its analyses.

The primary comparison is SHAP versus LIME. Both provide signed additive
feature contributions for the encoded positive class, making feature ranking
and direction directly comparable. Anchors and DiCE do not provide the same
kind of signed attribution: Anchors supplies a sufficient-condition rule and
DiCE supplies features changed in a counterfactual. Their feature-set
comparisons are secondary and descriptive, not evidence that the methods
estimate the same construct.

All Paper E results are new agreement or association statistics. The paper
will disclose that the source EXP2/EXP3 cohorts also support Papers A and B+C,
and will not re-report their published method-level quality results.

## 2. Research questions

- **RQ1 (primary):** For the same instance and model, how much do SHAP and LIME
  agree on the most influential features and their ordering?
- **RQ2:** How does SHAP–LIME agreement vary across model families and EXP2
  sampling intensities? How does it look in the two EXP3 datasets?
- **RQ3:** Within a model/run, is SHAP–LIME agreement different for correctly
  classified and misclassified instances?
- **RQ4 (exploratory):** Is instance-level SHAP–LIME disagreement associated
  with the fidelity or stability measured for either explainer?
- **Secondary (EXP2 only):** What feature-set overlap is observed between
  SHAP/LIME, Anchors' active rule features and DiCE's changed features?

All inferential tests are two-sided. No directional hypothesis is assumed
without a verified, author-approved literature basis.

## 3. Data and cohort alignment

### EXP2 — UCI Adult

Use the instance-level JSON under
`experiments/exp2_scaled/results/<model>_<method>/seed_*/n_*/results.json`.
The existing inventory records 299 run files across five model families,
four methods, five seeds and three intensities (`n = 50, 100, 200` per
quadrant); some runs are empty or failed. The analysis will inspect the source
files directly and use only runs with valid, aligned instance records for the
specific comparison. The stored top-10 entries are ordered by absolute
importance. `n` denotes the configured sample per quadrant, not total
instances in a run.

Within each `(model, seed, n)` block, comparisons use the intersection of
instance IDs across the methods being compared. The analysis will report
available, matched, missing and duplicate IDs by method and block; it will not
assume a complete grid from the directory names.

### EXP3 — German Credit and Breast Cancer

Use the committed per-instance SHAP and Anchors JSON files. The existing
`run_exp3_lime.py` samples the test set independently and currently writes only
run-level averages; that output cannot support instance-paired agreement.
Extend the experiment to save per-instance signed attributions and stable
instance IDs in a new, separate output directory. For each dataset/model/seed,
target the IDs in the existing SHAP cohort, then verify exact ID equality
before comparing methods. Do not overwrite
`outputs/analysis/exp3_lime_results.csv` or any existing EXP3 results.

This is a new LIME cohort, not a reproduction of the old aggregate run. Record
the source run IDs, model/preprocessor hashes, data split identity, LIME
configuration, random seeds, software versions and run status. If the IDs
cannot be reconstructed exactly or the model/split differs, stop the paired
EXP3 comparison and document the mismatch rather than silently using a
different sample.

### Attribution semantics

- **SHAP/LIME:** retain signed values for encoded class `1`; ranks use
  descending absolute contribution. State the direction as toward/away from
  class 1, not as a substantive benefit or harm.
- **Anchors:** a feature is active only when its rule indicator is `1`.
  Zero-padded entries are not rule features; rule length is not a feature rank.
  The serialized `raw_top` has a top-10 cap, so a row with ten active entries
  may be truncated and cannot be treated as the full rule set.
- **DiCE:** a feature is changed only when the encoded original-to-counterfactual
  absolute difference is positive. The change magnitude is not an additive
  attribution or a direction of effect.
- For SHAP/LIME, distinguish a genuinely empty explanation from missing,
  failed, non-finite or malformed output. Empty-vs-empty set similarity is
  undefined and will be counted separately, not scored as perfect agreement.

## 4. Measures

### Primary SHAP–LIME agreement

For each matched instance:

1. **Top-5 Jaccard overlap** is the primary agreement measure:
   `|SHAP_top5 ∩ LIME_top5| / |SHAP_top5 ∪ LIME_top5|`.
2. **Top-10 rank concordance** is secondary. Compute Kendall's `tau-b` on the
   union of the two top-10 lists, assigning rank 11 to a feature absent from a
   list; tied ranks use midranks. Report the proportion of instances with an
   undefined coefficient separately.
3. **Sign agreement** is the fraction of shared, nonzero top-5 features whose
   signed SHAP and LIME values have the same sign. Always report its denominator
   and feature coverage; do not interpret it without the overlap measure.
4. **Top-10 Jaccard** is a prespecified sensitivity measure.

Feature identity uses the exact encoded feature names in the artifacts. No
post-hoc grouping of one-hot features is allowed in the primary analysis.

### Secondary feature-set comparisons

For EXP2 only, report Jaccard overlap between (a) the nonzero active Anchors
serialized rule set, (b) the positive-change DiCE feature set and (c) each
additive method's top-5 set. Exclude Anchors rows whose top-10 cap may truncate
the rule. These are descriptive, cross-construct feature-set comparisons. Do
not calculate sign or rank agreement for Anchors or DiCE and do not make
inferential claims that they agree in attribution.

### Quality associations

For RQ4, relate per-instance disagreement (`1 - top-5 Jaccard`) to the
corresponding SHAP and LIME fidelity and stability values. Estimate within-run
rank associations and summarize them at the run/seed level. Report this as
association, not prediction or causation. Do not publish pooled fidelity or
stability means from the reused cohort.

## 5. Units, summaries and inference

Instances are nested within runs; some instances recur across the three EXP2
intensities and model families. Instances are the measurement unit, not
independent replicates. First summarize by `(dataset, model, seed, intensity,
method-pair)`. Report matched-instance counts and run-level means or medians.
Use seed-clustered resampling for intervals and keep Adult and EXP3 summaries
separate. There are only five EXP2 seeds and three EXP3 seeds; intervals and
moderator analyses must be interpreted accordingly.

For reproducibility, confidence intervals use 2,000 percentile bootstrap
resamples with RNG seed `20261003`. Resample seed IDs with replacement within
each reporting group, carrying all eligible run-level summaries for each
sampled seed into that replicate. Point estimates are means of eligible
run-level means; report medians as descriptive summaries. If fewer than two
seed units contribute, report the interval as not estimable.

- **RQ1:** report the distribution and seed-clustered 95% confidence interval
  for top-5 Jaccard, Kendall `tau-b` and sign agreement, with counts/coverage.
  These are agreement estimates, not tests against an arbitrary universal
  threshold.
- **RQ2:** report model- and intensity-stratified estimates and uncertainty.
  Treat both moderators as exploratory. The seed counts are too small for
  reliable cluster-level inferential tests, and model families are not a
  random sample of models. Do not treat repeated intensities or models as
  independent seed replicates.
- **RQ3:** within each `(model, seed, intensity)` run, calculate the
  misclassified-minus-correct agreement contrast. Summarize intensity-averaged
  contrasts by `(model, seed)` and report model-stratified estimates, the
  direction across seeds and seed-clustered intervals. Treat these contrasts
  as descriptive/exploratory: five seeds per model in Adult and three in EXP3
  do not support reliable confirmatory inference.
- **RQ4:** calculate within-run Spearman associations between disagreement and
  each explainer's fidelity/stability. Summarize by dataset, model and seed;
  do not pool instances across runs for a nominally large sample size. Treat
  associations as exploratory and report their direction and seed-level
  variability, not causal or predictive conclusions.

No confirmatory hypothesis tests are planned. Do not report p-values for the
moderator, correctness or quality-association analyses. If a later analysis
adds a test, add a dated deviation here before computing it and justify its
independent unit and multiplicity family.

If exclusions, missingness or insufficient matched observations prevent an
analysis, report that limitation instead of substituting an unplanned test.
Any deviations after inspecting results are dated and explained here before
they are included in a paper.

## 6. Quality control and exclusions

Before computing agreement statistics, the analysis must verify:

- JSON parses and each included `raw_top` has unique, known feature names and
  finite values;
- instance IDs are unique within each source run and agree across compared
  methods;
- SHAP/LIME lists are actually ordered by absolute signed contribution;
- Anchor zeros are padding rather than active rule conditions, and DiCE
  nonzeros represent changed features;
- the positive class and prediction-correctness labels agree across methods
  for a given model/instance;
- LIME's new EXP3 cohort has exact target-ID coverage, with no overwrite of
  existing cohorts;
- every exclusion, failed run, empty rule/counterfactual, and matched-instance
  denominator is recorded.

Malformed/non-finite records are excluded only from measures they invalidate,
with counts and reasons. No imputation is used. The primary SHAP–LIME analysis
requires both methods to have a usable explanation for the same instance.
For a correctness contrast, include a run only when at least ten matched
instances remain in each correctness group, following the per-run minimum
used in the Paper D analysis plan. Report all excluded runs and subgroup
counts.

## 7. Reuse, provenance and publication boundary

The EXP2/EXP3 source cohorts were also used in Papers A and B+C. Paper E must
state that provenance and report only the new agreement and association
analyses. The quality metrics in RQ4 are used to estimate new associations;
their cohort-level means and prior method comparisons are not repeated.

Paper D is a different question (correctness-related explanation quality) and
will be cited, not re-analysed. The new EXP3 LIME run is a distinct cohort and
must remain in its own tracked directory. When manuscript claims are drafted,
register every reported result and add Paper E to registry coverage and
exclusivity before building the manuscript.

## 8. Planned reproducible outputs

- New EXP3 LIME per-instance files and a run manifest, kept separate from the
  existing EXP3 aggregate output.
- A deterministic analysis script reading the raw EXP2/EXP3 run JSON and the
  new LIME cohort; it writes tables, diagnostic counts and figure-source CSVs
  under `outputs/analysis/paper_e/analysis/`.
- Outputs include run/group agreement summaries, per-run correctness
  contrasts, seed-level quality associations, explicit row/pairing exclusions,
  and three figures.
- Run inventory and matched-ID audit for every method comparison.
- Tables: agreement by dataset/model/intensity; correct-versus-misclassified
  contrasts; exploratory agreement-quality associations.
- Figures: distribution of top-5 overlap by model and dataset; agreement by
  correctness; exploratory disagreement-quality association plots.

No chart with data labels will be added to a manuscript without a committed
generator. No manuscript or claim-registry entry is in scope until the
analysis is verified and the paper is drafted.

## 9. Deviations

**2026-10-03 (pre-analysis refinement; no Paper E statistic computed).** Schema
inspection showed `raw_top` is capped at ten features, so an Anchors rule with
ten active entries may be truncated; those rows are excluded from full
feature-set comparisons. The correctness-contrast minimum is set at ten
matched instances per group, consistent with the Paper D analysis plan.

**2026-10-03 (execution clarification; before agreement analysis).** EXP3
`.joblib` model and preprocessor binaries are not tracked in the checkout.
Regenerate them in an isolated artifact directory using the checked-in
`train_exp3_models.py` recipe and frozen dependencies. Before generating LIME,
require the regenerated model metadata/configuration, feature order, training
dimensions and metrics to match the committed EXP3 records, and require exact
stored labels and predictions for every target SHAP instance ID. Abort on any
mismatch. Record the regenerated model/preprocessor hashes and source training
summary hash in each run. This validates the reproducible training pipeline
against the stored evidence; it does not claim byte identity with the absent
original binary artifacts.

**2026-10-03 (post hoc; after the prespecified results were inspected).** The
prespecified sign agreement was below one half on Breast Cancer (0.374), the dataset
with the highest top-5 overlap. Inspection showed why: LIME was run with
`discretize_continuous=False`, so its stored value is the coefficient of the local
linear model (a slope), while the SHAP value is a signed contribution relative to the
expected output. Three analyses were added in
`docs/reports/paper_e/scripts/paper_e_posthoc.py`, written to
`outputs/analysis/paper_e/posthoc/`:

1. sign agreement by predicted class, with the section 5 aggregation and bootstrap;
2. sign constancy: for each run and method, and each feature with a nonzero top-10
   value in at least ten paired instances, the share of those instances carrying the
   feature's majority sign (instance-weighted mean over features);
3. a chance reference: the exact expected top-k Jaccard of two independent random
   k-subsets of the p encoded features (p = 108 Adult, 61 German Credit, 30 Breast
   Cancer). It is a reference, not a threshold.

The same script also writes two aggregations of prespecified outputs that the analysis
script left at run level: the Adult agreement margins (per model pooled over intensity,
per intensity pooled over model) and the group summary of the secondary feature-set
overlaps. They use the section 5 procedure unchanged and are not new measures.

Consequence for the paper: the prespecified sign agreement is reported, but it is not
interpreted as disagreement about direction. No prespecified estimate was changed or
removed. The analyses in 1-3 are labelled post hoc wherever they appear.

**2026-10-04 (post hoc; direct test of the 2026-10-03 explanation).** The explanation
above rested on indirect evidence (the split by predicted class and the sign constancy).
The direct test was added in
`docs/reports/paper_e/scripts/paper_e_sign_contribution.py`, written to
`outputs/analysis/paper_e/posthoc/sign_contribution_*.csv`.

- **Conversion.** LIME without discretisation fits its local linear model on
  `z_j = (x_j - m_j) / s_j`, with `m` and `s` the mean and standard deviation of the
  training data given to the explainer. The contribution of feature `j` relative to the
  training mean is `c_j = w_j * z_j`; its sign is `sign(w_j) * sign(x_j - m_j)`. Sign
  agreement is recomputed on the same shared, nonzero top-5 features with the sign of
  `c_j` in place of the sign of `w_j`. A feature whose value equals the training mean has
  no defined contribution sign and is left out (none occurred).
- **Data.** The runs do not store feature values. They are reloaded with the loaders the
  runs used (`load_adult` with the stored Adult preprocessor; `load_tabular_dataset` for
  EXP3), by dataset and seed, and the instance is `X_test[instance_id]`.
- **Alignment checks, made before any statistic.** (a) The stored true label of every
  paired instance equals `y_test[instance_id]`. (b) For EXP3, the SHA-256 of the reloaded
  train and test arrays equals the hash recorded in the Paper E LIME run. A block failing
  a check is excluded and listed in `sign_contribution_checks.csv`. All 86 blocks passed.
- **Internal check.** The script recomputes the slope-based sign agreement on the same
  instances; it reproduces the prespecified values (0.717, 0.511, 0.374).
- **Aggregation.** Section 5 unchanged: mean of run means, seed-clustered percentile
  bootstrap, 2,000 resamples, seed 20261003.
- **Result.** Contribution-based sign agreement: 0.945 Adult, 0.960 German Credit, 0.990
  Breast Cancer, with no dependence on the predicted class and above 0.9 for every model
  family. The explanation of 2026-10-03 is confirmed.
- **Limit.** The reference of `c_j` is the training mean; the SHAP reference is the
  expected output on a 50-instance background sample. They are close, not identical.

**2026-10-04 (corrections to the method description, found by checking the manuscript
against the code; no statistic changed).** (1) The stored "fidelity" is
`FaithfulnessMetric`: the Pearson correlation, across features, between the absolute
attribution and the absolute change in predicted probability when that feature alone is
replaced by its training mean. It is not a surrogate R². RQ4 is therefore an association
with this masking-based fidelity. (2) TreeSHAP ran with `model_output="probability"` and
interventional perturbation, so SHAP and LIME explain the same scale. (3) The Adult
models were trained once on the seed-42 partition; for the other four seeds part of the
explained instances are training data. The manuscript now states all three.

**2026-10-04 (post hoc; in response to the rigor review
`docs/review/scientific-rigor-review_paper_e_2026-10-04.md`).** The review found four
interpretations stronger than the evidence. The analyses below were added to test them.
None changes a prespecified estimate.

*Self-agreement of each method (review F01).* Script
`docs/reports/paper_e/scripts/paper_e_ceiling.py`, outputs
`outputs/analysis/paper_e/posthoc/ceiling_*.csv`.

- Question: what does each explainer reproduce of itself when run again on the same
  instance and model? This, not identity, is the upper reference for SHAP-LIME agreement.
- Sample: a random subsample of the paired instances of each run, drawn with a generator
  seeded by `[20261003, run seed, dataset+model]`. Adult: intensity `n_100` only, 20 instances per run for LR, MLP, RF and XGB; EXP3: 30
  per run. The SVM is left out: KernelSHAP on it took about two minutes per explanation
  (one run of six instances took 23 minutes), and its stored SHAP runs cover 29% of the
  instances. 760 instances in 26 runs.
- Procedure: each instance is explained twice by LIME and twice by SHAP with the
  repository wrappers and the settings of the stored runs. The repetitions differ only in
  the random state (1001 and 2002): LIME's perturbed samples; SHAP's background sample
  and, for KernelSHAP, the coalition sampling (global NumPy generator seeded per
  instance).
- Models: Adult binaries from `experiments/exp1_adult/models/`; EXP3 binaries regenerated
  with `scripts/train_exp3_models.py`, as for the LIME cohort. An instance enters only if
  the loaded model reproduces its stored prediction (none was skipped).
- Measures: the prespecified `primary_agreement` function, between the two repetitions of
  each method, and between the stored SHAP and LIME explanations on the same subsample.
  The script also compares a repetition with the stored explanation of the same method.
- Aggregation: section 5 unchanged.
- Limits: small subsample, one pair of random states, not planned. For the Adult random
  forest the repetition agrees less with the stored SHAP explanation than with the other
  repetition, consistent with the known mismatch between the stored binary and the
  binary that produced the runs.

*Re-cuts of the stored explanations (review F02, F03, F06, F07, F09, F10).* Script
`docs/reports/paper_e/scripts/paper_e_review_analyses.py`, outputs
`outputs/analysis/paper_e/posthoc/review_*.csv`.

1. **Majority-sign baseline (F02).** The sign of every LIME slope is replaced by the
   majority sign of that feature's slope in the same run, then converted and compared
   with SHAP as in the 2026-10-04 direct test. It uses no instance-level information from
   LIME. It reaches the converted agreement (0.951, 0.978, 0.990 against 0.945, 0.960,
   0.990). Consequence: the converted sign agreement shows that the two methods imply the
   same global direction per feature; it is not evidence of agreement on
   instance-specific directions, and the manuscript no longer says "the direct test
   confirms".
2. **Sign-agreement denominator (F10).** Mean number of shared non-zero top-5 features.
3. **Re-ranking by contribution (F07).** LIME's ten stored features re-ordered by
   `|w_j z_j|`; top-5 overlap and Kendall recomputed with `primary_agreement`.
4. **Kendall on shared features only (F06).** `tau_b` on the features present in both
   top-10 lists, with no rank 11 for absent features; instances with fewer than two
   shared features are left out.
5. **Held-out correctness contrast (F03).** An Adult instance is a training row if its
   encoded feature vector equals a row of the seed-42 training matrix (seed 42 itself
   gives 0.1% matches, so false matches are negligible). The RQ3 contrast is recomputed on
   held-out rows, with the same minimum of ten per group, averaged over intensities per
   model and seed.
6. **Coverage (F09).** Paired instances as a share of valid LIME instances, by model.

*Wording changes that follow the review, with no new analysis:* the seed-clustered
intervals are described as the spread of seed means (with three seeds their limits are the
extreme seed means) and are not used as tests; "registered" is replaced by "written and
committed before"; every post hoc analysis is labelled where it appears; the second
companion manuscript (Paper B+C) is named.

