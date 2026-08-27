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

### A01 [major, RESOLVED 2026-08-23] — Paper A denies experimental work that exists and is published elsewhere

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
- **Resolution (2026-08-23)**: author approved the merge. The 12 Anchors run directories (1,768
  files) were imported from `results/exp3-windows-breast-cancer` via
  `git checkout <branch> -- <anchors paths>` rather than a full branch merge — that branch diverged
  at `89fae3d45` and carries stale docs plus junk paths (`.venvScriptspython.exe`, a file named
  `[14`) that must not reach the publication branch. No SHAP result was touched. Re-verified on the
  merged tree with July-canonical SHAP: SHAP > Anchors in 12/12 seed-level pairs, gap range
  +0.2601 (GC/XGB) to +0.5137 (BC/RF) — unchanged from what was already published.
  Paper A §sec:exp3, the Conclusion limitation bullet, and §Code and Artifact Availability were
  rewritten: the Anchors cohort is now described as executed on an earlier environment and released
  with this snapshot, and the `alibi`/`dice-ml` block is correctly scoped to the current
  environment and the 25 EXP2 cells.
- **Root cause (identified 2026-08-23)**: `scripts/run_exp3_shap_configs.py`, the July runner, opens
  with *"These don't need alibi/dice-ml, unlike the 12 Anchors configs in the same experiment set,
  which remain blocked by a numpy<2.0 vs. Python 3.13 environment incompatibility."* That statement
  is true **of the July environment**. Paper A was drafted from the July snapshot and generalized it
  into "could not be executed," losing the fact that the April environment had already run them.

### A02 [major, RESOLVED 2026-08-23] — The 2026-08-22 Paper A edit fixed the symptom in one place and left it in two others

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
- **Resolution (2026-08-23)**: problem (ii) closed alongside A01. §sec:exp3 and the Conclusion bullet
  no longer describe the Anchors cohort as unexecuted, so Paper A is internally consistent again and
  consistent with the other two documents.

### A03 [major, RESOLVED 2026-08-23] — Paper A and Paper B+C report different values for the same EXP3 SHAP cell

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
- **Resolution (2026-08-23)**: author selected the **July** snapshot as canonical. Paper B+C
  `tab:exp3_fidelity` BC/XGB corrected 0.607 → **0.617**, the BC/XGB SHAP−LIME fidelity gap follows
  (+0.06 → **+0.07**, from 0.6165 − 0.5433), and the caption now names the snapshot the SHAP column
  is drawn from. The gap range quoted in both Paper B+C and thesis `sec-exp3-nota` (+0.26 to +0.51)
  was re-verified against the merged tree and is unchanged.
- **Why only BC/XGB was re-run (investigated 2026-08-23)**: it was not re-run alone — all 12 SHAP
  configs were re-executed on 2026-07-23/24, and per-run cost differs everywhere by timing noise.
  BC/XGB is the only cell whose *quality* metrics moved (sparsity 0.3333 → 0.8822, fidelity
  0.6065 → 0.6165, stability 0.9531 → 0.9625); BC/RF, GC/RF and GC/XGB reproduced bit-identical
  fidelity. The cause is not the model and not the code: the EXP3 models were retrained 2026-05-10
  with identical config and **identical test metrics** (BC/XGB accuracy 0.9474, ROC-AUC 0.9934,
  same confusion matrix), and the July runner is a thin wrapper over the same `ExperimentRunner`
  and the same YAML configs. The signature is in the attribution vectors: in April the BC/XGB
  explanation had 10 of 30 features above the 1e-4 activity threshold; in July it had ~26.5 of 30.
  A denser TreeExplainer output for the same tree ensemble points to a SHAP/XGBoost library change
  between the April (numpy<2) and July (Python 3.13) environments — the same environment migration
  that made Anchors unrunnable in July. The remaining uncertainty is which library and version;
  pinning that would need the two environments' lockfiles, which are not in the repo.

### A04 [major, RESOLVED 2026-08-23] — Thesis F01 (Ch.5 vs Ch.4 numeric contradiction)

- **Location**: `thesis/capitulo-5-taxonomia.qmd:20,35-36` vs `capitulo-4-resultados.qmd:93-94,378,390`.
- **Evidence**: Ch.5 still reads *"(SHAP: 0.810, LIME: 0.560, Anchors: 0.514, DiCE: 0.412)"* and
  *"La parsimonia media de DiCE (0.085 ...) y su fidelidad baja (0.412)"*.
