#!/usr/bin/env python3
"""Paper G: record the run host in experiments/exp_g/host.json (RUN_PROTOCOL.md, section 3).

    python scripts/paper_g_host_check.py

Records OS, kernel, CPU model and cores, RAM, free disk, Python and the versions of the
packages the run uses, and the git commit. Fails (exit 1) if Python is not 3.13 or a
package version differs from requirements-frozen.txt, so that a mismatch is seen before the run.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments" / "exp_g" / "host.json"
PACKAGES = ("numpy", "pandas", "scipy", "scikit-learn", "xgboost", "shap", "lime")


def cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def ram_gib() -> float | None:
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                return round(int(line.split()[1]) / 1024**2, 1)
    except OSError:
        return None
    return None


def os_name() -> str:
    try:
        rel = dict(line.split("=", 1) for line in Path("/etc/os-release").read_text().splitlines()
                   if "=" in line)
        return rel.get("PRETTY_NAME", "").strip('"')
    except OSError:
        return platform.platform()


def frozen() -> dict:
    pins = {}
    for line in (ROOT / "requirements-frozen.txt").read_text(encoding="utf-8").splitlines():
        if "==" in line and not line.startswith("#"):
            name, ver = line.split("==", 1)
            pins[name.strip().lower()] = ver.strip()
    return pins


def main() -> int:
    pins = frozen()
    versions, mismatches = {}, []
    for p in PACKAGES:
        try:
            versions[p] = metadata.version(p)
        except metadata.PackageNotFoundError:
            versions[p] = None
        if pins.get(p) and versions[p] != pins[p]:
            mismatches.append(f"{p}: installed {versions[p]}, pinned {pins[p]}")
    commit = subprocess.run(["git", "rev-parse", "--short=12", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True).stdout.strip()
    record = {
        "hostname": platform.node(), "os": os_name(), "kernel": platform.release(),
        "cpu": cpu_model(), "logical_cpus": os.cpu_count(), "ram_gib": ram_gib(),
        "free_disk_gib": round(shutil.disk_usage(ROOT).free / 1024**3, 1),
        "python": platform.python_version(), "packages": versions, "commit": commit,
        "pin_mismatches": mismatches,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=1))
    ok = sys.version_info[:2] == (3, 13) and not mismatches
    if not ok:
        print("HOST CHECK FAILED: Python must be 3.13 and packages must match the pins.",
              file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
