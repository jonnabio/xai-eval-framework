# Experiments Catalog

> XAI Evaluation Framework - Complete Experiment Registry
>
> Last Updated: 2026-01-15

## Overview

This document provides a comprehensive catalog of all experiments conducted within the XAI Evaluation Framework. The framework evaluates explainability methods (LIME, SHAP, Anchors, DiCE) across multiple machine learning models using the UCI Adult Income dataset.

**Total Experiments Executed**: 66

---

## Experiment Summary by Category

| Category | Count | Description |
|----------|-------|-------------|
| Core Experiments | 4 | Primary model × XAI combinations |
| Reproducibility Runs | 37 | Multi-seed validation (seeds 42-51) |
| LIME Hyperparameter Tuning | 24 | Grid search over kernel width, samples, feature selection |
| Phase H (Expansion) | 1 | New model/XAI combinations (in progress) |

---

## EXP1: Adult Dataset Experiments

### Dataset Specification

| Property | Value |
|----------|-------|
| Name | UCI Adult Income |
| Source | OpenML (ID: 1590) |
| Samples | 48,842 |
| Features | 14 (6 numeric, 8 categorical) |
| Target | Income >50K (binary) |
| Train/Test Split | 80/20 (stratified) |
| Preprocessing | StandardScaler (numeric), OneHotEncoder (categorical) |

### Models

| Model | Type | Configuration | Test Accuracy |
|-------|------|---------------|---------------|
| **RF** | Random Forest | 100 trees, max_depth=None | ~0.85 |
| **XGB** | XGBoost | 100 rounds, max_depth=6 | ~0.87 |
| **SVM** | Support Vector Machine | RBF kernel, probability=True | Pending |
| **MLP** | Multi-Layer Perceptron | (100,) hidden layers | Pending |
| **LogReg** | Logistic Regression | L2 regularization | Pending |

### XAI Methods

| Method | Library | Configuration |
|--------|---------|---------------|
| **LIME** | lime | 1000 samples, 10 features, exponential kernel |
| **SHAP** | shap | TreeExplainer, 100 background samples |
| **Anchors** | alibi | threshold=0.95 |
| **DiCE** | dice-ml | 5 counterfactuals |

---

## Core Experiments (EXP1)

### Results Summary

| Experiment | Model | XAI | Instances | Fidelity | Stability | Sparsity | Cost (ms) | Duration |
|------------|-------|-----|-----------|----------|-----------|----------|-----------|----------|
| exp1_rf_lime | RF | LIME | 200 | 0.1075 | 0.0861 | 0.0926 | 42.86 | 102.4s |
| exp1_rf_shap | RF | SHAP | 200 | 0.5788 | 0.9464 | 0.4573 | 0.19 | 9.4s |
| exp1_xgb_lime | XGB | LIME | 200 | 0.5083 | 0.1210 | 0.0926 | 19.19 | 42.8s |
| exp1_xgb_shap | XGB | SHAP | 200 | 0.3463 | 0.4516 | 0.2286 | 0.02 | 0.5s |

### Key Findings

1. **Stability**: SHAP significantly outperforms LIME (0.95 vs 0.09 for RF)
2. **Efficiency**: SHAP is 200x faster than LIME with tree-based models
3. **Fidelity**: RF+SHAP achieves highest fidelity (0.58)
4. **Sparsity**: LIME produces sparser explanations (fewer non-zero features)

### Result Locations

```
experiments/exp1_adult/results/
├── rf_lime/
│   ├── results.json
│   └── metrics.csv
├── rf_shap/
│   ├── results.json
│   └── metrics.csv
├── xgb_lime/
│   ├── results.json
│   └── metrics.csv
└── xgb_shap/
    ├── results.json
    └── metrics.csv
```

---

## Reproducibility Study

Multi-seed experiments to validate result consistency (CV < 0.10).

### Configuration

- **Seeds**: 42, 43, 44, 45, 46, 47, 48, 49, 51 (9 seeds per experiment)
- **Experiments**: 4 core combinations × 9 seeds = 36 runs

### Result Locations

```
experiments/exp1_adult/reproducibility/
├── exp1_adult_rf_lime/
│   ├── seed_42/
│   ├── seed_43/
│   └── ...
├── exp1_adult_rf_shap/
├── exp1_adult_xgb_lime/
└── exp1_adult_xgb_shap/
```

---

## LIME Hyperparameter Tuning

Grid search to optimize LIME configuration.

### Parameter Grid

| Parameter | Values |
|-----------|--------|
| kernel_width | 0.25, 0.5, 0.75, 1.0, 2.0, auto |
| num_samples | 1000, 5000 |
| feature_selection | auto, none |

**Total Configurations**: 6 × 2 × 2 = 24

### Result Locations

