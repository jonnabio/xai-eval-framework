# Change log: Paper E, AAIR revision 1

Every change to the manuscript or its build, numbered C-###, with the items it answers.
Recorded in the commit that makes it. Working copy: `manuscript/paper_e_aair_rev1_template.tex`
(copied unchanged from `../paper_e_aair_template.tex` on 2026-11-24, C-000).

| C | Date | Change | Where | Items |
|---|---|---|---|---|
| C-000 | 2026-11-24 | Working copy of the submitted source; build redirected to `build/`; submitted edition frozen (`SUBMITTED_SNAPSHOT.sha256`, `--edition submitted` refused) | `manuscript/`, build script | — |
| C-001 | 2026-11-24 | Signs written as text (U+2212), not Word equations; every build checks each table row and every negative number in the Word text against the source (RCA-007) | `build_paper_e_aair_docx.py` (`plain_signs`, `verify_numbers`); `scripts/check_signs.py` | R2-1, R2-6 |
| C-002 | 2026-11-24 | Held-out sensitivity of the primary measures (Adult), same-class permutation reference, leave-one-seed-out ranges; Section 4.1 | `paper_e_revision1_analyses.py`; manuscript 3.3, 4.1 | R1-1, R2-2, R2-4, R2-5 |
| C-003 | 2026-11-24 | Origin of the LIME configuration stated (inherited, not tuned, no technical justification); estimates are for this configuration; Adult single-fit design and per-seed refit as the cleaner alternative | Manuscript 3.1, 3.2 | R3-1, R3-3, R1-2 |
| C-004 | 2026-11-24 | Pre-specified vs exploratory analyses listed separately; headings marked (self-agreement as reference analysis; signs: pre-specified measure and post hoc conversion) | Manuscript 3.6, 4.2, 4.4 | R3-4, R1-3, R1-4 |
| C-005 | 2026-11-24 | LIME settings experiment (package defaults; default width; width 3 at 5,000 / 10,000 samples) and its paragraph | `paper_e_lime_settings.py`; manuscript 3.3, 4.2 | R2-3, R3-1, R1-2 |
| C-006 | 2026-11-24 | Abstract, contributions and Conclusions conditional on the configuration; self-agreement described as reference analysis | Abstract, 1, 6 | R1-2, R1-3 |
| C-007 | 2026-11-24 | SVM qualified in every model comparison; no family ranking | Manuscript 4.3, 4.5, 4.6, 5 | R1-5 |
| C-008 | 2026-11-24 | Discussion and Limitations rewritten and condensed (~1,100 → ~810 words): evidence supported / not supported / signs / implications / limitations, each caveat once | Manuscript 5 | R3-5, R3-2, R1-4 |
| C-009 | 2026-11-24 | Zenodo 0.16.0 (`10.5281/zenodo.24518192`, release `paper-e-aair-2026-11-24-r1`) cited in Data Availability | Manuscript, Data Availability | R2-6 |
| C-010 | 2026-11-24 | Supplementary file S1–S8: model hyperparameters (read from the binaries), explainer settings with sources, measure definitions, held-out, same-class, leave-one-seed-out and LIME-settings tables, reproduction commands | `scripts/build_supplement.py`; `build/supplement/` | R2-6, R2-3 |
