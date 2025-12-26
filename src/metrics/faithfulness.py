"""
Faithfulness Metric (Feature Masking).
"""
import numpy as np
from scipy.stats import pearsonr
from typing import Any, Dict, Optional, Union, List
from .base import BaseMetric

class FaithfulnessMetric(BaseMetric):
    """
    Measures faithfulness by masking important features and observing prediction change.
    
    Metrics:
    - prediction_gap: |pred(x) - pred(x_masked)| for top-k features.
    - correlation: Pearson corr betweeen feature importance and prediction drop when masking single features.
    """

    def __init__(self, n_samples: int = 100, baseline_mode: str = 'mean', top_k: int = 5):
        """
        Args:
            n_samples: Not used for this metric, kept for interface consistency.
            baseline_mode: 'mean' or 'zeros'.
            top_k: Number of features to mask for prediction gap.
        """
        super().__init__(name="Faithfulness")
        self.baseline_mode = baseline_mode
        self.top_k = top_k
        self.baseline_values = None

    def set_baseline(self, X_train: np.ndarray):
        """Precompute baseline values from training data."""
        if self.baseline_mode == 'mean':
            self.baseline_values = np.mean(X_train, axis=0)
        elif self.baseline_mode == 'zeros':
            self.baseline_values = np.zeros(X_train.shape[1])
        else:
            raise ValueError(f"Unknown baseline mode: {self.baseline_mode}")

    def compute(
        self,
        explanation: Any, # Feature weights
        model: Any = None,
        data: Optional[Union[np.ndarray, dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Compute Faithfulness metrics.
        
        Args:
            explanation: Feature importance vector or dict.
            model: Model with predict method.
            data: Original instance.
            
        Returns:
            Dict with 'faithfulness_gap', 'faithfulness_corr'.
        """
        if model is None or data is None:
            raise ValueError("Faithfulness metric requires 'model' and 'data'.")
            
        instance = np.array(data)
        if instance.ndim > 1:
            instance = instance[0]
            
        # Ensure baseline is set
        if self.baseline_values is None:
            # Fallback if not set: zeros
            self.baseline_values = np.zeros_like(instance)
            
        # Extract weights
        if isinstance(explanation, dict):
            weights = explanation['feature_importance']
            if weights.ndim > 1: weights = weights[0]
        else:
            weights = explanation
            
        # 1. Prediction Gap (Top-K)
        # Create masked instance
        # Identify top-k indices by absolute weight
        top_indices = np.argsort(np.abs(weights))[-self.top_k:]
        
        masked_instance = instance.copy()
        masked_instance[top_indices] = self.baseline_values[top_indices]
        
        # Get predictions
        # Handle predict_proba
        if hasattr(model, "predict_proba"):
            p_orig = model.predict_proba(instance.reshape(1, -1))[:, 1][0]
            p_masked = model.predict_proba(masked_instance.reshape(1, -1))[:, 1][0]
        else:
            p_orig = model.predict(instance.reshape(1, -1))[0]
            p_masked = model.predict(masked_instance.reshape(1, -1))[0]
            
        pred_gap = np.abs(p_orig - p_masked)
        
        # 2. Correlation (Single Feature Masking)
        # For each feature, mask it and measure drop. Correlation with weight magnitude.
        # Computing for all features might be expensive for images/text, but fine for tabular (Adult ~100 feats).
        # We'll limit to top 10 or all if small.
        
        drops = []
        magnitudes = []
        
        # Optimize: Batch prediction
        # Create batch of masked instances for all features
        n_features = len(instance)
        batch_masked = np.tile(instance, (n_features, 1))
        
        # Apply mask diagonal
        # This masks feature i in row i
        np.fill_diagonal(batch_masked, self.baseline_values)
        
        if hasattr(model, "predict_proba"):
            p_batch = model.predict_proba(batch_masked)[:, 1]
        else:
            p_batch = model.predict(batch_masked)
            
        drops = np.abs(p_orig - p_batch)
        magnitudes = np.abs(weights)
        
        # Pearson correlation (avoid NaN if constant)
        if np.std(drops) < 1e-9 or np.std(magnitudes) < 1e-9:
            corr = 0.0
        else:
            corr, _ = pearsonr(magnitudes, drops)
            
        return {
            "faithfulness_gap": float(pred_gap), # Higher is better (if features are truly important)
            "faithfulness_corr": float(corr), # Higher is better
            "faithfulness_score": float(corr) # Primary metric
        }
