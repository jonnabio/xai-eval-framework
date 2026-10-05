# Paper C: LLM judges as evaluators of explanations

**Scope:** the LLM-judge reliability study (EXP4, two judge panels on the same 192 cases),
with the taxonomy and the 44-paper scoping corpus as framing (ADR-0022).

**Target:** *Tecnología en Marcha*, special issue on Artificial Intelligence, 2027 edition.
Deadline 2026-10-15, by email to revistatm@tec.ac.cr.

**Status (2026-10-04):** folder rebuilt; plan proposed in `PLAN.md`, waiting for the author's
approval. No manuscript and no new analysis yet.

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
| `PLAN.md` | Scope, venue rules, page budget, work packages, pre-specified analyses, schedule |
| `paper_c_review_corpus.csv` | The 44-paper coded corpus. Copied from `docs/reports/paper_bc/paper_bc_review_corpus.csv` on 2026-10-04; this copy is the working file |
| `corpus_audit/` | Second-reviewer audit (plan, template, results, summary) and the adjudication sheet with 28 open disagreements. Copied from `docs/reports/paper_bc/` on 2026-10-04; these copies are the working files |

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
