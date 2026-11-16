# Paper G — S1 results and interpretation

**Date:** 2026-11-16. **Status:** supplementary and exploratory (plan 12.3). The original H1/H2, their
decision and `RESULTS_REPORT.md` are unchanged and remain the confirmatory results. All numbers below
are from `outputs/analysis/paper_g/supplementary/s1/analysis/` (`S1_ANALYSIS_REPORT.md`) and
`exploratory_post/`, verified independently (`verification/verify_s1_independent_output.txt`, 37/37).
Estimates are means over the eight datasets with 95% t-intervals; no test was run and no decision
rule is applied to S1.

## 1. Question

Does the original system-level agreement among faithfulness metrics persist when LIME is represented
by surrogate contributions (S1-B: relative to the masking baseline; S1-M: relative to LIME's training
mean) instead of slopes?

## 2. Results

| Quantity | Original | S1-B | S1-M |
|---|---|---|---|
| H1-form mean pairwise Spearman (3 explainers, 7 metrics) | 0.723 [0.645, 0.802] | **0.529 [0.389, 0.669]** | 0.540 [0.389, 0.692] |
| Kendall's W | 0.762 [0.701, 0.824] | 0.588 [0.473, 0.703] | 0.598 [0.471, 0.725] |
| With the random control (4 explainers) | 0.753 | 0.757 | 0.762 |
| Second masking baseline | 0.616 [0.546, 0.687] | **0.309 [0.219, 0.398]** | 0.285 [0.212, 0.359] |
| Six metrics (no M4) | 0.690 | 0.483 | 0.489 |
| Within-metric stability benchmark | 0.873 | 0.797 | 0.798 |
| H2-form instance-level agreement (4 explainers) | 0.154 [0.099, 0.209] | 0.147 [0.095, 0.199] | 0.154 [0.097, 0.212] |
| H2-form adjusted for f_x (exploratory) | 0.233 | 0.225 | 0.235 |

**Explainer positions (3 studied explainers, 160 blocks).**

| | Original | S1-B | S1-M |
|---|---|---|---|
| Blocks with one explainer at the same extreme rank under all 7 metrics | 96 | 44 | 43 |
| ... LIME untied last under all 7 | 87 | 25 | 27 |
| LIME untied last under M1 / M2 / M4 (of 160) | 160 / 160 / 160 | 100 / 111 / 121 | 115 / 124 / 136 |
| Random control last under all 7 (4 explainers) | 15 | 126 | 128 |
| SHAP–LIME strict reversals, pairs of M1–M6 | 0.0–1.9% | 7.5–33.8% | 9.4–28.1% |
| SHAP–LIME strict reversals, pairs with M7 | 26.9–28.8% | 30.0–37.5% | 26.2–35.6% |
| Blocks with any SHAP–LIME reversal | 46 | 96 | 92 |
| Winner flips, pairs of M1–M6 | 6.9–31.2% | 7.5–40.6% | 7.5–39.4% |
| Winner flips, pairs with M7 | 49.4–63.8% | 49.4–62.5% | 46.2–59.4% |

**By dataset (H1-form).** Numeric datasets (magic_telescope, phoneme, qsar_biodeg; S1-B = S1-M by
construction): mean 0.758 → 0.484. Mixed datasets (adult, bank_marketing, compas, electricity,
german_credit): 0.703 → 0.557 (S1-B), 0.574 (S1-M). Per dataset, S1-B lowers agreement in seven of
eight datasets (largest drops: compas 0.639 → 0.271, qsar_biodeg 0.676 → 0.336); electricity rises
(0.578 → 0.759).

**M7.** Within-metric stability of M7 is unchanged (0.384 / 0.394 / 0.383); flips involving M7 stay at
about one in two blocks. LIME's mean M7 rises slightly (0.078 → 0.085).

**H2 pairs.** The pattern is unchanged: deletion–insertion stays negative (−0.351 → −0.407) and
infidelity–sufficiency negative (−0.181 → −0.121); the strongest pair stays M1–M3 (0.507 → 0.548).

## 3. Interpretation (observations first; explanations marked as such)

1. **S1-B changes H1-form agreement substantially.** It falls from 0.723 to 0.529, and its interval
   (0.389–0.669) now contains 0.5, which the original interval did not. Kendall's W falls likewise.
   *Observation.* No decision is attached to S1 (plan 12.3.4); the original "broadly agree" stays the
   frozen classification of the original analysis.
2. **LIME is no longer consistently last.** LIME untied last under all seven metrics drops from 87 to 25
   blocks; under each of M1–M6 it now ranks first or second in 24–42% of blocks (S1-B). The random control
   becomes the consistently last explainer (126 of 160 blocks under all seven metrics), which is what a
   negative control should do. *Observation.* *Interpretation:* much of the original agreement was
   agreement that LIME-as-slopes was worst — a shared response of contribution-based metrics to a
   representation mismatch, not agreement about the faithfulness of comparably represented explainers.