- **Artifact check**: run-level means over qualified runs are Anchors fidelity **0.3880**, DiCE
  fidelity **0.1716**, DiCE sparsity **0.0166**; block-level means are 0.389 / 0.170 / 0.0166.
  Ch.5's 0.514 and 0.412 match **neither** aggregation, and 0.085 is LIME/Anchors' parsimony,
  not DiCE's.
- **Status**: carried forward unchanged from the 2026-08-11 review (F01, major). It remains the
  single most examiner-visible defect in the thesis, because the thesis's own gate 7 is a
  claim-traceability guarantee. Open since 2026-08-11; closed 2026-08-23.

#### Provenance answered (2026-08-23)

The 2026-08-11 review asked whether 0.514 / 0.412 trace to some other aggregation or are draft
slips. They are draft slips, and the evidence is decisive:

- `git log -S "Anchors: 0.514"` returns exactly one commit, `f639935d0` (2026-05-10, *"resolve
  editor feedback ... and integrate EXP4 into thesis"*). The whole paragraph arrives as new `+`
  lines — the numbers were not carried over from an earlier revision.
- At that commit, `outputs/analysis/` **did not exist in the repository**. `git ls-tree -r
  f639935d0 outputs/analysis/` returns nothing; the EXP2 inferential exports were first committed
  in `553f65d71` (July). So when this paragraph was written there was no committed artifact to
  check the numbers against.
- No file in the repository, at any commit, contains 0.514 or 0.412 as an Anchors or DiCE fidelity.

So the fix is a numeric correction, not a re-derivation from some other cohort.

#### Full numeric audit of the Ch.5 opening

The scope is wider than the two numbers named in the original finding. Against
`exp2_run_level_metrics.csv`:

| Ch.5 claim | Stated | Artifact | Verdict |
|---|---|---|---|
| LIME fidelity | 0.560 | 0.5602 | correct |
| LIME stability | 0.014 | 0.0144 | correct |
| LIME stability CV | 86.2% | 86.2% | correct |
| SHAP fidelity | 0.810 | 0.8081 | rounds to 0.808 |
| SHAP stability | 0.724 | **0.7320** | wrong — same stale value fixed in Ch.4 under A05 |
| $d_z$ fidelity / stability | 4.82 / 3.00 | 4.820 / 3.002 | correct |
| DiCE parsimony | 0.085 | **0.0166** | wrong — 0.085 is LIME/Anchors |
| DiCE fidelity | 0.412 | **0.1716** | wrong |
| Anchors fidelity | 0.514 | **0.3880** | wrong |
| DiCE "óptimo en parsimonia y eficiencia" | — | parsimony 0.0166 (best); cost 28,209 ms (2nd worst) | parsimony correct, **efficiency claim wrong** |

The qualitative argument of the chapter — no method dominates every axis, fidelity and stability
are non-redundant — survives every correction. The DiCE efficiency claim is the only one that needs
rewording rather than renumbering: DiCE is the most parsimonious method but is not cheap.

#### Applied 2026-08-23 (author approved)

- *"(SHAP: 0.810, LIME: 0.560, Anchors: 0.514, DiCE: 0.412)"* → *"(SHAP: 0.808, LIME: 0.560,
  Anchors: 0.388, DiCE: 0.172)"*
- *"La parsimonia media de DiCE (0.085 características activas) y su fidelidad baja (0.412)"* →
  *"La parsimonia media de DiCE (0.017 de ratio activo, la más concisa del benchmark) y su fidelidad
  baja (0.172)"*
- *"estabilidad de 0.724"* → *"estabilidad de 0.732"*
- *"perfil óptimo en parsimonia y eficiencia"* → *"perfil óptimo en parsimonia --aunque no en coste,
  donde su media de 28,209 ms solo mejora a la de Anchors--"*

A sweep of the rest of Ch.5 found no further benchmark numbers: the only other figures in the
chapter are the EXP4 ICC/Krippendorff values, already verified against
`outputs/analysis/exp4_llm_evaluation/`. Thesis re-rendered clean.


