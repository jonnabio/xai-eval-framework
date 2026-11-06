# WP0 findings (2026-11-06)

Facts read from the code and the EXP2 artifacts that the revision builds on. Each finding
names the review item it answers. Nothing here changes a registered value yet.

## F1. Adult has 108 transformed features, not 103 (X-4; R2-3 quotes 103)

`experiments/exp1_adult/models/preprocessor.joblib` is a `ColumnTransformer` with 6 numeric and
8 categorical inputs; `get_feature_names_out()` returns **108** columns. LIME's maximum active
ratio in the artifacts is 10/108 = 0.0926, which agrees. The manuscript says 103 (current
lines 233 and 620). It is a factual correction to make and to acknowledge in the response
letter (Reviewer 2 repeats 103). Consequence for D-3: the LIME default kernel width is
$0.75\sqrt{108} \approx$ **7.79**.

## F2. Stability settings and zero-vector handling (R1-m6, R1-3, R1-M7)

- The runner (`src/experiment/metrics_engine.py`) uses `StabilityMetric` with
  `stability_perturbations` = 15 (EXP2 configs) and `stability_noise_level` = 0.1 (default in
  `src/experiment/config.py`). That agrees with the paper: $T$ = 15, σ = 0.1.
- Noise is added to **every transformed feature**, one-hot columns included
  (`src/metrics/stability.py`, line 51).
- Cosine is computed with scikit-learn's `cosine_similarity`, which returns **0 for an
  all-zero vector**. A degenerate LIME explanation therefore counts as maximally dissimilar.
  It is not excluded. Whether this contributes to LIME's near-zero stability is measured in WP4.5.
- The LIME explainer is constructed once with a fixed `random_state`. Successive calls draw
  new neighbourhoods, so explainer sampling noise is part of the measured instability (WP4.1).

## F3. Fidelity conventions (R1-m7)

`src/metrics/faithfulness.py`: fidelity is the Pearson correlation between **absolute**
attributions and **absolute** prediction drops when each feature is masked singly with its
training mean (signs are discarded on both sides). If either vector is constant (standard
deviation < 1e-9), for instance an all-zero explanation, **fidelity is set to 0**, not left
undefined or excluded. The faithfulness gap masks the top-5 features by |attribution|
together.

## F4. Instance sampling and overlap (R1-m5, R1-M2, R1-2)

From `src/evaluation/sampler.py` and the stored instance IDs:

- Instances are drawn from the test split per stratum (TP, TN, FP, FN), $N$ per stratum, seeded
  by the run seed. A cell holds 4N instances (N=100 gives 400).
- **The N levels are nested:** for a given model and seed, the N=50 instances are a subset of
  N=100, which is a subset of N=200 (checked on RF and XGBoost, seed 42).
- **Seeds barely overlap:** 7 (RF) and 1 (XGBoost) shared instances out of 400 between seeds 42
  and 123 at N=100.
- **Models differ in their instances** for the same seed: the strata depend on each model's
  errors (RF vs XGBoost, seed 42, N=100: 34 of 400 shared).
- **SHAP and LIME see identical instances in a cell**, so the pairing is exact.

Consequence for WP6: the three N cells of a (model, seed) are not independent replicates.
The highest level that has nearly disjoint instances is (model × seed): 25 units for SHAP vs
LIME. They are still clustered in 5 models that share one trained model each. The hierarchical
analysis uses model as the top level and (model, seed) as the replicate; N is a fixed factor,
not a replicate.

## F5. Candidate datasets for WP3 (D-4)

Checked on the OpenML API on 2026-11-06. All are public, active and binary:

