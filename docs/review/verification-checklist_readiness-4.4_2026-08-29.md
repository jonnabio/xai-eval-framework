# Verification Checklist — auditing the self-assessed 4.4/5

**Date**: 2026-08-29 | **Method**: `.ace/skills/scientific-rigor-review/SKILL.md`, applied in reverse
**Target**: `docs/review/readiness-status_thesis_2026-08-28.md` (Accept, mean 4.4)
**Auditor**: the author (independent of the agent that made the fixes)

## How to use this

Every item is a **falsification test**, not a confirmation. Each states the check, the
result that confirms, and — the important column — **what would break the score**. An item
that fails does not merely lose a point; the "impact" column says which dimension moves and
by how much, so you can recompute the grade yourself in §7.

Work top-down: §0 is ordered by probability-of-failure × cost-of-being-wrong. If §0 passes
clean, the remaining sections are confirmatory rather than exploratory.

Ordinary reading is not enough for most of these. The defects this remediation found were
invisible to four prior read-throughs and only appeared when numbers were re-derived from
artifacts. Run the commands.

---

## §0 — Highest-yield tests first (~40 min)

These are where I am most likely to be wrong, in order.

- [ ] **0.1 — The unswept files (highest expected yield).** Coverage enforcement reaches
  Ch.4 only. Add one file at a time to `[coverage]` in `pub/claim_registry.toml` and run:
  ```
  python scripts/pubs/verify_claims.py --coverage-report
  ```
  Do `capitulo-6-conclusiones.qmd` first (it carries the most prescriptive numbers), then
  Ch.3, Ch.5, `apendices.qmd`, then the three publication files.
  **Confirms**: literals are all registrable or genuinely structural.
  **Breaks the score**: any literal that is a *result* and matches no artifact — that is a
  live F02/F15-class defect. Base rate from the one swept file was **two defects**.
  → *Impact: D1 and D6 each −0.5 if a substantive one is found.*

- [ ] **0.2 — Did I miss more F01 sites?** I claimed F01 closed, then found six more sites
  on self-review. Search independently:
  ```
  grep -rn "estructural\|universal\|siempre\|en general" thesis/*.qmd | grep -i "lime\|estabilidad"
  ```
  **Confirms**: the only surviving "inestabilidad estructural" is
  `capitulo-6-conclusiones.qmd:292`, where the same sentence immediately qualifies it
  ("dependiente del espacio de características, no una propiedad universal").
  **Breaks the score**: any *other* unqualified use.
  → *Impact: D3 and D4 each −0.5.*

- [ ] **0.3 — Do the fixed numbers actually match the artifacts?** Don't trust the
  verifier's own registry; spot-check three by hand against
  `outputs/analysis/paper_a_exp2_stats/exp2_run_level_metrics.csv`:
  DiCE cost mean **28,208.8**; SHAP stability on XGBoost **0.575**; LIME cost on MLP
  **51.6 ms**.
  **Breaks the score**: any mismatch → the registry encodes a wrong value, which is worse
  than the original defect because CI now certifies it. → *Impact: D1 −1.0.*

- [ ] **0.4 — Is the F13 check real or decorative?** Insert a fabricated result number into
  Ch.4 (e.g. `4,321.9 ms`) and run `python scripts/pubs/verify_claims.py`.
  **Confirms**: exit 1, naming the literal and line.
  **Breaks the score**: exit 0 → the class-level fix does not work. → *Impact: D6 −1.0.*

- [ ] **0.5 — Rebuild everything yourself.** 3 PDFs via `tools/tectonic-portable`, DOCX via
  `thesis/render.ps1`. Grep the logs for `undefined`.
  **Note**: `render.ps1` prints a harmless `ERROR: Unknown command "clean"` — that is a
  known script bug, not a render failure. **Breaks the score**: any undefined reference or
  crossref warning (this is how A13 was originally found). → *Impact: D6 −0.5.*

---

## §1 — D1 Evidence Relevance (claimed 4.5, was 3.5)

- [ ] **1.1** `capitulo-6-conclusiones.qmd:234` — the LIME scope paragraph. Does it now
  state *both* directions (num_samples does not recover stability; kernel_width 10.0 does,
  at 0.664 with fidelity 0.518→0.441)? Cross-check against
  `outputs/analysis/lime_kernel_width_sensitivity.csv`.
- [ ] **1.2** `apendices.qmd:171` — the sentence that previously asserted the contradiction.
  Confirm it no longer says the instability is independent of the kernel parameter.
