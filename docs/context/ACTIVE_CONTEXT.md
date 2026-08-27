# Active Context: XAI Evaluation Framework

## Session Metadata
- **Last Updated:** 2026-08-22
- **Active Role:** Scientific Editor
- **Mode:** PUBLICATION — synchronized the thesis, Paper A, and merged Paper B+C around validation-boundary wording and EXP3 status. Created `docs/reports/sync/thesis_paper_sync_matrix.md`; updated the implementation plan with sync task 6; aligned Chapter 3/6 EXP3 wording to the Paper B+C + artifact source of truth (SHAP-Anchors fidelity replication plus LIME-only extension, but no full paired SHAP-LIME cross-dataset stability test); aligned Paper A boundary language while preserving its narrower SHAP-only EXP3 claim scope; aligned Paper B+C validity-claim language and corrected the LIME extension export path.
- **Mode (2026-08-22, second pass):** PUBLICATION — full tri-document alignment + recency audit
  (Paper A, Paper B+C, thesis Ch.1-6), every shared numeric claim re-derived from committed
  artifacts. Report at `docs/review/tri-document-alignment-review_2026-08-22.md`: 12 findings
  (A01-A05 major, A06-A10 minor, A11-A12 suggestions). All EXP2 confirmatory statistics verified
  and consistent across all three documents. **A01 (headline, and it inverts the earlier sync
  assumption):** Paper A says the EXP3 Anchors cross-dataset check "could not be executed" and
  books 12 cells as a permanent `alibi`/`dice-ml` limitation, but those 12 runs completed
  2026-04-26 and sit on the unmerged `results/exp3-windows-breast-cancer` and
  `results/exp3-linux-german-credit` branches; their recomputed fidelity means (0.2648 / 0.2079 /
  0.3510 / 0.4507) match Paper B+C's `tab:exp3_fidelity` exactly, and SHAP > Anchors holds 12/12.
  Paper A, not the thesis, is the stale document on EXP3. A02: the earlier same-day Paper A edit
  fixed only one of three places and mislabels the companion as a "LIME-only" extension. A03: the
  two papers report different values for EXP3 SHAP Breast Cancer/XGB (0.6165 committed July re-run
  vs 0.607 April side-branch snapshot). A04: thesis F01 (Ch.5 vs Ch.4 numbers) still unfixed. A05:
  thesis Ch.4 per-method profile uses pre-recovery-overlay costs (SHAP 24,804 ms vs artifact
  11,708 ms; LIME 226 vs 3,660.7; DiCE 2,056 vs 28,208.8). A08: thesis never received the Paper B+C
  EXP4 n=147/192 disclosure fix. A09: thesis cites the superseded `10.5281/zenodo.19297724`.
  Recency: both PDFs and the thesis `.docx` predate the current sources. No manuscript was edited —
  the substantive fixes need author decisions (branch merge, canonical EXP3 SHAP snapshot,
  provenance of Ch.5's 0.514/0.412). Sync matrix updated with the corrected EXP3 row, three new
  rows, and five new checklist items.
- **Mode (2026-08-22, third pass):** PUBLICATION — remediation. Landed the four-week backlog in
  three commits (`d1c9ba1d1` Paper B+C F01/F02 + EXP3 path; `00cdc8f3e` thesis/Paper A EXP3 wording
  + sync matrix; `b09b92a1d` both review reports + context), then applied six artifact-verified
  fixes in `3eeed3b04`: A02 partial (Paper A "LIME-only" mischaracterisation), A06 (thesis Anchors
  coverage 56→57 / 74.7%→76.0%), A07 (EXP3 minimum gap German Credit RF→XGB, in both Paper B+C and
  thesis Ch.6), A08 (EXP4 n=147/192 disclosure ported into thesis Ch.5), A10 (Paper B+C Friedman
  p-values labelled Holm-adjusted), A13 (new: dangling `@tbl-exp4-dimensiones` crossref in Ch.3,
  found by the rebuild, repointed to `@tbl-exp4-icc`). No statistic or table value changed.
  Rebuilt all four outputs — three PDFs via `tools/tectonic-portable`, thesis DOCX via
  `thesis/render.ps1` — all clean. Toolchain notes: MiKTeX `pdflatex` cannot build Paper A
  (microtype font-expansion error at the bibliography), use Tectonic; `render.ps1` calls a
  nonexistent `quarto clean` and prints a harmless error every run.
  **Still blocked on author decisions:** A01 (merge `results/exp3-*` branches, then rewrite Paper A
  §sec:exp3 + Conclusion), A03 (canonical EXP3 SHAP snapshot: July 0.6165 vs April 0.6065),
  A04 (thesis Ch.5 0.514/0.412 provenance), A05 (thesis Ch.4 cost profile), A09 (thesis Zenodo DOI).
- **Mode (2026-08-23):** PUBLICATION — remediation round 2, on author decisions. (1) Merged the EXP3
  Anchors cohort: imported the 12 run dirs (1,768 files) from `results/exp3-windows-breast-cancer`
  surgically via `git checkout <branch> -- <anchors paths>` (a full merge would have dragged in
  stale docs and junk paths `.venvScriptspython.exe` / `[14`); SHAP > Anchors re-verified 12/12,
  gap range +0.2601 GC/XGB to +0.5137 BC/RF. Paper A §sec:exp3 + Conclusion + artifact availability
  rewritten — A01/A02 closed. **Root cause of A01 found:** `scripts/run_exp3_shap_configs.py`'s
  docstring says Anchors "remain blocked by numpy<2.0 vs Python 3.13", true of the *July*
  environment; Paper A generalized it to "never executed". (2) A03 closed with July as canonical:
  Paper B+C BC/XGB 0.607→0.617, gap +0.06→+0.07. **Why BC/XGB differed:** all 12 SHAP configs were
  re-run 2026-07-23/24; only BC/XGB's quality metrics moved (sparsity 0.3333→0.8822 — 10/30 vs
  ~26.5/30 features above the 1e-4 threshold). Models were retrained 2026-05-10 with identical
  config *and identical test metrics*, and the runner is a thin wrapper over the same
  ExperimentRunner + YAML, so the cause is a SHAP/XGBoost library change across the April→July
  environment migration, not model or code. (3) A05 closed: Ch.4's profile *and* transversal
  subsections regenerated from `exp2_run_level_metrics.csv` with aggregation stated; the transversal
  section had been mixing per-model means with single-cell Appendix C sensitivity values (SVM
  0.928/159,059 is the k=50 row of `@tbl-appendix-shap-sensitivity`, not the 15-run mean 0.882/54,231).
  N-effect SHAP means also refreshed. (4) A09 closed: thesis repointed to `10.5281/zenodo.21538180`
  / commit `553f65d71`. (5) A12 closed incidentally. All four outputs rebuilt clean.
  (6) A04 closed on author approval: Ch.5's illustrative figures corrected to
  Anchors 0.388 / DiCE 0.172 / DiCE parsimony 0.017 / SHAP stability 0.732, and the "óptimo en
  parsimonia y eficiencia" claim reworded since DiCE's 28,209 ms cost is second-worst. Provenance
  settled first: the numbers entered in `f639935d0` (2026-05-10) at a commit where
  `outputs/analysis/` did not yet exist, and match no artifact at any commit — draft figures, not a
  different aggregation. Rest of Ch.5 swept: no other benchmark numbers.
  **All 13 audit findings (A01-A13) are now closed.** Remaining open items in the publication set
  are pre-existing and author-accepted: Paper B+C F03 (supplementary tables not independently
  re-derived) and F04 (EXP4 scripts + raw judge data unrecoverable); A11 (Paper A leads with the
  45-cell d_z, the others with the 75-cell) is an open suggestion with no action requested.
