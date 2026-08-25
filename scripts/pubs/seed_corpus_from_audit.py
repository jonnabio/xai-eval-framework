#!/usr/bin/env python3
"""Seed the Paper B+C corpus CSV from data that already exists.

Two sources, neither invented:

- `second_reviewer_audit_results.csv` supplies 16 rows complete with the
  original first-reviewer coding on all four taxonomy axes.
- `corpus_pdf_manifest.csv` supplies the remaining tracked citation keys, whose
  identity is known but whose coding is not. Those rows are written with the
  coding columns EMPTY, marked `TODO` in notes.

Nothing is guessed: an empty cell means the coding was not recovered and still
needs a human decision. Refuses to overwrite an existing corpus file.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
BC = ROOT / "docs" / "reports" / "paper_bc"
AUDIT = BC / "second_reviewer_audit_results.csv"
MANIFEST = BC / "corpus_pdf_manifest.csv"
OUT = BC / "paper_bc_review_corpus.csv"

COLUMNS = [
    "study_id", "record_slug", "title_short", "primary_cluster", "paper_role",
    "modality_context", "evaluation_targets", "evidence_sources",
    "quality_properties", "llm_validation_relevant", "source_confidence", "notes",
]

# The audit CSV names taxonomy values in the paper's vocabulary; the corpus CSV
# uses the shorter slugs established by the Paper C corpus.
TARGET_MAP = {
    "explanation_artifact": "artifact",
    "explainer_method": "explainer",
    "model_behavior": "model_behavior",
    "user_task_outcome": "user_task",
}


def _read(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Required input not found: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _map_targets(raw: str) -> str:
    out = []
    for item in filter(None, (s.strip() for s in raw.split(";"))):
        out.append(TARGET_MAP.get(item, item))
    return ";".join(out)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Seed the Paper B+C corpus CSV.")
    parser.add_argument("--force", action="store_true", help="overwrite an existing corpus file")
    args = parser.parse_args(argv)

    if OUT.exists() and not args.force:
        raise SystemExit(
            f"{OUT.relative_to(ROOT).as_posix()} already exists. "
            "Refusing to overwrite coding work -- pass --force if you mean it."
        )

    audit = _read(AUDIT)
    manifest = _read(MANIFEST)

    rows: list[dict] = []
    coded_keys = set()

    for entry in audit:
        key = entry["citation_key"]
        coded_keys.add(key)
        rows.append({
            "study_id": len(rows) + 1,
            "record_slug": key,
            "title_short": entry["title"],
            "primary_cluster": entry["primary_cluster"],
            "paper_role": "",
            "modality_context": entry.get("r1_task_context", ""),
            "evaluation_targets": _map_targets(entry.get("r1_evaluation_target", "")),
            "evidence_sources": entry.get("r1_evidence_source", ""),
            "quality_properties": entry.get("r1_quality_property", ""),
            "llm_validation_relevant": "",
            "source_confidence": "",
            "notes": "Coding recovered from second_reviewer_audit_results.csv (reviewer 1).",
        })

    for entry in manifest:
        key = entry["citation_key"]
        if key in coded_keys:
            continue
        rows.append({
            "study_id": len(rows) + 1,
            "record_slug": key,
            "title_short": entry["title"],
            "primary_cluster": "",
            "paper_role": "",
            "modality_context": "",
            "evaluation_targets": "",
            "evidence_sources": "",
            "quality_properties": "",
            "llm_validation_relevant": "",
            "source_confidence": "",
            "notes": "TODO: coding not recovered; decide include/exclude and code four axes.",
        })

    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    todo = sum(1 for r in rows if r["notes"].startswith("TODO"))
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}: {len(rows)} rows")
    print(f"  {len(rows) - todo} pre-coded from the audit record")
    print(f"  {todo} need coding (marked TODO)")
    print("\nNext: python scripts/pubs/check_review_corpus.py --corpus "
          f"{OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
