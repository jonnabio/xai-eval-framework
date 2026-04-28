# Active Context: XAI Evaluation Framework

- **Current Objective:** Developing the Multi-Level Evaluation Framework and drafting the PhD Thesis.
- **Current State:** 
    - **Thesis:** Structure finalized into a 5-chapter Quarto production environment in the top-level `/thesis` directory.
    - **Framework:** Transitioned title to "Marco para la Evaluación Multinivel de la Explicabilidad en IA".
    - **API & Dashboard:** Successfully integrated and serving finalized Experiment 1 results.
    - **References:** Consolidated ~124 research items into `thesis/references.bib`.
- **Next Steps:**
    1. Populate **Chapter 1** with refined Objectives and Research Questions.
    2. Populate **Chapter 2 (Foundations)** with LIME/SHAP and Taxonomy details from Paper C.
    3. Finalize Paper A (LLM Semantic Evaluation) results integration into **Chapter 4**.
    4. Render the first consolidated Word draft using `render.ps1`.
- **Active Constraints:**
    - **Tooling:** Quarto (required for thesis compilation).
    - **Template:** Must adhere to `thesis/assets/Plantilla_Tesis_Doctorado.docx`.
    - **Citations:** Use BibTeX format in `references.bib`.

## Integrated Evidence Pipeline: 2026-04-26

Current objective:

- Analyze EXP3 together with EXP1 and EXP2, then propagate the integrated
  evidence into the thesis and Paper A/B/C drafting surfaces.

Pipeline added:

- `scripts/integrate_experiment_evidence.py`
  - Normalizes EXP1, qualified EXP2, and completed EXP3 run-level metrics.
  - Applies the EXP2 recovery overlay from `outputs/batch_results.csv`.
  - Generates thesis and paper handoff fragments under
    `outputs/analysis/integrated_evidence/`.
- `docs/analysis/EXP1_EXP2_EXP3_INTEGRATION_PIPELINE.md`
  - Documents inputs, qualification rules, outputs, and publication guardrails.

Generated snapshot:

- EXP1 core calibration runs: `4 / 4`.
- EXP2 present result files: `299 / 300`.
- EXP2 qualified raw runs before recovery overlay: `274`.
- EXP2 recovery overlay rows: `30`.
- EXP2 analyzable runs after overlay: `275 / 300`.
- EXP3 completed runs: `24 / 24`.
- Integrated run rows: `303`.

Writing guidance:

- Use EXP2 for confirmatory statistical claims.
- Use EXP3 for external-validity and portability language.
- Use EXP1 for calibration, reproducibility, and historical continuity.
- Do not pool EXP2 and EXP3 into one omnibus hypothesis test without a new
  preregistered cross-study design.

Manuscript integration:

- Thesis introduction and future-work sections now position EXP4 as the next
  planned extension: an LLM-based semantic proxy evaluation layer for clarity,
  coherence, audit usefulness, and plausibility. This is explicitly bounded as
  proxy evaluation, not direct human validation.
- EXP4 planning documentation now follows the project experiment standard:
  experiment design README, result semantics README, execution plan, and ADR.
- EXP4 detailed protocol now defines PhD-level research questions, hypotheses,
  sampling, LLM judge conditions, rubric, schemas, statistical analysis, quality
  gates, and validity threats.
- EXP4 implementation planning now maps the protocol to concrete modules:
  schemas, case sampler, prompt renderer, LLM runner, parser, analysis pipeline,
  tests, and execution commands.
- EXP4 first-pass code implementation is now present: manifest, Pydantic
  schemas, EXP2/EXP3 case extraction, prompt rendering, dry-run/provider runner,
  parser, analysis exports, CLI scripts, and `tests/exp4`. The Windows
  `.venv-exp3` verification command `python -m pytest tests/exp4` passes with
  10 tests.
- EXP4 fixed case inventory has been generated with 192 cases from 126,017
  candidates: 96 from EXP2 Adult and 96 from EXP3 external-validation datasets
  (Breast Cancer and German Credit). The inventory has 192 unique case IDs and
  no empty normalized explanations.
- EXP4 5-case dry run has been executed end-to-end across the three prompt
  conditions. It produced 15 dummy LLM judgments, 15 parsed score rows, zero
  parse failures, and dry-run analysis summaries. These artifacts validate the
  execution path but are not real LLM evidence.
- EXP4 real-judge execution is prepared. The local environment has OpenAI,
  Google, and OpenRouter API credentials available. The manifest includes
  direct OpenAI and OpenRouter GPT-4.1 judge entries using locked model
  snapshots. The runner supports `--judge-id` filtering so real pilots can be
  limited to one judge, one condition, and a small case count before any full
  execution.
