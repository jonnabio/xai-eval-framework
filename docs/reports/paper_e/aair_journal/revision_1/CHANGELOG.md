# Change log: Paper E, AAIR revision 1

Every change to the manuscript or its build, numbered C-###, with the items it answers.
Recorded in the commit that makes it. Working copy: `manuscript/paper_e_aair_rev1_template.tex`
(copied unchanged from `../paper_e_aair_template.tex` on 2026-11-24, C-000).

| C | Date | Change | Where | Items |
|---|---|---|---|---|
| C-000 | 2026-11-24 | Working copy of the submitted source; build redirected to `build/`; submitted edition frozen (`SUBMITTED_SNAPSHOT.sha256`, `--edition submitted` refused) | `manuscript/`, build script | — |
| C-001 | 2026-11-24 | Signs written as text (U+2212), not Word equations; every build checks each table row and every negative number in the Word text against the source (RCA-006) | `build_paper_e_aair_docx.py` (`plain_signs`, `verify_numbers`); `scripts/check_signs.py` | R2-1, R2-6 |
