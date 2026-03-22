# EXP2 Grid Completion Instructions

This document provides step-by-step instructions to reach 100% completion (300/300) of the EXP2 Scaled robustness grid. These steps are designed to be run on a Linux workstation.

## 1. Environment Setup
Clone the repository and install dependencies:
```bash
git clone <repository_url>
cd xai-eval-framework
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-frozen.txt
```

## 2. Restore Recovered Artifacts (11 runs)
The following artifacts exist in recovery folders and should be moved to the target results directory to fill gaps without re-running:

```bash
# Restoration script
ROOT="experiments/exp2_scaled/results"
REC="experiments/recovery/phase1/results"
REC_P1="experiments/exp_recov_p1"

# SVM SHAP Recovery
mkdir -p "$ROOT/svm_shap/seed_123/n_50" && cp "$REC/svm_shap/seed_123/n_50/results.json" "$ROOT/svm_shap/seed_123/n_50/"
mkdir -p "$ROOT/svm_shap/seed_123/n_100" && cp "$REC/svm_shap/seed_123/n_100/results.json" "$ROOT/svm_shap/seed_123/n_100/"
mkdir -p "$ROOT/svm_shap/seed_123/n_200" && cp "$REC/svm_shap/seed_123/n_200/results.json" "$ROOT/svm_shap/seed_123/n_200/"
mkdir -p "$ROOT/svm_shap/seed_42/n_50" && cp "$REC/svm_shap/seed_42/n_50/results.json" "$ROOT/svm_shap/seed_42/n_50/"
mkdir -p "$ROOT/svm_shap/seed_42/n_100" && cp "$REC/svm_shap/seed_42/n_100/results.json" "$ROOT/svm_shap/seed_42/n_100/"

# MLP SHAP Recovery (from exp_recov_p1)
mkdir -p "$ROOT/mlp_shap/seed_42/n_50" && cp "$REC_P1/mlp_shap/seed_42/n_50/results.json" "$ROOT/mlp_shap/seed_42/n_50/"
mkdir -p "$ROOT/mlp_shap/seed_42/n_100" && cp "$REC_P1/mlp_shap/seed_42/n_100/results.json" "$ROOT/mlp_shap/seed_42/n_100/"
mkdir -p "$ROOT/mlp_shap/seed_456/n_100" && cp "$REC_P1/mlp_shap/seed_456/n_100/results.json" "$ROOT/mlp_shap/seed_456/n_100/"
mkdir -p "$ROOT/mlp_shap/seed_456/n_200" && cp "$REC_P1/mlp_shap/seed_456/n_200/results.json" "$ROOT/mlp_shap/seed_456/n_200/"
mkdir -p "$ROOT/mlp_shap/seed_789/n_100" && cp "$REC_P1/mlp_shap/seed_789/n_100/results.json" "$ROOT/mlp_shap/seed_789/n_100/"
mkdir -p "$ROOT/mlp_shap/seed_999/n_50" && cp "$REC_P1/mlp_shap/seed_999/n_50/results.json" "$ROOT/mlp_shap/seed_999/n_50/"
```

## 3. Execute Remaining Gaps (56 runs)
Execute the following commands to complete the grid. These are grouped by model for performance monitoring.

### 3.1 SVM Gaps (High Multi-core Overhead)
```bash
python -m src.experiment.runner --model svm --explainer anchors --seed 123 --sample-size 200 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer anchors --seed 456 --sample-size 200 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer anchors --seed 789 --sample-size 200 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer anchors --seed 999 --sample-size 200 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer dice --seed 42 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer dice --seed 42 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer dice --seed 456 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer dice --seed 456 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer dice --seed 789 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer dice --seed 789 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer dice --seed 999 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer dice --seed 999 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model svm --explainer dice --seed 999 --sample-size 200 --cohort exp2_scaled
```

### 3.2 RF Gaps
```bash
python -m src.experiment.runner --model rf --explainer anchors --seed 42 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model rf --explainer anchors --seed 789 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model rf --explainer anchors --seed 789 --sample-size 200 --cohort exp2_scaled
python -m src.experiment.runner --model rf --explainer anchors --seed 999 --sample-size 200 --cohort exp2_scaled
python -m src.experiment.runner --model rf --explainer dice --seed 123 --sample-size 200 --cohort exp2_scaled
python -m src.experiment.runner --model rf --explainer dice --seed 456 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model rf --explainer dice --seed 456 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model rf --explainer dice --seed 789 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model rf --explainer dice --seed 789 --sample-size 200 --cohort exp2_scaled
python -m src.experiment.runner --model rf --explainer dice --seed 999 --sample-size 200 --cohort exp2_scaled
```

### 3.3 XGB Gaps
```bash
python -m src.experiment.runner --model xgb --explainer anchors --seed 123 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model xgb --explainer anchors --seed 123 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model xgb --explainer anchors --seed 456 --sample-size 200 --cohort exp2_scaled
python -m src.experiment.runner --model xgb --explainer anchors --seed 999 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model xgb --explainer anchors --seed 999 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model xgb --explainer dice --seed 42 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model xgb --explainer dice --seed 456 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model xgb --explainer dice --seed 789 --sample-size 50 --cohort exp2_scaled
```

### 3.4 MLP Gaps
```bash
python -m src.experiment.runner --model mlp --explainer anchors --seed 42 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model mlp --explainer anchors --seed 42 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model mlp --explainer anchors --seed 456 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model mlp --explainer anchors --seed 456 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model mlp --explainer anchors --seed 789 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model mlp --explainer anchors --seed 789 --sample-size 200 --cohort exp2_scaled
python -m src.experiment.runner --model mlp --explainer dice --seed 42 --sample-size 50 --cohort exp2_scaled
python -m src.experiment.runner --model mlp --explainer dice --seed 42 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model mlp --explainer dice --seed 123 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model mlp --explainer dice --seed 789 --sample-size 100 --cohort exp2_scaled
```

### 3.5 LogReg Gaps
```bash
python -m src.experiment.runner --model logreg --explainer dice --seed 789 --sample-size 100 --cohort exp2_scaled
python -m src.experiment.runner --model logreg --explainer dice --seed 999 --sample-size 100 --cohort exp2_scaled
```

## 4. Final Aggregation
After completing the runs, update the paper figures and tables:
```bash
python scripts/generate_paper_a_figures.py
```
