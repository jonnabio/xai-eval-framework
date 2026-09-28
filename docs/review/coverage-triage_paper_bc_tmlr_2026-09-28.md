# Coverage Triage: Paper B+C (TMLR submission)

**Date**: 2026-09-28 | **Reviewer role**: Scientific Advisor
**Plan**: `docs/planning/paper_bc_tmlr_remediation_plan_2026-09-28.md`, Step 0.2. Read-only: the
registry was copied to the scratchpad with both files added to `[coverage]`, and
`verify_claims.py --registry <copy> --coverage-report` was run on it. The committed registry is
unchanged.

**Result**: 73 unregistered numeric literals, all in `paper_bc_tmlr.tex` and
`paper_bc_tmlr_supplementary.tex`; every other covered file is clean. Each literal was re-derived or
classified as below. Line numbers are the verifier's.

## Summary

| Class | Count | Action (remediation Step 1 / 7) |
|---|---|---|
| Structural: layout, settings, thresholds, identifiers | 22 | declare structural |
| Result, re-derives from a committed artifact | 44 | register with a resolver |
| Result, cannot be re-derived | 4 | `[[unbacked]]` (Table S5) |
| Wrong value | 2 | fix, then retire the old text (`0.85`, `0.93` → F07) |
| Result, to be removed by another fix | 1 | none (`0.02` goes with F02/F03 edits if the caption changes; otherwise register) |

## Structural (22)

- TikZ and column geometry: `1.5`, `6.2`, `00.3`, `2.1`, `0.98` (main); `5.6`, `4.2`, `2.4`, `2.8`,
  `1.5` (supplementary).
- Protocol settings: `3.0` and `10.0` (kernel widths, main and supplementary); `0.0` (judge
  temperature, S1).
- Selection thresholds: `0.10`, `0.15` (S3).
- arXiv identifiers: `1702.08608`, `2411.15594`, `2505.22252`, `2510.20721`. These disappear or
  change with reference-audit R05.
- Prose thresholds for EXP4 summary: `0.55`, `0.35` (l.592-593: "α > 0.55", "α < 0.35"). These are
  bounds stated over registered α values; declare them structural, or register them as bounds.

## Results that re-derive (44)

| Literal(s) | Site | Re-derived from | Value |
|---|---|---|---|
| `0.663`, `0.773`; `0.181`; `0.236`, `0.260`; `0.041`, `0.049`; `3939.2`, `12155.9` | `tab:paired_main` 95% CIs | `paired_cells_shap_lime_all_models.csv`, mean paired difference ± t(74) SE | 0.6626/0.7726; 0.1807; 0.2361/0.2597; 0.0414/0.0493; 3939.23/12155.93: **all match** |
| `0.45`, `1.2` | `tab:paired_main` cost $d_z$, $p_{\mathrm{Holm}}$ | `wilcoxon_shap_lime_all_models.csv` | 0.4507, 1.18e-10: match |
| `0.866` | l.959 median paired stability difference | `wilcoxon...csv` `median_diff` | 0.8663: match |
| `5.3` | l.1022 median SHAP/LIME cost ratio | paired cells, median of per-cell ratios | 5.265: match, **but see F17** |
| `51456`, `67066`, `12825`, `13192` | l.1024-1025 P90/P95 cost | paired cells, inclusive quantiles | 51,456 / 67,066 / 12,825 / 13,192: match |
| `694.6`, `53.3` | Tier 1 non-tree medians (also in the abstract, where they are registered) | paired cells, logreg+svm+mlp | 694.56 / 53.31: match. Register the paper site under the abstract's claim. |
| `0.23`, `0.24`, `0.21` | l.1080-1083 SHAP−LIME EXP3 gaps and Adult XGB gap | EXP3 SHAP (Anchors + gap) − `exp3_lime_results.csv` | GC RF 0.231, GC XGB 0.243; Adult RF 0.272, XGB 0.206 (paired cells): all match. A composing resolver is needed. |
| `0.363` | `tab:exp3_fidelity` GC/RF gap | EXP3 tree | +0.363, as already recorded in the registry's retired-guard reason for GC/RF; add it as a claim on the existing `exp3_shap` resolvers |
| `0.457`, `0.553` | `tab:exp3_lime` caption, LIME Adult RF/XGB fidelity | paired cells, per-model LIME mean | 0.457 / 0.553: match. The caption's "≈0.01--0.02" also matches (per-model LIME stability 0.007-0.019) |
| `12.3`, `7.5`, `21.1`, `10.2`, `0.163` | `tab:exp3_lime` cost and sparsity | `exp3_lime_results.csv`, 3-seed mean | 12.333, 7.533, 21.067, 10.2, 0.163: match |
| `25.0` (main l.479, S4) and `62.5`, `0.802`, `56.2`, `0.771`, `81.2`, `0.906`, `0.784` | audit agreement, Table S4 | `second_reviewer_audit_results.csv` (exact set match; mean Jaccard) | 25.0/0.657, 62.5/0.802, 56.2/0.771, 81.2/0.906, 12 adjudicated, 0.784: **all match** |
| `0.000`, `0.087` | Table S2, kw=3.0 stability and sparsity | same source as the registered S2 claims (e.g. `0.093`) | not yet re-derived here; register on the S2 resolver in Step 1, which checks it |
| `0.081`, `0.053` | Table S6 gaps, marginal and grouped | `exp6_paired_shap_lime.csv` `topk_gap` | register beside the registered zero/mean rows |

## Cannot be re-derived (4)

`0.452`, `0.011`, `0.459`, `0.016`: Table S5 rows 500 and 2000. The reference row (0.461/0.014) was
found registered, so it is covered by an existing entry that should be reviewed at the same time.
Handled by rigor-review F05: `[[unbacked]]` with the RCA-002 reason, plus the thesis disclosure.

## Wrong (2)

`0.85`, `0.93` (l.1082, and l.1372 as the same range): the range excludes GC/XGB 0.748. This is
rigor-review F07. Fix it to 0.75-0.93 and retire the old text.

## New findings raised by this triage

These are added to the remediation plan as F16 and F17.

- **F16 [minor], EXP6 sample misstated, significance not reported.** Main l.1396 ("the $n=50$ RF
  runs across five seeds") and S6 ("$n=50$ runs, 5 seeds") both misdescribe the probe.
  `exp6_summary.json` and `exp6_paired_shap_lime.csv` show $N=50$ is the sampling-intensity
  stratum: **5 paired runs** (one per seed), at most 40 instances each. With 5 pairs the exact
  Wilcoxon minimum is $p=0.0625$ (Holm 0.5) on every scheme, so "robust" can only mean
  directional consistency (5/5), not significance.
  **Fix**: "the five RF runs at $N=50$ (one per seed)"; state that the 5/5 sign agreement is
  descriptive and that $n=5$ cannot reach $\alpha=0.05$.
- **F17 [minor], cost ratio wording.** l.1020-1022: "Matched-cell median cost is 684.1 ms for SHAP
  versus 65.7 ms for LIME, corresponding to a median SHAP/LIME cost ratio of approximately $5.3\times$".
  The ratio of those medians is 10.4. The 5.3 is the median of per-cell ratios (5.27), a different
  statistic.
  **Fix**: "the median per-cell SHAP/LIME ratio is 5.3×". Drop "corresponding to".
