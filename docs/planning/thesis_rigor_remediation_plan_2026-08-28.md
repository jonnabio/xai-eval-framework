# Implementation Plan — Thesis Rigor Review Remediation (2026-08-28)

**Role**: Architect | **Mode**: PLANNING | **Created**: 2026-08-28
**Source review**: `docs/review/scientific-rigor-review_thesis_2026-08-28.md` (Accept, 3.9/5)
**Related**: RCA-001 (manuscript-artifact drift), RCA-002 (EXP4 source recovery),
Task 3 (RCA-001 Phase 2), `docs/reports/sync/thesis_paper_sync_matrix.md`

---

## 1. Analyze — what actually has to change

13 findings: 3 major, 6 minor, 4 suggestions. None touches H1–H3, P1, P2, the statistical
plan, or the FOM-7 protocol. Every fix is prose, scope wording, or number re-derivation —
**no experiment needs re-running** except the optional Table S5 probe (F03).

### Blast radius, verified against the actual files

| Finding | Thesis | Paper A | Paper B+C | Supplementary |
|:--|:--|:--|:--|:--|
| **F01** LIME instability scope | Ch.5 opening, Ch.6 §sec-limitaciones, §sec-sintesis | **clean** — §636 is already exemplary | main text ~l.1297 needs a reconciling clause (l.1041 already correct) | **clean** — Table S2 already discloses kw=10.0 |
| **F02** cost ranges | Ch.4 Contextos A–D, Ch.6 §sec-contribuciones | clean (aggregates only, registered) | clean | — |
| **F04** $F\geq0.80$ / $S\geq0.70$ | Ch.4 l.575, Ch.6 l.116-118 | clean | clean | — |
| F03, F08 | `apendices.qmd` §C.1 | — | — | S2 clean; S5 shares the probe |
| F05, F06, F07, F09 | thesis only | — | — | — |

**This is the key scoping result: F02 and F04 are thesis-only.** Paper A carries only the
aggregate costs (3,660.68 / 11,708.26 ms), which are correct and registered. Only F01 crosses
documents, and only into one Paper B+C paragraph.

### Root cause (feeds Task 3)

`verify_claims.py` is green — 61 claims, 111 sites — yet F02, F03, F08 and F09 all passed
through it, because **those numbers were never registered**. Phase 1 guarantees "a registered
number matches its artifact"; the failure mode found is "a load-bearing number was never
registered". The remediation must therefore be *registry-first*: register the values, then let
the prose consume them. Fixing the prose alone rebuilds the same defect.

---

## 2. Discuss — decisions (RESOLVED 2026-08-28)

**All three decisions were taken by the author on 2026-08-28. No blockers remain; T2.1 and T2.6
are unblocked and the plan is ready to execute.**

### D1 (F01) — which claim does the thesis defend? → **DECIDED: Option A (narrow, configuration-scoped)**

| Option | Claim | Cost | Consequence |
|:--|:--|:--|:--|
| **A (recommended)** | "Under `kernel_width=3.0` in Adult's 103-dim one-hot space, LIME's explanations are near-orthogonal under $\sigma=0.1$ perturbation. This is a property of the (configuration, feature-space) pair; practitioners must measure stability in their own space." | ~3 paragraphs | Fully supported by all evidence. *Stronger* for the regulatory audience — it is actionable, and it converts EXP3 from an embarrassment into a second contribution. |
| B | Keep the broad claim, demote EXP3 and the kw=10.0 row to caveats | ~1 paragraph | Not defensible: contradicted by the thesis's own Appendix C and §sec-exp3-nota. Not recommended. |

**Decision (2026-08-28): Option A.** The thesis defends the configuration- and feature-space-
scoped claim. The confirmatory result ($d_z=3.00$, 75/75 pairs) is untouched; only the
generalization language changes. EXP3's cross-dataset stability (0.75–0.93) and Appendix C's
kw=10.0 row (0.664) are promoted from contradictions to a second reported finding: LIME's
stability is modulated by feature-space geometry and kernel width, so it must be measured
per deployment rather than assumed. T2.1 implements this across Ch.5 opening,
Ch.6 §sec-limitaciones and §sec-sintesis; T3.1 propagates it to Paper B+C.

### D2 (F03) — the Table S5 `num_samples` probe → **DECIDED: (a) re-run, 1h timebox**

- **(a)** Re-run with `src/scripts/run_sensitivity_analysis.py`, commit the CSV, register it.
  Closes F03 and the open RCA-002 leftover in one move. Est. +1h.
- **(b)** Mark @tbl-appendix-lime-sensitivity as an exploratory measurement not re-derived under
  the current environment — the Appendix F pattern the thesis already uses successfully.

**Decision (2026-08-28): (a), timeboxed to one hour.** Re-run `src/scripts/run_sensitivity_analysis.py`,
commit the CSV, register the values (T1.3), and reconcile the two appendix reference cells.
If the script does not run clean within the hour, fall back to (b) — disclose
@tbl-appendix-lime-sensitivity as an exploratory measurement not re-derived under the current
environment — and close the RCA-002 leftover with that disclosure. The defense path must not
wait on a probe.

