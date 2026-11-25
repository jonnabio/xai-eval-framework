# Paper E, revision 1 (AAIR, DergiPark)

Major revision, decision of 2026-11-24 (editor Remzi Gürfidan). Reviewer 1: minor;
reviewers 2 and 3: major. Due **2026-12-09**; internal target **2026-12-06** (T-3).

**Archive of the revision:** Zenodo 0.16.0, `10.5281/zenodo.24518192`, GitHub release
`paper-e-aair-2026-11-24-r1` (`main` at `b994aa194`, PR #152), published 2026-11-24.

The submitted edition (`../submission/`, `../paper_e_aair_template.tex`) is frozen; the
revision works on copies in this folder, as Paper B revision 1 did.

| File | What |
|---|---|
| `DECISION_LETTER.md` | Decision and reports, verbatim |
| `REVIEW_ANALYSIS.md` | Every item (R1-1 … R3-6), verdict, ambiguity note, work package |
| `REVISION_PLAN.md` | Work packages, decisions for the author, constraints, order |

| `CHANGELOG.md` | Every change, C-###, with the items it answers |
| `RESPONSE_TO_REVIEWERS.md` | The answer to every item (in progress) |
| `SUBMITTED_SNAPSHOT.sha256` | Hashes of the submitted files, which are frozen |
| `manuscript/paper_e_aair_rev1_template.tex` | **The revised manuscript** (working copy); `paper_e_aair_rev1.tex` is generated |
| `build/` | Built manuscript `.docx` / `.pdf` |
| `build/paper_e_aair_rev1_changes_marked.docx/.pdf`, `_response.docx/.pdf` | Changes marked against the submitted text; letter by reviewer (`scripts/build_revision.py`) |
| `build/supplement/` | Supplementary file S1–S8 (`scripts/build_supplement.py --exp3-model-root <dir>`) |
| `scripts/check_signs.py` | RCA-007 guard on the built file |

Build (needs Word for the PDF; numbers checked on every build):

```bash
.venv/Scripts/python.exe docs/reports/paper_e/aair_journal/scripts/build_paper_e_aair_docx.py
.venv/Scripts/python.exe docs/reports/paper_e/aair_journal/revision_1/scripts/check_signs.py
```

Still to create: `scripts/check_revision.py --final` (every item answered, frozen files).
