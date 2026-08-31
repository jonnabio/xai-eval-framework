#!/usr/bin/env python3
"""Enforce thesis DOCX paragraph formatting.

The script patches WordprocessingML inside a .docx file so Quarto renders keep
paragraph text justified and line spacing at 1.5, and so page numbers are Arabic
throughout. It is intentionally stdlib-only so it works even when python-docx is
unavailable.

Page numbering: the reference template carries four sections, the first of which
numbers its pages in lower-case Roman numerals for the front matter. Pandoc
collapses the book into a single section and inherits that first `sectPr`, so
the Roman numbering leaks onto the whole thesis. `set_page_numbering` forces
every section in a rendered output back to `decimal`.
"""

from __future__ import annotations

import argparse
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}
ET.register_namespace("w", W_NS)


def qn(local: str) -> str:
    return f"{{{W_NS}}}{local}"


def ensure_child(parent: ET.Element, tag: str) -> ET.Element:
    child = parent.find(f"w:{tag}", NS)
    if child is None:
        child = ET.SubElement(parent, qn(tag))
    return child


def set_paragraph_format(ppr: ET.Element) -> None:
    spacing = ensure_child(ppr, "spacing")
    spacing.set(qn("line"), "360")
    spacing.set(qn("lineRule"), "auto")

    jc = ensure_child(ppr, "jc")
    jc.set(qn("val"), "both")


def patch_styles_xml(xml_bytes: bytes) -> bytes:
    root = ET.fromstring(xml_bytes)

    doc_defaults = ensure_child(root, "docDefaults")
    ppr_default = ensure_child(doc_defaults, "pPrDefault")
    ppr = ensure_child(ppr_default, "pPr")
    set_paragraph_format(ppr)

    for style in root.findall("w:style", NS):
        if style.get(qn("type")) != "paragraph":
            continue
        ppr = ensure_child(style, "pPr")
        set_paragraph_format(ppr)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


# Child order inside w:sectPr is fixed by the schema; w:pgNumType sits after
# these and before everything else (w:cols onwards).
SECTPR_BEFORE_PGNUMTYPE = (
    "footnotePr",
    "endnotePr",
    "type",
    "pgSz",
    "pgMar",
    "paperSrc",
    "pgBorders",
    "lnNumType",
)


def set_page_numbering(sectpr: ET.Element, fmt: str = "decimal") -> None:
    """Force one section's page numbers to `fmt`, inserting w:pgNumType if absent."""
    pg_num = sectpr.find("w:pgNumType", NS)
    if pg_num is None:
        pg_num = ET.Element(qn("pgNumType"))
        index = 0
        for i, child in enumerate(sectpr):
            tag = child.tag.split("}")[-1]
            if tag in SECTPR_BEFORE_PGNUMTYPE:
                index = i + 1
        sectpr.insert(index, pg_num)
    pg_num.set(qn("fmt"), fmt)
    if pg_num.get(qn("start")) is None:
        pg_num.set(qn("start"), "1")


# --- Cover page -------------------------------------------------------------

TITLE_BLOCK_STYLES = {"Title", "Subtitle", "Author", "Date"}


