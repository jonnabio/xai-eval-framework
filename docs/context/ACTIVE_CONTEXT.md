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

## EXP3 Handoff: 2026-04-26

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