3. **Agreement becomes more informative and lower.** With the mismatch removed, the three explainers'
   order varies between metrics, so the H1-form value now reflects disagreement about competing
   explainers; the three-explainer floor still applies to the 44 blocks with a consistently extreme
   explainer.
4. **SHAP–LIME comparisons become interpretable and unstable.** Under M1–M6 they now compare
   contributions with contributions; the order reverses between metric pairs in up to a third of blocks
   (S1-B), and in 96 of 160 blocks at least once. *Observation.*
5. **The reference matters little at system level.** S1-B and S1-M differ by at most 0.024 in every
   summary quantity; they are identical on numeric datasets by construction. On mixed datasets S1-M is
   slightly higher. Conclusions do not depend on the choice.
6. **Numeric versus mixed.** The drop is larger on the numeric datasets (0.758 → 0.484) than on the mixed
   ones (0.703 → 0.557). With three numeric and five mixed datasets this is descriptive; dataset-level
   heterogeneity (compas, qsar_biodeg large drops; electricity a rise) is larger than the type effect.
7. **M7 remains a major source of disagreement,** unchanged by S1: its stability and its flip rates are
   the same in all three conditions.
8. **Instance-level agreement remains weak** (0.147 / 0.154), and the f_x adjustment raises it similarly
   in all conditions; the representation does not drive H2.
9. **The masking baseline becomes the dominant sensitivity.** Under the second baseline, S1-B agreement is
   0.309 (original 0.616): once LIME is comparable, the metrics' agreement on the explainers' order is
   strongly baseline-dependent.

**Overall.** S1 changes the reading of Paper G. The original system-level agreement (0.72, "broadly
agree") does not persist at that level once LIME is represented as contributions: agreement is moderate
(0.53), uncertain (interval spanning 0.5), strongly baseline-dependent, and accompanied by frequent
winner flips and SHAP–LIME reversals. Instance-level agreement is weak under every representation.

**Not concluded.** That contributions are the right representation of LIME in general; that S1-B or S1-M
is superior; that LIME is more or less faithful than SHAP. The categorical part of S1 rests on LIME's
off-manifold sampling of one-hot columns and on a surrogate approximation of the model; SHAP's reference
(background expectation) still differs from S1-B's (masking baseline); three explainers keep rank
statistics coarse; eight datasets bound the inference.

## 4. Publication assessment

| Direction | Evidence | Rank |
|---|---|---|
| **C. Aggregation level, attribution semantics and evaluation protocol** | Supported on every axis: system- vs instance-level (0.72/0.53 vs 0.15); semantics (slopes inflated agreement; S3 and S1); protocol (baseline 0.62/0.31, M7 instability, three-explainer floor, random control) | **1 (recommended)** |
| **B. Disagreement concealed by representation incompatibility** | Directly supported (0.723 → 0.529; LIME-last 87 → 25), but on one explainer and one configuration; strongest as a central finding inside C, overclaimed alone | 2 |
| **A. Qualified agreement among faithfulness metrics** | Only for the original representation; under S1 the estimate is moderate, uncertain and baseline-dependent | 3 |

**Recommended central contribution (C):** faithfulness metrics agree weakly on individual explanations and
only moderately on explainer rankings; apparent system-level agreement can be produced by an
explainer whose output type does not match the metrics' assumptions, and is sensitive to the masking
baseline and the retraining metric. Report the original confirmatory result unchanged, S1 as the
supplementary analysis that qualifies it, and the evaluation-protocol recommendations that follow.

**Claims supported:** weak instance-level agreement (H2, robust to representation); system-level agreement
inflated by the slope representation; baseline dependence; M7 instability; the need to declare explainer
output semantics (RCA-005).
**Claims requiring qualification:** "the metrics broadly agree" (original representation only);
any SHAP–LIME statement (S1 only, with surrogate and categorical caveats); dataset-type differences.

**Minimum remaining work before submission (each needs authorization):** rewrite results and discussion
around C with the original and S1 results side by side; fill `[R]` placeholders from registered claims
(RCA-001: register original and S1 claims through a resolver, as for Paper F); generate the figures by
committed scripts; references with verified DOIs; scientific-rigor review and reference audit; journal
template and declarations (including generative-AI use).

**S2** (LIME re-run with its package defaults) would add external validity ("LIME as commonly run") but
would not change the central claim: S3 places discretised LIME further from the truth than S1, and S1-B
and S1-M already agree. Optional; not required for submission.
