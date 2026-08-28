# Scientific Rigor Review: PhD Thesis — "Marco para la Evaluación Multinivel de la Explicabilidad en IA" (FOM-7)

**Date**: 2026-08-28 | **Reviewer role**: Scientific Advisor | **Grade**: Accept
**Mean score**: 3.9 | **Dimensions**: D1=3.5 D2=4.5 D3=3.5 D4=3.5 D5'=4.5 D6=4.0

**Scope reviewed**: `thesis/index.qmd`, `introduccion.qmd`, `capitulo-1-marco-teorico.qmd`,
`capitulo-2-fundamentos.qmd`, `capitulo-3-diseno-experimental.qmd`,
`capitulo-4-resultados.qmd`, `capitulo-5-taxonomia.qmd`, `capitulo-6-conclusiones.qmd`,
`apendices.qmd` — full text. Numeric claims were re-derived from
`outputs/analysis/paper_a_exp2_stats/exp2_run_level_metrics.csv`,
`outputs/analysis/lime_kernel_width_sensitivity.csv` and `pub/claim_registry.toml`.

**Prior review**: `docs/review/scientific-rigor-review_thesis_2026-08-11.md` (Accept, 4.3).
F01 (Ch.5 vs Ch.4 numeric contradiction), F02 (Ch.6 "future work" item 4 vs `sec-exp3-nota`)
and F03 (parsimony-direction slip) are **confirmed fixed**. F04, F05 and F06 remain open and
are carried forward below as F10, F11 and F12.

**Regression guards**: `thesis/capitulo-3..6.qmd` and `apendices.qmd` are guarded by RCA-001;
`capitulo-5-taxonomia.qmd` additionally by RCA-002. Both RCAs were read before writing this
report. No manuscript file was edited. `scripts/pubs/verify_claims.py` was run at review time
and is green (61 claims, 111 sites, 16 retired-value guards, 10 cited artifacts).

---

## One-line summary

The thesis is methodologically mature, statistically disciplined and exceptionally honest in
its reporting — the confirmatory core (H1–H3, P1, P2) is exactly traceable to its artifacts —
but its **flagship practical claim, LIME's "structural" instability, is contradicted by two of
the thesis's own results**, and the prescriptive per-instance cost figures in the selection
criteria are not derivable from any committed artifact.

## Strengths

- **The confirmatory core is exact.** Every H1/H2/H3/P1 statistic in Ch.4 and Appendix D
  re-derives from `exp2_run_level_metrics.csv` to the reported precision: SHAP 0.8081 / LIME
  0.5602 / Anchors 0.3886 / DiCE 0.1701 fidelity (block level), stability 0.7320 / 0.0144 /
  0.0429 / 0.3611, Wilcoxon $d_z$ 4.820 / 3.002 / 0.839 / 2.626 / 0.451. The block-level vs
  run-level distinction that caused earlier drift is now handled correctly nearly everywhere.
- **Reporting honesty is the thesis's strongest dimension.** P2 is reported as a *negative*
  result and given its own objective (OE6) rather than buried; the ICC is labelled ICC(1,1)
  with an explicit note that a one-way model is *conservative* relative to ICC(2,1); the
  $n=147$ vs $n=192$ divergence between ICC and Krippendorff's $\alpha$ is disclosed in the
  table caption itself; LIME's parsimony is disclosed as a `num_features=10` configuration
  artifact rather than a property; the masking/feature-correlation confound is stated with the
  admission that "no puede descartarse" that it contributes to the SHAP–LIME fidelity gap.
  Appendix F goes further than most theses would: it names `explanation_eval.j2` and marks it
  "**no** es el instrumento de EXP4", preserving a corrected provenance error in the record.
- **Falsifiability is built in, not retrofitted.** Formal $H_0/H_1$ pairs, a numeric threshold
  fixed in advance for every proposition (CV < 15%, ICC $\geq$ 0.75, accuracy $\geq$ 0.83,
  AUC $\geq$ 0.88, $\tau = 0.95$), an inference plan frozen at Gate 1 and followed exactly,
  and Holm–Bonferroni within three explicitly named families.
- **Cross-reference integrity is clean.** All 69 `{#...}` labels resolve; no dangling
  `@tbl-`/`@fig-`/`@sec-` references remain (the A13 class is closed).
- **Ch.2 states the right epistemic rule.** "El experimento no solo compara 'LIME' como
  etiqueta, sino una configuración concreta de LIME: estrategia de perturbación, kernel,
  número de muestras..." — this is exactly the discipline F01 below asks Ch.6 to honour.
