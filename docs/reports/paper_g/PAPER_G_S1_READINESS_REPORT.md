# Paper G — S1 readiness report (specification, implementation and pilot)

**Date:** 2026-11-16. **Status:** supplementary and exploratory (plan 12.3). For methodological review
and the author's decision on the full S1 run, which is **not authorized**. No agreement statistic was
computed from S1 rows; nothing here bears on H1 or H2.

## A. Integration

| Item | Revision |
|---|---|
| PR #133 (S3 and diagnostics results) | merged `00bdca57d` |
| PR #135 (S1 specification 12.3, implementation, contract extension) | merged `03e462eb6` — the frozen S1 code |
| Pilot executed from | `03e462eb6`, 2026-11-16 14:03 UTC |
| `main` at writing | `03e462eb6` |

Verified unchanged on `main`: raw shards and logs, the original analysis outputs and
`RESULTS_REPORT.md` (identical to PR #129 head `3b0063f41`), the frozen code (`paper_g_lib`,
`paper_g_run`, `paper_g_synthetic`, `paper_g_analyze`), `experiments/exp_g/` (config and analysis
spec), and the S3 and diagnostic outputs (identical to PR #133 head).

## B. Scientific specification (plan 12.3.1)

**Definition.** With LIME's encoded-column coefficients `w` (its standardised coordinates), its
fitted `μ = scaler.mean_`, `s = scaler.scale_`, the explained instance `x` and a reference `r`:
`c_j(r) = w_j (x_j − r_j)/s_j`, summed over the columns of each raw feature and oriented to the
predicted class with the frozen `orient`. Exactly the additive decomposition of **LIME's fitted linear
surrogate** from `r` to `x`; a contribution to the model only as far as the surrogate approximates it.

| | S1-B (primary supplementary) | S1-M (sensitivity) |
|---|---|---|
| Reference | the metrics' masking baseline: training mean (numeric), one-hot of the mode (categorical) | LIME's training mean (categorical dummies at their shares) |
| Numeric columns | identical to S1-M (pilot: difference exactly 0) | S3 form |
| Categorical group, value = mode | exactly 0 (masking it changes nothing) | not 0 |
| Categorical group, value `a ≠` mode `m` | `w_a/s_a − w_m/s_m` | `Σ_j w_j (x_j − p_j)/s_j` (relative to an infeasible point) |
| Contract (RCA-005) | signed contribution, compatible with M1–M7 | compatible on numeric data; on mixed data admitted for M1–M6 only as the declared sensitivity estimand |

**Categorical encoding (frozen preprocessing, `lib.split`).** Full one-hot encoding, no dropped column,
rare levels pooled into one infrequent column (`max_categories = 20`); binary categories give two
dummies; each raw feature is one group; the masking baseline sets the group to the mode's one-hot
(`lib.baseline`). German credit: 20 groups, 13 categorical, up to 10 dummies, 61 encoded columns.

**How LIME treats one-hot columns.** Its scaler standardises each dummy with `p_j` and
`sqrt(p_j(1 − p_j))`; with no categorical features declared it samples every dummy as a continuous
Gaussian, so perturbed points are **off the one-hot manifold** (non-binary values, several or no
active dummies). The surrogate's dummy coefficients therefore describe the model's response to
infeasible inputs; the contribution of a category switch is a surrogate approximation, exact only for
models linear in the encoded columns.

**Differences from the original representation.** The original stored LIME's coefficients (slopes,
sign = direction of change, instance-invariant for linear models) as if they were contributions; S1
stores contributions of the same fitted surrogate with an explicit reference. LIME's fitting choices
(kernel width 3.0, sampling around the training mean, 1,000 samples) are **unchanged**.

**M7.** S1 ranks features by mean |group contribution| over the explained instances (as for SHAP),
per representation; the frozen slope-based M7 is not reused (summed one-hot slopes are not an
importance).

**Limitations of the estimand.** (i) Surrogate, not model, contributions; (ii) off-manifold
categorical sampling; (iii) S1-B's reference equals the masking baseline, but SHAP's reference is a
background expectation, so SHAP and S1-B are not referenced identically; (iv) the frozen kernel and
sampling remain, so S1 tests the representation, not LIME's configuration.

## C. Validation

