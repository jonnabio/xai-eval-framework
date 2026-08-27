# Thesis / Paper Synchronization Matrix

**Date:** 2026-08-22  
**Role:** Scientific Editor  
**Scope:** Thesis, Paper A, and merged Paper B+C

## Source-of-Truth Rule

The thesis is not assumed to be canonical for every item. For each claim, the
best-supported and most developed current version is canonical:

- **Paper A** is canonical for benchmark protocol, EXP2 artifact counts,
  EXP2 quantitative evidence, reproducibility/archive status, and benchmark caveats.
  **Exception (2026-08-22 audit):** Paper A is *not* canonical for EXP3 scope — its
  "Anchors check could not be executed" wording is factually wrong (see finding A01 in
  `docs/review/tri-document-alignment-review_2026-08-22.md`). Paper B+C is the accurate
  source for EXP3 coverage.
- **Paper B+C** is canonical for taxonomy, evidence-source distinctions,
  ranking-vs-validity framing, semantic-evaluation boundaries, and construct
  discipline.
- **Thesis** is canonical for doctoral synthesis, contribution hierarchy,
  chapter-level narrative, and defense framing.

## Claim Matrix

| Item | Best current source | Thesis status | Paper A status | Paper B+C status | Action |
|---|---|---|---|---|---|
| FOM-7 contribution | Thesis + Paper A | Present as doctoral protocol and governance contribution | Present as reproducible benchmark protocol | Present as empirical/taxonomy context | No edit needed |
| EXP1/EXP2 benchmark design | Paper A | Present | Most detailed source | Present through SHAP-LIME subset | Keep Paper A canonical |
| EXP2 artifact counts and archive status | Paper A | Present at synthesis level | Most detailed source | Scoped to 75 matched SHAP-LIME cells | Keep Paper A canonical |
| SHAP-LIME fidelity and stability claims | Paper A / Thesis | Present for Adult Income EXP2 | Present with quantitative benchmark framing | Present as ranking claim within protocol | No edit needed |
| EXP3 cross-dataset status | **Resolved 2026-08-23** — artifacts merged, all three aligned | Updated: SHAP-Anchors fidelity replication plus LIME extension; full paired SHAP-LIME stability outside Adult remains incomplete | **Incorrect (A01):** states the Anchors cross-dataset check was never executed and is blocked by the `alibi`/`dice-ml` gap. The 12 Anchors runs were completed 2026-04-26 and are on the unmerged `results/exp3-windows-breast-cancer` and `results/exp3-linux-german-credit` branches. The "LIME-only" mischaracterisation was corrected 2026-08-22 (A02 partial); the §sec:exp3 and Conclusion wording still awaits the A01 decision | Most complete source: SHAP-Anchors fidelity (verified against the side-branch artifacts), LIME extension, and missing SHAP-stability boundary | **Open:** merge the two `results/exp3-*` branches, then rewrite Paper A §sec:exp3 and its Conclusion limitation bullet |
| EXP3 SHAP fidelity, Breast Cancer / XGB | **Resolved 2026-08-23** — July snapshot canonical (0.6165) | Not reported at cell level | 0.6165 (committed July 2026 re-run) | 0.607 (April 2026 side-branch snapshot) | **Open:** choose one canonical EXP3 SHAP snapshot and re-derive both tables |
| EXP4 ICC vs Krippendorff sample sizes | Paper B+C | **Not propagated:** Ch.5 caption still says $n=147$ for both statistics (A08) | Out of scope | Discloses $n=147$ (ICC) / $n=192$ ($\alpha$) after the 2026-07-29 F02 fix | **Open:** port the Paper B+C disclosure into thesis Ch.5 |
| Archive DOI / evidence-cut snapshot | **Resolved 2026-08-23** — thesis repointed to 21538180 | Cites superseded `10.5281/zenodo.19297724` (April 2026) while reporting the current cut's numbers (A09) | Current: `10.5281/zenodo.21538180`, commit `553f65d71` | No DOI yet; snapshot to be frozen before submission | **Open:** align the thesis to the current cut or cut a new release |
| EXP4 semantic evaluator status | Paper B+C / Thesis | Present as low inter-judge reliability and future human calibration need | Out of confirmatory scope | Most detailed taxonomy/semantic boundary | No edit needed |
| Ranking claims vs validity claims | Paper B+C | Present conceptually | Present as benchmark-boundary text | Most explicit source | Paper A/B+C wording aligned |
| Synthetic ground-truth limitation | Paper B+C | Present via taxonomy/future validation boundary | Present as controlled ground-truth future need | Present as benchmark-grounded correctness family | No experiment claimed |
| Transparent-model recovery limitation | Paper B+C | Indirect through formal correctness boundary | Added to validation ladder | Added to validation ladder | Wording aligned |
| OOD / feature-dependence limitation | Thesis + Paper B+C | Present in masking/correlation caveat | Present through dependent-feature/suppressor framing | Present in metric transport and validity limits | No edit needed |
| Human-centered validation limitation | Paper B+C / Thesis | Present | Present as out of quantitative scope | Present as evidence-source and user-usefulness boundary | No edit needed |
| Review corpus size | **Resolved 2026-08-26** — 44-row reconstructed corpus released | Not stated at corpus level | Out of scope | 44 coded papers, distribution CI-verified against `paper_bc_review_corpus.csv` | Reconstruction disclosed in §Validity |
| Composite metric / weighting scheme | Thesis / Paper B+C | Present as multi-metric, no scalar collapse | Uses multi-metric benchmark, no composite | Taxonomy organizes constructs, not pooled ranking | No edit needed |

