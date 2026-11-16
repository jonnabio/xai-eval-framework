# Paper G — Provisional interpretation of the frozen analysis (2026-11-16)

For the author. Written from the generated outputs (`outputs/analysis/paper_g/analysis/`,
`RESULTS_REPORT.md`) and their independent verification only; no analysis was added. Not
manuscript text, and not reviewed yet (the post-analysis quality review has not started).

**Run:** one authorized execution, 2026-11-16 01:17 UTC, code `26ef7106f` (analysis code
`c56efa642`), data frozen at `04c6dfd84`, exit 0. Record: `verification/analysis_run_provenance.txt`.
**Verification:** independent re-computation (own loader, scipy/statsmodels), 0 failed checks
(`verification/verify_results_independent.log`).

## A. H1 — system-level agreement (three studied explainers, seven metrics, n = 8 datasets)

- Mean pairwise Spearman between metrics **0.723 (95% CI 0.645 to 0.802)**; Kendall's W 0.762
  (0.701 to 0.824). Permutation p = 0.00001, the smallest value 100,000 permutations can give;
  Holm-adjusted p (H1, H2) = 0.00002.
- **Decision table (raw p): "the metrics broadly agree"** (interval entirely above 0.5). The
  Holm-adjusted conclusion is the same.
- Against the **within-metric stability benchmark, 0.873 (0.826 to 0.920)**, between-metric
  agreement is lower by about 0.15, and the two intervals do not overlap. The benchmark is very
  uneven across metrics: M4 is perfectly stable across seeds (1.000) and M7 is not (0.384).
- Dataset means range from 0.578 (electricity) to 0.859 (phoneme); all eight are above 0.5.
- 18 of the 3,360 metric-pair correlations were undefined (all three explainers tied under M7
  in a block) and were excluded as specified.

Reading: the seven metrics order SHAP, LIME and occlusion similarly far more often than chance,
and the agreement is in the "broad" band of the preregistered rule. It is clearly below the
agreement of a metric with itself across seeds.

## B. H2 — instance-level agreement (six metrics, four explainers)

- Omnibus mean of the 15 pair correlations **0.154 (95% CI 0.099 to 0.209)**; one-sided t
  p = 0.00016 (Holm 0.00016); exact sign-flip p = 0.0039 (all eight dataset values positive);
  bootstrap sensitivity 0.112 to 0.198. Three studied explainers only: 0.147 (0.091 to 0.202).
- **Supported:** the mean instance-level agreement is positive. **Its size is small**: metrics
  agree only weakly on *which individual explanations* are good.
- Pairs (Holm over 15, one-sided for a positive mean): seven pairs are supported as positive —
  M1–M3 (0.51), M3–M4 (0.43), M1–M4 (0.38), M1–M6 (0.30), M4–M6 (0.28), M2–M4 (0.24), M3–M5
  (0.18). Three pairs have negative estimates with intervals below zero: **M1–M2 −0.35
  (−0.58 to −0.12)**, **M5–M6 −0.18 (−0.25 to −0.12)**; M2–M5 −0.09 (interval includes 0). The
  test was one-sided for positive agreement, so the negative pairs are descriptive, not tested:
  after orientation, deletion and insertion tend to rank the same explanations in *opposite*
  order. (A plausible mechanism, not examined: both AUCs scale with the instance's predicted
  probability.)

## C. Synthetic ground-truth check (descriptive; 20 condition × seed blocks)

- Agreement of each metric's explainer order with the reference order (four explainers):
  M1 0.92, M3 0.91, M4 0.85, M2 0.81, M6 0.81, M5 0.76. With interactions, most metrics agree
  less (e.g. M2 0.96 in the additive-independent condition, 0.64 in interaction-correlated; M6
  0.88 additive-independent, 0.64 interaction-independent); M3 does not drop (0.88 to 0.96).
  Three studied explainers: M3 1.00, M1 0.95, M2/M4/M6 0.75, M5 0.55.
- No test was planned; these are descriptive. M1 and M3 recover the reference order most
  consistently; M5 least.
- **Caveat that changes how this is read (see the major issue below):** in the reference order
  LIME is never above occlusion or SHAP and is below the random control in 9 of 20 blocks.
  LIME's mean agreement with the exact Shapley values is 0.00 to 0.02 in every condition, the
  same as the random control (SHAP 0.91 to 0.96; occlusion 0.68 to 0.97). The synthetic check
  therefore mainly tests whether a metric separates {SHAP, occlusion} from {LIME, random}.