- EXP4 OpenRouter connectivity has been validated through a one-case real pilot
  using `openrouter_gpt41` (`openai/gpt-4.1-2025-04-14`) on the hidden-label
  primary condition. The run wrote one raw OpenRouter response, parsed it
  successfully, and kept parser failures at zero.
- EXP4 OpenRouter real pilot expansion has been completed for 24 hidden-label
  cases. It produced 24 raw OpenRouter judgments, parsed all responses with zero
  failures, and generated analysis summaries. The pilot pattern shows higher
  concision and semantic plausibility than completeness, audit usefulness, and
  actionability, supporting the thesis claim that technical XAI outputs require
  complementary semantic evaluation.
- EXP4 interpretation guidance now explicitly documents the distinction between
  raw feature attribution and human-usable explanation. Attribution lists such
  as SHAP top-feature values are treated as compact technical signals, while
  EXP4 evaluates whether they include enough context, directionality, domain
  meaning, audit usefulness, and actionability to function as explanations.
- EXP4 label-visible bias-probe execution has partial OpenRouter results: 12 of
  24 planned label-visible pilot judgments completed with zero parse failures
  before OpenRouter account credits stopped additional requests. In the 12
  paired cases, label visibility did not materially change overall quality
  scores, though semantic plausibility decreased modestly.
- Thesis Resumen and Abstract now include the EXP1/EXP2/EXP3 evidence structure,
  the EXP3 Breast Cancer/German Credit validation role, and the bounded EXP3
  SHAP-vs-Anchors portability result.
- Paper A/B/C abstracts now include the relevant EXP3 interpretation boundary:
  Paper A as portability evidence, Paper B as non-pooled supporting context, and
  Paper C as taxonomy grounding across reproducibility, confirmatory benchmark,
  and external-validation evidence.
- Thesis Chapter 4 now includes an EXP3 external-validation integration section.
- Thesis Chapter 5 limitations now distinguish Adult-centered confirmatory
  inference from EXP3 two-domain tabular validation.
- Thesis Chapter 3 methodology now documents EXP3 as a compact external
  validation phase with its own datasets, factors, and statistical boundary.
- Paper A includes EXP3 as a framework portability and external-validity check.
- Paper B includes EXP3 as supporting context, not as a replacement for the
  SHAP-LIME paired test.
- Paper C uses EXP3 to motivate layered technical-plus-semantic evaluation.

Regenerated review artifacts:

- Paper A/B/C branded and neutral PDFs were regenerated with Tectonic.
- Thesis DOCX and PDF were regenerated with Quarto.

## EXP3 Completion and Merge: 2026-04-26

Current objective:

- Analyze EXP3 as a completed cross-dataset validation package and integrate the
  findings into the thesis and paper result narratives.

Execution status:

- Windows Breast Cancer partition completed: `12 / 12` configs.
- Linux/WSL German Credit partition completed: `12 / 12` configs.
- The two result branches were merged into
  `results/exp3-windows-breast-cancer`.
- Merged branch head:
  `aa22d1112 Merge remote-tracking branch 'origin/results/exp3-linux-german-credit' into results/exp3-windows-breast-cancer`.
- Raw EXP3 artifact count:
  - `24 / 24` `results.json`;
  - `24 / 24` `metrics.csv`.

Documentation added:

- `docs/adr/0012-exp3-partitioned-result-merge.md`
  - Records the accepted partition merge procedure and branch-level provenance.
- `docs/results/exp3_cross_dataset/MERGED_ANALYSIS.md`
  - Summarizes EXP3 as one 24-run cross-dataset unit.
- `docs/results/exp3_cross_dataset/README.md`
  - Updated from "ready for partitioned execution" to "complete; both dataset
    partitions merged."

Primary merged result interpretation:

- SHAP preserved a strong advantage over Anchors on fidelity, faithfulness gap,
  and stability across the merged EXP3 unit.
- Anchors preserved a compact rule-style profile, with far fewer active
  features.
- Runtime favored SHAP overall in EXP3 because Anchors was slower on both
  dataset partitions.
- German Credit XGB is the main dataset/model-sensitive caveat: Anchors slightly
  exceeded SHAP on stability while SHAP retained higher fidelity.

Thesis impact:

- EXP3 now supports the bounded phrase "Adult-centered benchmark with
  two-domain external tabular validation."
- EXP3 should not be described as a replacement for EXP2 or as a universal
  cross-domain benchmark.

Next steps:

1. Use the merged result set for publication-quality EXP3 statistical tables.
2. Integrate the bounded EXP3 claim into the thesis external-validity section.
3. Decide whether to create a neutral branch alias from `aa22d1112` for final
   archival packaging.

## EXP3 Handoff: 2026-04-26

