# Sample Experiment Data

This directory contains sample experiment result files for testing the XAI Evaluation API without running full experiments.

## Purpose

- **Development**: Test API endpoints during development
- **Integration**: Verify data_loader → transformer → endpoint workflow
- **Demo**: Demonstrate API functionality
- **CI/CD**: Use in automated tests

## Files

### rf_lime_metrics.json
- **Model**: Random Forest (200 trees)
- **Method**: LIME
- **Dataset**: AdultIncome
- **Accuracy**: 85.23%
- **Highlights**: Good clarity and usefulness scores

### xgb_shap_metrics.json
- **Model**: XGBoost (100 estimators)
- **Method**: SHAP
- **Dataset**: AdultIncome
- **Accuracy**: 87.45%
- **Highlights**: Highest overall metrics, excellent fidelity

### rf_shap_metrics.json
- **Model**: Random Forest (200 trees)
- **Method**: SHAP
- **Dataset**: AdultIncome
- **Accuracy**: 85.67%
- **Highlights**: Strong trustworthiness, good stability

### xgb_lime_metrics.json
- **Model**: XGBoost (100 estimators)
- **Method**: LIME
- **Dataset**: AdultIncome
- **Accuracy**: 87.12%
- **Highlights**: Fast processing, good clarity

### low_performance_example.json
- **Model**: Decision Tree (depth 5)
- **Method**: LIME
- **Dataset**: AdultIncome
- **Accuracy**: 72.34%
- **Highlights**: Lower metrics for testing edge cases

## File Structure

Each JSON file uses the standard experiment result format:

```json
{
  "model_name": "string",
  "model_type": "string",
  "dataset": "string",
  "xai_method": "string",
  "accuracy": 0.0,
  "metrics": { ... },
  "llm_evaluation": { ... },
  "config": { ... },
  "metadata": { ... }
}
```

## validation

To ensure these files remain compatible with the API:

```bash
python scripts/validate_sample_data.py
```