### D3 (F12) — keep "criterios prescriptivos"? → **DECIDED: keep + scope sentence**

**Decision (2026-08-28): keep "prescriptivos" and the imperative mood, add one opening sentence
cross-referencing @tbl-fronteras-generalizacion.** F04's fix (T2.4) removes the sharpest part
of the tension by making the $F\geq0.80$ / $S\geq0.70$ thresholds conditional on model family,
so the imperative is no longer attached to a threshold that fails in 2/5 families. F12 is
therefore promoted from Phase 4 (optional) to **T2.9 in Phase 2**, since it is now a one-line
addition adjacent to an edit T2.4 already makes in the same subsection.

---

## 3. Plan — tasks

Sequenced so that **no prose edit is made before the number it cites is registered**.

### Phase 1 — Registry first (closes F02's root cause; feeds Task 3)

| ID | Task | Files | Est. |
|:--|:--|:--|:--|
| T1.1 | Add per-model, per-method **cost** resolvers + claims (20 cells: 4 methods × 5 models, run-level means) | `pub/claim_registry.toml`, `scripts/pubs/claim_sources.py` | 1.5h |
| T1.2 | Add per-model **fidelity/stability** claims for SHAP (10 cells) — backing for F04 | same | 0.5h |
| T1.3 | Register Appendix C reference rows: LIME `num_samples` (pending D2), Anchors $\tau$ (F08) | same | 0.5h |
| T1.4 | Retire-value guards for the four bad ranges so they can never return: `770–4,500`, `3–9 ms`, `1–322 ms`, `10,000–70,000` | `pub/claim_registry.toml` | 0.25h |

Reference values already re-derived from `outputs/analysis/paper_a_exp2_stats/exp2_run_level_metrics.csv`
during the review (per-model run-level means, ms):

```
SHAP     logreg 935.6   rf 2819.8   xgb 20.7    svm 54230.5  mlp 534.7
LIME     logreg 73.2    rf 435.9    xgb 122.3   svm 17620.4  mlp 51.6
Anchors  logreg 2917.7  rf 48954.8  xgb 57704.9 svm 37415.2  mlp 15563.9
DiCE     logreg 10746.4 rf 27314.2  xgb 24506.2 svm 66266.1  mlp 12633.8
SHAP fidelity  logreg .946 rf .729 xgb .759 svm .882 mlp .725
SHAP stability logreg .880 rf .949 xgb .575 svm .925 mlp .331
```

### Phase 2 — Thesis prose (one atomic commit per finding)

| ID | Finding | Sev | Task | Files | Est. |
|:--|:--|:--|:--|:--|:--|
| T2.1 | **F01** | major | Apply D1. Delete "no dependiente de la configuración del kernel"; replace with the `num_samples`-vs-`kernel_width` distinction. Scope §sec-sintesis ("cualquier sistema" → scoped). Add the qualifier to Ch.5's opening. | `capitulo-6-conclusiones.qmd`, `capitulo-5-taxonomia.qmd` | 1.5h |
| T2.2 | **F02** | major | Rewrite the four cost ranges from T1.1 values, stating the aggregation. **Rewrite the DiCE recommendation itself** — 28,209 ms is second-worst, so "costes moderados… aceptables" must go. | `capitulo-4-resultados.qmd` (Contextos A–D), `capitulo-6-conclusiones.qmd` | 1h |
| T2.3 | **F03** | major | Apply D2. Reconcile or disclose the two appendix reference cells; stop calling both "la referencia". | `apendices.qmd` | 0.5h |
| T2.4 | F04 | minor | Make thresholds conditional on model family using T1.2 values | `capitulo-4-resultados.qmd`, `capitulo-6-conclusiones.qmd` | 0.5h |
| T2.5 | F05 | minor | Scope the CV<3% headline (3 sites); mirror the §sec-p1 "Nota de alcance" pattern | Ch.4, Ch.6 (OE4 + Fronteras) | 0.25h |
| T2.6 | F06 | minor | Define the Brechas in Ch.5 (material exists in Ch.2 §"brechas de constructo") **or** drop the numbering | `capitulo-5-taxonomia.qmd` | 0.75h |
| T2.7 | F07 | minor | Fronteras LIME row: add the dataset/feature-space boundary; replace the already-completed future-work cell | `capitulo-6-conclusiones.qmd` | 0.25h |
| T2.8 | F08, F09 | minor | Split the Anchors-$\tau$ table scope; fix "sobre los bloques" → "sobre las 57 ejecuciones calificadas" | `apendices.qmd`, `capitulo-4-resultados.qmd` | 0.5h |

### Phase 3 — Cross-document propagation (RCA-001 invariant 3)

