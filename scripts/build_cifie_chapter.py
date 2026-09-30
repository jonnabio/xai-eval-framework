#!/usr/bin/env python3
"""Build the CIFIE/FOM-7 book chapter as a Word document.

Assembles publications/book_chapters/2026_cifie_xai_fom7/manuscript/01..11 in
order, adds the title and authors from the editorial design sheet, appends the
APA 7 reference list from references/references_apa7.md, and converts the
result with the Pandoc bundled with Quarto. Citations are already written in
APA 7 author-date form in the sources, so no citation processing runs; the
reference list gets a hanging indent, as the submission notes require.

Tables 1-4 live in tables/*.md in final APA 7 form (bold number, italic
title, table, *Nota.*). Each is placed where the text first cites it, through
a marker line `<!-- TABLA: <file>.md -->` in the manuscript. The build fails
if a marker names a missing file, if a table file is placed twice, or if a
table file is never placed.

Requirements: pandoc (bundled with Quarto), python-docx and Pillow. The
figures are not drawn here: fig_cd_diagram_es.png comes from
scripts/generate_cifie_chapter_figures.py and the other five from
scripts/generate_spanish_thesis_figures.py (both need matplotlib and pandas);
see figures/figure_registry.md.

Usage: python scripts/build_cifie_chapter.py [--out PATH]
"""
from __future__ import annotations

import argparse
import io
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "publications" / "book_chapters" / "2026_cifie_xai_fom7"
MANUSCRIPT = CHAPTER / "manuscript"
PANDOC_CANDIDATES = [
    Path(r"C:\Program Files\Quarto\bin\tools\pandoc.exe"),
    Path("/usr/lib/rstudio/resources/app/bin/quarto/bin/tools/pandoc"),
]


def find_pandoc() -> str:
    for candidate in PANDOC_CANDIDATES:
        if candidate.exists():
            return str(candidate)
    found = shutil.which("pandoc")
    if found:
        return found
    raise SystemExit("pandoc not found: install Quarto (it bundles pandoc) or pandoc itself")


def design_sheet() -> tuple[str, list[str], str]:
    sheet = (MANUSCRIPT / "00_hoja_diseno_editorial.md").read_text(encoding="utf-8")

    def section(name: str) -> str:
        m = re.search(rf"^## {name}\n+(.*?)(?=\n## |\Z)", sheet, flags=re.S | re.M)
        return m.group(1).strip() if m else ""

    title = section("Título provisional")
    authors = [a.lstrip("- ").strip() for a in section("Autoría").splitlines() if a.strip()]
    affiliation = section("Afiliación institucional")
    return title, authors, affiliation


TABLE_MARKER = re.compile(r"^<!-- TABLA: ([\w.-]+\.md) -->$", flags=re.M)
SOURCE_PROVENANCE = re.compile(
    r"^[ \t]*Fuente inicial\s*:.*(?:\r?\n|$)",
    flags=re.I | re.M,
)


def place_tables(body: str) -> tuple[str, int]:
    """Replace each table marker with the table file's content."""
    tables_dir = CHAPTER / "tables"
    placed = TABLE_MARKER.findall(body)
    available = sorted(p.name for p in tables_dir.glob("table_*.md"))
    if len(placed) != len(set(placed)):
        raise SystemExit(f"table placed more than once: {placed}")
    missing = [t for t in placed if not (tables_dir / t).exists()]
    unused = [t for t in available if t not in placed]
    if missing or unused:
        raise SystemExit(f"table markers: missing files {missing}, unplaced tables {unused}")
    body = TABLE_MARKER.sub(lambda m: (tables_dir / m.group(1)).read_text(encoding="utf-8").strip(), body)
    return body, len(placed)


def references() -> str:
    text = (CHAPTER / "references" / "references_apa7.md").read_text(encoding="utf-8")
    entries = [
        line for line in text.splitlines()
        if line.strip() and not line.startswith("#") and not line.startswith("Estado:")
    ]
    body = "\n\n".join(entries)
    return f'# Referencias\n\n::: {{custom-style="Bibliography"}}\n{body}\n:::\n'


def reader_facing_body(body: str) -> str:
    """Remove authoring-only provenance notes from the reader-facing build.

    The source paths remain in the Markdown files and inventories, where they are
    useful for traceability, but they are not chapter prose and should not appear
    in the submission document.
    """
    return SOURCE_PROVENANCE.sub("", body)


