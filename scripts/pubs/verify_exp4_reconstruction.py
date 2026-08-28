#!/usr/bin/env python3
"""Verify that reconstructed EXP4 sources are equivalent to the original bytecode.

The EXP4 modules were lost from the working tree and rebuilt from the .pyc files
left in __pycache__ (see docs/rca/RCA-002-exp4-source-recovery.md). A rebuilt
file is only trustworthy if it compiles to the same instructions as the original,
so this check compiles each reconstruction and compares its opcode stream against
the committed bytecode.

Compared: opcode names, and the constants/names/varnames referenced by each code
object. Ignored: line numbers, formatting, comments, and the module docstring
(the reconstruction adds a provenance note to it).

Exit 0 if every reconstruction matches its bytecode, 1 otherwise.
"""
from __future__ import annotations

import dis
import marshal
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# reconstructed source -> the .pyc it must match
PAIRS = [
    (
        ROOT / "src" / "evaluation" / "exp4_reliability_metrics.py",
        ROOT / "src" / "evaluation" / "__pycache__" / "exp4_reliability_metrics.cpython-313.pyc",
    ),
]

PYC_HEADER = 16

# The comparison compiles the reconstruction with the running interpreter, so it
# is only meaningful when that interpreter emits the same bytecode version as
# the .pyc files. Those were written by CPython 3.13.
REQUIRED_PYTHON = (3, 13)


def load_pyc(path: Path):
    if not path.exists():
        raise SystemExit(f"missing bytecode: {path.relative_to(ROOT).as_posix()}")
    return marshal.loads(path.read_bytes()[PYC_HEADER:])


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


def compare(src: Path, pyc: Path) -> list[str]:
    problems: list[str] = []
    rel = src.relative_to(ROOT).as_posix()

    original = strip_module_doc(load_pyc(pyc))
    rebuilt = strip_module_doc(
        compile(src.read_text(encoding="utf-8"), str(src), "exec")
    )

    a, b = opcodes(original), opcodes(rebuilt)
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


def main() -> int:
    if sys.version_info[:2] != REQUIRED_PYTHON:
        running = ".".join(str(v) for v in sys.version_info[:2])
        required = ".".join(str(v) for v in REQUIRED_PYTHON)
        print(
            f"SKIP: EXP4 bytecode is CPython {required}; this interpreter is "
            f"{running}, which emits different instructions. Re-run under "
            f"Python {required} to check the reconstruction."
        )
        return 0

    problems: list[str] = []
    for src, pyc in PAIRS:
        problems.extend(compare(src, pyc))

    if problems:
        print("EXP4 reconstruction does NOT match the original bytecode:\n")
        for p in problems:
            print(f"  {p}")
        return 1

    print(
        f"OK: {len(PAIRS)} reconstructed EXP4 module(s) compile to the same "
        f"instructions as the committed bytecode"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