## D. Robustness and sensitivity

| Analysis | Mean pairwise Spearman (95% CI) | Note |
|---|---|---|
| Primary H1 | 0.723 (0.645–0.802) | |
| With the random control (4 explainers) | 0.753 (0.700–0.806) | the control raises agreement, as expected |
| Second masking baseline | **0.616 (0.546–0.687)** | the largest drop; still above 0.5 |
| Without M4 (six metrics) | 0.690 (0.602–0.777) | removes M4 for all explainers; does not isolate the occlusion–M4 overlap |
| Degenerate M4 excluded (exploratory) | 0.723 (identical) | no block's explainer order changed |
| Per model | logreg 0.798, xgb 0.788, mlp 0.671, **rf 0.637** | descriptive |

- **Winner flips** (the top explainer changes between two metrics): 7% to 31% of blocks among
  pairs of M1 to M6; **49% to 64% for every pair involving M7**, plus 10.6% of blocks where M7
  ties at the top.
- **SHAP–LIME order:** never reverses among M1–M4 and M6; reverses in 1.9% of blocks against M5
  and in 27–29% against M7. 46 of 160 blocks show at least one strict reversal, almost all
  because of M7.
- Unfavourable for a "metrics agree" reading: M7 (ROAR-lite) disagrees with the other metrics
  far more than they disagree among themselves, and it is unstable across seeds (0.384). The
  baseline matters: changing the masking baseline lowers agreement by about 0.1.

## E. Limitations

1. **Major — LIME as configured is not an attribution of contributions.** The explainer code
   (inherited from Paper F, hard-coded, not in `config.toml` or the plan) runs LIME with
   `discretize_continuous=False`; its weights are then local slopes of standardised features,
   not contributions, while SHAP, occlusion, the metrics and the synthetic truth treat the
   vector as contributions. The synthetic check shows LIME's attributions unrelated to the truth
   even for an additive model with independent features, and LIME's agreement differs in sign by
   predicted class (−0.11 for class 0, +0.13 for class 1). This mechanism is inferred from the
   code and not yet verified. Every result involving LIME (H1, SHAP–LIME reversals, the
   synthetic reference) must be read as "LIME in this configuration". The draft also says
   "with its default kernel", while `kernel_width = 3.0`.
2. Eight datasets carry all inference; intervals are t-intervals with 7 degrees of freedom.
3. Three ranked items make each block's rank correlations coarse (values in {−1, −0.5, 0.5, 1}
   without ties); high agreement can reflect a consistently placed explainer.
4. Metrics share perturbation machinery (masking with the same baseline; M4 and occlusion use
   the same single-feature removal), so part of the agreement is built in; the second-baseline
   and no-M4 analyses bound but do not remove it.
5. Post-execution amendments (plan section 11): the H2 test, the stability benchmark, the synthetic
   statistic and tie rules were fixed after the run, before any result was seen.
6. The eligibility gate ran after the experiment (all eight datasets met it).
7. The planned variance-share decomposition was omitted.
8. The synthetic check uses one dimension (8 features), two function families and a
   known-function "model"; it does not generalise to trained models on real data, and with LIME
   near zero it discriminates mainly between two pairs of explainers.

## F. Central question (provisional)

*Do common faithfulness metrics agree on which post-hoc explanation method is more faithful on
tabular data?*

**Partly.** On the coarse order of SHAP, LIME and occlusion within a dataset, model and seed,
the seven metrics agree more than chance and, by the preregistered rule, broadly (0.72, interval
above 0.5), and this survives the random-control, baseline and no-M4 sensitivity analyses. The
agreement is nevertheless clearly below each metric's own stability across seeds, it depends on
the masking baseline and the model, and the retraining-based metric (M7) frequently names a
different winner. On *which individual explanations* are faithful, the metrics agree only weakly
(0.15), and some pairs (deletion versus insertion; infidelity versus sufficiency) order instances
in opposite directions. A claim that one explainer is "more faithful" is therefore reasonably
stable across the removal-based metrics for this explainer set, but not across all metrics, and
not at the instance level. All statements involving LIME are conditional on the LIME
configuration issue above, which the quality review should resolve first.
