"""Every displayed equation of the thesis is numbered and cited (author rule, 2026-10-12)."""
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "pubs" / "check_equations.py"
spec = importlib.util.spec_from_file_location("check_equations", SCRIPT)
ce = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ce)


def run(tmp_path, **files):
    for name, text in files.items():
        (tmp_path / f"{name}.qmd").write_text(text, encoding="utf-8")
    return ce.problems(tmp_path)


def test_the_thesis_passes():
    assert ce.problems() == []


def test_a_labelled_and_cited_equation_passes(tmp_path):
    assert run(tmp_path, a="Según la @eq-uno:\n\n$$x = 1$$ {#eq-uno}\n") == []


def test_a_citation_from_another_chapter_counts(tmp_path):
    assert run(tmp_path, a="$$x =\n1$$ {#eq-uno}\n", b="Véase la @eq-uno.\n") == []


def test_an_equation_without_label_fails(tmp_path):
    found = run(tmp_path, a="Texto.\n\n$$x = 1$$\n")
    assert found == ["a.qmd:3 displayed equation without a label {#eq-...}"]


def test_an_equation_never_cited_fails(tmp_path):
    assert any("never cited" in p for p in run(tmp_path, a="$$x = 1$$ {#eq-uno}\n"))


def test_a_citation_without_equation_and_a_repeated_label_fail(tmp_path):
    found = run(tmp_path, a="La @eq-dos y la @eq-uno.\n\n$$x$$ {#eq-uno}\n\n$$y$$ {#eq-uno}\n")
    assert any("labels no equation" in p for p in found)
    assert any("already used" in p for p in found)


def test_a_figure_needs_a_label_and_a_citation(tmp_path):
    cited = "La @fig-uno muestra el resultado.\n\n![Pie de\nfigura.](a.png){#fig-uno width=80%}\n"
    assert run(tmp_path, a=cited) == []
    assert any("never cited" in p for p in run(tmp_path, a="![Pie.](a.png){#fig-uno}\n"))
    assert any("without a label" in p for p in run(tmp_path, a="![Pie.](a.png)\n"))
    assert any("labels no figure" in p for p in run(tmp_path, a="Véase la @fig-dos.\n"))


def test_a_table_needs_a_labelled_caption_and_a_citation(tmp_path):
    table = "| a | b |\n|---|---|\n| 1 | 2 |\n\n"
    caption = ": Pie de\ntabla. {#tbl-uno}\n"
    assert run(tmp_path, a="La @tbl-uno resume.\n\n" + table + caption) == []
    assert any("never cited" in p for p in run(tmp_path, a=table + caption))
    assert any("without a caption" in p for p in run(tmp_path, a=table + "Texto.\n"))


def test_code_blocks_are_not_read(tmp_path):
    assert run(tmp_path, a="```\n$$x = 1$$\n```\n") == []