- **Mode (2026-08-24):** INCIDENT → EXECUTION — RCA-001 Phase 1, the permanent fix for the defect
  class behind the whole audit. Diagnosis: FOM-7 gate 7 (claim traceability) was editorial policy
  with no mechanism, in a workflow where the same quantity is authored independently in three
  documents. The SSOT machinery already existed (`pub/claims.toml` → `pub/fragments/` →
  `pubs-sync.yml`) but covered only abstracts/keywords, hand-typed its own numbers, and excluded
  Paper B+C entirely. Built: `pub/claim_registry.toml` (44 numbers, each with resolver + every
  manuscript carrying it), `scripts/pubs/claim_sources.py` (resolvers over `outputs/analysis/` and
  the EXP3 tree; separates block-level from run-level aggregation — the origin of A05),
  `scripts/pubs/verify_claims.py` (4 checks: value vs artifact, per-site occurrence count, retired
  values, cited-artifact existence), `docs/rca/RCA-001-manuscript-artifact-drift.md`. Wired Paper
  B+C into the fragment pipeline (rebuilt byte-equivalent), added the verifier to `pubs-sync.yml`
  CI and to `.aceconfig` `pre_commit`, and registered the **first entry in
  `regression-guards.yaml`** (9 guarded files, 6 invariants, 2 tests, 4 review triggers).
  Negative-tested, not just passing: the first manuscript-site check failed to catch an edited
  Paper A table cell because the value recurs in prose, so per-site occurrence counts were added.
  **New finding A14 (major, OPEN):** building the verifier revealed Paper B+C claims a 48-paper
  coded corpus throughout, while the only committed corpus artifact
  (`docs/reports/paper_c/paper_c_review_corpus.csv`) has 24 rows and no 48-row corpus exists at any
  commit. Deliberately not registered in the registry (would encode an unbacked number or force CI
  red); needs the author to commit the corpus or correct the manuscript.
  Note: `.aceconfig` is excluded via `.git/info/exclude`, so its new hook line is local-only.
  Phase 2 remains: generate numbers into LaTeX macros / Quarto inline values, and a CI build gate
  failing on undefined references.