**Constructed tests** (`tests/analysis/test_paper_g_s1.py`, 15; contract 13; all Paper G 126 passed;
CI green on #135):

| Property | Result |
|---|---|
| Surrogate identity `Σ c_j(r) = g(x) − g(r)` | exact |
| Model linear in encoded columns, numeric and one-hot groups: S1-B = model contribution relative to the baseline | within 2e-3 (LIME sampling noise) |
| Numeric groups: S1-B = S1-M | exact |
| Categorical value at the mode: S1-B = 0, S1-M ≠ 0 | exact |
| Zero-variance column (scale set to 1 by the scaler) | finite |
| Non-positive, non-finite scales; shape mismatch | refused |
| Predicted-class orientation | `v(class 0) = −v(class 1)` |
| Encoded-column alignment | groups partition the columns; names match features |
| Fitted logistic model (nonlinear): S1-B vs exact baseline-Shapley over groups | S1-B tracks it better than the slopes and above 0.5 on average (a property, not an identity) |
| Reconstruction gate, tampered `attr` or metric | stops |
| M7 ranking | equals `order_of(mean |c|)` |
| Contract | enforced; refusal stops the block |
| LIME substitution for the later system level | replaces only LIME rows; incomplete input refused |
| Determinism, refusals, output paths outside frozen directories | pass |

**Real-data reconstruction (pilot, 160 instances):** every instance passed every check — identical
instance ids and predicted classes; `f_x` within 4.4e-16 (tolerance 1e-12); regrouped coefficients equal
to the stored `attr` exactly (tolerance 1e-8); repeated explanations identical; recomputed M1–M6 and
`_b2` within 1.4e-15 (tolerance 1e-9). Numeric baseline − LIME mean: exactly 0 in all 8 blocks.

**Semantic contract:** S1-B compatible in all 56 pairs; S1-M compatible in 32 (phoneme, and M7) and
admitted as the declared sensitivity estimand in 24 (german_credit × M1–M6); no refusal.

## D. Pilot (plan 12.3.6)

| Item | Value |
|---|---|
| Datasets (by rule) | phoneme (numeric, 5 groups); german_credit (mixed, 1,000 rows) |
| Models; seed; instances | logreg, rf, xgb, mlp; 42; first 20 frozen instances per block |
| Instance rows | 320 of 320 (2 representations) |
| M7 rows | 16 of 16 |
| Failed rows; non-finite values; `m4_degenerate` | 0; 0; 0 |
| Categorical values at the mode | 148 per german_credit block; S1-B non-zero at the mode: 0 |
| Resources | 32 s wall, 268 MB peak, one process |
| Acceptance | **PASS** |
| Outputs | `outputs/analysis/paper_g/supplementary/s1_pilot/`, `S1_PILOT_REPORT.md` |

**Defect found (reporting only; outputs preserved):** the generated pilot report labels gate 5
"recomputed M1–M6, _b2 on stored attr", but the gate (correctly, per 12.3.2 as amended before the
freeze) recomputes on the reconstructed unrounded vector. The generator's label is to be corrected
before any further execution; no value is affected.

## E. Statistical readiness (full run, if authorized)

**Planned supplementary outputs** (`supplementary/s1/`, stage `lime_supp`): per block and instance the
S1-B and S1-M metric rows (M1–M6, `_b2`), M7 rows; then, with the frozen `paper_g_analyze` functions
on the frozen non-LIME rows plus substituted LIME rows: system-level mean pairwise Spearman and
Kendall's W with dataset-level t-intervals; explainer positions (R3 form); winner flips; SHAP–LIME order
under M1–M7 (now meaningful for M1–M6); instance-level agreement (H2 form, unadjusted and R6-adjusted);
second-baseline and six-metric sensitivities; M7.

**Comparison with the historical findings:** side by side, same aggregation, descriptive differences.
No new decision classification; the 0.5 rule stays with the original analysis; no test of S1 against
the original; the three-explainer floor (review 4.1) still applies and is read with the position table.

**Ties and undefined values:** as plan 11.3/11.9 — average ranks, undefined correlations excluded and
counted; a zero group contribution is a valid value (ties broken by index in `order_of`, as frozen).

**Classification:** all S1 outputs are supplementary/exploratory; the original H1/H2 remain the
confirmatory results.

**Cost estimate (from measured times):** LIME explanation and metric recomputation for 160 blocks ×
200 instances, plus M7 for two representations (32 retrainings per block; MLP on the large mixed
datasets dominates, as in the original ROAR-lite: 7.35 h serial for four explainers). Estimate 5–8 h
serial; about 1–1.5 h with 6 parallel jobs, which needs a block-parallel driver (the pilot code is
single-process). Run on the recorded host with the frozen environment.

## F. Remaining risks

1. **Numeric features — defensible.** Exact identity for the surrogate, S3 (0.96 additive, 0.64–0.75
   with interactions), exact reconstruction, and numeric baseline = LIME mean.
2. **Categorical features — qualified.** S1-B is well defined, zero at the mode and equal to the
   model's category-switch effect for models linear in the encoded columns; for nonlinear models it rests
   on a surrogate fitted to off-manifold dummy samples, which no test on real models validates.
3. **Construct mismatch — addressed for the representation type,** not for LIME's fitting choices.
4. **Reassessing H1 — possible descriptively:** S1 shows whether the agreement survives once LIME is
   represented as a contribution; it cannot overturn or confirm H1's frozen decision, and with three
   explainers the result must be read with the position table.
5. **S2 — not needed for construct validity.** S3 found discretised LIME further from the truth than
   S1-B/S1-M; S2 would add external validity ("LIME as commonly run") and could be a later sensitivity.

**Recommendation:** proceed to the full S1 run after (a) correcting the pilot report's gate-5 label,
(b) adding a block-parallel driver with the same gate per block, and (c) the author's authorization.

---

**ORIGINAL RESULTS: PRESERVED**

**S1 SPECIFICATION: FROZEN**

**NUMERICAL SEMANTICS: PASS**

**CATEGORICAL SEMANTICS: QUALIFIED**

**RECONSTRUCTION: PASS**

**S1 PILOT: PASS**

**FULL S1 EXECUTION: NOT AUTHORIZED**
