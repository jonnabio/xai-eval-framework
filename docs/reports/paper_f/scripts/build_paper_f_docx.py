#!/usr/bin/env python3
"""Paper F in the Word template of Journal of Computer Sciences Institute.

    python docs/reports/paper_f/scripts/build_paper_f_docx.py [--no-pdf]

Reads paper_f.tex (written by build_paper_f.py; run that first) and writes, to submission/:

    herrera-vasquez.docx, herrera-vasquez.pdf     the manuscript in the journal's template
                                                  and the same printed by Word, under the
                                                  name the journal asks for (the surname of
                                                  the corresponding author)
    paper_f_blind.docx, paper_f_blind_word.pdf    the same without author data

The journal's file (venue/template/JCSI_template_2025.docx, downloaded from the journal site
and not redistributed here) is the package: its styles, headers, footers and settings are
kept, and only the body is replaced. Every paragraph takes a style of the template.

How the body is made:
1. The title block is written in the template's own paragraphs (one column).
2. The text from the Introduction on is converted by pandoc (through Quarto), which gives
   native Word equations, tables, links and the embedded figure. Citations are numbered
   here in the order of the reference list that BibTeX wrote (elsarticle-num, the order of
   first citation), and the list is printed from that same file.
3. The paragraphs of pandoc are given the template's styles; each numbered equation goes
   into the template's two-cell formula table; Tables 1 and 2 and Figure 1 span the page,
   between continuous section breaks; Table 3 stays in its column.

Word (through COM) repaginates, counts the pages and prints the PDF. Without Word the
.docx files are still written; pass --no-pdf.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[4]
F = Path(__file__).resolve().parents[1]
OUT = F / "submission"
TEMPLATE = F / "venue" / "template" / "JCSI_template_2025.docx"
TECTONIC = ROOT / "tools" / "tectonic-portable" / (
    "tectonic.exe" if sys.platform == "win32" else "tectonic")
MAX_PAGES = 8
TEXT_WIDTH_EMU = 6_050_000          # a little under the 17 cm between the margins
FIGURE_ALT = ("Four line charts, one for each measure (faithfulness gap, stability, sparsity, "
              "cost), showing the rank from 1 to 4 of LIME, SHAP, Anchors and DiCE on each of "
              "the sixteen datasets.")
AUTHOR = "Jonathan Herrera-V\u00e1squez"
AFFILIATION = ("Department of Computer Science, Universidad Americana de Europa (UNADE), "
               "Canc\u00fan, Quintana Roo, Mexico")
EMAIL = "jonnabio@gmail.com"
ORCID = "0000-0002-7149-6635"
BLIND_AUTHOR = "Author information omitted for double-blind review"
# The journal asks for the source as surname_of_corresponding_author.docx and a matching PDF.
FULL_NAME = "herrera-vasquez"

PAGE = ('<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1418" w:right="1134" w:bottom="1418" '
        'w:left="1134" w:header="709" w:footer="709" w:gutter="0"/>')
SECT_TWO = (f'<w:sectPr><w:type w:val="continuous"/>{PAGE}<w:cols w:num="2" w:space="567"/>'
            '<w:docGrid w:linePitch="360"/></w:sectPr>')
SECT_ONE = (f'<w:sectPr><w:type w:val="continuous"/>{PAGE}<w:cols w:space="708"/>'
            '<w:docGrid w:linePitch="360"/></w:sectPr>')
HEADER_SLOT = "<!--header of the text pages-->"
SMALL = '<w:sz w:val="16"/><w:szCs w:val="16"/>'      # 8 pt, two points under the text


def run(cmd: list[str], cwd: Path) -> None:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode:
        sys.exit(f"{cmd[0]} failed:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")


# --- LaTeX side -------------------------------------------------------------------

def resolve_full(tex: str, full: bool) -> str:
    """Keep one branch of every \\iffull ... [\\else ...] \\fi block."""
    def pick(m: re.Match) -> str:
        return (m.group(1) if full else (m.group(2) or ""))
    return re.sub(r"\\iffull\b(.*?)(?:\\else\b(.*?))?\\fi\b", pick, tex, flags=re.DOTALL)


def reference_list() -> list[tuple[str, str]]:
    """(key, LaTeX text) of every reference, in the order BibTeX wrote them."""
    stub = F / "_docx_bbl.tex"
    stub.write_text("\\def\\fullversion{}\n\\input{paper_f}\n", encoding="utf-8")
    try:
        run([str(TECTONIC), "-X", "compile", "--keep-intermediates", "--outdir", str(OUT),
             stub.name], F)
        bbl = (OUT / "_docx_bbl.bbl").read_text(encoding="utf-8")
    finally:
        stub.unlink(missing_ok=True)
        for ext in (".aux", ".bbl", ".blg", ".out", ".pdf", ".log"):
            (OUT / f"_docx_bbl{ext}").unlink(missing_ok=True)
    items = []
    for key, text in re.findall(r"\\bibitem\{([^}]+)\}(.*?)(?=\\bibitem\{|\\end\{thebibliography\})",
                                bbl, flags=re.DOTALL):
        text = " ".join(text.split())
        # The journal's format ends an entry with ", https://doi.org/...".
        text = re.sub(r"\.?\s*(?:\\newblock\s*)?\\href\s*\{([^}]*)\}\s*\{\\path\{[^}]*\}\}\.?",
                      r", \\url{\1}", text)
        if "\\newblock" in text or "\\href" in text:
            sys.exit(f"reference {key}: a form this script does not convert:\n{text}")
        items.append((key, text))
    return items


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


def pandoc_source(tex: str, refs: list[tuple[str, str]]) -> str:
    """The text from the Introduction to the declaration, as a small LaTeX file for pandoc."""
    archive = re.search(r"\\newcommand\{\\paperfarchive\}\{.*\}", tex)
    body = tex[tex.index("\\section{Introduction}"):]
    body = body[:body.index("{\\renewcommand{\\href}")]
    body = re.sub(r"\\input\{(generated/[^}]+)\}",
                  lambda m: (F / f"{m.group(1)}.tex").read_text(encoding="utf-8"), body)
    body = re.sub(r"(?<!\\)%.*", "", body)                       # comments
    number = {key: i for i, (key, _) in enumerate(refs, 1)}
    missing = {k.strip() for g in re.findall(r"\\cite\{([^}]*)\}", body)
               for k in g.split(",")} - set(number)
    if missing:
        sys.exit(f"cited but not in the reference list: {sorted(missing)}")
    body = re.sub(r"\\cite\{([^}]*)\}",
                  lambda m: cite_text([k.strip() for k in m.group(1).split(",")], number), body)
    # Numbers of tables, figure and equations, in the order of the text.
    for prefix in ("tab", "fig"):
        for i, label in enumerate(re.findall(r"\\label\{(" + prefix + r":[^}]+)\}", body), 1):
            body = body.replace(f"\\ref{{{label}}}", str(i))
    body = re.sub(r"\\label\{[^}]*\}", "", body)
    if "\\ref{" in body:
        sys.exit("a \\ref is left without a number")
    # Elements that span the page are fenced, to be put between section breaks later.
    for env in ("table", "figure"):
        body = re.sub(r"\\begin\{" + env + r"\*\}(?:\[[^\]]*\])?",
                      r"\n\nWIDEBEGIN\n\n\\begin{" + env + "}", body)
        body = body.replace(f"\\end{{{env}*}}", f"\\end{{{env}}}\n\nWIDEEND\n\n")
    body = re.sub(r"\\begin\{(table|figure)\}\[[^\]]*\]", r"\\begin{\1}", body)
    body = body.replace("figures/fig1.pdf", "figures/fig1.png")
    body = re.sub(r"\\setlength\{[^}]*\}\{[^}]*\}", "", body)
    body = re.sub(r"\\section\*\{([^}]*)\}", r"\n\nUNNUMHEAD \1\n\n", body)
    body += "\n\nUNNUMHEAD References\n\n" + "\n\n".join(f"REFITEM {t}" for _, t in refs)
    return ("\\documentclass{article}\n\\usepackage{amsmath,amssymb,graphicx,booktabs,hyperref}\n"
            + (archive.group(0) + "\n" if archive else "")
            + "\\begin{document}\n" + body + "\n\\end{document}\n")


# --- Word side --------------------------------------------------------------------

def text_of(xml: str) -> str:
    return "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml))


def set_style(p: str, style: str, sect: str = "") -> str:
    """Give a pandoc paragraph a style of the template (and nothing else in its pPr)."""
    jc = re.search(r"<w:jc w:val=\"[^\"]+\"\s*/>", p.split("</w:pPr>")[0]) if "<w:pPr>" in p else None
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/>{jc.group(0) if jc and style == "Table" else ""}{sect}</w:pPr>'
    p = re.sub(r"<w:pPr>.*?</w:pPr>", "", p, count=1, flags=re.DOTALL)
    return re.sub(r"<w:p>", "<w:p>" + ppr, p, count=1)


def strip_marker(p: str, marker: str) -> str:
    return re.sub(r"(<w:t[^>]*>)" + marker + r"\s*", r"\1", p, count=1)


def prefix_run(p: str, text: str) -> str:
    """Insert a run at the start of a paragraph's content."""
    run_xml = f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'
    return re.sub(r"(</w:pPr>)", r"\1" + run_xml, p, count=1)


