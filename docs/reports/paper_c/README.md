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
and has not been reviewed again. That draft was archived as Zenodo 0.10.0; **not submitted**.

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

**Second review (2026-10-04, a session that did not write the draft):**
`docs/review/scientific-rigor-review_paper_c_2026-10-04_r2.md`. All recomputed values equal
the draft. Two major findings, both answered with files already committed and no judge call:

- N01: the agreement among LIME cases comes from 5 of the 32 records whose ten weights are
  all zero; without them the coefficients are between -0.13 and 0.33.
- N02: among SHAP cases the judges gave almost the same score to every case (same score in
  83% of pairs for completeness); the low coefficient is not shown to be disagreement.

Five minor findings (N03 to N07) are clauses.

**Third draft (2026-10-04), revised after the second review.** The author accepted the
analysis and decided that the five records stay (`PLAN.md`, section 16). N01 to N07 are
answered in the abstract, resumen, methods, sections 3.2 and 3.5, discussion, limitations
and conclusions; one sentence and two references on LLM judges were added to the
introduction. **15 pages in Word**, abstract 248 words, resumen 250, 27 references. The
revision was made by the session that wrote the second review and has not been reviewed
again. The author read it and checked the two references marked "NEW 2" (2026-10-04).

**Archive:** Zenodo version 0.11.0, `10.5281/zenodo.23150204`, from GitHub release
`paper-c-tm-2026-10-04-r2` (`main` at `ae4fcd890`). It holds the analysis code and result
files of `PLAN.md` section 16; the full version cites it. Version 0.10.0 does not hold them.

**Open before submission**

0. Author: the last revision of the manuscript. After any change to the template, build,
   then register (section Build); the registration changes shared files and goes through
   a `pubs/*` branch.
1. Note to the editor: `EDITOR_NOTE.md` (Spanish to send, English for the record). Not
   sent. Its items 1 to 3 were checked against the registry and corrected on 2026-10-04.
   Left for the author: whether the thesis is still not deposited, and the telephone number.
2. **Decided 2026-10-04 (author): the human subset is not part of this submission.** The
   manuscript already says it has no human scores and names the comparison as future work.
   The sample and the rating sheets stay in `human_subset/`, not sent, for a later study.
3. Not needed: no rating sheet is sent (item 2).
4. Second reviewer: adjudication sheet in `corpus_audit/`; cut-off 2026-10-08.
5. Registry: **done 2026-10-04** (pull request #27, `pubs/paper-c-registry`).
   `scripts/pubs/register_paper_c.py` writes the Paper C block of
   `pub/claim_registry.toml`: 162 claims of this paper's own and 37 sites on quantities
   that the thesis or the 32-page edition already carries. `paper_c.tex` is under
   `[coverage]`, this folder is on the protected side of `[exclusivity]`, the abstract,
   keywords, resumen and palabras clave are in `pub/claims.toml`, and `verify_sync.py`
   compares them with the manuscript. CI runs `register_paper_c.py --check`, which also
   fails when `paper_c.tex` is not the template rendered from the result files.
   Found while triaging: the two quotations of an Anchors and a DiCE record in the
   methods omit an item of the stored text without marking it (after `capital-gain:
   1.0000` the records have a third weight of 1.0000; after `age: 1.6182` the record has
   `education_9th: 0.4000`). For the author's last revision.
6. Literature on LLM-judge reliability (F11): candidates in
   `LITERATURE_LLM_JUDGE_RELIABILITY.md`. XAI-Arena (arXiv:2609.09428, September 2026) uses
   an LLM judge on SHAP, LIME and DiCE explanations; it and Haldar and Hockenmaier (2025)
   are now cited in the introduction. The other candidates are not used.
   Done 2026-10-04: Zenodo version 0.10.0,
   `10.5281/zenodo.23149419`, from GitHub release `paper-c-tm-2026-10-04` (`main` at
   `d97dbe188`); superseded by version 0.11.0 (above). A later change to code or results needs a new
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
python scripts/pubs/register_paper_c.py                                    # registry block and abstract; shared files, on a pubs/* branch
python scripts/pubs/generate_fragments.py                                  # then restore pub/fragments/build_meta.env
```

`python scripts/pubs/register_paper_c.py --check` writes nothing and says whether the
registration is current. It is needed after a change to a printed number or to the
abstract, keywords, resumen or palabras clave; a change to other text needs only the build.

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
