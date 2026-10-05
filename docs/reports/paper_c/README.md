# Paper C: LLM judges as evaluators of explanations

**Scope:** the LLM-judge reliability study (EXP4, two judge panels on the same 192 cases),
with the taxonomy and the 44-paper scoping corpus as framing (ADR-0022).

**Target:** *Tecnología en Marcha*, special issue on Artificial Intelligence, 2027 edition.
Deadline 2026-10-15, by email to revistatm@tec.ac.cr.

**Status (2026-10-04):** plan approved; **first draft built**, 12 pages in Word (limit 15),
abstract 244 words and resumen 248 (limit 250), 4 tables, 1 figure, 25 references. The draft
is the version without the human-rated subset and without counts on the audited corpus axes
(the two fallbacks of the plan). It has not been reviewed and the author has not read it.

**Open before submission**

1. Author: read the draft (`submission/paper_c_blind.pdf`, local).
2. Author: decide on a clean prompt condition (`PLAN.md`, section 14.4).
3. Raters: send the two rating sheets (`human_subset/README.md`); cut-off 2026-10-10.
4. Second reviewer: adjudication sheet in `corpus_audit/`; cut-off 2026-10-08.
5. Registry: put `paper_c.tex` under `[coverage]`, add `docs/reports/paper_c/` to the
   protected side of `[exclusivity]`, wire `verify_sync.py`, replace the placeholder abstract
   in `pub/claims.toml` (shared files, through `main`). Not done: the numbers of the draft
   are generated from result files but are not yet in `pub/claim_registry.toml`.
6. Independent rigor review; Zenodo version; set `\papercrelease` and `\papercarchive` in
   the template.
7. Author: check the two references marked NEW in `references.bib`.

**Lane:** `paper-c`, branches `paper/c-*`, worked in the main folder. Everything of Paper C
lives in this directory: manuscript, plan, scripts, result files and copies of its inputs.

## History

Until 2026-10-04 this folder held the April 2026 survey prototype ("From Fidelity to
Semantics", JMLR style, 24-study corpus). The assessment of 2026-10-04 judged a survey-only
paper not viable, and the author had it removed. It remains in the git history; the last
commit that contains it is the parent of "paper c: remove the April 2026 survey prototype".

## Files

| Path | What it is |
|---|---|
| `PLAN.md` | Scope, venue rules, page budget, work packages, pre-specified analyses, schedule, findings after approval |
| `paper_c_template.tex` | **The manuscript source.** Numbers are placeholders filled from result files |
| `paper_c.tex` | Generated from the template by `scripts/build_paper_c.py`. Do not edit |
| `references.bib` | IEEE references; two entries marked NEW await the author's check |
| `scripts/paper_c_posthoc.py` | Judge scores against the metrics shown in the prompt (plan section 7) |
| `scripts/paper_c_summary.py` | Summary values and Figure 1 |
| `scripts/build_paper_c.py` | Render, PDF and Word in a blind and a full version, figure upload |
| `scripts/draw_human_sample.py` | The 56-case sample and the two rating sheets |
| `results/` | `summary.csv`, `posthoc_scores_vs_metrics.csv`, `posthoc_rank_regression.csv` |
| `figures/` | `fig1` as .pdf (LaTeX), .png (Word) and .tiff (upload, 300 ppi) |
| `human_subset/` | Sample, rating sheets and instructions for the raters |
| `submission/` | Built files: `paper_c_blind.{pdf,docx}`, `paper_c_full.*`, `Figure1.tiff`. Local only for now (`.gitignore`) |
| `ieee.csl`, `reference_default.docx` | Used to make the Word file (copies of Paper D's) |
| `paper_c_review_corpus.csv` | The 44-paper coded corpus. Copied from `docs/reports/paper_bc/paper_bc_review_corpus.csv` on 2026-10-04; this copy is the working file |
| `corpus_audit/` | Second-reviewer audit (plan, template, results, summary) and the adjudication sheet with 28 open disagreements. Copied from `docs/reports/paper_bc/` on 2026-10-04; these copies are the working files |

## Build

```
.venv/Scripts/python.exe docs/reports/paper_c/scripts/paper_c_posthoc.py   # about 10 minutes; only if the analysis changes
.venv/Scripts/python.exe docs/reports/paper_c/scripts/paper_c_summary.py   # summary values and the figure
python docs/reports/paper_c/scripts/build_paper_c.py                       # paper_c.tex, PDFs, Word files
```

The build needs Tectonic (`tools/tectonic-portable`) and Quarto's pandoc. It stops on a
placeholder it cannot resolve. Measure the length in Word itself.

## Inputs read in place, never rewritten

| Path | Content |
|---|---|
| `outputs/analysis/exp4_llm_evaluation/` | Original cohort aggregates (RCA-002) |
| `experiments/exp4_cohort2/` | Cohort 2 cases, prompts, raw responses, parsed scores |
| `outputs/analysis/exp4_cohort2/` | Cohort 2 analysis files |
| `docs/reports/paper_bc/paper_bc_iberamia.tex` and appendix | The rejected 32-page edition, source of the text to rewrite |

## Rules

- `docs/reports/paper_bc/` is frozen; do not edit it for Paper C.
- No Paper B result is printed here, and no Paper C result in Paper B (ADR-0022).
- Shared files (`pub/`, `scripts/pubs/`, `docs/adr/`, `ACTIVE_CONTEXT.md`) are committed
  separately and reach `main` by pull request.
