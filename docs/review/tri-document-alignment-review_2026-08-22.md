# Tri-Document Alignment Review: Paper A, Paper B+C, Thesis

**Date**: 2026-08-22 | **Role**: Scientific Editor (PUBLICATION mode) | **Mode**: cross-document
alignment + recency audit

**Targets**:

- Paper A — `docs/reports/paper_a/paper_a_prototype_jmlr.tex` (989 lines, working tree)
- Paper B+C — `docs/reports/paper_bc/paper_bc_jmlr.tex` (1,893 lines, working tree)
- Thesis — `thesis/*.qmd` (Ch.1–6 + appendices), focus on Ch.3–Ch.6

**Verification basis**: every shared numeric claim was re-derived from committed artifacts
(`outputs/analysis/paper_a_exp2_stats/*.csv`, `experiments/exp3_cross_dataset/results/**/results.json`,
`outputs/analysis/exp3_lime_results.csv`, `outputs/analysis/exp4_llm_evaluation/*.csv`), plus
`git ls-tree` recovery of the two unmerged `results/exp3-*` branches.

## One-line summary

The three documents agree on every EXP2 confirmatory number (all re-verified against artifacts),
but they disagree about EXP3 in a way that inverts the working assumption in the sync matrix:
**Paper A is the stale document, not the thesis** — it states the EXP3 Anchors cross-dataset check
"could not be executed" and treats 12 cells as a permanent gap, when those 12 runs were completed
in April 2026 and sit on two unmerged branches, and are the exact source of the SHAP>Anchors
numbers that Paper B+C and the thesis already publish.

## Severity-ranked findings

### A01 [major] — Paper A denies experimental work that exists and is published elsewhere

- **Location**: `paper_a_prototype_jmlr.tex:582-586` (§External Validity Check) and
  `:737` (Conclusion, Limitation bullet).
- **Evidence**: Paper A: *"A matching Anchors-based cross-dataset check was planned in the same
  `exp3_cross_dataset` configuration set but could not be executed in this pass; it is blocked by
  the same `alibi`/`dice-ml` environment incompatibility ... and is left as follow-up work"*; and
  *"these 25 cells and the matching 12 `exp3_cross_dataset` Anchors cells ... are accepted as a
  permanent, disclosed limitation of this evidence cut rather than pending work."*
- **Artifact check**: the 12 Anchors runs exist and are complete. They live on two unmerged
  branches, `results/exp3-windows-breast-cancer` (commit `380c1576e`, 2026-04-26) and
  `results/exp3-linux-german-credit`. Recomputed 3-seed mean Anchors fidelity:
  Breast Cancer RF **0.2648**, BC XGB **0.2079**, German Credit RF **0.3510**, GC XGB **0.4507** —
  matching Paper B+C's Table `tab:exp3_fidelity` (0.265 / 0.208 / 0.351 / 0.451) to reported
  precision. SHAP > Anchors holds in **12/12** seed-level pairs, exactly as Paper B+C and the
  thesis `sec-exp3-nota` claim.
- **Reasoning**: this is the most consequential misalignment in the set. Paper A both understates
  its own evidence base and asserts a false cause (a dependency block) for a run that succeeded.
  A reader comparing Paper A with Paper B+C — which cite the same repository — sees one paper say
  the Anchors cross-dataset comparison is impossible in this environment and the other report its
  results in a table and a figure.
- **Remediation** (author decision required): merge or cherry-pick the two `results/exp3-*`
  branches into the publication branch so the artifacts are on the cited snapshot, then rewrite
  Paper A §sec:exp3 and the Conclusion bullet to report the completed SHAP–Anchors comparison
  (or to cite the companion paper for it). The `alibi`/`dice-ml` block remains true and should be
  retained for the **25 EXP2 cells**; it is only the 12 EXP3 Anchors cells that are wrongly
  described.

### A02 [major, PARTIALLY FIXED 2026-08-22] — The 2026-08-22 Paper A edit fixed the symptom in one place and left it in two others

