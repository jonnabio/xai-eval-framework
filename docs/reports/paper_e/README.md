# Paper E — do explainers agree on which features matter?

**Status: SUBMITTED on 2026-10-04 to *Computación y Sistemas* (CIC-IPN, Mexico), in
English, as submission 6783.** See "Submission record" below. Do not rebuild
`submission/` or change the analysis unless the journal asks for a revision.

## Submission record

| | |
|---|---|
| Journal | *Computación y Sistemas*, online system |
| Submission ID | 6783 |
| Date | 2026-10-04 (acknowledgement received by email the same day) |
| Tracking | <https://cys.cic.ipn.mx/index.php/CyS/author/submission/6783> |
| File sent | `submission/paper_e_blind.pdf`, 15 pages, built from `main` at `193f1660e`; no supplementary file |
| Title | Do Explainers Agree on Which Features Matter? Instance-Level Agreement between SHAP and LIME |
| Author | Jonathan Herrera-Vásquez (single author) |
| Archive cited in the full version | Zenodo 0.8.0, `10.5281/zenodo.23142429` |
| Note to the editor | Sent with the submission: originality; the public repository and archive, where earlier drafts are reachable; the three related works on the same cohort; the analysis plan committed before the analysis |

Before submission the manuscript was revised after two rigor reviews
(`docs/review/scientific-rigor-review_paper_e_2026-10-04.md` and `..._r2.md`); the two
"Response" sections below say what was done for each finding. The text after the second
revision was read by the author and not reviewed a third time.

## Where this paper is worked

**Here: `xai-eval-framework/docs/reports/paper_e/`, on branch
`paper/e-feature-agreement` checked out in the main folder.** Not in `../xai-paper-e`
and not in any other folder. This is the author's instruction of 2026-10-03, recorded in
ADR-0021 and in `scripts/pubs/lanes.toml`. A session that finds the main folder on
another branch switches it (clean tree first); it does not go to another folder.

## Venue: Computación y Sistemas

Guidelines: <https://www.cys.cic.ipn.mx/index.php/CyS/about/submissions#authorGuidelines>
(read 2026-10-03).

- Original, unpublished work, not under review elsewhere.
- File: PDF made with LaTeX, or Word. Templates: `template/LATEX.ZIP` and
  `template/CyS-template.docx`, downloaded from the journal on 2026-10-03; `cys.cls` and
  `cys.bst` beside the manuscript are the unmodified files from that archive.
- Single spacing, 10-point Arial-like font, figures and tables inside the text, italics
  instead of underlining, URLs or DOIs in the references, BibTeX obligatory.
- Blind review: `submission/paper_e_blind.pdf` has no author block, no repository
  address and no self-citation.
- Submission is online, after registering at
  <https://www.cys.cic.ipn.mx/index.php/CyS/user/register>. The page states no fee and no
  page limit. The author's limit for this paper is 15 pages.

## Files

| File | What it is |
|---|---|
| `paper_e_template.tex` | **The source.** Edit this. Every number is a placeholder. |
| `paper_e.tex`, `tables/`, `figures/` | Generated. Do not edit. |
| `paper_e_layout.tex` | Layout constants and the release/archive macros. |
| `references.bib` | 25 entries, checked against Crossref, arXiv or the publisher page, except the bootstrap textbook. All approved by the author (24 on 2026-10-03; `bhatt2020evaluating`, the source of the fidelity measure, on 2026-10-04). |
| `scripts/paper_e_posthoc.py` | Post hoc diagnostics (plan section 9, 2026-10-03). |
| `scripts/paper_e_sign_contribution.py` | Post hoc direct sign test (plan section 9, 2026-10-04). |
| `scripts/paper_e_review_analyses.py` | Post hoc re-cuts for the rigor review (baseline, held-out contrast, rank sensitivity, coverage). |
| `scripts/paper_e_ceiling.py` | Post hoc self-agreement experiment, with the default-width LIME runs and the saved top-10 lists (needs the model binaries; see its docstring). `--summarise-only` recomputes its CSV files from `ceiling_lists.json`. |
| `scripts/paper_e_review2_analyses.py` | Post hoc analyses for the second review: permutation reference, range of the stored LIME stability, kernel weights (needs scikit-learn and the datasets). |
| `scripts/build_paper_e.py` | Figures, tables, `paper_e.tex` and both PDFs. |
| `submission/paper_e_blind.pdf` | The file for review. **Local only since 2026-10-04:** the PDFs are not tracked by git (blind review; the journal asks that the work is not available online). Run the build to regenerate them. |
| `submission/paper_e_full.pdf` | With author, repository address and self-citation. |

