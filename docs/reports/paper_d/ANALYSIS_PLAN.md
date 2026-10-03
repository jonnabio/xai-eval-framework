# Paper D — analysis plan (written before any result is computed)

**Question:** *Are explanations less reliable when the model is wrong?*
**Status:** plan, 2026-10-03. This file is committed **before** the analysis is run, so the
hypotheses, metrics, tests and corrections are fixed in advance. Any change after results
are seen is recorded in §9 with its reason, and the paper reports it.

---

## 1. Motivation

Explanations matter most where the model fails: an auditor or a decision-maker looks at an
explanation precisely to understand a questionable prediction. Benchmarks usually report
explanation quality averaged over all instances, which hides any difference between
correct and incorrect predictions. If explanations are less faithful or less stable on
misclassified instances, an explanation can look most convincing exactly where it should be
trusted least.

## 2. Research questions

- **RQ1.** Does explanation quality differ between correctly and incorrectly classified
  instances, for each of SHAP, LIME, Anchors and DiCE?
- **RQ2.** Does that difference depend on the model family (logistic regression, random
  forest, XGBoost, SVM, MLP)?
- **RQ3.** Among errors, do false positives and false negatives differ?
- **RQ4 (control).** Is any difference explained by proximity to the decision boundary?
  Misclassified instances tend to lie near it, and some quality metrics may depend on the
  prediction margin rather than on correctness itself.
- **External check.** Does the RQ1 pattern hold on a second dataset (EXP3 German Credit;
  SHAP and Anchors only)?

All tests are **two-sided**. There is no confirmed prior for the direction, so none is
assumed.

## 3. Data (existing; no new experiment)

- **EXP2, UCI Adult:** `experiments/exp2_scaled/results/<model>_<method>/seed_*/n_*/results.json`.
  Inventory on 2026-10-03:
  - 299 run files: 5 model families × 4 methods × 5 seeds × 3 sampling intensities
    (n = 50, 100, 200 per quadrant), minus one missing SHAP run.
  - About 123,000 instance-level explanations.
  - Each instance records its error quadrant (TP, TN, FP, FN), whether the prediction was
    correct, five per-instance quality metrics, and its top-10 attributions.
  - Quadrants are sampled in balance by design.
- **Trained models:** `experiments/exp1_adult/models/*.joblib` and `preprocessor.joblib`.
  These are used only for RQ4, to recompute each instance's predicted probability. The
  probability was not stored in the run files.
- **EXP3, German Credit:** `experiments/exp3_cross_dataset/results/german_credit/{rf,xgb}_{shap,anchors}/`.
  12 runs with per-instance data; FP and FN counts of 13–37 per run. Breast Cancer is
  **excluded**, because it has only 1–4 errors per quadrant per run, too few to compare.

## 4. Variables

- **Correctness** (primary contrast): correct = TP ∪ TN; misclassified = FP ∪ FN.
- **Quality metrics:** the per-instance metrics of the benchmark instrument, with
  definitions as in the thesis (Chapter 3) and Paper A, cited, not re-derived here.
  - Primary: **fidelity**, **stability**, **faithfulness gap**.
  - Secondary: **sparsity**.
  - Descriptive only: **cost**. Cost is not a quality property, but slower explanations on
    errors would still be worth reporting.
- **Prediction margin** (RQ4): |p̂ − 0.5|, where p̂ is the positive-class probability of the
  stored model for that instance.

## 5. Unit of analysis and statistics

Instances are nested in runs, and runs are the replicates. Instance-level tests would treat
thousands of non-independent explanations as independent, so they are **not** used for
inference.

- **Per run:** Δ = mean metric on misclassified − mean metric on correct instances. One Δ per
  run × metric.
- **RQ1:** for each method × primary metric (4 × 3 = 12 tests), a Wilcoxon signed-rank test
  of median Δ = 0 across runs.
  - Report: median Δ, mean Δ with 95% CI, and d_z.
  - **Holm correction across the 12 tests**, α = 0.05.
  - Sparsity is run as 4 further tests, Holm-corrected as their own family.
- **Robustness of RQ1:** average Δ over the three sampling intensities within each (model,
  seed), giving 25 units per method, and repeat. A conclusion is reported as firm only if
  both analyses agree in direction and significance.
