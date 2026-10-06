#!/usr/bin/env python3
"""Paper F: copy the raw rows of finished jobs to a directory that git tracks.

    python scripts/paper_f_snapshot.py

The run writes to outputs/analysis/paper_f/runs/ (local, git-ignored, files still being
written). This script copies the file of every job that has its `.done` marker to
outputs/analysis/paper_f/raw/<dataset>/<model>/seed_<seed>/<explainer>.jsonl, unchanged.
A finished job is never written again, so a file once copied stays as it is; the script
only adds files. It reads no value: it copies, and counts lines for the manifest.

outputs/analysis/paper_f/raw/MANIFEST.csv lists every copied file with its number of rows,
failed rows and SHA-256, so that a later copy can be checked against the first.
"""
from __future__ import annotations

import csv
import hashlib
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_f_lib as lib  # noqa: E402

RUNS = lib.OUT / "runs"
RAW = lib.OUT / "raw"


def main() -> int:
    copied = 0
    for marker in sorted(RUNS.glob("*/*/seed_*/*.done")):
        src = marker.with_suffix(".jsonl")
        dst = RAW / src.relative_to(RUNS)
        if not src.exists() or dst.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        copied += 1
    rows = []
    for path in sorted(RAW.glob("*/*/seed_*/*.jsonl")):
        data = path.read_bytes()
        lines = [l for l in data.splitlines() if l.strip()]
        d, m, s = path.relative_to(RAW).parts[:3]
        rows.append({"dataset": d, "model": m, "seed": s.removeprefix("seed_"),
                     "explainer": path.stem, "rows": len(lines),
                     "failed": sum(b'"failed": 1' in l for l in lines),
                     "sha256": hashlib.sha256(data).hexdigest()})
    RAW.mkdir(parents=True, exist_ok=True)
    with (RAW / "MANIFEST.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["dataset", "model", "seed", "explainer", "rows",
                                                "failed", "sha256"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    by_seed: dict[str, list[int]] = {}
    for r in rows:
        by_seed.setdefault(r["seed"], [0, 0])
        by_seed[r["seed"]][0] += 1
        by_seed[r["seed"]][1] += r["rows"]
    print(f"{copied} new files copied; {len(rows)} files, {sum(r['rows'] for r in rows)} rows, "
          f"{sum(r['failed'] for r in rows)} failed rows in {RAW.relative_to(lib.ROOT)}")
    for seed, (files, n) in sorted(by_seed.items(), key=lambda kv: int(kv[0])):
        print(f"  seed {seed}: {files} finished jobs, {n} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
