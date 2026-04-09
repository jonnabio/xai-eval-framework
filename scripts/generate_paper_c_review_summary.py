#!/usr/bin/env python3
"""Generate descriptive summary artifacts for the Paper C coded review corpus."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = PROJECT_ROOT / "docs" / "reports" / "paper_c" / "paper_c_review_corpus.csv"
OUTPUT_MD = PROJECT_ROOT / "outputs" / "analysis" / "paper_c_review_summary.md"
OUTPUT_MD_TRACKED = (
    PROJECT_ROOT / "docs" / "reports" / "paper_c" / "paper_c_review_summary.md"
)
OUTPUT_JSON = PROJECT_ROOT / "outputs" / "analysis" / "paper_c_review_summary.json"

UPSTREAM_MATRIX_ENTRIES = 25
DUPLICATE_REMOVED = 1
CORPUS_FREEZE_DATE = "2026-04-05"


def split_labels(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def markdown_counter(title: str, counts: Counter[str]) -> list[str]:
    lines = [f"## {title}", ""]
    for key, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{key}`: {count}")
    lines.append("")
    return lines


def main() -> None:
    with CORPUS_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    unique_papers = len(rows)
    cluster_counts = Counter(row["primary_cluster"] for row in rows)
    role_counts = Counter(row["paper_role"] for row in rows)
    modality_counts = Counter(row["modality_context"] for row in rows)
    evidence_counts = Counter()
    target_counts = Counter()
    property_counts = Counter()
    confidence_counts = Counter(row["source_confidence"] for row in rows)

    for row in rows:
        evidence_counts.update(split_labels(row["evidence_sources"]))
        target_counts.update(split_labels(row["evaluation_targets"]))
        property_counts.update(split_labels(row["quality_properties"]))

    llm_validation_relevant = sum(1 for row in rows if row["llm_validation_relevant"] == "yes")
    direct_human_expert = evidence_counts["human_expert"]
    direct_end_user = evidence_counts["end_user"]
    direct_llm_judge = evidence_counts["llm_judge"]
    direct_proxy = evidence_counts["proxy"]
    direct_benchmark = evidence_counts["benchmark"]

    takeaways = [
        (
            "Proxy-heavy evidence base",
            f"`proxy` evidence appears in {direct_proxy} coded studies, compared with "
            f"{direct_human_expert} using `human_expert` evidence and {direct_end_user} using "
            f"`end_user` evidence."
        ),
        (
            "Validation remains sparse",
            f"{llm_validation_relevant} studies are marked as LLM-validation-relevant, but only "
            f"{direct_end_user} directly include end-user evidence and {direct_human_expert} "
            "directly include expert-human evidence."
        ),
        (
            "Benchmark realism is present but concentrated",
            f"`benchmark` evidence appears in {direct_benchmark} studies and is concentrated in "
            "toolkit and modality-specific benchmark papers rather than across the whole corpus."
        ),
    ]

    summary = {
        "corpus_freeze_date": CORPUS_FREEZE_DATE,
        "upstream_matrix_entries": UPSTREAM_MATRIX_ENTRIES,
        "duplicate_removed": DUPLICATE_REMOVED,
        "unique_coded_papers": unique_papers,
        "cluster_counts": dict(cluster_counts),
        "role_counts": dict(role_counts),
        "modality_counts": dict(modality_counts),
        "evaluation_target_counts": dict(target_counts),
        "evidence_source_counts": dict(evidence_counts),
        "quality_property_counts": dict(property_counts),
        "confidence_counts": dict(confidence_counts),
        "llm_validation_relevant_count": llm_validation_relevant,
        "takeaways": [
            {"label": label, "detail": detail}
            for label, detail in takeaways
        ],
    }

    lines: list[str] = [
        "# Paper C Review Summary",
        "",
        f"- Corpus freeze date: `{CORPUS_FREEZE_DATE}`",
        f"- Upstream matrix entries reviewed: `{UPSTREAM_MATRIX_ENTRIES}`",
        f"- Duplicate rows removed during Paper C coding: `{DUPLICATE_REMOVED}`",
        f"- Unique coded papers in `docs/reports/paper_c/paper_c_review_corpus.csv`: `{unique_papers}`",
        "",
    ]
    lines.extend(markdown_counter("Primary Cluster Counts", cluster_counts))
    lines.extend(markdown_counter("Paper Role Counts", role_counts))
    lines.extend(markdown_counter("Modality Counts", modality_counts))
    lines.extend(markdown_counter("Evaluation Target Coverage", target_counts))
    lines.extend(markdown_counter("Evidence Source Coverage", evidence_counts))
    lines.extend(markdown_counter("Quality Property Coverage", property_counts))
    lines.extend(markdown_counter("Source Confidence Counts", confidence_counts))

    lines.append("## High-Level Takeaways")
    lines.append("")
    for label, detail in takeaways:
        lines.append(f"- **{label}:** {detail}")
    lines.append("")

    markdown = "\n".join(lines)
    OUTPUT_MD.write_text(markdown, encoding="utf-8")
    OUTPUT_MD_TRACKED.write_text(markdown, encoding="utf-8")
    OUTPUT_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    main()
