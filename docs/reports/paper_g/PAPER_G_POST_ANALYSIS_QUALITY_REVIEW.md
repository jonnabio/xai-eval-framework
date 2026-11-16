# Paper G — Post-analysis scientific quality review and LIME validity audit

**Date:** 2026-11-16. **Role:** Scientific Advisor (read-only on results; ACE `.ace/roles/roles.md` §8).
**Reviewed:** PR #129, head `3b0063f41` (49 files, result paths only), produced by the single
authorized run of `scripts/paper_g_analyze.py` at `26ef7106f` (analysis code `c56efa642`) on the
frozen run `04c6dfd84`. Result files are cited as on that branch, under
`outputs/analysis/paper_g/analysis/`.

**What this review did and did not do.** It read code, the LIME 0.2.0.1 source, Paper E's
validation record and the existing Paper G outputs, and ran one constructed demonstration of LIME's
output (`review/lime_semantics_demo.py`, toy model, no Paper G data). It recomputed nothing on the
Paper G data and changed no result, code, plan or stored attribution. Statements are marked
**[fact]** (established from code, library source or existing outputs), **[demo]** (shown by the
constructed demonstration), or **[hypothesis]** (plausible, not verified).

---

## 1. Executive verdict

1. **The LIME representation does not match what the metrics and the ground truth assume. [fact]**
   With `discretize_continuous=False` (hard-coded in `scripts/paper_g_lib.py::Lime`, inherited from
   Paper F, in neither `config.toml` nor the plan), LIME returns the **slopes of a ridge surrogate
   on standardised features**, not per-feature **contributions**. Metrics M1–M6 and the synthetic
   ground truth treat the attribution vector as signed contributions. This was already established
   and confirmed in Paper E (`docs/reports/paper_e/ANALYSIS_PLAN.md`, entries of 2026-10-03/04;
   `docs/reports/paper_e/README.md`, method table) and was not carried into Paper G's design.
