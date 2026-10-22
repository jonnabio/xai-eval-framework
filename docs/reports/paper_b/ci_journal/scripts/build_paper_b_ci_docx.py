#!/usr/bin/env python3
"""Paper B in the Word templates of Computers and Informatics (C&I, DergiPark).

    python docs/reports/paper_b/ci_journal/scripts/build_paper_b_ci_docx.py [--no-pdf]

Reads paper_b_ci.tex and writes, to submission/:

    paper_b_ci_manuscript.docx, paper_b_ci_manuscript.pdf   the manuscript, masked for review
                                                            (the journal accepts .doc/.docx only;
                                                            the PDF is for checking)
    paper_b_ci_title_page.docx                              the journal's title page, with the
                                                            author data and the acknowledgment
    paper_b_ci_cover_letter.docx                            the journal's cover letter

The journal's files (journal_files/, downloaded from its site and not redistributed here; see
CI_SUBMISSION.md) are the packages: their styles, headers, footers and settings are kept, and
only the text is replaced.

How the manuscript is made:
1. The title block is the template's own (title, dates, abstract, keywords, licence line,
   "cite this paper as"); the author table is replaced by a note, since review is masked.
2. The text from the Introduction on is converted by pandoc (through Quarto), which gives
   native Word equations, tables and figures. Sections, tables, figures, equations and
   citations are numbered here, in the order of the text; the reference list is printed in
   the order of first citation, in the journal's Vancouver form.
3. The paragraphs of pandoc take the template's styles: Balk1/Balk2 for the headings
   ("1. INTRODUCTION", "1.1. Title"), Altyaz for captions, figures and table cells, the
   template's two-cell table for each numbered equation, and the template's reference
   paragraph for each entry.

Word (through COM) updates the fields, repaginates, counts the pages and prints the PDF.
Without Word the .docx files are still written; pass --no-pdf.
"""
from __future__ import annotations

import argparse
import re
import shutil
import struct
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape, unescape

ROOT = Path(__file__).resolve().parents[5]
CI = Path(__file__).resolve().parents[1]
B = CI.parent
OUT = CI / "submission"
JOURNAL = CI / "journal_files"
TEMPLATE = JOURNAL / "manuscript_template.docx"
TITLE_TEMPLATE = JOURNAL / "title_page.docx"
LETTER_TEMPLATE = JOURNAL / "cover_letter_template.docx"
SOURCE = CI / "paper_b_ci.tex"
KEYWORDS = ROOT / "pub" / "fragments" / "paper_b_keywords_en.tex"
ABSTRACT = ROOT / "pub" / "fragments" / "paper_b_abstract_en.tex"
NAME = "paper_b_ci"
TEXT_WIDTH_EMU = 5_760_000          # 16 cm between the template's 2.5 cm margins

AUTHOR = "Jonathan Herrera-V\u00e1squez"
AFFILIATION = ("Universidad Americana de Europa (UNADE), Department of Computer Science, "
               "Canc\u00fan, Quintana Roo, Mexico")
EMAIL = "jonnabio@gmail.com"
ORCID = "0000-0002-7149-6635"
RUNNING_HEAD = "SHAP versus LIME on a paired tabular benchmark"
REPOSITORY = "https://github.com/jonnabio/xai-eval-framework"
ARCHIVE = "https://doi.org/10.5281/zenodo.23147228"
ACKNOWLEDGMENT = ("The author thanks Miguel Herrero Uceda, PhD, for his revision of this "
                  "manuscript and for his constructive comments during its development. No "
                  "external funding was received for this study.")
MASKED_NOTE = "Author information is given on the separate title page (masked review)."
# Words that must not appear in the masked manuscript. The self-citation of reference 10 names
# its authors in the third person, as any citation does, and is not a leak.
LEAKS = ("Jonathan", "jonnabio", EMAIL, ORCID, "UNADE", "Universidad Americana", "github",
         "zenodo", "Canc\u00fan", "Acknowledg")


def run(cmd: list[str], cwd: Path) -> None:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode:
        sys.exit(f"{cmd[0]} failed:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")


# --- LaTeX side -------------------------------------------------------------------