| OpenML id | Name | Rows | Features | Numeric / symbolic | Minority % | Missing | 2 × 2 cell |
|---|---|---|---|---|---|---|---|
| 37 | diabetes | 768 | 8 | 8 / 0 | 34.9 | 0 | numeric, low dimension |
| 44 | spambase | 4,601 | 57 | 57 / 0 | 39.4 | 0 | numeric, high dimension |
| 3 | kr-vs-kp | 3,196 | 36 | 0 / 36 | 47.8 | 0 | categorical, lower dimension |
| 24 | mushroom | 8,124 | 22 | 0 / 22 | 48.2 | 2,480 | categorical, high one-hot dimension |
| 40981 | Australian (optional) | 690 | 14 | 6 / 8 | 44.5 | 0 | mixed |

(Features exclude the target.) **Open point:** mushroom, and to a lesser degree kr-vs-kp, are
almost separable. Tree models make nearly no errors on them, so the **FP and FN strata will be
empty or tiny** and the confusion-matrix sampling of the protocol cannot fill them. Options for
the author:

1. keep them and report the realized stratum counts (the error strata are absent by
   construction);
2. replace mushroom with a high-dimensional categorical dataset that models do not separate,
   found in WP0 and kept outside Papers D, E and F;
3. sample those datasets uniformly instead of by stratum, which is a protocol deviation and
   would be stated.

The pilot (WP2.1) gives each model's error counts on these datasets before the choice.

**Resolved 2026-11-06 (author: option 2).** Screening with 3-fold cross-validation on the
one-hot data (logistic regression and a 100-tree random forest; errors pooled over folds):

| Dataset | One-hot columns | Rows | LogReg acc / FP / FN | RF acc / FP / FN | Verdict |
|---|---|---|---|---|---|
| mushroom | 117 | 8,124 | 1.000 / 3 / 0 | 1.000 / 0 / 0 | **Separable; dropped** |
| kr-vs-kp | 73 | 3,196 | 0.964 / 64 / 52 | 0.990 / 12 / 19 | Thin: about 10 RF errors in a test split |
| **connect-4**, win vs not-win (20,000-row sample) | **126** | 67,557 | 0.792 / 2,569 / 1,597 | 0.838 / 2,214 / 1,020 | **Replacement for mushroom** |
| splice, N vs boundary | 287 | 3,190 | 0.938 / 89 / 110 | 0.971 / 23 / 68 | Possible; small and binarized |
| **PhishingWebsites** | **68** | 11,055 | 0.940 / 378 / 290 | 0.968 / 216 / 138 | **Proposed replacement for kr-vs-kp** |

- **connect-4** (OpenML 40668, all 42 features categorical; classes 2 = 44,473, 1 = 16,635,
  0 = 6,449) is binarized as class 2 vs the rest (66.1% positive). This is a stated deviation:
  the protocol is binary. At 126 columns it is the closest categorical match to Adult's 108.
  Training uses a stratified subsample if the SVM needs it (to be stated).
- Neither connect-4 nor PhishingWebsites appears in any manuscript, thesis file, registry or
  Paper F list (searched 2026-11-06). Paper F's planning notes (`docs/reports/paper_f/
  ANALYSIS_PLAN.md`, version 2.1) show that Spambase, Chess (kr-vs-kp) and Mushroom were
  candidates for F and were **rejected** as too easy (AUC above 0.98); none reached F's results.
- Spambase is also near the ceiling (F's rule). It keeps errors (about 5%), so it stays in the
  numeric-high cell; its realized FP/FN counts are reported.

Resulting design (dimension × encoding, with Adult as the mixed case at 108):

| | Lower dimension | Higher dimension |
|---|---|---|
| Numeric | diabetes, 8 | spambase, 57 |
| Categorical (one-hot) | PhishingWebsites, 68 | connect-4, 126 |

Spambase (57 numeric) against PhishingWebsites (68 categorical) contrasts the **encoding at a
similar dimension**; the rows contrast dimension within each encoding.

## F6. Run cost reference from EXP2

One EXP2 Anchors run (RF, seed 123, N=100) took 27,199 s (7.5 h) for 400 instances, stability
included. The Anchors timing sub-sample of WP2-T has to be small. The pilot sets its size.
