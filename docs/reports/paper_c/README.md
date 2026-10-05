# Paper C: LLM judges as evaluators of explanations

**Scope:** the LLM-judge reliability study (EXP4, two judge panels on the same 192 cases),
with the taxonomy and the 44-paper scoping corpus as framing (ADR-0022).

**Target:** *Tecnología en Marcha*, special issue on Artificial Intelligence, 2027 edition.
Deadline 2026-10-15, by email to revistatm@tec.ac.cr.

**Status (2026-10-04):** **second draft, revised after the rigor review**
(`docs/review/scientific-rigor-review_paper_c_2026-10-04.md`). **15 pages in Word, the
journal's limit**; abstract 246 words and resumen 249 (limit 250), 5 tables, 1 figure, 25
references. The clean condition was run (576 calls, all valid). The draft has no human-rated
subset. The author has read it. The revision was made by the session that wrote the review
and has not been reviewed again. On `main`, archived as Zenodo 0.10.0; **not submitted**.

**Main results of the revision**

- Over all cases no dimension reaches ICC(1,1) 0.75 in either panel; with one call per judge
  the values are lower, and the mean of the three judges is 0.75 or more on four dimensions.
- Up to 67% of the score variance lies between explainers. Inside SHAP no dimension exceeds
  0.19 (0.20 without metrics); inside LIME five dimensions stay between 0.63 and 0.75.
- Without metrics in the prompt: the judge that cited them most scores higher, the relation
  with fidelity vanishes for SHAP and DiCE and stays for LIME and Anchors, and agreement on
  audit usefulness falls from 0.66 to 0.42.

**Response to the rigor review**

| Finding | Response |
|---|---|
| F01 pooled ICC measures the explainer | Section 3.2, Table 2, Figure 1; abstract, discussion and conclusions rewritten around it |
| F02 rendering of Anchors and DiCE | Described with examples in the methods; SHAP and LIME are the main analysis; stated in the limitations. Not re-rendered (author decision) |
| F03 unit of the estimate | Table 1: three calls averaged, one call, ICC(1,k); conclusion limited to a single judge |
| F04 metrics in the prompt | Share of rationales naming a metric per judge; clean condition run and reported (section 3.5, Table 5) |
| F05 panels confounded | Differences between the runs listed in the methods; "between the two runs" in the results |
| F06 raw agreement | Share of pairs with the same score in Table 1; narrow range described |
| F07 interval | Exact F-based intervals for both panels |
| F08 model | ICC(2,1) and ICC(3,1) reported as a check; "only" removed |
| F09 ties | Noted in the caption of Table 4 and in the text |
| F10 three sentences | Rewritten; the correctness contrast replaces the label comparison |
| F11 literature | Corpus reduced to one sentence in the introduction. **Open:** a targeted search on LLM-judge reliability (author) |
| F12 registry | **Open** (item 5 below) |
| F13, F14 | Distinct instances stated; decision rule stated in the methods |

**Open before submission**

1. Note to the editor: Paper D is in the same issue; earlier reliability tables are public
   in the 32-page edition and the thesis. Not drafted.
2. Author decision: whether the human subset is in this submission (recommendation: no).
   The rating sheets in `human_subset/` show the clean record. At 15 pages, a human-subset
   section needs an equal cut.
3. Raters, only if item 2 is yes: send the two rating sheets (`human_subset/README.md`);
   cut-off 2026-10-10.
4. Second reviewer: adjudication sheet in `corpus_audit/`; cut-off 2026-10-08.
5. Registry: put `paper_c.tex` under `[coverage]`, add `docs/reports/paper_c/` to the
   protected side of `[exclusivity]`, wire `verify_sync.py`, replace the placeholder abstract
   in `pub/claims.toml` (shared files, through `main`). Not done: the numbers of the draft
   are generated from result files but are not yet in `pub/claim_registry.toml`.
6. Independent rigor review. Done 2026-10-04: Zenodo version 0.10.0,
   `10.5281/zenodo.23149419`, from GitHub release `paper-c-tm-2026-10-04` (`main` at
   `d97dbe188`); the full version cites it. A later change to code or results needs a new
   version; a text change does not.
7. Done 2026-10-04: the author read the draft and checked the two added references.

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
| `references.bib` | IEEE references; the two entries added for this paper were checked by the author |
| `scripts/paper_c_posthoc.py` | Judge scores against the metrics shown in the prompt (plan section 7) |
| `scripts/paper_c_reliability.py` | Analyses added after the rigor review: agreement inside each explainer, one call, panel mean, two-way models, F-based intervals, raw agreement, use of the printed metrics, clean condition (plan section 15) |
| `scripts/run_clean_condition.py` | Runs the clean condition: 192 cases, 3 judges, one call, no metrics, outcome or label in the prompt |
| `clean_condition/` | The clean condition, a new cohort (RCA-002): rendered prompts, raw responses, parsed scores |
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
.venv/Scripts/python.exe docs/reports/paper_c/scripts/paper_c_reliability.py   # before the summary: the figure reads its output
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