- **RQ2:** Δ by model family, descriptively (median and range across seeds), plus one
  Kruskal–Wallis test per method × primary metric across the 5 families, Holm-corrected
  (12 tests).
- **RQ3:** per run, Δ_FP−FN = mean on FP − mean on FN. Wilcoxon signed-rank per method ×
  primary metric, Holm-corrected (12 tests).
- **RQ4:**
  - Per instance, regress metric on misclassified + margin, with run fixed effects.
  - Compare the misclassified coefficient with and without margin.
  - Run this for each method × primary metric, with cluster-robust standard errors by run.
  - Also report the contrast within margin quintiles.
  - A difference counts as explained by the boundary when the coefficient shrinks by more
    than half and its CI includes zero.
- **External check:** the RQ1 procedure on German Credit (6 runs per method), reported
  descriptively plus a sign count. With 6 runs, a Wilcoxon test cannot reach α = 0.05 after
  correction, so no inferential claim is made from it.
- **Practical relevance:** |d_z| ≥ 0.5 and |median Δ| ≥ 0.05 on a 0–1 metric. A
  significant but smaller effect is reported as statistically detectable but small.

## 6. Exclusions and missing data

- Instances with no quadrant label (278 in total: 235 SHAP, 42 Anchors, 1 DiCE) are
  excluded.
- Instances with a missing value of the metric under test are excluded for that metric
  only. Counts are reported per method.
- Runs with fewer than 10 misclassified or 10 correct instances after exclusion are
  excluded and reported.
- Anchors and DiCE have incomplete grids (failed or non-converged runs). Their missingness
  is not random, which the paper states as in Paper A. All comparisons are within-run, so the
  missing runs remove units but do not bias Δ within the runs that exist.

## 7. Overlap guard (Papers A and B+C)

- Paper D reports **only within-run correct-versus-misclassified contrasts** and the
  analyses above. It reports no per-method mean level, no omnibus test and no SHAP–LIME
  paired contrast; those belong to Papers A and B+C and are cited.
- The cohort's provenance is stated as in Paper B+C §"Provenance of the Empirical Cohort".
- `paper_d.tex` is under the registry's `[exclusivity]` and `[coverage]`. The build fails if
  any Paper B+C result is printed, and `scan_shared_literals.py` is extended to Paper D
  before submission.

## 8. Outputs

- `scripts/pubs/paper_d_analysis.py` → `outputs/analysis/paper_d/` (one CSV per analysis,
  plus `metric,value` summaries for the registry's `paper_d:` resolver).
- `scripts/generate_paper_d_figures.py` → `docs/reports/paper_d/figures/`.
- Every printed number registered in `pub/claim_registry.toml` before the paper is built.

**Planned figures:**
- Δ per method and metric with CIs;
- Δ by model family;
- metric versus margin, by correctness.

**Planned tables:**
- RQ1 results;
- RQ3 results;
- RQ4 coefficients.

## 9. Deviations from this plan

Record each one here with its date and reason, before reporting it.

1. **2026-10-03, RQ4 restricted to reproducible runs.** Recomputing p̂ from the stored
   models reproduced the recorded predictions exactly for logistic regression, XGBoost, SVM
   and MLP, but only 75–82% for the random-forest runs made in January–February 2026; the
   random-forest runs made in April 2026 reproduce (≥ 99.5%). The model file has the same
   hash throughout the repository history, and neither the earlier preprocessor nor a
   freshly fitted one restores the agreement, so the model those runs used cannot be
   reconstructed. A run therefore enters RQ4 only if the stored model reproduces at least 99%
   of its recorded predictions. RQ1–RQ3 are unaffected: their correct/misclassified labels
   were assigned by the model that actually ran. Found by the reproduction check on the first
   RQ4 run, whose output had been printed; the 99% rule is a data-validity criterion fixed
   without regard to its effect on the coefficients, and both versions are archived in the
   analysis log of the commit that introduced this deviation.
2. **2026-10-03, implementation detail of RQ4 (not a change of plan).** The fixed-effects
   regression is computed by within-run demeaning, with CR1 cluster-robust standard errors
   by run; margin quintile edges are computed per explainer over all its instances. For the
   SVM, p̂ is the Platt-scaled probability, which can disagree with `predict()` near the
   boundary; the count is reported.