- **The Fronteras de generalización table** remains a rare and genuinely useful device, and
  Ch.5's separation of the taxonomy's *supported* contribution ("operacionalización doctoral
  integradora") from a strong originality claim is well judged.

---

## Findings

### F01 [major] — D1 (Evidence Relevance) / D3 (Scope Calibration) / D4 (Coherence)

- **Location**: `capitulo-6-conclusiones.qmd` §sec-limitaciones (l.208), §sec-futuro item 3
  (l.309), §sec-sintesis; `capitulo-5-taxonomia.qmd` opening; vs.
  `apendices.qmd` @tbl-appendix-lime-kw-sensitivity and `capitulo-6-conclusiones.qmd`
  §sec-exp3-nota.
- **Evidence**: Ch.6 §sec-limitaciones: *"confirmando que la referencia es el mínimo viable y
  que la inestabilidad es estructural, **no dependiente de la configuración del kernel**
  (Apéndice C)."* Ch.6 §sec-futuro item 3, one page later: *"`kernel_width = 10.0` como
  **alternativa más estable** a costa de localidad"*. Appendix C, same reference cell
  (RF, seed 42, $N=100$): `kernel_width = 3.0` → estabilidad **0.000**; `kernel_width = 10.0`
  → estabilidad **0.664**. And §sec-exp3-nota: *"LIME obtiene similitud coseno media de
  $0.922$–$0.927$ en Breast Cancer y $0.748$–$0.854$ en German Credit... La inestabilidad
  estructural de LIME documentada en EXP2 es, por tanto, **dependiente del espacio de
  características, no una propiedad universal del método**."* Yet §sec-sintesis closes with:
  *"El hallazgo de que LIME exhibe inestabilidad estructural —no marginal, sino sistemática,
  con CV=86.2% y similitud coseno media de 0.014— es relevante para **cualquier sistema** de
  apoyo a la decisión que emplee LIME..."*
- **Observation**: The thesis holds two mutually exclusive positions on the same claim. Its own
  sensitivity artifact (`outputs/analysis/lime_kernel_width_sensitivity.csv`, verified: the
  0.664 value is registered as `supp.s2.kw10.stability`) shows stability rising from ~0 to
  0.664 by changing **one hyperparameter**, and EXP3 shows it at 0.75–0.93 on two other
  datasets **at the reference `kernel_width = 3.0`**. Either result alone falsifies "no
  dependiente de la configuración del kernel" and "cualquier sistema". §sec-exp3-nota states
  the correct, narrow conclusion; §sec-limitaciones and §sec-sintesis do not inherit it.
- **Reasoning**: This is the claim Ch.6 itself nominates as *"la afirmación de mayor impacto
  práctico de la tesis"*, and the one an examiner or a practitioner is most likely to act on —
  it is framed as a regulatory argument (EU AI Act, GDPR Art. 22) against deploying LIME. As
  written it overreaches in exactly the way Ch.2 warns against: it compares "LIME as a label"
  rather than the frozen configuration actually measured. The supported claim is materially
  narrower but still valuable and still publishable: *under `kernel_width = 3.0` in Adult
  Income's 103-dimensional one-hot space, LIME's explanations are near-orthogonal under
  $\sigma=0.1$ perturbation; this is a property of the (configuration, feature-space) pair, and
  a practitioner deploying LIME must measure stability in their own space rather than assume
  it.* That is arguably a **more** useful conclusion for the regulatory audience than a blanket
  warning, because it is actionable.
- **Suggestion**: (i) Delete "no dependiente de la configuración del kernel" from
  §sec-limitaciones — it is contradicted two pages later and by the cited appendix; replace
  with "no atribuible a falta de convergencia del muestreo (`num_samples`), aunque sí sensible
  al ancho del kernel: `kernel_width = 10.0` recupera estabilidad 0.664 a costa de fidelidad
  (0.518 → 0.441)". (ii) In §sec-sintesis, replace "cualquier sistema" with the scoped form and
  add one clause carrying the EXP3 finding forward. (iii) Add the same qualifier to Ch.5's
  opening paragraph, which currently states "estabilidad estructural prácticamente nula"
  unqualified. The confirmatory result ($d_z = 3.00$ on 75/75 pairs in Adult) is untouched by
  all three edits.

### F02 [major] — D1 (Evidence Relevance) / D6 (Methodological Rigor)

- **Location**: `capitulo-4-resultados.qmd` §sec-discusion, "Contextos A–D"; and
  `capitulo-6-conclusiones.qmd` §sec-contribuciones, "criterios prescriptivos".
- **Evidence**: Ch.4 Contexto B: *"LIME es viable para modelos logreg/xgb/mlp con costes de
  **3–9 ms**"*. Ch.6: *"TreeSHAP produce estas garantías con un coste de **1–322 ms**/
  instancia"*; *"Los **3–9 ms** de LIME en logreg/xgb/mlp"*; *"Anchors... sus costes de
  **10,000–70,000 ms**/instancia"*; *"DiCE... sus costes moderados (**770–4,500 ms**) son
  aceptables en la mayoría de los contextos"*.
- **Observation**: None of these four ranges is derivable from the committed artifact. Re-derived
  per-model run-level means from `exp2_run_level_metrics.csv`:

  | Claimed | Manuscript | Artifact (per-model run means; min–max of runs) |
  |:--|:--|:--|
  | LIME logreg/xgb/mlp | 3–9 ms | means 73.2 / 122.3 / 51.6 ms; run min 43.2 ms |
  | TreeSHAP (xgb, rf) | 1–322 ms | xgb mean 20.7 (15.7–55.3); **rf mean 2,819.8 (533.2–7,835.6)** |
  | Anchors (rf, svm, mlp) | 10,000–70,000 ms | rf 16,426–67,998; **svm 2,765–80,105**; mlp 10,886–34,063 |
  | DiCE | 770–4,500 ms | **global mean 28,208.8, median 11,880.5**; per-model means 10,746–66,266 |

  The DiCE figure is the most severe: it is roughly an order of magnitude below the artifact and
  is directly contradicted by Ch.4's own DiCE profile (*"Su coste medio (28,209 ms...) lo sitúa
  por debajo de Anchors (38,159 ms) pero muy por encima de SHAP y LIME"*) and by Ch.5 (*"su
  media de 28,209 ms solo mejora a la de Anchors"*). "Costes moderados... aceptables en la
  mayoría de los contextos" is the opposite of what the data shows.
- **Reasoning**: This is the same defect class the 2026-08-23 audit closed as A05 for Ch.4's
  *profile* and *transversal* sections — the fix did not reach the Contexto A–D paragraphs or
  Ch.6's prescriptive criteria, which are precisely the passages a practitioner will read and
  act on. It also exposes a real coverage gap in RCA-001 Phase 1: `verify_claims.py` passes
  green because these ranges were never registered in `pub/claim_registry.toml`. The registry
  holds `A05.dice.cost` as a *retired value* guard, but 770–4,500 is a different unregistered
  string, so nothing catches it.
- **Suggestion**: Re-derive all four ranges from `exp2_run_level_metrics.csv`, state the
  aggregation ("medias por familia de modelo sobre las ejecuciones calificadas"), and register
  each as a claim in `pub/claim_registry.toml` with a per-model resolver so CI holds them. For
  DiCE specifically, the recommendation text needs rewriting, not just the number: DiCE's cost
  is second-worst in the benchmark, so the honest framing is "coste elevado (media 28,209 ms),
  justificable únicamente cuando el objetivo de recourse no admite sustituto". Because these
  are guarded files (RCA-001), run `verify_claims.py` and `verify_sync.py` after the edit.

### F03 [major] — D6 (Methodological Rigor)

- **Location**: `apendices.qmd` §C.1, @tbl-appendix-lime-sensitivity vs
  @tbl-appendix-lime-kw-sensitivity.
- **Evidence**: Both tables declare the same reference condition — RF, semilla 42, $N=100$,
  `num_samples = 1000`, `num_features = 10`, `kernel_width = 3.0` — and report different values
  for it:

  | | Fidelidad | Estabilidad | Coste (ms) | Parsimonia |
  |:--|--:|--:|--:|--:|
  | @tbl-appendix-lime-sensitivity, row "1000 (referencia)" | 0.461 | 0.014 | **226** | 0.085 |
  | @tbl-appendix-lime-kw-sensitivity, row "3.0 (referencia)" | **0.518** | **0.000** | **30** | 0.087 |

- **Observation**: Four of four columns disagree at the identical cell, with cost differing by a
  factor of 7.5 and fidelity by 12%. Neither caption discloses that the two probes were run
  under different conditions. For context, EXP2's own RF/LIME runs cost 299.7–918.7 ms, so
  *both* appendix figures sit below the benchmark range — the probes evidently measure
  something narrower (fewer instances, or a different timing basis) than a full EXP2 run, and
  neither table says so. Only the `kernel_width` table is backed by a committed artifact
  (`outputs/analysis/lime_kernel_width_sensitivity.csv`, registered as `supp.s2.*`); the
  `num_samples` table is not re-derivable from anything in the tree — consistent with the open
  RCA-002 leftover item ("re-run and archive the Table S5 `num_samples` probe").
- **Reasoning**: These two tables are the sole evidence for the claim that LIME's instability is
  not a convergence artifact — a load-bearing claim for F01 above and for §sec-futuro item 3. A
  reader who checks them against each other finds the reference cell disagreeing with itself,
  which undermines both. This is a violation of RCA-001 invariant 6 ("the aggregation level is
  stated wherever a number is reported").
- **Suggestion**: Re-run the `num_samples` probe with the archived script and commit its output
  alongside `lime_kernel_width_sensitivity.csv`; if the two probes genuinely used different
  instance counts or timing bases, state that in both captions and stop calling both rows "la
  referencia". Register the resulting values in `pub/claim_registry.toml`. If the probe cannot
  be re-run before the defense, mark @tbl-appendix-lime-sensitivity explicitly as an
  exploratory measurement not re-derived under the current environment — the honesty register
  the thesis already uses successfully in Appendix F.

### F04 [minor] — D3 (Scope Calibration)

- **Location**: `capitulo-4-resultados.qmd` §sec-discusion "Contexto A";
  `capitulo-6-conclusiones.qmd` §sec-contribuciones.
- **Evidence**: *"SHAP es la opción con mejor evidencia empírica de fidelidad $\geq$ 0.80 y
  estabilidad $\geq$ 0.70. **Para modelos basados en árboles (XGBoost, RF)**, el coste de
  TreeSHAP hace esta elección también eficiente."* and *"**SHAP debe seleccionarse**... en
  cualquier aplicación que requiera fidelidad verificable ($\bar{F} \geq 0.80$) o consistencia
  explicativa ($\bar{S} \geq 0.70$)."*
- **Observation**: Both thresholds hold for SHAP's *global* mean (0.808 / 0.732) but fail in two
  of five model families each — and, awkwardly, in the two families the same sentence
  recommends. Artifact per-model means: fidelity rf **0.729**, mlp **0.725**, xgb 0.759 (only
  logreg 0.946 and svm 0.882 clear 0.80); stability xgb **0.575**, mlp **0.331** (rf 0.949,
  svm 0.925, logreg 0.880). So "Contexto A → use SHAP on XGBoost/RF because it delivers
  $F \geq 0.80$ and $S \geq 0.70$" is false for XGBoost on stability (0.575) and for RF on
  fidelity (0.729).
- **Reasoning**: The thresholds are presented as operational guarantees a practitioner can rely
  on, not as descriptions of a grand mean. This is a scope slip rather than a numeric error —
  the underlying values are all correct elsewhere in Ch.4 — but it converts a benchmark average
  into a per-deployment promise the data does not support.
- **Suggestion**: Restate as conditional on model family, e.g. *"SHAP alcanza $\bar{F} \geq
  0.80$ en logreg y SVM y $\bar{S} \geq 0.70$ en logreg, RF y SVM; en XGBoost la estabilidad
  media desciende a 0.575 y en MLP a 0.331, por lo que el criterio debe verificarse por familia
  de modelo antes del despliegue."* This is a genuinely useful refinement — it is the kind of
  per-model caveat the Fronteras table exists to surface.

### F05 [minor] — D3 (Scope Calibration)

- **Location**: `capitulo-4-resultados.qmd` §sec-discusion and §sec-p1;
  `capitulo-6-conclusiones.qmd` @tbl-objetivos (OE4) and @tbl-fronteras-generalizacion.
- **Evidence**: *"demuestran que el protocolo FOM-7 produce resultados reproducibles (**CV < 3%
  en fidelidad primaria**)"*; OE4: *"**CV < 3% para fidelidad**"*; Fronteras: *"FOM-7 produce
  resultados reproducibles (**CV<3% en fidelidad primaria**)"*. Against, in the same chapter:
  *"el CV en fidelidad para todos los métodos y modelos oscila entre **12.0% (LIME) y 12.8%
  (SHAP)**"*.
- **Observation**: The "< 3%" headline is the RF/$N=100$ subgroup of @tbl-cv-p1 (SHAP 0.8%,
  LIME 2.6%); the benchmark-wide figure is four times larger. "Fidelidad primaria" is doing the
  scope work but does not tell the reader that "primaria" means one model family at one sample
  size — a reader will parse it as "the primary metric, fidelity".
- **Reasoning**: Both figures comfortably satisfy P1's own 15% threshold, so nothing about the
  proposition changes. But the reproducibility headline is repeated in three places including
  the Fronteras table, whose entire purpose is stating scope precisely.
- **Suggestion**: Write "CV < 3% en fidelidad para el subgrupo replicado RF/$N=100$; CV
  $\approx$ 12–13% sobre el conjunto completo de métodos y modelos, ambos dentro del umbral
  P1 del 15%". Note the §sec-p1 "Nota de alcance" already does exactly this for SHAP's
  stability value (0.948 vs 0.732) — apply the same pattern.

### F06 [minor] — D4 (Argument Coherence)

- **Location**: `capitulo-5-taxonomia.qmd` §sec-exp4-fiabilidad (l.287, l.337, l.345) and
  `capitulo-3-diseno-experimental.qmd` §sec-exp4-diseno (l.615).
- **Evidence**: Ch.5: *"**La Brecha 3** identifica que la evaluación semántica crece más rápido
  que su base de validación empírica."*; *"EXP4 confirma cuantitativamente **la Brecha 3**"*;
  *"la operacionalización doctoral de **la Brecha 3**"*. Ch.3: *"la taxonomía del Capítulo 5
  (**Brecha 3**: la evaluación semántica crece más rápido que su base de validación empírica)"*.
- **Observation** (absence): No enumeration of Brechas 1, 2 or 3 exists anywhere in the thesis.
  A full-text search finds "brecha" used only as "brecha de fidelidad" (the metric), "brecha de
  constructo" and "la brecha central de la tesis" (Ch.2, unnumbered). The definite article "La
  Brecha 3" presupposes a numbered list the reader is never shown.
- **Reasoning**: This is the hinge that attaches EXP4 — the taxonomy chapter's only empirical
  component, and the source of the thesis's headline negative result P2 — to the taxonomy it is
  supposed to substantiate. Without the enumeration, the connection is asserted rather than
  shown, and a committee member will ask what Gaps 1 and 2 are. This is the conceptual analogue
  of the dangling-crossref class (A13); the mechanical crossrefs are now clean, so this is the
  last one of its kind.
- **Suggestion**: Add a short subsection to Ch.5 (naturally after §sec-taxonomia-contribucion)
  enumerating the construct gaps the taxonomy exposes — the material largely exists already in
  Ch.2 §"Taxonomias de métricas y brechas de constructo" and in §sec-taxonomia-benchmark's
  "cuadrantes no cubiertos" — and number them so "Brecha 3" resolves. Alternatively, if only
  one gap is meant to carry weight, drop the numbering and name it ("la brecha de validación de
  la evaluación semántica").

### F07 [minor] — D3 (Scope Calibration) / D4 (Coherence)

- **Location**: `capitulo-6-conclusiones.qmd` @tbl-fronteras-generalizacion, row "La
  inestabilidad de LIME es estructural".
- **Evidence**: The row's *No soportada para* cell reads *"Otras configuraciones de LIME; otras
  definiciones de estabilidad (distancia Lipschitz local, varianza de pesos)"* and its
  *Validación futura requerida* cell reads *"Análisis de sensibilidad de hiperparámetros con
  variación sistemática de `num_samples`, `kernel_width` y estrategia de perturbación"*.
- **Observation**: Two problems in one row. (i) The boundary omits **other datasets / feature
  spaces**, even though §sec-exp3-nota four pages earlier reports LIME stability of 0.748–0.927
  on Breast Cancer and German Credit and concludes the instability is "dependiente del espacio
  de características". (ii) The future-work cell requests the `num_samples` and `kernel_width`
  sensitivity analyses that §sec-limitaciones and §sec-futuro item 3 both report as
  **completed** in Appendix C.
- **Reasoning**: This is the same failure mode as the prior review's F02 — a boundary/agenda
  cell drafted before the supporting work landed and not updated afterward — recurring in the
  one table whose function is to state boundaries precisely. It compounds F01: the table that
  should have caught the overreach instead omits the relevant boundary.
- **Suggestion**: Add "otros espacios de características / datasets (véase §sec-exp3-nota:
  estabilidad LIME 0.75–0.93 en BC y GC)" to *No soportada para*, and replace the future-work
  cell with the residual gap: interaction between `kernel_width` and feature-space
  dimensionality, and stability under non-Gaussian perturbation schemes.

### F08 [minor] — D6 (Methodological Rigor)

- **Location**: `apendices.qmd` §C.1, @tbl-appendix-anchors-sensitivity.
- **Evidence**: Caption: *"Sensibilidad de Anchors al umbral de precisión $\tau$ (**RF, semilla
  42**)"*, with a "Cobertura de celdas" column reading 72/75 (96%), **57/75 (76%)**, 31/75 (41%).
