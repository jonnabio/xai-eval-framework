# CIFIE Chapter Sync and Reference Audit — 2026-09-27

**Lane:** `chapter/cifie-sync-2026-09` (third lane, ADR-0013 `chapter/cifie-*`)
**Chapter:** `publications/book_chapters/2026_cifie_xai_fom7/`
**Decision record:** [ADR-0018](../adr/0018-cifie-chapter-excludes-unpublished-results.md)

The chapter was last edited on 2026-07-26. That was before the August audits
(A01–A14), RCA-002, the tutor feedback of 22 September and EXP4 cohort 2. It
was outside every verifier.

## 1. Drift found and fixed

| Finding | Where | Fix |
|---|---|---|
| Five retired values: SHAP cost 24,804 ms, DiCE cost 2,056 ms, SHAP stability 0.724 | §04, §08, Table 4 | Replaced with current thesis values. The aggregation is stated at each site: block means for fidelity and stability, run means for parsimony, faithfulness gap and cost. |
| Pre-audit SHAP profile presented as "valores consolidados reportados en la tesis": 0.810 / 0.724 / 0.234 / 0.431 / 24,804 ms | §08, Table 4 | Current values: 0.808 / 0.732 (block), 0.226 / 0.380 (run); cost given per model family |
| LIME cost 226 ms (pre-A05) | §08, Table 4 | Run means per model family: 52–122 ms, and 17,620 ms on SVM |
| Anchors fidelity 0.386 (the unbacked Apéndice C τ-probe value, not the benchmark mean) | §04, §08, Table 4 | Block mean 0.389 |
| LIME instability called "una propiedad estructural del método" (the universal framing the thesis retracted on 2026-09-02) | §08 | Scoped to the configuration and the feature space; the EXP3 contrast is cited to the thesis |
| Seed handling in Friedman blocks not stated (tutor correction) | §07 | Seeds are averaged within each (g, n) block and are not counted as replicates |
| Neither the thesis nor RIMI in the reference list | references | Both added (APA 7 and `.bib`) |

## 2. Paper B+C results removed (ADR-0018)

The chapter printed the 75-cell paired SHAP–LIME statistics: d_z 4.820 and
3.002; mean differences +0.2479, +0.7176 and +8047.6 ms; the full paired table
in Table 4; SHAP wins in 75 of 75 cells. It also printed LIME's stability CV of
86.2% and Anchors' coverage of 76.0%. All of these are Paper B+C results.

- **Changed:** these are now reported as direction only, citing the thesis.
- **Figure 4** (paired differences) is retired and the later figures are
  renumbered.
- **What remains:**
  - results already published in RIMI (Friedman statistics, block means);
  - thesis-only values;
  - the thesis's 15-block follow-up, reported by counts and $p_{\mathrm{Holm}}$
    only, because its mean difference coincides with the 75-cell one.

## 3. Mechanism

- **`verify_claims.py` exclusivity check:** fails if a protected chapter file
  prints a value registered for Paper B+C, unless the same value is also
  registered for Paper A. It matches by value at the printed precision, so
  "4.820" matches "4.82".
- **New Paper B+C sites registered,** without which the check could not see
  those values: 0.248, 0.718, 8047.6 and 86.2.
- **Coverage:** the chapter's 11 sections and Table 4 are under `[coverage]`.
  Every number has a chapter site with a pinned count: 61 sites on 31 claims.
  50,000 (the Adult income threshold) is declared structural.
- **Negative-tested:**
  - reintroducing the stale 0.810 fails twice (the site count and the
    coverage check);
  - inserting "4.82" fails the exclusivity check.

## 4. Reference audit

- **Coverage:** 42 entries in the list, 41 distinct in-text citations.
- **Orphan fixed:** "Abdul Kadir et al., 2023" was cited 3 times (4
  occurrences) with no list entry.
  - The `.bib` DOI `10.1109/INES59045.2023.1030000` returns 404.
  - Crossref gives `10.1109/INES59282.2023.10297629` (IEEE INES 2023,
    pp. 111–124), with first author Md Abdul **Kadir**.
  - In-text citations corrected to "Kadir et al., 2023"; the entry added and
    the `.bib` corrected.
- **All 35 DOIs** in the reference list resolve.
- Altukhi, Pradhan & Aljohani (2025) was listed but never cited. Removed at
  the author's request (APA 7 lists only cited works). The list now has 41
  entries for 41 cited works.
- **Not an error:** the two Herrera-Vásquez 2026 entries have different author
  lists, so APA needs no a/b suffix.

## 5. Build

`scripts/build_cifie_chapter.py` assembles sections 01–11 with the title and
authors from the editorial sheet. It appends the APA 7 list with a hanging
indent and writes `drafts/v3_editorial_review/cifie_xai_fom7_<date>.docx`
using the Pandoc bundled with Quarto. The first build is 17,756 words with 6
figures and no Paper B+C statistic.

## 6. Still open

- ~~Tables 1–4 in working form~~ **Done 2026-09-27.** The tables are in
  final APA 7 form (bold number, italic title, table, *Nota.*):
  - They are renumbered by first mention: 1 methods (§04), 2 FOM-7 gates
    (§06), 3 metrics (§07), 4 results by hypothesis (§08).
  - §04's forward reference to the results table is reworded, so it no
    longer fixes the numbering.
  - Working-only material (usage columns, repository paths, traceability
    notes) is removed.
  - The build places each table after the paragraph that first cites it,
    through `<!-- TABLA: ... -->` markers. It fails on a missing,
    duplicated or unplaced table.
  - All four table files are under `[coverage]` and `[exclusivity]`.
- **Noted by the author:** the thesis is cited as "[Tesis doctoral no publicada]".** Update the entry
  when the thesis is deposited.
- **A full Scientific Advisor rigor review** of the whole chapter was not run
  in this pass. The empirical sections (§01, §04, §07, §08, §11) and Table 4
  were re-read and corrected; §02, §03, §05, §06, §09 and §10 were only
  scanned for numbers and sensitive content.
