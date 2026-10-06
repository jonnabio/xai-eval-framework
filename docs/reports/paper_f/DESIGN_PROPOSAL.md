# Paper F — Design Proposal for the Author (Scientific Advisor)

**Date:** 2026-10-05
**Status:** Approved by the author on 2026-10-05 (16 datasets by rule, 200 instances, four
models, both statistical models with the mixed model as primary, permutation tests only,
a new run) and written into `ANALYSIS_PLAN.md`, version 2. Kept as the record of the
reasons. The text below is as proposed. Original status line: Proposal. `ANALYSIS_PLAN.md` is not changed. If the author approves, each point
becomes a dated row of its section 12 and the sections it names are rewritten, before any
dataset is loaded or any explainer is run.
**Inputs:** `ANALYSIS_PLAN.md`, `METHODOLOGICAL_ANALYSIS.md`, the metric code in
`src/metrics/`, the stored run times of EXP2 and EXP3, and a simulation
(`scripts/paper_f_power_simulation.py`, output `outputs/analysis/paper_f/power_simulation.csv`).
No Paper F data exist.

---

## 1. Recommendations

| # | Question | Recommendation |
|---|---|---|
| 1 | How many datasets | **16 (Adult and 15 more); 12 is the floor.** Four cannot support the claim of the paper (section 2). |
| 2 | Which datasets | Chosen by a rule fixed in advance from public benchmark collections, not by hand (section 3.1). |
| 3 | Instances | **200 per dataset, model and seed**, stratified by predicted class. The balance by quadrant is dropped (section 3.3). |
| 4 | Models | **Four: logistic regression, random forest, XGBoost, MLP.** Both tree models are run. |
| 5 | Statistical model | Both are run. **One is primary and is named now**; the other is a sensitivity analysis (section 5). |
| 6 | Fidelity for Anchors and DiCE | Not as one metric for the four explainers. Rank the four on the metrics defined for all of them; report fidelity for LIME and SHAP only (section 4). |
| 7 | Ranking tests | Exact or permutation tests only. The primary quantity is the mean rank correlation between datasets with an interval, not a test on each pair (section 5). |
| 8 | Adult baseline | A new run, as the author decided. Estimated cost in section 6. |

---

## 2. Why four datasets are not enough

The paper asks whether a conclusion reached on one dataset holds on others. The unit that
is sampled is therefore the dataset. Thousands of instances inside four datasets make the
estimates for those four datasets precise; they say nothing more about a fifth.

Three facts about the planned tests, for four explainers:

1. **A test on one pair of datasets cannot be significant.** Four explainers have 24
   possible orders. Two datasets that agree perfectly give a two-sided p of 2/24 = 0.083.
   The criterion "pairwise tau significance" of section 10 of the plan cannot be met by
   any data.
2. **Kendall's W depends on the number of datasets.** With random rankings its expected
   value is 1/k: 0.25 for four datasets and 0.06 for sixteen. The fixed thresholds 0.50
   and 0.80 of section 8.3 do not mean the same thing for different k. The mean Spearman
   correlation between pairs of datasets, (kW − 1)/(k − 1), does not have this problem and
   is proposed as the reported quantity.
3. **With four datasets the estimate is close to uninformative.** Simulation of 20,000
   studies for each case:

| Datasets | W needed for p < 0.05 | Power when the true correlation is 0.2 | Power when it is 0.5 | Central 95% range of the estimate when the true value is 0.5 | Same, true value 0.8 |
|---|---|---|---|---|---|
| 4 | 0.63 | 0.16 | 0.51 | −0.07 to 0.90 | 0.43 to 1.00 |
| 8 | 0.31 | 0.43 | 0.94 | 0.15 to 0.81 | 0.56 to 0.95 |
| 12 | 0.21 | 0.62 | 0.99 | 0.22 to 0.76 | 0.62 to 0.93 |
| 16 | 0.16 | 0.77 | 1.00 | 0.27 to 0.72 | 0.65 to 0.93 |
| 20 | 0.13 | 0.88 | 1.00 | 0.29 to 0.70 | 0.67 to 0.91 |

With four datasets a moderate true agreement (0.5) is detected half of the time, and the
estimate can fall anywhere between no agreement and near-perfect agreement. With twelve,
detection is almost certain, but "moderate" and "strong" still overlap (0.62 to 0.76).
With sixteen the overlap is small. The gain from sixteen to twenty is slight.

The simulation assumes that the datasets are independent draws and that scores have no
ties. Real datasets from the same domain are more alike than that, so the figures are
optimistic; this is one more reason to prefer sixteen.

---

## 3. Design

### 3.1 Datasets: a rule, then a list

The three "structural contrasts" of the plan were to be picked by the author. Picking by
hand lets a reviewer ask whether the datasets were chosen to show disagreement. A rule
fixed before any explanation is computed answers that.

