"""
Sparsity (Complexity) Metric.
"""
from typing import Any, Dict, Optional, Union
import numpy as np
from .base import BaseMetric

class SparsityMetric(BaseMetric):
    """
    Measures the sparsity/complexity of an explanation.
    """

    def __init__(self, threshold: float = 1e-4):
        """
        Args:
            threshold: Minimum absolute importance to consider a feature "active".
        """
        super().__init__(name="Sparsity")
        self.threshold = threshold

    def compute(
        self,
        explanation: Any,
        model: Any = None,
        data: Optional[Union[np.ndarray, dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Compute sparsity metrics.

        Args:
            explanation: Dict with 'feature_importance' (dense array) or direct array.
        
        Returns:
            Dict containing:
            - nonzero_count: Number of features > threshold.
            - nonzero_percentage: Ratio of active features.
            - gini_index: Inequality of importance distribution.
        """
        # Extract importance vector
        if isinstance(explanation, dict) and 'feature_importance' in explanation:
            # Handle batch or single
            imp = explanation['feature_importance']
            if imp.ndim > 1:
                # Take first if batch (or handle average? usually instance level)
                # We assume instance level for metrics usually
                imp = imp[0]
        elif isinstance(explanation, np.ndarray):
             imp = explanation
             if imp.ndim > 1:
                 imp = imp[0]
        else:
            raise ValueError(f"Unsupported explanation format: {type(explanation)}")

        # Absolute importance
        abs_imp = np.abs(imp)
        total_features = len(abs_imp)
        
        # 1. Non-zero count (Sparsity)
        active_mask = abs_imp > self.threshold
        nonzero_count = np.sum(active_mask)
        nonzero_pct = nonzero_count / total_features if total_features > 0 else 0.0

        # 2. Gini Index (Concentration)
        # Sort values
        sorted_imp = np.sort(abs_imp)
        # Cumulative sum
        cum_imp = np.cumsum(sorted_imp)
        # Gini formula
        n = total_features
        if np.sum(abs_imp) == 0:
            gini = 0.0
        else:
            gini = (2 * np.sum((np.arange(1, n + 1) * sorted_imp))) / (n * np.sum(sorted_imp)) - (n + 1) / n
        
        return {
            "nonzero_count": int(nonzero_count),
            "nonzero_percentage": float(nonzero_pct),
            "gini_index": float(gini),
            "total_features": int(total_features)
        }
