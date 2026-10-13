"""The context file stays a state file (.ace/standards/context.md)."""
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "pubs" / "check_active_context.py"
spec = importlib.util.spec_from_file_location("check_active_context", SCRIPT)
cac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cac)

HEAD = "# Active Context\n\n> History: archive/README.md, rule .ace/standards/context.md\n"


def make(tmp_path, body, index="| [2026-10-12.md](2026-10-12.md) | x |\n", files=("2026-10-12.md",)):
    context = tmp_path / "ACTIVE_CONTEXT.md"
    context.write_text(body, encoding="utf-8")
    archive = tmp_path / "archive"
    archive.mkdir()
    (archive / "README.md").write_text(index, encoding="utf-8")
    for name in files:
        (archive / name).write_text("# x\n", encoding="utf-8")
    return context, archive


def test_repository_files_pass():
    assert cac.problems() == []


def test_a_state_file_passes(tmp_path):
    assert cac.problems(*make(tmp_path, HEAD + "\n## Latest handoff - 2026-10-12\n")) == []


def test_a_long_file_fails(tmp_path):
    found = cac.problems(*make(tmp_path, HEAD + "line\n" * cac.MAX_LINES))
    assert any("limit" in p for p in found)


def test_the_archive_must_be_named_at_the_top(tmp_path):
    found = cac.problems(*make(tmp_path, "# Active Context\n" + "\n" * cac.HEAD_LINES + HEAD))
    assert len(found) == len(cac.REQUIRED_IN_HEAD)


def test_two_handoffs_fail(tmp_path):
    body = HEAD + "\n## Latest handoff - 2026-10-12\n\n## Session Handoff - 2026-10-11\n"
    assert any("handoffs" in p for p in cac.problems(*make(tmp_path, body)))


def test_the_index_and_the_files_must_agree(tmp_path):
    found = cac.problems(*make(tmp_path, HEAD, files=("2026-10-12.md", "2026-10-11.md")))
    assert found == ["archive file 2026-10-11.md is not in the index"]
    (tmp_path / "b").mkdir()
    found = cac.problems(*make(tmp_path / "b", HEAD, files=()))
    assert found == ["the index names 2026-10-12.md, which does not exist"]