### A05 [major, RESOLVED 2026-08-23] — Thesis per-method profile section is built on a pre-recovery snapshot

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
- **Answer to "is it worth stating both?" (2026-08-23)**: stating both aggregations would be worth
  it if both were currently true at different levels. They are not. Every plausible aggregation was
  computed from `exp2_run_level_metrics.csv` — mean of run-level values, median of run-level values,
  per-model mean, per-model median — and **none** reproduces the thesis's 24,804 / 226 / 2,056 ms.
  Those are simply superseded values. What *is* worth stating is the mean **and** the median,
  because the cost distribution is extremely heavy-tailed (SHAP mean 11,708 ms vs median 684 ms),
  and a single mean invites the reader to think SHAP costs 12 seconds per instance in the typical
  case when the typical case is under a second.
- **Root cause (identified 2026-08-23)**: two separate problems, not one. (i) The SHAP figures
  predate the 30-row recovery overlay. (ii) The §Análisis transversal subsection silently mixed
  **per-model means** with **single-cell Appendix C sensitivity values** — "SVM ... 0.928 ... 159,059
  ms" is the `k=50` row of `@tbl-appendix-shap-sensitivity` (SVM, seed 42, N=100), not the 15-run
  SVM mean (0.882 / 54,231 ms). Likewise XGB "1.2 ms" and logreg "85 ms".
- **Resolution (2026-08-23)**: both subsections rewritten from the artifact with the aggregation
  stated explicitly in each. SHAP 0.808 / 0.732 / 0.226 / 0.380 / 11,708 ms mean with 684 ms median
  over **75** qualified runs (the "71 bloques" denominator was also wrong); LIME cost 3,661 ms mean
  / 65.7 ms median; Anchors fidelity 0.388, cost 38,159 ms mean; DiCE cost 28,209 ms mean / 11,880 ms
  median. Per-model: SHAP SVM 0.882, MLP 0.725, XGB cost 21 ms, SVM cost 54,231 ms, logreg 936 ms;
  Anchors SVM 37,415 ms, MLP 15,564 ms. The N-effect SHAP means were stale too
  (0.811/0.804/0.814 → **0.809/0.809/0.807**); the "differences below 0.010" claim tightens to 0.002
  and still holds. The KernelSHAP scaling argument now cites Appendix C explicitly as a single-cell
  study instead of borrowing its numbers as per-model summaries.

### A14 [major, OPEN — found 2026-08-24 while building RCA-001 Phase 1]

Paper B+C's review corpus has no committed artifact at the size it claims.

- **Location**: `paper_bc_jmlr.tex` — abstract ("48-paper structured scoping
  corpus"), `tab:prisma` ("Included in coded corpus: **48**"), `tab:corpus_profile`
  ("Unique coded papers: 48"), §Gap 1 ("29 of 48 coded studies"), and the
  second-reviewer audit ("16 papers, one third of the coded corpus").
- **Evidence**: the only review-corpus artifact in the repository,
  `docs/reports/paper_c/paper_c_review_corpus.csv`, has **24 rows**. `git log`
  shows it added once, in `8d2864f56`, and no 48-row corpus exists at any commit.
  Paper C's abstract (via `pub/claims.toml`) says "cleaned **24**-study coded
  review corpus", which matches the artifact.
- **Reasoning**: Paper B+C is internally consistent at 48 — the cluster
  distribution sums to 48 and the "one third" audit fraction works — so this is
  not an arithmetic slip inside the paper. Either the 48-paper corpus was built
  and never committed, or the corpus grew from 24 to 48 without the artifact
  being updated. Paper B+C's §Code and Artifact Availability tells readers "the
  review corpus CSV underlying the taxonomy and gap analysis is also available in
  the companion repository," which is currently true only of a 24-row file
  describing a different paper.
- **Severity**: this is the same class as F04 (EXP4 scripts and raw judge data
  missing) but load-bearing for a headline contribution: the taxonomy and all
  three gap claims rest on this corpus, and the paper's own single-reviewer
  limitation discussion invites a reviewer to inspect it.
- **Deliberately not registered** in `pub/claim_registry.toml`: doing so would
  either encode a number with no backing artifact or force CI red from day one.
  The registry carries a comment at that point explaining why.
- **Resolution requires the author**: commit the 48-paper corpus, or correct
  Paper B+C to the corpus that exists. I cannot determine which is right.

- **Progress (2026-08-26)**: the *source material* is now assembled — all 44
  identifiable corpus PDFs are collected under `docs/reports/paper_bc/corpus_pdfs/`,
  named by citation key, each verified as the correct paper (PDF header, size floor,
  page-one title match). Provenance per paper in `corpus_pdfs/RETRIEVAL_LOG.md`.
  **A14 remains open**: the PDFs are the input, not the deliverable. What Paper B+C
  actually needs is the coded corpus CSV, and 28 of the 44 still require an
  include/exclude decision and four-axis coding. The remaining ~4 of the claimed 48
  were coded but never cited, so they are not recoverable from the citation record.

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

### A09 [minor, RESOLVED 2026-08-23] — Thesis archives to a superseded DOI

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

### A12 [suggestion, RESOLVED 2026-08-23] — Thesis F03 (parsimony-direction slip) still open

- **Location**: `capitulo-4-resultados.qmd:315` — *"La parsimonia más alta de todos los métodos
  (0.234 frente a 0.085 de LIME)"* — against the same chapter's later, correct *"LIME es el método
  más parsimonioso en este benchmark."* Parsimony is defined ↓ in Ch.3. Carried forward unchanged
  from the 2026-08-11 review.
- **Resolution (2026-08-23)**: fixed incidentally while rewriting the profile section for A05. The
  SHAP paragraph now reads *"El ratio activo más alto de todos los métodos (0.226 frente a 0.085 de
  LIME) ... por la dirección de la métrica (§sec-metricas), esto significa que SHAP es el método
  *menos* parsimonioso del benchmark,"* and the LIME paragraph states explicitly that LIME is the
  most parsimonious. The two passages now agree.

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

