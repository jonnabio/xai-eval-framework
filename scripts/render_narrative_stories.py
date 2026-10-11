#!/usr/bin/env python3
"""Render the 3 PhD narrative stories (Beginner, Intermediate, PhD) into LaTeX (.tex) and PDF (.pdf)."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "publications" / "book_chapters" / "2026_cifie_xai_fom7"
PANDOC = Path(r"C:\Program Files\Quarto\bin\tools\pandoc.exe")

FILES = [
    "STORY_PhD_NARRATIVE_BEGINNER",
    "STORY_PhD_NARRATIVE_INTERMIDIATE",
    "STORY_PhD_NARRATIVE_PhD",
]


def find_pandoc() -> str:
    if PANDOC.exists():
        return str(PANDOC)
    found = shutil.which("pandoc")
    if found:
        return found
    raise SystemExit("pandoc not found")


def render_file(stem: str) -> None:
    md_file = CHAPTER / f"{stem}.md"
    tex_file = CHAPTER / f"{stem}.tex"
    pdf_file = CHAPTER / f"{stem}.pdf"
    
    pandoc_bin = find_pandoc()
    
    # 1. Render to LaTeX (.tex)
    subprocess.run(
        [
            pandoc_bin,
            str(md_file),
            "-f", "markdown",
            "-t", "latex",
            "-s",
            "-o", str(tex_file),
            "--variable", "geometry:margin=1in",
            "--variable", "documentclass=article",
        ],
        check=True,
    )
    print(f"OK (LaTeX): {tex_file.relative_to(ROOT).as_posix()}")

    # 2. Render to PDF (.pdf) via Word COM for exact formatting & math rendering
    with tempfile.TemporaryDirectory() as tmp_dir:
        docx_tmp = Path(tmp_dir) / f"{stem}.docx"
        subprocess.run(
            [
                pandoc_bin,
                str(md_file),
                "-f", "markdown",
                "-t", "docx",
                "-o", str(docx_tmp),
            ],
            check=True,
        )
        
        cmd = (
            f"$word = New-Object -ComObject Word.Application; "
            f"$word.Visible = $false; "
            f"$doc = $word.Documents.Open('{docx_tmp.resolve()}'); "
            f"$doc.SaveAs([ref]'{pdf_file.resolve()}', [ref]17); "
            f"$doc.Close(); "
            f"$word.Quit();"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", cmd], check=True)
    print(f"OK (PDF): {pdf_file.relative_to(ROOT).as_posix()}")


def main() -> None:
    for stem in FILES:
        render_file(stem)


if __name__ == "__main__":
    main()
