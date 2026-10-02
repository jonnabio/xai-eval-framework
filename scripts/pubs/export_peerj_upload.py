#!/usr/bin/env python3
"""Export the separate figure and table files PeerJ asks for at upload.

PeerJ wants each figure and table uploaded as its own file, named in order of
first appearance (Figure1.pdf, Table1.tex, ...). This script derives them from
docs/reports/paper_bc/paper_bc_peerjcs.tex, so they cannot drift from the
manuscript:

- figures embedded with \\includegraphics are copied from figures/;
- TikZ figures are compiled to a standalone PDF with Tectonic;
- each table environment is written to its own compilable .tex file.

    python scripts/pubs/export_peerj_upload.py

Output: docs/reports/paper_bc/peerj_upload/ (rebuilt from scratch each run).
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BC = ROOT / "docs" / "reports" / "paper_bc"
SRC = BC / "paper_bc_peerjcs.tex"
OUT = BC / "peerj_upload"
TECTONIC = ROOT / "tools" / "tectonic-portable" / ("tectonic.exe" if sys.platform == "win32" else "tectonic")

FLOAT = re.compile(r"\\begin\{(figure|table)\}.*?\\end\{\1\}", re.DOTALL)
GRAPHIC = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
TIKZ = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.DOTALL)
REF = re.compile(r"\\ref\{([^}]+)\}")
NEWLABEL = re.compile(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}")
CITE = re.compile(r"\\cite([pt]?)\{([^}]+)\}")
BIBITEM = re.compile(r"\\bibitem\[(.+?)\((\d{4}[a-z]?)\)[^\]]*\]\{([^}]+)\}", re.DOTALL)

STANDALONE = r"""\documentclass[border=4pt]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{tikz}
\usetikzlibrary{positioning,calc,arrows.meta}
\begin{document}
%s
\end{document}
"""

TABLE_DOC = r"""%% %s of paper_bc_peerjcs.tex, exported for PeerJ upload by
%% scripts/pubs/export_peerj_upload.py. Do not edit: edit the manuscript and re-export.
\documentclass[10pt]{article}
\usepackage[letterpaper,margin=25mm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{multirow}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage[authoryear,round]{natbib}
\begin{document}
%s
\end{document}
"""


def _resolve_citations(block: str, refs: dict[str, tuple[str, str]]) -> str:
    """A standalone table has no bibliography, so write citations as plain author-year text."""
    def one(m: re.Match) -> str:
        cites = [refs[k.strip()] for k in m.group(2).split(",")]
        if m.group(1) == "t":
            return "; ".join(f"{a} ({y})" for a, y in cites)
        return "(" + "; ".join(f"{a}, {y}" for a, y in cites) + ")"
    return CITE.sub(one, block)


def _labels() -> dict[str, str]:
    """Label -> printed number, from a fresh build of the manuscript's .aux file."""
    subprocess.run([str(TECTONIC), "-X", "compile", "--keep-intermediates", SRC.name],
                   cwd=BC, check=True, capture_output=True)
    aux = (BC / SRC.with_suffix(".aux").name).read_text(encoding="utf-8", errors="ignore")
    return dict(NEWLABEL.findall(aux))


def main() -> int:
    tex = SRC.read_text(encoding="utf-8")
    refs = {key: (" ".join(author.split()), year) for author, year, key in BIBITEM.findall(tex)}
    labels = _labels()
    body = tex[tex.index(r"\begin{document}"):]
    # Empty the folder rather than removing it: on Windows a shell or Explorer window
    # open in it would block the removal.
    OUT.mkdir(exist_ok=True)
    for old in OUT.iterdir():
        shutil.rmtree(old) if old.is_dir() else old.unlink()

    n_fig = n_tab = 0
    for m in FLOAT.finditer(body):
        kind, block = m.group(1), m.group(0)
        if kind == "figure":
            n_fig += 1
            g = GRAPHIC.search(block)
            if g:
                src = BC / g.group(1)
                shutil.copyfile(src, OUT / f"Figure{n_fig}{src.suffix}")
            else:
                t = TIKZ.search(block)
                if not t:
                    raise SystemExit(f"Figure {n_fig}: no graphic and no tikzpicture")
                stub = OUT / f"Figure{n_fig}.tex"
                stub.write_text(STANDALONE % t.group(0), encoding="utf-8")
                subprocess.run([str(TECTONIC), "-X", "compile", stub.name], cwd=OUT,
                               check=True, capture_output=True)
                stub.unlink()
        else:
            n_tab += 1
            # Keep the caption: PeerJ requires a title for every table.
            block = _resolve_citations(block, refs)
            # Cross-references to sections and other floats: print the manuscript's number.
            block = REF.sub(lambda r: labels[r.group(1)], block)
            block = re.sub(r"\\label\{[^}]*\}", "", block)
            (OUT / f"Table{n_tab}.tex").write_text(TABLE_DOC % (f"Table {n_tab}", block),
                                                   encoding="utf-8", newline="\n")

    print(f"exported {n_fig} figures and {n_tab} tables to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
