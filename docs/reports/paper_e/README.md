# Paper E — do explainers agree on which features matter?

**Status (2026-10-03): draft complete, registered and archived; awaiting the author's read.** Target journal: *Computación y
Sistemas* (CyS, CIC-IPN, Mexico), in English. Not submitted.

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
| `references.bib` | 24 entries; 22 checked against Crossref or arXiv on 2026-10-03 (not the bootstrap textbook or the Paper A entry). Approved by the author. |
| `scripts/paper_e_posthoc.py` | Post hoc diagnostics (plan section 9, 2026-10-03). |
| `scripts/build_paper_e.py` | Figures, tables, `paper_e.tex` and both PDFs. |
| `submission/paper_e_blind.pdf` | The file for review. |
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
- Agreement depends on model family and dataset, not on sampling intensity.
- No consistent difference between correct and misclassified instances.
- Disagreement is higher where LIME's local fidelity is lower.
- **Post hoc:** sign agreement follows the predicted class (Breast Cancer: 0.977 for
  class 0, 0.036 for class 1) because LIME without discretisation stores slopes and SHAP
  stores contributions. The paper reports it as a methodological finding.

## Decisions by the author (2026-10-03)

- **Single author.** The thesis director declined co-authorship: the work is the
  author's.
- **References approved:** the 24 entries of `references.bib`.
- **No AI-use declaration** in the manuscript; the journal does not ask for one.
- **Length: at most 15 pages** in the journal layout (the draft has 11). The journal
  states no limit; this is the author's limit. `build_paper_e.py` stops if a PDF has more
  than `MAX_PAGES = 15`.

## Claim registry

Paper E is under `[coverage]` and `[exclusivity]` in `pub/claim_registry.toml`
(`paper_e.tex` and the five files in `tables/`). Every printed number is a `paper_e`
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
| Release | `paper-e-cys-2026-10-03` (commit `fe3604406`, on `main`), published 2026-10-03 |
| Version | 0.6.0 |
| Version DOI (cited in the full PDF) | `10.5281/zenodo.23130949` |
| Concept DOI (all versions) | `10.5281/zenodo.19297723` |
| Archive | one zip, 918 MB, open access, MIT licence |

If the analysis code or its results change before submission, publish a new version and
update the two macros. A change to the text alone does not need one.

## Open items

1. Author: read the draft and the interpretation.
2. The reference to Paper A (RIMI) has no volume in the record; the journal style prints
   an empty field. Add the volume if the journal has one.
3. Author: register at the journal site and submit `submission/paper_e_blind.pdf`; confirm
   there that no fee applies.
4. Possible addition: convert LIME slopes to contributions and recompute sign agreement
   (needs the feature values of each instance, so the runs must be reloaded).

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
