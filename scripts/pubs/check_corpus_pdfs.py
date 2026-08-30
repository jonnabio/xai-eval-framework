#!/usr/bin/env python3
"""Report which Paper B+C corpus PDFs are still missing.

Reads docs/reports/paper_bc/corpus_pdf_manifest.csv and checks
docs/reports/paper_bc/corpus_pdfs/<citation_key>.pdf for each tracked paper.
Run it after each retrieval batch to see what is left.

Exits non-zero only with --strict, so it is safe to run while the collection is
still being assembled.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs" / "reports" / "paper_bc" / "corpus_pdf_manifest.csv"
PDF_DIR = ROOT / "docs" / "reports" / "paper_bc" / "corpus_pdfs"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check corpus PDF collection progress.")
    parser.add_argument("--strict", action="store_true", help="exit non-zero if any PDF is missing")
    args = parser.parse_args(argv)

    if not MANIFEST.exists():
        raise SystemExit(f"Manifest not found: {MANIFEST}")

    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    have, need = [], []
    for row in rows:
        target = PDF_DIR / f"{row['citation_key']}.pdf"
        (have if target.exists() else need).append(row)

    print(f"corpus PDFs: {len(have)}/{len(rows)} collected in {PDF_DIR.relative_to(ROOT).as_posix()}/")

    if need:
        print(f"\nstill needed ({len(need)}):")
        for row in sorted(need, key=lambda r: (r["group"] != "confirmed", r["citation_key"])):
            hint = row["link"] or "search by title"
            note = ""
            if row["status"] == "present" and row["matched_file"]:
                note = f"  [already in thesis/papers/ as: {row['matched_file']}]"
            print(f"  {row['citation_key']:<28} {hint}{note}")

    stragglers = [p.stem for p in PDF_DIR.glob("*.pdf")] if PDF_DIR.exists() else []
    tracked = {r["citation_key"] for r in rows}
    unknown = sorted(set(stragglers) - tracked)
    if unknown:
        print(f"\nPDFs present but not in the manifest ({len(unknown)}):")
        for key in unknown:
            print(f"  {key}.pdf")
        print("  -- either add them to the manifest or rename to a tracked citation key")

    if args.strict and (need or unknown):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