Superseded by the completion record above. The original handoff notes are
preserved for provenance.

Current objective:

- Prepare and launch EXP3 as a partitioned Windows + Linux/WSL execution, with
  Windows handling the Breast Cancer partition and Linux/WSL handling the German
  Credit partition.

What was added:

- `docs/planning/exp3_partitioned_execution_plan.md`
  - Full partitioned EXP3 runbook.
  - Dataset-level split: Windows = `breast_cancer`, Linux/WSL = `german_credit`.
  - Safety rules, preflights, smoke gate, execution loops, verification, and
    recovery steps.
- `scripts/setup_exp3_windows.ps1`
  - Windows automation for EXP3 setup and smoke testing.
  - Creates `.venv-exp3` with Python 3.11.
  - Installs `requirements.txt`.
  - Runs EXP3 dependency preflight.
  - Trains Breast Cancer RF seed `42`.
  - Runs `configs/experiments/exp3_cross_dataset/breast_cancer/rf_shap_s42_n100.yaml`.
  - Verifies the smoke `results.json`.
  - Optional `-RunBreastCancerPartition` switch launches all 12 Breast Cancer
    configs after smoke.
- Cross-links were added from:
  - `README.md`
  - `docs/experiments/README.md`
  - `docs/experiments/EXPERIMENTS_CATALOG.md`
  - `docs/experiments/exp3_cross_dataset/README.md`
  - `docs/planning/exp3_execution_plan.md`

Important finding:

- The existing Windows `.venv` uses Python 3.13.
- Installing `alibi` into that venv failed because dependency resolution fell
  into fragile source builds for compiled packages.
- EXP3 should use a dedicated Windows Python 3.11 venv: `.venv-exp3`.

Current execution status:

- EXP3 configs present: `24`.
- EXP3 seed-specific model artifacts are prepared:
  - `12` model binaries: `rf.joblib` / `xgb.joblib`;
  - `12` fitted preprocessors: `preprocessor.joblib`;
  - `12` training summaries: `exp3_training_summary.json`.
- EXP3 smoke gate passed on 2026-04-26:
  - config:
    `configs/experiments/exp3_cross_dataset/breast_cancer/rf_shap_s42_n100.yaml`;
  - result:
    `experiments/exp3_cross_dataset/results/breast_cancer/rf_shap/seed_42/n_100/results.json`.
- German Credit data is cached locally at `data/openml/dataset_31_credit-g.arff`.
- `src/data_loading/cross_dataset.py` now loads German Credit through the
  canonical OpenML ARFF download instead of sklearn's OpenML metadata API,
  which was failing with HTTP 301 redirect loops in this environment.
- Verification passed:
  - `pytest -q tests/test_cross_dataset_loader.py`: `3 passed`;
  - German Credit loader smoke: `(800, 61)` train and `(200, 61)` test.
- This Linux/container session cannot run Windows PowerShell because
  `powershell.exe`, `pwsh`, and `cmd.exe` are not available here.

Execution readiness:

- Linux/WSL German Credit partition is ready from this checkout, assuming Git
  push credentials are working.
- Windows Breast Cancer partition is ready after syncing/pulling this checkout
  on Windows and confirming the Windows Python 3.11 dependency preflight. The
  Linux smoke result already satisfies the EXP3 gate, but a Windows-side
  preflight remains necessary because Windows uses a separate `.venv-exp3`.

Branching status:

- `origin/results/exp3-linux-german-credit` exists and is the Linux/WSL result
  branch.
- `origin/results/exp3-windows-breast-cancer` exists and is the Windows result
  branch.
- Both were initialized at
  `6960da6c EXP3: prepare partitioned execution branches`.

Linux/WSL launch handoff:

```bash
git fetch origin
git switch results/exp3-linux-german-credit
git pull --ff-only
git push --dry-run
```

Then run only the German Credit partition from
`docs/planning/exp3_partitioned_execution_plan.md`.

Resume on Windows:

1. Open Windows PowerShell at the repo root:

   ```powershell
   cd C:\Users\jonna\Github\xai-eval-framework
   ```

2. Run the automated Windows EXP3 setup and dependency preflight:

   ```powershell
   .\scripts\setup_exp3_windows.ps1
   ```

3. Check the tail of the log:

   ```powershell
   Get-Content logs\setup_exp3_windows.log -Tail 30
   ```

4. If the script reports `Smoke gate passed` or finds the existing smoke result,
   launch the Windows Breast Cancer partition:

   ```powershell
   .\scripts\setup_exp3_windows.ps1 -SkipInstall -RunBreastCancerPartition
   ```

5. Launch the Linux/WSL German Credit partition only from the Linux/WSL
   environment using the commands in
   `docs/planning/exp3_partitioned_execution_plan.md`.
