# RCA-002: EXP4 sources lost from the tree; supplementary tables never re-derived

**Status**: Open (partial recovery landed; see Remaining)
**Severity**: High
**Opened**: 2026-08-28
**Role**: Scientific Editor → Incident Responder
**Related**: [RCA-001](RCA-001-manuscript-artifact-drift.md) (F04 was recorded
there as "not covered"), findings F03/F04 in
`docs/reports/paper_bc/scientific-rigor-review_paper_bc_jmlr_2026-07-28.md`

## Symptoms

Two items were carried as accepted-as-is at the close of RCA-001:

- **F04**: the EXP4 analysis scripts were absent from the repository, so the
  reported ICC and Krippendorff figures could not be re-derived from committed
  source. RCA-001 recorded them as unrecoverable.
- **F03**: the supplementary tables (S2, S3, S5, S6) carry three of the paper's
  robustness arguments and had never been checked against their artifacts.

Both were re-examined on 2026-08-28. F04 was **partly recoverable** and the
recovery exposed a mislabelled statistic; F03 was checkable and **two of its
four tables were wrong**.

## Evidence

### The sources were recoverable

`src/evaluation/exp4_*.py` and `scripts/exp4_*.py` are gone from the working
tree and from history, but their compiled bytecode survives in `__pycache__`:
seven modules (3.11/3.12/3.13), four CLI scripts, five test modules. Bytecode
retains docstrings, signatures, defaults, annotations, constants, names and
full control flow. RCA-001's "unrecoverable" was wrong: it assessed the raw
judge data, which is genuinely gone, and generalised to the scripts.

### The ICC is a one-way model, not the two-way model reported

`ICC.icc_2_1` computes only two mean squares:

```
bms = k * Σ(case_mean − grand_mean)² / (n−1)
wms = Σ(x − case_mean)² / (n(k−1))
icc = (bms − wms) / (bms + (k−1)·wms)
```

There is no judge/column term. That is **ICC(1,1)**, one-way random effects,
not the ICC(2,1) the function is named for and the paper describes. Confirmed
numerically against reference two-way mean squares on synthetic data with
deliberate judge bias: the module reproduces ICC(1,1) to machine precision and
understates ICC(2,1) by 0.067 on that fixture.

A one-way model charges systematic between-judge offsets to error, so the
published values are **conservative** — the true ICC(2,1) would be somewhat
higher. The conclusion is unaffected: the largest reported value is 0.601 with
an upper confidence bound of 0.695, well short of the 0.75 threshold.

### The 147 vs 192 question is answered

`icc_2_1` calls `pivot_table(...).dropna()`, requiring a complete
cases-by-judges matrix (n=147). `alpha_ordinal` pivots without `dropna` and
masks with `np.isnan` (n=192). This is principled and standard — ICC needs a
complete matrix, Krippendorff's α is defined for missing data — and answers
question 2 of the 2026-07-28 rigor review, which the manuscript had previously
addressed only circumstantially via row counts.

`_analysis_scope` additionally excludes judges matching
`dummy|dry-run|dry_run`, so dry-run rows never entered the published pools.

### Supplementary Table S6 was wrong in three of four rows

The top-*k* gap column matches `exp6_paired_shap_lime.csv` exactly (4/4). The
drop-correlation column did not:

| scheme | printed | artifact |
|---|---|---|
| independent zero | +0.625 | **+0.515** |
| mean replacement | +0.591 | **+0.512** |
| marginal empirical | +0.534 | **+0.625** |
| grouped mean | +0.493 | +0.494 |

The printed column is strictly decreasing; the artifact is not — marginal
replacement is the *highest*. The paragraph beneath the table generalised the
attenuation claim to both endpoints, so the prose asserted a pattern only one
of the two columns shows. `+0.591` and `+0.534` appear nowhere in the EXP6
artifacts at scheme level.

### Supplementary Table S3 was not reproducible

Five of nine associations reproduce exactly. The four involving
`occupation`/`workclass` did not, under any convention tested (full dataset,
listwise deletion, bias-corrected V). Those two columns are unobserved on the
same 2,809 records, so treating missingness as a category manufactures an
association between them — `workclass`–`occupation` rises from 0.216 to 0.400.

### Supplementary Table S5 has no artifact

The `num_samples` probe has no committed output. Its generating script,
`src/scripts/run_sensitivity_analysis.py`, **is** committed and sweeps
`[500, 1000, 2000, 5000, 10000]`; the table reports the first three. The probe
is re-runnable; only its output was never archived.

## Root cause

Same as RCA-001 — traceability enforced by convention, not tooling — with two
extensions RCA-001's fix did not reach:

1. **The registry covered the main text only.** The supplementary document was
   outside it, so its tables were never re-derived by anything.
2. **A missing artifact was assessed once and written off.** F04 was closed as
   unrecoverable without checking `__pycache__`. "Not recoverable" is a claim
   about evidence and deserves the same verification as any other.

## Fixes (2026-08-28)

- `src/evaluation/exp4_reliability_metrics.py` reconstructed from bytecode.
- `scripts/pubs/verify_exp4_reconstruction.py` compares the reconstruction's
  opcode stream, signatures, defaults and constants against the original
  `.pyc`, ignoring line numbers and the added provenance docstring. It found
  two real defects in a first draft of the reconstruction (a missing
  `dim in group_df.columns` guard, and a call whose argument layout changed the
  emitted instructions) before it passed.
- ICC relabelled ICC(1,1) with the conservativeness noted, in Paper B+C
  (text, caption, table header, validity-ladder figure) and the thesis
  (Ch.3, Ch.5 ×3, Ch.6 ×2, appendix).
- Table S6 corrected; the paragraph now separates the two endpoints.
- Table S3 corrected to pairwise-complete cases, with the convention and the
  co-missingness hazard stated in the caption.
- 16 supplementary claims, 2 retired-value guards and 2 cited artifacts added
  to `pub/claim_registry.toml`, with stdlib-only resolvers for Cramér's V and
  Pearson r so CI needs no scientific stack.
- `pubs-sync.yml` gains an `exp4-reconstruction` job pinned to Python 3.13.

## Remaining

1. **Six EXP4 modules and four CLI scripts are still unreconstructed**:
   `exp4_analysis`, `exp4_cases`, `exp4_parser`, `exp4_prompts`,
   `exp4_runner`, `exp4_schema`, plus `exp4_build_cases`,
   `exp4_run_llm_judges`, `exp4_parse_llm_responses`,
   `exp4_analyze_llm_scores`, and five test modules. All are recoverable by the
   method above; the reliability module was prioritised because it is the one
   that produces the published statistics. Add each to `PAIRS` in the verifier
   as it lands.
2. **Raw judge responses are genuinely gone.** Only aggregates, 192 case IDs
   and per-case disagreement survive; `experiments/exp1_adult/llm_eval/` is
   EXP1's 80-case set, not EXP4's. The EXP4 figures therefore still cannot be
   re-derived end-to-end. Re-running the judges would produce a new cohort, not
   a reproduction — a re-experiment, not a fix.
3. **Table S5 needs its probe re-run** and the output archived, or the table
   withdrawn. Until then it is the one supplementary table with no backing
   artifact.
4. Whether to state in §Validity that EXP4's raw judge responses were not
   retained. Recommended: the paper already reports EXP4 as a negative result
   and discloses its other limits plainly.
