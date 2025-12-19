"""
Stability (Robustness) Metric.
"""
from typing import Any, Dict, Optional, Union, Callable
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import jaccard
from .base import BaseMetric
import copy

class StabilityMetric(BaseMetric):
    """
    Measures how much the explanation changes when the input/sampling is perturbed.
    High stability = explanation is robust to noise.
    """

    def __init__(self, n_iterations: int = 10, perturbation_std: float = 0.01):
        super().__init__(name="Stability")
        self.n_iterations = n_iterations
        self.perturbation_std = perturbation_std

    def compute(
        self,
        explanation: Any, # The baseline explanation
        model: Any = None,
        data: Optional[Union[np.ndarray, dict]] = None, # Original data
        explainer_func: Optional[Callable] = None, # Function to generate explanation
        **kwargs
    ) -> Dict[str, Any]:
        """
        Compute Stability metrics.
        
        Args:
            explanation: Initial result (ignored, we regenerate).
            model: The black-box model.
            data: The original instance.
            explainer_func: Callable(model, data) -> result dict.
        
        Returns:
            Dict with 'cosine_similarity_mean', 'cosine_similarity_std'.
        """
        if explainer_func is None or model is None or data is None:
            raise ValueError("Stability metric requires 'explainer_func', 'model', and 'data'.")

        instance = np.array(data)
        if instance.ndim > 1: instance = instance[0]

        # Generate K explanations for perturbed inputs
        explanations = []
        
        for i in range(self.n_iterations):
            # Perturb input
            noise = np.random.normal(0, self.perturbation_std, size=instance.shape)
            perturbed_instance = instance + noise
            
            # Generate explanation
            # Assume func returns dict with 'feature_importance'
            res = explainer_func(model, perturbed_instance.reshape(1, -1))
            
            vec = res['feature_importance']
            
            # Ensure numpy
            if not isinstance(vec, np.ndarray):
                vec = np.array(vec)
                
            if vec.ndim > 1: vec = vec[0]
            explanations.append(vec)
            
        explanations = np.array(explanations)
        
        # Calculate pairwise cosine similarity
        # (N, D)
        sim_matrix = cosine_similarity(explanations)
        
        # Get upper triangle (excluding diagonal which is 1.0)
        tri_indices = np.triu_indices(self.n_iterations, k=1)
        similarities = sim_matrix[tri_indices]
        
        return {
            "cosine_similarity_mean": float(np.mean(similarities)),
            "cosine_similarity_std": float(np.std(similarities)),
            "n_iterations": self.n_iterations
        }