## Build

```
python docs/reports/paper_e/scripts/paper_e_posthoc.py    # writes outputs/analysis/paper_e/posthoc/
python docs/reports/paper_e/scripts/build_paper_e.py      # figures, tables, tex, two PDFs
```

Needs Python with numpy, pandas and matplotlib (the project `.venv` works) and the
Tectonic compiler at `tools/tectonic-portable/`. The build fails on a placeholder it
cannot resolve, so a number cannot be typed by hand or left stale.

## Main results (all generated; see the PDF)

- Top-5 Jaccard overlap between SHAP and LIME: 0.393 on Adult, 0.387 on German Credit,
  0.714 on Breast Cancer; rank concordance is weak on the first two.
- **Post hoc, permutation reference:** the SHAP list of an instance and the LIME list of
  another instance of the same run already overlap by 0.203 / 0.287 / 0.648. The
  instance-specific part is 0.191 / 0.100 / 0.066: largest on Adult, smallest on Breast
  Cancer, where most of the overlap is a ranking common to the instances.
- **Post hoc, self-agreement:** neither method reproduces its own top-5 list (Adult: LIME
  0.690, SHAP 0.782); SHAP-LIME agreement is below both for every model, between the new
  runs as between the stored explanations.
- Agreement varies between the fitted models and the datasets, not visibly with the
  sampling intensity. On Adult each family is one fitted model.
- No consistent difference between correct and misclassified instances, also on held-out
  rows.
- Disagreement is higher where the fidelity of the LIME explanation is lower, on Adult and,
  more weakly, on German Credit. The measure favours contributions over slopes.
- **Post hoc, signs:** sign agreement follows the predicted class (Breast Cancer: 0.977 for
  class 0, 0.036 for class 1) because LIME without discretisation stores slopes and SHAP
  stores contributions. After conversion it is 0.945 / 0.960 / 0.990, a level that one
  fixed direction per feature also reaches (0.951 / 0.978 / 0.990). The paper claims a
  shared global direction per feature, not agreement on instance-specific directions.
- **Post hoc, LIME configuration:** the kernel width is 3 (package default: 0.75 times the
  square root of the number of features), chosen without a technical reason. The 999
  perturbed samples together receive a median weight of 0.26 on Adult, 2.3 on German
  Credit and 83.6 on Breast Cancer, against 1 for the instance. LIME at the default width
  shares 0.370 of its top-5 with LIME at width 3 on Adult, and is less specific to the
  instance (two explanations of different instances overlap by 0.589, against 0.195).

## Method statements checked against the code (2026-10-04)

| Statement | Checked in | Result |
|---|---|---|
| Fidelity definition | `src/experiment/metrics_engine.py`, `src/metrics/faithfulness.py`, `scripts/run_exp3_lime.py` | **Corrected.** It is the correlation between attribution size and single-feature masking effect, not a surrogate R². |
| Stability definition | `src/metrics/stability.py`, run configs | Confirmed: mean pairwise cosine similarity over 15 noisy copies. |
| TreeSHAP output scale | `src/xai/shap_tabular.py` | **Corrected.** Probability, interventional; the draft said log-odds for XGB. |
| KernelSHAP for LR, SVM, MLP; 50 background instances | `configs/experiments/exp2_scaled/*_shap_*.yaml` | Confirmed. |
| LIME: 1000 samples, kernel width 3, ten features, no discretisation | `src/xai/lime_tabular.py`, `src/experiment/runner.py`, configs | Confirmed. |
| LIME value is a slope on a standardised scale | `lime` package behaviour with `discretize_continuous=False` | Confirmed, and by the direct test above. |
| Stored top-10 by absolute value | `runner.py::_format_explanation` | Confirmed. |
| 108 / 61 / 30 encoded features | reloaded data; run metadata | Confirmed. |
| Sampling per confusion-matrix quadrant | `src/evaluation/sampler.py` | Confirmed. |
| Adult models trained once; seed fixes the partition | `runner.py::setup`, model metadata | **Added** to the manuscript with the training-overlap limitation. |

