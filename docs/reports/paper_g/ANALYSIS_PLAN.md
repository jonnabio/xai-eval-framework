# Paper G — Analysis and Execution Plan (version 2)

**Question:** Do faithfulness metrics agree on which explanation method is more faithful?
**Title:** *Do Faithfulness Metrics Agree? Metric-Dependent Rankings of Post-hoc Explanations
on Tabular Data* (author, 2026-11-13).
**Status:** Version 2, 2026-11-13, written from the author's decisions of that day (section 9).
Version 1 is in the history of this file. No dataset loaded, no model trained, no explanation
computed for Paper G.
**Lane:** `paper-g` (branch `paper/g-*`, main folder), owning `docs/reports/paper_g/**`,
`experiments/exp_g/**`, `outputs/analysis/paper_g/**`, `docs/planning/paper_g_*`,
`scripts/paper_g_*`, `tests/analysis/test_paper_g_*` (`scripts/pubs/lanes.toml`, PR #116).
**Venue:** *Informática y Sistemas* (`VENUE.md`).

---

## 1. What the study is

Benchmarks of explanation methods name a "more faithful" method from one faithfulness
metric, usually chosen by convention. Several metrics exist, and each operationalises
"faithful" differently: deletion, insertion, masking a top set, correlation with single-feature
removal, infidelity under perturbation, sufficiency and comprehensiveness. If these metrics
order the same explainers differently, a conclusion of the form "A is more faithful than B"
depends on the metric chosen, not only on A and B.

The study measures that agreement directly, at two levels:

- **System level:** do the metrics give the same *order of explainers* in each dataset and model?
- **Instance level:** do the metrics agree on *which individual explanations* are good?

It is not a study of which explainer is best. The order of the explainers is an input to the
agreement analysis, and is reported only to make the agreement readable.

## 2. Design

**8 datasets × 4 models × 4 explainers × 7 metrics (M7 system level only), 5 seeds, 200 instances;
plus a synthetic ground-truth check (section 2.5).**

### 2.1 Datasets

Eight public binary tabular datasets from OpenML, two per stratum of feature composition,
loaded with the existing Paper F loader (code reused; no Paper F result is reused or printed).
Confirmed by the author on 2026-11-13:

| Stratum | Datasets |
|---|---|
| Numeric, small | phoneme, qsar-biodeg |
| Numeric, large | MagicTelescope, electricity |
| Mixed | credit-g (German Credit), adult |
| Mixed / categorical | bank-marketing, compas-two-years |

Rule: the list is fixed and committed (`outputs/analysis/paper_g/datasets.csv`) before any
explanation is computed. Gate: cross-validated AUC between 0.65 and 0.98 for at least two of
the three models; a dataset that fails is replaced by the next of its stratum from the Paper F
candidate pool, and the replacement is recorded.

### 2.2 Models

Logistic regression (L2), random forest, XGBoost, multilayer perceptron. One configuration per
model for all datasets, committed before training. Preprocessing: standard scaling, one-hot
encoding, median or mode imputation. Split 80/20, stratified, by seed. The MLP was kept (author,
2026-11-13): it adds about 2 to 4 hours of machine time, estimated from Paper F timings.

### 2.3 Explainers (the four items that are ranked)

| Explainer | Role |
|---|---|
| SHAP (TreeSHAP for trees, KernelSHAP for logistic regression and MLP) | studied |
| LIME | studied |
| Occlusion (leave-one-feature-out with baseline replacement) | studied; also a known circularity check (section 3.2) |
| Random attribution (seeded Gaussian scores) | negative control: every metric must rank it last |

Four items is the minimum that makes a rank order informative. The random control gives a
sanity check that each metric works at all.

### 2.4 Seeds and instances

Seeds 42, 123, 456, 789, 101112. A seed fixes the split, the model, explainer sampling and
the random control. 200 test instances per dataset, model and seed, stratified by predicted
class. All explainers explain the same instances; all metrics score the same explanations.

### 2.5 Synthetic ground-truth check (light version, author 2026-11-13)

Known functions are used directly as the model, so the true attribution is exact and no
trained model stands between the data and the truth.

- Generators: (a) additive logistic model; (b) additive model with two pairwise interactions.
- Features: 8 standard normal features, (i) independent and (ii) correlated (pairwise 0.5).
- Four generator conditions × 5 seeds × 200 instances; the same four explainers and M1 to M6.
- Ground truth: exact interventional Shapley values with the same baseline the metrics use
  (closed form for the additive case; exact enumeration over 8 features otherwise).
- Outcome: the error of each explainer against the truth (Spearman correlation of attribution
  ranks); the order of explainers by true error is the reference. Each metric is scored by its
  rank agreement with that reference.
- Cost: about 3 working days of code; minutes of compute.

## 3. Metrics (the "raters")

All metrics act on the same explanation vector and the same baseline (training mean for
numeric features, mode for categorical; one-hot groups masked together as one raw feature).

| ID | Metric | Direction | Definition (to be fixed in code with tests) |
|---|---|---|---|
| M1 | Deletion AUC | lower is better | area under predicted-class probability as features are removed in attribution order |
| M2 | Insertion AUC | higher is better | area under probability as features are added to the baseline in attribution order |
| M3 | Top-k prediction gap | higher is better | drop in probability when the top 20% of features (at least one) are masked |
| M4 | Faithfulness correlation | higher is better | Pearson correlation between attribution and single-feature masking drop |
| M5 | Infidelity | lower is better | over 100 random subsets S of features (each masked with probability 0.5): 1 − R² of the no-intercept fit of f(x) − f(x masked on S) on the summed attributions of S (scale-free; section 10) |
| M6 | Sufficiency | lower is better | probability change when only the top 20% of features are kept |

Comprehensiveness is the same quantity as M3 and is not counted twice.

**M7 — ROAR-lite** (included, author 2026-11-13). Global ranking of each explainer = mean
|attribution| over its 200 instances. The model is retrained without the top 10, 20, 30 and 50%
of features of that ranking (at least one), and the drop in test AUC is averaged over the four
levels; a larger drop is better. 2,560 retrainings, about 4 to 6 hours wall time with 8 jobs.
System level only: it enters H1, not H2.

### 3.1 Baseline sensitivity

Every masking metric depends on the replacement value. As a secondary factor, M1 to M3 and M6
are recomputed with a second baseline (random draw from training rows). This shows how much of
the disagreement comes from the baseline, not from the metric.

### 3.2 Known circularity

M4 and Occlusion are built from the same single-feature removal, so M4 is expected to favour
Occlusion. The analysis is reported with and without the Occlusion–M4 combination.

## 4. Analysis

**Level.** For the system level, one mean per dataset, model, explainer, seed and metric:
8 × 4 × 4 × 5 = 640 means per metric. Instances never count as independent evidence about
datasets.

### 4.1 Primary analysis: system-level agreement (H1)

For each dataset × model × seed block: rank the four explainers under each of the six metrics.
Treat metrics (M1 to M7) as raters and explainers as items.

1. **Estimate:** Kendall's W across the six metrics, per block; reported as the mean over
   blocks and as the mean pairwise Spearman correlation between metrics, (mW − 1)/(m − 1).
2. **Interval:** 95% t-interval on the eight dataset means (each dataset mean is the mean of
   its 20 blocks), 7 degrees of freedom. The percentile bootstrap over datasets is reported as
   a sensitivity analysis only (section 4.5).
3. **Test:** permutation test of "metrics order explainers independently", **with the dataset
   as the unit**: for each dataset and metric, one permutation of the explainer labels is
   applied to all 20 blocks of that dataset; 100,000 permutations, one-sided. The one-sided
   t-test on the dataset means is reported as a sensitivity analysis.
4. **Ceiling:** agreement of *one metric with itself* across the five seeds. Agreement between
   metrics is read against this ceiling.
5. **Without the random control:** repeated with the three studied explainers, because the
   control inflates W (every metric should put it last).

### 4.2 Primary analysis: instance-level agreement (H2)

For each dataset × model × explainer × seed: Spearman correlation between every pair of metrics
across the 200 instances (15 pairs). Summary: the mean over datasets, with a bootstrap interval
over datasets, per pair. Output: a 6 × 6 agreement matrix.

### 4.3 Secondary analyses

1. **Winner flips:** share of blocks in which the top-ranked studied explainer differs between
   two metrics; pairwise matrix.
2. **Which pairs of metrics disagree, and how often the SHAP–LIME order reverses** under a
   change of metric (the comparison most papers make).
3. **Variance shares** of the explainer ranks: metric, dataset, model, metric × explainer.
   Linear mixed model with dataset random; aligned rank transform as sensitivity.
4. **Baseline effect:** H1 repeated under the second baseline (section 3.1).
5. **Per model.**

### 4.4 Hypotheses and decision rule (fixed before the run)

- **H1:** across faithfulness metrics, the order of the explainers agrees more than chance.
- **H2:** across instances, pairs of faithfulness metrics correlate positively.

For H1, with the permutation p and the 95% interval of the mean pairwise Spearman correlation
between metrics (studied explainers only):

| Outcome | Wording |
|---|---|
| p ≥ 0.05 | no evidence that the metrics share an order |
| p < 0.05, interval above 0.5 | the metrics broadly agree |
| p < 0.05, interval below 0.5 | the metrics agree only weakly |
| p < 0.05, interval contains 0.5 | agreement present, strength not determined |

The threshold 0.5 and the decision table are those of Paper F, kept for consistency. A power
simulation (`scripts/paper_g_power_simulation.py`) is run before the full run to check that
eight datasets give useful precision; if not, the author decides between more datasets and a
weaker claim.

Holm correction over H1 and H2 (and over metric pairs in 4.2 when tested). The interval of
the decision rule is the t-interval of section 4.1.

### 4.5 Power and precision (`scripts/paper_g_power_simulation.py`, run 2026-11-13)

Simulation of the H1 design (7 metrics, 3 studied explainers, 20 blocks per dataset), 1,000
studies per condition, with dataset-level disagreement making up 20%, 50% or 80% of the
noise (h). Output: `outputs/analysis/paper_g/power_simulation.csv`. With eight datasets:

| h | Width of the 95% t-interval (true agreement 0.2 / 0.5 / 0.8) | Coverage of the t-interval | Size of the t-test (true 0) | Power at a true 0.2 |
|---|---|---|---|---|
| 0.2 | 0.15 / 0.14 / 0.08 | 0.94 to 0.95 | 0.03 | 1.00 |
| 0.5 | 0.22 / 0.22 / 0.12 | 0.91 to 0.95 | 0.02 | 1.00 |
| 0.8 | 0.29 / 0.30 / 0.18 | 0.91 to 0.95 | 0.02 | 0.92 |

**Conclusion: eight datasets are enough.** Any non-trivial agreement is detected, and an
interval of about ±0.07 to ±0.15 separates the outcomes of the decision rule unless the true
value is near 0.5. Twelve datasets would narrow the interval by about a quarter; not needed.

**Two changes made before the run because of the simulation** (they replace the version 2
wording of section 4.1):

1. A permutation test that permutes ranks independently **in each block** is invalid here:
   with true agreement 0 and strong dataset-level disagreement (h = 0.8) it rejected in 13%
   of studies at a nominal 5%, because the 20 blocks of a dataset are not independent. The
   permutation unit is therefore the dataset.
2. The percentile bootstrap over eight datasets covered the true value in only 86% to 90% of
   studies. The t-interval on dataset means covered it in 91% to 95%, and is the primary
   interval. The bootstrap stays as a sensitivity analysis.

## 5. What is not done

- No claim about which explainer is best in general.
- No claim about which metric is "correct". Disagreement is reported as a property of the
  measurement, not resolved by choosing a winner.
- No result of Papers A to F is printed. The SHAP and LIME values of Paper G come from its own run.
- Ground truth exists only in the synthetic check (section 2.5); on real data the study
  measures agreement, not correctness.

## 6. Order of work (BMAD)

| Step | Work | Output | Estimate |
|---|---|---|---|
| 1 | Author reviews this plan and the draft; decisions of section 9 | approved plan | author |
| 2 | Configuration file; power simulation | `experiments/exp_g/config.toml`, `scripts/paper_g_power_simulation.py` | 1–2 days |
| 3 | Metric code M1–M7 and synthetic generators with exact Shapley values, with unit tests on toy models where the answer is known | `scripts/paper_g_metrics.py`, `scripts/paper_g_synthetic.py`, `tests/analysis/test_paper_g_*.py` | 9–11 days |
| 4 | Dataset gate and `datasets.csv` committed | `outputs/analysis/paper_g/datasets.csv` | 1 day |
| 5 | Pilot: 1 dataset, 3 models, 1 seed, 20 instances; time and failure check; outputs deleted | timing note | 1–2 days |
| 6 | Full run on the **Linux run host**, resumable shards, progress and logs pushed to `paper/g-runs` (`RUN_PROTOCOL.md`) | `outputs/analysis/paper_g/raw/`, `STATUS.md` | about 1–2 days machine time (re-estimated without Anchors and DiCE; pilot to confirm) |
| 7 | Analysis script; figures by committed generators; registry entries | `scripts/paper_g_analyze.py`, `RESULTS_REPORT.md` | 3–4 days |
| 8 | References: search, DOI verification, ≥ 80% from 2024 or later | `reference_records.json` | 3–4 days, parallel to 6 |
| 9 | Assistant writes results and discussion into the draft; author decides content; journal .docx template | `paper_g.docx` | 3–5 days + author review |
| 10 | Scientific-rigor review and reference audit (Scientific Advisor) | `docs/review/…paper_g…` | 2 days |
| 11 | Anonymise; declarations; similarity and AI-content check; Zenodo release | submission package | 2 days |

Earliest submission: late December 2026 or early January 2027.

## 7. Risks

| Risk | Mitigation |
|---|---|
| Kendall W with four items is coarse | instance-level analysis (H2) carries most of the information; ranks reported with ties |
| Random control inflates agreement | primary estimate uses the three studied explainers only |
| Occlusion–M4 circularity | reported with and without that combination |
| Masking baseline drives the result | second baseline as a secondary factor |
| ROAR-lite too slow | timed in the pilot; levels reduced from four to two if needed |
| Overlap with Papers B, E, F | own run; the paper cites them as prior work and prints none of their values |
| Journal limit of 30% AI-generated text | owned and managed by the author (decision 2026-11-13) |

## 8. Possible extension (not in version 2)

Full synthetic study: more generator families, higher dimension, sensitivity to the correlation
level. About one more week. Only if reviewers ask.

## 9. Decisions of the author (2026-11-13)

1. The eight datasets of section 2.1: confirmed.
2. MLP: kept (cost about 2 to 4 hours of machine time).
3. ROAR-lite (M7): included (about 3 days added).
4. Synthetic ground-truth check: light version (section 2.5; about 3 days).
5. Title: *Do Faithfulness Metrics Agree? Metric-Dependent Rankings of Post-hoc Explanations
   on Tabular Data*.

## 10. Changes made before the run

Logged here with date and reason. None was made after any result was seen.

| Date | Change | Reason |
|---|---|---|
| 2026-11-13 | Primary interval: t-interval on dataset means; permutation unit: dataset (section 4.5) | power simulation: block-level permutation anti-conservative, bootstrap undercovers |
| 2026-11-14 | M5 infidelity: random subset masking instead of Gaussian noise, scored as 1 − R² of the optimally scaled fit | Gaussian noise is undefined for categorical features; raw infidelity depends on the scale of the attributions, which differs between LIME and SHAP, so it would partly rank scale |
| 2026-11-14 | Removal metrics (M1–M3, M6) order features by their attribution toward the predicted class, largest first, ties by index; attributions are summed per raw feature and oriented to the predicted class | fixes the definition of "top" for signed attributions; one-hot columns of a feature are masked together |
| 2026-11-14 | KernelSHAP with `l1_reg = false` | the default feature selection left 12 of 20 features at zero in the smoke test, which would truncate SHAP's ranking for logistic regression and the MLP only |
| 2026-11-14 | Synthetic ground truth: exact interventional Shapley values with the expectation over 500 background rows of the same distribution | standard definition of SHAP values; independent of the metrics' single-point baseline |
| 2026-11-14 | Machine-time estimate: smoke test on the documentation laptop gave 0.01–0.2 s per instance and explainer, metrics included; MLP training up to about 40 s (Adult). The full stage is a few CPU hours; ROAR-lite is dominated by MLP refits. Expected well under one day with 6 jobs; the pilot on the run host gives the figure | |

## 11. Post-execution, pre-unblinding analysis clarifications and deviations

Recorded **2026-11-16 00:40 UTC**, after all four stages finished (run frozen at `04c6dfd84`,
merged into `main` by PR #123) and **before any scientific result was seen**. Decisions A to G
were accepted by the author on 2026-11-16 (Task 13). Sections 1 to 10 above are kept unchanged:
where they are ambiguous or contradict each other, the original wording is quoted here and
the resolution is stated. Nothing in this section is preregistered in the sense of section 10.

**What had been seen before these decisions:** shard, row and failure counts; timings, memory
and temperatures; hashes; field names; whether a field was present, null, non-finite or flagged
(147 rows flagged `m4_degenerate`); and the consistency of `true_attr` across explainers. No
faithfulness metric value, attribution value, model score, agreement statistic or explainer
order was displayed, computed or summarised.

Classes used below: **C** clarification of preregistered intent; **M** post-execution
methodological amendment; **S** exploratory or sensitivity analysis; **D** protocol deviation.

### 11.1 Decision A: dataset eligibility gate (class D, with a diagnostic)

- **Original (section 2.1, step 4 of section 6):** "the list is fixed and committed
  (`outputs/analysis/paper_g/datasets.csv`) before any explanation is computed. Gate:
  cross-validated AUC between 0.65 and 0.98 for at least two of the three models".
- **What happened:** the gate was never implemented or run; no `datasets.csv` exists; the run
  used the eight datasets confirmed by the author on 2026-11-13. The wording "three models" is
  out of date (four models since version 2; `config.toml` `[rule] min_models_in_range = 2`).
- **Resolution:** the gate is run now as a **retrospective diagnostic**. Procedure, inherited
  unchanged from the Paper F gate (`scripts/paper_f_datasets.py`, `cv_auc`, whose loader the
  plan says Paper G reuses), with the values of `config.toml` `[rule]`:
  1. the stratified 80/20 split of `gate_seed` = 42 with the frozen preprocessing (`lib.split`);
  2. on its training part, `StratifiedKFold(5, shuffle=True, random_state=42)`;
  3. each of the four models built by `lib.make_model(model, 42, cfg)` and fitted on each fold;
  4. the AUC on the held-out fold; the mean over the five folds;
  5. a model is in range if 0.65 <= mean AUC <= 0.98 (inclusive, as in Paper F); a dataset
     passes if at least 2 of the 4 models are in range.
  Known property of the inherited procedure: the preprocessing is fitted on the whole training
  part before the folds, so each validation fold has seen the scaler and encoder (the same as
  Paper F). It is kept, so as not to choose a variant that could change eligibility.
- **All eight datasets stay in the study whatever the outcome.** A failing dataset is recorded,
  kept, and reported with its implications; any analysis without it is exploratory.
- **Outputs:** `outputs/analysis/paper_g/diagnostics/dataset_gate.csv` (kept apart from the
  confirmatory outputs). The diagnostic computes model AUCs only; it reads no run output.
- **Changes estimand, test or population:** no.
- **Justification:** the gate guards against datasets on which the models are trivial or near
  chance; running it late shows whether that risk occurred, without letting the result alter the
  study.

### 11.2 Decision B: seven metrics in H1 (class C)

- **Original:** section 4.1 says "rank the four explainers under each of the six metrics" and
  "Kendall's W across the six metrics", but also "Treat metrics (M1 to M7) as raters"; section
  3 says M7 "enters H1"; the power simulation (section 4.5) used seven metrics; the draft speaks
  of a "6 × 6" heat map for H1.
- **Resolution:** H1 uses **seven raters, M1 to M7**. M1 to M6 enter as the mean over the 200
  instances of the block; M7 is the block's single ROAR-lite value (`m7_roar`), never treated as
  an instance-level metric. The **primary H1 population is the three studied explainers** (SHAP,
  LIME, Occlusion), as section 4.4 states for the decision rule; the four-explainer analysis
  (with the random control) is the planned sensitivity of section 4.1 item 5.
- **Changes estimand:** no; it fixes which of two conflicting texts holds, choosing the one the
  power simulation and section 3 use.

### 11.3 Decision C: within-metric stability benchmark and ties (class C for ties, M for the benchmark)

- **Original:** section 4.1 item 4, "Ceiling: agreement of one metric with itself across the
  five seeds", without an operational definition; ties not specified (section 7: "ranks reported
  with ties").
- **Ties:** explainers are ranked with **average ranks**; Kendall's W uses the tie-corrected
  form W = 12 S / (m²(n³ − n) − m Σ_j T_j), T_j = Σ (t³ − t) over the tie groups of rater j.
- **Mean pairwise Spearman** is computed directly as the mean of the Spearman correlations of
  all rater pairs, not derived from W.
- **Undefined values:** a Spearman correlation is undefined when either rank vector is constant
  (all items tied); W is undefined when its denominator is 0. **An undefined value is never
  replaced by 0**: it is left out of the mean it would enter (the mean over the defined values),
  and the number of undefined values is reported with every summary. A block whose statistic is
  undefined for all pairs is reported and left out of its dataset mean.
- **Benchmark:** for each dataset × model × metric, the three studied explainers are ranked in
  each of the five seeds; the Spearman correlation of every unordered pair of seeds (10 pairs) is
  computed; these are averaged within dataset × model × metric, then over the four models, then
  over the seven metrics, giving one value per dataset; the eight dataset values give the overall
  mean and a t-interval. Dataset-level and metric-specific values are reported.
- It is called a **within-metric stability benchmark**, not a ceiling: different seeds change
  the split, the fitted model and the explainers' sampling, so cross-seed variation is not
  measurement error alone, and between-metric agreement is not bounded by it mathematically.
- **Changes estimand:** the benchmark is newly operationalised (M); the tie and undefined-value
  rules fix behaviour the plan left open (C).

### 11.4 Decision D: degenerate M4 observations (primary class C; sensitivity class S)

- **Evidence:** 147 of the 128,000 full-stage rows have `m4_degenerate = true`; for them the
  metric code (`correlation_metric`) stores M4 = 0.0 (when the attribution or the single-feature
  drops are constant). The plan does not mention the case.
- **Primary:** M4 is used **exactly as generated** (0.0 retained).
- **Exploratory sensitivity:** flagged rows are left out of every computation involving M4 and
  of nothing else. H1: the M4 block mean is recomputed over the valid rows; if a block has no
  valid row for an explainer, the M4 aggregate is **missing** (not 0) and the M4 rater is left
  out of that block (pairs with M4 undefined, W over the remaining raters). H2: correlations for
  pairs with M4 are pairwise-complete (flagged instances dropped from those pairs only). Counts by
  dataset, model and explainer, the rows remaining per affected correlation and any undefined
  correlation are reported. Class S, because the exclusion rule was set after the run.

### 11.5 Decision E: H2 inference (class M)

- **Original:** section 4.2 gives the estimate (15 metric-pair Spearman correlations per dataset ×
  model × explainer × seed, mean over datasets, a 6 × 6 matrix) and "a bootstrap interval over
  datasets", but no test, although section 4.4 asks for a Holm correction over H1 and H2; and
  section 4.5 found the bootstrap over eight datasets undercovers.
- **Orientation (class C):** before correlating, every metric is oriented so that higher means
  more faithful (M1, M5, M6 multiplied by −1; section 3 directions). H2 asks whether metrics agree
  on *which explanations are good*; on raw values M1 and M2 correlate negatively when they agree.
- **Population:** all four explainers (the plan's instance-level design); the three studied
  explainers as a sensitivity.
- **Omnibus statistic:** the mean of the 15 correlations in each block; the mean of the blocks of
  each dataset (80 blocks: 4 models × 4 explainers × 5 seeds); eight dataset values; their mean.
  Instances are never units of inference.
- **Test (primary for the Holm family of section 4.4):** one-sided one-sample t-test on the eight
  dataset values, H0: mean ≤ 0, H1: mean > 0; 95% t-interval with 7 degrees of freedom.
- **Supplementary:** exact sign-flip test over the 2^8 = 256 sign assignments of the dataset
  values, p = share of assignments whose mean is at least the observed mean. It assumes that,
  under H0, each dataset value is symmetric about 0; it is not distribution-free under arbitrary
  heterogeneity between datasets.
- **Pairs:** for each of the 15 pairs, the same dataset-level estimate, t-interval and one-sided
  t-test; **Holm over the 15 pair tests** (a family separate from the H1/H2 family).
- **Sensitivity:** the planned percentile bootstrap over datasets (10,000 resamples, fixed seed),
  for the omnibus and the pairs. It never replaces the t-interval.

### 11.6 Decision F: synthetic ground-truth agreement (class M for the statistic)

- **Original:** section 2.5, "the order of explainers by true error is the reference. Each metric
  is scored by its rank agreement with that reference", without the statistic.
- **Resolution:** in each condition × seed block (4 × 5 = 20): the reference score of an explainer
  is the mean of `spearman_truth` over the 200 instances (higher is better); each metric M1 to M6 is
  averaged over the same instances and oriented; explainers are ranked (average ranks) under the
  reference and under each metric; the agreement is the Spearman correlation of the two rank
  vectors (undefined values handled as in 11.3). Primary population: all four explainers;
  sensitivity: the three studied explainers. Reported per metric, per condition, per seed, with
  the reference order of every block. Descriptive only: no test was planned and none is added.
  All four conditions are reported; none is selected.

### 11.7 Decision G: aligned rank transform and the variance shares (class D)

- **Original:** section 4.3 item 3, "Variance shares of the explainer ranks: metric, dataset,
  model, metric × explainer. Linear mixed model with dataset random; aligned rank transform as
  sensitivity."
- **Finding:** as specified, the decomposition is **not identifiable**. In every block and metric
  the ranks of the three explainers are a permutation of {1, 2, 3} (or average ranks with the same
  sum), so their mean is 2 by construction: the main effects of metric, dataset and model on the
  ranks are identically zero, and their "shares" are zero by design, not by data. Only terms that
  involve the explainer factor (explainer; explainer × metric; explainer × dataset; explainer ×
  model) can carry variance, and the plan does not say which response, terms or variance-share
  definition (marginal R², variance components, ICC) are meant.
- **Resolution:** the variance-share component is **stopped, not implemented**, and reported as a
  deviation; it needs an author-approved specification before it can be added. The aligned rank
  transform is **omitted**: no ART package is installed, adding one needs approval, and an
  unvalidated implementation would not be ART. No other method is substituted.

### 11.8 Open items that need the author's approval before the real-data run

The analysis script refuses to run while these are unset (`experiments/exp_g/analysis.toml`).

1. **H1 decision table and Holm (O1).** Section 4.4 writes the decision table on "the permutation
   p" and, separately, "Holm correction over H1 and H2". The plan does not say whether the table's
   "p < 0.05" is the raw permutation p or the Holm-adjusted p. Both are computed and reported; the
   author chooses which one the table uses (`h1_decision_p = "raw"` or `"holm"`).
2. **Occlusion–M4 circularity estimand (O2).** Section 3.2: "reported with and without the
   Occlusion–M4 combination". Removing one rater × item cell leaves an incomplete rank matrix, for
   which ordinary Kendall's W is undefined. Two valid estimands are implemented; the author
   chooses (`circularity_variant`):
   - `drop_m4_rater`: H1 with the six raters M1 to M3 and M5 to M7 over the three studied explainers
     (complete matrix; W and the mean pairwise Spearman are well defined; removes more than the one
     cell);
   - `pairwise_available`: the mean pairwise Spearman over all 21 rater pairs, where pairs with M4
     use only SHAP and LIME (two items: +1 or −1, undefined if tied); W is not reported for it,
     and no permutation test is computed for it (the relabelling scheme of 4.5 assumes a complete
     matrix); its estimate and t-interval are reported.
3. **Variance shares (O3):** stopped (11.7) until a specification is approved.

### 11.9 Rules common to all analyses (class C)

- Direction (section 3): higher is better for M2, M3, M4, M7; lower for M1, M5, M6. Rank 1 is the
  most faithful explainer under a metric.
- The pilot is excluded from every analysis.
- Fixed seeds: permutation test 20261116; bootstrap 20261117. 100,000 permutations; Monte Carlo
  p = (1 + number of permuted statistics ≥ observed) / (1 + 100,000), never 0.
- The H1 permutation statistic is the decision measure: the mean over datasets of the dataset
  mean of the block mean pairwise Spearman (three studied explainers, seven raters).
- Winner flips: a block's winner under a metric is the explainer of rank 1; if the top is tied the
  block is counted as a tie for every pair with that metric, not as a flip. SHAP–LIME: in a block,
  the sign of (oriented SHAP − oriented LIME) under each metric; a pair of metrics is a strict
  reversal if the signs are opposite and non-zero, tie-involved if either is zero.
- Per-model summaries are descriptive (estimate and t-interval over the eight datasets, no test).
- Outputs: `outputs/analysis/paper_g/analysis/` with `confirmatory/`, `sensitivity/`,
  `exploratory/`, `synthetic/`, `figures/`; the report is `docs/reports/paper_g/RESULTS_REPORT.md`,
  generated, never hand-edited.

### 11.10 Record after the decisions (2026-11-16)

- **Dataset gate (11.1), run 2026-11-16 at commit `b993f434d` + script
  `scripts/paper_g_dataset_gate.py`:** all eight datasets pass; in every dataset all four models
  have a mean five-fold AUC inside [0.65, 0.98] (lowest: compas, random forest; highest:
  electricity, random forest). The OpenML files used are byte-identical to those of the run.
  Output: `outputs/analysis/paper_g/diagnostics/dataset_gate.csv`. The deviation (gate run after
  the experiment, not before) stands; the eligibility condition itself is met, so no dataset
  carries an eligibility caveat.
- **Implementation:** `scripts/paper_g_analyze.py` with `tests/analysis/test_paper_g_analyze.py`
  (constructed data only). Planned claims: `docs/reports/paper_g/CLAIMS_PLAN.toml` (RCA-001;
  not registered until the authorized run).
- **Structural validation of the frozen data** (`paper_g_analyze.py --validate-only`): manifest
  hashes and coverage, row counts, keys, instance alignment across explainers, ROAR-lite block
  alignment. Counts only (344 shards; 128,000, 640 and 16,000 rows; 147 degenerate-M4 flags); no
  statistic computed, no analysis output written.
- **The real-data analysis has not been run.** It needs the author's choices on O1 and O2 in
  `experiments/exp_g/analysis.toml` and an explicit authorization (`--authorized`).

### 11.11 Final decisions on the open items (author, 2026-11-16; Task 14)

Recorded before any scientific result was seen; no analysis had been run on the frozen data.

- **O1, H1 decision table (class C).** The four-outcome classification of section 4.4 uses the
  **raw permutation p** and the 95% t-interval of the dataset means, as written before the run.
  Holm-adjusted p-values over the family {H1, H2} are reported beside it. The manuscript keeps
  the two apart: the preregistered classification, and the multiplicity-adjusted inferential
  conclusion. If they differ, both are reported. (`analysis.toml` `h1_decision_p = "raw"`.)
- **O2, Occlusion–M4 sensitivity (class S).** The primary H1 keeps all seven metrics. The
  circularity sensitivity **removes M4 for every explainer**, leaving six complete rankings
  (M1 to M3, M5 to M7) of the three studied explainers; Kendall's W, the mean pairwise Spearman,
  the t-interval and the dataset-unit permutation test (same scheme, seed and number of
  permutations as the primary) are recomputed on that six-metric matrix. Because it removes more
  than the occlusion–M4 cell, a change against the primary **does not isolate** the effect of
  the occlusion–M4 overlap; it shows only whether the H1 conclusion depends on M4.
  (`circularity_variant = "drop_m4_rater"`.)
- **O3, variance shares (class D).** The variance-share decomposition and the aligned rank
  transform of section 4.3 item 3 are **omitted**. The planned decomposition lacks a sufficiently
  defensible operational specification: its main-effect terms of metric, dataset and model on
  the ranks are zero by construction (11.7), and the plan does not fix the response, the terms
  involving the explainer factor, or the definition of a share. This does not mean that every
  rank-based interaction analysis is impossible; any replacement would be proposed separately
  and reported as exploratory. No variance-share output is produced. (`[variance] status =
  "OMITTED"`.)

The specification is frozen with these decisions. The analysis still runs only with an explicit
authorization (`--authorized`).

## 12. Post-analysis supplementary LIME validation and exploratory diagnostics

Written **2026-11-16**, after the single authorized analysis (PR #129, merged as `ae8fccf04`) and
after the post-analysis quality review (PR #130, `e466c2a4e`), on the author's authorization of the
same day (Task 17, Scenario C). Sections 1 to 11 are unchanged.

- The original analysis was completed before this investigation; its outputs
  (`outputs/analysis/paper_g/analysis/`, `RESULTS_REPORT.md`) are frozen historical evidence.
- The LIME representation mismatch was found by the post-analysis review
  (`PAPER_G_POST_ANALYSIS_QUALITY_REVIEW.md`, section 2): with `discretize_continuous=False`, LIME
  stores surrogate slopes, while M1 to M6 and the synthetic truth assume signed contributions.
- Everything in this section is **supplementary and exploratory**. It does not replace the
  confirmatory experiment, cannot change H1 or H2 retroactively, and is written to separate output
  paths with its own provenance. It is written after the results of sections 4 and 11 were seen.

### 12.1 S3: focused synthetic validation of LIME representations

**Question.** Under the existing synthetic conditions, do alternative LIME output representations
recover the known contributions (the stored exact interventional Shapley values) more faithfully than
the frozen slopes?

**Conditions, data and truth (unchanged).** The four conditions of section 2.5 (additive and
interaction generators × correlation 0 and 0.5), seeds 42, 123, 456, 789, 101112, rebuilt with the
frozen `paper_g_synthetic.make_condition(generator, rho, seed, cfg)`; the same 200 instances
(`data["instances"]`); the truth is the stored `true_attr` of the synthetic shards (never recomputed
or changed). All 8 features are numeric; no categorical column exists.

**Reproduction gate (before any new representation is computed).** For every instance, the frozen
LIME (`paper_g_lib.make_explainer("lime", model, data, seed, cfg)`, the same per-instance seed
`(seed · 100003 + pos) mod 2^31`, oriented by `orient` and rounded to 8 decimals) must reproduce the
stored `attr` to within 1e-8 in every component. If any instance fails, S3 stops and is reported; no
representation is computed on a block that does not reproduce. In the same gate, the exact
Shapley values of the first instance of every block are recomputed with the frozen
`true_attribution` and must equal the stored `true_attr` to within 1e-6 (a check of the rebuilt
condition only; the stored truth remains the reference).

**LIME configurations (a 2 × 2 design, so that each change is isolated).** All other settings as in
`paper_g_lib.Lime` (1,000 samples, all features, `labels=(1,)`, explainer `random_state` = shard seed,
per-instance seed as above, quartile discretizer where discretisation is on):

| Config | `discretize_continuous` | kernel width |
|---|---|---|
| F3 (frozen) | False | 3.0 |
| FD | False | package default, 0.75·sqrt(8) ≈ 2.121 |
| T3 | True | 3.0 |
| TD | True | package default |

**Representations (all oriented to the predicted class with `orient`, as in the frozen pipeline).**

| Id | Representation | Definition |
|---|---|---|
| S3-A | slopes, frozen | the stored `attr` (F3) |
| S3-A-kd | slopes, default width | weights of FD |
| S3-B | reference-relative contributions | `c_j = w_j · (x_j − μ_j) / s_j` with `w` the F3 weights and `μ`, `s` the explainer's own fitted `scaler.mean_` and `scaler.scale_` |
| S3-B-kd | same, default width | from FD |
| S3-C | discretised weights | weights of T3 (indicator of the instance's quartile bin) |
| S3-C-kd | discretised, default width | weights of TD |

Isolated comparisons: kernel width within each family (A vs A-kd, B vs B-kd, C vs C-kd);
discretisation at fixed width (A vs C, A-kd vs C-kd); the transformation at fixed fit (A vs B,
A-kd vs B-kd). No conclusion attributes a difference to one factor when two changed.

**Assumptions and limits of S3-B.** `c_j` is the exact additive decomposition, relative to the
training mean `μ`, of LIME's own linear surrogate; it equals the model's contributions only where the
surrogate equals the model (exactly for a linear model). LIME fits the surrogate on samples drawn
around `μ`, weighted toward the instance, so `w` is a smoothed slope. The truth uses a different
reference: the expectation over a 500-row background of the same distribution, not the single point
`μ`, and it is computed for the probability, which is nonlinear in the features. S3-C's weights are
effects of the instance's quartile indicators; they are not claimed to be Shapley-equivalent.

**Reference check.** For each condition × seed: `max_j |μ_j − mean of truth_background_j|` and
`max_j |μ_j − base_j|` (the metrics' baseline), to show how far the references differ.

**Primary supplementary diagnostic.** For each condition × seed × representation and each of the 200
instances: Spearman correlation (`scipy.stats.spearmanr`) between the 8-vector representation and the
stored `true_attr`; undefined (either vector constant) is left out and counted, never set to 0. The
instance values are averaged per condition × seed × representation (120 values); reported per
condition and seed, per condition (mean over seeds, with minimum and maximum), and split by predicted
class. No global mean across conditions is reported on its own.

**Expected records.** 4,000 reproduction rows; 24,000 instance rows (4,000 × 6 representations).

**Rules.** Descriptive only; no test; no representation is selected as a new primary LIME output;
all values are reported, including unfavourable ones. S3 may inform the design of S1 or S2; that
would be a separate, adaptive, post-analysis decision.

**Outputs.** `outputs/analysis/paper_g/supplementary/s3/` (`s3_reproduction.csv`,
`s3_instances.csv.gz`, `s3_condition_seed.csv`, `s3_condition.csv`, `s3_by_class.csv`,
`s3_reference.csv`, `s3_provenance.json`) and the generated `docs/reports/paper_g/S3_REPORT.md`.
Code: `scripts/paper_g_s3_lime.py`; tests: `tests/analysis/test_paper_g_s3.py`.

### 12.2 Exploratory diagnostics on the frozen data (R3, R6, R7, R11)

Computed from the frozen raw shards with the frozen orientation and average-rank conventions of
section 11.9; outputs in `outputs/analysis/paper_g/exploratory_post/`; generated report
`docs/reports/paper_g/DIAGNOSTICS_REPORT.md`; code `scripts/paper_g_diagnostics.py`. All exploratory.
No original table is changed.

- **R3, explainer rank positions (three studied explainers, seven metrics, 160 blocks).** Per metric
  and dataset: how often each explainer has rank 1, 2 or 3 (untied), and how often it is tied. Per
  block: whether one explainer has the same untied extreme rank (all 1 or all 3) under all seven
  metrics; whether one explainer is untied last under all seven. SHAP versus occlusion without LIME:
  per block and metric the sign of (oriented SHAP − oriented occlusion); the share of the 21 metric
  pairs with the same non-zero sign, and the share of blocks in which all seven metrics give the same
  order. Descriptive; the 0.5 decision rule is not applied.
- **R6, prediction-level adjustment of H2.** Within each H2 block (dataset × model × explainer ×
  seed, all four explainers, 200 instances), every oriented metric and `f_x` (the predicted-class
  probability at the instance, stored by the run) are converted to average ranks; the adjusted value
  of a metric pair is the Pearson correlation of the residuals of the two ranks after an ordinary
  least-squares fit (with intercept) on the rank of `f_x` (a rank-based partial correlation);
  undefined if a residual is constant (counted, never 0). The 15 pairs and their block mean are
  aggregated exactly as H2 (block → dataset → eight dataset values, mean and 95% t-interval). The
  unadjusted values are recomputed by the same code and must equal the frozen H2 outputs to within
  5e-7, the precision of the frozen CSV files (six decimals) (a validation of the code path). No test; no replacement of H2; no causal reading.
- **R7, M7 structure.** Groups per dataset (the length of a ROAR-lite `global_rank`); the removal-set
  size `n_top(G, level)` per dataset and level; per block and level, whether two or three studied
  explainers remove identical sets (sets compared as sets); M7 ties (equal `m7_roar` between studied
  explainers, and a tied top) by dataset and by model. Untested explanations (retraining variance)
  are named as such.
- **R11, random control last.** Per block (160) and metric (M1 to M7), the rank of the random control
  among the four explainers (average ranks). Reported: the share of blocks in which it is untied last
  under all seven metrics, the share in which it is last or tied last under all seven, and the share
  per metric. Denominator: 160 blocks.

### 12.3 S1: supplementary LIME contributions — specification and pilot

Written **2026-11-16**, after S3 (PR #133, merged `00bdca57d`) and before any S1 code or output
existed, on the author's authorization of the same day (Task 18). **Supplementary and exploratory;
not preregistered.** It cannot replace or reclassify the original H1/H2 or their decision; the
original 0.5 decision table stays attached to the original analysis only. Authorized now: this
specification, the implementation, its tests and the pilot of 12.3.6. The full S1 run needs a
separate authorization.

**Motivation (S3, `S3_REPORT.md`).** On the synthetic conditions, LIME's frozen slopes agree with the
exact Shapley values at 0.00–0.02; the surrogate contributions `w_j (x_j − μ_j)/s_j` at 0.96
(additive) and 0.64–0.75 (interaction). S3's features are all numeric, so it did not test
categorical groups.

**Question.** Does the agreement among faithfulness metrics observed in the original analysis persist
when LIME's surrogate coefficients are converted into signed contributions relative to a defined
reference?

#### 12.3.1 Representations and estimands

For an explained instance `x` (encoded, as given to LIME), LIME's coefficients `w` in its own
standardised coordinates, its fitted `μ = scaler.mean_` and `s = scaler.scale_`, and a reference
point `r`, the contribution of encoded column `j` to **LIME's fitted linear surrogate** is
`c_j(r) = w_j (x_j − r_j) / s_j`; the group contribution of a raw feature `G` is `Σ_{j∈G} c_j(r)`,
oriented to the predicted class with the frozen `orient`. This is the exact additive decomposition of
the surrogate's change from `r` to `x`; it is a contribution to the model only as far as the
surrogate approximates the model.

| Id | Reference `r` | Estimand | Status |
|---|---|---|---|
| **S1-B** | the metrics' masking baseline `b` (`lib.baseline`: training mean for numeric columns; one-hot of the training mode for categorical groups) | surrogate change from the masked point to `x`: the reference that M1–M6 use when they mask a group | primary supplementary representation |
| **S1-M** | LIME's training mean `μ` (dummy columns at their category shares, an infeasible point for a categorical group) | the representation validated by S3 | predefined sensitivity |

For numeric columns `b_j = μ_j` up to floating point (verified in the pilot), so S1-B and S1-M
differ only on categorical groups. For a categorical group whose instance value is the mode, S1-B is
exactly 0 (masking it changes nothing); S1-M is not. For category `a ≠ mode m`, S1-B equals
`w_a/s_a − w_m/s_m`. The choice of S1-B as primary is made here, before any S1 output, because it
matches the semantics of M1–M6 (Section 3 and the RCA-005 contract).

**M7.** The S1 global ranking of LIME is the mean |group contribution| over the explained
instances (as for SHAP), separately for S1-B and S1-M. The frozen slope-based M7 for LIME is not
reused: summed one-hot slopes are not an importance (RCA-005 contract).

**Semantic contract.** Both representations are declared in `scripts/paper_g_semantics.py` as signed
contributions with their references; S1-M on a dataset with categorical groups is admitted for M1–M6
only as the declared sensitivity estimand "mean reference differs from the masking baseline". The
S1 code calls the contract before computing any metric.

#### 12.3.2 Reconstruction gate (per block, before any conversion)

With the frozen `lib.prepare` (dataset version, split, preprocessing, model, seed), the frozen LIME
(`lib.make_explainer`, explainer seed = block seed, per-instance seed `(seed·100003 + pos) mod 2^31`):

1. the instance identifiers equal the stored ones;
2. for every instance, the reconstructed predicted class equals the stored `pred_class` and the
   reconstructed `f_x` equals the stored LIME row's `f_x` within **1e-12**;
3. the reconstructed encoded-column vector `w`, grouped with `group_attr`, oriented and rounded to
   8 decimals, equals the stored `attr` within **1e-8** in every group;
4. explaining the same instance twice gives the identical encoded vector;
5. recomputing M1–M6 (and their `_b2` forms) with the frozen `instance_metrics` on the reconstructed,
   unrounded LIME group vector (the vector the run scored; check 3 ties it to the stored, rounded
   `attr`), with the frozen per-instance generators, equals the stored metric values within **1e-9**.

Any failure stops the block and the run; outputs written so far are kept.

#### 12.3.3 Metrics

M1–M6 and their second-baseline forms: the frozen `lib.instance_metrics` with the frozen per-instance
generators (`default_rng([seed, pos, 2])` for the second baseline, `default_rng([seed, pos, 5])` for
M4/M5), applied to the S1-B and S1-M group vectors. M7: the frozen `lib.roar_score` with the S1
global rankings. Directions as in section 3. `m4_degenerate` is recorded as in the frozen run.

#### 12.3.4 Full-run analysis (if authorized later; not computed now)

The frozen SHAP, occlusion and random rows are reused unchanged; only LIME's rows are replaced by S1-B
(and, as sensitivity, S1-M). With the frozen functions of `scripts/paper_g_analyze.py`, unchanged:
system-level agreement (mean pairwise Spearman, Kendall's W, dataset-level t-intervals), explainer
positions (R3 form), winner flips, SHAP–LIME order under M1–M7 (now comparable for M1–M6),
instance-level agreement (H2 form, and the R6 adjustment), second-baseline and six-metric
sensitivities, M7. **Comparison with the original:** estimates are reported beside the original ones,
with the same aggregation; differences are descriptive. No new decision classification, no 0.5 rule,
no test of "S1 versus original". Synthetic: S3 already compares the representations with the truth;
no further synthetic run is planned.

#### 12.3.5 Ties and undefined values

As in 11.3 and 11.9: average ranks; undefined correlations left out and counted, never 0; a group
contribution that is exactly 0 is a valid value (it ties with other zeros under `order_of`, broken
by index, as in the frozen metric code).

#### 12.3.6 Pilot (authorized now)

Purpose: implementation and construct validation, **not** an estimate of agreement. Scope, chosen by
rule before any S1 output:

- **numerical dataset:** the numeric-small dataset with the fewest feature groups: **phoneme** (5);
- **mixed dataset:** the dataset with categorical groups and the fewest rows: **german_credit**
  (1,000 rows);
- all four models; seed **42**; the first **20** instances of the frozen `data["instances"]` order
  (the frozen pilot size); M7 with the global ranking over those 20 instances.

Records: 2 datasets × 4 models × 20 instances × 2 representations = **320** instance rows; 16 M7
rows; 160 reconstruction rows. No agreement statistic (H1/H2 form) is computed on the pilot.
**Acceptance:** every gate of 12.3.2 passes; `b_j = μ_j` for numeric columns within 1e-12; every
categorical instance at the mode has S1-B group contribution exactly 0; no failed metric row; the
contract admits every computed pair; outputs and provenance complete. **Stop criteria:** any gate
failure, a contract refusal, or a failed row.

**Outputs.** `outputs/analysis/paper_g/supplementary/s1_pilot/` and the generated
`docs/reports/paper_g/S1_PILOT_REPORT.md`; full run (later) `supplementary/s1/` with stage name
`lime_supp`. Code: `scripts/paper_g_s1_lime.py`; tests: `tests/analysis/test_paper_g_s1.py`.