| ID | Task | Files | Est. |
|:--|:--|:--|:--|
| T3.1 | Paper B+C: reconcile l.~1297 ("Both probes indicate the instability is structural") with l.~1041 and Supplementary S2 — add the kw=10.0 clause the supplementary already carries | `paper_bc_jmlr.tex` | 0.5h |
| T3.2 | Update the sync matrix with the F01 resolution and the newly registered per-model cost rows | `docs/reports/sync/thesis_paper_sync_matrix.md` | 0.5h |

### Phase 4 — Suggestions (only if time allows, pre-defense)

T4.1 F10 (derive or drop $\chi^2\approx15.2$) · T4.2 F11 (Anchors MNAR direction — the
$\tau=0.90$ row gives an empirical handle) · T4.3 F12 (per D3).

### Phase 5 — Task 3 / RCA-001 Phase 2 input

| ID | Task | Est. |
|:--|:--|:--|
| T5.1 | **F13** — add an *unregistered numeric literal* check to `verify_claims.py`: scan guarded manuscript bodies, report literals with no registry entry and no explicit unbacked annotation. Turns "absence of registration" from silent into visible. | 3h |
| T5.2 | Registration-completeness sweep over Ch.4–6 + appendices, before Phase 2 macro generation | 2h |

---

## 4. Execute — protocol

- **Guards**: every target file is guarded (Ch.3–6 + `apendices.qmd` by RCA-001; Ch.5 and the
  supplementary also by RCA-002). Read both RCAs before the first edit.
- **Commits**: atomic, one per finding, message `fix(thesis): F0X — <one line>`. No batching.
- **Rule**: numbers enter the manuscript from the registry, never typed from this plan.
- **No statistic changes.** If any edit would move a confirmatory value, stop — that is a
  different task and needs its own RCA.

## 5. Verify — acceptance criteria

- [ ] `python scripts/pubs/verify_claims.py` green, with claim count risen from 61 to ≥ 91
- [ ] `python scripts/pubs/verify_sync.py` green
- [ ] `python scripts/pubs/verify_exp4_reconstruction.py` green (Python 3.13)
- [ ] All four outputs rebuilt clean: 3 PDFs via `tools/tectonic-portable`, thesis DOCX via
      `thesis/render.ps1` — no undefined refs, no crossref warnings
- [ ] Full-text search finds zero occurrences of `770`, `3–9 ms`, `1–322`, `10,000–70,000`
- [ ] Crossref integrity re-check: all labels resolve, zero dangling (currently 69 / 0)
- [ ] `grep -c "Brecha 3"` either resolves to a definition or returns 0
- [ ] Re-run `scientific-rigor-review` on the thesis; target **≥ 4.3**, D1 and D3 ≥ 4
- [ ] `ACTIVE_CONTEXT.md` updated

## 6. Risks

| Risk | L | I | Mitigation |
|:--|:--|:--|:--|
| F01 rewrite weakens the perceived contribution | M | M | Option A *adds* a finding (feature-space dependence) rather than retracting one; EXP3 becomes a second result, not a caveat |
| Re-running the S5 probe produces values matching neither appendix table | M | M | Timebox to 1h, fall back to D2(b) disclosure |
| Editing guarded files regresses a registered claim | L | H | Registry-first ordering + `verify_claims.py` before every commit |
| Toolchain: MiKTeX `pdflatex` cannot build Paper A (microtype/bibliography) | H | L | Known — use Tectonic. `render.ps1` prints a harmless `quarto clean` error |
| Thesis DOCX regenerated but the reviewed source drifts again | M | M | Rebuild all four outputs as the final step, not per-commit |

## 7. Effort

| Phase | Est. |
|:--|:--|
| 1 — Registry | 2.75h |
| 2 — Thesis prose (incl. T2.9) | 5.35h |
| 3 — Cross-document | 1h |
| 4 — Suggestions (optional, F10/F11) | 1.25h |
| 5 — Task 3 input (separable) | 5h |
| **Pre-defense critical path (1–3)** | **~9h / ~1.5 days** |

## 8. Recommended sequencing

1. **Now**: author answers D1, D2, D3 (10 minutes; D1 is the only true blocker).
2. **Session 1** — Phase 1 (registry) + T2.2, T2.4 (the numbers those tasks need are then live).
3. **Session 2** — T2.1, T2.6, T2.7 (the F01 scope cluster, one coherent editing pass).
4. **Session 3** — T2.3, T2.5, T2.8 + Phase 3, then Phase 4 if time.
5. **Session 4** — Phase 5 folded into Task 3 (RCA-001 Phase 2), separately from the defense path.

Phases 1–3 close every major and minor finding. Phase 5 is what stops the class from recurring.

---

## Approval

| Role | Name | Date | Status |
| ---- | ---- | ---- | ------ |
| Architect | Claude | 2026-08-28 | **Approved — D1/D2/D3 resolved, ready to execute** |

_Implementation Plan — ACE-Framework v2.5.0_
