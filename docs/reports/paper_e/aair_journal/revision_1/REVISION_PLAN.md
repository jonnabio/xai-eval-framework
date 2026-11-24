# Revision plan: Paper E, AAIR revision 1

Lane `paper-e`, branch `paper/e-aair-revision-1` (claimed 2026-11-24 by
`claude-2026-11-24-paper-e`). Model: Paper B revision 1 (`docs/reports/paper_b/ci_journal/revision_1/`).
Items: `REVIEW_ANALYSIS.md` (21 items).

## Constraints (AAIR rules, `../AAIR_SUBMISSION.md`)

- ≤ 15 pages (now 14); ≤ 10 figures + tables (now exactly 10: nothing new may be added
  as a table or figure in the paper; new results go in text or the supplement); abstract
  ≤ 250 words (now 249: any addition replaces words); ≤ 60 references (now 25).
- New references: DOI and verified; the 80% rule handled as Paper B did ("option A",
  `paper_b/.../REFERENCE_AUDIT.md`), to be confirmed (D-4).
- Equations, figures, tables numbered and cited by generated references; impersonal voice;
  every printed number generated from a CSV.

## Work packages

| WP | Content | Items | New computation |
|---|---|---|---|
| WP0 | Set-up: freeze snapshot hashes of the submitted files; copy source into `manuscript/`; `CHANGELOG.md`, `RESPONSE_TO_REVIEWERS.md` skeleton; `check_revision.py` (frozen files, every item answered, every C-### cited) | all | no |
| WP1 | **Minus-sign defect**: fix the Word converter; check comparing every number of the built `.docx` (tables and text) with the generated LaTeX and the CSVs; RCA-00x + regression guard; full numeric audit | R2-1, R2-6 | no |
| WP2 | Analyses from stored outputs: held-out-only Adult agreement (top-5, top-10, Kendall); same-predicted-class permutation reference; leave-one-seed-out ranges | R1-1, R2-2, R2-4, R2-5, R3-3 | yes, cheap (stored rows) |
| WP3 | LIME sensitivity run on the self-agreement subsample: package defaults (width default + discretisation) and sampling budgets, vs SHAP | R2-3, R3-1 | **yes, new LIME runs** (D-1) |
| WP4 | Text: conditional wording (Abstract, Conclusion), self-agreement as reference analysis, sign pre-specified vs post-hoc, SVM qualification sweep, pre-specified vs exploratory paragraph and labels, generalization limits, per-seed retraining design, origin of width 3 | R1-2…R1-5, R2-5, R3-1…R3-4 | no |
| WP5 | Supplementary file: configurations of every explainer and model, measure definitions, held-out and LIME-sensitivity tables | R2-6, R2-3 | no |
| WP6 | Condense Discussion and Limitations (each caveat once); page and abstract budget | R3-5 | no |
| WP7 | Build: manuscript `.docx` (template), changes-marked `.docx`, response letter, supplement; `check_revision.py --final`; Zenodo release; README and ACTIVE_CONTEXT | ED-1, all | no |

Order: WP0 → WP1 (blocks every build) → WP2 → WP3 (in parallel once D-1 decided) → WP4
→ WP5 → WP6 → WP7.

## Response letter

As Paper B: per reviewer, each comment quoted briefly, then "Response" (polite, concise)
and "Changes" (section, page, C-###). For AMBIGUOUS items, one sentence: "The comment was
understood as …; if a different analysis was intended, it will be provided." Reviewer 2's
sign finding acknowledged directly as an error of the Word conversion, corrected and now
checked automatically.

## Decisions for the author

| ID | Question | Proposal |
|---|---|---|
| D-1 | WP3 runs: scope and machine | Self-agreement subsample (Adult LR/MLP/RF/XGB, 100 each; GC and BC RF/XGB); settings: defaults (width √d·0.75, discretise on), width 3 with 1,000 / 5,000 / 10,000 samples; on the experiment laptop or this one if light enough (to time first) |
| D-2 | New results in the paper | In text, numbers only; tables in the supplement (paper at the 10-item limit) |
| D-3 | Deadline | Record from DergiPark |
| D-4 | References | Add only if a new claim needs one; 80% rule as Paper B option A |
| D-5 | Zenodo | New version of the Paper E record with the revision (as for B) |