- [ ] **1.3** The four rewritten cost passages (`capitulo-4-resultados.qmd:599`;
  `capitulo-6-conclusiones.qmd:136, 142, 148, 160`). Each figure traceable to a per-model
  run mean.
- [ ] **1.4** **The DiCE recommendation, not just its number.** `:160` should now justify
  DiCE on the grounds that recourse has no substitute — *not* on cost. If it still reads as
  "affordable", the finding is only half-fixed. → *This is the one most likely to have been
  patched numerically without fixing the argument.*
- [ ] **1.5** Confirm no confirmatory statistic moved: H1 42.12, H2 40.68, H3 $d_z$ 4.820 /
  3.002, 75/75, P1, P2 ICC(1,1) 0.321–0.601. `git log -p --  thesis/ | grep -E "^\+.*(42\.12|40\.68|4\.820|3\.002)"` should show no *changed* values.

## §2 — D2 Falsifiability (claimed 4.5, unchanged)

- [ ] **2.1** `capitulo-3-diseno-experimental.qmd` — the stress test. Recompute:
  `30.44/2 = 15.22`; `P(χ²₃ > 15.22) = 0.0016`; noncentrality reading `λ=27.44 → 13.72`,
  `E[χ²]=16.72`, `p=0.0008`.
  **Breaks the score**: if the text still calls this a "50% power reduction" anywhere.
- [ ] **2.2** Every proposition still carries its pre-set threshold (CV<15%, ICC≥0.75,
  accuracy≥0.83, AUC≥0.88, τ=0.95) and none was adjusted to fit a result.
- [ ] **2.3** The new per-family SHAP thresholds (§F04) are stated so a reader can tell what
  would disconfirm them.

## §3 — D3 Scope Calibration (claimed 4.5, was 3.5)

- [ ] **3.1** `capitulo-5-taxonomia.qmd:7` — Ch.5's opening now scopes the instability.
- [ ] **3.2** `capitulo-6-conclusiones.qmd:387` — the final synthesis. Does the regulatory
  argument still land, or did scoping hollow it out? **Judgement call, and yours to make:**
  I claim the scoped version is *more* actionable. Disagree if it reads as hedging.
- [ ] **3.3** `capitulo-6-conclusiones.qmd:132–134` — per-family thresholds. Verify
  logreg 0.946 / SVM 0.882 clear 0.80; XGB 0.575 / MLP 0.331 fail 0.70.
- [ ] **3.4** The `@tbl-fronteras-generalizacion` LIME row now lists other feature spaces as
  unsupported, and its future-work cell no longer requests completed work.
- [ ] **3.5** §F12 — "prescriptivos" kept with the scope sentence. Confirm the opening
  sentence actually constrains the four bullets that follow.

## §4 — D4 Argument Coherence (claimed 4.5, was 3.5)

- [ ] **4.1** `capitulo-5-taxonomia.qmd:262` — read §sec-taxonomia-brechas cold. Do Gaps 1–3
  read as the thesis's own argument, or as text inserted to satisfy a reference?
  **Breaks the score**: if Gap 3 as defined is not what EXP4 actually tests.
- [ ] **4.2** Crossref integrity — 70 labels, 0 dangling:
  ```
  cd thesis && grep -oh '{#[a-z]*-[A-Za-z0-9_-]*' *.qmd | sed 's/{#//' | sort -u > /tmp/L.txt
  grep -oh '@\(tbl\|fig\|sec\|eq\)-[A-Za-z0-9_-]*' *.qmd | tr -d '@' | sed 's/[.,;:)-]$//' | sort -u | comm -23 - /tmp/L.txt
  ```
- [ ] **4.3** Ch.4 / Ch.5 / Ch.6 now agree on DiCE's cost (28,209 ms, second-worst).
- [ ] **4.4** Ch.6 §sec-limitaciones and §sec-futuro item 3 no longer contradict each other
  on kernel dependence.

## §5 — D5' Reporting Honesty (claimed 5.0, was 4.5)

**A 5 should be rare.** Test it adversarially — the question is not "is it honest?" but
"does anything remain undisclosed that a reader would want?"

- [ ] **5.1** `apendices.qmd` §C.1 provenance note — does it disclose the probe
  disagreement *and* that neither probe measures a full EXP2 run?
- [ ] **5.2** Is disclosing F03 rather than resolving it acceptable to you, or does the
  defense need the probe re-run? **Your call — I took the fallback.**