def small_math(xml: str) -> str:
    """Equation runs at the size of the small text around them (table cells, captions)."""
    rpr = ('<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>' + SMALL + "</w:rPr>")
    return re.sub(r"<m:r>(<m:rPr>.*?</m:rPr>|<m:rPr\s*/>)?", lambda m: "<m:r>" + (m.group(1) or "") + rpr,
                  xml, flags=re.DOTALL)


def small_runs(xml: str) -> str:
    # A lone sign set as an equation ("<" before 0.001, a minus) becomes ordinary text.
    def sign(m: re.Match) -> str:
        t = "".join(re.findall(r"<m:t[^>]*>([^<]*)</m:t>", m.group(0)))
        return f"<w:r><w:t>{t}</w:t></w:r>" if t in ("&lt;", "−", "-") else m.group(0)
    xml = re.sub(r"<m:oMath>.*?</m:oMath>", sign, xml, flags=re.DOTALL)
    xml = re.sub(r"<w:r><w:rPr>", "<w:r><w:rPr>" + SMALL, xml)
    return small_math(re.sub(r"<w:r>(?!<w:rPr>)", f"<w:r><w:rPr>{SMALL}</w:rPr>", xml))


def restyle_table(tbl: str, example_tblpr: str, width: int) -> str:
    cells = re.findall(r"<w:tc>.*?</w:tc>", tbl, flags=re.DOTALL)
    rows = re.findall(r"<w:tr>.*?</w:tr>|<w:tr [^>]*>.*?</w:tr>", tbl, flags=re.DOTALL)
    ncol = len(cells) // max(len(rows), 1)
    out = re.sub(r"<w:tblPr>.*?</w:tblPr>", example_tblpr, tbl, count=1, flags=re.DOTALL)
    out = re.sub(r"<w:tblGrid>.*?</w:tblGrid>", "<w:tblGrid>" + "<w:gridCol/>" * ncol
                 + "</w:tblGrid>", out, count=1, flags=re.DOTALL)
    out = re.sub(r"<w:tcPr>.*?</w:tcPr>", "", out, flags=re.DOTALL)
    out = re.sub(r"<w:trPr>.*?</w:trPr>", "", out, flags=re.DOTALL)
    out = re.sub(r"<w:p>.*?</w:p>", lambda m: set_style(m.group(0), "Table"), out,
                 flags=re.DOTALL)
    # The rows stay on one page: every row but the last is kept with the next.
    last = out.rindex("<w:tr")
    out = out[:last].replace('<w:pStyle w:val="Table"/>',
                             '<w:pStyle w:val="Table"/><w:keepNext/>') + out[last:]
    return small_runs(out)


