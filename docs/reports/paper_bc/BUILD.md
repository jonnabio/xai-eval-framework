# Paper BC PDF Build

This directory is self-contained for PDF compilation. It includes the local
JMLR style file (`jmlr2e.sty`) and uses the repository's portable Tectonic
binary by default.

## Build Both PDFs

From `docs/reports/paper_bc`:

```bash
make all
```

This produces:

- `paper_bc_jmlr.pdf`
- `paper_bc_jmlr_supplementary.pdf`

## Build One PDF

```bash
make main
make supplement
```

## Direct Tectonic Commands

From the repository root:

```bash
./tools/tectonic-portable/tectonic docs/reports/paper_bc/paper_bc_jmlr.tex
./tools/tectonic-portable/tectonic docs/reports/paper_bc/paper_bc_jmlr_supplementary.tex
```

On Windows PowerShell, use:

```powershell
.\tools\tectonic-portable\tectonic.exe .\docs\reports\paper_bc\paper_bc_jmlr.tex
.\tools\tectonic-portable\tectonic.exe .\docs\reports\paper_bc\paper_bc_jmlr_supplementary.tex
```

## Notes

- No BibTeX step is required because references are embedded in the manuscript.
- The main manuscript uses local figures under `figures/`.
- The second-reviewer audit CSV is a data artifact, not a LaTeX input.
