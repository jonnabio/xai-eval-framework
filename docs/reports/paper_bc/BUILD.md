# Paper BC PDF Build

Target venue: **TMLR** (Transactions on Machine Learning Research). This
directory is self-contained for PDF compilation: it carries the official TMLR
style files (`tmlr.sty`, `fancyhdr.sty`, from
<https://github.com/JmlrOrg/tmlr-style-file>) and uses the repository's
portable Tectonic binary by default.

The manuscript files are `paper_bc_tmlr.tex` and
`paper_bc_tmlr_supplementary.tex`, renamed from `paper_bc_jmlr*` on 2026-09-05
when the target venue was settled. Both `scripts/pubs/verify_sync.py` and
`pub/claim_registry.toml` address them by path, so the rename was a single
substrate commit that also updated both regression guards.

Dated records deliberately keep the old name: the 2026-07-28 rigor review, the
2026-08-22 alignment review, the dated remediation plans and the
`ACTIVE_CONTEXT.md` session narratives describe the file as it was then called.

## Anonymity

Review is double-blind. `tmlr.sty` handles this: loaded plain, it prints
"Anonymous authors / Paper under double-blind review" and the running head
"Under review as submission to TMLR", and the `\author{...}` block in the
source is simply not typeset.

**Do not de-anonymise by hand.** Flip the package option and the rest follows,
because identity-revealing content is guarded by `\ifdeanon`, which is defined
in terms of that option:

| Build | Preamble line | Effect |
| ----- | ------------- | ------ |
| Submission (default) | `\usepackage{tmlr}` | anonymous; acknowledgments suppressed; repository cited as an anonymised mirror |
| Camera-ready | `\usepackage[accepted]{tmlr}` | authors, acknowledgments and the real repository URL restored |
| Preprint / arXiv | `\usepackage[preprint]{tmlr}` | as accepted, without the TMLR running head |

Two blocks are guarded today: the `\acks{...}` funding and competing-interests
statement, and the GitHub URL in §Code and Artifact Availability.

**Before submitting, replace the anonymised-mirror wording with a real
anonymous artifact link** (for example anonymous.4open.science). Reviewers
otherwise have no way to reach the code, and the abstract promises that all
experimental artifacts are publicly available.

Set `\month` and `\year`, and point `\openreview` at the forum URL, only for
the camera-ready build.

## Build Both PDFs

From `docs/reports/paper_bc`:

```bash
make all
```

This produces:

- `paper_bc_tmlr.pdf` (main manuscript)
- `paper_bc_tmlr_supplementary.pdf` (six supplementary tables)

## Build One PDF

```bash
make main
make supplement
```

## Direct Tectonic Commands

From the repository root:

```bash
./tools/tectonic-portable/tectonic docs/reports/paper_bc/paper_bc_tmlr.tex
./tools/tectonic-portable/tectonic docs/reports/paper_bc/paper_bc_tmlr_supplementary.tex
```

On Windows PowerShell, use:

```powershell
.\tools\tectonic-portable\tectonic.exe .\docs\reports\paper_bc\paper_bc_tmlr.tex
.\tools\tectonic-portable\tectonic.exe .\docs\reports\paper_bc\paper_bc_tmlr_supplementary.tex
```

## Notes

- No BibTeX step is required: references are embedded as a `thebibliography`
  environment, so `tmlr.bst` is not needed and is not vendored.
- The main manuscript uses local figures under `figures/`.
- The second-reviewer audit CSV is a data artifact, not a LaTeX input.
- `tools/tectonic-portable/` is gitignored, so a fresh `git worktree` will not
  have it; copy the binary in before building there. Copy `tectonic.exe`
  explicitly — Git Bash resolves `tectonic` to `tectonic.exe` on Windows and
  will silently overwrite one with the other.
- `jmlr2e.sty` is kept only as the record of the previous format; nothing in
  this directory loads it any more.
