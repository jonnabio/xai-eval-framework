# Paper BC PDF Build

Target venue: **TMLR** (Transactions on Machine Learning Research). This
directory is self-contained for PDF compilation: it carries the official TMLR
style files (`tmlr.sty`, `fancyhdr.sty`, from
<https://github.com/JmlrOrg/tmlr-style-file>) and uses the repository's
portable Tectonic binary by default.

The filenames keep the `_jmlr` suffix on purpose. TMLR is published by the
JMLR organisation, and both `scripts/pubs/verify_sync.py` and
`pub/claim_registry.toml` address the manuscript by path; renaming it would be
a substrate change touching two regression guards for no reader-visible gain.

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

- `paper_bc_jmlr.pdf` (main manuscript)
- `paper_bc_jmlr_supplementary.pdf` (six supplementary tables)

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
