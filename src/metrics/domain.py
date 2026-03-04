"""
Domain Alignment Metric Implementation.

This metric evaluates how well XAI explanations align with domain expert priors
(specifically labor economics theory for the Adult dataset).

It is distinct from "Causal" evaluation as it measures alignment with theoretical
importance rather than causal graphs.
"""

import numpy as np
from typing import List, Dict

class DomainAlignmentMetric:
    """
    Measures alignment between XAI explanations and domain expert priors.
    
    Currently configured for the Adult Income dataset based on labor economics theory.
    """
    
    # Tier 1: Strongly supported by labor economics as primary drivers of income
    CORE_FEATURES = {
        'age', 
        'education-num', 
        'education', # In case education-num is not used/named differently
        'hours-per-week', 
        'occupation', 
        'workclass'
    }
    
    # Tier 2: Important demographic/household determinants
    SECONDARY_FEATURES = {
        'marital-status', 
        'capital-gain', 
        'capital-loss', 
        'sex', 
        'race'
    }

    def __init__(self):
        """Initialize the metric."""
        pass
        
    def _get_base_feature(self, feature_name: str) -> str:
        """
        Extract base feature name from potentially one-hot encoded feature.
        Example: 'occupation_Sales' -> 'occupation'
        """
        # Handle standard OHE formats
        if '_' in feature_name:
            return feature_name.split('_')[0]
        return feature_name

    def compute(
        self, 
        feature_importance: np.ndarray, 
        feature_names: List[str], 
        k: int = 5
    ) -> Dict[str, float]:
        """
        Compute domain alignment metrics.

        Args:
            feature_importance: Array of feature importance weights.
            feature_names: List of feature names corresponding to weights.
            k: Number of top features to consider.

        Returns:
            Dictionary containing:
                - domain_precision_k: Fraction of Top-K features that are Domain Features.
                - domain_recall_k: Fraction of Core Domain Features found in Top-K.
        """
        if len(feature_importance) != len(feature_names):
            raise ValueError(f"Length mismatch: weights ({len(feature_importance)}) vs names ({len(feature_names)})")

        # Get absolute importance
        abs_weights = np.abs(feature_importance)
        
        # Get indices of top K features
        if k > len(abs_weights):
            k = len(abs_weights)
            
        top_k_indices = np.argsort(abs_weights)[-k:][::-1]
        top_k_features = [feature_names[i] for i in top_k_indices]
        
        # Map to base names
        top_k_base = set(self._get_base_feature(f) for f in top_k_features)
        
        # 1. Precision@K: How many of the Top-K are in Core or Secondary sets?
        # We check if the base name of a top-k feature is in our lists
        relevant_in_top_k = 0
        for f_base in top_k_base:
            if f_base in self.CORE_FEATURES or f_base in self.SECONDARY_FEATURES:
                relevant_in_top_k += 1
                
        precision = relevant_in_top_k / k if k > 0 else 0.0
        
        # 2. Recall@K (Core): How many Core features were found?
        # We only look for Core features for recall to be strict
        core_found = 0
        for core_f in self.CORE_FEATURES:
            if core_f in top_k_base:
                core_found += 1
                
        # Denominator is number of Core features
        recall = core_found / len(self.CORE_FEATURES)
        
        return {
            "domain_precision": precision,
            "domain_recall": recall
        }
