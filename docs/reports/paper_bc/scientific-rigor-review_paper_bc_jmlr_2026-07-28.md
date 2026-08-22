# Scientific Rigor Review: Paper B+C (JMLR submission)

**Target**: `docs/reports/paper_bc/paper_bc_jmlr.tex` / `paper_bc_jmlr.pdf` ("From Fidelity to Semantics: A Taxonomy of XAI Evaluation Metrics and Paired Empirical Comparison of LIME versus SHAP")
**Date**: 2026-07-28 | **Reviewer role**: Scientific Advisor | **Skill**: `scientific-rigor-review` v1.0.0
**Grade**: **Accept** | **Mean score**: 4.0 | **Dimensions**: D1=4 D2=4 D3=4 D4=4 D5'=5 D6=3
**Post-fix status (2026-07-29)**: F01 (major) and F02 (minor) both fixed via captioning/disclosure-only corrections to `paper_bc_jmlr.tex`; recompiled clean both times. F03 (suggestion, supplementary tables) remains open. F04 (minor, new) was surfaced while resolving F02: the EXP4 analysis scripts are missing from the repository, so F02's explanation is well-evidenced circumstantially (via row counts) but not independently re-derivable from committed source — deliberately not papered over with a fabricated script citation. Scores above reflect the pre-fix assessment; re-review recommended only if further changes are made before submission.

## One-line summary

A well-scoped, unusually honest taxonomy-plus-benchmark paper whose primary paired inference (SHAP vs. LIME, n=75 matched cells) is fully evidence-verified against the underlying artifacts, but the pre-analysis Friedman/Nemenyi omnibus test misreports its own block count (claims n=75, computation used n=15), and a reliability table quietly mixes two sample sizes.

## Method note

Read `paper_bc_jmlr.tex` in full (1,880 lines: Introduction → Background → Taxonomy → Comparative Synthesis/Gaps → Empirical Benchmark (EXP2/EXP3) → Recommendations → Validity/Limitations → Conclusion). Cross-checked the manuscript's numerical claims against the underlying analysis artifacts referenced in §Code and Artifact Availability:
- `outputs/analysis/paper_a_exp2_stats/wilcoxon_shap_lime_all_models.csv`, `friedman_results.csv`, `nemenyi_stability.csv`, `analysis_summary.json`, `exp2_block_method_summary.csv`
- `outputs/analysis/exp3_lime_results.csv`
- `outputs/analysis/exp4_llm_evaluation/icc_analysis.csv`, `krippendorff_alpha.csv`
- `docs/reports/paper_bc/second_reviewer_audit_summary.md`
- Supplementary tex (spot-checked table references S2/S3/S5/S6 exist and are described consistently)

Did not independently re-derive the supplementary tables' numeric content, and did not re-run the analysis scripts.

## Strengths

