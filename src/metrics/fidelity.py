"""
Fidelity (Faithfulness) Metric.
"""
from typing import Any, Dict, Optional, Union
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error
from .base import BaseMetric

class FidelityMetric(BaseMetric):
    """
    Measures how well the explanation model mimics the black-box model locally.
    Typically uses R^2 or MAE on a neighborhood of points.
    """

    def __init__(self, n_samples: int = 5000, kernel_width: float = 0.75):
        super().__init__(name="Fidelity")
        self.n_samples = n_samples
        self.kernel_width = kernel_width

    def _generate_neighborhood(self, data_point: np.ndarray) -> np.ndarray:
        """
        Generate random perturbations around the data point.
        Simplified Gaussian sampling for numeric data.
        """
        # Feature-wise standard deviation (assuming standard scaling approx)
        # In practice, LIME does this more carefully with training stats.
        # Here we use a simple additive noise to test fidelity logic.
        n_features = len(data_point)
        noise = np.random.normal(0, 1, size=(self.n_samples, n_features))
        return data_point + noise

    def compute(
        self,
        explanation: Any, # Expects feature weights vector
        model: Any = None,
        data: Optional[Union[np.ndarray, dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Compute Fidelity metrics.
        
        Args:
            explanation: Feature importance vector (np.ndarray).
            model: Black-box model with predict (or predict_proba).
            data: The original instance (shape (n_features,)).
        
        Returns:
            Dict with 'r2_score', 'mae'.
        """
        if model is None or data is None:
            raise ValueError("Fidelity metric requires 'model' and 'data'.")
            
        instance = np.array(data)
        if instance.ndim > 1:
            instance = instance[0]

        # Extract weights
        if isinstance(explanation, dict):
            weights = explanation['feature_importance']
            if weights.ndim > 1: weights = weights[0]
            bias = explanation.get('expected_value', 0.0) # OR base value
            # Note: LIME wrappers might put intercept elsewhere.
            # SHAP base value is the intercept.
        else:
            weights = explanation
            bias = 0.0 # Assumption if not provided

        # 1. Generate Neighborhood
        # Metric definition: We want to see if Linear Model (Weights) approximates Black Box on neighborhood.
        # Problem: 'Data' is just one point. We need the neighborhood used by the explainer OR generate new one.
        # Generating new one might differ from what explainer saw.
        # ADAPTATION: We will use a standard Gaussian neighborhood to evaluate the *generalization* of the linear approximation.
        
        neighborhood = self._generate_neighborhood(instance)
        
        # 2. Get Black Box Predictions (Target)
        # Use predict_proba for classifiers (continuous score) if available
        if hasattr(model, "predict_proba"):
            # Assume binary, take positive class
            bb_preds = model.predict_proba(neighborhood)
            if bb_preds.ndim > 1 and bb_preds.shape[1] > 1:
                bb_preds = bb_preds[:, 1]
        else:
            bb_preds = model.predict(neighborhood)
            
        # 3. Get Explanation Predictions (Approximation)
        # Linear approximation: y = w*x + b
        # SHAP/LIME usually explain difference from base/mean.
        # SHAP: pred = base + sum(w * x) (BUT x is usually feature contribution, not raw value)
        # This is tricky. 
        # FOR SHAP: weights are attribution to *value*.
        # FOR LIME: weights are coeff for *features*.
        
        # SIMPLIFICATION for MVP:
        # We assume weights are linear coefficients on the normalized data.
        # expl_preds = neighborhood @ weights + bias
        # This might be inaccurate for SHAP if not careful.
        # Alternative: Ask explainer to predict? No standard API.
        
        # Let's use the standard definition for LIME-like fidelity:
        # We need to know if the weights provided actually work as a linear model.
        expl_preds = np.dot(neighborhood, weights) + bias
        
        # 4. Compute Metrics
        r2 = r2_score(bb_preds, expl_preds)
        mae = mean_absolute_error(bb_preds, expl_preds)
        
        return {
            "r2_score": float(r2),
            "mae": float(mae),
            "n_samples": self.n_samples
        }