def formula_table(template_formula: str, p: str, n: int) -> str:
    math = re.search(r"<m:oMathPara>.*?</m:oMathPara>", p, flags=re.DOTALL).group(0)
    out = re.sub(r"<m:oMathPara>.*?</m:oMathPara>", lambda _: math, template_formula, count=1,
                 flags=re.DOTALL)
    # The cached result of the template's SEQ field, between "separate" and "end".
    return re.sub(r'(<w:fldChar w:fldCharType="separate"/></w:r><w:r[^>]*>(?:<w:rPr>.*?</w:rPr>)?'
                  r"<w:t>)\d+(</w:t>)", rf"\g<1>{n}\g<2>", out, count=1, flags=re.DOTALL)


def break_paragraph(sect: str, before: int = 0) -> str:
    """An empty paragraph of almost no height that ends a section."""
    return (f'<w:p><w:pPr><w:pStyle w:val="Normaltextnoindent"/><w:spacing w:before="{before}" '
            f'w:after="0" w:line="20" w:lineRule="exact"/><w:rPr><w:sz w:val="2"/></w:rPr>{sect}'
            '</w:pPr></w:p>')


def convert_body(pandoc_doc: str, template_doc: str) -> tuple[str, int]:
    """Blocks of pandoc with the template's styles. Returns the XML and the equations found."""
    template_tables = re.findall(r"<w:tbl>.*?</w:tbl>", template_doc, flags=re.DOTALL)
    template_formula = template_tables[0]
    example_tblpr = re.search(r"<w:tblPr>.*?</w:tblPr>", template_tables[1], flags=re.DOTALL).group(0)
    # The header of the template's text pages goes in every section of ours: a section
    # without one takes that of the section before it, which for the first would be the
    # title page's. It is a placeholder here and is filled by assemble(), after the
    # relationship ids of pandoc are renamed (they can equal the template's).
    sect_two = SECT_TWO.replace("<w:sectPr>", "<w:sectPr>" + HEADER_SLOT)
    sect_one = SECT_ONE.replace("<w:sectPr>", "<w:sectPr>" + HEADER_SLOT)
    inner = pandoc_doc.split("<w:body>", 1)[1]
    inner = inner[:inner.rindex("<w:sectPr")]
    blocks = re.findall(r"<w:tbl>.*?</w:tbl>|<w:p>.*?</w:p>|<w:p/>", inner, flags=re.DOTALL)
    out: list[str] = []
    tables = figures = equations = 0
    wide = after_formula = False
    for b in blocks:
        if b.startswith("<w:tbl>"):
            out.append(restyle_table(b, example_tblpr, 0))
            continue
        if b == "<w:p/>":
            continue
        style = re.search(r'<w:pStyle w:val="([^"]+)"', b)
        style = style.group(1) if style else ""
        text = text_of(b).strip()
        was_formula, after_formula = after_formula, False
        if text == "WIDEBEGIN":
            out.append(break_paragraph(sect_two))
            wide = True
        elif text == "WIDEEND":
            out.append(break_paragraph(sect_one, before=120))
            wide = False
        elif text.startswith("UNNUMHEAD"):
            out.append(set_style(strip_marker(b, "UNNUMHEAD"), "Referenceheading"))
            after_formula = True              # the paragraph after a heading has no indent
        elif text.startswith("REFITEM"):
            out.append(set_style(strip_marker(b, "REFITEM"), "References"))
        elif "<m:oMathPara>" in b:
            equations += 1
            out.append(formula_table(template_formula, b, equations))
            after_formula = True
        elif style in ("Heading1", "Heading2"):
            out.append(set_style(b, style))
        elif style == "TableCaption":
            tables += 1
            b = prefix_run(set_style(b, "Tablecapture"), f"Table {tables}: ")
            out.append(small_math(b.replace('<w:pStyle w:val="Tablecapture"/>',
                                            '<w:pStyle w:val="Tablecapture"/><w:keepNext/>')))
        elif style == "ImageCaption":
            figures += 1
            out.append(small_math(prefix_run(set_style(b, "Figurecapture"), f"Figure {figures}: ")))
        elif style == "CaptionedFigure" or "<w:drawing>" in b:
            b = re.sub(r"<wp:docPr ([^>]*?)/?>", lambda m: "<wp:docPr " + re.sub(
                r'\s*descr="[^"]*"', "", m.group(1)) + f' descr="{escape(FIGURE_ALT)}"/>', b, count=1)
            out.append(set_style(b, "Figure"))
        elif "<w:numPr>" in b:
            out.append(set_style(b, "Numberedlist"))
        elif style in ("FirstParagraph", "BodyText", "Compact", ""):
            first = style == "FirstParagraph" or was_formula
            out.append(set_style(b, "Normaltextnoindent" if first else "Normaltextwithindent"))
        else:
            sys.exit(f"a pandoc paragraph style this script does not map: {style!r}: {text[:60]}")
    if wide:
        sys.exit("a WIDEBEGIN without its WIDEEND")
    xml = re.sub(r'<w:rStyle w:val="Hyperlink"\s*/>', '<w:rStyle w:val="Hipercze"/>', "".join(out))
    left = set(re.findall(r'<w:[pr]Style w:val="([^"]+)"', xml)) - {
        "Heading1", "Heading2", "Referenceheading", "References", "Tablecapture", "Figurecapture",
        "Figure", "Numberedlist", "Normaltextnoindent", "Normaltextwithindent", "Table",
        "formula", "Hipercze", "Odwoanieprzypisudolnego"}
    if left:
        sys.exit(f"styles that are not of the template remain: {sorted(left)}")
    return xml, equations


