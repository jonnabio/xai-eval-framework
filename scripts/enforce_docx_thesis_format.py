#!/usr/bin/env python3
"""Enforce thesis DOCX paragraph formatting.

The thesis render depends on a Word reference document, but Pandoc/Quarto can
still emit body paragraphs without explicit alignment or line-spacing. This
script patches the reference DOCX and the rendered DOCX so body text is always
justified and double-spaced.
"""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}
W = f"{{{W_NS}}}"
DOCX_NAMESPACES = {
    "w": W_NS,
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "o": "urn:schemas-microsoft-com:office:office",
    "v": "urn:schemas-microsoft-com:vml",
    "w10": "urn:schemas-microsoft-com:office:word",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16cid": "http://schemas.microsoft.com/office/word/2016/wordml/cid",
    "w16se": "http://schemas.microsoft.com/office/word/2015/wordml/symex",
}
for prefix, uri in DOCX_NAMESPACES.items():
    ET.register_namespace(prefix, uri)

BODY_STYLE_IDS = {
    "Normal",
    "Default",
    "Textoindependiente",  # Body Text in the Spanish Word template.
    "BodyText",
    "Prrafodelista",  # List Paragraph in the Spanish Word template.
    "ListParagraph",
    "Bibliography",
    "FirstParagraph",
    "Compact",
    "BlockText",
}

EXCLUDED_STYLE_PREFIXES = (
    "Ttulo",  # heading styles in the Spanish Word template.
    "Heading",
    "TDC",  # table of contents styles.
    "TOC",
)

EXCLUDED_STYLE_IDS = {
    "Epgrafe",
    "Caption",
    "SourceCode",
    "Piedepagina",
    "Piedepgina",
    "Encabezado",
    "Textodeglobo",
    "Textocomentario",
    "Asuntodelcomentario",
    "Tabladeilustraciones",
    "TtulodeTDC",
}


def w_attr(name: str) -> str:
    return f"{W}{name}"


def ensure_child(parent: ET.Element, tag: str) -> ET.Element:
    child = parent.find(f"w:{tag.removeprefix(W)}", NS)
    if child is None:
        child = ET.SubElement(parent, tag)
    return child


def style_id(paragraph: ET.Element) -> str | None:
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        return None
    pstyle = ppr.find("w:pStyle", NS)
    if pstyle is None:
        return None
    return pstyle.get(w_attr("val"))


def is_excluded_style(style: str | None) -> bool:
    if not style:
        return False
    return style in EXCLUDED_STYLE_IDS or style.startswith(EXCLUDED_STYLE_PREFIXES)


def is_body_style(style: str | None) -> bool:
    return style is None or style in BODY_STYLE_IDS


def set_double_justified(ppr: ET.Element) -> bool:
    changed = False

    jc = ppr.find("w:jc", NS)
    if jc is None:
        jc = ET.SubElement(ppr, f"{W}jc")
        changed = True
    if jc.get(w_attr("val")) != "both":
        jc.set(w_attr("val"), "both")
        changed = True

    spacing = ppr.find("w:spacing", NS)
    if spacing is None:
        spacing = ET.SubElement(ppr, f"{W}spacing")
        changed = True
    desired = {
        "line": "480",
        "lineRule": "auto",
    }
    for key, value in desired.items():
        if spacing.get(w_attr(key)) != value:
            spacing.set(w_attr(key), value)
            changed = True

    return changed


def update_styles_xml(xml: bytes) -> tuple[bytes, int]:
    root = ET.fromstring(xml)
    changed = 0

    for style in root.findall("w:style[@w:type='paragraph']", NS):
        sid = style.get(w_attr("styleId"))
        if is_body_style(sid) and not is_excluded_style(sid):
            ppr = style.find("w:pPr", NS)
            if ppr is None:
                ppr = ET.SubElement(style, f"{W}pPr")
            if set_double_justified(ppr):
                changed += 1

    return ET.tostring(root, encoding="utf-8", xml_declaration=True), changed


