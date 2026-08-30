#!/usr/bin/env python3
"""Cross-check a coded review corpus CSV against the distribution a paper claims.

Paper B+C states its corpus size, cluster distribution, evidence-source coverage
and confidence mix in prose and in tab:corpus_profile. This script recomputes all
four from the CSV and reports every disagreement, so the corpus and the
manuscript cannot drift apart the way they did in finding A14.

Usage:
    python scripts/pubs/check_review_corpus.py --corpus <csv> --expect <toml-section>

With no --expect, it just prints the observed distribution -- useful while
entering rows, to see how far the coding has got.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
import sys

try:
    import tomllib  # py3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "pub" / "claim_registry.toml"

REQUIRED_COLUMNS = [
    "study_id",
    "record_slug",
    "title_short",
    "primary_cluster",
    "paper_role",
    "modality_context",
    "evaluation_targets",
    "evidence_sources",
    "quality_properties",
    "llm_validation_relevant",
    "source_confidence",
    "notes",
]

# Controlled vocabularies. Extend deliberately: a cluster the manuscript names
# but this list omits is a coding-scheme change that the paper must describe.
CLUSTERS = {
    "faithfulness_robustness",
    "human_grounded",
    "taxonomy_survey",
    "benchmark_toolkit",
    "llm_judge",
    "counterfactual_recourse",
    "modality_domain",
}
EVIDENCE_SOURCES = {"proxy", "benchmark", "human_expert", "end_user", "llm_judge"}
CONFIDENCE = {"high", "medium", "title_level"}


def _load(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Corpus not found: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _structural_problems(rows: list[dict]) -> list[str]:
    problems: list[str] = []
    if not rows:
        return ["corpus is empty"]

    missing = [c for c in REQUIRED_COLUMNS if c not in rows[0]]
    if missing:
        problems.append(f"missing columns: {', '.join(missing)}")
        return problems

    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()
    for i, row in enumerate(rows, start=2):  # header is line 1
        where = f"line {i} ({row.get('record_slug') or 'no slug'})"
        if not row["record_slug"].strip():
            problems.append(f"{where}: empty record_slug")
        elif row["record_slug"] in seen_slugs:
            problems.append(f"{where}: duplicate record_slug")
        seen_slugs.add(row["record_slug"])

        if row["study_id"] in seen_ids:
            problems.append(f"{where}: duplicate study_id {row['study_id']}")
        seen_ids.add(row["study_id"])

        if row["primary_cluster"] not in CLUSTERS:
            problems.append(f"{where}: unknown primary_cluster '{row['primary_cluster']}'")
        if row["source_confidence"] not in CONFIDENCE:
            problems.append(f"{where}: unknown source_confidence '{row['source_confidence']}'")
        for src in filter(None, (s.strip() for s in row["evidence_sources"].split(";"))):
            if src not in EVIDENCE_SOURCES:
                problems.append(f"{where}: unknown evidence_source '{src}'")
    return problems


def _observed(rows: list[dict]) -> dict:
    sources: Counter = Counter()
    for row in rows:
        for src in filter(None, (s.strip() for s in row["evidence_sources"].split(";"))):
            sources[src] += 1
    return {
        "size": len(rows),
        "clusters": Counter(r["primary_cluster"] for r in rows),
        "evidence_sources": sources,
        "confidence": Counter(r["source_confidence"] for r in rows),
    }


def _report(observed: dict) -> None:
    print(f"corpus size: {observed['size']}")
    for label in ("clusters", "evidence_sources", "confidence"):
        print(f"\n{label}:")
        for key, count in observed[label].most_common():
            print(f"  {count:3}  {key}")


def _compare(observed: dict, expected: dict) -> list[str]:
    problems: list[str] = []
    if expected.get("size") and observed["size"] != expected["size"]:
        problems.append(
            f"corpus has {observed['size']} rows but the manuscript claims {expected['size']}"
        )
    for label in ("clusters", "evidence_sources", "confidence"):
        claimed = expected.get(label)
        if not claimed:
            # A manuscript that only states its corpus size is checked on size
            # alone; absence of a breakdown is not a mismatch.
            continue
        for key, want in claimed.items():
            got = observed[label].get(key, 0)
            if got != want:
                problems.append(f"{label}.{key}: corpus has {got}, manuscript claims {want}")
        for key in observed[label]:
            if key not in claimed:
                problems.append(f"{label}.{key}: present in corpus but not claimed by the manuscript")
    return problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check a review corpus against a paper's claims.")
    parser.add_argument("--corpus", required=True, help="Path to the coded corpus CSV")
    parser.add_argument("--expect", help="Key under [review_corpus] in pub/claim_registry.toml")
    args = parser.parse_args(argv)

    rows = _load(Path(args.corpus))
    problems = _structural_problems(rows)
    observed = _observed(rows) if not problems else None

    if observed:
        _report(observed)

    if args.expect and observed:
        registry = tomllib.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        expected = registry.get("review_corpus", {}).get(args.expect)
        if expected is None:
            raise SystemExit(f"No [review_corpus.{args.expect}] section in {REGISTRY_PATH}")
        problems += _compare(observed, expected)

    if problems:
        joined = "\n".join(f"- {p}" for p in problems)
        raise SystemExit(f"\nReview corpus check failed:\n{joined}\n")

    print("\nOK: corpus is structurally valid" + (" and matches the manuscript" if args.expect else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
