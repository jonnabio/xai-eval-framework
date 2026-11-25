#!/usr/bin/env python3
"""RCA-007 guard: every table row and sign of the built revision manuscript is plain text.

    .venv/Scripts/python.exe docs/reports/paper_e/aair_journal/revision_1/scripts/check_signs.py
"""
import importlib.util
import sys
from pathlib import Path

AAIR = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("build", AAIR / "scripts" / "build_paper_e_aair_docx.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
build.use_revision_1()
docx = build.OUT / f"{build.NAME}_manuscript.docx"
if not docx.exists():
    sys.exit(f"{docx} not built")
b = build.cys_build()
rows = build.verify_numbers(docx, build.RENDERED.read_text(encoding="utf-8"), (b, b.Numbers()))
print(f"OK: {rows} table rows and every sign of {docx.name} are plain text and match the source")
