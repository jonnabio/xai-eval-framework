#!/usr/bin/env python3
"""Enforce thesis DOCX paragraph formatting.

The script patches WordprocessingML inside a .docx file so Quarto renders keep
paragraph text justified and line spacing at 1.5. It is intentionally stdlib-only
so it works even when python-docx is unavailable.
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


def patch_document_xml(xml_bytes: bytes) -> bytes:
    root = ET.fromstring(xml_bytes)
    for p in root.findall(".//w:p", NS):
        ppr = p.find("w:pPr", NS)
        if ppr is None:
            ppr = ET.Element(qn("pPr"))
            p.insert(0, ppr)
        set_paragraph_format(ppr)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_docx(path: Path, patch_document: bool = False, backup: bool = True) -> None:
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
                    data = patch_document_xml(data)
                zout.writestr(item, data)
        shutil.move(str(tmp_path), path)


def inspect_docx(path: Path) -> None:
    with zipfile.ZipFile(path, "r") as zf:
        styles = ET.fromstring(zf.read("word/styles.xml"))
        ppr = styles.find("w:docDefaults/w:pPrDefault/w:pPr", NS)
        spacing = ppr.find("w:spacing", NS) if ppr is not None else None
        jc = ppr.find("w:jc", NS) if ppr is not None else None
        print(
            {
                "path": str(path),
                "default_line": spacing.get(qn("line")) if spacing is not None else None,
                "default_line_rule": spacing.get(qn("lineRule")) if spacing is not None else None,
                "default_justification": jc.get(qn("val")) if jc is not None else None,
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
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()

    for raw in args.docx:
        path = Path(raw)
        if args.inspect:
            inspect_docx(path)
        else:
            patch_docx(path, patch_document=args.document, backup=not args.no_backup)
            inspect_docx(path)


if __name__ == "__main__":
    main()
