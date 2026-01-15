"""
Anchors Wrapper (Alibi) for Tabular Data.

This module provides a wrapper for the AnchorTabular explainer from alibi.
It adapts the rule-based explanation to the ExplainerWrapper interface by
treating features present in the anchor as having high importance.
"""
import logging
import numpy as np
from typing import Dict, Any, Optional, List
import time

from .base import ExplainerWrapper

logger = logging.getLogger(__name__)

class AnchorsTabularWrapper(ExplainerWrapper):
    """
    Wrapper for Alibi AnchorTabular.
    
    Anchors provides "sufficient" conditions (rules) for a prediction.
    We map "importance" as 1.0 if a feature is part of the anchor rule, 0.0 otherwise.
    """
    
    def __init__(self, training_data: np.ndarray, feature_names: List[str], **kwargs):
        super().__init__(training_data, feature_names, **kwargs)
        self.explainer = None
        
    def _lazy_init(self, predict_fn):
        """Initialize Alibi explainer lazily to verify dependencies/performance."""
        if self.explainer is not None:
            return

        try:
            from alibi.explainers import AnchorTabular
        except ImportError:
            raise ImportError("alibi is required for Anchors. Install with `pip install alibi`.")
            
        logger.info("Initializing AnchorTabular explainer...")
        # AnchorTabular expects a predict function
        self.explainer = AnchorTabular(predict_fn, self.feature_names)
        
        # Fit on training data (discretizer)
        # Alibi expects regular numpy array
        self.explainer.fit(self.training_data)
        logger.info("AnchorTabular initialized.")

    def generate_explanations(
        self, 
        model: Any, 
        X_samples: np.ndarray, 
        predict_fn: Optional[Any] = None
    ) -> Dict[str, np.ndarray]:
        """
        Generate Anchor explanations.
        
        Args:
            model: The black-box model.
            X_samples: Input samples to explain.
            predict_fn: Function returning prediction.
            
        Returns:
            Dictionary with 'feature_importance' (binary mask of anchor features).
        """
        if predict_fn is None:
            if hasattr(model, "predict"):
                predict_fn = model.predict
            else:
                raise ValueError("predict_fn or model.predict must be provided.")
                
        self._lazy_init(predict_fn)
        
        n_samples = X_samples.shape[0]
        n_features = X_samples.shape[1]
        
        feature_importance = np.zeros((n_samples, n_features))
        top_features_list = []
        
        start_time = time.time()
        
        # Anchors processes one by one
        for i in range(n_samples):
            try:
                # threshold=0.95 is standard for high precision
                explanation = self.explainer.explain(X_samples[i], threshold=0.95)
                
                # explanation.data['raw']['feature'] contains indices of features in the anchor
                # Note: Alibi might return indices relevant to discretised buckets, but usually maps back.
                # In standard tabular, it gives feature indices.
                
                anchor_features = explanation.data['raw']['feature']
                for idx in anchor_features:
                    if idx < n_features:
                        feature_importance[i, idx] = 1.0
                        
                top_features_list.append(anchor_features)
                
            except Exception as e:
                logger.warning(f"Failed to generate Anchor for sample {i}: {e}")
                
        duration = time.time() - start_time
        
        # Pad top_features to make rectangular array (optional/not strictly required by base but good)
        max_len = max(len(t) for t in top_features_list) if top_features_list else 0
        top_features = np.full((n_samples, max_len), -1)
        for i, t in enumerate(top_features_list):
            top_features[i, :len(t)] = t

        return {
            'feature_importance': feature_importance,
            'top_features': top_features,
            'metadata': {
                'method': 'Anchors',
                'duration': duration,
                'count': n_samples
            }
        }

    def get_config(self) -> Dict[str, Any]:
        return {
            "method": "Anchors",
            "kwargs": self.kwargs
        }