`docs/reports/sync/thesis_paper_sync_matrix.md` originally recorded Paper A's narrower SHAP-only
EXP3 check as an accepted scoping choice and made Paper A canonical for artifact counts and
reproducibility status. A01 showed that premise was wrong for EXP3. The matrix has been updated:
the EXP3 row now records the true history, three rows were added (EXP3 SHAP snapshot, EXP4 sample
sizes, archive DOI), and the checklist tracks each finding. As of 2026-08-23 every row is closed
except the Ch.5 numeric contradiction.

## Status

| Finding | Severity | Status |
|---|---|---|
| A01 Paper A denies executed EXP3 Anchors work | major | Resolved 2026-08-23 — artifacts imported, Paper A rewritten |
| A02 partial fix left two sites stale | major | Resolved 2026-08-23 |
| A03 same EXP3 cell, two values | major | Resolved 2026-08-23 — July canonical, Paper B+C corrected |
| A04 thesis Ch.5 vs Ch.4 numbers | major | Resolved 2026-08-23 — four-part edit applied, Ch.5 swept |
| A05 thesis Ch.4 profile on stale snapshot | major | Resolved 2026-08-23 — both subsections regenerated |
| A06 Anchors coverage 56 vs 57 | minor | Fixed 2026-08-22 |
| A07 EXP3 minimum-gap model mislabelled | minor | Fixed 2026-08-22 |
| A08 EXP4 n=147/192 not in thesis | minor | Fixed 2026-08-22 |
| A09 thesis on superseded DOI | minor | Resolved 2026-08-23 |
| A10 raw vs Holm p-value labelling | minor | Fixed 2026-08-22 |
| A13 dangling crossref in Ch.3 | minor | Fixed 2026-08-22 |
| **A14 Paper B+C 48-paper corpus has no artifact** | **major** | **OPEN — 44/44 PDFs collected 2026-08-26; corpus coding outstanding** |
| A11 Paper A 45-cell vs 75-cell $d_z$ | suggestion | Open, no action requested |
| A12 parsimony-direction slip | suggestion | Resolved 2026-08-23 |

Carried over from earlier reviews and still open, unchanged by this pass:
Paper B+C **F03** (supplementary tables never independently re-derived) and **F04** (EXP4 analysis
scripts and raw judge data absent from the repository; accepted as-is on 2026-07-30).

## Outcome

All thirteen findings from the original audit are closed. Two were found by the remediation itself: A13 by rebuilding the thesis, and **A14 by building the claim verifier** — Paper B+C's 48-paper corpus has no committed artifact. A14 is open and needs the author. The only items
still outstanding in the publication set are carried over from earlier reviews and were accepted
as-is by the author: Paper B+C **F03** (supplementary tables never independently re-derived) and
**F04** (EXP4 analysis scripts and raw judge-response data absent from the repository; investigated
2026-07-30 and confirmed unrecoverable without re-running EXP4). **A11** (Paper A leads with the
45-cell $d_z$ while the other two documents lead with the 75-cell values) remains an open
suggestion; both sets are declared and correct, so no action was requested.