- **Location**: `paper_a_prototype_jmlr.tex:391-397` vs `:582-586` and `:737`.
- **Evidence**: today's working-tree edit removed the "blocked by an environment dependency gap"
  clause from the External-validity bullet and replaced it with *"the companion synthesis evidence
  base, which also reports a **LIME-only** EXP3 extension."*
- **Observation**: two problems. (i) The companion reports a SHAP–Anchors comparison **and** a LIME
  extension, so "LIME-only" mischaracterises it. (ii) §sec:exp3 and the Conclusion bullet still
  carry the original "could not be executed" / "permanent limitation" wording, so Paper A is now
  internally inconsistent as well as inconsistent with the other two documents.
- **Resolution (2026-08-22, partial)**: problem (i) fixed — the bullet now reads *"the companion
  synthesis evidence base, which reports both a SHAP--Anchors fidelity comparison and a LIME
  fidelity/stability extension on the same two datasets."* Problem (ii) is **not** fixed and cannot
  be until A01 is decided: rewriting §sec:exp3 and the Conclusion bullet depends on whether the
  `results/exp3-*` branches are merged. Note that this partial fix makes Paper A's internal tension
  *more* visible, not less — the validity bullet now correctly names a SHAP--Anchors comparison
  that §sec:exp3 two pages later still calls impossible. That is the intended state: accurate and
  visibly incomplete, rather than inaccurate and superficially coherent.

### A03 [major] — Paper A and Paper B+C report different values for the same EXP3 SHAP cell

- **Location**: Paper A `tab:exp3-shap` (`:598-601`) vs Paper B+C `tab:exp3_fidelity` (`:1067-1070`).
- **Evidence**: Breast Cancer / XGB SHAP fidelity is **0.6165** in Paper A and **0.607** in Paper B+C.
- **Artifact check**: two distinct EXP3 SHAP execution snapshots exist. The committed
  `experiments/exp3_cross_dataset/results/` tree (timestamps 2026-07-23/24, per
  `logs/run_exp3_shap_configs_status.json`) gives BC/XGB fidelity **0.6165**, stability 0.9625,
  sparsity 0.9134. The April side-branch snapshot gives **0.6065**, stability 0.9531, sparsity
  **0.3333**. Paper A uses the July re-run; Paper B+C uses the April snapshot.
- **Reasoning**: Paper B+C's §Code and Artifact Availability points readers at
  `experiments/exp3_cross_dataset/results/`, which does **not** contain the value its table reports.
  The sparsity divergence (0.333 vs 0.913) shows the two snapshots are materially different runs,
  not a rounding artifact. The other three cells (BC/RF 0.7785, GC/RF 0.7137, GC/XGB 0.7108) are
  identical across snapshots and both papers, so only BC/XGB was re-run.
- **Remediation**: pick one snapshot as canonical for EXP3 SHAP across both papers, state which,
  and re-derive both tables from it. The July run is the one currently committed and the one
  Paper A's archived DOI resolves to.

### A04 [major] — Thesis F01 (Ch.5 vs Ch.4 numeric contradiction) is still open

- **Location**: `thesis/capitulo-5-taxonomia.qmd:20,35-36` vs `capitulo-4-resultados.qmd:93-94,378,390`.
- **Evidence**: Ch.5 still reads *"(SHAP: 0.810, LIME: 0.560, Anchors: 0.514, DiCE: 0.412)"* and
  *"La parsimonia media de DiCE (0.085 ...) y su fidelidad baja (0.412)"*.
- **Artifact check**: run-level means over qualified runs are Anchors fidelity **0.3880**, DiCE
  fidelity **0.1716**, DiCE sparsity **0.0166**; block-level means are 0.389 / 0.170 / 0.0166.
  Ch.5's 0.514 and 0.412 match **neither** aggregation, and 0.085 is LIME/Anchors' parsimony,
  not DiCE's.
- **Status**: carried forward unchanged from the 2026-08-11 review (F01, major). It remains the
  single most examiner-visible defect in the thesis, because the thesis's own gate 7 is a
  claim-traceability guarantee.