def scale_figure(xml: str, png: Path) -> str:
    """Set the figure to the width of the text, keeping its proportions."""
    import struct
    with png.open("rb") as fh:
        head = fh.read(24)
    w, h = struct.unpack(">II", head[16:24])
    cx, cy = TEXT_WIDTH_EMU, round(TEXT_WIDTH_EMU * h / w)
    xml = re.sub(r'<wp:extent cx="\d+" cy="\d+"\s*/>', f'<wp:extent cx="{cx}" cy="{cy}"/>', xml)
    return re.sub(r'<a:ext cx="\d+" cy="\d+"\s*/>', f'<a:ext cx="{cx}" cy="{cy}"/>', xml)


def abstract_runs(latex: str) -> str:
    """The abstract as runs: plain text, with the variable p in italics."""
    text = " ".join(latex.split()).replace("\\%", "%").replace("~", "\u00a0").replace("$<$", "<\u00a0")
    runs = []
    for i, part in enumerate(re.split(r"\$([^$]+)\$", text)):
        if not part:
            continue
        rpr = "<w:rPr><w:i/><w:iCs/><w:lang w:val=\"en-GB\"/></w:rPr>" if i % 2 else \
            "<w:rPr><w:lang w:val=\"en-GB\"/></w:rPr>"
        runs.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    if "\\" in text or "{" in text:
        sys.exit(f"the abstract holds LaTeX this script does not convert: {text}")
    return "".join(runs)