2. **The analysis itself is correct.** The frozen procedure was implemented as specified and
   reproduced exactly by an independent recomputation (PR #129, 24/24 checks). The problem is the
   validity of one explainer's input to the measurements, not the statistics.
3. **H1's "broad agreement" is partly a structural floor. [fact + hypothesis]** With three ranked
   explainers, if one explainer holds the same extreme rank under every metric, every pairwise
   Spearman is 0.5 or 1, so the block mean cannot fall below 0.5, the decision threshold. LIME's
   representation is a plausible reason for one explainer to be consistently placed (Section 3).
4. **H2 (0.154) is a weak positive agreement whose size is likely depressed and distorted by
   prediction-level nuisance variation [hypothesis]**; two pairs are negative.
5. **The synthetic check mainly separates {SHAP, occlusion} from {LIME, random}. [fact]** LIME's
   agreement with the truth equals the random control's because slopes and contributions are not
   comparable objects, so the check cannot validate metrics on LIME.
6. **The paper remains publishable** with a narrower, qualified claim (Scenario B), and becomes
   stronger with a small pre-specified supplementary LIME experiment (Scenario C, Section 8).
   Several current statements must be withdrawn or qualified before submission (Section 9).

---

## 2. LIME semantic audit

### 2.1 What `exp.as_map()[1]` returns under Paper G's configuration

Configuration (`scripts/paper_g_lib.py`, class `Lime`): `LimeTabularExplainer(X_train,
discretize_continuous=False, kernel_width=3.0, random_state=seed)` with no `categorical_features`,
`sample_around_instance` at its default `False`; `explain_instance(x, predict_proba, labels=(1,),
num_features=d, num_samples=1000)`; the weights of label 1 are copied into `w` by column index.

From the LIME 0.2.0.1 source (`lime/lime_tabular.py`, `lime/lime_base.py`) **[fact]**:

1. **Scaler.** `StandardScaler(with_mean=False).fit(X_train)` (line 257) stores the column means
   `m` and standard deviations `s`; with no categorical features declared, every column, including
   one-hot dummies, keeps its own `m_j`, `s_j`.
2. **Sampling.** Without a discretizer, perturbations are `N(0, 1) * s + m` (lines 508–516):
   **around the training mean, not around the instance** (`sample_around_instance=False`). Row 0
   is the instance itself. One-hot columns are sampled as continuous Gaussians, so the model is
   queried on non-binary dummy values.
3. **Coordinates.** The surrogate is fitted on `z = (data − m) / s` (line 348).
4. **Weights.** Each sample is weighted by `sqrt(exp(−d² / kw²))`, `d` the Euclidean distance to
   the instance in `z`-space, `kw = 3.0` (package default `0.75·sqrt(p)`, lines 242–248).
5. **Surrogate.** `Ridge(alpha=1, fit_intercept=True)` on all `p` features (feature selection
   `auto` keeps all when `num_features = p`), weighted by the kernel (`lime_base.py` lines 189–205).
   `as_map()[1]` is the list of `(column, coef_j)`.

**Therefore `w_j` is the coefficient of `z_j` in a locally weighted linear fit of the class-1
probability: the change in probability per one training standard deviation of feature `j`**.

**Answers to the audit questions.**

| # | Question | Answer |
|---|---|---|
| 1 | Coefficients, contributions or other? | **Coefficients (slopes)** of a weighted ridge surrogate. [fact; demo] |
| 2 | Coordinates? | LIME's own standardisation of the explainer's training data, `z_j = (x_j − m_j)/s_j`, applied to Paper G's already preprocessed columns (scaled numerics; one-hot dummies with `m_j` = category share). Grouping then sums `w` over a feature's columns (`group_attr`). [fact] |
| 3 | Effect of standardisation | Units are "probability per s.d.", so magnitudes are comparable across columns; but the value does not depend on where the instance lies relative to the reference, so its sign is the direction of the local slope, not whether the feature's current value pushes the prediction up. [fact] |
| 4 | Role of kernel width 3.0 | Wider than the default (`0.75·sqrt(p)`, e.g. 2.12 for p = 8), so distant samples count more and the slope is closer to a global average over the mean-centred cloud; for a linear model it has no effect (demo: ρ = 1.000 between widths). Paper E measured that width 3 makes LIME far less instance-specific (`docs/reports/paper_e/README.md`). [fact; demo] |
| 5 | Predicted-class sign orientation | **Consistent.** All four explainers return class-1 quantities (`Lime` uses `labels=(1,)`; `Shap` selects class 1; `Occlusion` uses `[:, 1]`; `RandomControl` is sign-free); `orient` negates for predicted class 0; `true_attribution` is computed on the predicted-class probability (`scripts/paper_g_synthetic.py::true_attribution`). For a slope, negation correctly gives the slope of the predicted-class probability. [fact] |
| 6 | Is the synthetic comparison of like with like? | **No.** `spearman_truth` correlates LIME slopes with exact interventional Shapley **contributions**. For contributions `c_j ≈ w_j · z_j`, the rank correlation of `w` with `c` depends on the signs of `z_j`, which vary by instance; it averages near zero and differs by predicted class. [fact; demo: ρ(w, c) from −0.50 to +0.29 across six instances; ρ(w·z, c) = 1.000] |
| 7 | Metrics requiring contribution-valued inputs | **M1, M2, M3, M6** (feature order by *signed* attribution toward the predicted class, `order_of`, then masking to the baseline: "top" must mean "pushes the current prediction most", a contribution notion); **M4** (Pearson with single-feature masking drops, which are contributions relative to the baseline); **M5** (fits `f(x) − f(x masked on S)` on the summed attributions of `S`, i.e. additive contributions). [fact] |
| 8 | Metrics that can consume coefficients as importances | **M7 only, and only partly**: it ranks features by mean \|attribution\| over instances (`scripts/paper_g_run.py`, line 152), a magnitude-only global importance; \|slope per s.d.\| is a defensible global importance for numeric features. For one-hot groups, `group_attr` sums dummy slopes, which is not a defined importance (opposite-signed dummy slopes can cancel). [fact for the code; validity for categorical groups: hypothesis] |

### 2.2 Constructed demonstration (`review/lime_semantics_demo.py`, output beside it) [demo]

Toy model `p(x) = 0.5 + 0.04·β·(x − μ)` on 8 features with unequal scales; exact contributions
relative to the mean `c_j = 0.04·β_j·(x_j − μ_j)`; LIME configured exactly as in Paper G:

- LIME weight = `0.04·β_j·s_j` (slope per s.d.) to within 0.0007, **identical for every instance**;
- ρ(LIME weight, true contribution) per instance: −0.048, 0.286, −0.167, −0.500, −0.405, −0.024;
- ρ(weight × z, true contribution) = 1.000 for every instance;
- the package default (`discretize_continuous=True`): ρ = 0.595 with the contribution (coarser,
  contribution-like, not identical).

A linear toy is the case most favourable to `w·z`; for nonlinear models `w·z` is a first-order
approximation relative to the training mean, fitted on a mean-centred sample weighted toward the
instance (Section 8 does not assume it is valid).

### 2.3 Consistency with prior evidence in this repository [fact]

Paper E found the same mechanism after its sign agreement split by predicted class (0.977 vs 0.036
on Breast Cancer), converted slopes with `c_j = w_j·z_j`, and obtained sign agreement 0.945 / 0.960
/ 0.990 with no class dependence (`docs/reports/paper_e/scripts/paper_e_sign_contribution.py`).
Paper G shows the same signature in the synthetic check: LIME's mean `spearman_truth` is −0.111
for predicted class 0 and +0.128 for class 1 (Task 15 diagnostic, recorded in
`RESULTS_INTERPRETATION_2026-11-16.md`), and 0.00–0.02 overall, equal to the random control.

**Root cause (process):** Paper G reused Paper F's explainer code; Paper E's documented LIME
semantics were not checked when Paper G's plan defined metrics on signed contributions. Per ACE
("every issue requires RCA"), this warrants **RCA-005** with a guard (Section 7, R9).

---

## 3. Validity by research question and result

| Result | Impact class | Basis |
|---|---|---|
| **H1 primary (0.723; decision "broadly agree")** | **Potentially biased**; interpretation requires qualification | LIME's slopes are scored by contribution-based metrics (M1–M6), which plausibly places LIME consistently, and a consistently extreme explainer forces every pairwise Spearman into {0.5, 1} (Section 4.1). Existing outputs support a stable SHAP–LIME order: across M1–M4 and M6 there is **no** strict SHAP–LIME reversal in any of the 160 blocks (`sensitivity/shap_lime_reversals.csv`). Whether LIME is the consistently placed explainer is **not yet shown** (diagnostic R3). |
| **H2 (0.154)** | Interpretation requires qualification | One quarter of the H2 blocks are LIME explanations, whose metric values evaluate a slope ordering; the three-explainer sensitivity is similar (0.147, `sensitivity/h2_sensitivity.csv`). Prediction-level nuisance (Section 4.2) is a plausible further distortion. |
| **Winner flips** | Interpretation requires qualification | Flips are informative about SHAP vs occlusion; the share involving LIME is affected by its representation. M7 drives most flips (49–64%, `sensitivity/winner_flips.csv`). |
| **SHAP–LIME reversals** | **Invalid under the intended estimand** for M1–M6; qualified for M7 | Under M1–M6 the comparison is SHAP contributions vs LIME slopes, both scored as contributions; "how often the SHAP–LIME order reverses" is not the intended comparison. Under M7 (magnitude-based) the comparison is closer to meaningful, but M7 is unstable (Section 4.3). |
| **Synthetic ground-truth validation** | **Invalid** for LIME's position; potentially biased overall | LIME's reference rank is a representation artifact. With four ranked explainers, a metric that separates {SHAP, occlusion} from {LIME, random} scores high regardless of LIME vs random order (Section 5). |
| **M7 comparisons** | Interpretation requires qualification | Legitimate magnitude input for numeric features; questionable for summed one-hot slopes; low within-metric stability (0.384, `confirmatory/stability_dataset_metric.csv`) and 10.6% tied winners. |
| **Central conclusion ("partly agree")** | Interpretation requires qualification | The direction (system-level agreement above instance-level; strong dependence on M7 and baseline) is robust to the LIME issue in kind but not in size; "broadly agree" needs the floor caveat and the LIME restriction. |

Not inferred: that LIME is intrinsically less faithful. The data show that LIME **as configured**
outputs a quantity the metrics and the truth do not expect.

---

## 4. Statistical review

### 4.1 H1

- **Decision floor. [fact, derivation]** For n = 3 items without ties, Spearman ρ = 1 − 6Σd²/24.
  If one item has the same extreme rank (1 or 3) under both raters, the only possible disagreement
  is a swap of the other two: Σd² = 2, ρ = 0.5. Hence if any explainer is consistently first or
  last across all seven metrics in a block, that block's mean pairwise Spearman is in [0.5, 1]. The
  frozen decision table's threshold 0.5 (inherited from Paper F, where four explainers were ranked
  with datasets as raters) then
  separates nothing below "one explainer is always last". The power simulation did not consider this
  structure. **Qualification required** in any reading of "broadly agree".