- **Mode (2026-08-24 to 26):** INCIDENT/EXECUTION — RCA-001 Phase 1 plus A14 closure.
  Built the claim-traceability enforcement that makes FOM-7 gate 7 executable
  (`pub/claim_registry.toml`, `scripts/pubs/claim_sources.py`, `verify_claims.py`,
  `check_review_corpus.py`, `check_corpus_pdfs.py`, `fetch_corpus_pdfs.py`,
  `seed_corpus_from_audit.py`), wired Paper B+C into the fragment pipeline, added all
  checks to `pubs-sync.yml` CI, and registered the first `regression-guards.yaml` entry.
  **A14 closed 2026-08-26:** Paper B+C's review corpus is reconstructed and released as
  `docs/reports/paper_bc/paper_bc_review_corpus.csv` — 44 rows, of which 16 carry the
  original first-reviewer coding recovered from `second_reviewer_audit_results.csv` and
  28 were identified from the citation record and re-coded from full text. All 44 full
  texts are held under `corpus_pdfs/` (25 auto-retrieved, 17 copied from
  `thesis/papers/`, 2 supplied by the author), each verified by PDF header, size floor
  and page-one title match. ~4 papers coded but never cited are unrecoverable, so the
  corpus is 44 not 48, and twelve manuscript edits moved Paper B+C's printed figures
  onto the corpus: cluster distribution 15/10/7/6/4/2, evidence coverage
  21 proxy / 15 expert-taxonomy / 13 benchmark / 12 end-user / 4 LLM-judge, PRISMA
  included 44, audit fraction 36%, plus a new **Corpus provenance** paragraph in
  §Validity disclosing the reconstruction. `[review_corpus.paper_bc]` now pins the
  distribution and CI verifies it. **All 15 audit findings (A01-A15) are closed.**
  Outstanding by author decision: F03 (supplementary tables not re-derived), F04 (EXP4
  scripts/raw judge data unrecoverable), A11 (Paper A leads with 45-cell d_z).
  Author verification wanted on the 28 reconstructed coding rows before submission.
- **Prior session (2026-08-11):** ran `scientific-rigor-review` against the full PhD thesis (`thesis/index.qmd` through `apendices.qmd`, all 6 chapters + appendices); report at `docs/review/scientific-rigor-review_thesis_2026-08-11.md` (Grade: Accept, mean 4.3/5). Six findings: F01/F02 major (Ch.5 restates Ch.4's Anchors/DiCE fidelity+parsimony numbers incorrectly — needs a numeric fix before defense; Ch.6 "future work" item 4 contradicts the completed-work note `sec-exp3-nota` a few paragraphs earlier), F03-F06 minor/suggestions (parsimony-direction wording slip in Ch.4, undreived 50%-power-reduction sensitivity claim in Ch.3, unflagged Anchors non-convergence selection-bias direction, "prescriptivo" framing in Ch.6 in tension with the thesis's own conditional-language discipline).
- **Prior session (2026-07-30):** ran `scientific-rigor-review` against `docs/reports/paper_bc/paper_bc_jmlr.pdf`; report at `docs/reports/paper_bc/scientific-rigor-review_paper_bc_jmlr_2026-07-28.md` (Grade: Accept, mean 4.0/5). F01 (major, Friedman/Nemenyi block-count mislabeling) and F02 (minor, EXP4 ICC/Krippendorff n=147-vs-192 disclosure) were fixed with captioning-only edits to `paper_bc_jmlr.tex`; recompiled clean both times, no statistics changed. F03 (suggestion, supplementary tables not independently re-verified) remains open, lower priority. F04 (EXP4 analysis scripts + raw judge-response data both missing from the repo, never committed) was investigated in depth on 2026-07-30 — confirmed not fixable without re-running EXP4 from scratch; author decided to leave it as-is rather than fabricate a restoration. CIFIE PUBLICATION work below is unaffected by either review.

