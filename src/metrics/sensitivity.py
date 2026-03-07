"""
Counterfactual Sensitivity Metric.

Measures the alignment between feature importance explanations (SHAP/LIME)
and counterfactual explanations (DiCE).
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional, Any, Union

from .base import BaseMetric

class CounterfactualSensitivityMetric(BaseMetric):
    """
    Computes sensitivity of explanation to counterfactual changes.
    
    Definition:
    Recall of Top-K explanation features with respect to the set of features 
    modified in the generated counterfactuals.
    """
    
    def __init__(self, k: int = 5):
        """
        Args:
            k: Top-K features to check for overlap.
        """
        super().__init__(name="Sensitivity")
        self.k = k
        
    def compute(
        self, 
        explanation: Any, 
        model: Any = None,
        data: Optional[Union[pd.DataFrame, np.ndarray, dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Compute agreement between importance and CF changes.
        
        Args:
            explanation: Feature importance weights (np.ndarray).
            model: (Unused here, kept for interface).
            data: The original instance (pd.DataFrame).
            **kwargs: Must contain 'cf_files' (DataFrame) and 'feature_names' (List[str]).
            
        Returns:
            Dictionary with 'cf_sensitivity', 'cf_sensitivity_recall', etc.
        """
        # Extract required args
        feature_names = kwargs.get('feature_names')
        cf_files = kwargs.get('cf_files')
        
        if feature_names is None:
            raise ValueError("CounterfactualSensitivityMetric requiring 'feature_names' in kwargs.")
        if cf_files is None:
            # If no CFs provided, return 0 (or could raise, but safe default preferred)
             return {
                'cf_sensitivity': 0.0,
                'cf_sensitivity_recall': 0.0, 
                'cf_sensitivity_precision': 0.0
            }
            
        original_instance = data
        if not isinstance(original_instance, pd.DataFrame):
             # Try to wrap if dict? But this specific metric relies heavily on pandas structure for CF comparison
             # If passed as numpy, we might fail unless we reconstruct DF with feature_names
             if isinstance(original_instance, (dict, list, np.ndarray)):
                 original_instance = pd.DataFrame([original_instance], columns=feature_names)
             else:
                 raise ValueError("Sensitivity metric requires 'data' as DataFrame or convertible to DF.")

        feature_importance = explanation
        if isinstance(feature_importance, dict):
            feature_importance = feature_importance['feature_importance']
        
        if feature_importance.ndim > 1:
            feature_importance = feature_importance[0]

        if cf_files.empty:
            return {
                'cf_sensitivity': 0.0,
                'cf_sensitivity_recall': 0.0, 
                'cf_sensitivity_precision': 0.0
            }

        # 1. Identify Modifed Features in CFs
        # Iterate cols and check if value changed
        # We need to ensure columns match. DiCE CFs usually include target, need to drop it.
        
        # Common cols
        common_cols = [c for c in original_instance.columns if c in cf_files.columns]
        
        modified_features = set()
        
        # original array
        orig_vals = original_instance[common_cols].iloc[0].values
        
        # Check each CF
        for _, cf_row in cf_files.iterrows():
            cf_vals = cf_row[common_cols].values
            
            # Simple inequality mask
            for i, col in enumerate(common_cols):
                v1 = orig_vals[i]
                v2 = cf_vals[i]
                
                is_diff = False
                try:
                    if isinstance(v1, (int, float, np.number)) and isinstance(v2, (int, float, np.number)):
                        if not np.isclose(v1, v2, atol=1e-5):
                            is_diff = True
                    else:
                        if v1 != v2:
                            is_diff = True
                except:
                    # Fallback
                    if str(v1) != str(v2):
                        is_diff = True
                        
                if is_diff:
                    modified_features.add(col)
                    
        if not modified_features:
            return {
                'cf_sensitivity': 0.0,
                'cf_sensitivity_recall': 0.0, 
                'cf_sensitivity_precision': 0.0
            }

        # 2. Identify Top-K Explanation Features
        abs_weights = np.abs(feature_importance)
        top_k_indices = np.argsort(abs_weights)[-self.k:][::-1]
        top_k_features = [feature_names[i] for i in top_k_indices]
        
        # 3. Compute Overlap
        def get_base_feature(f):
            if '_' in f:
                return f.split('_')[0]
            return f
            
        top_k_base = set(get_base_feature(f) for f in top_k_features)
        
        # Intersection
        intersection = top_k_base.intersection(modified_features)
        
        recall = len(intersection) / len(modified_features) if modified_features else 0.0
        precision = len(intersection) / len(top_k_base) if top_k_base else 0.0
        
        return {
            'cf_sensitivity': recall, # Primary metric
            'cf_sensitivity_recall': recall,
            'cf_sensitivity_precision': precision
        }