def title_block(template_doc: str, tex: str, full: bool) -> str:
    """The template's own first paragraphs, with the text of the paper."""
    paras = re.findall(r"<w:p[ >].*?</w:p>", template_doc.split("<w:body>", 1)[1], flags=re.DOTALL)
    by_text = {text_of(p).strip(): p for p in paras[:10]}
    copyright_p = next(p for p in paras[:10] if "<w:sectPr" in p)
    abstract_head = by_text["Abstract"]

    def para(style: str, runs: str, ppr_extra: str = "") -> str:
        return f'<w:p><w:pPr><w:pStyle w:val="{style}"/>{ppr_extra}</w:pPr>{runs}</w:p>'

    def r(text: str, rpr: str = "") -> str:
        return (f'<w:r><w:rPr>{rpr}<w:lang w:val="en-GB"/></w:rPr>'
                f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r>')

    title = re.search(r"\{\\Large\\bfseries (.*?)\\par\}", tex).group(1)
    abstract = re.search(r"\\textbf\{Abstract\}\\par\s*\\smallskip(.*?)\\medskip", tex,
                         flags=re.DOTALL).group(1)
    keywords = " ".join(re.search(r"\\textit\{Keywords\}:(.*?)\\medskip", tex,
                                  flags=re.DOTALL).group(1).split())
    sup = '<w:vertAlign w:val="superscript"/>'
    base = '<w:vertAlign w:val="baseline"/>'
    out = [para("Papertitle", r(title), "<w:suppressAutoHyphens/>")]
    if full:
        out.append(para("Authors", r(AUTHOR) + r("a,", sup) + r("*")))
        out.append(para("Affilation", r("a") + r(" " + AFFILIATION, base)))
    else:
        out.append(para("Authors", r(BLIND_AUTHOR)))
    out.append(abstract_head)
    out.append(para("Abstract", abstract_runs(abstract)))
    out.append(para("Keywords", r("Keywords", "<w:i/><w:iCs/>") + r(": " + keywords)))
    if full:
        size = '<w:sz w:val="16"/><w:szCs w:val="16"/>'
        out.append(para("Footnote", '<w:r><w:rPr><w:rStyle w:val="Odwoanieprzypisudolnego"/>'
                        "</w:rPr><w:t>*</w:t></w:r><w:r><w:t>Corresponding author</w:t></w:r>"))
        out.append(para("Keywords", r("Email address", "<w:i/><w:iCs/>" + size)
                        + r(f": {EMAIL} (J. Herrera-V\u00e1squez). ", size)
                        + r("ORCID", "<w:i/><w:iCs/>" + size)
                        + r(f": https://orcid.org/{ORCID}", size)))
    out.append(copyright_p)
    return "".join(out)


def merge_namespaces(template_doc: str, pandoc_doc: str) -> str:
    """Declare on the template's root the prefixes pandoc uses and the template lacks."""
    troot = re.search(r"<w:document [^>]*>", template_doc).group(0)
    proot = re.search(r"<w:document [^>]*>", pandoc_doc).group(0)
    have = set(re.findall(r"xmlns:(\w+)=", troot))
    extra = "".join(f' xmlns:{p}="{u}"' for p, u in re.findall(r'xmlns:(\w+)="([^"]+)"', proot)
                    if p not in have)
    return template_doc.replace(troot, troot[:-1] + extra + ">", 1)


def assemble(full: bool, tex: str, refs: list[tuple[str, str]]) -> Path:
    name = FULL_NAME if full else "paper_f_blind"
    tex = resolve_full(tex, full)
    src = F / f"_{name}_pandoc.tex"
    tmp = OUT / f"_{name}_pandoc.docx"
    src.write_text(pandoc_source(tex, refs), encoding="utf-8")
    try:
        run(["quarto", "pandoc", src.name, "-f", "latex", "-t", "docx", "-o", str(tmp),
             "--resource-path=."], F)
    finally:
        src.unlink(missing_ok=True)

    with zipfile.ZipFile(tmp) as zp:
        pandoc_doc = zp.read("word/document.xml").decode("utf-8")
        pandoc_rels = zp.read("word/_rels/document.xml.rels").decode("utf-8")
        pandoc_media = {n: zp.read(n) for n in zp.namelist() if n.startswith("word/media/")}
    tmp.unlink()

    with zipfile.ZipFile(TEMPLATE) as zt:
        template_doc = zt.read("word/document.xml").decode("utf-8")
        template_rels = zt.read("word/_rels/document.xml.rels").decode("utf-8")
        body, equations = convert_body(pandoc_doc, template_doc)
        if equations != tex.count("\\begin{equation}"):
            sys.exit("the equations found in Word are not those of the source")
        body = scale_figure(body, F / "figures" / "fig1.png")

        # Relationships of pandoc (links, the figure) under new ids; its media under new names.
        new_rels, media = [], {}
        for rel in re.findall(r"<Relationship [^>]*>", pandoc_rels):
            attr = dict(re.findall(r'(\w+)="([^"]*)"', rel))
            rid, rtype, target = attr["Id"], attr["Type"], attr["Target"]
            mode = ' TargetMode="External"' if attr.get("TargetMode") == "External" else ""
            kind = rtype.rsplit("/", 1)[1]
            if kind not in ("hyperlink", "image") or f'"{rid}"' not in body:
                continue
            new = f"rIdPF{len(new_rels) + 1}"
            body = body.replace(f'"{rid}"', f'"{new}"')
            if kind == "image":
                data = pandoc_media["word/" + target]
                target = f"media/paperf_{len(media) + 1}{Path(target).suffix}"
                media["word/" + target] = data
            new_rels.append(f'<Relationship Id="{new}" Type="{rtype}" Target="{target}"{mode}/>')

        block = title_block(template_doc, tex, full)
        final_sect = re.findall(r"<w:sectPr.*?</w:sectPr>", template_doc, flags=re.DOTALL)[1]
        body = body.replace(HEADER_SLOT,
                            re.search(r"<w:headerReference [^>]*/>", final_sect).group(0))
        head = merge_namespaces(template_doc, pandoc_doc)
        head = head[:head.index("<w:body>") + len("<w:body>")]
        document = head + block + body + final_sect + "</w:body></w:document>"

        # Relationships and media of the template's sample text that the body no longer uses.
        kept = []
        for rel in re.findall(r"<Relationship [^>]*/>", template_rels):
            rid = re.search(r'Id="([^"]+)"', rel).group(1)
            kind = re.search(r'Type="[^"]*/([^"/]+)"', rel).group(1)
            if kind in ("hyperlink", "image") and f'"{rid}"' not in document:
                continue
            kept.append(rel)
        rels = (template_rels[:template_rels.index("<Relationship ")] + "".join(kept + new_rels)
                + "</Relationships>")
        used_media = set(re.findall(r'Target="(media/[^"]+)"', rels))
        for n in zt.namelist():
            if n.startswith("word/_rels/") and n != "word/_rels/document.xml.rels":
                used_media |= set(re.findall(r'Target="(media/[^"]+)"', zt.read(n).decode("utf-8")))

        out = OUT / f"{name}.docx"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zo:
            for item in zt.infolist():
                n = item.filename
                data = zt.read(n)
                if n == "word/document.xml":
                    data = document.encode("utf-8")
                elif n == "word/_rels/document.xml.rels":
                    data = rels.encode("utf-8")
                elif n.startswith("word/media/") and n[len("word/"):] not in used_media:
                    continue
                elif n == "docProps/core.xml":
                    data = core_properties(data.decode("utf-8"), tex, full).encode("utf-8")
                elif n == "docProps/thumbnail.emf":
                    continue                      # a picture of the template's first page
                elif n == "_rels/.rels":
                    data = re.sub(rb'<Relationship [^>]*thumbnail[^>]*/>', b"", data)
                elif n == "[Content_Types].xml":
                    text = data.decode("utf-8")
                    for ext, mime in (("png", "image/png"), ("jpeg", "image/jpeg")):
                        if any(m.endswith("." + ext) for m in media) and f'Extension="{ext}"' not in text:
                            text = text.replace("<Default ", f'<Default Extension="{ext}" '
                                                f'ContentType="{mime}"/><Default ', 1)
                    data = text.encode("utf-8")
                zo.writestr(n, data)      # by name: the template's own entry records go stale
            for n, data in media.items():
                zo.writestr(n, data)
    return out


def core_properties(xml: str, tex: str, full: bool) -> str:
    title = re.search(r"\{\\Large\\bfseries (.*?)\\par\}", tex).group(1)
    who = AUTHOR if full else ""
    xml = re.sub(r"<dc:creator>.*?</dc:creator>|<dc:creator/>", f"<dc:creator>{escape(who)}</dc:creator>", xml)
    xml = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>|<cp:lastModifiedBy/>",
                 f"<cp:lastModifiedBy>{escape(who)}</cp:lastModifiedBy>", xml)
    return re.sub(r"<dc:title>.*?</dc:title>|<dc:title/>", f"<dc:title>{escape(title)}</dc:title>", xml)


