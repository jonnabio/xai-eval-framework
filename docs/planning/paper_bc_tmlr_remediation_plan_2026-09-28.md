# Paper B+C remediation plan (TMLR pre-submission review)

**Date:** 2026-09-28
**Role:** Architect (plan). Execution is by the Scientific Editor / Developer in a separate session;
verification by QA.
**Lane:** `paper/bc-venue-definition` (worktree `../xai-paper-bc`)
**Input:** `docs/review/scientific-rigor-review_paper_bc_tmlr_2026-09-28.md` (F01-F15), plus the
reference items it hands to Phase 2.
**Parent plan:** `docs/planning/paper_bc_tmlr_review_plan_2026-09-28.md` (this document is Phase 4).

## Principles

1. **Register first, edit second.** Every new or changed number goes into `pub/claim_registry.toml`
   before it reaches the manuscript (RCA-001 invariant 1). Every number that cannot be re-derived
   is entered as `[[unbacked]]` with its reason.
2. **One commit per finding or cluster**, each with `verify_claims.py` and `verify_sync.py` green,
   pushed immediately.
3. **Abstract edits go through `pub/claims.toml`**, never the fragment (RCA-003). Macros are written
   with doubled backslashes. After each abstract edit, read page 1 of the built PDF.
4. **Rescoped claims trigger the top-level statement sweep** and a check of the thesis sync matrix
   (`docs/reports/sync/thesis_paper_sync_matrix.md`). A thesis passage carrying the same claim is
   fixed on the thesis lane, not here.
5. **No experiment is re-run.** All fixes are prose, figures or the registry.

## Author decisions (2026-09-28)

Q1, Q2 and Q4: the defaults below are adopted. Q3: **overridden** - no disclosure and no
mention of the EXP4 prompt question; F10 is closed as won't-fix by author decision and no
manuscript text is added or changed for it.

Each question below has a recommended default. If the author doesn't answer, execution goes ahead
on the default, and the default is recorded in the commit message.

