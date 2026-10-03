#!/usr/bin/env python3
"""Measure the claim registry for Paper D (the registry case study).

Paper D reports how the claim registry (pub/claim_registry.toml, checked by
scripts/pubs/verify_claims.py) grew and what it covers. Every number it prints
must re-derive like any other result (RCA-001), so this script reads the
registry from git at pinned commits instead of from the working tree: the
registry keeps changing, the published numbers must not.

    python scripts/pubs/paper_d_metrics.py

Writes to outputs/analysis/paper_d/:
    registry_snapshot.csv   metric,value at SNAPSHOT_COMMIT
    registry_growth.csv     one row per commit that changed the registry
"""
from __future__ import annotations

import csv
import subprocess
import tomllib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "analysis" / "paper_d"
REGISTRY = "pub/claim_registry.toml"

# The registry as it stood when Paper D's case study was frozen
# (main after the Inteligencia Artificial refactor of Paper B+C, 2026-10-02).
SNAPSHOT_COMMIT = "124a7db4c"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout


def _registry_at(commit: str) -> dict:
    return tomllib.loads(_git("show", f"{commit}:{REGISTRY}"))


def _document(path: str) -> str:
    """Group a manuscript file into the document it belongs to."""
    if path.startswith("thesis/"):
        return "thesis"
    if "/paper_a/" in path:
        return "paper_a"
    if "/paper_bc/" in path or path.startswith("pub/fragments/paper_bc"):
        return "paper_bc"
    if "book_chapters" in path:
        return "book_chapter"
    if path.startswith("pub/fragments/thesis"):
        return "thesis"
    return "other"


def summarise(reg: dict) -> dict[str, float]:
    claims = reg.get("claim", [])
    sites = [s for c in claims for s in c.get("appears_in", [])]
    docs_per_claim = [len({_document(s["file"]) for s in c.get("appears_in", [])}) for c in claims]
    resolvers = {c["source"].split(":")[0] for c in claims}
    by_doc = Counter(_document(s["file"]) for s in sites)
    coverage = reg.get("coverage", {})
    out = {
        "claims": len(claims),
        "sites": len(sites),
        "claims_multi_document": sum(1 for n in docs_per_claim if n > 1),
        "retired": len(reg.get("retired", [])),
        "unbacked": len(reg.get("unbacked", [])),
        "structural_literals": len(coverage.get("structural", []) or []),
        "coverage_files": len(coverage.get("files", []) or []),
        "exclusivity_files": len(reg.get("exclusivity", {}).get("files", []) or []),
        "resolver_kinds": len(resolvers),
        "documents": len({d for d in by_doc if d != "other"}),
    }
    for doc in ("thesis", "paper_a", "paper_bc", "book_chapter"):
        out[f"sites_{doc}"] = by_doc.get(doc, 0)
    return out


# Implementation size at the pinned commit: the verifier, the resolvers and the
# registry itself (non-blank lines).
SIZE_FILES = {
    "loc_verifier": "scripts/pubs/verify_claims.py",
    "loc_resolvers": "scripts/pubs/claim_sources.py",
    "lines_registry": REGISTRY,
}


def sizes(commit: str) -> dict[str, int]:
    return {k: sum(1 for l in _git("show", f"{commit}:{p}").splitlines() if l.strip())
            for k, p in SIZE_FILES.items()}


def catalogue_summary() -> dict[str, int]:
    """Counts over incident_catalogue.csv (hand-coded; see the paper's Methods).

    Excluded: rows carried forward from an earlier review (dup_of set), and rows
    that are not defects in a document (not_a_defect, process_gap).
    """
    rows = list(csv.DictReader((OUT / "incident_catalogue.csv").open(encoding="utf-8")))
    raw = len(rows)
    rows = [r for r in rows if not r["dup_of"] and r["defect_class"] not in ("not_a_defect", "process_gap")]
    num = [r for r in rows if r["numeric"] == "yes"]
    non = [r for r in rows if r["numeric"] == "no"]
    out = {
        "rows_raw": raw,
        "defects": len(rows),
        "numeric": len(num),
        "non_numeric": len(non),
        "major": sum(r["severity"] == "major" for r in rows),
        "caught_yes": sum(r["caught_now"] == "yes" for r in rows),
        "caught_partial": sum(r["caught_now"] == "partial" for r in rows),
        "caught_no": sum(r["caught_now"] == "no" for r in rows),
        "numeric_caught_yes": sum(r["caught_now"] == "yes" for r in num),
        "numeric_caught_partial": sum(r["caught_now"] == "partial" for r in num),
        "numeric_caught_no": sum(r["caught_now"] == "no" for r in num),
        "non_numeric_caught_yes": sum(r["caught_now"] == "yes" for r in non),
        "found_by_tooling": sum(r["detected_by"] in ("registry_construction", "coverage_sweep",
                                                      "clean_worktree_verify") for r in rows),
        "found_by_manual": sum(r["detected_by"] in ("manual_audit", "manual_review") for r in rows),
        "found_by_rendering": sum(r["detected_by"] in ("rebuild", "manual_pdf_check") for r in rows),
    }
    for cls, n in sorted(Counter(r["defect_class"] for r in rows).items()):
        out[f"class_{cls}"] = n
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    snap = summarise(_registry_at(SNAPSHOT_COMMIT))
    snap.update(sizes(SNAPSHOT_COMMIT))
    with (OUT / "registry_snapshot.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "value", "commit"])
        for k, v in snap.items():
            w.writerow([k, v, SNAPSHOT_COMMIT])

    log = _git("log", "--reverse", "--format=%h %ad", "--date=short",
               f"{SNAPSHOT_COMMIT}", "--", REGISTRY).split("\n")
    rows = []
    for line in filter(None, log):
        sha, date = line.split()
        s = summarise(_registry_at(sha))
        rows.append({"commit": sha, "date": date, "claims": s["claims"], "sites": s["sites"],
                     "retired": s["retired"], "unbacked": s["unbacked"],
                     "coverage_files": s["coverage_files"]})
    with (OUT / "registry_growth.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # CI history of the publication-sync workflow, from the committed export
    # ci_runs_pubs_sync.csv (gh run list, retrieved 2026-10-02).
    runs = list(csv.DictReader((OUT / "ci_runs_pubs_sync.csv").open(encoding="utf-8")))
    ok = [r for r in runs if r["conclusion"] == "success"]
    first_ok = min(r["created_at"] for r in ok)
    with (OUT / "ci_summary.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "value"])
        w.writerow(["runs", len(runs)])
        w.writerow(["failures", sum(r["conclusion"] == "failure" for r in runs)])
        w.writerow(["successes", len(ok)])
        w.writerow(["runs_before_first_success", sum(r["created_at"] < first_ok for r in runs)])
        w.writerow(["failures_after_first_success",
                    sum(r["created_at"] > first_ok and r["conclusion"] == "failure" for r in runs)])

    cat = catalogue_summary()
    with (OUT / "incident_summary.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "value"])
        for k, v in cat.items():
            w.writerow([k, v])

    print(f"snapshot @ {SNAPSHOT_COMMIT}: " + ", ".join(f"{k}={v}" for k, v in snap.items()))
    print("incidents: " + ", ".join(f"{k}={v}" for k, v in cat.items()))
    print(f"growth: {len(rows)} registry commits, {rows[0]['date']} .. {rows[-1]['date']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