def strip_comments(tex: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", tex)


def title_of(tex: str) -> str:
    return " ".join(re.search(r"\\title\{(.*?)\}\n", tex, flags=re.DOTALL).group(1).split())


def references(tex: str, body: str) -> list[tuple[str, str]]:
    """(key, LaTeX text) of every entry, in the order of first citation in the body."""
    bib = re.search(r"\\begin\{thebibliography\}\{\d+\}(.*?)\\end\{thebibliography\}", tex,
                    flags=re.DOTALL).group(1)
    entries = {k: " ".join(t.split()) for k, t in
               re.findall(r"\\bibitem\{([^}]+)\}(.*?)(?=\\bibitem\{|\Z)", bib, flags=re.DOTALL)}
    order: list[str] = []
    for group in re.findall(r"\\cite\{([^}]*)\}", body):
        for k in (k.strip() for k in group.split(",")):
            if k not in entries:
                sys.exit(f"cited but not in the reference list: {k}")
            if k not in order:
                order.append(k)
    unused = set(entries) - set(order)
    if unused:
        sys.exit(f"in the reference list but never cited: {sorted(unused)}")
    return [(k, entries[k]) for k in order]


def cite_text(keys: list[str], number: dict[str, int]) -> str:
    """[1], [8, 9], [15-17]: numbers sorted, runs of three or more compressed."""
    nums = sorted(number[k] for k in keys)
    parts, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        parts.append(str(nums[i]) if j == i else
                     f"{nums[i]}, {nums[j]}" if j == i + 1 else f"{nums[i]}--{nums[j]}")
        i = j + 1
    return "[" + ", ".join(parts) + "]"


def number_sections(body: str) -> str:
    """Number the headings as the template does and resolve every \\ref{sec:...}."""
    sec = sub = 0
    labels: dict[str, str] = {}
    current = ""

    def heading(m: re.Match) -> str:
        nonlocal sec, sub, current
        kind, star, text = m.group(1), m.group(2), " ".join(m.group(3).split())
        if star:
            return f"\n\nUNNUMHEAD {text}\n\n"
        if kind == "section":
            sec, sub = sec + 1, 0
            current = str(sec)
            return f"\\section*{{{sec}. {text.upper()}}}"
        sub += 1
        current = f"{sec}.{sub}"
        return f"\\subsection*{{{sec}.{sub}. {text}}}"

    out = []
    for piece in re.split(r"(\\(?:sub)?section\*?\{[^}]*\}|\\label\{sec:[^}]+\})", body):
        m = re.fullmatch(r"\\(section|subsection)(\*?)\{([^}]*)\}", piece)
        if m:
            out.append(heading(m))
            continue
        m = re.fullmatch(r"\\label\{(sec:[^}]+)\}", piece)
        if m:
            labels[m.group(1)] = current
            continue
        out.append(piece)
    body = "".join(out)
    body = re.sub(r"\\ref\{(sec:[^}]+)\}", lambda m: labels[m.group(1)], body)
    return body


def pandoc_source(tex: str) -> tuple[str, list[tuple[str, str]], set[int], int]:
    """The text from the Introduction on, as a small LaTeX file for pandoc.

    Returns the source, the references, the numbers of the tables that span the text width
    (tabularx in the source) and the number of numbered equations.
    """
    tex = strip_comments(tex)
    body = tex[tex.index("\\section{Introduction}"):tex.index("\\begin{thebibliography}")]
    refs = references(tex, body)
    number = {key: i for i, (key, _) in enumerate(refs, 1)}
    body = re.sub(r"\\cite\{([^}]*)\}",
                  lambda m: cite_text([k.strip() for k in m.group(1).split(",")], number), body)
    body = number_sections(body)
    # Tables, figures and equations, numbered in the order of the text.
    for prefix in ("tab", "fig", "eq"):
        for i, label in enumerate(re.findall(r"\\label\{(" + prefix + r":[^}]+)\}", body), 1):
            body = body.replace(f"\\ref{{{label}}}", str(i))
    equations = len(re.findall(r"\\label\{eq:", body))
    if equations != body.count("\\begin{equation}"):
        sys.exit("every displayed equation needs its label")
    body = re.sub(r"\\label\{[^}]*\}", "", body)
    if "\\ref{" in body:
        sys.exit("a \\ref is left without a number")
    # tabularx becomes a plain tabular; its tables (by number) span the text width.
    wide: set[int] = set()
    out = []
    for piece in re.split(r"(\\begin\{tabularx\}\{[^}]*\}\{(?:[^{}]|\{[^{}]*\})*\})", body):
        m = re.match(r"\\begin\{tabularx\}\{[^}]*\}\{((?:[^{}]|\{[^{}]*\})*)\}", piece)
        if m:
            cols = len(re.findall(r"p\{[^}]*\}|[lcrX]", re.sub(r">\{[^{}]*\}", "", m.group(1))))
            piece = "\\begin{tabular}{" + "l" * cols + "}"
            wide.add(len(re.findall(r"\\begin\{table\}", "".join(out))))
        out.append(piece)
    body = "".join(out).replace("\\end{tabularx}", "\\end{tabular}")
    body = re.sub(r"\\\\\[\d+pt\]", r"\\\\", body)
    body = re.sub(r"\\begin\{(table|figure)\}\[[^\]]*\]", r"\\begin{\1}", body)
    body = re.sub(r"\\includegraphics\[[^\]]*\]\{([^}]+)\.pdf\}",
                  lambda m: "\\includegraphics{" + m.group(1) + ".png}", body)
    body += "\n\nREFHEAD REFERENCES\n\n" + "\n\n".join(
        f"REFITEM [{i}] {text}" for i, (_, text) in enumerate(refs, 1))
    return ("\\documentclass{article}\n\\usepackage{amsmath,amssymb,graphicx,booktabs,hyperref}\n"
            "\\begin{document}\n" + body + "\n\\end{document}\n"), refs, wide, equations


# --- Word side --------------------------------------------------------------------

BLOCK = re.compile(r"<w:p(?: [^>]*)?/>|<w:p(?: [^>]*)?>.*?</w:p>|<w:tbl>.*?</w:tbl>", re.DOTALL)


def text_of(xml: str) -> str:
    return "".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", xml))


def ppr(style: str = "", extra: str = "") -> str:
    inner = (f'<w:pStyle w:val="{style}"/>' if style else "") + extra
    return f"<w:pPr>{inner}</w:pPr>" if inner else ""


def set_ppr(p: str, new_ppr: str) -> str:
    p = re.sub(r"<w:pPr>.*?</w:pPr>", "", p, count=1, flags=re.DOTALL)
    return re.sub(r"^<w:p(?: [^>]*)?>", "<w:p>" + new_ppr, p, count=1)


def strip_marker(p: str, marker: str) -> str:
    return re.sub(r"(<w:t(?: [^>]*)?>)" + marker + r"\s*", r"\1", p, count=1)


def prefix_run(p: str, text: str, rpr: str = "") -> str:
    r = f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'
    if "</w:pPr>" in p:
        return p.replace("</w:pPr>", "</w:pPr>" + r, 1)
    return re.sub(r"^<w:p(?: [^>]*)?>", lambda m: m.group(0) + r, p, count=1)


def math_size(xml: str, half_points: int) -> str:
    rpr = (f'<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
           f'<w:sz w:val="{half_points}"/><w:szCs w:val="{half_points}"/></w:rPr>')
    return re.sub(r"<m:r>(<m:rPr>.*?</m:rPr>|<m:rPr\s*/>)?(?:<w:rPr>.*?</w:rPr>)?",
                  lambda m: "<m:r>" + (m.group(1) or "") + rpr, xml, flags=re.DOTALL)


def list_formats(numbering_xml: str) -> dict[str, str]:
    """numId of pandoc -> "decimal", "bullet", or "continuation" (the paragraphs that continue
    a list item, which pandoc puts in a list whose marker is empty)."""
    fmt = {}
    for a, body in re.findall(r'<w:abstractNum [^>]*w:abstractNumId="(\d+)"[^>]*>(.*?)'
                              r"</w:abstractNum>", numbering_xml, flags=re.DOTALL):
        lvl = re.search(r'<w:lvl w:ilvl="0"[^>]*>(.*?)</w:lvl>', body, flags=re.DOTALL).group(1)
        text = re.search(r'<w:lvlText w:val="([^"]*)"', lvl)
        num_fmt = re.search(r'<w:numFmt w:val="([^"]+)"', lvl).group(1)
        fmt[a] = "continuation" if num_fmt == "none" or not (text and text.group(1)) else num_fmt
    return {n: fmt[a] for n, a in re.findall(r'<w:num w:numId="(\d+)"[^>]*>\s*<w:abstractNumId '
                                             r'w:val="(\d+)"', numbering_xml)}


def restyle_table(tbl: str, example_tblpr: str, wide: bool) -> str:
    """A pandoc table with the borders of the template's example: rules above and below the
    table and under the header row, no vertical lines; cells in Altyaz, not italic."""
    rows = re.findall(r"<w:tr(?: [^>]*)?>.*?</w:tr>", tbl, flags=re.DOTALL)
    ncol = len(re.findall(r"<w:tc>", rows[0]))
    tblpr = example_tblpr
    if wide:
        tblpr = re.sub(r'<w:tblW [^>]*/>', '<w:tblW w:w="5000" w:type="pct"/>', tblpr)
    rule = '<w:{0} w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    out_rows = []
    for i, row in enumerate(rows):
        borders = (rule.format("top") if i == 0 else "") + \
                  (rule.format("bottom") if i in (0, len(rows) - 1) else "")
        tcpr = f"<w:tcPr><w:tcBorders>{borders}</w:tcBorders></w:tcPr>" if borders else ""
        row = re.sub(r"<w:trPr>.*?</w:trPr>", "", row, flags=re.DOTALL)
        row = re.sub(r"<w:tcPr>.*?</w:tcPr>|<w:tcPr\s*/>", "", row, flags=re.DOTALL)
        row = row.replace("<w:tc>", "<w:tc>" + tcpr)
        keep = "<w:keepNext/>" if i < len(rows) - 1 else ""
        row = re.sub(r"<w:p(?: [^>]*)?>.*?</w:p>", lambda m: set_ppr(m.group(0), ppr(
            "Altyaz", keep + '<w:spacing w:before="20" w:after="20"/><w:jc w:val="left"/>'
            '<w:rPr><w:i w:val="0"/><w:iCs w:val="0"/></w:rPr>')), row, flags=re.DOTALL)
        # Runs of a cell are upright (Altyaz is italic) unless pandoc made them so.
        row = re.sub(r"<w:r>(?!<w:rPr>)", '<w:r><w:rPr><w:i w:val="0"/></w:rPr>', row)
        row = re.sub(r"<w:r><w:rPr>(?!(?:(?!</w:rPr>).)*<w:i/>)", '<w:r><w:rPr><w:i w:val="0"/>',
                     row)
        out_rows.append(row)
    grid = "<w:tblGrid>" + "<w:gridCol/>" * ncol + "</w:tblGrid>"
    return math_size("<w:tbl>" + tblpr + grid + "".join(out_rows) + "</w:tbl>", 18)


def formula_table(template_formula: str, p: str, n: int) -> str:
    math = re.search(r"<m:oMathPara>.*?</m:oMathPara>", p, flags=re.DOTALL).group(0)
    out = re.sub(r"<m:oMathPara>.*?</m:oMathPara>", lambda _: math, template_formula, count=1,
                 flags=re.DOTALL)
    return out.replace("<w:t>(1)</w:t>", f"<w:t>({n})</w:t>", 1)


def scale_figures(xml: str, pngs: list[Path], widths: list[float]) -> str:
    """Each figure at the share of the text width the source gives it, in proportion."""
    parts = re.split(r"(<w:drawing>.*?</w:drawing>)", xml, flags=re.DOTALL)
    k = 0
    for i, part in enumerate(parts):
        if not part.startswith("<w:drawing>"):
            continue
        with pngs[k].open("rb") as fh:
            w, h = struct.unpack(">II", fh.read(24)[16:24])
        cx = round(TEXT_WIDTH_EMU * widths[k])
        cy = round(cx * h / w)
        part = re.sub(r'<wp:extent cx="\d+" cy="\d+"\s*/>', f'<wp:extent cx="{cx}" cy="{cy}"/>', part)
        parts[i] = re.sub(r'<a:ext cx="\d+" cy="\d+"\s*/>', f'<a:ext cx="{cx}" cy="{cy}"/>', part)
        k += 1
    if k != len(pngs):
        sys.exit(f"{k} figures in Word, {len(pngs)} in the source")
    return "".join(parts)


def convert_body(pandoc_doc: str, numbering_xml: str, template_doc: str, wide: set[int],
                 template_ref: str) -> tuple[str, int]:
    """Blocks of pandoc with the template's styles. Returns the XML and the equations found."""
    template_tables = re.findall(r"<w:tbl>.*?</w:tbl>", template_doc, flags=re.DOTALL)
    template_formula = next(t for t in template_tables if "<m:oMathPara>" in t)
    example = next(t for t in template_tables if "Item no" in text_of(t))
    example_tblpr = re.search(r"<w:tblPr>.*?</w:tblPr>", example, flags=re.DOTALL).group(0)
    ref_ppr = re.search(r"<w:pPr>.*?</w:pPr>", template_ref, flags=re.DOTALL).group(0)
    ref_rpr = re.search(r"<w:r><w:rPr>(.*?)</w:rPr>", template_ref, flags=re.DOTALL).group(1)
    formats = list_formats(numbering_xml)
    inner = pandoc_doc.split("<w:body>", 1)[1]
    inner = inner[:inner.rindex("<w:sectPr")]
    out: list[str] = []
    tables = figures = equations = 0
    counters: dict[str, int] = {}
    for b in BLOCK.findall(inner):
        if b.startswith("<w:tbl>"):
            out.append(restyle_table(b, example_tblpr, tables in wide))
            continue
        if b.endswith("/>") and not b.endswith("</w:p>"):
            continue
        style = re.search(r'<w:pStyle w:val="([^"]+)"', b)
        style = style.group(1) if style else ""
        text = text_of(b).strip()
        if text.startswith("UNNUMHEAD"):
            out.append(set_ppr(strip_marker(b, "UNNUMHEAD"), ppr("Balk3", "<w:keepNext/>")))
        elif text.startswith("REFHEAD"):
            out.append(set_ppr(strip_marker(b, "REFHEAD"), ppr("Balk1", "<w:keepNext/>")))
        elif text.startswith("REFITEM"):
            b = strip_marker(b, "REFITEM")
            b = re.sub(r"<w:r>(?:<w:rPr>(.*?)</w:rPr>)?",
                       lambda m: "<w:r><w:rPr>" + ref_rpr + (m.group(1) or "") + "</w:rPr>", b,
                       flags=re.DOTALL)
            # Left-aligned: justified, the long DOIs and URLs open wide gaps in the line.
            out.append(set_ppr(b, ref_ppr.replace('<w:pStyle w:val="Default"/>',
                                                  '<w:pStyle w:val="Default"/><w:spacing w:after="60"/>')
                               .replace('<w:jc w:val="both"/>', '<w:jc w:val="left"/>')))
        elif "<m:oMathPara>" in b:
            equations += 1
            out.append(formula_table(template_formula, b, equations))
        elif style in ("Heading1", "Heading2"):
            out.append(set_ppr(b, ppr("Balk1" if style == "Heading1" else "Balk2",
                                      "<w:keepNext/>")))
        elif style == "TableCaption":
            tables += 1
            b = prefix_run(set_ppr(b, ppr("Altyaz", '<w:keepNext/><w:jc w:val="both"/>')),
                           f"Table {tables}. ")
            out.append(math_size(b, 18))
        elif style == "ImageCaption":
            figures += 1
            out.append(math_size(prefix_run(set_ppr(b, ppr("Altyaz")), f"Figure {figures}. "), 18))
        elif style == "CaptionedFigure" or "<w:drawing>" in b:
            out.append(set_ppr(b, ppr("Altyaz", "<w:keepNext/>")))
        elif "<w:numPr>" in b:
            num = re.search(r'<w:numId w:val="(\d+)"', b).group(1)
            kind = formats.get(num)
            if kind is None:
                sys.exit(f"list {num} of pandoc has no format: {text[:60]}")
            spacing = '<w:spacing w:before="40" w:beforeAutospacing="0" w:after="40" w:afterAutospacing="0"/>'
            if kind == "continuation":
                out.append(set_ppr(b, ppr("", spacing + '<w:ind w:left="357"/>')))
                continue
            counters[num] = counters.get(num, 0) + 1
            mark = "\u2022\t" if kind == "bullet" else f"{counters[num]}.\t"
            b = set_ppr(b, ppr("", spacing + '<w:ind w:left="357" w:hanging="357"/>'))
            out.append(prefix_run(b, mark))
        elif style in ("FirstParagraph", "BodyText", "Compact", ""):
            out.append(set_ppr(b, ""))
        else:
            sys.exit(f"a pandoc paragraph style this script does not map: {style!r}: {text[:60]}")
    xml = "".join(out)
    xml = re.sub(r'<w:rStyle w:val="Hyperlink"\s*/>', '<w:rStyle w:val="Kpr"/>', xml)
    xml = re.sub(r'<w:rStyle w:val="VerbatimChar"\s*/>',
                 '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/>', xml)
    left = set(re.findall(r'<w:[pr]Style w:val="([^"]+)"', xml)) - {
        "Balk1", "Balk2", "Balk3", "Altyaz", "Default", "Kpr"}
    if left:
        sys.exit(f"styles that are not of the template remain: {sorted(left)}")
    return xml, equations


def abstract_runs(latex: str, rpr: str) -> str:
    """The abstract as runs; d_z set as italic d with subscript z, spaced around "="."""
    text = " ".join(strip_comments(latex).split())
    text = re.sub(r"\\texttt\{([^}]*)\}", r"\1", text).replace("\\ ", " ").replace("~", "\u00a0")
    runs = []
    for i, part in enumerate(re.split(r"\$d_z\{=\}([\d.]+)\$", text)):
        if i % 2:
            runs += [f'<w:r><w:rPr>{rpr}<w:i/></w:rPr><w:t>d</w:t></w:r>',
                     f'<w:r><w:rPr>{rpr}<w:i/><w:vertAlign w:val="subscript"/></w:rPr><w:t>z</w:t></w:r>',
                     f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve"> = {part}</w:t></w:r>']
        elif part:
            runs.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    if any(c in re.sub(r"\$d_z\{=\}[\d.]+\$", "", text) for c in "\\{}$"):
        sys.exit(f"the abstract holds LaTeX this script does not convert: {text}")
    return "".join(runs)


def keywords() -> str:
    """Three to five keywords in alphabetical order, each with a capital first letter."""
    words = [w.strip() for w in strip_comments(KEYWORDS.read_text(encoding="utf-8")).split(",")]
    words = [w[0].upper() + w[1:] for w in words if w]
    if not 3 <= len(words) <= 5:
        sys.exit(f"the journal asks for 3 to 5 keywords, not {len(words)}")
    return ", ".join(sorted(words, key=str.lower))


def replace_text(p: str, new: str) -> str:
    """The paragraph's text replaced by `new`, in the format of its first run."""
    runs = re.findall(r"<w:r(?: [^>]*)?>.*?</w:r>", p, flags=re.DOTALL)
    first = next(r for r in runs if "<w:t" in r)
    rpr = re.search(r"<w:rPr>.*?</w:rPr>", first, flags=re.DOTALL)
    new_run = (f'<w:r>{rpr.group(0) if rpr else ""}'
               f'<w:t xml:space="preserve">{escape(new)}</w:t></w:r>')
    head = p[:p.index(first)]
    tail = p[p.rindex(runs[-1]) + len(runs[-1]):]
    return head + new_run + tail


def title_block(blocks: list[str], tex: str) -> list[str]:
    """The template's first blocks (up to the first section break), with the paper's text."""
    end = next(i for i, b in enumerate(blocks) if "<w:sectPr" in b)
    out = []
    for b in blocks[:end + 1]:
        t = text_of(b).strip()
        if t == "Manuscript title":
            b = replace_text(b, title_of(tex))
        elif b.startswith("<w:tbl>") and "Author Name Surname" in t:
            b = ('<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="18"/>'
                 f'</w:rPr><w:t>{escape(MASKED_NOTE)}</w:t></w:r></w:p>')
        elif t == "* Corresponding Author":
            continue
        elif t.startswith("The abstract should"):
            rpr = '<w:sz w:val="18"/><w:szCs w:val="20"/><w:lang w:val="en-US"/>'
            b = re.sub(r"(</w:pPr>).*(</w:p>)", lambda m: m.group(1) + abstract_runs(
                ABSTRACT.read_text(encoding="utf-8"), rpr) + m.group(2), b, count=1, flags=re.DOTALL)
        elif t.startswith("Keywords"):
            runs = re.findall(r"<w:r(?: [^>]*)?>.*?</w:r>", b, flags=re.DOTALL)
            b = b.replace(runs[-1], replace_text("<w:p>" + runs[-1] + "</w:p>", keywords())[5:-6])
        out.append(b)
    return out


def merge_namespaces(template_doc: str, pandoc_doc: str) -> str:
    troot = re.search(r"<w:document [^>]*>", template_doc).group(0)
    proot = re.search(r"<w:document [^>]*>", pandoc_doc).group(0)
    have = set(re.findall(r"xmlns:(\w+)=", troot))
    extra = "".join(f' xmlns:{p}="{u}"' for p, u in re.findall(r'xmlns:(\w+)="([^"]+)"', proot)
                    if p not in have)
    return template_doc.replace(troot, troot[:-1] + extra + ">", 1)


def core_properties(xml: str, title: str, creator: str) -> str:
    for tag in ("dc:creator", "cp:lastModifiedBy"):
        xml = re.sub(rf"<{tag}>.*?</{tag}>|<{tag}/>", f"<{tag}>{escape(creator)}</{tag}>", xml)
    xml = re.sub(r"<dc:title>.*?</dc:title>|<dc:title/>", f"<dc:title>{escape(title)}</dc:title>", xml)
    if "<dc:title>" not in xml:
        xml = xml.replace("</cp:coreProperties>", f"<dc:title>{escape(title)}</dc:title></cp:coreProperties>")
    return xml


def write_package(template: Path, out: Path, document: str, rels: str | None,
                  media: dict[str, bytes], title: str, creator: str,
                  used_media: set[str] | None = None) -> None:
    with zipfile.ZipFile(template) as zt, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zo:
        for item in zt.infolist():
            n = item.filename
            data = zt.read(n)
            if n == "word/document.xml":
                data = document.encode("utf-8")
            elif n == "word/_rels/document.xml.rels" and rels is not None:
                data = rels.encode("utf-8")
            elif used_media is not None and n.startswith("word/media/") and \
                    n[len("word/"):] not in used_media:
                continue
            elif n == "docProps/core.xml":
                data = core_properties(data.decode("utf-8"), title, creator).encode("utf-8")
            elif n == "docProps/custom.xml":
                continue                          # the template's own custom properties
            elif n == "_rels/.rels":
                data = re.sub(rb'<Relationship [^>]*(?:thumbnail|custom-properties)[^>]*/>', b"", data)
            elif n == "[Content_Types].xml":
                text = re.sub(r'<Override PartName="/docProps/custom.xml"[^>]*/>', "",
                              data.decode("utf-8"))
                for ext, mime in (("png", "image/png"), ("jpeg", "image/jpeg")):
                    if any(m.endswith("." + ext) for m in media) and f'Extension="{ext}"' not in text:
                        text = text.replace("<Default ", f'<Default Extension="{ext}" '
                                            f'ContentType="{mime}"/><Default ', 1)
                data = text.encode("utf-8")
            zo.writestr(n, data)
        for n, data in media.items():
            zo.writestr(n, data)


def build_manuscript(tex: str) -> Path:
    src, refs, wide, n_eq = pandoc_source(tex)
    pngs = [CI / f"{p}.png" for p in re.findall(r"\\includegraphics\[[^\]]*\]\{([^}]+)\.pdf\}", tex)]
    widths = [float(w) for w in re.findall(r"\\includegraphics\[width=([\d.]+)\\linewidth\]", tex)]
    tmp_src, tmp_docx = CI / f"_{NAME}_pandoc.tex", OUT / f"_{NAME}_pandoc.docx"
    tmp_src.write_text(src, encoding="utf-8")
    try:
        run(["quarto", "pandoc", tmp_src.name, "-f", "latex", "-t", "docx", "-o", str(tmp_docx),
             "--resource-path=."], CI)
    finally:
        tmp_src.unlink(missing_ok=True)
    with zipfile.ZipFile(tmp_docx) as zp:
        pandoc_doc = zp.read("word/document.xml").decode("utf-8")
        pandoc_rels = zp.read("word/_rels/document.xml.rels").decode("utf-8")
        numbering = zp.read("word/numbering.xml").decode("utf-8") if "word/numbering.xml" in zp.namelist() else ""
        pandoc_media = {n: zp.read(n) for n in zp.namelist() if n.startswith("word/media/")}
    tmp_docx.unlink()

    with zipfile.ZipFile(TEMPLATE) as zt:
        template_doc = zt.read("word/document.xml").decode("utf-8")
        template_rels = zt.read("word/_rels/document.xml.rels").decode("utf-8")
        other_rels = "".join(zt.read(n).decode("utf-8") for n in zt.namelist()
                             if n.startswith("word/_rels/") and n != "word/_rels/document.xml.rels")
    blocks = BLOCK.findall(template_doc.split("<w:body>", 1)[1])
    template_ref = next(b for b in blocks if text_of(b).startswith("[1] "))
    body, equations = convert_body(pandoc_doc, numbering, template_doc, wide, template_ref)
    if equations != n_eq:
        sys.exit("the equations found in Word are not those of the source")
    body = scale_figures(body, pngs, widths)

    new_rels, media = [], {}
    for rel in re.findall(r"<Relationship [^>]*>", pandoc_rels):
        attr = dict(re.findall(r'(\w+)="([^"]*)"', rel))
        rid, rtype, target = attr["Id"], attr["Type"], attr["Target"]
        mode = ' TargetMode="External"' if attr.get("TargetMode") == "External" else ""
        kind = rtype.rsplit("/", 1)[1]
        if kind not in ("hyperlink", "image") or f'"{rid}"' not in body:
            continue
        new = f"rIdPB{len(new_rels) + 1}"
        body = body.replace(f'"{rid}"', f'"{new}"')
        if kind == "image":
            data = pandoc_media["word/" + target]
            target = f"media/paperb_{len(media) + 1}{Path(target).suffix}"
            media["word/" + target] = data
        new_rels.append(f'<Relationship Id="{new}" Type="{rtype}" Target="{target}"{mode}/>')

    head = merge_namespaces(template_doc, pandoc_doc)
    head = head[:head.index("<w:body>") + len("<w:body>")]
    final_sect = re.findall(r"<w:sectPr[ >].*?</w:sectPr>", template_doc, flags=re.DOTALL)[-1]
    document = head + "".join(title_block(blocks, tex)) + body + final_sect + "</w:body></w:document>"

    kept = []
    for rel in re.findall(r"<Relationship [^>]*/>", template_rels):
        rid = re.search(r'Id="([^"]+)"', rel).group(1)
        kind = re.search(r'Type="[^"]*/([^"/]+)"', rel).group(1)
        if kind in ("hyperlink", "image") and f'"{rid}"' not in document:
            continue
        kept.append(rel)
    rels = (template_rels[:template_rels.index("<Relationship ")] + "".join(kept + new_rels)
            + "</Relationships>")
    used = set(re.findall(r'Target="(media/[^"]+)"', rels + other_rels))
    out = OUT / f"{NAME}_manuscript.docx"
    write_package(TEMPLATE, out, document, rels, media, title_of(tex), "", used)
    return out


def fill_paragraphs(template: Path, out: Path, fills: list[tuple[str, list[str] | None]],
                    title: str) -> None:
    """Replace paragraphs of a journal form, matched by their text in order.

    Each fill is (text of the template paragraph, new lines); None drops the paragraph, and
    several lines become several paragraphs in the same format.
    """
    with zipfile.ZipFile(template) as zt:
        doc = zt.read("word/document.xml").decode("utf-8")
    paras = re.findall(r"<w:p(?: [^>]*)?>.*?</w:p>", doc, flags=re.DOTALL)
    pos = 0
    for old_text, lines in fills:
        idx = next((i for i in range(pos, len(paras))
                    if unescape(text_of(paras[i])).strip() == old_text), None)
        if idx is None:
            sys.exit(f"{template.name}: no paragraph {old_text!r}")
        new = "" if lines is None else "".join(replace_text(paras[idx], line) for line in lines)
        doc = doc.replace(paras[idx], new, 1)
        pos = idx + 1
    write_package(template, out, doc, None, {}, title, AUTHOR)


def build_title_page(tex: str) -> Path:
    out = OUT / f"{NAME}_title_page.docx"
    fill_paragraphs(TITLE_TEMPLATE, out, [
        ("Paper title", [title_of(tex)]),
        ("Running head", [f"Running head: {RUNNING_HEAD}"]),
        ("Author Name Surname", [f"{AUTHOR} *"]),
        ("Affiliation, Address, City, Country, email address", [f"{AFFILIATION}, {EMAIL}"]),
        ("ORCID: orcid.org/xxxx-xxxx-xxxx-xxxx", [f"ORCID: orcid.org/{ORCID}",
                                                  "* Corresponding author"]),
        ("\u2026", None),
        ("Acknowledgement:", ["Acknowledgement:", ACKNOWLEDGMENT, "",
                              "Data and code availability:",
                              f"The experimental code, the run artifacts and the analysis exports "
                              f"are in the public repository {REPOSITORY}, released under the MIT "
                              f"License, and in its archived release, {ARCHIVE}.", "",
                              "Competing interests:",
                              "The author declares no competing interests.", "",
                              "Author contribution:",
                              "The author is the sole author of the study and of the manuscript."]),
    ], title_of(tex))
    return out


def build_cover_letter(tex: str) -> Path:
    title = title_of(tex)
    out = OUT / f"{NAME}_cover_letter.docx"
    fill_paragraphs(LETTER_TEMPLATE, out, [
        ("Cover Letter [Sample]", ["Cover Letter"]),
        ("[Your Name]", [AUTHOR]),
        ("[Your Affiliation]", ["Universidad Americana de Europa (UNADE), Department of Computer Science"]),
        ("[Your Address]", ["Canc\u00fan, Quintana Roo, Mexico"]),
        ("[Date]", ["[date of submission]"]),
        ("Dear [Editor name],", ["Dear Editor,"]),
        ("I/We wish to submit an original research article entitled \u201c[title of article]\u201d "
         "for consideration by Computers and Informatics.",
         [f"I wish to submit an original research article entitled \u201c{title}\u201d for "
          "consideration by Computers and Informatics."]),
        ("I/We confirm that this work is original and has not been published elsewhere, nor is it "
         "currently under consideration for publication elsewhere.",
         ["I confirm that this work is original and has not been published elsewhere, nor is it "
          "currently under consideration for publication elsewhere. An earlier version was "
          "submitted to another journal and has been withdrawn from it before this submission."]),
        ("In this paper, I/we report on / show that _______. This is significant because "
         "__________.",
         ["In this paper, I report a paired comparison of LIME and SHAP, the two explanation "
          "methods most used for tabular machine-learning models, in which both methods explain "
          "the same model, the same instances and the same random seed. This pairing separates a "
          "difference between the methods from a difference between the models or samples they "
          "were run on, which is rarely done. The comparison shows that SHAP is more stable and "
          "more faithful to the model, but also that two common rules of thumb need a condition: "
          "the latency ordering of the two methods depends on the model family and reverses "
          "between two tree ensembles, and the low stability of LIME on one dataset depends on its "
          "kernel width and on the feature space. This is significant because practitioners "
          "choose between the two methods on such rules, and a ranking obtained on one dataset and "
          "one configuration does not transfer by default."]),
        ("We believe that this manuscript is appropriate for publication by Computers and "
         "Informatics because it\u2026 [Specific reference to the journal\u2019s Aims & Scope]. "
         "__________.",
         ["I believe that this manuscript is appropriate for Computers and Informatics because it "
          "contributes to artificial intelligence, one of the computer-science areas of the "
          "journal\u2019s Aims & Scope, with an empirical, reproducible study of explainable "
          "machine learning that ends in a deployment recommendation conditioned on the model "
          "architecture. The code and all run artifacts are public."]),
        ("[Please explain in your own words the significance and novelty of the work, the problem "
         "that is being addressed, and why the manuscript belongs in this journal. Do not simply "
         "insert your abstract into your cover letter! Briefly describe the research you are "
         "reporting in your paper, why it is important, and why you think the readership of the "
         "journal would be interested in it.]",
         ["Relation to earlier work. The runs analysed here were released with an earlier article "
          "by the author and a co-author (Revista de Investigaci\u00f3n Multidisciplinaria "
          "Iberoamericana, https://doi.org/10.69850/rimi.vi3.307), which includes a paired "
          "SHAP\u2013LIME test on a 45-cell subset of three model families. The present manuscript "
          "extends that test to the full 75 cells, adds confidence intervals and effect sizes, and "
          "contributes the conditional results above, which are not in that article; it restates "
          "none of its numerical results. Other manuscripts by the author, under review at other "
          "journals, analyse the same runs for different questions and report none of the results "
          "reported here. The code, the run artifacts and earlier drafts of this work are in a "
          "public repository, archived at https://doi.org/10.5281/zenodo.23147228; this may show "
          "in the similarity report."]),
        ("We have no conflicts of interest to disclose.", ["I have no conflicts of interest to disclose."]),
        ("Please address all correspondence concerning this manuscript to me at [email address].",
         [f"Please address all correspondence concerning this manuscript to me at {EMAIL}."]),
        ("[Your name]", [AUTHOR]),
    ], title)
    return out


WORD_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
  $doc = $word.Documents.Open($args[0], $false, $false)
  $doc.Fields.Update() | Out-Null
  $doc.Repaginate()
  $pages = $doc.ComputeStatistics(2)
  $words = $doc.ComputeStatistics(0)
  $doc.Save()
  $doc.ExportAsFixedFormat($args[1], 17, $false, 0, 0, 0, 0, 0, $false)
  $doc.Close($false)
  Write-Output "pages=$pages words=$words"
} finally { $word.Quit() }
"""


def word_pass(docx: Path, title: str, creator: str) -> str:
    script = OUT / "_word.ps1"
    script.write_text(WORD_SCRIPT, encoding="utf-8")
    pdf = docx.with_suffix(".pdf")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                            str(script), str(docx), str(pdf)], capture_output=True, text=True)
    finally:
        script.unlink(missing_ok=True)
    m = re.search(r"pages=(\d+) words=(\d+)", r.stdout)
    if r.returncode or not m:
        sys.exit(f"Word failed on {docx.name}:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")
    # Word signs the file it saves with the name of the Windows user; set the properties again.
    tmp = docx.with_suffix(".tmp")
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in zin.namelist():
            data = zin.read(n)
            if n == "docProps/core.xml":
                data = core_properties(data.decode("utf-8"), title, creator).encode("utf-8")
            zout.writestr(n, data)
    tmp.replace(docx)
    return f"{m.group(1)} pages, {m.group(2)} words in Word"


def check_masked(docx: Path) -> None:
    with zipfile.ZipFile(docx) as z:
        text = " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist()
                        if n.endswith(".xml") or n.endswith(".rels"))
    found = [w for w in LEAKS if w.lower() in text.lower()]
    if found:
        sys.exit(f"{docx.name}: the masked manuscript carries author data: {found}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-pdf", action="store_true", help="do not open Word")
    args = ap.parse_args()
    for f in (TEMPLATE, TITLE_TEMPLATE, LETTER_TEMPLATE):
        if not f.exists():
            sys.exit(f"{f.relative_to(ROOT)} is missing; download it from the journal site "
                     "(CI_SUBMISSION.md)")
    if shutil.which("quarto") is None:
        sys.exit("quarto (for its pandoc) is not installed")
    OUT.mkdir(exist_ok=True)
    tex = SOURCE.read_text(encoding="utf-8")
    manuscript = build_manuscript(tex)
    check_masked(manuscript)
    built = [(manuscript, ""), (build_title_page(tex), AUTHOR), (build_cover_letter(tex), AUTHOR)]
    for docx, creator in built:
        line = f"docx  {docx.relative_to(ROOT)}"
        if not args.no_pdf:
            line += f" ({word_pass(docx, title_of(tex), creator)})"
        print(line)
    check_masked(manuscript)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
