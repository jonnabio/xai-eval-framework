# XAI Evaluation Metrics

This module (`src/metrics`) implements standardized metrics to evaluate the quality of explanations (LIME, SHAP).

## Overview

We evaluate explanations across four dimensions defined in **ADR-009**:

1.  **Fidelity** (Faithfulness): How well the explanation mimics the model?
2.  **Stability** (Robustness): Does the explanation hold up to noise?
3.  **Sparsity** (Complexity): How concise is the explanation?
4.  **Cost** (Efficiency): How fast is it?

## usage

### Basic Usage

```python
from metrics import FidelityMetric, StabilityMetric, SparsityMetric, CostMetric

# 1. Sparsity
sparsity = SparsityMetric(threshold=0.01)
res = sparsity.compute(explanation_weights)
print(f"Non-zero features: {res['nonzero_count']}")

# 2. Fidelity
fidelity = FidelityMetric(n_samples=5000)
res = fidelity.compute(weights, model=model, data=instance)
print(f"R2 Score: {res['r2_score']}")

# 3. Cost
cost = CostMetric()
# Compute from metadata
res = cost.compute(result_dict) 
# Or measure function
result, time_meta = cost.measure(func, args...)

# 4. Stability
stability = StabilityMetric(n_iterations=10)
res = stability.compute(
    None, 
    model=model, 
    data=instance, 
    explainer_func=my_explainer_wrapper
)
print(f"Stability: {res['cosine_similarity_mean']}")
```

## Metrics Details

### Fidelity
- **Metric**: $R^2$ score of the explanation weights applied to a local neighborhood vs black-box predictions.
- **Goal**: > 0.9.

### Stability
- **Metric**: Average Cosine Similarity between explanations of perturbed inputs.
- **Goal**: > 0.9.

### Sparsity
- **Metric**: Percentage of non-zero weights (above threshold).
- **Goal**: Minimized (while maintaining Fidelity).

### Cost
- **Metric**: Wall-clock time (ms).