## Shared Boundary Text

Use manuscript-specific versions of this boundary:

> The work provides reproducible, functionally grounded, multi-metric
> comparative evidence under controlled benchmark conditions. It does not
> establish full explanation correctness, causal validity, universal method
> superiority, or human-centered usefulness. Stronger validity claims require
> synthetic or transparent-model ground-truth tests, dependency-aware
> perturbation protocols, broader replication, and human-centered validation.

## Verification Checklist

- [x] EXP3 wording no longer says LIME was never included after the LIME extension is described.
- [x] No manuscript claims synthetic ground-truth validation as completed work.
- [x] No manuscript claims transparent-model recovery as completed work.
- [x] No manuscript claims human-centered validation as completed work.
- [x] No manuscript introduces a normalized composite metric or weighting scheme.
- [x] Paper A and Paper B+C use compatible validity-boundary language.
- [x] No manuscript describes a completed experiment as never executed (A01, A02 — closed 2026-08-23).
- [x] The same experimental cell reports the same value in every manuscript (A03 — July snapshot canonical, 2026-08-23).
- [x] Thesis Ch.5 illustrative numbers match Ch.4/Appendix D (A04 — closed 2026-08-23).
- [x] Thesis Ch.4 per-method profile figures match `exp2_run_level_metrics.csv` (A05 — regenerated 2026-08-23).
- [x] Thesis archive DOI matches the reported evidence cut (A09 — 2026-08-23).
- [x] All rendered outputs (3 PDFs + thesis docx) rebuilt from current sources, 2026-08-22.
- [x] EXP4 ICC/Krippendorff sample sizes disclosed in both Paper B+C and thesis Ch.5 (A08).
- [x] EXP3 minimum-gap model label corrected to German Credit / XGB in both documents (A07).
- [x] Anchors coverage stated as 57/75 (76.0%) throughout the thesis (A06).
- [x] Paper B+C Friedman p-values labelled as Holm-adjusted (A10).
- [x] No dangling cross-references in the thesis (A13).
- [x] Manuscript numbers are machine-verified against artifacts (RCA-001, `scripts/pubs/verify_claims.py`).
- [x] Paper B+C corpus source PDFs collected and verified (44/44, 2026-08-26).
- [x] Paper B+C's review corpus has a committed coded CSV, CI-verified against the manuscript (A14, closed 2026-08-26).