- **Three items** give coarse statistics (ρ ∈ {−1, −0.5, 0.5, 1} without ties) and little
  discrimination; with the random control (four items) agreement rises to 0.753, as expected
  because every metric can rank a random attribution low.
- **Against the stability benchmark** (0.873; intervals do not overlap) the gap is informative, but
  the benchmark is dominated by highly stable metrics (M4 = 1.000) and pulled down by M7 (0.384).
- **Permutation test.** Valid for its null (metrics order explainers independently, dataset as
  unit); rejection is near-certain whenever one explainer is systematically disadvantaged, so
  p = 1/100,001 (the floor) says little about strength.
- **Undefined correlations:** 18 of 3,360 (M7 ties), excluded as specified; negligible effect.

### 4.2 H2

- **Nuisance variation. [hypothesis]** M1 (deletion AUC) and M2 (insertion AUC) both rise with the
  instance's predicted probability `f(x)` and its baseline value; after orientation M1 is negated,
  which induces a negative correlation unrelated to explanation quality — consistent with the
  observed M1–M2 −0.351 (`confirmatory/h2_pairs.csv`). M3 and M6 are differences that also scale with
  `f(x)`. The records store `f_x`, so partial correlations given `f(x)` are possible (R6).
- **Inference** (one-sided t on eight dataset values) is a post-execution amendment; the sign-flip
  test (all eight positive, p = 1/256) and bootstrap agree. Negative pairs were not tested (the
  family is one-sided); they are descriptive.
