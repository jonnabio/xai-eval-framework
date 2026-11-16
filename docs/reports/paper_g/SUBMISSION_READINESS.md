# Paper G — submission readiness (Task 20)

**Date:** 2026-11-16. **Direction (author, Task 20):** C — faithfulness-metric agreement depends on
the level of evaluation, attribution semantics and the evaluation protocol. **Submission:** not
authorized; the author submits.

## 1. Manuscript

| Item | State |
|---|---|
| Source | `paper_g_draft.md` v0.2 (revised from the v0.1 scaffold; methods of #134 kept, results, discussion, conclusions and declarations written) |
| Rendered | `paper_g.md`; `submission/paper_g_blind.docx` (journal template styles) and `.pdf`; `submission/Figure_1` … `Figure_5` (.png 600 dpi, .svg) |
| Build | `python docs/reports/paper_g/scripts/build_paper_g.py --evidence-map`; figures `~/xai-eval-framework/.venv/bin/python docs/reports/paper_g/scripts/paper_g_figures.py`; references `python docs/reports/paper_g/scripts/verify_references.py` |
| Structure | Abstract; 1 Introduction (1.1 Related work); 2 Materials and methods (2.1 design and the five evidence classes, 2.2 data and models, 2.3 explainers and attribution semantics, 2.4 metrics, Equations (1) to (3), 2.5 agreement analysis, Equation (4), decision rule, 2.6 S3, S1, Equation (5), diagnostics, 2.7 reproducibility); 3 Results and discussion (3.1 confirmatory, 3.2 pre-specified sensitivity, 3.3 S3, 3.4 S1, 3.5 positions, 3.6 *f(x)*-adjusted H2, 3.7 M7 and random control, 3.8 discussion with the three contributions, recommendations and limitations); 4 Conclusions; declarations |
| Reporting hierarchy | A confirmatory (3.1, reported exactly: 0.723 [0.645, 0.802], *W* 0.762, permutation *p* 0.00001, Holm 0.00002, "the metrics broadly agree", LIME slope semantics explained); B supplementary (3.3 S3, 3.4 S1 with S1-B primary and S1-M sensitivity, no decision); C exploratory (3.5 R3, 3.6 R6, 3.7 R7 and R11 last) |
| Length | 12 pages (8 to 16); abstract 203 words; 5 keywords; 4 tables, 5 figures, 5 equations |
| Voice, anonymity | Impersonal; no names; own work in the third person, anonymised |

## 2. Claims

| Item | State |
|---|---|
| Registered numbers | 185 claims (`pub/claim_registry.toml`, block `paper_g`, written by `scripts/pubs/register_paper_g.py`), re-derived by `scripts/pubs/verify_claims.py` from the committed result files; `paper_g.md` is under the coverage and exclusivity guards |
| Bare integers | covered by `register_paper_g.py --check` (the rendered file must equal the rendering from the result files) |
| Evidence map | `EVIDENCE_MAP.md` (generated): section, class, values, source files |
| Typed numbers | none: every result is a placeholder resolved from a result file |
| `[R]` markers of v0.1 | 18. Filled from verified evidence: H1 value and interval, decision wording (raw and Holm), stability benchmark, winner flips, H2 (omnibus and pairs), permutation and Holm *p*, SHAP–LIME reversals under M7, random-control share (3.7, exploratory; not in the abstract), model AUCs (Table 2), hardware (CPU model, from `outputs/analysis/paper_g/STATUS.md`). **Withdrawn:** total run time (no result file holds it). **Unresolved:** none |
| `[REF]` markers | all replaced by verified references |

## 3. References

50 references, all verified against their records (`REFERENCE_VERIFICATION.md`, generated):
42 with DOI; 5 peer-reviewed without DOI (NeurIPS 2017, 2019, TMLR 2024, ICLR 2025) verified on the
publisher's page or OpenReview; 3 anonymised own manuscripts. 84% from 2024 onward (83% without
own work); 92% scientific articles; all cited. Closest competitor (Shanklin et al., 2026,
conceptual) checked: no overlap with the empirical contribution.

## 4. Reviews

- `RIGOR_REVIEW.md`: no Critical finding; six Major (four disclosed in the manuscript, two author
  decisions); Minor findings recorded.
- `JOURNAL_COMPLIANCE.md`: formal requirements pass; author actions listed.

## 5. Remaining corrections (author)

1. **AI-content limit (30%, Compilatio).** The text is assistant-drafted; rewrite as needed. A
   rebuild re-inserts and re-verifies every number.
2. **Declarations.** Confirm Funding, Conflicts of interest and the AI-use statement (bracketed).
3. **Public repository during double-blind review.** Decide whether the Paper G source stays public.
4. **Word check.** Open the .docx in Word (pagination, equations, header row repeat).
5. **Title.** Kept as in the plan; it fits direction C, but the author may prefer a title that names
   the three dependencies.
6. **At acceptance.** Author block, CRediT roles, Zenodo DOI of the code and results, published
   records of Papers B, E and F.

## 6. Pull requests

See the consolidated report in the pull request descriptions: one lane PR (manuscript, scripts,
figures, reports, built files) and one shared PR (`paper_g` resolver, registration script, registry
block, coverage and exclusivity entries, CI step, section-number rule of the claim scanner, active
context), stacked on the lane PR. Merge order: lane PR first, then the shared PR.

## Status

- ORIGINAL SCIENTIFIC RESULTS: PRESERVED
- SUPPLEMENTARY EVIDENCE: INTEGRATED
- CLAIM TRACEABILITY: PASS
- REFERENCE AUDIT: PASS
- SCIENTIFIC RIGOR REVIEW: PASS
- JOURNAL COMPLIANCE: PASS
- MANUSCRIPT: READY FOR AUTHOR REVIEW
- SUBMISSION: NOT AUTHORIZED
