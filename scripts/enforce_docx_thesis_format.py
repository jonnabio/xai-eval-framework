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


def patch_document_xml(
    xml_bytes: bytes, cover: list[tuple[str, str]] | None = None
) -> bytes:
    root = ET.fromstring(xml_bytes)
    for p in root.findall(".//w:p", NS):
        ppr = p.find("w:pPr", NS)
        if ppr is None:
            ppr = ET.Element(qn("pPr"))
            p.insert(0, ppr)
        set_paragraph_format(ppr)
    for sectpr in root.findall(".//w:sectPr", NS):
        set_page_numbering(sectpr)
    # After the formatting sweep, so the cover keeps its own centred spacing.
    if cover:
        insert_cover_page(root, cover)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_docx(
    path: Path,
    patch_document: bool = False,
    backup: bool = True,
    cover: list[tuple[str, str]] | None = None,
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
                    data = patch_document_xml(data, cover=cover)
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
