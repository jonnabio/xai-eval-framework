#!/usr/bin/env python3
"""Verify that manuscript numbers still match the artifacts they came from.

Three checks, driven by pub/claim_registry.toml:

1. Every registered claim's value is re-derived from the committed artifacts and
   compared within tolerance. Catches a manuscript number going stale because
   the analysis was re-run.
2. Every registered claim's literal text is still present in each manuscript
   that is supposed to carry it. Catches a number being edited to something the
   artifacts do not support.
3. Retired values (numbers a previous audit removed) must not reappear in the
   manuscripts. This is the regression guard proper -- see RCA-001.

Plus a structural check: artifact paths a manuscript points readers at must
exist in the working tree, so a paper cannot cite evidence that only lives on
an unmerged branch.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    import tomllib  # py3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

sys.path.insert(0, str(Path(__file__).resolve().parent))
from claim_sources import MissingArtifact, resolve  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "pub" / "claim_registry.toml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _as_number(text: str) -> float:
    return float(text.replace(",", "").replace("$", "").strip())


def _check_values(registry: dict, problems: list[str]) -> int:
    checked = 0
    for claim in registry.get("claim", []):
        claim_id = claim["id"]
        try:
            actual = resolve(claim["source"])
        except MissingArtifact as exc:
            problems.append(f"[{claim_id}] {exc}")
            continue
        expected = _as_number(claim["value"])
        tolerance = float(claim.get("tolerance", 0.0005))
        if abs(actual - expected) > tolerance:
            problems.append(
                f"[{claim_id}] registered {claim['value']} but {claim['source']} "
                f"now yields {actual:.6g} (tolerance {tolerance:g})"
            )
        checked += 1
    return checked


def _check_appearances(registry: dict, problems: list[str]) -> int:
    checked = 0
    for claim in registry.get("claim", []):
        for site in claim.get("appears_in", []):
            path = ROOT / site["file"]
            if not path.exists():
                problems.append(f"[{claim['id']}] manuscript not found: {site['file']}")
                continue
            needle = site.get("text", claim["value"])
            found = _read(path).count(needle)
            if found == 0:
                problems.append(
                    f"[{claim['id']}] {site['file']} no longer contains \"{needle}\""
                )
            elif "count" in site and found != site["count"]:
                # A bare substring test passes as long as the value survives
                # anywhere in the file, which is too weak for a number that also
                # appears in prose. Pinning the occurrence count catches an edit
                # to one site out of several.
                problems.append(
                    f"[{claim['id']}] {site['file']} contains \"{needle}\" {found} time(s), "
                    f"expected {site['count']}"
                )
            checked += 1
    return checked


def _check_retired(registry: dict, problems: list[str]) -> int:
    checked = 0
    for entry in registry.get("retired", []):
        for rel in entry["files"]:
            path = ROOT / rel
            if not path.exists():
                problems.append(f"[retired:{entry['id']}] file not found: {rel}")
                continue
            if entry["text"] in _read(path):
                problems.append(
                    f"[retired:{entry['id']}] stale value \"{entry['text']}\" reappeared "
                    f"in {rel} -- {entry['reason']}"
                )
            checked += 1
    return checked


def _check_cited_artifacts(registry: dict, problems: list[str]) -> int:
    checked = 0
    for entry in registry.get("cited_artifact", []):
        target = ROOT / entry["path"]
        present = target.exists() and (not entry.get("glob") or any(target.glob(entry["glob"])))
        if not present:
            problems.append(
                f"[artifact:{entry['id']}] {entry['path']} "
                f"{'(glob ' + entry['glob'] + ') ' if entry.get('glob') else ''}"
                f"is cited by {entry['cited_by']} but is not in the working tree"
            )
        checked += 1
    return checked


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Verify manuscript claims against artifacts.")
    parser.add_argument("--registry", default=str(REGISTRY_PATH), help="Path to claim_registry.toml")
    args = parser.parse_args(argv)

    registry_path = Path(args.registry)
    if not registry_path.exists():
        raise SystemExit(f"Claim registry not found: {registry_path}")

    registry = tomllib.loads(registry_path.read_text(encoding="utf-8"))
    problems: list[str] = []

    n_values = _check_values(registry, problems)
    n_sites = _check_appearances(registry, problems)
    n_retired = _check_retired(registry, problems)
    n_artifacts = _check_cited_artifacts(registry, problems)

    if problems:
        joined = "\n".join(f"- {p}" for p in problems)
        raise SystemExit(f"Manuscript claim verification failed:\n{joined}\n")

    print(
        f"OK: {n_values} claims re-derived from artifacts, {n_sites} manuscript sites checked, "
        f"{n_retired} retired-value guards clear, {n_artifacts} cited artifacts present"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
