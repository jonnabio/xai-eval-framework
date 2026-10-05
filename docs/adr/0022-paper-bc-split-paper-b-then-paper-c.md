# ADR-0022: Paper B+C Is Split; Paper B Goes First, to the CLEI Electronic Journal

> **Status:** Accepted<br>
> **Date:** 2026-10-04<br>
> **Supersedes:** [ADR-0020](0020-paper-bc-venue-inteligencia-artificial.md) (venue
> *Inteligencia Artificial*). Amends decision 3 of
> [ADR-0019](0019-paper-bc-venue-peerj-and-single-working-folder.md) ("there is one Paper B+C
> edition"); its working-folder decisions stand.<br>
> **Related:** [ADR-0018](0018-cifie-chapter-excludes-unpublished-results.md),
> [RCA-001](../rca/RCA-001-manuscript-artifact-drift.md),
> `docs/review/paper-c-resurrection-assessment_2026-10-04.md`,
> `docs/planning/paper_b_13pp_reduction_plan_2026-10-04.md`,
> `docs/reports/paper_bc/IBERAMIA_REJECTION_RECORD.md`

---

## Context

The 32-page Paper B+C was rejected at the desk by TMLR (2026-10-02) and by *Inteligencia
Artificial* (reported 2026-10-04). Neither notice names a defect. The paper joined a paired
SHAP-LIME benchmark, a taxonomy with a 44-paper scoping corpus, and an LLM-judge reliability
study. The author's hypothesis is that a long article is harder to review and publish, and
set a target of 13 pages. The Scientific Advisor's assessment found that the removed material
can become a second paper in one form only: the LLM-judge study with the taxonomy as framing.

## Decision

1. **Paper B+C is split into two papers.** Paper B is the paired SHAP-LIME comparison.
   Paper C is the LLM-judge reliability study, with the taxonomy and the scoping corpus as its
   framing.
2. **Paper B goes first.** Target: about 13 pages including references, no appendix.
3. **Paper B targets the *CLEI Electronic Journal*** (author, 2026-10-04): no author charges,
   single-blind review, English, CC-BY, at least 12 pages, abstract of at most 200 words,
   IEEE-style numbered references, the journal's `cleiej` LaTeX class.
4. **Paper B has its own folder and lane** (author, 2026-10-04): `docs/reports/paper_b/`, lane
   `paper-b` on `paper/b-*` branches, worked in the main folder. The manuscript is
   `docs/reports/paper_b/paper_b_cleiej.tex`, with its own copies of the figures. Nothing of
   Paper B is kept in `docs/reports/paper_bc/`, which holds the 32-page edition and the Paper C
   material. The April 2026 prototype that was in `docs/reports/paper_b/` was removed; it
   remains in the history (last present at commit `cd4af0e94`).
5. **No text or result appears in both papers.** Paper B keeps no taxonomy, scoping corpus or
   LLM-judge material. Each paper cites the other once it exists, and the RIMI article.
6. **The 32-page edition is kept unedited** (`paper_bc_iberamia.*`, tag
   `iberamia-submission-2026-10`) as the source for Paper C. It stays under `[coverage]` until
   Paper C replaces it.
7. **The second-reviewer disagreements are adjudicated** before Paper C uses the corpus counts
   (`docs/reports/paper_bc/second_reviewer_adjudication_sheet.csv`).

## Consequences

- No experiment is run and no registered value changes for Paper B. `paper_b_cleiej.tex` goes under
  `[coverage]`; each kept claim gains a site in it. It needs no entry under `[exclusivity]`:
  files in `docs/reports/paper_bc/` and `docs/reports/paper_b/` are the protected side of that
  check (`forbid`).
- ADR-0018 applies to both papers: the CIFIE chapter prints no result of Paper B or Paper C
  while they are unpublished.
- Single-blind review: the author block, the repository address and the archive DOI are
  printed. A new Zenodo version is published before submission.
- Paper E's submitted text names the 32-page paper as a companion manuscript; it is corrected
  only if Paper E is revised.
- Paper C needs its own plan: adjudication, a human-rated subset (two raters, 50 to 60 cases),
  and a dated plan for any post hoc analysis.

## Amendment (2026-10-04, same day): Paper C has its own folder and lane

Author decisions, taken after Paper B was submitted. They replace the last clause of decision
4 ("`docs/reports/paper_bc/` ... holds ... the Paper C material").

1. **Paper C is worked in `docs/reports/paper_c/` only**, lane `paper-c` on `paper/c-*`
   branches, in the main folder. Its manuscript, plan, scripts, result files and copies of its
   inputs live in that directory.
2. **The April 2026 survey prototype in that folder is removed.** It was the survey-only form
   that the assessment judged not viable. It remains in the history (last present at the
   commit before the removal on `paper/c-llm-judges`).
3. **`docs/reports/paper_bc/` is frozen** as the record of the rejected 32-page edition. The
   inputs Paper C needs (the 44-paper corpus, the second-reviewer audit and the adjudication
   sheet) are copied into `docs/reports/paper_c/`; the copies are the working files from then
   on. Decision 6 stands: the 32-page edition stays under `[coverage]` until Paper C replaces
   it.
4. **Paper C targets *Tecnología en Marcha*,** special issue on Artificial Intelligence, 2027
   edition (call closes 2026-10-15). Paper D was sent to the same issue on 2026-10-03.
5. **Tooling.** The publication-sync checks no longer read the prototype: `verify_sync.py`
   does not check a Paper C manuscript until the new one exists, the 24-study corpus claim and
   its `[review_corpus.paper_c]` block are removed from the registry, and the Paper C abstract
   in `pub/claims.toml` is a placeholder until the new abstract is written.