## Current Objective
Maintain the CIFIE/FOM-7 book chapter workstream and its ACE manuscript-editing support tooling.

## Current State

### Working
- Thesis/Paper synchronization pass completed for validation-boundary language and EXP3 scope. The sync matrix is available at `docs/reports/sync/thesis_paper_sync_matrix.md`.
- New `Scientific Advisor` role added to `.ace/roles/roles.md` (idea/hypothesis critique, manuscript rigor review, reference audit), sitting between Data Scientist/AI Expert (research) and Scientific Editor (publication) in the Research Workflow.
- New project-local skill `.ace/skills/scientific-rigor-review/SKILL.md`: adapts the ai-research pack's ARA-directory `rigor-reviewer` (6-dimension epistemic review) to plain manuscript/thesis-chapter prose. Produces severity-ranked reports to `docs/review/scientific-rigor-review_*.md`. Read-only on the manuscript.
- New project-local skill `.ace/skills/reference-audit/SKILL.md`: bibliography dedup, orphaned/unused citation detection, APA7 consistency checks, and re-verification via `paper-lookup`. Produces reports to `docs/review/reference-audit_*.md`. Report-only by default; does not edit `.bib`/reference files without explicit instruction.
- `.aceconfig` updated: added `PEER_REVIEW: Scientific Advisor` to `role_routing`, and trigger keywords `idea review`, `hypothesis review`, `peer review`, `science correctness`, `methodology review` → scientific-rigor-review; `references`, `bibliography`, `duplicate citations`, `citation dedup` → reference-audit.
- `.ace/packs/scientific/.aceconfig-ext` updated: added `scientific rigor` / `reference audit` triggers and `Scientific Advisor` to `roles_augmented`.
- Project-local reusable manuscript editing skill available at `.ace/skills/manuscript-editing/SKILL.md`.
- `.aceconfig` now maps `cifie`, `book chapter`, `manuscript editing`, `publication editing`, `academic manuscript`, `citation editing`, and `literature enrichment` to the reusable skill.
- The skill supports Spanish academic prose revision, APA 7 consistency, evidence traceability, open-access literature enrichment, FOM-7 terminology preservation, and submission-readiness checks.
- Sections 09 and 10 have been strengthened with verified open-access XAI evaluation sources supporting multidimensional evaluation, functionally grounded benchmarks, and human/application-grounded limits.
- `10_limitaciones_trabajo_futuro.md` has been revised into a stronger academic Spanish section aligned with FOM-7 evidence boundaries, with expanded in-text citations for metric dependence, method configuration sensitivity, human validation limits, recourse constraints, coverage gaps, and future-work priorities.
- `02_introduccion.md` has been revised into a stronger academic Spanish introduction that frames FOM-7 as a response to the evidentiary gap in XAI evaluation, with expanded APA-style in-text citations for opacity, post-hoc methods, metric fragmentation, functional evaluation, toolkits, and auditable evidence.
- `02_introduccion.md` received a follow-up polish aligning its evidentiary language with section 03: explanation as evidence must not confuse narrative persuasiveness with technical validity, and FOM-7 preserves the relationship among artefact, construct, test, result, and claim.
- `03_fundamentos_xai.md` has been revised through a literature-enrichment loop into a stronger foundations section. It now distinguishes artifact type, interpretability, explainability, transparency, local/global scope, plausibility, fidelity, stability, robustness, metric proxies, and the functionally-grounded scope of FOM-7.
- `@miller2019` was added to the CIFIE references to support the social/contrastive dimension of explanation while keeping the manuscript clear that audience plausibility is not technical fidelity.

### In Progress
- CIFIE/FOM-7 book chapter publication editing
- Thesis/Paper final scientific-editor consistency checks

### Blocked
- Final CIFIE template, word limit, and citation rendering requirements still need confirmation.

## Next Steps
1. [ ] Resolve remaining thesis-review numerical findings F01/F03 in Ch.4/Ch.5 before defense.
2. [ ] Re-run targeted consistency check for EXP3 mentions after any future Paper A or Paper B+C edits.
3. [ ] Verify final rendered PDFs after publication manuscripts stabilize.
4. [ ] Use `manuscript-editing` with the CIFIE/FOM-7 profile for future CIFIE section revision passes.
5. [ ] Continue APA/citation and compression checks once final CIFIE requirements are confirmed.
6. [ ] Validate final submission artifacts after manuscript stabilization.
7. [ ] Run `Scientific Advisor` (`scientific-rigor-review` + `reference-audit`) against the CIFIE chapter and/or Paper A/B+C once each is near-final, before final submission.

