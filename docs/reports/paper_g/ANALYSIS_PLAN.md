# Paper G — Analysis and Execution Plan (version 1)

**Question:** Do faithfulness metrics agree on which explanation method is more faithful?
**Status:** Version 1, 2026-11-13. Draft for the author's review. No dataset loaded, no model
trained, no explanation computed for Paper G.
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

**8 datasets × 3 models × 4 explainers × 6 metrics, 5 seeds, 200 instances.**

### 2.1 Datasets

Eight public binary tabular datasets from OpenML, two per stratum of feature composition,
loaded with the existing Paper F loader (code reused; no Paper F result is reused or printed).
Proposed, to be confirmed by the author before the run:

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

Logistic regression (L2), random forest, XGBoost. One configuration per model for all datasets,
committed before training. Preprocessing: standard scaling, one-hot encoding, median or mode
imputation. Split 80/20, stratified, by seed. The MLP is left out to hold compute for the
retraining-based metric; this is stated as a limit.

### 2.3 Explainers (the four items that are ranked)

| Explainer | Role |
|---|---|
| SHAP (TreeSHAP for trees, KernelSHAP for logistic regression) | studied |
| LIME | studied |
| Occlusion (leave-one-feature-out with baseline replacement) | studied; also a known circularity check (section 3.2) |
| Random attribution (seeded Gaussian scores) | negative control: every metric must rank it last |

Four items is the minimum that makes a rank order informative. The random control gives a
sanity check that each metric works at all.

### 2.4 Seeds and instances

Seeds 42, 123, 456, 789, 101112. A seed fixes the split, the model, explainer sampling and
the random control. 200 test instances per dataset, model and seed, stratified by predicted
class. All explainers explain the same instances; all metrics score the same explanations.

## 3. Metrics (the "raters")

All metrics act on the same explanation vector and the same baseline (training mean for
numeric features, mode for categorical; one-hot groups masked together as one raw feature).

| ID | Metric | Direction | Definition (to be fixed in code with tests) |
|---|---|---|---|
| M1 | Deletion AUC | lower is better | area under predicted-class probability as features are removed in attribution order |
| M2 | Insertion AUC | higher is better | area under probability as features are added to the baseline in attribution order |
| M3 | Top-k prediction gap | higher is better | drop in probability when the top 20% of features (at least one) are masked |
| M4 | Faithfulness correlation | higher is better | Pearson correlation between attribution and single-feature masking drop |
| M5 | Infidelity | lower is better | expected squared error between attribution·perturbation and output change, Gaussian perturbations |
| M6 | Sufficiency | lower is better | probability change when only the top 20% of features are kept |

Comprehensiveness is the same quantity as M3 and is not counted twice.

**Optional M7 — ROAR-lite** (retrain without the globally top-ranked features; accuracy drop).
It is global, costly, and only defined at system level. It is run only if the pilot shows it fits
the time budget; otherwise it is left out and the paper says so.

### 3.1 Baseline sensitivity

Every masking metric depends on the replacement value. As a secondary factor, M1 to M3 and M6
are recomputed with a second baseline (random draw from training rows). This shows how much of
the disagreement comes from the baseline, not from the metric.

### 3.2 Known circularity

M4 and Occlusion are built from the same single-feature removal, so M4 is expected to favour
Occlusion. The analysis is reported with and without the Occlusion–M4 combination.

## 4. Analysis

**Level.** For the system level, one mean per dataset, model, explainer, seed and metric:
8 × 3 × 4 × 5 = 480 means per metric. Instances never count as independent evidence about
datasets.

### 4.1 Primary analysis: system-level agreement (H1)

For each dataset × model × seed block: rank the four explainers under each of the six metrics.
Treat metrics as raters and explainers as items.

1. **Estimate:** Kendall's W across the six metrics, per block; reported as the mean over
   blocks and as the mean pairwise Spearman correlation between metrics, (mW − 1)/(m − 1).
2. **Interval:** 95% percentile bootstrap over datasets (resampling datasets, 10,000 draws).
3. **Test:** permutation test of "metrics order explainers independently": ranks permuted
   independently within each metric and block, 100,000 permutations, one-sided.
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

Holm correction over H1 and H2 (and over metric pairs in 4.2 when tested).

## 5. What is not done

- No claim about which explainer is best in general.
- No claim about which metric is "correct". Disagreement is reported as a property of the
  measurement, not resolved by choosing a winner.
- No result of Papers A to F is printed. The SHAP and LIME values of Paper G come from its own run.
- No ground-truth faithfulness (synthetic models with known attributions) in the main study;
  it is a possible extension (section 8).

## 6. Order of work (BMAD)

| Step | Work | Output | Estimate |
|---|---|---|---|
| 1 | Author reviews this plan and the draft; decisions of section 9 | approved plan | author |
| 2 | Configuration file; power simulation | `experiments/exp_g/config.toml`, `scripts/paper_g_power_simulation.py` | 1–2 days |
| 3 | Metric code M1–M6 (+M7) with unit tests on toy models where the answer is known | `scripts/paper_g_metrics.py`, `tests/analysis/test_paper_g_metrics.py` | 4–6 days |
| 4 | Dataset gate and `datasets.csv` committed | `outputs/analysis/paper_g/datasets.csv` | 1 day |
| 5 | Pilot: 1 dataset, 3 models, 1 seed, 20 instances; time and failure check; outputs deleted | timing note | 1–2 days |
| 6 | Full run on the experiment laptop, resumable shards by seed | `outputs/analysis/paper_g/raw/` | 4–8 days machine time |
| 7 | Analysis script; figures by committed generators; registry entries | `scripts/paper_g_analyze.py`, `RESULTS_REPORT.md` | 3–4 days |
| 8 | References: search, DOI verification, ≥ 80% from 2024 or later | `reference_records.json` | 3–4 days, parallel to 6 |
| 9 | Fill the draft with results; transfer to the journal .docx template | `paper_g.docx` | author + 1 week |
| 10 | Scientific-rigor review and reference audit (Scientific Advisor) | `docs/review/…paper_g…` | 2 days |
| 11 | Anonymise; declarations; similarity and AI-content check; Zenodo release | submission package | 2 days |

Earliest submission: mid to late December 2026.

## 7. Risks

| Risk | Mitigation |
|---|---|
| Kendall W with four items is coarse | instance-level analysis (H2) carries most of the information; ranks reported with ties |
| Random control inflates agreement | primary estimate uses the three studied explainers only |
| Occlusion–M4 circularity | reported with and without that combination |
| Masking baseline drives the result | second baseline as a secondary factor |
| ROAR-lite too slow | optional; dropped if the pilot exceeds the budget |
| Overlap with Papers B, E, F | own run; the paper cites them as prior work and prints none of their values |
| Journal limit of 30% AI-generated text | the author rewrites the draft; the draft is a scaffold |

## 8. Possible extension (not in version 1)

Synthetic data with a known generating model, where the true attribution is known, to say which
metrics track it. Adds a strong anchor; costs about one week.

## 9. Decisions needed from the author

1. The eight datasets (section 2.1).
2. Whether the MLP is left out (section 2.2).
3. Whether ROAR-lite (M7) is attempted.
4. Whether the synthetic ground-truth extension (section 8) is in version 1.
5. Title (proposals in `paper_g_draft.md`).
