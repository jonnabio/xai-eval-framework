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
4. Coverage: every result-shaped numeric literal in a guarded manuscript body is
   either registered (checks 1-2) or explicitly annotated as unbacked. Checks
   1-3 all answer "is this registered number still right?"; none of them answers
   "is this number registered at all?". The 2026-08-28 rigor review found four
   unbacked cost ranges, two disagreeing appendix probes and two mislabelled
   aggregations that all passed a green verifier for exactly that reason -- they
   were never registered. See RCA-001 and review finding F13.

Plus a structural check: artifact paths a manuscript points readers at must
exist in the working tree, so a paper cannot cite evidence that only lives on
an unmerged branch.
"""
from __future__ import annotations

import argparse
import re
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

# Numbers that carry results look like decimals ("0.808", "11,708.3") or
# thousands-separated integers ("28,209"). Bare small integers -- block counts,
# method counts, section numbers -- are structural and would drown the signal,
# so they are deliberately out of scope.
NUMBER_RE = re.compile(r"\d[\d,]*\.\d+|\d{1,3}(?:,\d{3})+")

# Stripped before scanning: they carry digits that are never results.
_TEX_COMMENT = re.compile(r"(?<!\\)%.*$", re.MULTILINE)
_MD_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_FENCED = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE = re.compile(r"`[^`\n]*`")
_URL = re.compile(r"https?://\S+|10\.\d{4,}/\S+|zenodo\.\d+", re.IGNORECASE)
_CITEKEY = re.compile(r"@[A-Za-z][A-Za-z0-9_-]*\d{4}[a-z]?")
_LATEX_CITE = re.compile(
    r"\\(?:cite[a-z]*|ref|label|includegraphics)\s*\{[^}]*\}"
)


def _literals(text: str) -> set[str]:
    return {m.group(0).replace(",", "") for m in NUMBER_RE.finditer(text)}


def _scannable(text: str) -> str:
    for pattern in (_MD_COMMENT, _FENCED, _TEX_COMMENT, _INLINE_CODE,
                    _LATEX_CITE, _URL, _CITEKEY):
        text = pattern.sub(" ", text)
    return text


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


def _check_coverage(registry: dict, problems: list[str]) -> tuple[int, int]:
    """Report result-shaped literals that no registry entry accounts for.

    A green run of checks 1-3 says every *registered* number is right. It says
    nothing about a load-bearing number nobody ever registered, which is how the
    F02/F03/F08/F09 defects survived. This closes that gap for the files listed
    under [coverage] in the registry.
    """
    coverage = registry.get("coverage") or {}
    files = coverage.get("files") or []
    if not files:
        return 0, 0

    allowed: set[str] = set()
    for claim in registry.get("claim", []):
        allowed |= _literals(claim["value"])
        for site in claim.get("appears_in", []):
            allowed |= _literals(site.get("text", ""))
    for entry in registry.get("retired", []):
        allowed |= _literals(entry.get("text", ""))
    for entry in registry.get("unbacked", []):
        allowed |= _literals(entry.get("text", ""))
    allowed |= set(coverage.get("structural") or [])

    n_files = 0
    n_unregistered = 0
    for rel in files:
        path = ROOT / rel
        if not path.exists():
            problems.append(f"[coverage] file not found: {rel}")
            continue
        n_files += 1
        seen: dict[str, int] = {}
        for lineno, line in enumerate(_scannable(_read(path)).splitlines(), 1):
            for literal in _literals(line):
                if literal not in allowed:
                    seen.setdefault(literal, lineno)
        for literal, lineno in sorted(seen.items(), key=lambda kv: kv[1]):
            n_unregistered += 1
            problems.append(
                f"[coverage] {rel}:{lineno} numeric literal {literal!r} is neither "
                f"registered nor annotated as unbacked -- add a [[claim]] with the "
                f"resolver that re-derives it, or an [[unbacked]] entry saying why "
                f"it cannot be"
            )
    return n_files, n_unregistered


def _decimals(literal: str) -> int:
    return len(literal.split(".", 1)[1]) if "." in literal else 0


def _check_exclusivity(registry: dict, problems: list[str]) -> int:
    """Keep an unpublished manuscript's results out of another publication.

    [exclusivity] names protected files, which may not print a result that is
    registered for an unpublished manuscript (`forbid`), unless the same
    result is also registered for an already published one (`allow_if_also`),
    or is listed as an [[exclusivity_exception]] with a reason.

    Matching is by value at the printed precision, not by text: Paper B+C
    prints "4.82" where another document prints "4.820". A literal matches a
    claim when it rounds from the claim's value at the literal's own number of
    decimals. Integers, and one-decimal literals below 10, are ignored as too
    coarse to identify a result; one-decimal literals of 10 or more
    (percentages, milliseconds such as "86.2") are compared.
    """
    cfg = registry.get("exclusivity") or {}
    files = cfg.get("files") or []
    if not files:
        return 0
    forbid = tuple(cfg.get("forbid") or [])
    allow = tuple(cfg.get("allow_if_also") or [])
    excepted = {e["text"] for e in registry.get("exclusivity_exception", [])}

    protected: list[tuple[str, float, set[str]]] = []
    for claim in registry.get("claim", []):
        site_files = [s["file"] for s in claim.get("appears_in", [])]
        if not any(f.startswith(forbid) for f in site_files):
            continue
        if any(f.startswith(allow) for f in site_files):
            continue
        texts = {lit for s in claim["appears_in"] for lit in _literals(s.get("text", ""))}
        protected.append((claim["id"], _as_number(claim["value"]), texts))

    checked = 0
    for rel in files:
        path = ROOT / rel
        if not path.exists():
            problems.append(f"[exclusivity] file not found: {rel}")
            continue
        checked += 1
        for lineno, line in enumerate(_scannable(_read(path)).splitlines(), 1):
            for literal in _literals(line):
                places = _decimals(literal)
                if literal in excepted or places == 0 or (places == 1 and float(literal) < 10):
                    continue
                shown = float(literal)
                step = 10 ** -_decimals(literal)
                for claim_id, value, texts in protected:
                    if literal in texts or abs(abs(value) - shown) <= step / 2 + 1e-12:
                        problems.append(
                            f"[exclusivity] {rel}:{lineno} prints {literal!r}, a result of the "
                            f"unpublished manuscript ({claim_id}); cite the thesis in prose instead, "
                            f"or add an [[exclusivity_exception]] saying why it is not that result"
                        )
                        break
    return checked


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Verify manuscript claims against artifacts.")
    parser.add_argument("--registry", default=str(REGISTRY_PATH), help="Path to claim_registry.toml")
    parser.add_argument(
        "--coverage-report",
        action="store_true",
        help="List unregistered numeric literals and exit 0 (triage aid for extending [coverage]).",
    )
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
    n_exclusive = _check_exclusivity(registry, problems)

    coverage_problems: list[str] = []
    n_cov_files, n_unregistered = _check_coverage(registry, coverage_problems)
    if args.coverage_report:
        for line in coverage_problems:
            print(line)
        print(
            f"coverage report: {n_unregistered} unregistered literal(s) "
            f"across {n_cov_files} file(s)"
        )
        return 0
    problems.extend(coverage_problems)

    if problems:
        joined = "\n".join(f"- {p}" for p in problems)
        raise SystemExit(f"Manuscript claim verification failed:\n{joined}\n")

    print(
        f"OK: {n_values} claims re-derived from artifacts, {n_sites} manuscript sites checked, "
        f"{n_retired} retired-value guards clear, {n_artifacts} cited artifacts present, "
        f"{n_cov_files} file(s) fully registered, "
        f"{n_exclusive} file(s) clear of unpublished results"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
