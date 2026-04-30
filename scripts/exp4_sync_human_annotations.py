"""
exp4_sync_human_annotations.py
--------------------------------
Incrementally fetches human validation annotations from the live Render API
and merges them into a local CSV, deduplicating by annotation_id.

Usage:
    python scripts/exp4_sync_human_annotations.py            # sync and report
    python scripts/exp4_sync_human_annotations.py --dry-run  # fetch only, no write

Output:
    experiments/exp4_llm_evaluation/human_validation_responses.csv
"""

import argparse
import csv
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────
API_URL = "https://xai-benchmark.onrender.com/api/human-eval/export?format=json"
OUT_CSV = Path("experiments/exp4_llm_evaluation/human_validation_responses.csv")

CSV_FIELDS = [
    "annotation_id",
    "case_id",
    "annotator_id",
    "clarity",
    "completeness",
    "concision",
    "plausibility",
    "audit_usefulness",
    "comments",
    "time_spent_seconds",
    "submitted_at",
    "dataset",
    "explainer",
    "quadrant",
    "synced_at",
]


def fetch_remote() -> list[dict]:
    """Fetch all annotations from the live API."""
    print(f"[fetch] GET {API_URL}")
    req = urllib.request.Request(API_URL, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode())
    annotations = payload.get("annotations", [])
    print(f"[fetch] {len(annotations)} annotation(s) returned by API")
    return annotations


def flatten(raw: dict, synced_at: str) -> dict:
    """Flatten nested ratings dict into a single-level row."""
    r = raw.get("ratings", {})
    return {
        "annotation_id": raw.get("annotation_id", ""),
        "case_id": raw.get("case_id", ""),
        "annotator_id": raw.get("annotator_id", ""),
        "clarity": r.get("clarity", ""),
        "completeness": r.get("completeness", ""),
        "concision": r.get("concision", ""),
        "plausibility": r.get("plausibility", ""),
        "audit_usefulness": r.get("audit_usefulness", ""),
        "comments": raw.get("comments", ""),
        "time_spent_seconds": raw.get("time_spent_seconds", ""),
        "submitted_at": raw.get("submitted_at", ""),
        "dataset": raw.get("dataset", ""),
        "explainer": raw.get("explainer", ""),
        "quadrant": raw.get("quadrant", ""),
        "synced_at": synced_at,
    }


def load_existing(path: Path) -> dict[str, dict]:
    """Load existing CSV rows keyed by annotation_id."""
    if not path.exists():
        return {}
    existing: dict[str, dict] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            existing[row["annotation_id"]] = row
    print(f"[local]  {len(existing)} existing row(s) in {path}")
    return existing


def save(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync EXP4 human annotations from Render API")
    parser.add_argument("--dry-run", action="store_true", help="Fetch only, do not write CSV")
    parser.add_argument("--out", default=str(OUT_CSV), help="Output CSV path")
    args = parser.parse_args()

    out_path = Path(args.out)
    synced_at = datetime.now(timezone.utc).isoformat()

    # 1. Fetch remote
    try:
        remote = fetch_remote()
    except Exception as exc:
        print(f"[ERROR] Failed to fetch from API: {exc}", file=sys.stderr)
        sys.exit(1)

    # 2. Load existing local rows
    existing = load_existing(out_path)

    # 3. Merge: remote is authoritative; new rows are added, existing rows updated
    merged = dict(existing)  # start with local copy
    new_count = 0
    updated_count = 0
    for raw in remote:
        row = flatten(raw, synced_at)
        aid = row["annotation_id"]
        if aid not in merged:
            new_count += 1
        elif merged[aid].get("submitted_at") != row["submitted_at"]:
            updated_count += 1
        merged[aid] = row

    all_rows = sorted(merged.values(), key=lambda r: r["submitted_at"])

    # 4. Report
    print(f"[merge]  {new_count} new, {updated_count} updated, {len(all_rows)} total")

    if args.dry_run:
        print("[dry-run] No file written.")
        for row in all_rows:
            print(f"  {row['annotation_id']}  {row['annotator_id']}  submitted={row['submitted_at']}")
        return

    # 5. Write
    save(out_path, all_rows)
    print(f"[saved]  {out_path} ({len(all_rows)} rows)")

    # 6. Quick summary by annotator
    by_annotator: dict[str, int] = {}
    for row in all_rows:
        by_annotator[row["annotator_id"]] = by_annotator.get(row["annotator_id"], 0) + 1
    print("\n[summary] Annotations per annotator:")
    for ann, cnt in sorted(by_annotator.items()):
        print(f"  {ann:20s}  {cnt:3d}")


if __name__ == "__main__":
    main()
