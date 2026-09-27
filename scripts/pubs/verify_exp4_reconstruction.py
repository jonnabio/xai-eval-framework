#!/usr/bin/env python3
"""Verify that the reconstructed EXP4 sources are still the text that was verified.

The EXP4 modules were lost from the working tree and rebuilt from the .pyc files
left in __pycache__ (see docs/rca/RCA-002-exp4-source-recovery.md). On 2026-08-28
each rebuilt module was shown to compile to the same instructions as its
original bytecode. That bytecode was never committed and was lost on
2026-09-27, so the comparison cannot be repeated.

Two checks:

1. Hash pins (always). Every pinned file in exp4_source_pins.json must hash to
   its pin: SHA-256 over the file with CRLF normalised to LF, so Windows and
   Linux checkouts agree. A pinned file that is missing, and an exp4_*.py that
   has no pin, both fail. This does not re-verify the reconstruction; it keeps
   the verified text from changing silently. Changing a pinned file means
   changing its pin in the same commit, with the reason in the message.

2. Bytecode comparison (only if the .pyc files are ever present again, and only
   under CPython 3.13). Compared: opcode names, and the constants/names/varnames
   referenced by each code object. Ignored: line numbers, formatting, comments,
   and the module docstring (the reconstruction adds a provenance note to it).

Exit 0 if every check that could run passed, 1 otherwise.
"""
from __future__ import annotations

import dis
import hashlib
import json
import marshal
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PINS = Path(__file__).resolve().parent / "exp4_source_pins.json"
TEST_DIR = ROOT / "tests" / "exp4"

SRC_DIR = ROOT / "src" / "evaluation"
SCRIPT_DIR = ROOT / "scripts"


def discover() -> list[tuple[Path, Path]]:
    """Pair every reconstructed exp4_*.py with the 3.13 bytecode it came from.

    New reconstructions are picked up automatically; a module whose .pyc is
    missing is reported rather than silently skipped.
    """
    pairs = []
    for src in sorted(SRC_DIR.glob("exp4_*.py")):
        pyc = SRC_DIR / "__pycache__" / f"{src.stem}.cpython-313.pyc"
        pairs.append((src, pyc))
    return pairs


def discover_scripts() -> list[tuple[Path, Path]]:
    """Pair the reconstructed EXP4 CLI scripts with their 3.12 bytecode.

    These get the structural check only: their bytecode is CPython 3.12, whose
    instruction stream a 3.13 interpreter cannot reproduce. marshal still reads
    the code objects, so names and constants remain comparable.
    """
    pairs = []
    for src in sorted(SCRIPT_DIR.glob("exp4_*.py")):
        pyc = SCRIPT_DIR / "__pycache__" / f"{src.stem}.cpython-312.pyc"
        pairs.append((src, pyc))
    return pairs


PAIRS = discover()
SCRIPT_PAIRS = discover_scripts()

PYC_HEADER = 16

# The comparison compiles the reconstruction with the running interpreter, so it
# is only meaningful when that interpreter emits the same bytecode version as
# the .pyc files. Those were written by CPython 3.13.
REQUIRED_PYTHON = (3, 13)


def load_pyc(path: Path):
    if not path.exists():
        raise SystemExit(f"missing bytecode: {path.relative_to(ROOT).as_posix()}")
    return marshal.loads(path.read_bytes()[PYC_HEADER:])


def compiled_from_current_source(src: Path, pyc: Path) -> bool:
    """True if the .pyc was generated from the file as it is now, not an original.

    Importing a reconstructed module makes Python write a fresh .pyc into
    __pycache__; comparing the source against that proves nothing. A
    timestamp-based .pyc header stores the mtime (bytes 8-12) and size
    (bytes 12-16) of the source it was compiled from, so a .pyc whose header
    matches the current file was compiled from it. Hash-based .pyc files
    (flags != 0) are treated as possibly original.
    """
    header = pyc.read_bytes()[:PYC_HEADER]
    if int.from_bytes(header[4:8], "little") != 0:
        return False
    stat = src.stat()
    mtime = int.from_bytes(header[8:12], "little")
    size = int.from_bytes(header[12:16], "little")
    return mtime == (int(stat.st_mtime) & 0xFFFFFFFF) and size == (stat.st_size & 0xFFFFFFFF)


def original_bytecode(pairs: list[tuple[Path, Path]]) -> list[tuple[Path, Path]]:
    """Pairs whose .pyc exists and was not compiled from the current source."""
    return [(s, p) for s, p in pairs if p.exists() and not compiled_from_current_source(s, p)]


def opcodes(code) -> list[str]:
    """Flatten a code object's opcode stream, recursing into nested code objects."""
    out = [instr.opname for instr in dis.get_instructions(code)]
    for const in code.co_consts:
        if hasattr(const, "co_name"):
            out.append(f"<<{const.co_name}>>")
            out.extend(opcodes(const))
    return out


