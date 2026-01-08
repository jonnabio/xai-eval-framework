"""
Base XAI Explainer Wrapper.

This module defines the abstract base class for all XAI explainers (SHAP, LIME, etc.),
enforcing a consistent interface for the evaluation framework.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import numpy as np

class ExplainerWrapper(ABC):
    """
    Abstract Base Class for XAI explainers.
    
    All specific implementations (SHAP, LIME, etc.) must inherit from this
    and implement the core generation methods.
    """
    
    def __init__(
        self, 
        training_data: np.ndarray, 
        feature_names: List[str], 
        **kwargs
    ):
        """
        Initialize the explainer.
        
        Args:
            training_data: Background/Training data for initialization.
            feature_names: List of feature names.
            **kwargs: Explainer-specific configuration.
        """
        self.training_data = training_data
        self.feature_names = feature_names
        self.kwargs = kwargs

    @abstractmethod
    def generate_explanations(
        self, 
        model: Any, 
        X_samples: np.ndarray,
        predict_fn: Optional[Any] = None
    ) -> Dict[str, np.ndarray]:
        """
        Generate explanations for a batch of samples.
        
        Args:
            model: The black-box model to explain.
            X_samples: Input samples (N, feature_count).
            predict_fn: Optional custom prediction function.
            
        Returns:
            Dictionary containing:
            - 'feature_importance': (N, feature_count) array of attribution scores.
            - 'top_features': (N, k) array of feature indices.
            - 'metadata': Dictionary of timing and config info.
        """
        pass

    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """Return the configuration used for this explainer."""
        pass    
    
    def explain_instance(
        self, 
        model: Any, 
        instance: np.ndarray,
        predict_fn: Optional[Any] = None
    ) -> np.ndarray:
        """
        Explain a single instance.
        
        Default implementation delegates to generate_explanations with batch size 1.
        Override if the specific explainer facilitates single-instance optimization.
        """
        # Ensure 2D (1, F)
        if instance.ndim == 1:
            X_batch = instance.reshape(1, -1)
        else:
            X_batch = instance
            
        result = self.generate_explanations(model, X_batch, predict_fn=predict_fn)
        return result['feature_importance'][0]
