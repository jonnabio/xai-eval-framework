# Plan: Paper B, the 13-page paired SHAP-LIME paper

**Date**: 2026-10-04 | **Role**: Architect | **Status**: proposed, waiting for the author's approval

**Basis**: `docs/review/paper-c-resurrection-assessment_2026-10-04.md`. Author decisions of
2026-10-04: reduce Paper B+C to 13 pages; Paper B goes first, Paper C second; the
second-reviewer disagreements are adjudicated (Paper C work, not part of this plan).

## 1. Goal

One paper with one question: how do LIME and SHAP differ under matched conditions, and when
does the answer depend on the model and the configuration? Target length 13 pages including
references, no appendix. The target is the author's, not a journal rule.

## 2. What does not change

- No experiment is run and no result changes. Every number that stays is already registered
  in `pub/claim_registry.toml`.
- The 32-page edition (`paper_bc_iberamia.tex`, its appendix and PDF) is not edited. It is
  the source for Paper C and is tagged before anything is retired.
- Nothing about the original EXP4 cohort is rewritten.

## 3. Decisions

| # | Decision | Proposal | Who decides |
|---|---|---|---|
| D1 | Folder and lane | Stay in `docs/reports/paper_bc/` on the `paper/bc-*` lane; new source `paper_b.tex` | Proposed; follows the author's rule that this material stays in one folder |
| D2 | Venue | Open. Only no-fee journals. *Computación y Sistemas* holds Paper E | **Author** |
| D3 | Template | A neutral 10 pt A4 article layout until D2 is settled; the journal template is applied afterwards | Proposed |
| D4 | Title | "LIME versus SHAP under Matched Conditions: A Paired Comparison on Tabular Models" | **Author** |
| D5 | Lead finding | The conditional result: the latency ordering depends on the model family, and LIME's stability on Adult depends on kernel width and feature space | Proposed (assessment F02) |
| D6 | Tables S2, S5, S6 | Out of the PDF; cited from the archive | Proposed |
| D7 | Record of the split | New ADR-0022; it supersedes ADR-0020 and amends ADR-0019 | Proposed |

## 4. Content: what stays, what leaves

| Block | Pages now | Target | Action |
|---|---|---|---|
| Title, abstract, keywords | 1.0 | 0.75 | New abstract in `pub/claims.toml`; Spanish Resumen only if the venue asks |
| Introduction | 1.25 | 1.0 | Two contributions. The optimisation problem (Eq. 1) is removed |
| Background | 1.75 | 0.75 | LIME and SHAP only; the distinctions table is removed |
| Benchmark design | 3.0 | 2.25 | Hypotheses in text, not a table; infrastructure in two sentences |
| Paired results | 2.75 | 2.5 | Kept almost whole |
| Cross-dataset results (EXP3) | 2.0 | 1.25 | One table instead of two, if the registry allows it |
| Recommendations and discussion | 1.5 | 1.0 | Deployment table kept, scoped to the measured families |
| Validity and limitations | 4.0 | 1.25 | Provenance, scope of the comparison, generalisability table |
| Conclusions, acknowledgments, availability | 1.75 | 0.75 | Broader impact removed |
| References | 3.75 | 1.5 | About 30 entries; every one cited |
| **Total** | | **13.0** | |

Leaves for Paper C: the scoping review protocol and corpus, the taxonomy, the three gaps,
the formalization-aware criteria, the layered architecture, EXP4 (method and results),
Tables S1 and S4. Dropped: Table S3.

## 5. Steps

Each step ends with the checks named in section 6 and its own commit.

1. **Tag and record.** Tag the 32-page edition. Write `IBERAMIA_REJECTION_RECORD.md`
   (needs the submission date and ID from the author). Write ADR-0022.
2. **Inventory.** List every table, figure and registered claim site of the 32-page
   edition and mark each as B, C or dropped. Output: a table in this plan. This shows whether
   a claim would be left with no site, and how the verifier treats that.
3. **Skeleton.** Create `paper_b.tex` by copying the kept blocks unchanged. Add the file to
   `[coverage]` and `[exclusivity]` and move the claim sites (shared commit, through `main`).
   The file is long at this point; the numbers must already verify.
4. **Reduce.** Cut to the targets of section 4, block by block. Prose only; no number is
   added. The validity section is cut last.
5. **Reframe.** New title, abstract and introduction around D5. The abstract is edited in
   `pub/claims.toml` with doubled backslashes (RCA-003) and the built page 1 is read.
6. **References.** Remove uncited entries; check each remaining entry once.
7. **Independent review.** A new session in the Scientific Advisor role reviews the result
   for focus, novelty against Papers A, D and E, and claim support. Findings go to
   `docs/review/`.
8. **Venue.** Apply the template of the chosen journal, re-check the length, run the
   anonymity check if the review is blind, publish a new Zenodo version.

## 6. Checks after every step that touches the manuscript or the registry

- `python scripts/pubs/verify_claims.py`
- `python scripts/pubs/verify_sync.py`
- `python scripts/pubs/scan_shared_literals.py --strict` (overlap with Paper A)
- `python scripts/pubs/verify_exp4_reconstruction.py`
- Page count of the built PDF: 13 or fewer from step 4 onward.

## 7. Regression guards touched

- **RCA-001** (`pub/claim_registry.toml`, manuscript numbers): steps 3 to 5. Every literal
  in the new file is registered; no retired value returns; the three figures keep their
  committed generators.
- **RCA-002** (`pub/claim_registry.toml`): step 3. No EXP4 source or pin is edited.
- **RCA-003** (`pub/claims.toml`, abstract fragments): step 5.

## 8. Risks

1. **Novelty** (assessment F02). The reduced paper shares its runs with Papers A, D and E.
   Mitigation: D5, a clear provenance paragraph, and the review in step 7 before any
   submission.
2. **The same text in two papers.** Until Paper C is written, the taxonomy and EXP4 text
   exists only in the 32-page edition. Paper B must not keep a shortened copy of it.
3. **Paper E's companion statement** names the 32-page paper by its old title. It is
   corrected only if Paper E is revised.
4. **Thesis and chapter.** The thesis numbers do not change. ADR-0018 (the CIFIE chapter
   prints no unpublished Paper B+C result) must name both new papers; the sync matrix rows
   are renamed in step 3.

## 9. Needed from the author

1. Approval of this plan, or changes to it.
2. D2: the journal, or permission to search for no-fee candidates.
3. D4: the title.
4. For the rejection record: the date of submission to *Inteligencia Artificial* and the
   submission ID, if one was given.
