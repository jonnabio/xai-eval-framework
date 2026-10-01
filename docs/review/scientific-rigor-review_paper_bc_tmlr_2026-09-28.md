# Scientific Rigor Review: Paper B+C (TMLR submission)

**Date**: 2026-09-28 | **Reviewer role**: Scientific Advisor | **Grade**: Major revision (pre-submission)
**Mean score**: 3.4 | **Dimensions**: D1=3 D2=4.5 D3=3 D4=3 D5'=3.5 D6=3.5

**Scope reviewed**: all of `docs/reports/paper_bc/paper_bc_tmlr.tex` (2,036 lines, including the
bibliography); `paper_bc_tmlr_supplementary.tex` (Tables S1-S6); and the abstract and keywords
fragments `pub/fragments/paper_bc_{abstract,keywords}_en.tex`. The paper lane was at `a3258e80e`.
The plan is `docs/planning/paper_bc_tmlr_review_plan_2026-09-28.md` (Phase 1).

**Prior review**: `docs/reports/paper_bc/scientific-rigor-review_paper_bc_jmlr_2026-07-28.md`.
- F01 (Friedman block count): **confirmed fixed**. l.906-908 states $n=15$ blocks.
- F02 (ICC $n=147$ vs $\alpha$ $n=192$): **confirmed fixed**. l.581-586 and the caption of
  `tab:exp4_icc` give both.
- F03 (supplementary not re-derived): **partly fixed, reopened as F05**. S2, S3 and S6 are now
  registered. S5 is neither registered nor disclosed.
- F04 (EXP4 scripts missing): **resolved differently**. The sources were reconstructed and hash-pinned
  (RCA-002), and the replication's raw data is released. The loss of the original raw data is
  disclosed at l.598-599.

**Regression guards**: the main text is guarded by RCA-001 and RCA-002, and the supplementary by
RCA-002. The abstract fragment and `pub/claims.toml` are guarded by RCA-003. This review is read-only;
no guarded file was edited.
`verify_claims.py`: `OK: 257 claims re-derived from artifacts, 429 manuscript sites checked,
26 retired-value guards clear, 13 cited artifacts present, 19 file(s) fully registered, 15 file(s)
clear of unpublished results`. `verify_sync.py` and `verify_exp4_reconstruction.py` are also green.
Neither the main text nor the supplementary is under `[coverage]`, so the verifier does not see their
unregistered numbers. Several of the findings below are in that blind spot.

## One-line summary

The paired SHAP-LIME core is still sound and re-derives from the artifacts. The claims built around it
have moved past the evidence, in five places:
- The deployment pattern's headline, "for tree-based models SHAP's TreeExplainer reverses this
  ordering", is contradicted by the paper's own Random Forest cells.
- Two per-method results that Paper A has already published (the RIMI article) are printed again,
  one of them in a figure, and the shared-result query cannot see them.
- The abstract assigns LIME's instability to one-hot encoding, which the body treats only as a
  hypothesis.
- The screening table labels four lost papers as full-text exclusions.
- A robustness table (S5) is presented without the disclosure the thesis already carries for it.

Every fix is a prose, figure or registry change. None requires a new experiment.

## Strengths

- **The confirmatory core re-derives.** The paired table, the cost medians and percentiles, and the
  per-model cell counts all match `paired_cells_shap_lime_all_models.csv`. Examples: 59/75
  SHAP-slower cells; non-tree medians of 694.6 ms (SHAP) and 53.3 ms (LIME).
- **The EXP4 reporting is exemplary.** The primary estimate is fixed before the sensitivity views. The
  secondary views that cross 0.75 are named rather than hidden (l.608-616). The original and the
  replication are kept apart, and the panel-dependent ranking is stated (l.617-622). This is what
  ADR-0016/0017 require, and it reads as honest, not defensive.
- **Ranking claims are kept separate from validity claims** (l.1248-1256), there is a
  generalizability-boundary table (l.1337-1353), and the Broader Impact Statement is concrete rather
  than boilerplate.
- **The corpus reconstruction is disclosed** where the reader needs it (l.1268-1279), and the 44-row
  corpus is released and CI-verified.
- **The masking-sensitivity probe (EXP6, Table S6)** reports the endpoint where the attenuation claim
  fails, rather than dropping it.

## Findings

### F01 [major] - D1 Evidence relevance / D4 Coherence: "TreeExplainer reverses the latency ordering for tree models" is false for Random Forest

