"""Lane guard rules (ADR-0021): path ownership and what one commit may contain."""
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "pubs" / "check_lane.py"
spec = importlib.util.spec_from_file_location("check_lane", SCRIPT)
check_lane = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_lane)

REG = check_lane.load_registry()


def lane(branch):
    return check_lane.lane_of(branch, REG)


def test_paths_resolve_to_their_lane():
    assert check_lane.owner_of("docs/reports/paper_d/paper_d_template.tex", REG) == "paper-d"
    assert check_lane.owner_of("scripts/pubs/render_paper_d.py", REG) == "paper-d"
    assert check_lane.owner_of("docs/reports/paper_c/PLAN.md", REG) == "paper-c"
    assert check_lane.owner_of("docs/reports/paper_bc/paper_bc_iberamia.tex", REG) == "paper-bc"
    assert check_lane.owner_of("thesis/capitulo-4-resultados.qmd", REG) == "thesis"
    assert check_lane.owner_of("tests/analysis/test_analyze_paper_e.py", REG) == "paper-e"


def test_unowned_paths_are_shared():
    for p in ("pub/claim_registry.toml", "docs/context/ACTIVE_CONTEXT.md",
              "scripts/pubs/verify_claims.py", "docs/adr/0021-one-working-tree-per-paper.md"):
        assert check_lane.owner_of(p, REG) is None


def test_no_path_has_two_owners():
    patterns = [(l["name"], pat) for l in REG["lane"] for pat in l["owns"]]
    for name, pat in patterns:
        probe = pat.replace("/**", "/x").replace("*", "x")
        owners = {n for n, p in patterns if check_lane.matches(probe, p)}
        assert owners == {name}, (pat, owners)


def test_branches_resolve_to_their_lane_and_folder():
    assert lane("paper/d-tecnologia-en-marcha")["folder"] == REG["main_folder"]
    assert lane("thesis/rca-001-phase-2")["name"] == "thesis"
    assert lane("paper/e-feature-agreement")["folder"] == REG["main_folder"]
    assert lane("paper/f-external-validity")["folder"] == "xai-paper-f"
    assert lane("paper/c-llm-judges")["name"] == "paper-c"
    assert lane("paper/c-llm-judges")["folder"] == REG["main_folder"]
    assert lane("main") is None
    assert lane("feature/anything") is None


def test_own_paths_pass():
    d = lane("paper/d-x")
    assert check_lane.commit_problems(["docs/reports/paper_d/paper_d_template.tex"], d, REG) == []


def test_shared_only_commit_passes():
    d = lane("paper/d-x")
    assert check_lane.commit_problems(["docs/context/ACTIVE_CONTEXT.md"], d, REG) == []


def test_another_lanes_path_is_refused():
    chapter = lane("chapter/cifie-sync-2026-09")
    problems = check_lane.commit_problems(["docs/reports/paper_d/paper_d.tex"], chapter, REG)
    assert len(problems) == 1 and "paper-d" in problems[0]


def test_mixing_lane_and_shared_paths_is_refused():
    d = lane("paper/d-x")
    problems = check_lane.commit_problems(
        ["docs/reports/paper_d/paper_d.tex", "pub/claim_registry.toml"], d, REG)
    assert len(problems) == 1 and "mixes" in problems[0]


def test_range_mode_refuses_a_commit_spanning_two_lanes():
    problems = check_lane.commit_problems(
        ["docs/reports/paper_d/paper_d.tex", "thesis/index.qmd"], None, REG)
    assert len(problems) == 1 and "several lanes" in problems[0]