def load_cover(path: Path) -> list[tuple[str, str]]:
    """Parse `STYLE|TEXT` lines into (style, text) pairs; `|` alone is a spacer."""
    items: list[tuple[str, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        style, _, text = line.partition("|")
        items.append((style.strip(), text.strip()))
    return items


def make_paragraph(style: str, text: str) -> ET.Element:
    """A centred, single-spaced paragraph. Direct formatting is deliberate: it
    overrides the justified 1.5 spacing that patch_styles_xml applies to every
    style, which is right for body prose and wrong for a cover."""
    p = ET.Element(qn("p"))
    ppr = ET.SubElement(p, qn("pPr"))
    if style:
        ET.SubElement(ppr, qn("pStyle")).set(qn("val"), style)
    spacing = ET.SubElement(ppr, qn("spacing"))
    spacing.set(qn("line"), "240")
    spacing.set(qn("lineRule"), "auto")
    ET.SubElement(ppr, qn("jc")).set(qn("val"), "center")
    if text:
        run = ET.SubElement(p, qn("r"))
        node = ET.SubElement(run, qn("t"))
        node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        node.text = text
    return p


def make_page_break() -> ET.Element:
    p = ET.Element(qn("p"))
    run = ET.SubElement(p, qn("r"))
    ET.SubElement(run, qn("br")).set(qn("type"), "page")
    return p


def insert_cover_page(root: ET.Element, items: list[tuple[str, str]]) -> bool:
    """Swap the leading Quarto title block for the cover. Returns True if applied.

    Only the *leading* run of title-block paragraphs is removed: the same styles
    recur later in the document and must be left alone.
    """
    body = root.find("w:body", NS)
    if body is None:
        return False

    children = list(body)
    end = 0
    for child in children:
        if child.tag != qn("p"):
            break
        style = child.find("w:pPr/w:pStyle", NS)
        if style is None or style.get(qn("val")) not in TITLE_BLOCK_STYLES:
            break
        end += 1

    for child in children[:end]:
        body.remove(child)

    for offset, (style, text) in enumerate(items):
        body.insert(offset, make_paragraph(style, text))
    body.insert(len(items), make_page_break())
    return True


def insert_break_after_toc(root: ET.Element) -> bool:
    """Start the first chapter on its own page.

    Quarto promotes a chapter file's first level-1 heading to the chapter title
    when the file declares no `title`, hoisting it above everything else in the
    file -- so a page break written at the top of index.qmd lands *after* that
    heading and strands it on the TOC page. Inserting the break here, right
    after the TOC block, is immune to that reordering.
    """
    body = root.find("w:body", NS)
    if body is None:
        return False
    for index, child in enumerate(body):
        if child.tag == qn("sdt"):
            body.insert(index + 1, make_page_break())
            return True
    return False


# --- Section numbering ------------------------------------------------------

HEADING_STYLE = re.compile(r"^(?:Ttulo|Titulo|Heading)(\d)$")


def collect_unnumbered_titles(source_dir: Path) -> set[str]:
    """Heading texts marked `{.unnumbered}` in the Quarto sources.

    The rendered DOCX gives numbered and unnumbered headings the identical
    style and pPr, so the output alone cannot distinguish them; the sources can.
    """
    titles: set[str] = set()
    for qmd in sorted(source_dir.glob("*.qmd")):
        for line in qmd.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^#+\s+(.*?)\s*\{([^}]*)\}\s*$", line)
            if m and ".unnumbered" in m.group(2):
                titles.add(m.group(1).strip())
    return titles


def number_headings(root: ET.Element, unnumbered: set[str]) -> int:
    """Prefix headings with 1, 1.1, 1.1.1 ... matching Quarto's own counting.

    Quarto computes these numbers for `@sec-` crossrefs but pandoc's docx
    writer never puts them on the headings, so every "Seccion 3.6" reference
    pointed at a label the document did not show. Numbering here rather than in
    the .docx template keeps the rule in version control.

    An unnumbered level-1 heading suppresses numbering for everything beneath
    it, which is what keeps Resumen, Introduccion, Referencias and the
    self-lettered Apendices (A, B, C.1 ...) out of the sequence.
    """
    body = root.find("w:body", NS)
    if body is None:
        return 0
    counters = [0] * 10
    skipping = False
    applied = 0
    for para in body.findall("w:p", NS):
        style = para.find("w:pPr/w:pStyle", NS)
        if style is None:
            continue
        match = HEADING_STYLE.match(style.get(qn("val")) or "")
        if not match:
            continue
        level = int(match.group(1))
        text = "".join(node.text or "" for node in para.iter(qn("t"))).strip()
        if level == 1:
            skipping = text in unnumbered
            if skipping:
                continue
        elif skipping:
            continue
        counters[level] += 1
        for deeper in range(level + 1, len(counters)):
            counters[deeper] = 0
        label = ".".join(str(counters[i]) for i in range(1, level + 1))

        run = ET.Element(qn("r"))
        node = ET.SubElement(run, qn("t"))
        node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        node.text = f"{label} "
        para.insert(1, run)  # after w:pPr
        applied += 1
    return applied


# Child order inside w:pPr is fixed by the schema; only the members this script
# touches or preserves are listed, and anything unknown is appended after them.
PPR_ORDER = (
    "pStyle",
    "keepNext",
    "keepLines",
    "pageBreakBefore",
    "framePr",
    "widowControl",
    "numPr",
    "pBdr",
    "shd",
    "tabs",
    "bidi",
    "spacing",
    "ind",
    "contextualSpacing",
    "jc",
    "textDirection",
    "textAlignment",
    "outlineLvl",
    "rPr",
    "sectPr",
)


def merge_paragraph_properties(root) -> int:
    """Collapse duplicate w:pPr elements into one, in schema order.

    A w:p may carry at most one w:pPr and it must come first. Earlier revisions
    of this script inserted a fresh w:pPr at index 0 whenever `find` missed the
    existing one, which left all 44 caption paragraphs with two: an injected one
    holding the justification, ahead of pandoc's, which holds `pStyle`. Word
    honours the first and the caption style is lost -- and any lookup by style
    finds the wrong element. Later definitions win, so pandoc's pStyle survives.
    """
    fixed = 0
    for para in root.iter(qn("p")):
        pprs = [child for child in para if child.tag == qn("pPr")]
        if len(pprs) < 2:
            continue
        merged: dict[str, ET.Element] = {}
        for ppr in pprs:
            for child in ppr:
                merged[child.tag.split("}")[-1]] = child
            para.remove(ppr)
        combined = ET.Element(qn("pPr"))
        for tag in PPR_ORDER:
            if tag in merged:
                combined.append(merged.pop(tag))
        for leftover in merged.values():
            combined.append(leftover)
        para.insert(0, combined)
        fixed += 1
    return fixed


# --- Tables and figures -----------------------------------------------------

# Child order inside w:tblPr is fixed by the schema. w:jc sits after these,
# and w:tblBorders after those plus jc/tblCellSpacing/tblInd.
TBLPR_BEFORE_JC = (
    "tblStyle",
    "tblpPr",
    "tblOverlap",
    "bidiVisual",
    "tblStyleRowBandSize",
    "tblStyleColBandSize",
    "tblW",
)
TBLPR_BEFORE_BORDERS = TBLPR_BEFORE_JC + ("jc", "tblCellSpacing", "tblInd")

# Order inside w:tblBorders is also fixed.
BORDER_EDGES = ("top", "left", "bottom", "right", "insideH", "insideV")

CAPTION_STYLES = {"ImageCaption", "TableCaption", "Descripcin", "Leyenda"}


def _insert_ordered(parent, tag, before_tags):
    """Insert (or find) a child, respecting the schema's fixed child order."""
    existing = parent.find(f"w:{tag}", NS)
    if existing is not None:
        return existing
    node = ET.Element(qn(tag))
    index = 0
    for i, child in enumerate(parent):
        if child.tag.split("}")[-1] in before_tags:
            index = i + 1
    parent.insert(index, node)
    return node


def set_table_borders(tblpr):
    """Give a table solid black gridlines on every edge.

    The rendered tables reference a table style named "Table" that the reference
    template does not define, and neither w:tblBorders nor w:tcBorders appears
    anywhere in the output, so they arrive in Word with no rules at all. No cell
    overrides them, so setting the borders once at table level covers every cell.
    """
    borders = _insert_ordered(tblpr, "tblBorders", TBLPR_BEFORE_BORDERS)
    for edge in BORDER_EDGES:
        node = borders.find(f"w:{edge}", NS)
        if node is None:
            node = ET.SubElement(borders, qn(edge))
        node.set(qn("val"), "single")
        node.set(qn("sz"), "4")
        node.set(qn("space"), "0")
        node.set(qn("color"), "000000")


def format_tables(root) -> tuple[int, int]:
    """Centre every table; give solid black borders to the data tables only.

    Pandoc wraps each captioned table in a single-cell table that holds the
    caption and the real table together, so the document has two tbl elements
    per captioned table. Centring both is right -- it centres the whole block --
    but bordering both would draw a second box around caption and table. Borders
    therefore go only to leaf tables, those containing no nested table, which is
    also how the document looked before: the wrapper never had rules.
    """
    centred = bordered = 0
    for tbl in root.iter(qn("tbl")):
        tblpr = tbl.find("w:tblPr", NS)
        if tblpr is None:
            tblpr = ET.Element(qn("tblPr"))
            tbl.insert(0, tblpr)
        _insert_ordered(tblpr, "jc", TBLPR_BEFORE_JC).set(qn("val"), "center")
        centred += 1
        if not list(tbl.iter(qn("tbl")))[1:]:
            set_table_borders(tblpr)
            bordered += 1
    return centred, bordered


def centre_captions_and_figures(root) -> tuple[int, int]:
    """Centre caption paragraphs and the paragraphs holding an image.

    Runs after the global formatting sweep, which justifies every paragraph --
    correct for body prose, wrong for a caption or a figure. Pandoc gives table
    captions and figure captions the same style, so one rule covers both.
    """
    captions = figures = 0
    for para in root.iter(qn("p")):
        ppr = para.find("w:pPr", NS)
        if ppr is None:
            continue
        style = ppr.find("w:pStyle", NS)
        is_caption = style is not None and style.get(qn("val")) in CAPTION_STYLES
        is_figure = para.find(".//w:drawing", NS) is not None
        if not (is_caption or is_figure):
            continue
        jc = ppr.find("w:jc", NS)
        if jc is None:
            jc = ET.SubElement(ppr, qn("jc"))
        jc.set(qn("val"), "center")
        if is_caption:
            captions += 1
        else:
            figures += 1
    return captions, figures


def patch_document_xml(
    xml_bytes: bytes,
    cover: list[tuple[str, str]] | None = None,
    unnumbered: set[str] | None = None,
) -> bytes:
    root = ET.fromstring(xml_bytes)
    merge_paragraph_properties(root)
    for p in root.findall(".//w:p", NS):
        ppr = p.find("w:pPr", NS)
        if ppr is None:
            ppr = ET.Element(qn("pPr"))
            p.insert(0, ppr)
        set_paragraph_format(ppr)
    for sectpr in root.findall(".//w:sectPr", NS):
        set_page_numbering(sectpr)
    format_tables(root)
    centre_captions_and_figures(root)
    # After the formatting sweep, so the cover keeps its own centred spacing.
    if cover:
        insert_cover_page(root, cover)
        insert_break_after_toc(root)
    if unnumbered is not None:
        number_headings(root, unnumbered)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_docx(
    path: Path,
    patch_document: bool = False,
    backup: bool = True,
    cover: list[tuple[str, str]] | None = None,
    unnumbered: set[str] | None = None,
) -> None:
    if backup:
        backup_path = path.with_suffix(path.suffix + ".bak")
        if not backup_path.exists():
            shutil.copy2(path, backup_path)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp) / path.name
        with zipfile.ZipFile(path, "r") as zin, zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/styles.xml":
                    data = patch_styles_xml(data)
                elif patch_document and item.filename == "word/document.xml":
                    data = patch_document_xml(data, cover=cover, unnumbered=unnumbered)
                zout.writestr(item, data)
        shutil.move(str(tmp_path), path)


def inspect_docx(path: Path) -> None:
    with zipfile.ZipFile(path, "r") as zf:
        styles = ET.fromstring(zf.read("word/styles.xml"))
        ppr = styles.find("w:docDefaults/w:pPrDefault/w:pPr", NS)
        spacing = ppr.find("w:spacing", NS) if ppr is not None else None
        jc = ppr.find("w:jc", NS) if ppr is not None else None

        document = ET.fromstring(zf.read("word/document.xml"))
        page_formats = []
        for sectpr in document.findall(".//w:sectPr", NS):
            pg_num = sectpr.find("w:pgNumType", NS)
            page_formats.append(pg_num.get(qn("fmt")) if pg_num is not None else "decimal")

        print(
            {
                "path": str(path),
                "default_line": spacing.get(qn("line")) if spacing is not None else None,
                "default_line_rule": spacing.get(qn("lineRule")) if spacing is not None else None,
                "default_justification": jc.get(qn("val")) if jc is not None else None,
                "page_number_formats": page_formats,
            }
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", nargs="+", help="DOCX file(s) to patch")
    parser.add_argument(
        "--document",
        action="store_true",
        help="Also patch concrete paragraphs in word/document.xml, useful for generated outputs.",
    )
    parser.add_argument("--no-backup", action="store_true")
    parser.add_argument("--cover", help="Path to a cover definition file (STYLE|TEXT lines)")
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()
    cover = load_cover(Path(args.cover)) if args.cover else None

    for raw in args.docx:
        path = Path(raw)
        if args.inspect:
            inspect_docx(path)
        else:
            patch_docx(path, patch_document=args.document, backup=not args.no_backup, cover=cover)
            inspect_docx(path)


if __name__ == "__main__":
    main()