## Decisions by the author (2026-10-03)

- **Single author.** The thesis director declined co-authorship: the work is the
  author's.
- **References approved:** the 24 entries of `references.bib`.
- **No AI-use declaration** in the manuscript; the journal does not ask for one.
- **Clickable blue links** (2026-10-04) for citations, cross-references, URLs and DOIs,
  through `hyperref` (`colorlinks`, all blue). The journal class does not load it. Of the
  24 articles in the journal's current issue on 2026-10-04, 9 have links, added by their
  authors, in mixed styles; there is no journal rule. A DOI in the reference list links
  to `https://doi.org/<doi>`; a complete address in `references.bib` is written with
  `\fullurl{...}`, not `\url{...}`. The PDF metadata carries no author.
- **Length: at most 15 pages** in the journal layout (the draft has 11). The journal
  states no limit; this is the author's limit. `build_paper_e.py` stops if a PDF has more
  than `MAX_PAGES = 15`.

## Response to the rigor review (2026-10-04)

| Finding | What was done |
|---|---|
| F01 no within-method ceiling | New experiment `scripts/paper_e_ceiling.py`: each method run twice on 760 instances. New Section 4.2 and Table 2; abstract, discussion and conclusions rewritten around it. SVM left out (cost). |
| F02 converted sign agreement matched by a fixed direction | Majority-sign baseline computed and reported beside the converted value; "the direct test confirms" removed; claim limited to a global direction per feature. |
| F03 correctness contrast confounded with training rows | Share of training rows reported; contrast repeated on held-out rows (the MLP and RF signs remain). |
| F04 intervals are ranges of seed means | Stated in Methods and limitations; "do not overlap" and "includes zero" removed; "five fitted models". |
| F05 LIME selection and sampling | Described in Section 3.2. |
| F06 Kendall measure read on the wrong scale | Measure described; comparison with overlap removed; shared-only tau added as sensitivity. |
| F07 untested cause of low rank concordance | Re-ranking by contribution computed and reported; sentence replaced. |
| F08 overclaims | Reworded ("did not vary visibly", "no consistent association", fidelity claim limited to Adult and German Credit). |
| F09 SVM coverage | 29.5% stated in Section 3.4 and in the limitations. |
| F10 "registered"; unreported plan items | "Written and committed before"; sign intervals and the number of shared features reported; every post hoc analysis labelled; second companion manuscript named. Medians of the run means for the primary measure are given in one sentence of Section 4.1 (the remaining medians are in `group_agreement_summary.csv`). |
| F11 citation fit | Roy, Garreau, Alvarez-Melis and Bhatt sentences reworded. |
| F12 seed-42 sentence | Names the measure; held-out contrast added. |
| F13 public PDFs | PDFs untracked and ignored from 2026-10-04. They remain in the earlier git history, on `main` and in the Zenodo archive v0.6.0, which cannot be withdrawn; declare this in the cover letter. |
| Reference audit | URL added to Lundberg and Lee; DOI added to Efron and Tibshirani; Krishna et al. kept on arXiv by the author's decision. |

## Response to the second rigor review (2026-10-04)

Author's answers to the review's questions: no technical reason for the kernel width of 3;
the run log of the self-agreement experiment is not available; the default-width rerun is
accepted. The title is kept, and the permutation reference is reported in the abstract.

| Finding | What was done |
|---|---|
| F01 overlap compared only with random sets | Permutation reference computed (`paper_e_review2_analyses.py`, 20 draws per instance) and reported in the abstract, Section 3.3, Section 4.1, a new column of Table 1, Fig. 1, Section 4.3, the discussion and the conclusions. The dataset paragraph and "low agreement is not inevitable" are rewritten. The self-agreement experiment has its own permutation reference (Table 2). |
| F02 LIME configuration | Kernel width and package default stated in Section 3.2 and in the abstract; kernel weights computed and reported in the limitations; range of the stored LIME stability reported (dated deviation from plan section 4) and Table 5 annotated; LIME rerun with the default width on the 760 instances (new paragraph in Section 4.2). Result: the width changes the LIME list as much as the change of explainer; the narrow kernel gives the more instance-specific explanations. |
| F03 random-forest row of Table 2 | The experiment was rerun; it counts the skipped candidates (32 for the Adult random forest, none elsewhere) and Table 2 now gives SHAP-LIME agreement between the new runs. The limitation sentence and the two plan statements are corrected. |
| F04 sentence on the wrong column | Moved to the fidelity paragraph; the stability values of gradient boosting are given. |
| F05 models and self-agreement | Sentence limited to the multilayer perceptron, in Section 4.2 and in the discussion. |
| F06 held-out contrast | SVM value and its coverage in the text; contribution (iii) labelled post hoc. A column in Table 4 did not fit the single-column table; the five values are in the text. |
| F07 captions | "Spread of the seed means" added to the captions; SVM coverage noted in Tables 1 and 4; plan commit hash in the full version. |
| F08 README and plan | This README rewritten; the plan entry of the first conversion is qualified by a later entry. |
| F09 same runs in Table 2 | Done (see F03). |
| F10 title | Kept, with the permutation reference in the abstract (author asked for a recommendation; this is it). |

