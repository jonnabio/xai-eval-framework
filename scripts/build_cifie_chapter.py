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

Usage: python scripts/build_cifie_chapter.py [--out PATH]
"""
from __future__ import annotations

import argparse
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
    source = header + body + "\n\n" + references()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        md = Path(tmp) / "chapter.md"
        md.write_text(source, encoding="utf-8")
        subprocess.run(
            [find_pandoc(), str(md), "-f", "markdown", "-t", "docx",
             "--resource-path", str(MANUSCRIPT), "-o", str(args.out)],
            check=True,
        )
    hanging_indent(args.out)

    words = len(re.findall(r"\w+", body))
    print(f"OK: {len(sections)} sections, {n_tables} tables, ~{words} words -> {args.out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
