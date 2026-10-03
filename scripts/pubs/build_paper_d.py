#!/usr/bin/env python3
"""Build Paper D for Tecnologia en Marcha: PDFs, Word files and figure uploads.

The journal accepts a Microsoft Word document (letter, one column, Times 12 pt,
1.5 line spacing, equations made with Word's equation editor) and wants each
image also as a separate file (.jpg, .tiff, .eps, .psd or .ai). The source of
truth is docs/reports/paper_d/paper_d.tex; this script derives everything else:

    submission/paper_d_blind.pdf    review build, author identity omitted
    submission/paper_d_full.pdf     with the author block and repository links
    submission/paper_d_blind.docx   the manuscript to send (Word, native equations)
    submission/paper_d_full.docx    the same with author data, for the editor
    submission/Figure1-3.tiff       separate image files, 300 ppi

    python scripts/pubs/build_paper_d.py

Run scripts/generate_paper_d_figures.py first if a figure changed.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "docs" / "reports" / "paper_d"
OUT = D / "submission"
TECTONIC = ROOT / "tools" / "tectonic-portable" / ("tectonic.exe" if sys.platform == "win32" else "tectonic")
FIGURES = ["fig1_architecture", "fig2_registry_growth", "fig3_incident_classes"]


def _run(cmd: list[str], cwd: Path) -> None:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        sys.exit(f"failed: {' '.join(cmd)}\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")


def _variant(tex: str, full: bool) -> str:
    """Resolve the \\iffull ... \\else ... \\fi blocks, for pandoc (it does not evaluate them)."""
    # Only blocks whose \iffull, \else and \fi stand on lines of their own; the
    # preamble's \newif\iffull and \ifdefined lines are left alone (pandoc skips them).
    pat = re.compile(r"^\\iffull\n(.*?)^\\else\n(.*?)^\\fi\n", re.DOTALL | re.MULTILINE)
    out, n = pat.subn(lambda m: m.group(1) if full else m.group(2), tex)
    if n != 2:
        sys.exit(f"expected 2 \\iffull blocks (author, data availability), found {n}")
    return out


def build_pdf(full: bool) -> Path:
    name = "paper_d_full" if full else "paper_d_blind"
    src = D / f"{name}.tex"
    src.write_text(("\\def\\fullversion{}\n" if full else "") + "\\input{paper_d}\n", encoding="utf-8")
    _run([str(TECTONIC), "-X", "compile", "--keep-logs", src.name], D)
    log = (D / f"{name}.log").read_text(encoding="utf-8", errors="ignore")
    bad = [l for l in log.splitlines() if re.search(r"undefined|Citation .* undefined", l)]
    if bad:
        sys.exit(f"{name}: unresolved references:\n" + "\n".join(bad[:10]))
    pdf = OUT / f"{name}.pdf"
    shutil.move(str(D / f"{name}.pdf"), pdf)
    src.unlink()
    for ext in (".log",):
        (D / f"{name}{ext}").unlink(missing_ok=True)
    return pdf


def reference_docx() -> Path:
    """Pandoc's default reference.docx restyled to the journal's format."""
    ref = OUT / "_reference.docx"
    src = D / "reference_default.docx"
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(ref, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                x = data.decode("utf-8")
                # Times New Roman everywhere, 12 pt (24 half-points), 1.5 line spacing.
                x = re.sub(r'w:ascii="[^"]*"', 'w:ascii="Times New Roman"', x)
                x = re.sub(r'w:hAnsi="[^"]*"', 'w:hAnsi="Times New Roman"', x)
                x = re.sub(r'w:eastAsia="[^"]*"', 'w:eastAsia="Times New Roman"', x)
                x = re.sub(r'w:cs="[^"]*"', 'w:cs="Times New Roman"', x)
                x = re.sub(r'w:asciiTheme="[^"]*"\s*', "", x)
                x = re.sub(r'w:hAnsiTheme="[^"]*"\s*', "", x)
                x = re.sub(r'w:eastAsiaTheme="[^"]*"\s*', "", x)
                x = re.sub(r'w:cstheme="[^"]*"\s*', "", x)
                x = re.sub(r'<w:sz w:val="\d+"\s*/>', '<w:sz w:val="24"/>', x)
                x = re.sub(r'<w:szCs w:val="\d+"\s*/>', '<w:szCs w:val="24"/>', x)
                x = re.sub(r'<w:spacing ([^/]*?)w:line="\d+"', r'<w:spacing \1w:line="360"', x)
                x = x.replace("<w:pPrDefault><w:pPr>",
                              '<w:pPrDefault><w:pPr><w:spacing w:line="360" w:lineRule="auto"/>', 1) \
                    if 'w:line="360"' not in x else x
                data = x.encode("utf-8")
            if item.filename == "word/document.xml":
                x = data.decode("utf-8")
                # US Letter: 12240 x 15840 twips; 2.5 cm margins = 1418 twips.
                x = re.sub(r'<w:pgSz [^>]*/>', '<w:pgSz w:w="12240" w:h="15840"/>', x)
                x = re.sub(r'<w:pgMar [^>]*/>', '<w:pgMar w:top="1418" w:right="1418" w:bottom="1418" '
                           'w:left="1418" w:header="720" w:footer="720" w:gutter="0"/>', x)
                data = x.encode("utf-8")
            zout.writestr(item, data)
    return ref


TIMES = ('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
         'w:eastAsia="Times New Roman" w:cs="Times New Roman"/>')
# US Letter (12240 x 15840 twips), 2.5 cm margins (1418 twips).
SECT = ('<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1418" w:right="1418" '
        'w:bottom="1418" w:left="1418" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>')


def enforce_format(docx: Path) -> None:
    """Set the journal's format in the finished file: Times New Roman 12 pt, 1.5 line
    spacing (line=360, auto) in every paragraph style, letter paper, 2.5 cm margins."""
    tmp = docx.with_suffix(".tmp")
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                x = data.decode("utf-8")
                x = re.sub(r"<w:rFonts\b[^>]*/>", TIMES, x)
                x = re.sub(r'<w:sz w:val="\d+"\s*/>', '<w:sz w:val="24"/>', x)
                x = re.sub(r'<w:szCs w:val="\d+"\s*/>', '<w:szCs w:val="24"/>', x)
                # Line spacing: rewrite every existing spacing element, then make sure
                # the document default carries one.
                x = re.sub(r"<w:spacing\b([^>]*?)\s*/>",
                           lambda m: "<w:spacing" + re.sub(r'\s*w:(line|lineRule)="[^"]*"', "", m.group(1))
                           + ' w:line="360" w:lineRule="auto"/>', x)
                x = re.sub(r"(<w:pPrDefault>\s*<w:pPr>)(?![\s\S]{0,80}w:line=)",
                           r'\1<w:spacing w:line="360" w:lineRule="auto"/>', x)
                # Paragraph gaps: pandoc's 9 pt before and after body paragraphs is not
                # part of the journal's format; use 0 before and 5 pt (100) after.
                x = re.sub(r'(<w:style [^>]*w:styleId="(?:BodyText|FirstParagraph|Compact)"[\s\S]*?)'
                           r'<w:spacing\b[^>]*/>',
                           r'\1<w:spacing w:before="0" w:after="100" w:line="360" w:lineRule="auto"/>', x)
                # Table cells (Compact): no gap after each cell paragraph.
                x = re.sub(r'(<w:style [^>]*w:styleId="Compact"[\s\S]*?)<w:spacing\b[^>]*/>',
                           r'\1<w:spacing w:before="0" w:after="0" w:line="360" w:lineRule="auto"/>', x)
                x = re.sub(r'(<w:pPrDefault>\s*<w:pPr>\s*)<w:spacing\b[^>]*/>',
                           r'\1<w:spacing w:before="0" w:after="100" w:line="360" w:lineRule="auto"/>', x)
                data = x.encode("utf-8")
            if item.filename == "word/document.xml":
                x = data.decode("utf-8")
                x = re.sub(r"<w:sectPr\b[\s\S]*?</w:sectPr>", "", x)
                x = x.replace("</w:body>", SECT + "</w:body>")
                data = x.encode("utf-8")
            zout.writestr(item, data)
    tmp.replace(docx)


def build_docx(full: bool, ref: Path) -> Path:
    name = "paper_d_full" if full else "paper_d_blind"
    tmp = D / f"_{name}_pandoc.tex"
    tmp.write_text(_variant((D / "paper_d.tex").read_text(encoding="utf-8"), full), encoding="utf-8")
    out = OUT / f"{name}.docx"
    _run(["quarto", "pandoc", tmp.name, "-o", str(out), "--citeproc",
          "--bibliography", "references.bib", "--csl", "ieee.csl",
          f"--reference-doc={ref}", "--default-image-extension=png",
          "--resource-path=.", "-f", "latex", "-t", "docx"], D)
    tmp.unlink()
    enforce_format(out)
    return out


def main() -> int:
    OUT.mkdir(exist_ok=True)
    for full in (False, True):
        print("pdf ", build_pdf(full).relative_to(ROOT))
    ref = reference_docx()
    for full in (False, True):
        print("docx", build_docx(full, ref).relative_to(ROOT))
    ref.unlink()
    for i, fig in enumerate(FIGURES, 1):
        shutil.copyfile(D / "figures" / f"{fig}.tiff", OUT / f"Figure{i}.tiff")
        print("fig ", (OUT / f"Figure{i}.tiff").relative_to(ROOT))
    # Auxiliary files Tectonic and BibTeX leave when --keep-logs is used.
    for pattern in ("paper_d*.aux", "paper_d*.blg", "paper_d*.bbl"):
        for p in D.glob(pattern):
            p.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