- **Holm over 15 pairs** is correctly separate from the H1/H2 family.

### 4.3 M7

- **Instability** (0.384 across seeds) has several sources [hypothesis, not separated]: (i) the
  retrained models differ by seed through the split; (ii) small drops in AUC are noisy; (iii) with
  few features the removal sets coincide — `n_top` gives 1, 1, 2, 3 features for 5 groups (phoneme)
  [fact], so two explainers with the same top feature remove identical sets and tie (10.6% tied
  winners, `sensitivity/winner_flips.csv`); (iv) global rankings depend on attribution magnitudes
  (LIME's summed dummy slopes on mixed datasets).
- M7 is the main source of winner flips and SHAP–LIME reversals; its role should be reported as
  "the retraining metric disagrees and is itself unstable", not as evidence about explainers.

### 4.4 Inference in general

- Eight datasets, t-intervals with 7 d.f.: inference is to datasets like these, not to tabular data
  in general; dataset values range widely (H1 0.578 electricity to 0.859 phoneme,
  `confirmatory/h1_datasets_spearman.csv`).
- Dataset independence is assumed; the datasets come from one OpenML pool and share no records.
- Holm (H1, H2) is correct; the raw and adjusted conclusions coincide, so O1 does not bite here.
- Ties: average ranks; M7 is the only metric with frequent ties.
- Degenerate M4 (147 rows) does not change any block's order (verified in PR #129).

---

## 5. Synthetic ground-truth review

- **Ground truth:** interventional Shapley values of the predicted-class probability over 500
  background rows; the metrics mask to the training mean. Close but not identical references (the
  same limitation Paper E recorded). [fact]
- **Design:** 4 conditions × 5 seeds, 8 features, two function families; descriptive only. [fact]
- **Comparability:** SHAP and occlusion output contributions; LIME outputs slopes (Section 2); the
  random control outputs noise. LIME's and the random control's truth agreement are both ≈ 0, so
  their reference order is arbitrary. [fact]
- **What the agreement measures:** in every block LIME ranks 3rd or 4th and the random control 3rd or
  4th (`synthetic/four_reference.csv`); SHAP and occlusion share ranks 1 and 2. With four items a
  metric that separates the two pairs scores 0.8 or 1.0 depending on two essentially arbitrary
  pairwise orders. The reported 0.76–0.92 therefore mostly measure pair separation plus the SHAP vs
  occlusion order. **The three-explainer sensitivity still contains LIME** and does not remove the
  problem.
- **Defensible from the synthetic check:** descriptive statements about whether metrics order SHAP
  and occlusion as the truth does, and how this degrades with interactions; not statements about
  LIME.

---

## 6. Threats to validity

| Threat | Type | Status |
|---|---|---|
| LIME slopes scored as contributions | construct | **demonstrated** (code, library source, demo, Paper E) |
| H1 floor at 0.5 with a consistently placed explainer | statistical conclusion | derived; occurrence in data not yet shown |
| Shared masking baseline and machinery across M1–M6 | construct | built-in; second baseline lowers H1 to 0.616 |
| Occlusion–M4 shared single-feature removal | construct | known; six-metric analysis 0.690 does not isolate it |
| One-hot columns sampled as continuous by LIME (off-manifold queries) | construct | fact for the code; effect on mixed datasets unknown |
| Prediction-level nuisance in H2 | construct | hypothesis |
| M7 noise and small-`G` ties | reliability | fact (ties, n_top); size of noise unknown |
| Eight datasets, one OpenML pool | external | fact |
| Post-execution amendments (plan 11) | statistical conclusion | recorded; decided before unblinding |
| Retrospective eligibility gate | internal | recorded; all eight pass |
| Variance decomposition omitted | completeness | recorded deviation |
| Draft misdescribes LIME ("default kernel"; no mention of slopes, mean-centred sampling) | reporting | fact |

---

## 7. Ranked improvement recommendations

Ranked by scientific impact. "Required" means before submission.

**R1 — Disclose and restrict the LIME estimand. Critical. Required.**
Location: `paper_g_draft.md` §3.4, §3.5, §3.7, abstract; `RESULTS_INTERPRETATION_2026-11-16.md`.
Evidence: Section 2. Rationale: the metrics' construct does not match LIME's output.
Action: describe LIME exactly (`discretize_continuous=False`, kernel width 3, sampling around the
training mean, slopes per s.d.); state that M1–M6 and the synthetic truth assume contributions; label
every LIME-involving result "LIME as configured (slopes)". Benefit: prevents an invalid claim.
Computation: none. Effort: small. Preregistration risk: none (reporting). Class: reporting improvement.

**R2 — Withdraw the SHAP–LIME reversal claim for M1–M6 and the synthetic statements about LIME. Critical. Required.**
Location: draft §4.3, §4.5, abstract ("the order of SHAP and LIME reversed …"). Evidence: Section 3.
Action: remove or restrict to M7 with the instability caveat. Effort: small. Risk: none. Class: correction (reporting).

**R3 — Qualify H1 with the decision floor; add an explainer-position diagnostic. Major. Qualification required; diagnostic strongly recommended.**
Location: plan §11 (new entry), draft §3.7/§4.2. Evidence: Section 4.1; no SHAP–LIME reversal
across M1–M4, M6. Action: report, per metric and dataset, how often each explainer is ranked 1st/2nd/3rd
(from existing block means; no new experiment), and H1 restricted to {SHAP, occlusion} (pairwise order
agreement). Benefit: shows whether "broad agreement" means "agree on the worst explainer". Computation:
seconds on stored outputs. Effort: small. Risk: none if labelled exploratory and added after
unblinding. Class: exploratory analysis.

**R4 — Supplementary LIME experiment with a contribution-valued representation. Critical for any LIME claim; Major for the paper. Recommended (required only to keep LIME in the paper's claims).**
See Section 8 (S3 then S1 or S2). Class: supplementary experiment.

**R5 — Correct the draft's method description. Major. Required.**
Location: draft §3.4 ("with its default kernel" is wrong; width 3.0), §3.5 (state signed ordering for
M1–M3/M6 and contribution assumption), §3.6 (truth reference vs metric baseline). Class: reporting.

**R6 — H2 adjusted for prediction level. Major. Optional, recommended.**
Location: new exploratory output. Evidence: Section 4.2 (M1–M2 −0.351; M5–M6 −0.181). Action: partial
Spearman of metric pairs given `f_x` (stored), same dataset-level aggregation; report beside, never
instead of, H2. Computation: seconds. Risk: low if exploratory. Class: exploratory analysis.

**R7 — Characterise M7. Major. Reporting required; analysis optional.**
Action: report `n_top` per dataset, tie frequency, and that M7 drives flips; optionally the share of
blocks where two explainers remove the identical feature set. Computation: seconds. Class: reporting + exploratory.

**R8 — Restate the synthetic check as a {SHAP, occlusion} check. Major. Required (reporting); supplementary S3 recommended.**
Evidence: Section 5. Class: reporting improvement.

**R9 — RCA-005: inherited explainer semantics not checked against the metric construct. Major. Required by ACE.**
Location: `docs/rca/`, `regression-guards.yaml`. Action: RCA with a guard (e.g., a test that each
explainer's output type is declared and matches the metrics' expected input; plan template item:
"state what each explainer returns"). Class: correction (process).

**R10 — Give the baseline sensitivity due weight. Minor→Major (reporting). Required.**
H1 falls from 0.723 to 0.616 under the second baseline; the draft should state that the masking
baseline is a major source of disagreement, as the plan anticipated (§3.1). Class: reporting.

**R11 — Abstract claim with no planned output. Minor. Required.**
The abstract scaffold says "All metrics placed the random control last in [R: share] of conditions";
no output computes this. Either remove it or compute it as an exploratory diagnostic (seconds).
Class: reporting / exploratory.

**R12 — Per-dataset heterogeneity. Minor. Optional.** Report dataset values (0.578–0.859) in a figure
(Figure R1 exists). Class: reporting.

**R13 — Replacement for the omitted variance shares. Minor. Optional.** E.g. a model of
explainer × {metric, dataset, model} interaction on the ranks; only as a separately proposed
exploratory analysis. Class: exploratory.

**R14 — Report cosmetics. Minor. Optional.** `n` printed as 8.000 in Tables R3/R4 of
`RESULTS_REPORT.md` (generated; fix in the generator for any future run, not by editing).

**Required before submission:** R1, R2, R3 (qualification), R5, R7 (reporting), R8, R9, R10, R11.
**Optional/recommended:** R3 diagnostic, R4, R6, R12, R13, R14.

---

## 8. Supplementary experiment options (not implemented, not run)

All share these safeguards: a new plan section (§12) written and committed **before** any run;
a distinct stage name and output directory (e.g. `lime_supp`), never overwriting the frozen run;
results reported as **supplementary**, beside — never replacing — the confirmatory H1/H2.

| Option | What | Validity argument | Cost (measured run-host times as reference) |
|---|---|---|---|
| **S3. Focused synthetic validation of LIME representations** (do first) | On the four synthetic conditions, compare to the exact truth: (a) raw slopes, (b) `w·z` relative to the training mean, (c) `discretize_continuous=True`, (d) default kernel width | Tests, rather than assumes, whether any transformation recovers contributions for nonlinear and interaction models | Synthetic stage took about 25 s; S3 ≈ minutes. Methodological cost: small |
| **S1. Post-hoc contribution transform** `c_j = w_j·z_j` with LIME's own `m`, `s` | Recompute M1–M7 for LIME only, with stored slopes and reconstructed instances (splits are deterministic by seed; Paper E did the same reconstruction with hash checks) | Exact for a linear surrogate; for nonlinear models a first-order contribution relative to the training mean; the metrics' baseline is the mean for numerics but the **mode** for categorical groups, so the references differ for one-hot features | No new LIME sampling. Metric recomputation needs refitted models: bounded by the full stage (18.5 min, all explainers) plus ROAR for LIME (≤ about 20 min of the 81 min). Effort: 1–2 days of code + tests |
| **S2. Controlled alternative LIME configuration** | Re-explain with the package default `discretize_continuous=True` (declaring categorical columns), and the default kernel width, as a second LIME condition | Uses LIME as most users run it; weights are bin-indicator effects, contribution-like but coarser (demo ρ = 0.595 on the linear toy) | Full LIME re-explanation on all shards: bounded by 18.5 min + ROAR LIME ≈ 20 min + synthetic seconds. Effort: 1 day |
| **S4. Limited pilot before any full rerun** | S1 or S2 on 2 datasets × 4 models × 1 seed | Checks semantics and cost before committing | Minutes |

Recommended path: **S3 → (S1 or S2, chosen by S3's outcome) → S4 → full supplementary run**.

---

## 9. Publication-readiness assessment

**Scenario A — LIME representation valid for the comparisons.** Not supported by the evidence
(Section 2). Listed for completeness.

**Scenario B — qualify, keep the existing analysis (no new experiment).**
- Defensible: metrics agree well above chance on the system-level order of the three explainers *as
  configured*, with agreement below within-metric stability, sensitive to the masking baseline and
  strongly broken by the retraining metric; instance-level agreement is weak (0.154) and some pairs are
  opposed; descriptive synthetic evidence on SHAP vs occlusion.
- Withdraw or qualify: "broadly agree" (floor caveat, R3); every SHAP–LIME statement (R2); synthetic
  statements about LIME (R8); any implication that LIME is less faithful.
- Journal objections to expect: "the agreement is driven by a mis-specified explainer"; "three items";
  "post-hoc amendments". B answers them by narrowing the claim. Publishable as a methods-caution paper.

**Scenario C — supplementary experiment needed.**
- With S3+S1/S2, the paper can state whether H1's agreement survives a contribution-valued LIME, which
  directly addresses the main reviewer objection and restores the SHAP–LIME comparison as a
  supplementary result. Strongest version; cost about one to two days of work plus under one hour of
  machine time; preregistration integrity preserved by §12 written before the run.

**Recommendation:** C if time allows before submission; otherwise B. In both, the confirmatory results
of PR #129 are reported unchanged.

---

## 10. Decisions requiring author authorization

1. Merge PR #129 as the unchanged record of the preregistered analysis (recommended in all scenarios;
   this review supersedes its provisional interpretation).
2. Scenario B or C.
3. If C: run S3 first; then S1 or S2; write plan §12 before any run; use stage `lime_supp`.
4. Exploratory diagnostics R3, R6, R7, R11 (seconds of computation on stored outputs).
5. RCA-005 and its guard (R9).
6. Draft corrections R1, R2, R5, R8, R10, R11 (methods and claims only; no `[R]` filled until decided).

---

**LIME VALIDITY: FAIL** (for the intended contribution-based comparisons; the stored values are valid
slopes and remain usable as "LIME as configured")

**H1 INTERPRETATION: QUALIFIED**

**H2 INTERPRETATION: QUALIFIED**

**SYNTHETIC VALIDATION: QUALIFIED** (valid only as a check on SHAP vs occlusion; invalid for LIME)

**ADDITIONAL EXPERIMENTS: RECOMMENDED**

**PR #129: READY FOR MERGE** (as the unchanged record of the preregistered analysis; its provisional
interpretation is superseded by this review)