def update_document_xml(xml: bytes) -> tuple[bytes, int]:
    root = ET.fromstring(xml)
    parent_map = {child: parent for parent in root.iter() for child in parent}
    changed = 0

    for paragraph in root.findall(".//w:p", NS):
        style = style_id(paragraph)
        if is_excluded_style(style) or not is_body_style(style):
            continue

        in_table = False
        parent = parent_map.get(paragraph)
        while parent is not None:
            if parent.tag == f"{W}tbl":
                in_table = True
                break
            parent = parent_map.get(parent)
        if in_table:
            continue

        ppr = paragraph.find("w:pPr", NS)
        if ppr is None:
            ppr = ET.Element(f"{W}pPr")
            paragraph.insert(0, ppr)
        if set_double_justified(ppr):
            changed += 1

    return ET.tostring(root, encoding="utf-8", xml_declaration=True), changed


def patch_docx(path: Path) -> tuple[int, int]:
    if not path.exists():
        raise FileNotFoundError(path)

    style_changes = 0
    paragraph_changes = 0
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
        tmp_path = Path(tmp_file.name)

    try:
        with ZipFile(path, "r") as src, ZipFile(tmp_path, "w", ZIP_DEFLATED) as dst:
            for item in src.infolist():
                data = src.read(item.filename)
                if item.filename == "word/styles.xml":
                    data, style_changes = update_styles_xml(data)
                elif item.filename == "word/document.xml":
                    data, paragraph_changes = update_document_xml(data)
                dst.writestr(item, data)
        shutil.move(str(tmp_path), path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()

    return style_changes, paragraph_changes


def verify_docx(path: Path) -> list[str]:
    failures: list[str] = []
    with ZipFile(path, "r") as docx:
        styles = ET.fromstring(docx.read("word/styles.xml"))
        for style in styles.findall("w:style[@w:type='paragraph']", NS):
            sid = style.get(w_attr("styleId"))
            if not is_body_style(sid) or is_excluded_style(sid):
                continue
            ppr = style.find("w:pPr", NS)
            jc = ppr.find("w:jc", NS) if ppr is not None else None
            spacing = ppr.find("w:spacing", NS) if ppr is not None else None
            if jc is None or jc.get(w_attr("val")) != "both":
                failures.append(f"{path}: style {sid or '(default)'} is not justified")
            if (
                spacing is None
                or spacing.get(w_attr("line")) != "480"
                or spacing.get(w_attr("lineRule")) != "auto"
            ):
                failures.append(f"{path}: style {sid or '(default)'} is not double-spaced")

        document = ET.fromstring(docx.read("word/document.xml"))
        parent_map = {child: parent for parent in document.iter() for child in parent}
        for index, paragraph in enumerate(document.findall(".//w:p", NS), start=1):
            style = style_id(paragraph)
            if is_excluded_style(style) or not is_body_style(style):
                continue
            parent = parent_map.get(paragraph)
            while parent is not None and parent.tag != f"{W}tbl":
                parent = parent_map.get(parent)
            if parent is not None:
                continue

            ppr = paragraph.find("w:pPr", NS)
            jc = ppr.find("w:jc", NS) if ppr is not None else None
            spacing = ppr.find("w:spacing", NS) if ppr is not None else None
            if jc is None or jc.get(w_attr("val")) != "both":
                failures.append(f"{path}: body paragraph {index} is not justified")
            if (
                spacing is None
                or spacing.get(w_attr("line")) != "480"
                or spacing.get(w_attr("lineRule")) != "auto"
            ):
                failures.append(f"{path}: body paragraph {index} is not double-spaced")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", nargs="+", type=Path)
    parser.add_argument("--check", action="store_true", help="verify after patching")
    args = parser.parse_args()

    failures: list[str] = []
    for path in args.docx:
        style_changes, paragraph_changes = patch_docx(path)
        print(
            f"Formatted {path}: {style_changes} style updates, "
            f"{paragraph_changes} paragraph updates"
        )
        if args.check:
            failures.extend(verify_docx(path))

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