- **Location**: the abstract fragment ("for tree-based models, SHAP's `TreeExplainer` reverses this
  ordering"; "SHAP is preferred at both fidelity and latency for tree-based models"); Table
  `tab:hybrid_deployment` Tier 1 (l.1173-1178: "SHAP (TreeExplainer) for tree-based models (XGBoost,
  LightGBM, Random Forest) ... SHAP is simultaneously faster *and* more faithful"); l.1199-1205
  ("making SHAP the dominant choice at both tiers for tree-based deployments"); and
  `tab:generalizability_boundary` (l.1347: "tree-specific SHAP reverses the ranking").
- **Evidence**: re-derived from `outputs/analysis/paper_a_exp2_stats/paired_cells_shap_lime_all_models.csv`,
  matched cells, per-cell run means:

  | Model | Median SHAP (ms) | Median LIME (ms) | SHAP-faster cells |
  |---|---|---|---|
  | xgb | 18.1 | 61.8 | 15/15 |
  | rf | 1,262.4 | 335.6 | **0/15** |
  | tree models pooled | 294.2 | 301.8 | 15/30 |

  The paper's own body agrees with the data and not with the abstract. l.1032-1034 reads "SHAP is
  faster in all 15 XGBoost matched cells ... whereas LogReg, RF, and MLP are uniformly SHAP-slower."
- **Reasoning**: this is the single claim the deployment pattern (contribution 5) turns on. It
  generalises one tree family (XGBoost) to all of them, including one (RF) where the data shows the
  opposite. LightGBM was never tested. A TMLR reviewer who checks Figure 2 against Tier 1 will find the
  contradiction, and TMLR's first acceptance criterion is exactly this: claims supported by evidence.
- **Fix**: condition the recommendation on the measured family. Suggested wording: "for XGBoost,
  `TreeExplainer` was faster in all 15 cells; for Random Forest it was slower in all 15 (median 1,262
  vs. 336 ms), so the latency advantage depends on the ensemble, not on tree structure as such." In
  Tier 1, drop LightGBM and Random Forest from the list, or move RF to "measure first". Restate the
  $O(TLD)$ argument as the reason XGBoost's shallow trees are cheap, not as a guarantee. Register the
  per-model medians before editing (RCA-001 invariant 1). Changing the abstract triggers the
  top-level statement sweep and RCA-003's page-1 read.

### F02 [major] - D5' Reporting honesty / TMLR policy: results already published in Paper A are printed again, and the shared-result query cannot see them

- **Location**: l.1022-1023 ("Means are more separated (11,708.3 ms vs. 3,660.7 ms)"); Figure
  `fig:quality_endpoints` (`fig_b1_quality_endpoints.pdf`); the provenance statement (l.1220-1223:
  "reports no result that the earlier study reports: per-method fidelity and stability levels ... are
  cited to it rather than restated"); and the caption of `tab:paired_main` (l.940-943).
- **Evidence**:
  - Paper A (`docs/reports/paper_a/paper_a_prototype_jmlr.tex` l.436-437, l.447-453) prints the SHAP
    and LIME mean costs as 11708.26 and 3660.68 ms. Paper B+C prints the same two quantities at one
    decimal.
  - The registry entry `exp2.run.shap.cost.mean` lists `appears_in` = Paper B+C and thesis Ch.4 only;
    Paper A's site is not registered. So the shared-result query from `EIC_ENQUIRY_prior_publication.md`
    returned nothing on 2026-09-27, and "no result shared with Paper A" was recorded as verified.
  - `scripts/generate_paper_b_figures.py:46-60` draws Figure 1 as side-by-side bars of `lime_mean` and
    `shap_mean` for stability, fidelity, faithfulness gap and sparsity. Those are the per-method levels
    Paper A's Table (l.436-437) publishes and the provenance paragraph says are not restated. The bars
    carry no data labels, but the figure *is* the result.
  - I scanned every decimal literal in Paper B+C and its supplementary against Paper A at printed
    precision. Apart from these two means, all 28 matches are coincidences of low-precision numbers or
    identifiers.
- **Reasoning**: RCA-001's prior-publication invariant exists for this case. The check that enforces
  it is only as complete as the registry's `appears_in` lists, and one Paper A site was never
  registered. The overlap is small, but the manuscript asserts in writing that no overlap exists, and
  the editor note makes the same assertion. The EXP3 figure (`fig_exp3_gap.pdf`) raises a related
  question: it stacks the Anchors level and the gap, so each bar reaches the SHAP level Paper A prints
  (e.g. BC/RF 0.265 + 0.514 = 0.779 against Paper A's 0.7785). The caption says so ("so each bar
  reaches the SHAP level without restating it"). Whether a derivable level counts as reuse is a
  judgement for you and, possibly, the editor. It is listed under Questions.
- **Fix**:
  1. Delete the means sentence at l.1022-1023, or cite the means to Paper A. The medians and
     percentiles are not in Paper A and can stay.
  2. Redraw Figure 1 as the paired differences with their 95% CIs (the quantities of
     `tab:paired_main`), not as per-method bars.
  3. Add Paper A's site to `exp2.run.shap.cost.mean` and the LIME equivalent.
  4. Add a registry-independent step to the submission gate, such as the literal scan used here, so
     the query no longer depends on complete registration. Also change the generator to write into
     `docs/reports/paper_bc/figures/`; at present it writes to `docs/reports/paper_b/figures/` (see F12).

### F03 [major] - D3 Scope calibration / D4 Coherence: the abstract attributes LIME's instability to one-hot encoding, which the body calls a hypothesis and contradicts twice

- **Location**:
  - The abstract: "suggesting that LIME's instability on Adult stems from its high-dimensional one-hot
    encoding rather than from the method itself".
  - l.1088-1091: "The Adult dataset's 103-dimensional one-hot-encoded space appears to be the primary
    driver of instability".
  - Against them:
    - l.995-998: "LIME stability is structurally irreproducible ... geometrically unstable---not merely
      noisy".
    - l.1374-1376: "LIME's instability is a property of its local surrogate fitting under Gaussian
      perturbation".
    - Supplementary S5: "reflects the local surrogate fitting process itself".
    - l.1139-1141: "should be taken as a moderation hypothesis requiring further confirmation".
- **Evidence**: the paper's own results make the Adult instability depend on **configuration** as
  well as feature space. On Adult itself, widening the kernel to 10.0 raises stability from 0.000 to
  0.664 (Table S2). Breast Cancer and German Credit differ from Adult in dimensionality, the
  continuous/categorical mix, sample size and class balance, so two datasets cannot isolate encoding
  as the cause.
- **Reasoning**: this is the defect the thesis review found and fixed on 2026-08-28 (thesis F01,
  decision D1 = Option A: a narrow, configuration- and feature-space-scoped claim). The Paper B+C body
  partly adopted that fix (l.1367-1378). The abstract was rewritten on 2026-09-27 and now overshoots
  in the opposite direction, while l.995-998 and S5 keep the "structural" reading the thesis retracted.
  The same paper now says both "it is the method" and "it is not the method".
- **Fix**: one scoped statement, used everywhere. For example: "under the reference kernel width,
  LIME's stability on Adult is near zero; it rises with kernel width and is high on two
  lower-dimensional datasets, so it is modulated by configuration and feature space; the one-hot
  encoding is a candidate cause this design does not isolate." Also:
  - Remove "structurally irreproducible" and "geometrically unstable" (see F08).
  - Change "primary driver" to "a candidate driver".
  - Align the concluding sentence of S5.
  - Run the top-level statement sweep, since the abstract and contribution 4 restate this finding,
    and check the thesis sync matrix row for it.

### F04 [major] - D5' Reporting honesty: the screening record labels four lost papers as full-text exclusions, and cites a search log that is not released

- **Location**: `tab:prisma` (l.437-455) and its caption ("Identification and screening counts are from
  the original search log. The final two rows reflect the coded corpus released with this paper");
  contribution 2 (l.146-147); the abstract ("assembled through a documented five-database search and
  transparent screening record"); l.1281-1283.
- **Evidence**:
  - The original chain, recorded in `docs/reports/paper_bc/REVIEW_CORPUS.md:50-52`, was 312 → 65 →
    247 → 152 → 95 → **47 excluded → 48 included**. The table now prints **51** excluded at full text,
    under the stated reason "intrinsic only, no codeable metric", and 44 included.
  - 51 = 95 − 44. The four extra papers were included and coded, then lost (l.1274-1276). They were
    not excluded for that reason.
  - No search log or screening record is tracked in the repository (`git ls-files` finds none), so the
    312/65/247/152/95 counts are unbacked. They are not in the registry either.
- **Reasoning**: a screening table is read as a record of decisions. One row now records a decision
  that was never taken, and the table cites a log a reader cannot obtain. The provenance paragraph
  discloses the reconstruction in §Validity, but the table itself contradicts that paragraph.
  "Documented" and "transparent" in the abstract promise a record the artifact bundle does not
  contain.
- **Fix**:
  - Restore 47 at the full-text exclusion row.
  - Add rows "Included in the original coding pass: 48" and "Not recoverable (coded, not cited): 4 →
    released corpus: 44".
  - Either release the search log, or say in the caption that the identification and screening counts
    come from the original record, which is not released.
  - Soften "documented ... transparent" in the abstract to match.
  - Register the chain, or mark it `[[unbacked]]` with that reason.

### F05 [major] - D5' Reporting honesty / D4 Coherence: Table S5 is unbacked, disagrees with Table S2 on the same cell, and is presented as clean (reopens 2026-07-28 F03)

- **Location**: Supplementary Table S5 and its closing paragraph; main text l.1355-1363 ("Two
  robustness probes rule out under-sampling ...").
- **Evidence**:
  - The two tables report the identical reference cell (RF, seed 42, $N=100$, `kernel_width=3.0`,
    `num_samples=1000`) with different values. **Table S2**: fidelity 0.518, stability 0.000,
    96/100 valid. **Table S5**: fidelity 0.461, stability 0.014.
  - Table S5's values are neither registered nor listed as `[[unbacked]]`.
  - The thesis carries the same probe (Apéndice C) and, since 2026-08-28 (remediation D2 fallback),
    discloses it as a historical exploratory probe that cannot be re-derived and disagrees with the
    `kernel_width` probe. The fallback was chosen because the surviving script does not reproduce this
    design (ACTIVE_CONTEXT, 2026-08-28 third pass).
- **Reasoning**: the main text uses S5 to "rule out" a confound. A careful reviewer will put S2 next to
  S5 and ask which reference cell is right. The thesis already answers that question and the paper
  does not, so the two documents also disagree on what the probe is.
- **Fix**: port the thesis disclosure into the S5 caption and paragraph, including that the two probes
  disagree on the reference cell and why the directional conclusion survives. Change "rule out" to
  "find no evidence of" at l.1356. Register the S5 values as `[[unbacked]]` with the RCA-002 reason.

### F06 [major] - D1 Evidence relevance / D6 Methodological rigor: an unsupported theoretical claim is offered as the explanation of the fidelity result

- **Location**: l.1306-1320 ("SHAP's axiomatic guarantee implies that, conditional on its background
  distribution assumptions, its attribution rankings are optimally aligned with the feature-removal
  signal that fidelity metrics probe ... it does explain why SHAP consistently outperforms LIME").
- **Evidence**:
  - No cited result establishes that the Shapley axioms make attributions optimal for the
    correlation between attribution magnitude and single-feature masking drop.
  - The paper's masking replaces features with zero or reference values (l.1383-1386), while
    KernelSHAP's value function uses a background expectation over 50 samples. The two value functions
    differ, and KernelSHAP is itself a sampled estimate.
  - Three paragraphs earlier, the paper cites the suppressor-variable results (l.1240-1244) that argue
    against reading attribution magnitude as importance.
  - "Causal responsibility" (l.1313) conflates responsibility for the model output with causation in
    the data.
  - "Consistently" overstates the evidence: the Breast Cancer SHAP-LIME fidelity gap is +0.07 (l.1082).
  - The axiom list also differs between l.236 (efficiency, symmetry, dummy) and l.1307 (adds
    linearity), and neither matches the properties used by `lundberg2017unified` (local accuracy,
    missingness, consistency).
- **Reasoning**: TMLR reviewers with a theory background will read "implies ... optimally aligned" as
  a theorem claim without a proof or a citation.
- **Fix**: restate it as a plausible mechanism. For example: "SHAP's efficiency property ties
  attribution mass to the prediction change under its background distribution, which plausibly favours
  it on removal-based fidelity; we do not test this, and removal under a different reference
  distribution need not preserve it." Delete "optimally" and "causal". Make the axiom lists at l.236
  and l.1307 agree, and cite the axiom set used.

### F07 [minor] - D4 Coherence: the LIME cross-dataset stability range excludes a value in its own table

- **Location**: l.1085 and l.1372: "$0.85$--$0.93$".
- **Evidence**: `tab:exp3_lime` l.1131 gives German Credit/XGB stability **0.748**. The range is
  0.748-0.927.
- **Fix**: "0.75--0.93" at both sites, then register it. The verifier missed this because the range is
  an unregistered literal in an uncovered file (Phase 3).

### F08 [minor] - D6 Methodological rigor: the CV argument for "structural" instability runs backwards

- **Location**: l.993-998 and `tab:cv_reproducibility`.
- **Evidence**: the text concedes that "when the mean cosine similarity is near zero, any nonzero
  variation produces an extreme relative deviation". That is exactly why a CV of 86.2% on a mean of
  about 0.014 is an artifact of the ratio. It is not evidence of geometric instability.
- **Fix**: report the seed SD, or an absolute spread, for LIME stability. Say that CV is
  uninformative near a zero mean, and drop "structurally irreproducible" and "geometrically unstable"
  (see F03).

### F09 [minor] - D3 Scope calibration: "SHAP dominates all measured quality endpoints"

- **Location**: the abstract.
- **Evidence**: parsimony is one of the paper's quality properties (RQ2; `tab:constructs`; Figure 1
  plots active ratio among the "quality-oriented endpoints"), and LIME wins it in all 75 cells (l.964).
- **Fix**: "SHAP leads on every fidelity- and stability-oriented endpoint".

### F10 [minor] - D6 Methodological rigor: the original EXP4 prompt names the wrong dataset for half the cases

- **Location**: Supplementary S1, the per-instance prompt ("Dataset: UCI Adult Income (Census Income,
  14 features)"; "Explainer: (SHAP or LIME)"). Main text §EXP4, l.565-596.
- **Evidence**: 96 of the 192 cases come from German Credit and Breast Cancer, and the cases span all
  four explainers (l.569-572). The supplementary notes that the replication read the dataset from each
  case record, "although the system instruction above names Adult only".
- **Reasoning**: if the transcription is accurate, the original judges were told the wrong dataset for
  half the cases. That is a validity threat specific to the original cohort's ICC, and an instrument
  difference between the cohorts beyond the change of panel. The main text mentions neither.
- **Fix**: one sentence in §EXP4 naming this as a difference between the cohorts, qualified by the
  fact that the original templates are lost, so the transcription cannot confirm what the judges saw.

### F11 [minor] - D6: "Both methods were run with default hyperparameter settings"

- **Location**: l.1432-1433.
- **Evidence**: `kernel_width=3.0`, `num_samples=1000` and a 50-sample SHAP background (l.834-838) are
  not library defaults. LIME's default kernel width is $0.75\sqrt{d}$, about 7.6 at $d=103$, and its
  default `num_samples` is 5000. The paper itself calls 3.0 "the minimum viable configuration".
- **Fix**: "fixed reference settings".

### F12 [minor] - D5': stale and mis-rendering statements in the artifact sections

- **Location and evidence**:
  - l.1417-1419, "Before journal submission, the exact review snapshot should be frozen ... under a
    version-specific DOI", is an internal to-do. It contradicts l.1498, which says the snapshot is
    archived.
  - l.1462-1466: the `\ifdeanon` branches are spliced into "available in the public repository at ...".
    The anonymous build reads "in the public repository at the anonymised artifact bundle", and the
    camera-ready build reads "in the public repository at the public repository <url>".
  - l.1415-1416, "Figures are regenerated directly from the paired-cell Wilcoxon exports", does not
    hold for `fig_exp3_gap.pdf`, which has its own generator.
  - `scripts/generate_paper_b_figures.py` writes to `docs/reports/paper_b/figures/`, not the
    `paper_bc/figures/` the manuscript includes. RCA-001's figure invariant asks for a committed
    generator that rebuilds the figure actually used.
- **Fix**:
  - Delete the to-do.
  - Restructure the sentence so each branch is a whole clause.
  - Name both figure sources.
  - Point the generator at `paper_bc/figures/`, which is also needed for F02's redrawn Figure 1.

### F13 [suggestion] - D1: priority claim

- **Location**: l.149-151: "to our knowledge, the first multi-rater LLM-judge reliability measurement
  in XAI".
- **Fix**: priority claims attract reviewer counter-examples. "Among the first", or a stated search
  that supports "first", is safer.

### F14 [suggestion] - D5': "almost every score is 1"

- **Location**: l.620-621.
- **Evidence**: `experiments/exp4_cohort2/RESULTS.md:60` gives 86% of actionability scores at 1.
- **Fix**: print the figure.

### F15 [suggestion] - wording

- **S6**: "decreases monotonically ... (+0.098 → +0.098 → ...)" contains a tie; use "does not
  increase".
- **S1 caption**: "Three primary condition:" should read "Three conditions:".

## Handed to Phase 2 (reference audit), noticed in passing

- 8 of 60 bibliography entries are never cited: `agrawal2025xaieval`, `covert2020sage`,
  `guidotti2018survey`, `lipton2018mythos`, `samek2017evaluating`, `sithakoul2024beexai`,
  `wachter2017counterfactual`, `yeh2019infidelity`.
- `nauta2023anecdotal`: mojibake ("SchlÃ¶tterer") in the `\bibitem` label.
- Year and volume combinations to check: `fok2023verifiability` (AI Magazine 45(3) is a 2024 volume);
  `zhou2025medthink` (npj Digital Medicine 9 is a 2026 volume); `wachter2017counterfactual` (key 2017,
  entry 2018).

## Dimension rationale

- **D1 = 3**: the confirmatory evidence is strong, but the headline deployment claim (F01) and the
  mechanism claim (F06) are not supported by it.
- **D2 = 4.5**: four directional hypotheses with stated tests, and a pre-set 0.75 threshold for EXP4.
- **D3 = 3**: the abstract overshoots the body twice (F03, F09), and "tree-based" generalises from
  one family (F01).
- **D4 = 3**: the paper contradicts itself on LIME's instability (F03), the stability range (F07),
  and its provenance statement against its own figure (F02).
- **D5' = 3.5**: the EXP4 and corpus disclosures are exemplary. The screening table (F04), Table S5
  (F05) and the Paper A overlap (F02) fall short of them.
- **D6 = 3.5**: the paired design and multiplicity control are right. The CV argument (F08), the
  mislabelled defaults (F11) and the undisclosed prompt issue (F10) are fixable.

## Readiness assessment

**Not ready to file as it stands.**
- **F01 and F02 must be fixed before filing.** F01 is a false headline claim in the abstract. F02 is a
  written statement to TMLR, repeated in the editor note, that is contradicted by a sentence and a
  figure.
- **F03-F06 are the passages a reviewer is most likely to probe.** They take about half a day of prose
  and registry work.
- **Nothing reopens the confirmatory core**, and no experiment needs re-running.

Estimated remediation effort: 5-7 hours, followed by the whole "After any revision" checklist. The
abstract changes (F01, F03, F09) trigger the RCA-003 page-1 read and the top-level statement sweep.
F03 and F05 also touch the thesis sync matrix, since the thesis carries the same LIME claim and the
same Table S5.

## Questions for the author

1. **F02, EXP3 figure**: is showing SHAP levels by stacking (Anchors level + gap) acceptable to you
   under TMLR's reuse policy, or should the figure show the gaps alone? The caption presents the
   stacking as deliberate.
2. **F04**: does the original search/screening log exist anywhere (a spreadsheet, Zotero, email)? If
   so it can be released and the counts registered. If not, the caption must say it is not released.
3. **F10**: do you recall whether the original EXP4 prompt really hard-coded "UCI Adult Income", or is
   that an artifact of transcribing Table S1 after the templates were lost?
4. **F01**: do you want Tier 1 conditioned on XGBoost only, or to add "measure first" guidance for
   other tree ensembles?

## Post-fix status (Step 8, 2026-09-30)

Checked against the rebuilt PDF (27 pages) on the paper lane at `e57f49e04`.

| Finding | Status | Commit |
| ------- | ------ | ------ |
| F01, F03, F09 | Fixed: Tier 1 scoped to XGBoost; one scoped account of LIME instability | `91766b04d` |
| F02 | Fixed: restated Paper A means removed; paired-difference and gap-only figures; registry-independent scan added | `85c65557a`, `b37fae1ff` |
| F04, F05, F06 | Fixed: screening record, Table S5 provenance, scoped axiom paragraph | `c5457ab9c` |
| F07, F08, F11, F12, F18, F19 | Fixed | `8caf2b29e` |
| F10 | Closed by author decision (won't fix) | `22f8f26c8` |
| F13, F14, F15 | Fixed | `f6c244dd1` |
| F16, F17 | Fixed | `3929936e3` |

Later, beyond the review: the abstract names the dataset as the "UCI Adult census-income dataset"
(`57811d139`), and the equations are numbered with every term defined and their sources cited
(`05016a963`). The "After any revision" checklist passes; its record is in `OPENREVIEW_SUBMISSION.md`.
