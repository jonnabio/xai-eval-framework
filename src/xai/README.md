# XAI Methods

This directory contains wrappers for explainable AI (XAI) methods used in the evaluation framework.

## Overview

The XAI wrappers provide standardized interfaces for generating explanations across different methods (LIME, SHAP, etc.) and models. Each wrapper ensures:

- **Consistent output format**: All methods return dictionaries with `feature_importance`, `top_features`, and `metadata`
- **Reproducibility**: Random seeds and configuration tracking
- **Performance monitoring**: Timing information for each explanation
- **Flexibility**: Support for custom prediction functions and configurations

## Available Methods

### LIME (Local Interpretable Model-agnostic Explanations)

**File:** `lime_tabular.py`

**Description:** Generates local explanations by training interpretable models on perturbed samples.

**Key Features:**
- Model-agnostic (works with any classifier)
- Local explanations (explains individual predictions)
- Feature importance can be positive (increases prediction) or negative (decreases prediction)

**Usage:**
```python
from xai.lime_tabular import LIMETabularWrapper

# Initialize wrapper
wrapper = LIMETabularWrapper(
    training_data=X_train,
    feature_names=feature_names,
    num_features=10,
    num_samples=5000,
    random_state=42
)

# Generate explanations
explanations = wrapper.generate_explanations(
    model=model,
    X_samples=X_test[:5]
)

# Access results
feature_importance = explanations['feature_importance']  # (5, n_features)
top_features = explanations['top_features']              # (5, 10)
metadata = explanations['metadata']                      # timing, config
```

**Configuration Parameters:**
- `num_features`: Number of top features to include (default: 10)
- `num_samples`: Perturbation samples for local model (default: 5000)
- `kernel_width`: Locality control (default: None = auto)
- `random_state`: Reproducibility seed (default: 42)

**Output Format:**
```python
{
    'feature_importance': np.ndarray,  # Shape: (n_instances, n_features)
                                        # Values: Positive/negative importance
    'top_features': np.ndarray,        # Shape: (n_instances, num_features)
                                        # Values: Feature indices sorted by |importance|
    'metadata': {
        'total_time_seconds': float,
        'avg_time_per_instance': float,
        'instance_times': List[float],
        'num_features_requested': int,
        'num_samples': int,
        'n_instances': int,
        'n_features': int,
        'kernel_width': Optional[float],
        'random_state': int
    }
}
```

**References:**
- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. KDD 2016.
- Documentation: https://lime-ml.readthedocs.io/

---

## Design Principles

### 1. Standardized Interface
All wrappers follow the same pattern:
- Initialization with training data and configuration
- `generate_explanations(model, X_samples)` for batch processing
- `explain_instance(model, instance)` for single instances
- `get_config()` for configuration retrieval

### 2. Model Agnosticism
Wrappers accept any model with a `predict_proba` method or custom prediction function.

### 3. Dense Output Format
All methods return dense feature importance arrays (shape: n_instances × n_features) for consistent downstream processing, even if the underlying method uses sparse representations.

### 4. Comprehensive Metadata
Each explanation includes timing information, configuration parameters, and method-specific details for reproducibility and analysis.