- **Primary confirmatory result is fully evidence-verified.** All five paired endpoints in Table `paired_main` (stability $d_z=3.00$, sparsity $d_z=0.84$, fidelity $d_z=4.82$, faithfulness gap $d_z=2.63$, cost $d_z=0.45$) match `wilcoxon_shap_lime_all_models.csv` to the reported precision, including the Holm-adjusted p-values.
- **Exceptional reporting honesty (D5').** The paper explicitly reports a negative result (EXP4 LLM-judge ICC < 0.75 on all seven dimensions), discloses its own second-reviewer audit's weakest axis (25% exact agreement on quality-property coding) without softening it, and maintains a dedicated "Generalizability Boundary" table distinguishing what is confirmed vs. partially supported vs. out of scope.
- **Scope discipline (D3).** The explicit ranking-claim vs. validity-claim distinction (§Interpretation Scope), the "sparsity is a hyperparameter constraint, not an emergent property" caveat, and the axiom–metric-alignment discussion all pre-empt likely reviewer objections rather than overclaiming.
- **Real robustness probes, not just claims of robustness.** The `num_samples` and `kernel_width` sensitivity probes, and the EXP6 masking-scheme sensitivity check, are genuine ablation-style checks addressing plausible confounds (undersampling, kernel miscalibration, OOD masking) rather than assumed away.
- **EXP3 cross-dataset extension is honestly bounded** — the paper states outright that SHAP stability was not instrumented on the cross-dataset cohorts and frames the LIME stability finding as a "moderation hypothesis requiring further confirmation," not a settled result.

## Findings

### F01 [major, FIXED 2026-07-28] — D1 Evidence Relevance / D6 Methodological Rigor

- **Location**: §Empirical Benchmark → "Multi-Method Context (Friedman)" (line ~829) and Table `tab:friedman` caption (line ~839)
- **Evidence**: "we ran a Friedman test across all four methods in EXP2 ... on $n=75$ run means per method, treating $(g, s, N)$ combinations as blocks" and caption "Friedman omnibus test across four methods (EXP2, $n=75$ blocks, $k=4$)."
- **Observation**: `outputs/analysis/paper_a_exp2_stats/analysis_summary.json` records `n_complete_blocks: 15`, and `complete_blocks` lists only 15 `(model, N)` pairs (5 models × 3 sampling sizes) — seed is not a block dimension in the omnibus test. Independently, back-solving the reported Nemenyi critical distance ($\mathrm{CD}=1.211$, $k=4$, $\alpha=0.05$) with the standard formula $\mathrm{CD} = q_\alpha\sqrt{k(k+1)/6N}$ only reproduces 1.211 at $N=15$ (it gives $\mathrm{CD}\approx0.54$ at $N=75$). Both independent checks confirm the Friedman/Nemenyi test was actually computed over 15 blocks (each block itself a 5-seed mean), not the 75 $(g,s,N)$ triples the text and table caption claim.
- **Reasoning**: This is a factual mismatch between what the manuscript says was done and what the underlying artifact shows was done, not a stylistic nit — block count directly determines the degrees of freedom context, statistical power, and how a reader should interpret "$n$" in the table. It also means the 75-block-labeled Friedman result and the true 75-cell paired Wilcoxon result (which *is* over 75 (g,s,N) cells) risk being read as the same unit of analysis when they are not: one pools seeds first, the other does not.
- **Suggestion**: Correct the text and table caption to state the true block construction ("$n=15$ blocks, each the 5-seed mean of a $(g,N)$ configuration") or, if 75-block granularity is preferred, re-run the Friedman/Nemenyi test on the ungrouped 75 $(g,s,N)$ triples and update $\chi^2$, $p$, $W$, and CD accordingly. Either fix is straightforward; leaving the current mislabeling risks a desk-reject-level correctness objection from a statistically careful reviewer.
- **Resolution (2026-07-28)**: Root cause confirmed via `exp2_run_level_metrics.csv`: Anchors and DiCE are missing runs across the full $(g,s,N)$ grid (57/75 and 68/75 artifact-qualified runs, versus 75/75 for SHAP/LIME), so a raw $n=75$ Friedman design is not achievable without dropping incomplete blocks — the 15-block, seed-averaged design was the correct choice, just mislabeled. Applied the labeling fix (not a re-run) to `paper_bc_jmlr.tex`: (1) the Friedman prose now states "$n=15$ blocks per method... each block value the mean across the 5 available seeds" with the Anchors/DiCE coverage caveat; (2) the `tab:friedman` caption now reads "$n=15$ blocks — 5 model families × 3 sampling intensities, each a 5-seed mean"; (3) the `tab:method_ranks` caption now discloses per-method run coverage (75/75 SHAP and LIME, 68/75 DiCE, 57/75 Anchors) instead of the inaccurate blanket "$n=75$ runs each." No statistics ($\chi^2$, $p$, $W$, CD, means, ranks) were changed — this was a captioning/labeling-only fix. Recompiled with `tectonic`: no errors, no new overfull/underfull warnings.

### F02 [minor, FIXED 2026-07-29] — D6 Methodological Rigor

- **Location**: §Gap 3 / Table `tab:exp4_icc` (line ~570)
- **Evidence**: Table caption states "EXP4; $n=147$ runs, 3 LLM judges" and reports both ICC(2,1) and Krippendorff's $\alpha$ per dimension in the same row, implying a shared sample.
- **Observation**: `outputs/analysis/exp4_llm_evaluation/icc_analysis.csv` has `n_cases=147` for every dimension, but `krippendorff_alpha.csv` has `n_cases=192` for every dimension. The two reliability statistics shown side by side in one table were computed on different underlying case counts, and this is not disclosed anywhere in the text or caption.
- **Reasoning**: Not necessarily an error (ICC and Krippendorff's $\alpha$ can legitimately use different case-inclusion rules, e.g. one requiring complete triplets and the other tolerating missing judges), but presenting both under one "$n=147$" caption without noting the difference could mislead a reader who assumes both columns describe the same 147 cases.
- **Suggestion**: Add a one-line note explaining why the two statistics have different effective $n$ (e.g., "$\alpha$ computed on the fuller $n=192$ pool including partially-judged items; ICC restricted to $n=147$ fully-judged triplets"), or reconcile them to a common case set if the difference is unintentional.
- **Resolution (2026-07-29)**: Root cause confirmed via artifact cross-check: `judge_disagreement.csv` has exactly 192 rows, matching `krippendorff_alpha.csv`'s `n_cases=192` for every dimension, while `icc_analysis.csv` uses `n_cases=147` for every dimension (matching the paper's in-text "$n=147$"). This is consistent with a legitimate statistical reason — ICC(2,1)'s two-way random-effects model requires a complete cases×judges matrix, so it is restricted to the 147 fully-triple-rated cases, while Krippendorff's $\alpha$ tolerates missing ratings and was computed on the fuller 192-case pool. Applied a disclosure-only fix to `paper_bc_jmlr.tex`: added one clarifying sentence after the Table~\ref{tab:exp4_icc} introduction stating the two different effective $n$ values and why, and updated the `tab:exp4_icc` caption to state both $n=147$ (ICC) and $n=192$ (Krippendorff's $\alpha$) explicitly instead of the single blanket "$n=147$ runs." No statistics changed. Recompiled with `tectonic`: no errors, no new warnings.
- **Caveat — could not fully verify from source**: the analysis scripts that would prove this filtering logic (`scripts/exp4_analyze_llm_scores.py`, `src/evaluation/exp4_reliability_metrics.py`) are absent from the working tree — only stale, untracked `.pyc` bytecode caches remain, and `git log --all` shows no history for either path (never committed). The row-count cross-check above is strong circumstantial evidence for the stated mechanism but is not a substitute for re-running the actual filtering logic. See F04 below.

### F04 [minor, open — confirmed unresolvable without regenerating EXP4] — D6 Methodological Rigor / Reproducibility

- **Location**: §Code and Artifact Availability (line ~1383, "EXP4 ICC exports: `outputs/analysis/exp4_llm_evaluation/`")
- **Observation**: Unlike EXP2, EXP3, and EXP6 — each of which cites a specific analysis script (`scripts/run_exp2_statistical_analysis.py`, `scripts/run_exp6_masking_sensitivity.py`, etc.) — the EXP4 artifact entry cites only the *output* directory. The scripts that would actually compute ICC/Krippendorff's $\alpha$ from raw judge responses are not present in the repository (only orphaned `.pyc` bytecode caches, never committed to git). This means EXP4's reliability numbers, and specifically the F02 case-count explanation above, are not currently independently re-derivable from committed source.
- **Reasoning**: This weakens the paper's own Reproducibility Contract claim ("deterministic audit trail from configuration to manuscript-level claim," §Reproducibility Contract) for the one experiment (EXP4) that produced a negative result — the experiment most likely to draw scrutiny.
- **Investigated 2026-07-30, confirmed not fixable in place**: checked whether the original scripts could be restored or reconstructed.
  - `git ls-files | grep -i exp4` returns nothing — the EXP4 scripts were never committed at any point in this repo's history, not merely deleted.
  - The **raw per-case, per-judge score data** that `icc_analysis.csv`/`krippendorff_alpha.csv` were computed from is also not present anywhere in the repository — only the aggregated output CSVs survive.
  - No Python decompiler is installed (`decompyle3`, `uncompyle6`, `pycdc`), and none of them reliably support the Python 3.11–3.13 bytecode found in the orphaned `.pyc` caches, so recovering the original source from bytecode was not attempted.
  - A newly written replacement script implementing the documented methodology (ICC(2,1) on complete triplets, Krippendorff's $\alpha$ on the full pool) cannot be validated against the existing numbers, because there is no raw data left to run it on. Writing one and calling it a "restoration" would itself be an unverifiable claim.
- **Decision (author, 2026-07-30)**: left as-is. No repo or manuscript changes were made for F04. The gap is documented here for the record; closing it properly would require re-running EXP4 from scratch (fresh LLM judge queries) rather than any reconstruction of the missing artifacts.
- **Suggestion**: If EXP4 is ever re-run before submission (e.g., to strengthen the negative result or extend it), archive both the raw per-case judge responses and the analysis script this time, and update §Code and Artifact Availability to cite them — bringing EXP4 up to the same reproducibility standard already met by EXP2/EXP3/EXP6.

### F03 [suggestion] — D1 Evidence Relevance

- **Location**: §Code and Artifact Availability / Supplementary references to Tables S2, S3, S5, S6
- **Observation**: The supplementary document's tables exist and are described consistently with in-text references, but this review did not independently re-derive their numeric content (kernel_width probe, num_samples probe, feature-correlation matrix, EXP6 masking breakdown).
- **Suggestion**: Before final submission, run the same artifact cross-check performed here (manuscript claim → source CSV/JSON) against the supplementary tables specifically, since they carry three of the paper's robustness arguments (LIME stability is "not a convergence artifact," minimum-viable kernel_width, masking-scheme sensitivity).

## Questions for the author

1. Was the choice to aggregate seeds into 15 blocks for the Friedman/Nemenyi test a deliberate design decision (e.g., to satisfy Friedman's assumption of one observation per block/treatment) that was simply mislabeled as "$n=75$," or was 75 blocks originally intended and the aggregation is an unnoticed artifact of the analysis script?
2. For Table `tab:exp4_icc`, is there a principled reason the Krippendorff's $\alpha$ pool ($n=192$) is larger than the ICC pool ($n=147$) — e.g., different handling of missing-judge rows — and should the manuscript state it?

## Recommendation

Given the memory record showing this paper's readiness was independently tracked at 98/100 as of 2026-07-04, this review's findings are consistent with that assessment: the paper is very close to submission-ready, and F01 is the one item worth fixing before submission since it is a verifiable, correctable factual discrepancy in a reported statistic rather than a judgment call. F02 and F03 are lower priority polish items.