The rerun of the self-agreement experiment reproduced every earlier estimate exactly; the
interval limits moved by at most 0.003 because the bootstrap draws more groups.

## Claim registry

Paper E is under `[coverage]` and `[exclusivity]` in `pub/claim_registry.toml`
(`paper_e.tex` and the six files in `tables/`). Every printed number is a `paper_e`
source expression (`scripts/pubs/claim_sources.py`); the build writes them to the
generated Paper E block of the registry, and `python scripts/pubs/verify_claims.py`
re-derives each from the CSV files. Consequences:

- a decimal typed by hand in `paper_e_template.tex` fails the coverage check;
- layout constants live in `paper_e_layout.tex`, which is not under coverage;
- a literal that equals a Paper B+C result by chance is listed by the build as an
  `[[exclusivity_exception]]` naming its Paper E source;
- the registry block is a shared path: commit it separately from the Paper E files.

## Release and archive

Procedure: `docs/reports/paper_bc/ZENODO_RELEASE.md`, Route A (bump `.zenodo.json` and
`CITATION.cff`, publish a GitHub release, wait for Zenodo, set `\papererelease` and
`\paperearchive` in `paper_e_layout.tex`, rebuild). The manuscript inside the archive
prints "[ZENODO VERSION DOI PENDING]"; the code and data in it are exact.

| | |
|---|---|
| Release | `paper-e-cys-2026-10-04-r2` (commit `8bed86320`, on `main`), published 2026-10-04 |
| Version | 0.8.0. Earlier: 0.7.0 (`10.5281/zenodo.23139911`, release `paper-e-cys-2026-10-04`, before the second review) and 0.6.0 (`10.5281/zenodo.23130949`, release `paper-e-cys-2026-10-03`, before the first review) |
| Version DOI (cited in the full PDF) | `10.5281/zenodo.23142429` |
| Concept DOI (all versions) | `10.5281/zenodo.19297723` |
| Archive | one zip, 918 MB, open access, MIT licence |

If the analysis code or its results change before submission, publish a new version and
update the two macros. A change to the text alone does not need one.

Version 0.8.0 contains the analysis code and result files of the second revision. Its
manuscript source has the shortened title and still cites 0.7.0; the code and data are
exact.

## Open items

1. Author: read the draft and the interpretation.
2. The reference to Paper A (RIMI) has no volume in the record; the journal style prints
   an empty field. Add the volume if the journal has one.
3. Author: register at the journal site and submit `submission/paper_e_blind.pdf`; confirm
   there that no fee applies.
4. Cover letter: say that earlier drafts were in a public repository and in Zenodo 0.6.0,
   and name the two companion manuscripts.

## The question

When several post-hoc explainers explain the **same prediction**, do they point to the same
features, in the same order and with the same direction of effect? The literature calls this
the "disagreement problem". Practitioners often treat SHAP, LIME and other methods as
interchangeable, but if they disagree on the top features, the choice of explainer changes
the explanation a user sees.

## Sub-questions (formalized in `ANALYSIS_PLAN.md` before results are computed)

1. How much do the explainers agree on the top-k features for the same instance?
   Measures: top-k overlap, rank correlation, and sign agreement.
2. Does agreement depend on the model family, the dataset, or the sampling intensity?
3. Is agreement lower on misclassified instances? This links to Paper D's result; cite it,
   do not repeat it.
