#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

try:
    import tomllib  # py3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


ROOT = Path(__file__).resolve().parents[2]
CLAIMS_PATH = ROOT / "pub" / "claims.toml"
FRAGMENTS_DIR = ROOT / "pub" / "fragments"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _join_keywords(items: list[str]) -> str:
    return "; ".join(x.strip() for x in items if x.strip())


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate pub fragments from SSOT claims.")
    parser.add_argument("--claims", default=str(CLAIMS_PATH), help="Path to claims.toml")
    parser.add_argument("--out", default=str(FRAGMENTS_DIR), help="Output fragments directory")
    args = parser.parse_args(argv)

    claims_path = Path(args.claims)
    out_dir = Path(args.out)

    if not claims_path.exists():
        raise SystemExit(f"Claims file not found: {claims_path}")

    data = tomllib.loads(claims_path.read_text(encoding="utf-8"))
    thesis = data["thesis"]
    papers = data["papers"]

    header = (
        "<!--\n"
        "  AUTO-GENERATED FILE.\n"
        "  Source: pub/claims.toml\n"
        "  Do not edit by hand.\n"
        "-->\n\n"
    )

    # Thesis (Quarto fragments)
    _write(out_dir / "thesis_title.txt", f"{thesis['title'].strip()}\n")
    _write(out_dir / "thesis_resumen_es.qmd", header + thesis["resumen_es"].strip() + "\n")
    _write(
        out_dir / "thesis_palabras_clave_es.qmd",
        header + f"**Palabras clave:** {_join_keywords(thesis['palabras_clave_es'])}.\n",
    )
    _write(out_dir / "thesis_abstract_en.qmd", header + thesis["abstract_en"].strip() + "\n")
    _write(
        out_dir / "thesis_keywords_en.qmd",
        header + f"**Keywords:** {_join_keywords(thesis['keywords_en'])}.\n",
    )

    # Papers (LaTeX fragments)
    for paper_id in ("paper_a", "paper_b", "paper_c"):
        paper = papers[paper_id]
        _write(
            out_dir / f"{paper_id}_abstract_en.tex",
            "% AUTO-GENERATED FILE. Source: pub/claims.toml\n"
            + paper["abstract_en_tex"].strip()
            + "\n",
        )
        _write(
            out_dir / f"{paper_id}_keywords_en.tex",
            "% AUTO-GENERATED FILE. Source: pub/claims.toml\n"
            + paper["keywords_en_tex"].strip()
            + "\n",
        )

    # Minimal build metadata
    _write(
        out_dir / "build_meta.env",
        f"CLAIMS_PATH={claims_path.as_posix()}\n"
        f"CLAIMS_MTIME={int(os.path.getmtime(claims_path))}\n",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

