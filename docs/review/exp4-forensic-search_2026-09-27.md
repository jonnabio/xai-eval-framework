# EXP4 Forensic Search — 2026-09-27

**Question:** can the EXP4 reliability results (ICC, Krippendorff's alpha) be
recomputed from raw judge data?

**Answer:** No. The aggregate results are committed and intact; the raw judge
responses, the prompt templates and (since 2026-09-27) the bytecode the
reconstructed code was verified against exist nowhere that could be searched.
Nothing was recomputed, simulated or re-derived, and no reported value changed.

## 1. What exists

The four aggregate CSVs entered Git in `f6591d68078ca65c500079f0da5abeb18331b54c`
(2026-09-05) and have one blob each, identical on `main`, `thesis/rca-001-phase-2`
and `paper/bc-venue-definition`:

| File | Blob | Content |
|---|---|---|
| `outputs/analysis/exp4_llm_evaluation/icc_analysis.csv` | `3708e8cd5be36c8be2162b9ddf3fc9a07db4bda6` | 7 dimensions, n=147, 3 judges |
| `outputs/analysis/exp4_llm_evaluation/krippendorff_alpha.csv` | `2e0374ecdd3cabfb644c7d13c433cbd76e56427d` | 7 dimensions, n=192, 3 judges |
| `outputs/analysis/exp4_llm_evaluation/judge_disagreement.csv` | `1fc48ed5bf614f8e090226be995dad6db8d9a970` | 192 case IDs, per-case disagreement SD |
| `outputs/analysis/exp4_llm_evaluation/judge_comparison_summary.csv` | `8b137891791fe96927ad78e64b0aad7bded08bdc` | empty (the blob of a single `\n`) |

Working-tree copies on a Windows checkout differ byte-wise only by CRLF
(`core.autocrlf=true`); `git hash-object` with filters reproduces the blobs.

The values, with the CSV column `icc_2_1` holding ICC(1,1) as RCA-002 shows:

| Dimension | ICC(1,1) | 95% CI | Krippendorff alpha |
|---|---|---|---|
| clarity | 0.3206 | 0.167-0.459 | 0.2779 |
| completeness | 0.5848 | 0.467-0.682 | 0.5665 |
| concision | 0.4531 | 0.314-0.573 | 0.4089 |
| semantic_plausibility | 0.6007 | 0.486-0.695 | 0.5733 |
| audit_usefulness | 0.3763 | 0.228-0.507 | 0.3400 |
| actionability | 0.3998 | 0.254-0.528 | 0.3624 |
| overall_quality | 0.4309 | 0.289-0.554 | 0.3943 |

No dimension reaches the 0.75 threshold (Koo & Li 2016); the highest upper
confidence bound is 0.695. Every value matches Paper B+C `tab:exp4_icc` and
thesis Ch.5/Ch.6 at three decimals, and `verify_claims.py` re-derives the 14
registered `exp4:` claims directly from these CSVs.

## 2. What is missing, and where it was looked for

| Item | Status |
|---|---|
| Raw judge responses | Absent. Known since RCA-002. |
| EXP4 Jinja templates (`exp4_semantic_eval_v1.j2`, `_label_visible.j2`, `_alt.j2`) | Absent. Known since RCA-002. |
| EXP4 bytecode (`src/evaluation/__pycache__/exp4_*.cpython-313.pyc`, `scripts/__pycache__/exp4_*.cpython-312.pyc`) | **Lost 2026-09-27.** Never committed on any branch; it existed only on the previous author laptop. |

Places searched, all negative except the aggregates:

- **Git history, every ref.** Not a shallow clone. `git log --all --no-textconv
  -S exp4_e9eba60d9edc4d8a` (a case ID from `judge_disagreement.csv`) finds only
  `f6591d680`. `git log --all --name-only` finds no EXP4 path other than the four
  CSVs, RCA-002 and the verifier. No `.pyc` has ever been committed.
- **Remote refs.** `git ls-remote origin`: five branches and two tags
  (`v0.2.0`, `paper-a-submission-2026-03-28`); all covered by the search above.
- **Unreachable objects and stash.** `git fsck --unreachable --no-reflogs`: two
  commits and one stash, all created in this session (the `data/adult.csv`
  commit and the S-table heading fix); no EXP4 content.
- **GitHub.** One release (the Paper A snapshot of 2026-03-28, which predates
  EXP4); zero Actions artifacts.
- **This laptop.** No file named like `*exp4*`, `*llm_eval*`, `*judge*`,
  `*semantic_eval*` or `*.j2` under Documents, Downloads or either OneDrive root.

Not searchable from here: the previous laptop, and any Zenodo deposit (the
cited snapshot `10.5281/zenodo.21538180` archives commit `553f65d71`, which
holds only tracked files, so it cannot contain what Git never held).

## 3. Consequences

- **The published EXP4 numbers are unaffected.** They are committed aggregates,
  re-derived in CI from the committed CSVs.
- **End-to-end reproduction is impossible**, as RCA-002 already stated. Re-running
  three LLM judges would create a new cohort, not reproduce this one, and would
  also need the lost templates; Supplementary Table S1 is the only record of the
  instrument.
- **The source reconstruction can no longer be re-verified.** RCA-002's check
  that the reconstructed `exp4_*.py` compile to the original bytecode passed on
  2026-08-28 and cannot be repeated. `verify_exp4_reconstruction.py` and the
  `exp4-reconstruction` CI job fail on `missing bytecode` (run 36339931425). The
  2026-08-28 result stands as a recorded, dated verification, not a live one.

## 4. Open decision (author)

How RCA-002 and CI should treat the lost bytecode: retire the opcode check,
replace it with a hash pin of the reconstructed sources as verified, or keep it
as a documented permanent failure. Until decided, CI stays red on that job.