def format_data_tables(docx: Path) -> None:
    """Apply readable, deterministic widths and pagination to the four APA tables."""
    try:
        from docx import Document
        from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from docx.shared import Cm, Pt
    except ImportError as exc:  # pragma: no cover - environment guard
        raise SystemExit("python-docx is required for CIFIE table formatting") from exc

    # Widths sum to the 13.97 cm text block. The allocations protect short label
    # columns from mid-word breaks while preserving space for substantive content.
    width_specs_cm = [
        [2.10, 2.65, 2.40, 3.35, 3.47],
        [2.80, 2.35, 4.25, 4.57],
        [3.00, 1.45, 4.55, 2.80, 2.17],
        [3.31, 2.20, 2.20, 3.31, 2.95],
    ]

    document = Document(docx)
    if len(document.tables) != len(width_specs_cm):
        raise SystemExit(
            f"expected {len(width_specs_cm)} data tables, found {len(document.tables)}"
        )

    for table, widths in zip(document.tables, width_specs_cm):
        if len(table.columns) != len(widths):
            raise SystemExit(
                f"table width specification has {len(widths)} columns; "
                f"document table has {len(table.columns)}"
            )
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        tbl_pr = table._tbl.tblPr
        layout = tbl_pr.find(qn("w:tblLayout"))
        if layout is None:
            layout = OxmlElement("w:tblLayout")
            tbl_pr.append(layout)
        layout.set(qn("w:type"), "fixed")

        # Pandoc writes a tblGrid that Word/LibreOffice treats as authoritative.
        # Setting only tcW leaves those original grid widths in place, so update
        # both representations to make the intended widths survive rendering.
        grid_columns = table._tbl.tblGrid.gridCol_lst
        if len(grid_columns) != len(widths):
            raise SystemExit(
                f"table grid has {len(grid_columns)} columns; expected {len(widths)}"
            )
        for column, grid_column, width_cm in zip(table.columns, grid_columns, widths):
            width = Cm(width_cm)
            column.width = width
            grid_column.set(qn("w:w"), str(int(width.emu / 635)))

        for row_index, row in enumerate(table.rows):
            tr_pr = row._tr.get_or_add_trPr()
            if tr_pr.find(qn("w:cantSplit")) is None:
                tr_pr.append(OxmlElement("w:cantSplit"))
            if row_index == 0 and tr_pr.find(qn("w:tblHeader")) is None:
                tr_pr.append(OxmlElement("w:tblHeader"))

            for cell, width_cm in zip(row.cells, widths):
                width = Cm(width_cm)
                cell.width = width
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
                tc_pr = cell._tc.get_or_add_tcPr()
                tc_w = tc_pr.find(qn("w:tcW"))
                if tc_w is None:
                    tc_w = OxmlElement("w:tcW")
                    tc_pr.append(tc_w)
                tc_w.set(qn("w:w"), str(int(width.emu / 635)))
                tc_w.set(qn("w:type"), "dxa")
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.space_after = Pt(0)
                    paragraph.paragraph_format.line_spacing = 1.0
                    for run in paragraph.runs:
                        run.font.size = Pt(10)

    document.save(docx)


def format_academic_text(docx: Path) -> None:
    """Apply the chapter-wide black, justified, 1.5-spaced text standard.

    Prose, captions, references, and table text are justified. Titles remain
    centered, headings remain left-aligned, and image-only paragraphs retain
    their placement so the layout hierarchy is not damaged by blanket styling.
    """
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from docx.shared import RGBColor
    except ImportError as exc:  # pragma: no cover - environment guard
        raise SystemExit("python-docx is required for CIFIE text formatting") from exc

    document = Document(docx)

    # Make every text and character style explicitly black and 1.5-spaced.
    # Explicit black removes theme-color fallbacks that otherwise render the
    # default Word headings and hyperlinks in blue.
    for style in document.styles:
        if getattr(style, "font", None) is not None:
            style.font.color.rgb = RGBColor(0, 0, 0)
        if getattr(style, "paragraph_format", None) is not None:
            style.paragraph_format.line_spacing = 1.5

    def iter_container_paragraphs(container):
        yield from container.paragraphs
        for table in container.tables:
            for row in table.rows:
                for cell in row.cells:
                    yield from iter_container_paragraphs(cell)

    stories = [document]
    seen_story_elements = {id(document.element.body)}
    for section in document.sections:
        for story in (
            section.header,
            section.first_page_header,
            section.even_page_header,
            section.footer,
            section.first_page_footer,
            section.even_page_footer,
        ):
            element_id = id(story._element)
            if element_id not in seen_story_elements:
                seen_story_elements.add(element_id)
                stories.append(story)

    for story in stories:
        for paragraph in list(iter_container_paragraphs(story)):
            if SOURCE_PROVENANCE.match(paragraph.text):
                paragraph._element.getparent().remove(paragraph._element)
                continue

            paragraph.paragraph_format.line_spacing = 1.5
            style_name = paragraph.style.name if paragraph.style is not None else ""
            has_drawing = paragraph._p.find(".//" + qn("w:drawing")) is not None
            in_table = paragraph._p.getparent().tag == qn("w:tc")
            if paragraph.text.strip():
                if style_name == "Title":
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif style_name == "Author":
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif style_name.startswith("Heading"):
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                elif in_table:
                    # Full justification produces distracting gaps in narrow
                    # columns; conventional left alignment keeps tables legible.
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                else:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            elif has_drawing:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # paragraph.runs omits runs nested inside hyperlinks in some
            # python-docx versions, so operate on every w:r node directly.
            for run_element in paragraph._p.iter(qn("w:r")):
                run_properties = run_element.find(qn("w:rPr"))
                if run_properties is None:
                    run_properties = OxmlElement("w:rPr")
                    run_element.insert(0, run_properties)
                color = run_properties.find(qn("w:color"))
                if color is None:
                    color = OxmlElement("w:color")
                    run_properties.append(color)
                color.set(qn("w:val"), "000000")
                for attribute in ("themeColor", "themeTint", "themeShade"):
                    qualified = qn(f"w:{attribute}")
                    if qualified in color.attrib:
                        del color.attrib[qualified]

    document.save(docx)