4. Does agreement predict explanation quality? For example, are instances where explainers
   disagree also those with low fidelity or stability?

## Why it can be a separate paper (and how to keep it separate)

- **Different question.** Paper D compares quality between correct and incorrect
  predictions. Paper E compares explainers with one another.
- **New data, not only re-analysis.** It must include something that exists nowhere else:
  - EXP2 (Adult): all four methods explained the **same instances**, and each run stores the
    top-10 attributions (`instance_evaluations[].explanation.raw_top`).
  - EXP3 (German Credit, Breast Cancer): SHAP and Anchors have per-instance attributions.
    **LIME stored only averages** (`outputs/analysis/exp3_lime_results.csv`), so a new LIME
    run with per-instance attributions is needed: `scripts/run_exp3_lime.py`, extended to save
    `raw_top`. That run is a new experiment, and it is what makes Paper E broader than a slice
    of the existing cohort.
- **Different venue and time.** Submit after Paper D, to a different journal.
- **Disclosed provenance.** State, as Papers B+C and D do, that the EXP2/EXP3 runs are the
  benchmark cohort of Papers A and B+C, and report none of their results.
- **Enforced.** When the manuscript exists, add it to `[coverage]` and `[exclusivity]` in
  `pub/claim_registry.toml`.

## Data available now (checked 2026-10-03)

| Source | Explainers with per-instance attributions | Notes |
|---|---|---|
| EXP2, UCI Adult | SHAP, LIME, Anchors, DiCE | 299 source run files; valid instance-ID coverage varies by method and block, so each comparison uses its recorded matched intersection |
| EXP3, German Credit | SHAP, Anchors, Paper E LIME | Six new LIME runs explain the exact stored SHAP instance IDs |
| EXP3, Breast Cancer | SHAP, Anchors, Paper E LIME | Six new LIME runs explain the exact stored SHAP instance IDs |

## Generated artifacts

The new per-instance LIME cohort, run manifest, analysis tables, diagnostics and figures
are committed on `results/paper-e-agreement`:

- [`EXP3 LIME cohort`](../../../outputs/analysis/paper_e/exp3_lime/)
- [`Analysis report and artifacts`](../../../outputs/analysis/paper_e/analysis/)
- [`RESULTS.md`](../../../outputs/analysis/paper_e/analysis/RESULTS.md)

The primary SHAP-LIME analysis contains 31,411 paired instance records across 87 audited
blocks. Only matched, classification-consistent IDs are included. The machine-readable
diagnostics record 76 blocks with exact valid-ID sets, 4,936 unpaired valid method-IDs and
zero classification mismatches in primary pairs. Secondary Anchors/DiCE comparisons are
feature-set overlaps only; mismatched classifications and potentially truncated Anchor
rules are excluded and documented in the diagnostics.

The aggregate EXP3 LIME file at `outputs/analysis/exp3_lime_results.csv` remains unchanged.

**Caveat:** Anchors returns rules and DiCE returns counterfactuals, not additive
attributions. How their "top features" are defined in `raw_top` must be checked before they
are compared with SHAP and LIME. The comparison may be limited to SHAP versus LIME, plus
feature *sets* for Anchors and DiCE.

## Analysis workflow

1. `ANALYSIS_PLAN.md` was committed before computing any Paper E result.
2. The initial source audit in `DATA_AUDIT.md` was reproduced with
   `python scripts/paper_e_data_audit.py`; it is structural/identity QC, not a Paper E result.
3. The EXP3 LIME cohort is stored separately and uses the exact IDs in the existing SHAP
   runs. EXP3 model binaries are not tracked; regenerate them to an isolated artifact root:
   `python scripts/train_exp3_models.py --model-root <model-root> --data-cache-dir <cache-dir>`.
   The LIME runner validates the regenerated metadata, training metrics, feature order and
   stored target predictions before running:
   `python scripts/run_exp3_lime.py --paper-e --model-root <model-root> --data-cache-dir <cache-dir> --paper-e-output-dir <lime-output-dir>`.
4. The prespecified analyses are reproducible with
   `python scripts/analyze_paper_e.py --lime-root <lime-output-dir> --output-dir <analysis-output-dir>`
   and produced committed tables, diagnostics and figures on the results branch.
5. Remaining: verify each literature reference against its DOI with author approval, choose a
   different venue (no publication fee; English), and draft only after scientific review.
