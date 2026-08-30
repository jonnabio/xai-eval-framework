#!/usr/bin/env python3
"""Post-render DOCX formatting hook for Quarto.

Quarto reads paragraph styles from the reference document, but direct paragraph
properties can still appear in generated DOCX files. This hook formats rendered
outputs after every project render so body paragraphs remain justified with 1.5
line spacing, and replaces Quarto's automatic title block with the cover page
declared in `cover.txt`.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from enforce_docx_thesis_format import load_cover, patch_docx  # noqa: E402


def main() -> None:
    thesis_dir = Path(__file__).resolve().parent
    cover_file = thesis_dir / "cover.txt"
    cover = load_cover(cover_file) if cover_file.exists() else None
    if cover is None:
        print(f"AVISO: no se encontro {cover_file}; se omite la portada.")
    docx_files = sorted(thesis_dir.glob("_output*/JHerrera_XAI_Tesis_Doctorado.docx"))
    for docx in docx_files:
        patch_docx(docx, patch_document=True, backup=False, cover=cover)
        print(f"Formato DOCX aplicado: {docx}")


if __name__ == "__main__":
    main()