| # | Question | Default |
|---|---|---|
| Q1 | EXP3 figure stacks Anchors + gap to reach SHAP levels Paper A prints. Keep? | **Redraw as gaps only** (same generator, one panel). It removes the question from the TMLR reuse policy at no cost to the argument. |
| Q2 | Does the original search/screening log exist? | **Assume no.** The caption says the counts come from the original record, which is not released, and the chain is registered `[[unbacked]]`. If the log is found later, release it and register the counts. |
| Q3 | Did the original EXP4 prompt hard-code "UCI Adult Income"? | ~~Disclose~~ **Author decision: no disclosure, nothing added (F10 won't-fix).** |
| Q4 | Tier 1 wording for tree models | **XGBoost only, with "measure first" for other tree ensembles**. RF was slower in 15/15 cells, and LightGBM was not tested. |

## Step 0 - Finish the review (Phases 2 and 3 of the parent plan)

Run these first, so the fixes are done in a single pass and not in rounds.

- **0.1 Reference audit** (`reference-audit` skill), producing
  `docs/review/reference-audit_paper_bc_tmlr_2026-09-28.md`. It starts from the items already found:
  - 8 entries are never cited;
  - `nauta2023anecdotal` has mojibake in its label;
  - three entries have questionable year/volume data: `fok2023verifiability`, `zhou2025medthink`
    and `wachter2017counterfactual`.
- **0.2 Coverage report** for `paper_bc_tmlr.tex` and the supplementary
  (`verify_claims.py --coverage-report`). Each unregistered literal is classified as registered,
  structural, `[[unbacked]]` or a finding. Unregistered literals that no step below touches become
  the work of Step 7.

**Exit:** both reports committed. Any new findings are appended to this plan as F16+.

## Step 1 - Registry groundwork (one commit: `pubs(paper-bc): register remediation values`)

Everything later steps will print or remove is entered here:

| Entry | Source | For |
|---|---|---|
| Per-model median cost, SHAP and LIME, for xgb and rf (18.1/61.8, 1,262.4/335.6), and the SHAP-faster cell counts (15/15, 0/15) | `paired_cells_shap_lime_all_models.csv` (new resolver `exp2_paired_median:<model>:<method>:cost` if none exists) | F01 |
| Add the Paper A site to `exp2.run.shap.cost.mean` and the LIME mean claim | Paper A l.436-437 | F02 |
| Paired differences with 95% CI, if not already registered at figure precision | `wilcoxon_shap_lime_all_models.csv` | F02 figure |
| `exp3.lime.stability.range` = 0.75-0.93 | `exp3_lime_results.csv` | F07 |
| LIME stability seed SD per stratum (median) | EXP2 run-level CSV | F08 |
| PRISMA chain 312/65/247/152/95/47/48/4/44, as `[[unbacked]]` (Q2 default) | `REVIEW_CORPUS.md:50-52` | F04 |
| Table S5 values 0.452/0.011, 0.461/0.014, 0.459/0.016, as `[[unbacked]]` | RCA-002 reason, as in the thesis | F05 |
| Actionability floor share, 86% | `experiments/exp4_cohort2/` analysis output | F14 |
| Retired: `11,708.3` and `3,660.7` in `paper_bc_tmlr.tex` | reason: shared with published Paper A | F02 |
| Retired: `0.85--0.93` in `paper_bc_tmlr.tex` | reason: excludes GC/XGB 0.748 | F07 |

Negative test: re-insert "11,708.3" locally, and confirm `verify_claims.py` fails.

## Step 2 - Headline claims (F01, F03, F09): abstract, Tier 1, conclusion

These three share the abstract, so they are done together, then checked against page 1 of the PDF.

- **F01 - tree-model latency**
  - `pub/claims.toml`: replace "for tree-based models, SHAP's TreeExplainer reverses this ordering"
    with the XGBoost-specific statement. Also replace "SHAP is preferred at both fidelity and latency
    for tree-based models" with "for XGBoost; for other tree ensembles, measure latency first
    (Random Forest was SHAP-slower in all 15 cells)".
  - `tab:hybrid_deployment`, Tier 1: remove LightGBM and RF from the list, restate the $O(TLD)$
    argument as the reason XGBoost's shallow trees are cheap, and add the RF counter-case.
  - l.1199-1205, `tab:generalizability_boundary` l.1347, and the conclusion's deployment sentence:
    same scoping.
- **F03 - LIME instability**, one scoped statement used at every site:
  - the abstract;
  - contribution 4;
  - l.1086-1091 ("primary driver" → "a candidate driver");
  - l.1374-1378;
  - the S5 closing paragraph;
  - l.993-998 (with F08).

  Proposed wording: "Under the reference kernel width, LIME's stability on Adult is near zero; it
  rises with kernel width and is high on two lower-dimensional datasets, so it is modulated by
  configuration and feature space; the one-hot encoding is a candidate cause this design does not
  isolate."
- **F09**: "SHAP dominates all measured quality endpoints" → "SHAP leads on every fidelity- and
  stability-oriented endpoint, while LIME is sparser".
- **Then:**
  1. Regenerate the fragments, rebuild the PDF and read page 1.
  2. Run the top-level statement sweep, covering contribution 2/4, the conclusion and the Broader
     Impact Statement.
  3. Check the sync matrix row for the LIME claim, and open a thesis-lane item if the thesis still
     says "structural".

**Commits:**
- `paper-bc: scope the tree-model latency claim to XGBoost (F01)`
- `paper-bc: one scoped statement of LIME instability (F03, F08, F09)`

## Step 3 - Prior-publication overlap (F02, Q1)

1. Delete the means sentence at l.1022-1023. Keep the medians and percentiles, which are not in
   Paper A.
2. `scripts/generate_paper_b_figures.py`:
   - point the output at `docs/reports/paper_bc/figures/` (F12);
   - rewrite `generate_quality_figure` to plot the paired mean difference with its 95% CI per endpoint
     (from `wilcoxon_shap_lime_all_models.csv`), with the sparsity direction noted.
   - Regenerate Figure 1 and update its caption. The caption no longer says "paired mean comparison
     across ... Active ratio is reported directly".
3. Q1 default: `scripts/generate_exp3_gap_figure.py` plots the gap only, and the caption drops
   "so each bar reaches the SHAP level".
4. Re-read the provenance paragraph (l.1218-1232) and the caption of `tab:paired_main`. They must now
   be true as written. The caption of `tab:exp3_lime` (LIME Adult per-model levels 0.457/0.553) is
   not in Paper A. Keep it, but change the provenance wording from "per-method levels" to "the
   per-method levels Paper A reports".
5. **Harden the gate:** add a step to the "After any revision" checklist in
   `OPENREVIEW_SUBMISSION.md`. It is a registry-independent literal scan of Paper B+C (main,
   supplementary, abstract) against Paper A at printed precision, which lists matches for triage.
   Implement it as `scripts/pubs/scan_shared_literals.py` and add it to `pubs-sync.yml` as a
   report-only step. Record the defect class in RCA-001: the check depended on complete `appears_in`
   registration.
6. Update `EIC_ENQUIRY_prior_publication.md` if it quotes the "no shared result" claim, so the
   editor note stays true.

**Commits:**
- `paper-bc: remove restated Paper A means; plot paired differences (F02)`
- `pubs: registry-independent shared-literal scan against Paper A (F02, RCA-001)`

## Step 4 - Evidence and disclosure (F04, F05, F06)

- **F04**, `tab:prisma`:
  - restore 47 at the full-text exclusion row;
  - add the rows "Included in original coding pass: 48", "Not recoverable (coded, not cited): 4" and
    "Released coded corpus: 44";
  - caption: the counts come from the original screening record, which is not released (Q2 default);
  - abstract and contribution 2: "documented five-database search and transparent screening
    record" → "five-database search with a reported screening record".

  Update `[review_corpus.paper_bc]` only if a printed figure changes; the size stays 44.
- **F05**, Table S5: port the thesis Apéndice C disclosure. It is a historical exploratory probe
  that cannot be re-derived, and its reference cell disagrees with Table S2 (0.461/0.014 against
  0.518/0.000). State why the directional conclusion survives. In the main text, l.1356: "rule out"
  → "find no evidence of". Use the thesis wording as the source of truth, for sync.
- **F06**, l.1306-1320: rewrite as a plausible, untested mechanism. Delete "optimally" and "causal
  responsibility", and drop "consistently" (Breast Cancer gap +0.07). Make the axiom lists at l.236
  and l.1307 agree, and cite the property set from `lundberg2017unified`.
- **F10**: won't-fix by author decision (2026-09-28). No edit.

**Commits:** one per finding.

## Step 5 - Minor corrections (F07, F08, F11, F12)

- **F07**: "0.85--0.93" → "0.75--0.93" at l.1085 and l.1372.
- **F08**: `tab:cv_reproducibility` — replace LIME stability's CV with its seed SD, or add an SD
  column, and state that CV is uninformative near a zero mean. Remove "structurally irreproducible" and
  "geometrically unstable" (with F03).
- **F11**, l.1432: "default hyperparameter settings" → "fixed reference settings".
- **F12**:
  - delete the to-do at l.1417-1419;
  - rewrite l.1462-1466 so each `\ifdeanon` branch is a whole clause, and check both builds;
  - l.1415-1416 names both figure generators;
  - the generator path is fixed in Step 3.

**Commit:** `paper-bc: minor corrections (F07, F08, F11, F12)`

## Step 6 - Suggestions and references (F13-F15, reference audit)

- **F13**: "the first" → "among the first".
- **F14**: "almost every score is 1" → "86% of scores are 1".
- **F15**: S6 "decreases monotonically" → "does not increase"; S1 caption typo.
- **Reference audit fixes**, per Step 0.1:
  - remove the 8 uncited entries, or cite them where they genuinely support a claim (default:
    remove);
  - fix the `nauta2023anecdotal` label;
  - correct the year and volume data.

  `thebibliography` is hand-written, so re-check each `\bibitem[...]` label against its entry.

**Commits:** `paper-bc: wording suggestions (F13-F15)` and `paper-bc: bibliography fixes (reference audit)`

## Step 7 - Put Paper B+C under coverage

Clear the remaining Step 0.2 triage list, then add `paper_bc_tmlr.tex` and
`paper_bc_tmlr_supplementary.tex` to `[coverage]`. This is a trunk event, so merge it through `main`
and into both other lanes in the same session, with CI green on each.

**Commit:** `pubs(paper-bc): enforce coverage on the TMLR manuscript and supplementary`

## Step 8 - Verification (QA, fresh session)

1. Rebuild both PDFs with Tectonic: 0 undefined references or citations, no unrepresentable
   characters. Check the page count against TMLR's guidance.
2. Read, in the rendered PDF: page 1 (the abstract), Table 1 (the screening record), Figure 1,
   Tier 1, the EXP3 figure, and the artifact paragraph in the anonymous build.
3. Build the de-anonymised variant once, to check the `\ifdeanon` sentence (F12). Discard it
   afterwards.
4. Run the whole "After any revision" checklist in `OPENREVIEW_SUBMISSION.md`, including the new
   shared-literal scan. Regenerate the sheet's abstract, word count and stamp.
5. Re-run this review's findings as a checklist: each of F01-F15 is marked fixed, with its commit.
   Append the result to the review report as a post-fix status.
6. Merge the paper lane to `main`. Merge `main` into the thesis and chapter lanes, and confirm the
   chapter's `[exclusivity]` check still passes with any new Paper B+C sites.
7. Hand the author a written report. Filing waits for it.

## Cross-lane follow-ups (not in this lane)

- **Thesis**: if the sync matrix shows Ch.4/Ch.5/Ch.6 still use "structural" LIME instability, the
  Paper A cost means or the tree-latency generalisation, open a thesis-lane item. The thesis may
  keep the Paper A means, because they are its own results.
- **CIFIE chapter**: no Paper B+C results may be printed there (ADR-0018). Nothing here adds any.

## Estimate

| Step | Effort |
|---|---|
| 0 Review Phases 2-3 | ~2 h |
| 1 Registry | ~1 h |
| 2 Headline claims | ~1.5 h |
| 3 Overlap and figures | ~1.5 h |
| 4 Evidence and disclosure | ~1.5 h |
| 5-6 Minor, suggestions, references | ~1 h |
| 7 Coverage | ~0.5-1 h |
| 8 Verification | ~1.5 h |
| **Total** | **~10-11 h** (two sessions) |

Critical path for filing: Steps 1-3 and 8. Steps 4-7 are strongly recommended. F04 and F05 are
the likeliest reviewer objections after F01 and F02.

## Step 0 outcome (2026-09-28, `b2ee05ce7`)

Reports: `docs/review/reference-audit_paper_bc_tmlr_2026-09-28.md` (R01-R10) and
`docs/review/coverage-triage_paper_bc_tmlr_2026-09-28.md` (73 literals classified).
Additions to the steps above:

- **Step 1** also registers the 44 re-deriving literals in the triage table, declares its 22
  structural literals, and adds `[[unbacked]]` entries for the four S5 values. A new resolver is
  needed for the paired t-CIs (mean ± t(74)·SE over `paired_cells_shap_lime_all_models.csv`), and
  a composing resolver for the EXP3 SHAP−LIME gaps.
- **F16 [minor], EXP6 sample misstated** (Step 5): "the $n=50$ RF runs across five seeds" → "the
  five RF runs at $N=50$, one per seed". State that 5/5 sign agreement is descriptive, since with
  $n=5$ the exact Wilcoxon minimum is $p=0.0625$. Fix both main l.1396 and the S6 caption/intro.
- **F17 [minor], cost ratio** (Step 5): l.1020-1022 → "the median per-cell SHAP/LIME ratio is 5.3×"
  (the ratio of the medians is 10.4). Drop "corresponding to".
- **Step 6 reference fixes**, per R01-R10:
  - remove the 8 unused entries;
  - R02 fix the label;
  - R03 year 2024;
  - R04 add volume, issue, pages and DOI;
  - R05 cite ACL 2026;
  - R06 NeurIPS DOI and pages;
  - R07-R09 check and keep the entry unless a published version is found.
- The rigor review's suspicion about `zhou2025medthink` is withdrawn: Crossref confirms 2025.

- **F16 and F17 FIXED 2026-09-28** (ahead of Step 1, at the author's request). No number was added
  or changed: F17 is a wording fix, and F16 adds only the structural $\alpha = 0.05$. Verifiers
  green; both PDFs rebuilt with 0 undefined references. The 2026-09-27 gate record in
  `OPENREVIEW_SUBMISSION.md` is now invalid, as expected until Step 8.

## Step 1 outcome (2026-09-28)

Registry: 257 → 319 claims, 429 → 481 sites; 5 `[[unbacked]]` entries (4 for Table S5, 1 for
the PRISMA chain); 23 structural literals; the Paper A sites were added to the SHAP and LIME cost
means. The Paper B+C coverage gap fell from 73 literals to 2, and both are the F07 range
(`0.85`, `0.93`), which Step 5 fixes. Negative-tested: editing one registered CI in the
manuscript fails the verifier.

New resolvers in `scripts/pubs/claim_sources.py`:
- `exp2_paired` (mean or median of a paired-cell column over a model group);
- `exp2_paired_faster`;
- `exp2_paired_quantile`;
- `exp2_paired_ratio_median`;
- `exp2_paired_ci` (t, df = 74);
- `exp2_stratum_median` (SD or CV over (model, N) strata);
- `review_audit`;
- `exp4c2_score_pct`.

**Deviation from the plan:** the retired entries (`11,708.3`, `3,660.7`, `0.85--0.93`) are
**not** added in Step 1. A retired text fails the verifier while it is still in the manuscript,
so each goes in the commit that removes it: F02 in Step 3, F07 in Step 5. The negative test for
`11,708.3` moves to Step 3.

**New findings from registration**, both minor, both fixed in Step 5:
- **F18, CV table aggregation mislabelled.** The caption and text of `tab:cv_reproducibility`
  say "stratum-median CV across (N, model) strata". All four printed values (0.8 / 0.7 / 2.6 /
  86.2%) are the single RF/N=100 stratum (`p1.*.cv`). The actual stratum medians are
  0.9 / 1.4 / 2.3 / 88.2 (registered as `exp2.stratum_median.*.cv`). No conclusion changes.
  Fix: either relabel the table as the RF/N=100 stratum, or print the medians; the default is
  to relabel, which matches the thesis P1 cell. Combine with F08, whose SD is registered for
  both readings (`exp2.subset.lime.stability.sd.rf100` 0.0151 and
  `exp2.stratum_median.lime.stability.sd` 0.0150).
- **F19, German Credit SHAP-LIME gap ranges wrong.** l.1080 prints "+0.23--+0.24 for RF,
  +0.24--+0.25 for XGB". The per-seed gaps are 0.212-0.244 (RF) and 0.220-0.270 (XGB); the means
  are 0.231 and 0.243. Fix: print the means, "+0.23 (RF) and +0.24 (XGB)", as the Breast Cancer
  gaps are printed. Then drop "0.25".

**Note on F05:** Table S5's reference row (0.461 / 0.014) equals two EXP2 aggregates (RF/N=100
five-seed LIME fidelity, and block-level LIME stability). It does not equal the seed-42 cell of
Table S2. Say so in the S5 disclosure.

## Step 2 outcome (2026-09-28)

**F01, F03 and F09 fixed**, at these sites:
- the abstract (`pub/claims.toml`, fragment regenerated);
- the Tier 1 row and the paragraph after `tab:hybrid_deployment`;
- the "LIME lower runtime" row of `tab:generalizability_boundary`;
- the reproducibility-probe paragraph (the "structurally" / "geometrically" wording is removed;
  the CV/SD rework is still Step 5);
- the EXP3 LIME paragraph ("primary driver" → a candidate driver the design does not isolate);
- the closing of "LIME stability is not a convergence artifact";
- the Table S5 and S2 closing sentences.

Tier 1 now names XGBoost and the RF counter-case with registered medians: 18.1/61.8 ms and
1,262.4/335.6 ms (sites added). No number is new or changed.

Checks:
- verifiers green (319 claims / 485 sites);
- both PDFs rebuilt, 26 + 5 pp, 0 undefined references;
- **page 1 read from the built PDF**: the new abstract renders with no garbled macros;
- the Tier 1 recommendation column is now ragged-right;
- the remaining 2 pt overfull box at the end of `tab:hybrid_deployment` was already present
  before this step;
- the fragments that `generate_fragments.py` rewrote with only line-ending changes were
  restored, so only `paper_bc_abstract_en.tex` and `build_meta.env` changed.

**Top-level statement sweep.** Contribution 2 and contribution 4 carry neither claim. The
conclusion ("LIME remains the pragmatic option when latency and compactness are the primary
constraints"; "lower runtime for most model contexts") and the Broader Impact Statement are
consistent with the new wording, so no edit was needed.

**Thesis-lane follow-up (open, not this lane):** the thesis carries both claims.
- Ch.4 l.193 says LIME's instability "no es marginal, sino estructural".
- Ch.6 `tbl` P1 row: "incoherencia estructural, no ruido del protocolo".
- Ch.4 l.620: "Para modelos basados en árboles, el coste de TreeSHAP hace esta elección también
  eficiente". Ch.6 l.134-136 already scopes this correctly to XGBoost.

These are the same defect class as thesis F01 (2026-08-28). Fix them on
`thesis/rca-001-phase-2` through the sync matrix.

## Step 3 outcome (2026-09-28)

**F02 fixed** (`85c65557a` and the following commit):
- The SHAP/LIME mean costs are removed from the text and cited to Paper A. Both texts are
  retired, and the retirement was negative-tested.
- Figure 1 now plots the mean paired difference with its 95% t interval.
- The EXP3 figure shows the gaps only (Q1).
- The generator writes to `paper_bc/figures/`.
- The provenance paragraph now says "in the text or in a figure".

`scripts/pubs/scan_shared_literals.py` compares the printed decimals of Paper B+C (main,
supplementary, abstract) with Paper A at printed precision, without the registry. 48 matches were
triaged as coincidences, each with its reason. It is negative-tested: a planted 0.808 and
11,708.3 are both caught, and 0.808 is not registered anywhere. It runs report-only in
`pubs-sync.yml`, is `--strict` in the submission checklist (step 6), and is listed under
RCA-001's tests in `regression-guards.yaml`. RCA-001 "Not covered" records the defect class.

The editor note (`EIC_ENQUIRY_prior_publication.md`) now says fifteen results were removed,
not thirteen, and mentions the figure and the mean runtimes, so it stays true.

The runtime figure (Figure 2) was regenerated to the corrected path. It plots distributions
and per-model medians; the scan and a visual check find nothing that Paper A prints.

## Step 4 outcome (2026-09-28)

**F04, F05 and F06 fixed**, in one commit because they share the same two files.

- **F04:** `tab:prisma` now shows the original chain: 47 excluded at full text and 48
  included in the original coding pass. Two further rows follow: 4 coded but not recoverable,
  and 44 released. The caption says the screening record is not released (Q2). The abstract
  now says "a five-database search with a reported screening record", where it said
  "documented … transparent". Contribution 2 says "released 44-paper corpus", and §Validity
  says the counts are reported but the record is not released. The corpus check is green.
- **F05:** Table S5 has a caption note and a provenance paragraph, ported from thesis
  Apéndice C. It is historical and cannot be re-derived; its reference row disagrees with S2
  (0.461/0.014 against 0.518/0.000); the conclusion it supports is directional only; and the
  surviving script sweeps a different grid. In the main text, "rule out" became "find no
  evidence", with a sentence on the probe's status. The S5 values are already `[[unbacked]]`
  (Step 1).
- **F06:** the axiom paragraph is rewritten as an untested, plausible mechanism, with the
  reasons it carries no guarantee: replacement masking rather than the background
  expectation, KernelSHAP being an estimate, the small Breast Cancer gap, and the properties
  holding for the model rather than the data. "Optimally aligned" and "causal responsibility"
  are removed. The property set is now local accuracy, missingness and consistency
  (`lundberg2017unified`), both here and at l.236, which listed efficiency, symmetry and dummy.

No number changed. Checks: verifiers green; shared-literal scan clean; both PDFs 0 undefined
references; page 1 and each edited passage read from the PDFs. The coverage gap is still only
the F07 range.

## Step 5 outcome (2026-09-28)

**F07, F08, F11, F12, F18 and F19 fixed** (F16 and F17 were fixed earlier).

- **F07:** "0.85--0.93" → "0.75--0.93" at both sites. The old text is retired, and both
  bounds are registered.
- **F08 + F18:** `tab:cv_reproducibility` is relabelled as the RF/N=100 stratum (the default
  decision). The text gives the medians over all 15 strata (0.9 / 1.4 / 2.3 / 88.2%) and the
  LIME stability seed SD (0.015), and states that the CV is not meaningful near a zero mean.
  The table's "No" became "CV not meaningful". All of these values are registered with sites.
- **F11:** "default hyperparameter settings" → "a single fixed reference configuration …
  not the library defaults".
- **F12:**
  - the internal to-do ("Before journal submission … DOI") is deleted;
  - the figure sentence names the generator of each figure;
  - the `\ifdeanon` availability sentence is restructured so each branch is a whole clause.
    The anonymous build is read and correct; the de-anonymised variant is checked in Step 8.
- **F19:** the German Credit gaps are printed as the means +0.23 (RF) and +0.24 (XGB),
  "positive for every seed". The old XGB range is retired.

**Coverage gap: 0.** Every numeric literal in the main text and supplementary is registered,
structural or unbacked, so Step 7 can add both files to `[coverage]` directly. The
shared-literal scan flagged four new low-precision matches (0.015, 0.9, 1.4, 2.3); each was
triaged against its Paper A context as a coincidence. Checks: verifiers green (320 claims /
490 sites / 35 retired guards); PDF 26 pp, 0 undefined references.

## Step 6 outcome (2026-09-28)

**F13, F14 and F15 fixed; bibliography R01-R06 fixed.**

- **F13:** "the first" → "one of the first".
- **F14:** "almost every score is 1" → "86% of its primary-condition scores are 1" (registered).
- **F15:** S1 caption "Three primary condition" → "Three conditions"; S6 "decreases
  monotonically" → "does not increase, and falls overall".
- **Bibliography:** 60 → 52 entries, all cited, no orphans.
  - R01: the 8 unused entries are removed.
  - R02: the Nauta label is fixed.
  - R03: Fok & Weld 2024, with DOI.
  - R04: Wilming 2022 now has 111(5):1903-1923 and its DOI.
  - R05: Wu et al. cites the ACL 2026 version (Crossref-verified authors).
  - R06: Zheng 2023 cites the NeurIPS DOI and pages.
  - R07-R09 (unverified entries) are kept unchanged; no published version was confirmed.
- **Registry:** removing `agrawal2025xaieval` removed a DOI containing "0.117". The site of
  `exp4c2.hidden.ci_upper.actionability` had pinned `count = 2` on that coincidence. It is
  now anchored on the table cell ("0.117]", count 1).

Checks: verifiers green (320 claims / 491 sites); shared-literal scan clean; both PDFs
0 undefined references (26 + 5 pp); each change read in the PDFs.

## Step 7 outcome (2026-09-28)

`paper_bc_tmlr.tex` and `paper_bc_tmlr_supplementary.tex` are added to `[coverage]`. The
verifier is green: 21 files are fully registered, up from 19. Negative-tested: a planted
unregistered literal (0.4321) fails with a `[coverage]` error. The change is merged to `main`
by fast-forward, then from `main` into the thesis and chapter lanes, with the verifiers run on
each lane after its merge.