### A05 [major] — Thesis per-method profile section is built on a pre-recovery snapshot

- **Location**: `thesis/capitulo-4-resultados.qmd:313-315` (SHAP), `:341` (LIME), `:390-393` (DiCE).
- **Evidence**: *"Sus medias consolidadas sobre los 71 bloques calificados son: fidelidad = 0.810,
  estabilidad = 0.724, parsimonia = 0.234, brecha de fidelidad = 0.431, coste = 24,804 ms"*;
  LIME *"media 226 ms"*; DiCE *"coste moderado (2,056 ms en media)"*.
- **Artifact check** (run-level means, `exp2_run_level_metrics.csv`):

  | Method | Thesis Ch.4 profile | Artifact / Paper A / Paper B+C |
  |---|---|---|
  | SHAP stability | 0.724 | **0.7320** |
  | SHAP faithfulness gap | 0.431 | **0.3796** |
  | SHAP cost | 24,804 ms | **11,708.26 ms** |
  | SHAP parsimony | 0.234 | **0.2264** |
  | LIME cost | 226 ms | **3,660.68 ms** |
  | DiCE cost | 2,056 ms | **28,208.84 ms** |
  | Anchors cost | 2,027–68,874 ms | 38,159.37 ms (mean) |

- **Reasoning**: the quality metrics are close enough to be rounding drift, but the cost figures are
  off by factors of 2× (SHAP), 16× (LIME) and 14× (DiCE) and appear to mix per-instance and
  per-run aggregations within one section. The SHAP figure (24,804 ms) is the **pre-recovery-overlay**
  value; integrating the 30-row SHAP recovery batch is what moved it to 11,708 ms, and Paper A
  narrates exactly that move (*"a substantially reduced mean runtime ... relative to earlier
  artifact-only snapshots"*). The thesis never received that update. The "71 bloques calificados"
  denominator is also wrong: SHAP has 75 qualified runs.
- **Impact**: this does not touch H1–H3, which rest on Ch.4's block-level and paired tables — both
  of which re-verified as exact matches to the artifacts. It is confined to the descriptive profile
  section, but that section is where a reader looks up "how expensive is SHAP."

### A06 [minor, FIXED 2026-08-22] — Thesis internal contradiction on Anchors coverage

- **Location**: `capitulo-4-resultados.qmd:356` (*"cobertura de solo 56 celdas calificadas (74.7%)"*)
  vs `capitulo-4-resultados.qmd:37` and `capitulo-3-diseno-experimental.qmd:400`
  (*"57 de 75 celdas (76.0%)"*).
- **Artifact check**: 57 qualified Anchors runs. The 57 / 76.0% figure is correct and is what Paper A
  and Paper B+C both use (Paper B+C: "57/75 artifact-qualified runs"). Ch.4:356 is the outlier.
- **Resolution (2026-08-22)**: `capitulo-4-resultados.qmd:356` corrected to
  *"57 celdas calificadas (76.0%)"*. No other number in the paragraph depends on it.

### A07 [minor, FIXED 2026-08-22] — The "+0.26 (German Credit, RF)" gap is mislabelled in both Paper B+C and the thesis

- **Location**: `paper_bc_jmlr.tex:1036-1037`; `thesis/capitulo-6-conclusiones.qmd:245-246`.
- **Evidence**: both state mean SHAP−Anchors fidelity gaps range *"from +0.26 (German Credit, RF)
  to +0.51 (Breast Cancer, RF)"*.
- **Artifact check**: GC/RF gap = 0.7137 − 0.3510 = **+0.363**. The minimum gap is GC/**XGB**
  (0.7108 − 0.4507 = **+0.260**). BC/RF = +0.514 ✓. The two documents are consistent with each
  other and both wrong against the artifact — a shared-source error, so fix in both.
- **Resolution (2026-08-22)**: both corrected to *"German Credit, XGB"*
  (`paper_bc_jmlr.tex:1039`, `capitulo-6-conclusiones.qmd:246`). The `+0.26` and `+0.51` values
  themselves were correct and are unchanged; only the model label was wrong.

### A08 [minor, FIXED 2026-08-22] — Thesis carries the EXP4 n=147/n=192 defect that Paper B+C already fixed

- **Location**: `thesis/capitulo-5-taxonomia.qmd:291-292,305-307` (table `@tbl-exp4-icc`).
- **Evidence**: the thesis presents ICC(2,1) and Krippendorff's α side by side under a single
  *"$n = 147$ pares"* caption.
- **Artifact check**: `icc_analysis.csv` has `n_cases=147`; `krippendorff_alpha.csv` has
  `n_cases=192`. This is the exact defect logged as F02 in the Paper B+C review and fixed there on
  2026-07-29 (disclosure sentence + caption). The fix was never propagated to the thesis, even
  though the seven values are identical in both documents.
- **Remediation**: port the Paper B+C disclosure sentence and caption wording into Ch.5.
  Note the standing F04 caveat: the EXP4 analysis scripts and raw judge data are absent from the
  repo, so this remains a documented-but-not-re-derivable explanation in either document.
- **Resolution (2026-08-22)**: ported. `capitulo-5-taxonomia.qmd` now carries a Spanish rendering of
  the Paper B+C disclosure sentence (ICC requires a complete cases × judges matrix, hence n=147;
  Krippendorff's α tolerates missing ratings, hence n=192), and the `@tbl-exp4-icc` caption states
  both sample sizes. No values changed. The F04 caveat (missing EXP4 scripts and raw judge data)
  stands and is unaffected.

### A09 [minor] — Thesis archives to a superseded DOI

- **Location**: `thesis/capitulo-3-diseno-experimental.qmd:554-555` and `apendices.qmd:236-237`.
- **Evidence**: thesis cites commit `33fd952a...` / DOI `10.5281/zenodo.19297724`, *"instantánea de
  referencia de abril de 2026."*
- **Cross-check**: Paper A states that this exact DOI *"remains separately archived ... for
  provenance but **does not reflect the evidence cut reported here**"*, and gives the current cut as
  `10.5281/zenodo.21538180` at commit `553f65d71` (2026-07-24).
- **Reasoning**: the thesis reports the current evidence cut's numbers (275 qualified runs,
  $d_z=4.82$/$3.00$) while pointing its reproducibility contract at an archive that predates that
  cut. For a thesis whose central methodological claim is end-to-end traceability, this is the kind
  of gap a committee will probe.

### A10 [minor, FIXED 2026-08-22] — Undisclosed raw-vs-adjusted p-value convention between Paper A and Paper B+C

- **Location**: Paper A `tab:friedman` (`:462-476`) vs Paper B+C `tab:friedman` (`:846-860`).
- **Evidence**: same $\chi^2$ (42.12, 40.68), different p-values: Paper A reports
  3.78e-09 / 7.65e-09, Paper B+C reports 1.51e-08 / 2.29e-08.
- **Artifact check**: `friedman_results.csv` — Paper A reports `p_value_raw`, and labels the column
  "p-value (raw)" with a Holm sentence following ✓. Paper B+C reports `p_value_holm` under a bare
  "$p$-value" heading. The thesis matches Paper B+C (Holm). Both are correct; only Paper B+C's
  label is ambiguous. One-word caption fix.
- **Resolution (2026-08-22)**: `tab:friedman`'s column header is now $p_{\mathrm{Holm}}$ and the
  caption states the values are Holm-Bonferroni-adjusted across the five primary metrics, quoting
  the raw values (3.78e-09 fidelity, 7.65e-09 stability) so the two papers can be reconciled by a
  reader without opening the CSV. No values changed.

### A13 [minor, FIXED 2026-08-22] — Broken cross-reference in thesis Ch.3 (found during rebuild)

- **Location**: `thesis/capitulo-3-diseno-experimental.qmd:619`.
- **Evidence**: the EXP4 design section referenced *"(Tabla @tbl-exp4-dimensiones del Capítulo 5)"*.
  No `tbl-exp4-dimensiones` label exists anywhere in the thesis; Ch.5 defines only
  `tbl-taxonomia-ampliada`, `tbl-taxonomia-benchmark`, and `tbl-exp4-icc`.
- **Detection**: surfaced by the Quarto rebuild —
  `WARNING Unable to resolve crossref @tbl-exp4-dimensiones`. It was not visible in the previous
  rendered output because that output predates the current sources; a dangling crossref renders as
  a literal `?@tbl-exp4-dimensiones` in the DOCX.
- **Resolution (2026-08-22)**: repointed to `@tbl-exp4-icc`, whose first column enumerates the seven
  semantic dimensions the sentence is describing. Re-rendered: no crossref warnings remain.

### A11 [suggestion] — Paper A's headline $d_z$ differs from the other two documents by design

- **Location**: Paper A `tab:shap-lime` (45 matched `logreg/rf/xgb` cells: fidelity $d_z=5.37$,
  stability $4.85$) vs Paper B+C `tab:paired_main` and thesis `@tbl-paired-shap-lime`
  (75 matched cells: $4.82$, $3.00$).
- **Artifact check**: both re-verified exactly against `wilcoxon_shap_lime_primary.csv` (45) and
  `wilcoxon_shap_lime_all_models.csv` (75). Not an error — Paper A declares both sets in
  §sec:methods-inference ("45-cell primary set; 75-cell sensitivity set").
- **Suggestion**: Paper A reports only the 45-cell table in Results while the other two documents
  lead with the 75-cell numbers, so a reader moving between them sees "SHAP beats LIME by
  $d_z=5.37$" and "$d_z=4.82$" for what looks like the same contrast. One sentence in Paper A
  giving the 75-cell values alongside would close the gap at no cost.

### A12 [suggestion] — Thesis F03 (parsimony-direction slip) still open

- **Location**: `capitulo-4-resultados.qmd:315` — *"La parsimonia más alta de todos los métodos
  (0.234 frente a 0.085 de LIME)"* — against the same chapter's later, correct *"LIME es el método
  más parsimonioso en este benchmark."* Parsimony is defined ↓ in Ch.3. Carried forward unchanged
  from the 2026-08-11 review.

## Recency audit

**Status at audit time (2026-08-22, before rebuild):**

| Artifact | Source last modified | Rendered output | Gap |
|---|---|---|---|
| Paper A | `paper_a_prototype_jmlr.tex` 2026-08-22 | PDF 2026-07-24 | PDF predates the edits |
| Paper B+C | `paper_bc_jmlr.tex` 2026-08-22 | PDF 2026-07-29 | PDF predates the F01/F02 fixes **and** the 08-22 edits |
| Paper B+C supplementary | — | PDF 2026-07-26 | not re-verified (Paper B+C review F03, still open) |
| Thesis | `.qmd` 2026-08-22 | `_output/*.docx` 2026-05-10 | rendered output 3.5 months stale, predating all EXP3 and alignment work |

**Resolved 2026-08-22.** All four outputs rebuilt from current sources:

| Artifact | Toolchain | Result |
|---|---|---|
| `paper_a_prototype_jmlr.pdf` | `tools/tectonic-portable/tectonic.exe` | 147.07 KiB, clean; 2 pre-existing underfull-box warnings |
| `paper_bc_jmlr.pdf` | same | 257.32 KiB, clean; 1 overfull hbox (0.90 pt), pre-existing |
| `paper_bc_jmlr_supplementary.pdf` | same | 80.79 KiB, clean |
| `JHerrera_XAI_Tesis_Doctorado.docx` | `thesis/render.ps1` (Quarto to DOCX) | clean; the one crossref warning was A13, now fixed and re-rendered warning-free |

Two toolchain notes for the record:

- The repository's portable Tectonic is the correct builder for both papers. A MiKTeX
  `pdflatex` build of Paper A fails with *"pdfTeX error (font expansion): auto expansion is only
  possible with scalable fonts"* at the bibliography -- an environment/`microtype` interaction, not
  a manuscript defect. Paper B+C happens to build under both, but at ~3x the file size because of
  different font embedding. Use Tectonic per `docs/reports/paper_bc/BUILD.md`.
- `thesis/render.ps1` calls `quarto clean`, which is not a valid command in the installed Quarto
  version and prints `ERROR: Unknown command "clean"` on every run. The render proceeds regardless
  (the script's own `Remove-Item` calls already do the cleaning), but the line should be dropped so
  a real failure is not mistaken for this cosmetic one.

## Working-tree risk -- RESOLVED 2026-08-22

At audit time every alignment fix was uncommitted, including the Paper B+C F01/F02 statistical
fixes that had survived nearly four weeks in the working tree only. Landed in three commits:

- `d1c9ba1d1` -- Paper B+C rigor-review fixes F01/F02 and the EXP3 export path, plus the review
  report that motivated them.
- `00cdc8f3e` -- thesis Ch.3/Ch.6 and Paper A EXP3 scope wording; adds the sync matrix.
- `b09b92a1d` -- the 2026-08-11 thesis review, this audit, and the ACTIVE_CONTEXT update.

## What is confirmed aligned

- **All EXP2 confirmatory statistics** — Friedman $\chi^2$/$W$ (15 blocks), Nemenyi CD 1.211,
  75-cell paired Wilcoxon ($d_z$ 4.82 / 3.00 / 0.84 / 2.63 / 0.45, sign counts 75-0, 74-1, 59-16),
  45-cell paired Wilcoxon — re-derived from artifacts and identical wherever two documents report
  the same quantity.
- **Evidence accounting** — 300 planned / 299 committed / 275 analyzable / 91.7%, 25 unavailable
  cells, Anchors 57/75, DiCE 68/75: consistent across Paper A, Paper B+C and thesis Ch.3/Ch.4/Ch.6
  (sole exception A06).
- **EXP3 LIME extension** — LIME fidelity/stability values and the feature-space moderation
  argument are identical in Paper B+C `tab:exp3_lime` and thesis `sec-exp3-nota`, and match
  `outputs/analysis/exp3_lime_results.csv`. Today's Ch.3 and Ch.6-item-4 edits closed the
  2026-08-11 F02 contradiction correctly.
- **EXP4** — all seven ICC/α values identical across Paper B+C and thesis and matching the
  artifacts; both correctly report it as a negative result.
- **Validity-boundary language** — the synthetic/transparent-model ground-truth,
  dependency-aware-perturbation and human-centered-validation caveats now read compatibly in
  Paper A §sec:formal_framing and Paper B+C §sec:interpretation_scope after today's edits.

## Correction to the sync matrix

`docs/reports/sync/thesis_paper_sync_matrix.md` row "EXP3 cross-dataset status" records Paper A's
narrower SHAP-only check as an accepted scoping choice. Given A01, that row's premise is wrong:
Paper A is not narrower by choice, it is out of date, and its stated reason is false. The row and
the "Source-of-Truth Rule" (which makes Paper A canonical for artifact counts and reproducibility
status) should be revised — Paper B+C is currently the more accurate source for EXP3 scope.

## Questions for the author

1. **A01/A03**: should the two `results/exp3-*` branches be merged into the publication branch?
   Until they are, Paper B+C's and the thesis's EXP3 Anchors claims have no artifact backing on
   the branch their availability sections cite, and Paper A's "never executed" wording is
   defensible only as a statement about the main-line tree.
2. **A03**: which EXP3 SHAP snapshot is canonical — the committed July re-run (BC/XGB fidelity
   0.6165) or the April side-branch run (0.6065)? Why was BC/XGB alone re-run?
3. **A04**: can Ch.5's 0.514 / 0.412 be traced to any artifact, or are they draft-stage
   transcription slips? This determines whether the fix is one line or a full Ch.5 numeric re-audit.
4. **A05**: are the Ch.4 profile cost figures per-instance or per-run, and should the section be
   regenerated from `exp2_run_level_metrics.csv`?
5. **A09**: will a new Zenodo release be cut for the thesis, or should Ch.3/appendix cite the
   existing `10.5281/zenodo.21538180`?