- [ ] **5.3** `capitulo-3-diseno-experimental.qmd` §F11 — the Anchors MNAR paragraph states
  the bias is *optimistic* (against the thesis's interest) and bounds it with τ=0.90.
- [ ] **5.4** **Is anything still undisclosed?** Candidates I did *not* address: the
  `total_CFs=1` / YAML-not-consumed caveats for DiCE and Anchors are noted in Appendix C but
  never revisited where those methods are ranked. Judge whether that needs surfacing.
- [ ] **5.5** F14's provenance error was self-reported. Confirm the correction at
  `capitulo-4-resultados.qmd:482` and `apendices.qmd:259` names the EXP2 table as the source
  and demotes the EXP1 report to a complementary profile.

## §6 — D6 Methodological Rigor (claimed 4.0, deliberately *not* raised)

- [ ] **6.1** Agree or disagree with holding D6 at 4.0. My reasoning: coverage spans one
  file of eight, and F03 is disclosed rather than resolved. **If §0.1 finds nothing in the
  other seven files, D6 arguably rises to 4.5 and the mean to 4.6.**
- [ ] **6.2** Aggregation labels: `capitulo-4-resultados.qmd` Anchors profile says "sobre
  las 57 ejecuciones calificadas" (not "bloques") and reconciles 0.052 vs 0.043.
- [ ] **6.3** `@tbl-appendix-anchors-sensitivity` — coverage column labelled design-wide
  (x/75), fidelity/cost labelled RF/seed 42.
- [ ] **6.4** Review the 9 new resolvers in `scripts/pubs/claim_sources.py` for correctness,
  especially `friedman_rank` (ranks 1=best; ties untested — the data has none, but the code
  would mis-handle them) and `exp2_subset_sd` (sample SD, not population — this choice is
  what makes the P1 table reproduce).
- [ ] **6.5** `[coverage].structural` list — every entry should be a genuine design constant.
  **Breaks the score**: a real result parked in `structural` to silence the check. This is
  the most abusable part of the mechanism I added, so audit it directly.
- [ ] **6.6** `[[unbacked]]` entries (2) — both genuinely unbackable, both disclosed in text.

---

## §7 — Recompute the grade yourself

| Dim | My score | Yours |
|:--|:--:|:--:|
| D1 Evidence Relevance | 4.5 | |
| D2 Falsifiability | 4.5 | |
| D3 Scope Calibration | 4.5 | |
| D4 Argument Coherence | 4.5 | |
| D5' Reporting Honesty | 5.0 | |
| D6 Methodological Rigor | 4.0 | |
| **Mean** | **4.5 → reported 4.4** | |

Grade mapping (unchanged from the skill):

| Grade | Condition |
|---|---|
| Strong Accept | mean ≥ 4.5 AND no dimension < 3 |
| Accept | mean ≥ 3.8 AND no dimension < 2 |
| Weak Accept | mean ≥ 3.0 AND no dimension < 2 |
| Weak Reject | mean ≥ 2.0 AND (mean < 3.0 OR any dimension < 2) |
| Reject | mean < 2.0 OR any dimension = 1 |

Note the arithmetic mean is **4.5**, which is the Strong Accept boundary. I reported 4.4
and did not claim Strong Accept, because coverage reaches one file of eight. If §0.1 comes
back clean across the other seven, that discount is no longer justified and the honest
grade is Strong Accept.

---

## §8 — Conflict of interest, stated plainly

I performed the review, wrote the fixes, and assigned the score. Three specific reasons to
discount it:

1. **A grader marking their own work.** The dimensions that moved most (D1, D3, D4) are
   precisely the ones my edits targeted.
2. **Demonstrated incompleteness.** My first pass at F01 and F15 missed seven sites,
   including one that reasserted the very contradiction F01 was about. Caught on self-review
   — but it was caught *after* I had reported those findings closed.
3. **The check I built defines its own escape hatches.** `structural` and `[[unbacked]]`
   are populated by me. §6.5 and §6.6 exist because of this.

**What would settle it**: a `scientific-rigor-review` run by a fresh session with no
knowledge of this remediation, against the current sources. That is a different and stronger
test than this checklist, which can only confirm that the stated fixes are present.

## §9 — Items this checklist cannot settle

- The 28 reconstructed Paper B+C corpus rows still want author verification (from A14).
- Whether the scoped LIME claim is *rhetorically* strong enough for the viva — §3.2 is a
  judgement only you can make.
- Whether F03's disclosure suffices, or the probe must be re-run before submission (§5.2).
EOF