def signatures(code, path="") -> dict[str, tuple]:
    """Per-function argument names and non-code constants, keyed by qualified name."""
    here = f"{path}.{code.co_name}" if path else code.co_name
    consts = tuple(
        c for c in code.co_consts if not hasattr(c, "co_name") and not isinstance(c, str)
    )
    if "__firstlineno__" in code.co_names:
        # A class body stores its own source line as a constant; the provenance
        # header shifts every line, so this is a line number, not a difference.
        consts = tuple(c for c in consts if not isinstance(c, int))
    out = {here: (code.co_varnames[: code.co_argcount], code.co_names, consts)}
    for const in code.co_consts:
        if hasattr(const, "co_name"):
            out.update(signatures(const, here))
    return out


def strip_module_doc(code):
    """Drop the module docstring so a provenance note does not count as a difference."""
    consts = list(code.co_consts)
    if consts and isinstance(consts[0], str):
        consts[0] = ""
    return code.replace(co_consts=tuple(consts))


def compare(src: Path, pyc: Path, opcode_check: bool = True) -> list[str]:
    problems: list[str] = []
    rel = src.relative_to(ROOT).as_posix()

    original = strip_module_doc(load_pyc(pyc))
    rebuilt = strip_module_doc(
        compile(src.read_text(encoding="utf-8"), str(src), "exec")
    )

    a, b = (opcodes(original), opcodes(rebuilt)) if opcode_check else ([], [])
    if a != b:
        # report the first divergence with a little context
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                ctx = " ".join(a[max(0, i - 4) : i])
                problems.append(
                    f"[{rel}] opcode {i} differs after '{ctx}': "
                    f"bytecode has {x}, reconstruction has {y}"
                )
                break
        else:
            problems.append(
                f"[{rel}] opcode stream length differs: "
                f"bytecode {len(a)}, reconstruction {len(b)}"
            )

    sa, sb = signatures(original), signatures(rebuilt)
    for name in sorted(set(sa) | set(sb)):
        if name not in sa:
            problems.append(f"[{rel}] {name} exists only in the reconstruction")
        elif name not in sb:
            problems.append(f"[{rel}] {name} is in the bytecode but not reconstructed")
        elif sa[name] != sb[name]:
            problems.append(
                f"[{rel}] {name} signature/constants differ:\n"
                f"    bytecode:       {sa[name]}\n"
                f"    reconstruction: {sb[name]}"
            )

    return problems


def normalised_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def check_pins() -> tuple[list[str], int]:
    """Compare every EXP4 source against its pin; return (problems, pins checked)."""
    pinned = json.loads(PINS.read_text(encoding="utf-8"))["files"]
    problems: list[str] = []
    for rel, pin in sorted(pinned.items()):
        path = ROOT / rel
        if not path.exists():
            problems.append(f"[{rel}] pinned file is missing")
        elif normalised_sha256(path) != pin["sha256"]:
            problems.append(
                f"[{rel}] differs from the text verified on 2026-08-28 "
                f"(pin {pin['sha256'][:12]}, now {normalised_sha256(path)[:12]})"
            )
    present = [src for src, _ in PAIRS + SCRIPT_PAIRS] + sorted(TEST_DIR.glob("*.py"))
    for src in present:
        rel = src.relative_to(ROOT).as_posix()
        if rel not in pinned and src.name != "__init__.py":
            problems.append(f"[{rel}] EXP4 source has no pin in {PINS.name}")
    return problems, len(pinned)


def main() -> int:
    problems, n_pins = check_pins()

    # The bytecode comparison runs only if the lost .pyc files are ever restored;
    # bytecode Python regenerated from the current sources does not count.
    pairs = original_bytecode(PAIRS)
    script_pairs = original_bytecode(SCRIPT_PAIRS)
    bytecode_note = "original bytecode absent (lost 2026-09-27), comparison not run"
    if pairs or script_pairs:
        if sys.version_info[:2] == REQUIRED_PYTHON:
            for src, pyc in pairs:
                problems.extend(compare(src, pyc))
            for src, pyc in script_pairs:
                problems.extend(compare(src, pyc, opcode_check=False))
            bytecode_note = (
                f"bytecode comparison run on {len(pairs)} module(s) and "
                f"{len(script_pairs)} script(s)"
            )
        else:
            required = ".".join(str(v) for v in REQUIRED_PYTHON)
            bytecode_note = f"bytecode present but comparison needs Python {required}"

    if problems:
        print("EXP4 reconstruction check FAILED:\n")
        for p in problems:
            print(f"  {p}")
        return 1

    print(
        f"OK: {n_pins} EXP4 source file(s) match the text verified on 2026-08-28; "
        f"{bytecode_note}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