def hanging_indent(docx: Path) -> None:
    """Give the Bibliography paragraph style a 0.5-inch hanging indent."""
    tmp = docx.with_suffix(".tmp.docx")
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                xml = data.decode("utf-8")
                pattern = re.compile(r'(<w:style [^>]*w:styleId="Bibliography"[^>]*>.*?)(</w:style>)', re.S)
                m = pattern.search(xml)
                if m and "w:hanging" not in m.group(1):
                    block = m.group(1)
                    ind = '<w:ind w:left="720" w:hanging="720"/>'
                    if "<w:pPr>" in block:
                        block = block.replace("<w:pPr>", "<w:pPr>" + ind, 1)
                    else:
                        block = block + f"<w:pPr>{ind}</w:pPr>"
                    xml = xml[: m.start()] + block + m.group(2) + xml[m.end():]
                data = xml.encode("utf-8")
            zout.writestr(item, data)
    tmp.replace(docx)


def monochrome_embedded_images(docx: Path) -> None:
    """Convert embedded raster figures to grayscale for black-ink output.

    The source figures remain unchanged; only the copies packaged in the Word
    document are transformed. Existing OOXML image extents are preserved.
    """
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:  # pragma: no cover - environment guard
        raise SystemExit("Pillow is required for black-ink CIFIE figures") from exc

    supported = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG"}
    tmp = docx.with_suffix(".monochrome.tmp.docx")
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            suffix = Path(item.filename).suffix.lower()
            if item.filename.startswith("word/media/") and suffix in supported:
                with Image.open(io.BytesIO(data)) as image:
                    if "A" in image.getbands():
                        rgba = image.convert("RGBA")
                        background = Image.new("RGBA", rgba.size, "white")
                        image = Image.alpha_composite(background, rgba).convert("RGB")
                    else:
                        image = image.convert("RGB")
                    grayscale = ImageOps.grayscale(image).convert("RGB")
                    output = io.BytesIO()
                    save_options = {"format": supported[suffix]}
                    if supported[suffix] == "JPEG":
                        save_options.update({"quality": 95, "subsampling": 0})
                    grayscale.save(output, **save_options)
                    data = output.getvalue()
            zout.writestr(item, data)
    tmp.replace(docx)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    default_out = CHAPTER / "drafts" / "v3_editorial_review" / f"cifie_xai_fom7_{date.today():%Y-%m-%d}.docx"
    parser.add_argument("--out", type=Path, default=default_out)
    args = parser.parse_args()

    sections = sorted(p for p in MANUSCRIPT.glob("[01][0-9]_*.md") if not p.name.startswith("00_"))
    if [p.name[:2] for p in sections] != [f"{i:02d}" for i in range(1, 12)]:
        raise SystemExit(f"expected sections 01..11, found {[p.name for p in sections]}")

    title, authors, affiliation = design_sheet()
    header = "---\n" f'title: "{title}"\n' "author:\n" + "".join(
        f'  - "{a}, {affiliation}"\n' for a in authors) + "lang: es-ES\n---\n\n"
    body = "\n\n".join(p.read_text(encoding="utf-8").strip() for p in sections)
    body, n_tables = place_tables(body)
    body = reader_facing_body(body)
    source = header + body + "\n\n" + references()

    args.out = args.out.resolve()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        md = Path(tmp) / "chapter.md"
        md.write_text(source, encoding="utf-8")
        subprocess.run(
            [find_pandoc(), str(md), "-f", "markdown", "-t", "docx",
             "--resource-path", str(MANUSCRIPT), "-o", str(args.out)],
            check=True,
        )
    format_data_tables(args.out)
    format_academic_text(args.out)
    hanging_indent(args.out)
    monochrome_embedded_images(args.out)

    words = len(re.findall(r"\w+", body))
    shown = args.out.relative_to(ROOT) if args.out.is_relative_to(ROOT) else args.out
    print(f"OK: {len(sections)} sections, {n_tables} tables, ~{words} words -> {shown.as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
