# 11. Publication Sync Pipeline (SSOT + Fragments)

Date: 2026-04-23
Status: Accepted

## Context

The repository maintains multiple publication surfaces that must remain
consistent:

- Thesis rendered to Word (`thesis/` Quarto book → `.docx`)
- Three papers under `docs/reports/paper_{a,b,c}/` (LaTeX sources + PDFs)

Historically, summaries, keywords, and high-level findings were duplicated across
these surfaces, which created two recurring problems:

1. **Drift**: changes made in one manuscript were not propagated to the others.
2. **Stale renders**: Quarto builds could surface outdated content due to cached
   artifacts or output filename mismatches, causing confusion and regressions.

We need a workflow that guarantees propagation and fails fast when outputs are
out of sync.

## Decision

Adopt a **single source of truth (SSOT)** for thesis and paper abstracts/keywords
and generate **reusable fragments** consumed by all manuscripts.

### SSOT

- `pub/claims.toml` becomes the SSOT for:
  - Thesis title, Resumen/Abstract, ES/EN keywords
  - Paper A/B/C abstract + keywords (LaTeX)

### Generated fragments

- `scripts/pubs/generate_fragments.py` generates `pub/fragments/*`.
- Thesis and papers consume fragments via include mechanisms:
  - `thesis/index.qmd` includes `pub/fragments/thesis_*.qmd`
  - Paper A/B/C `paper_*_prototype_jmlr.tex` uses `\input{...}` for
    `pub/fragments/paper_*_*.tex`

### Verification gate

- `scripts/pubs/verify_sync.py` fails if any paper/thesis stops consuming
  fragments or if fragments are missing.
- CI workflow `.github/workflows/pubs-sync.yml` regenerates fragments and fails
  if `pub/fragments/` is not up to date.

## Consequences

### Positive

- A change to abstracts/keywords is made once and propagates everywhere.
- CI prevents “merge drift” by failing when fragments are stale.
- Quarto/Paper builds become more reproducible by removing duplicated narrative
  sources.

### Negative

- Authors must learn and follow the SSOT rule (edit `pub/claims.toml` rather than
  editing LaTeX/Quarto sections directly).
- Generated fragments are committed, which adds a small maintenance step (run
  generator before committing). CI enforces this to keep it reliable.