WORD_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
  $doc = $word.Documents.Open($args[0], $false, $false)
  $doc.Fields.Update() | Out-Null
  $doc.Repaginate()
  $pages = $doc.ComputeStatistics(2)
  $doc.Save()
  # The ninth argument is IncludeDocProps: the blind PDF carries no document properties.
  $props = $args[2] -eq 'full'
  $doc.ExportAsFixedFormat($args[1], 17, $false, 0, 0, 0, 0, 0, $props)
  $doc.Close($false)
  Write-Output "pages=$pages"
} finally { $word.Quit() }
"""


def word_pass(docx: Path, full: bool, tex: str) -> int:
    """Word updates the fields, repaginates, saves, prints the PDF; returns the pages."""
    script = OUT / "_word.ps1"
    script.write_text(WORD_SCRIPT, encoding="utf-8")
    # The full file takes the journal's name for both; the blind PDF is told apart from
    # the LaTeX one of build_paper_f.py.
    pdf = docx.with_suffix(".pdf") if full else docx.with_name(docx.stem + "_word.pdf")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                            str(script), str(docx), str(pdf), "full" if full else "blind"],
                           capture_output=True, text=True)
    finally:
        script.unlink(missing_ok=True)
    m = re.search(r"pages=(\d+)", r.stdout)
    if r.returncode or not m:
        sys.exit(f"Word failed on {docx.name}:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")
    # Word signs the file it saves with the name of the Windows user; set the properties again.
    tmp = docx.with_suffix(".tmp")
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in zin.namelist():
            data = zin.read(n)
            if n == "docProps/core.xml":
                data = core_properties(data.decode("utf-8"), tex, full).encode("utf-8")
            zout.writestr(n, data)
    tmp.replace(docx)
    if not full:
        leaks = [w for w in ("Herrera", EMAIL, ORCID, "zenodo", "UNADE") for n in ("docProps/core.xml", "docProps/app.xml")
                 if w.lower() in zipfile.ZipFile(docx).read(n).decode("utf-8", "ignore").lower()]
        raw = pdf.read_bytes()
        leaks += [f"PDF:{w}" for w in (EMAIL, ORCID, "Jonathan") if w.encode() in raw
                  or w.encode("utf-16-be") in raw]
        if leaks:
            sys.exit(f"{docx.name}: the blind files carry author data: {leaks}")
    return int(m.group(1))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-pdf", action="store_true", help="do not open Word")
    args = ap.parse_args()
    if not TEMPLATE.exists():
        sys.exit(f"the journal's template is not at {TEMPLATE.relative_to(ROOT)}; download it "
                 "from the journal site (VENUE_JCSI.md)")
    if shutil.which("quarto") is None:
        sys.exit("quarto (for its pandoc) is not installed")
    OUT.mkdir(exist_ok=True)
    tex = (F / "paper_f.tex").read_text(encoding="utf-8")
    if "\\pending{" in tex.split("\\begin{document}", 1)[1]:
        sys.exit("paper_f.tex still has pending marks; run build_paper_f.py --final first")
    refs = reference_list()
    for full in (False, True):
        docx = assemble(full, tex, refs)
        line = f"docx  {docx.relative_to(ROOT)}"
        if not args.no_pdf:
            pages = word_pass(docx, full, tex)
            line += f" ({pages} pages in Word)"
            if pages > MAX_PAGES:
                line += f"  WARNING: the journal's limit is {MAX_PAGES}"
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