```
experiments/exp1_adult/results/tuning/
├── exp1_lime_k0.25_n1000_fsauto/
├── exp1_lime_k0.25_n1000_fsnone/
├── exp1_lime_k0.25_n5000_fsauto/
├── exp1_lime_k0.25_n5000_fsnone/
├── exp1_lime_k0.5_n1000_fsauto/
├── ...
└── exp1_lime_kauto_n5000_fsnone/
```

---

## Phase H: Breadth Expansion (In Progress)

### Target Matrix

Expand from 2×2 to 5×4 experiment matrix.

|           | LIME | SHAP | Anchors | DiCE |
|-----------|------|------|---------|------|
| **RF**    | ✅   | ✅   | ⏳      | ⏳   |
| **XGB**   | ✅   | ✅   | ⏳      | ⏳   |
| **SVM**   | ⏳   | ⏳   | ⚠️      | ⏳   |
| **MLP**   | ⏳   | ⏳   | ⏳      | ⏳   |
| **LogReg**| ⏳   | ⏳   | ⏳      | ⏳   |

Legend: ✅ Complete | ⏳ Planned | ⚠️ Test run (0 instances)

### Completed Test Runs

| Experiment | Status | Notes |
|------------|--------|-------|
| test_svm_anchors | ⚠️ Partial | Executed but 0 instances evaluated (2026-01-13) |

---

## Metrics Reference

### Classical Metrics

| Metric | Range | Description | Higher is Better? |
|--------|-------|-------------|-------------------|
| **Fidelity** | [0, 1] | R² correlation between explanation weights and model sensitivity | Yes |
| **Stability** | [0, 1] | Cosine similarity of explanations under input perturbation | Yes |
| **Sparsity** | [0, 1] | Fraction of non-zero feature weights | Depends |
| **Cost** | ms | Explanation generation time | No |

### Advanced Metrics

| Metric | Description |
|--------|-------------|
| **Domain Alignment** | Overlap with expert-defined important features |
| **Counterfactual Sensitivity** | Explanation change when prediction flips |

### LLM-Based Evaluation

- **Provider**: OpenAI GPT-4 / Gemini Pro
- **Samples Evaluated**: 80 (stratified)
- **Human Agreement (κ)**: 0.65

---

## Execution Commands

### Run Single Experiment

```bash
python -m src.experiment.runner --config configs/experiments/exp1_adult_rf_shap.yaml
```

### Run Batch Experiments

```bash
python -m src.experiment.batch_runner --config-dir configs/experiments/ --output-dir outputs/
```

### Run Reproducibility Study

```bash
python scripts/run_reproducibility.py --experiment exp1_adult_rf_shap --seeds 42 43 44 45 46
```

---

## File Structure

```
experiments/
└── exp1_adult/
    ├── configs/           # Experiment YAML configurations
    ├── models/            # Trained model artifacts (.pkl)
    │   ├── rf_model.pkl
    │   └── xgb_model.pkl
    ├── results/           # Core experiment outputs
    │   ├── rf_lime/
    │   ├── rf_shap/
    │   ├── xgb_lime/
    │   ├── xgb_shap/
    │   ├── test_svm_anchors/
    │   └── tuning/
    ├── reproducibility/   # Multi-seed validation runs
    ├── llm_eval/          # LLM evaluation results
    ├── human_eval/        # Human annotation data
    └── reproducibility_package/  # Zenodo archive materials
```

---

## Related Documentation

- [Experiment Observations](../../experiments/exp1_adult/EXPERIMENT_OBSERVATIONS.md)
- [Evaluation Report](../../experiments/exp1_adult/EVALUATION_REPORT.md)
- [Reproducibility Guide](../../experiments/exp1_adult/reproducibility_package/REPRODUCIBILITY_GUIDE.md)
- [Phase H Checklist](../planning/task_checklist_phase_h.md)
- [Publication Strategy](../planning/publication_strategy.md)

---

## Appendix: Experiment IDs

### Core Experiments

| ID | Config File | Output Directory |
|----|-------------|------------------|
| EXP1-RF-LIME | `exp1_adult_rf_lime.yaml` | `results/rf_lime/` |
| EXP1-RF-SHAP | `exp1_adult_rf_shap.yaml` | `results/rf_shap/` |
| EXP1-XGB-LIME | `exp1_adult_xgb_lime.yaml` | `results/xgb_lime/` |
| EXP1-XGB-SHAP | `exp1_adult_xgb_shap.yaml` | `results/xgb_shap/` |

### Tuning Experiments

| ID Pattern | Parameters |
|------------|------------|
| `exp1_lime_k{kw}_n{ns}_fs{fs}` | kw=kernel_width, ns=num_samples, fs=feature_selection |

---

*Document generated from xai-eval-framework repository analysis.*
