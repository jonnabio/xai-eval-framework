# Publication Sync Pipeline (Thesis + Papers)

This document defines the **standard publication workflow** to ensure that new
results, findings, and manuscript edits propagate consistently into:

- Thesis (Quarto → Word `.docx`) under `thesis/`
- Paper A/B/C sources under `docs/reports/paper_{a,b,c}/`

The goal is to prevent “content drift” (e.g., a finding updated in the thesis but
not in Paper B) and to eliminate stale-build regressions (e.g., DOCX renders
showing old summaries).

## 1) Source of Truth (SSOT)

### 1.1 Claims registry

`pub/claims.toml` is the **single source of truth** for:

- Thesis title + Resumen/Abstract
- Thesis keywords (ES/EN)
- Paper A/B/C abstract + keywords (LaTeX)

Edits to abstracts/keywords must be made **only** in `pub/claims.toml`.

### 1.2 Generated fragments

`scripts/pubs/generate_fragments.py` generates synchronized manuscript fragments
into `pub/fragments/`.

These fragments are treated as *build artifacts with traceability* and are
consumed by thesis/papers via include mechanisms (see below).

## 2) Wiring (How content propagates)

### 2.1 Thesis (Quarto book → DOCX)

`thesis/index.qmd` includes generated fragments:

- `pub/fragments/thesis_resumen_es.qmd`
- `pub/fragments/thesis_palabras_clave_es.qmd`
- `pub/fragments/thesis_abstract_en.qmd`
- `pub/fragments/thesis_keywords_en.qmd`

This makes `thesis/index.qmd` a **consumer** of the SSOT, not an independent
authoritative source for summaries/keywords.

### 2.2 Papers A/B/C (LaTeX)

Each paper’s JMLR LaTeX source consumes fragments via `\input{...}`:

- Paper A: `docs/reports/paper_a/paper_a_prototype_jmlr.tex`
  - `pub/fragments/paper_a_abstract_en.tex`
  - `pub/fragments/paper_a_keywords_en.tex`
- Paper B: `docs/reports/paper_b/paper_b_prototype_jmlr.tex`
  - `pub/fragments/paper_b_abstract_en.tex`
  - `pub/fragments/paper_b_keywords_en.tex`
- Paper C: `docs/reports/paper_c/paper_c_prototype_jmlr.tex`
  - `pub/fragments/paper_c_abstract_en.tex`
  - `pub/fragments/paper_c_keywords_en.tex`

## 3) Build commands (single entrypoint)

### 3.1 Windows (PowerShell)

Run everything:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/pubs/build_all.ps1
```

### 3.2 WSL/Linux/macOS (bash)

```bash
scripts/pubs/build_all.sh
```

What the build does:

1. Generate fragments from `pub/claims.toml`
2. Verify thesis/papers are wired to fragments
3. Render thesis DOCX (if `quarto` is installed and available)

## 4) Verification gates (how drift is prevented)

### 4.1 Wiring verification

`scripts/pubs/verify_sync.py` fails the build if:

- Thesis no longer includes the fragments
- Paper A/B/C no longer `\input{...}` the fragments
- Expected fragments are missing from `pub/fragments/`

### 4.2 CI enforcement

GitHub Actions workflow `.github/workflows/pubs-sync.yml` regenerates fragments
and fails if `pub/fragments/` differs from what is committed. This prevents PRs
from changing the SSOT without updating generated artifacts.

## 5) Operational caveats / troubleshooting

### 5.1 Word file locking

Word can lock the output `.docx`, causing Quarto to silently keep an older file
or fail to overwrite it.

Standard practice:

- Close the thesis `.docx` before running `thesis/render.ps1` or `build_all.ps1`.

### 5.2 Stale renders

If the generated DOCX shows old content:

- Ensure you ran the build from the thesis project directory
- Ensure caches were cleared (`thesis/render.ps1` performs a defensive clean)

## 6) Policy (what to edit where)

- Update abstracts/keywords: edit `pub/claims.toml`, then regenerate fragments.
- Do not edit abstracts/keywords directly in:
  - `thesis/index.qmd` (it includes fragments)
  - `docs/reports/paper_*/paper_*_prototype_jmlr.tex` (they `\input` fragments)