**Inclusion rule:**
- public, usable without registration or a restrictive licence;
- tabular, binary target (or a binarisation that the source itself documents);
- at least 1,000 rows and between 5 and 100 raw features;
- after training: cross-validated AUC between 0.65 and 0.98 for at least three of the four
  models. This removes datasets that are noise or that are trivially separable. It uses
  model results only, never explanation results.

**Strata**, so that the structure varies on purpose: feature composition (all numeric;
mixed; all or mostly categorical) by size (under 10,000 rows; 10,000 or more). Six strata.
Target: the sixteen spread as evenly as the pool allows, Adult counted in "mixed, large".

**Order inside a stratum:** the candidates are listed by their identifier in the source
collection, and taken in that order until the stratum is full. A candidate that fails the
rule is recorded with the reason.

**Candidate pool** (to be verified in the characterisation step; the sizes are from the
collections' documentation as recalled, and the rule decides, not this list):

| Stratum | Candidates |
|---|---|
| Numeric, small | Phoneme, Spambase, QSAR biodegradation, Ozone level |
| Numeric, large | MAGIC telescope, Electricity, Default of credit card clients |
| Mixed, small | German Credit, Churn, Sick, COMPAS |
| Mixed, large | **Adult**, Bank Marketing, Nomao |
| Categorical, small | Chess (king-rook vs king-pawn), Mushroom |
| Categorical, large | Amazon employee access |

Notes:
- **Breast Cancer (569 rows) fails the size rule.** Its test split gives about 114
  instances. It can be shown in a supplement; it is not one of the sixteen.
- HELOC needs registration with its owner and is left out. COMPAS is public but carries a
  known debate about its labels; if it is used, the paper says so.
- Mushroom is likely to fail the AUC ceiling. The categorical strata are thin; if they
  cannot be filled, the paper states it as a limit of the claim.
- The pool above has seventeen names. If fewer than sixteen pass, the study runs with what
  passes, provided it is at least twelve; below twelve the pool is widened by the same rule.

### 3.2 Models and explainers

- Models: logistic regression, random forest, XGBoost, MLP. One fixed configuration per
  model for all datasets, stated in the plan. SVM is left out: in EXP2 one SHAP explanation
  of the SVM took about 26 minutes.
- Explainers: LIME, SHAP, Anchors, DiCE, each with one fixed configuration.
- Conditions: 16 datasets × 4 models × 4 explainers = 256, each with 5 seeds.

### 3.3 Instances

The plan asks for 100 instances per quadrant (true and false positives and negatives).
That belongs to the question of Paper D. Small or accurate datasets do not have 100
misclassified cases, and the sample would differ in kind between datasets.

Proposal: 200 test instances per dataset, model and seed, stratified by predicted class,
the same instances for the four explainers. An instance for which an explainer returns
nothing is kept and counted as a failure; the failure rate is reported for every cell
(threat 2 of the appraisal).

---

## 4. Metrics: what may be compared across the four explainers

The fidelity metric of the framework (`src/metrics/fidelity.py`) treats every explanation
as a vector of linear weights and measures how well that linear model predicts the
classifier around the instance. That is what LIME produces and close to what SHAP
produces. An Anchors rule and a DiCE counterfactual are not linear models; turning them
into weights and scoring them this way measures the conversion, not the method. Paper C
already states this limit for the same explanations.

| Metric | Defined for | Use |
|---|---|---|
| Faithfulness gap (prediction change when the features the explanation names are masked) | all four | ranking of the four |
| Stability | all four | ranking of the four, after the change below |
| Sparsity (number of features used) | all four | ranking of the four |
| Cost | all four | ranking of the four; also as a ratio to the model's prediction time |
| Failure rate | all four | reported for every cell |
| Fidelity (R² of the local linear model) | LIME, SHAP | comparison of the two only |
| Rule precision and coverage | Anchors | reported, not ranked against others |
| Validity and proximity of the counterfactual | DiCE | reported, not ranked against others |

Two changes to the metric code are needed for a study across datasets, both shared files:

- **Stability** adds Gaussian noise with standard deviation 0.01 to every feature and
  compares weight vectors by cosine similarity. On one-hot columns that noise has no
  meaning, and its size relative to the data differs between datasets. Proposed: perturb
  numeric features by a fixed fraction of each feature's standard deviation, leave
  categorical features unchanged, and compare the sets of features named (Jaccard of the
  top five), which is defined for the four explainers.
- **Faithfulness gap** masks the top five features. For datasets with five to ten features
  that is most of the input. Proposed: mask the top 20% of features, at least one.

These are new definitions, so no Paper F value can coincide by construction with a value
of Papers A to E.

---

## 5. Analysis

**Level.** Instances are not independent evidence about generalisation. Every analysis
starts from one mean per dataset, model, explainer and seed (1,280 values per metric).

**Primary analysis (one per metric, four metrics, Holm correction over the four):**
1. For each dataset, the mean of each explainer over models and seeds, and the order of
   the four explainers.
2. The mean Spearman correlation between the orders of all pairs of datasets, with a 95%
   interval from resampling datasets (bootstrap, 10,000 draws).
3. A permutation test of "the orders are unrelated" (exact distribution of W).
4. **A noise ceiling:** the same correlation between seeds inside each dataset. Agreement
   between datasets cannot exceed agreement between two runs on the same dataset, so the
   result is read against that ceiling.

**Secondary, declared now:**
- For each of the six pairs of explainers, the share of datasets in which the order is the
  same as on Adult, with an exact binomial interval. This is the direct answer to "can a
  result on Adult be trusted elsewhere".
- The largest rank change of each explainer between any two datasets.
- Variance shares on the cell means: explainer, dataset, model, explainer × dataset,
  explainer × model, residual. The share of explainer × dataset relative to explainer is
  the size of the non-generalisation. **Primary model: linear mixed model with dataset as
  a random factor** (random intercept and random explainer effect by dataset; seed nested).
  **Sensitivity: the aligned rank transform** on the same cell means. If the two disagree,
  both are reported and the conclusion is the weaker one.
- The cost and quality frontier per dataset (section 9 of the plan), descriptive.

**Dropped or changed from the plan:**
- H1 (datasets differ in level) is descriptive only. With this many values it is
  significant for any data and does not bear on the question.
- The test of the interaction with datasets as a fixed factor and instances as replicates
  is dropped for the same reason.
- Significance of tau for single pairs of datasets is dropped (section 2, point 1).
- The labels "strong" (0.80) and "breakdown" (0.50) are kept as words for the mean
  correlation, not for W; the paper reports the estimate, its interval and the ceiling.

**What the study can and cannot say.** With sixteen datasets chosen by a public rule it can
say how well explainer orders agree across tabular binary-classification datasets of this
kind, and how far the Adult result carries. It cannot say which property of a dataset
causes a disagreement (the plan already forbids that).

---

## 6. Cost of the new run

**Basis.** Median wall time per explained instance in the stored EXP2 runs on Adult,
metrics included, in seconds (rounded; planning figures, not results):

| Model | LIME | SHAP | Anchors | DiCE | Sum |
|---|---|---|---|---|---|
| Logistic regression | 0.05 | 0.6 | 2.7 | 8.1 | 11.4 |
| MLP | 0.05 | 1.5 | 12.8 | 8.5 | 22.9 |
| Random forest | 0.3 | 1.3 | 57.3 | 22.8 | 81.8 |
| XGBoost | 0.06 | 0.02 | 4.8 | 10.7 | 15.6 |
| **All four models** | | | | | **131.6** |

EXP3 gave similar times for Anchors on the random forest on two other datasets (about 44
and 59 seconds), so the Adult figures are a fair guide.

**Total compute** = datasets × 5 seeds × 200 instances × 131.6 s:

| Design | Processor hours | Wall time on this laptop, 12 processes | With a 50% margin |
|---|---|---|---|
| 16 datasets, 4 models (recommended) | 585 | 49 h | about 3 days |
| 12 datasets, 4 models | 439 | 37 h | about 2.5 days |
| 16 datasets, random forest left out | 222 | 18 h | about 1 day |
| 16 datasets, 4 models, 100 instances | 292 | 24 h | about 1.5 days |

- Anchors on the random forest alone is 44% of the total.
- **Money.** On the laptop (16 cores): electricity only, a few US dollars. On a rented
  16-core machine at roughly 0.70 to 0.80 US dollars per hour (price recalled, to be
  checked): about 40 to 60 US dollars for the recommended design. No language-model calls
  are needed, so there is no API cost.
- **Uncertainty.** The stored times come from other hardware and from runs whose slowest
  cases took several times the median. Before the full run, a pilot of one dataset, four
  models, four explainers, one seed and 20 instances (under one processor hour) gives the
  real figure for this machine. The pilot's outputs are not used as results.

**Work before the run** (not included above):
1. A generic loader for the new datasets and the dataset characterisation — shared code.
2. The two metric changes of section 4 and their tests — shared code.
3. Runner for 256 conditions with resumable shards: `scripts/paper_f_*`.
4. Training of 64 models (16 datasets × 4) per seed and the AUC gate.

---

## 7. Decisions for the author

1. Sixteen datasets by rule (floor twelve), as in section 3.1?
2. 200 instances by predicted class, no quadrant balance?
3. Four models, SVM left out?
4. The metric table of section 4, with the two changes to stability and faithfulness?
5. The primary and secondary analyses of section 5?
6. Run on the laptop (about three days) or on a rented machine?
7. The venue, when known: its page limit decides how much of section 5 goes to a supplement.
