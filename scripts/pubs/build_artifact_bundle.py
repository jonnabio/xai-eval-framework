"""Build the artifact bundle archived with Paper B+C (code and data release).

Run from anywhere:  python scripts/pubs/build_artifact_bundle.py

Scrubbing happens on the copies. The in-repo artifacts are the evidence the
claim registry resolves against and are left untouched.
"""
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "docs" / "reports" / "paper_bc" / "_bundle_stage"
OUT = ROOT / "docs" / "reports" / "paper_bc" / "paper_bc_artifacts.zip"

if STAGE.exists():
    shutil.rmtree(STAGE)
STAGE.mkdir(parents=True)

# (source, destination-inside-bundle)
COPY = [
    ("outputs/analysis/paper_a_exp2_stats", "analysis/exp2_stats"),
    ("outputs/analysis/exp4_llm_evaluation", "analysis/exp4_llm_evaluation"),
    # EXP4 replication cohort (ADR-0017): analysis exports, and the raw judge
    # responses, rendered prompts and case inventory the original lacks.
    ("outputs/analysis/exp4_cohort2", "analysis/exp4_cohort2"),
    ("experiments/exp4_cohort2", "experiments/exp4_cohort2"),
    ("src/prompts/templates/exp4_semantic_eval_v1.j2",
     "experiments/exp4_cohort2/templates/exp4_semantic_eval_v1.j2"),
    ("src/prompts/templates/exp4_semantic_eval_v1_label_visible.j2",
     "experiments/exp4_cohort2/templates/exp4_semantic_eval_v1_label_visible.j2"),
    ("src/prompts/templates/exp4_semantic_eval_v1_alt.j2",
     "experiments/exp4_cohort2/templates/exp4_semantic_eval_v1_alt.j2"),
    ("scripts/exp4_cohort2_compare.py", "scripts/exp4_cohort2_compare.py"),
    ("outputs/analysis/exp6_masking_sensitivity", "analysis/exp6_masking_sensitivity"),
    ("outputs/analysis/exp3_lime_results.csv", "analysis/exp3_lime_results.csv"),
    ("outputs/analysis/lime_kernel_width_sensitivity.csv",
     "analysis/lime_kernel_width_sensitivity.csv"),
    ("experiments/exp3_cross_dataset/results", "experiments/exp3_cross_dataset/results"),
    ("scripts/run_exp2_statistical_analysis.py", "scripts/run_exp2_statistical_analysis.py"),
    ("scripts/generate_paper_b_figures.py", "scripts/generate_paper_b_figures.py"),
    ("scripts/run_exp6_masking_sensitivity.py", "scripts/run_exp6_masking_sensitivity.py"),
    ("docs/reports/paper_bc/paper_bc_review_corpus.csv", "review_corpus/review_corpus.csv"),
    ("docs/reports/paper_bc/corpus_pdfs/RETRIEVAL_LOG.md", "review_corpus/RETRIEVAL_LOG.md"),
    ("data/adult.csv", "data/adult.csv"),
    # The paper, whose Appendix A holds supplementary Tables S1-S6, travels
    # inside the bundle (RCA-003: never omit the supplementary tables).
    ("docs/reports/paper_bc/paper_bc_iberamia.pdf",
     "paper_with_appendix.pdf"),
]

missing = []
for src, dst in COPY:
    s, d = ROOT / src, STAGE / dst
    if not s.exists():
        missing.append(src)
        continue
    d.parent.mkdir(parents=True, exist_ok=True)
    if s.is_dir():
        shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)
print("copied:", len(COPY) - len(missing), "entries; missing:", missing or "none")
if missing:
    shutil.rmtree(STAGE)
    raise SystemExit("refusing to build an incomplete bundle")

# --- scrub identifying absolute paths from the copies --------------------
PATTERNS = [
    r"C:\\\\Users\\\\jonna\\\\Github\\\\xai-eval-framework\\\\",  # JSON-escaped
    r"C:\\Users\\jonna\\Github\\xai-eval-framework\\",
    r"C:/Users/jonna/Github/xai-eval-framework/",
]
scrubbed = {}
for p in STAGE.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in {".csv", ".json", ".md", ".py", ".txt"}:
        continue
    try:
        t = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    orig = t
    for pat in PATTERNS:
        t = re.sub(pat, "", t)
    if t != orig:
        p.write_text(t, encoding="utf-8", newline="")
        scrubbed[str(p.relative_to(STAGE))] = orig.count("jonna")
for k, v in scrubbed.items():
    print(f"  scrubbed {v:5d} path(s) in {k}")

README = """# Artifact bundle

Artifact bundle for "From Fidelity to Semantics: A Taxonomy of Explainable
AI Evaluation Metrics and a Paired Empirical Comparison of LIME and SHAP".
Local user paths are scrubbed.

## Contents

    paper_with_appendix.pdf           the paper; Appendix A holds the
                                      supplementary Tables S1-S6.
    analysis/exp2_stats/              EXP2 inferential exports. Every EXP2
                                      number in the paper is computed from
                                      these files, not from the raw runs.
    analysis/exp4_llm_evaluation/     ICC and Krippendorff alpha exports
                                      behind the inter-judge reliability
                                      result (original cohort).
    analysis/exp4_cohort2/            reliability by condition and pooled,
                                      label-bias and rubric-sensitivity
                                      contrasts for the EXP4 replication.
    experiments/exp4_cohort2/         the replication's 192-case inventory,
                                      rendered prompts, templates, raw judge
                                      responses and parsed scores.
    analysis/exp6_masking_sensitivity/ masking-scheme sensitivity exports
                                      (supplementary Table S6).
    analysis/exp3_lime_results.csv    EXP3 LIME extension.
    analysis/lime_kernel_width_sensitivity.csv   supplementary Table S2.
    experiments/exp3_cross_dataset/results/      raw EXP3 runs; the
                                      cross-dataset fidelity values are
                                      derived directly from these.
    scripts/                          the analysis scripts cited in the
                                      paper.
    review_corpus/                    the 44-row coded corpus behind the
                                      taxonomy and gap analysis, with a
                                      per-paper retrieval log.
    data/adult.csv                    UCI Adult Income, so the supplementary
                                      association table can be recomputed.

## Not included, and why

    experiments/exp2_scaled/results/  251 MB of raw EXP2 runs, above the
                                      100 MB supplementary limit. The
                                      exports under analysis/exp2_stats/ are
                                      what the paper's numbers are computed
                                      from.
    review_corpus full texts          46 third-party publications, ~142 MB,
                                      not redistributable. RETRIEVAL_LOG.md
                                      records a source and a verification
                                      per paper so the set is reproducible.

Both are in the public release, which is linked from the camera-ready version.

## Note

Absolute filesystem paths have been removed from three exported files so the
bundle carries no author-identifying information. No numeric value was
altered; the paths appeared only in provenance columns and metadata.
"""
(STAGE / "README.md").write_text(README, encoding="utf-8")

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(STAGE.rglob("*")):
        if p.is_file():
            z.write(p, p.relative_to(STAGE).as_posix())

n = sum(1 for p in STAGE.rglob("*") if p.is_file())
print(f"\nbundle: {OUT}  {OUT.stat().st_size/1e6:.1f} MB, {n} files")

# Leave no staging copy behind; the zip is the deliverable.
shutil.rmtree(STAGE)
print("staging removed; regenerate with: python scripts/pubs/build_artifact_bundle.py")