- **Observation**: The denominator 75 is the full per-method design ($5$ models $\times$ $5$
  seeds $\times$ $3$ sizes); RF at seed 42 has only three cells. The reference row's 57/75 =
  76.0% is exactly the benchmark-wide Anchors coverage reported in Ch.3 @tbl-coverage-method and
  Ch.4, so the coverage column is design-wide while the caption scopes the table to one model
  and one seed. The fidelity and cost columns may well be RF/seed-42 (fidelity 0.386 is close to
  Anchors' block-level 0.3886), which would mean a single table mixes two scopes.
- **Reasoning**: RCA-001 invariant 6 requires the aggregation level to be stated wherever a
  number is reported; here it is stated *incorrectly* for at least one column. The substantive
  conclusion — $\tau$ is the highest-impact configuration decision for Anchors — is unaffected,
  which is why this is minor rather than major.
- **Suggestion**: Split the scope explicitly: report coverage over the full 75-cell design in
  its own column header ("Cobertura del diseño completo, 75 celdas") and either recompute
  fidelity/cost design-wide too, or label those columns "(RF, semilla 42)" individually. Then
  register the reference row in `pub/claim_registry.toml`.

### F09 [minor] — D6 (Methodological Rigor)

- **Location**: `capitulo-4-resultados.qmd` §sec-perfiles → Anchors.
- **Evidence**: *"**Sobre los bloques calificados**, la fidelidad media es 0.388 y la
  estabilidad **0.052**"*.
- **Observation**: 0.388 and 0.052 are the **run-level** means over Anchors' 57 qualified runs;
  the block-level means over the 15 $(g,n)$ blocks are 0.3886 and **0.0429**. The stability
  figure differs by 21% relative between the two aggregations, and @tbl-friedman-stability in
  the same chapter reports the block-level 0.043 — so the chapter prints both values without
  reconciling them.
- **Reasoning**: Anchors is the method whose coverage is most unbalanced across blocks (57/75,
  concentrated in `logreg` and `mlp`), which is precisely why run-level and block-level diverge
  for it and not for SHAP/LIME (identical to four decimals). Mislabelling the aggregation for
  the one method where it matters is the exact pattern RCA-001 was opened to prevent.
- **Suggestion**: Change to "Sobre las 57 ejecuciones calificadas..." to match the SHAP profile's
  correct wording ("medias consolidadas sobre las 75 ejecuciones calificadas"), and add one
  clause noting that the block-level value used in the Friedman analysis is 0.043 because
  Anchors' coverage is unevenly distributed across blocks.

### F10 [suggestion] — D6 (Methodological Rigor) *(carried from 2026-08-11 F04, unchanged)*

- **Location**: `capitulo-3-diseno-experimental.qmd` § Evaluación cuantitativa del impacto
  estadístico.
- **Evidence**: *"Incluso asumiendo una reducción del poder del 50%... el estadístico de Coste
  sería $\chi^2 \approx 15.2$ ($p \approx 0.0016$)"*.
- **Observation**: Still asserted without derivation; no formula maps a power-loss percentage
  onto a statistic reduction.
- **Suggestion**: Either show the noncentrality halving and the recomputed tail probability, or
  drop the figure — the 290% margin argument stands alone.

### F11 [suggestion] — D5' (Reporting Honesty) *(carried from 2026-08-11 F05, unchanged)*

- **Location**: `capitulo-3-diseno-experimental.qmd` § Cobertura de artefactos;
  `capitulo-6-conclusiones.qmd` §sec-limitaciones.
- **Observation** (absence): Anchors' 24% missingness is caused by non-convergence to a rule
  meeting $\tau = 0.95$ — outcome-dependent (MNAR) missingness concentrated in the hardest
  blocks. Ch.3 quantifies the *variance* impact ($\sqrt{5/2.3} \approx 1.47$) but never names
  the *direction* of the resulting selection bias. Appendix C now strengthens the case: at
  $\tau = 0.90$ coverage rises to 96% and mean fidelity rises to 0.421, versus 0.386 at
  $\tau = 0.95$ — i.e. the excluded cells are not neutral.
- **Suggestion**: One sentence in §sec-limitaciones: non-convergence exclusion is not
  missing-at-random and plausibly biases Anchors' reported quality metrics *optimistically*;
  the $\tau = 0.90$ row of @tbl-appendix-anchors-sensitivity gives an empirical handle on the
  size of the effect. This strengthens rather than weakens the "usar con cautela" recommendation.

### F12 [suggestion] — D3 (Scope Calibration) *(carried from 2026-08-11 F06, unchanged)*

- **Location**: `capitulo-6-conclusiones.qmd` §sec-contribuciones, "criterios prescriptivos".
- **Observation**: "Prescriptivos" plus bare imperative ("SHAP **debe** seleccionarse") remains
  a stronger register than the conditional discipline Ch.2 commits the thesis to, and sits in
  tension with @tbl-fronteras-generalizacion, which restricts the same criteria to "Condiciones
  del benchmark descritas". F04 above makes this more pressing than it was in August: the
  imperative is attached to thresholds that do not hold per model family.
- **Suggestion**: Open the subsection with one sentence cross-referencing the Fronteras table,
  or soften to "criterios orientativos con fundamento empírico".

### F13 [suggestion] — D6 (Methodological Rigor) / process

- **Location**: `pub/claim_registry.toml` coverage vs `apendices.qmd` §C.1 and
  `capitulo-6-conclusiones.qmd` §sec-contribuciones.
- **Observation**: `verify_claims.py` is green (61 claims / 111 sites), yet F02, F03, F08 and
  F09 all passed through it — because the numbers involved are simply **not registered**. The
  registry covers EXP2 aggregate metrics, EXP3, EXP4, the corpora and the supplementary tables,
  but not the per-model cost/quality figures that the prescriptive criteria are built on, and
  not @tbl-appendix-lime-sensitivity or @tbl-appendix-anchors-sensitivity.
- **Reasoning**: Not a defect in the manuscript, but a scoping observation for the open Task 3
  (RCA-001 Phase 2). Phase 1's guarantee is "a registered number matches its artifact"; the
  failure mode this review actually found is "a load-bearing number was never registered". A
  green verifier reads as broader assurance than it is.
- **Suggestion**: Before Phase 2's macro generation, do a registration-completeness sweep:
  enumerate every numeric literal in Ch.4–Ch.6 and the appendices and require each to be either
  registered, or explicitly annotated as unbacked (the Appendix F pattern). Consider adding a
  `verify_claims.py` check that reports *unregistered numeric literals* in guarded manuscript
  files, so absence-of-registration is visible rather than silent.

---

## Dimension rationale

| Dim | Score | Rationale |
|:--|:--:|:--|
| **D1** Evidence Relevance | 3.5 | Confirmatory claims (H1–H3, P1, P2) trace exactly to artifacts, verified independently. Deducted for F01 (headline instability claim contradicted by two of the thesis's own results) and F02 (four cost ranges with no artifact backing, one contradicting the same chapter). |
| **D2** Falsifiability | 4.5 | Formal $H_0/H_1$, thresholds fixed in advance for every proposition, decision rules stated per hypothesis, negative result reported against its own pre-set threshold. Deducted only for F10 (the $\chi^2 \approx 15.2$ sensitivity figure a reader cannot check) and the prescriptive cost ranges, which are not falsifiable as stated. |
| **D3** Scope Calibration | 3.5 | The Fronteras table and §sec-exp3-nota calibrate scope unusually well; the problem is *propagation*, not absence — the correct qualifier exists in one place and is missing from the synthesis (F01), the thresholds (F04), the reproducibility headline (F05) and the boundary table's own row (F07). |
| **D4** Argument Coherence | 3.5 | Prior F02 fixed; crossrefs clean; the motivation→gap→method→results→conclusion arc is strong. Deducted for the internal contradiction on kernel dependence (F01), the orphan "Brecha 3" (F06), the DiCE cost contradiction across Ch.4/Ch.5/Ch.6 (F02) and the stale Fronteras row (F07). |
| **D5'** Reporting Honesty | 4.5 | Best dimension. Negative result promoted to an objective; ICC conservatively relabelled with an explanatory note; $n=147$/$n=192$ disclosed in-caption; parsimony disclosed as a config artifact; masking confound admitted as possibly explaining part of the headline gap; a corrected provenance error preserved in Appendix F. Deducted for F11 (MNAR direction still undisclosed) and F03's un-re-derived probe not being flagged as such. |
| **D6** Methodological Rigor | 4.0 | Frozen models and preprocessor, leakage controls, seeds, block-level inference against pseudoreplication, Friedman + Nemenyi + Wilcoxon with Holm within named families, effect sizes, coverage-impact analysis, four sensitivity studies. Deducted for F03 (reference cell disagreeing with itself), F08 and F09 (aggregation scope mislabels) and F02. |

**Mean**: (3.5 + 4.5 + 3.5 + 3.5 + 4.5 + 4.0) / 6 = **3.92 → 3.9**
**Grade**: **Accept** (mean $\geq$ 3.8, no dimension < 2).

The score is lower than the 2026-08-11 review's 4.3 not because the thesis got worse — three of
that review's findings were fixed and the confirmatory core verified clean against artifacts
this time — but because this pass re-derived numbers from the artifacts rather than checking
internal consistency alone, which surfaced F02 and F03. F01 was reachable in August but was
not found then.

## Readiness assessment

**Defensible as-is? Yes, with reservations.** The doctoral contribution is intact and none of
the findings touches H1, H2, H3, P1 or P2, the statistical plan, or the FOM-7 protocol itself.
The confirmatory evidence chain re-derives exactly. But two of the findings are in passages an
examiner is likely to probe — the practical selection criteria (F02, F04) and the thesis's
self-nominated highest-impact claim (F01) — and both are checkable in minutes against the
repository the thesis itself publishes. F01 in particular is the kind of finding a committee
enjoys: the contradiction is between two paragraphs of the same chapter.

**Recommended before defense** (est. half a day of editing, no re-analysis required):

1. **F01** — scope the LIME instability claim in §sec-limitaciones, §sec-sintesis and Ch.5's
   opening. *Highest priority; it is a one-paragraph fix to the thesis's flagship claim.*
2. **F02** — re-derive the four cost ranges and rewrite the DiCE recommendation.
3. **F04** — make the SHAP $F \geq 0.80$ / $S \geq 0.70$ thresholds conditional on model family.
4. **F06** — define the Brechas, or drop the numbering.
5. **F07**, **F05**, **F09** — three sentence-level corrections.

**Recommended if time allows**: F03 (re-run or explicitly flag the `num_samples` probe), F08,
F11, F12, F10.

**Handoff**: F01, F02, F04, F05, F06, F07, F09, F12 are prose/scope fixes → `manuscript-editing`
(Scientific Editor). F03, F08, F10, F11 involve re-derivation or statistical argument → Data
Scientist. F13 is a Task 3 / RCA-001 Phase 2 scoping input → Architect.

**Guard note**: every file implicated (Ch.3–Ch.6, `apendices.qmd`) is guarded by RCA-001, and
Ch.5 also by RCA-002. Remediation must run `scripts/pubs/verify_claims.py` and
`scripts/pubs/verify_sync.py`, and any newly derived number should be registered in
`pub/claim_registry.toml` rather than typed into the manuscript — F02 and F13 are the same
problem seen from two sides.

**Cross-document note (not a thesis finding)**: F01, F02 and F04 concern claims the thesis
shares with Paper A and Paper B+C. Per RCA-001 invariant 3, whichever fix is adopted should be
checked against `docs/reports/sync/thesis_paper_sync_matrix.md` and applied to every document
carrying the quantity, not to the thesis alone.

## Questions for the author

- **F01**: is the intended claim "LIME is unstable in high-dimensional one-hot tabular spaces at
  `kernel_width = 3.0`" or the broader "LIME is unstable"? The evidence supports the first
  cleanly and the second not at all — but the first is the more useful claim for the regulatory
  argument, since it tells a practitioner what to measure. Which do you want to defend?
- **F02**: where did 770–4,500 ms (DiCE), 3–9 ms (LIME) and 1–322 ms (TreeSHAP) come from? If
  they are per-instance medians from a pilot run rather than run-level means from EXP2, that is
  a defensible aggregation — but it must be stated, and the DiCE figure still contradicts
  Ch.4/Ch.5 whichever aggregation is meant.
- **F03**: were @tbl-appendix-lime-sensitivity and @tbl-appendix-lime-kw-sensitivity produced by
  the same probe script? If not, can the `num_samples` probe be re-run under the current
  environment before the defense, or should it be flagged as historical?
- **F06**: does a numbered list of construct gaps (Brecha 1, 2, 3) exist in a draft that did not
  make it into the current Ch.5, or was "Brecha 3" always shorthand for the semantic-evaluation
  gap alone?