## Active Constraints
- .ace/standards/coding.md
- .ace/standards/security.md
- Keep thesis and paper artifacts read-only unless explicitly instructed otherwise.
- Keep the CIFIE chapter as a distinct publication output under `publications/book_chapters/2026_cifie_xai_fom7/`.

## Session Notes
- Synchronized thesis, Paper A, and Paper B+C around the June 13 validation-boundary assessment: functionally grounded comparative evidence is retained as the supported contribution; synthetic/transparent-model ground-truth tests, dependency-aware perturbation, and human-centered validation remain future validity-strengthening work.
- Updated `thesis/capitulo-3-diseno-experimental.qmd` and `thesis/capitulo-6-conclusiones.qmd` so EXP3 no longer contradicts the later LIME extension: EXP3 supports SHAP-Anchors fidelity replication and a LIME-only extension, but not a full paired SHAP-LIME cross-dataset stability claim.
- Updated `docs/reports/paper_a/paper_a_prototype_jmlr.tex` and `docs/reports/paper_a/paper_a_validity_and_reporting_caveats.md` to keep Paper A scoped to its SHAP-only EXP3 check while acknowledging the broader LIME-only extension outside Paper A's confirmatory claim.
- Updated `docs/reports/paper_bc/paper_bc_jmlr.tex` to align the validity-claim ladder and correct the LIME extension export path to `outputs/analysis/exp3_lime_results.csv`.
- Created and later generalized the CIFIE skill into the reusable `manuscript-editing` ACE skill with CIFIE/FOM-7 profile support.
- Updated `.aceconfig` trigger mappings for CIFIE manuscript editing tasks.
- Strengthened the skill with an explicit open-access literature enrichment workflow that uses the `literature` / `paper-lookup` skill for Semantic Scholar, Crossref/OpenAlex, and OA verification before citations are added.
- Ran an OA literature enrichment pass: Semantic Scholar returned HTTP 429 for broad searches but verified selected identifier lookups; OpenAlex and Crossref verified accepted DOI metadata and OA status for Nauta et al. (2023), Canha et al. (2025), Pawlicki et al. (2024), Bhattacharya and Verbert (2024), and Doshi-Velez and Kim (2017).
- Updated section 09/10 manuscript citations, `references.bib`, `references_apa7.md`, `citation_audit.md`, and `sources/evidence_map.md` with accepted source details.
- Revised `10_limitaciones_trabajo_futuro.md` for academic prose, APA 7 in-text citation support, and FOM-7 alignment; no thesis or paper artifacts were edited.
- Revised `02_introduccion.md` for academic prose, APA 7 in-text citation support, and FOM-7 alignment; no thesis or paper artifacts were edited.
- Updated `docs/planning/implementation_plan.md` for the skill creation task.
- On branch `publication/cifie-xai-fom7-book-chapter`, added implementation-plan task 5 for revising section 03 through a literature-enrichment loop.
- Queried Semantic Scholar first for selected XAI foundations sources; the shared pool returned successful DOI lookups for Murdoch et al. (2019), Marcinkevičs and Vogt (2023), and Miller (2019), and HTTP 429 for some other DOI/topic queries.
- Cross-checked accepted foundations sources through OpenAlex and Crossref. OpenAlex verified OA status for Murdoch et al. (PNAS PDF), Marcinkevičs and Vogt (Wiley PDF), Nauta et al. (ACM PDF), Schwalbe and Finzel (Springer PDF), Rudin et al. (Project Euclid PDF), and Miller (arXiv PDF).
- Added `@miller2019` to `references/references.bib` and `references/references_apa7.md`; updated `references/citation_audit.md` and `sources/evidence_map.md` for the section 03 literature loop.
- Revised `03_fundamentos_xai.md` for academic Spanish prose, citation support, and FOM-7 alignment; no `thesis/` or `pub/` artifacts were edited.
- Added `Scientific Advisor` role and `scientific-rigor-review`/`reference-audit` skills to extend ACE with peer-review-style science-correctness and bibliography-hygiene capability, on user request. No thesis/paper/CIFIE content was reviewed or edited in this session — this was a framework-extension task only.
