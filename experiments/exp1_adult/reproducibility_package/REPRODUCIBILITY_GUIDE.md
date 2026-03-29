# Reproducibility Guide: Experiment 1 (Adult Dataset) - XAI Evaluation Framework

This guide provides step-by-step instructions to reproduce the experimental results for the Adult dataset use case in the XAI Evaluation Framework. It covers environment setup, data acquisition, model training, XAI generation, results extraction, and thesis chapter generation.

## 1. Prerequisites

### Hardware Requirements
*   **Minimum**: 4 CPU cores, 8 GB RAM, 2 GB disk space. Runtime: ~2 hours.
*   **Recommended**: 8+ CPU cores, 16 GB RAM. Runtime: ~30 minutes (parallel execution).
*   **Platform**: Tested on macOS 13+ (Apple Silicon/Intel), Ubuntu 20.04+, Windows 10+ (WSL2).

### Software Requirements
*   **Python**: 3.11.5
*   **Git**: For checking out the codebase.
*   **Docker** (Optional): For containerized reproduction.

### Cloud Dependencies (Optional)
*   **OpenAI API Key**: Required *only* if you wish to re-run the LLM-based evaluation from scratch.
    *   *Default behavior*: The pipeline uses cached responses (`experiments/exp1_adult/llm_eval/cached_responses.json`) for deterministic reproduction without API costs.
    *   To use live API: `export OPENAI_API_KEY="sk-..."`

## 2. Environment Setup

### Option A: Conda (Recommended)
```bash
conda env create -f environment.yml
conda activate xai-eval
```

### Option B: Pip
```bash
# It is recommended to use a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-frozen.txt
```

### Option C: Docker
See Section 6 for containerized execution.

## 3. Data Acquisition & Provenance

**Dataset**: [UCI Adult Income Dataset](https://archive.ics.uci.edu/ml/datasets/adult)
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

Run the automated download command:
```bash
python scripts/download_data.py --data-dir data/adult
```
*   **Verification**: The script automatically verifies the MD5 checksum of `adult.data` (`5d7c39d7b8804f071cdd1f2a7c460872`).

## 4. Reproducibility Settings & Seeds

To ensure deterministic results, we enforce the following random seeds:
*   **Data Splitting**: `random_state=42`
*   **Model Training**:
    *   Random Forest: `random_state=42`
    *   XGBoost: `random_seed=42`
*   **LIME Sampling**: `random_state=42`
*   **SHAP Background**: `random_state=42` (kmeans summary)
*   **Cross-Validation**: `random_state=42` (KFold shuffle)

## 5. Execution Instructions

We provide a master orchestration script `experiments/exp1_adult/reproducibility_package/run_full_pipeline.sh`.

### Mode 1: Minimal Reproduction (Thesis Ready)
Reproduces trained models, XAI scores, and generates the LaTeX Results Chapter.
**Runtime**: ~1.5 hours.

```bash
bash experiments/exp1_adult/reproducibility_package/run_full_pipeline.sh --mode minimal
```

### Mode 2: Complete Reproduction (Statistical Analysis)
Includes Cross-Validation (5-fold) and Statistical Significance testing.
**Runtime**: ~15-20 hours (depending on hardware).

```bash
bash experiments/exp1_adult/reproducibility_package/run_full_pipeline.sh --mode complete
```

### Manual Steps (If not using script)
1.  **Train Models**: `python scripts/run_train_models.py --model all`
2.  **Run Experiments**: `python -m src.experiment.runner --config configs/experiments/exp1_adult_rf_lime.yaml` (repeat for all 4 configs)
3.  **Extract Results**: `python src/scripts/extract_results_metadata.py ...`
4.  **Generate LaTeX**: `python src/scripts/generate_results_latex.py ...`

## 6. Verification

After execution, verify the integrity of the results using the automated checker:

```bash
python experiments/exp1_adult/reproducibility_package/verify_reproducibility.py
```
This script checks:
1.  Environment versions.
2.  Data integrity.
3.  Model existence.
4.  Metric values (within valid tolerance of original results).
5.  Presence of generated LaTeX artifacts.

## 7. Repository Snapshot and Archiving

The current public repository is:
*   **Repository**: [https://github.com/jonnabio/xai-eval-framework](https://github.com/jonnabio/xai-eval-framework)
*   **Paper A snapshot release tag**: `paper-a-submission-2026-03-28`
*   **Version-specific Zenodo DOI**: [10.5281/zenodo.19297724](https://doi.org/10.5281/zenodo.19297724)

Archive citation:
```bibtex
@software{herrera_vasquez_2026_xai_eval_framework,
  author = {Jonathan Herrera-Vasquez},
  title = {XAI Evaluation Framework},
  version = {0.2.0},
  doi = {10.5281/zenodo.19297724},
  url = {https://github.com/jonnabio/xai-eval-framework},
  note = {Repository snapshot for reproducibility materials; release tag paper-a-submission-2026-03-28}
}
```

## 8. Troubleshooting

*   **Missing Data**: Ensure `experiments/exp1_adult/reproducibility_package/run_full_pipeline.sh` has executable permissions (`chmod +x`).
*   **OpenAI Errors**: Ensure `OPENAI_API_KEY` is set if running without cache.
*   **Windows Paths**: Use WSL2 or Git Bash to run `.sh` scripts to avoid path separator issues.
