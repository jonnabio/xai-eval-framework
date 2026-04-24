#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _fail(msg: str) -> None:
    raise SystemExit(msg)


def main() -> int:
    problems: list[str] = []

    thesis_index = ROOT / "thesis" / "index.qmd"
    thesis_expected = [
        "{{< include ../pub/fragments/thesis_resumen_es.qmd >}}",
        "{{< include ../pub/fragments/thesis_palabras_clave_es.qmd >}}",
        "{{< include ../pub/fragments/thesis_abstract_en.qmd >}}",
        "{{< include ../pub/fragments/thesis_keywords_en.qmd >}}",
    ]
    ti = _read(thesis_index)
    for needle in thesis_expected:
        if needle not in ti:
            problems.append(f"Missing include in {thesis_index}: {needle}")

    papers = {
        "paper_a": ROOT / "docs" / "reports" / "paper_a" / "paper_a_prototype_jmlr.tex",
        "paper_b": ROOT / "docs" / "reports" / "paper_b" / "paper_b_prototype_jmlr.tex",
        "paper_c": ROOT / "docs" / "reports" / "paper_c" / "paper_c_prototype_jmlr.tex",
    }
    for paper_id, path in papers.items():
        text = _read(path)
        abs_inc = f"\\input{{../../../pub/fragments/{paper_id}_abstract_en.tex}}"
        key_inc = f"\\input{{../../../pub/fragments/{paper_id}_keywords_en.tex}}"
        if abs_inc not in text:
            problems.append(f"Missing abstract include in {path}: {abs_inc}")
        if key_inc not in text:
            problems.append(f"Missing keywords include in {path}: {key_inc}")

    fragments = [
        ROOT / "pub" / "fragments" / "thesis_resumen_es.qmd",
        ROOT / "pub" / "fragments" / "thesis_abstract_en.qmd",
        ROOT / "pub" / "fragments" / "paper_a_abstract_en.tex",
        ROOT / "pub" / "fragments" / "paper_b_abstract_en.tex",
        ROOT / "pub" / "fragments" / "paper_c_abstract_en.tex",
    ]
    for frag in fragments:
        if not frag.exists():
            problems.append(f"Missing generated fragment: {frag}")

    if problems:
        joined = "\n".join(f"- {p}" for p in problems)
        _fail(f"Publication sync verification failed:\n{joined}\n")

    print("OK: papers and thesis are wired to pub/fragments")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

