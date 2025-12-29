"""
Counterfactual Sensitivity Metric.

Measures the alignment between feature importance explanations (SHAP/LIME)
and counterfactual explanations (DiCE).
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional

class CounterfactualSensivtyMetric:
    """
    Computes sensitivity of explanation to counterfactual changes.
    
    Definition:
    Recall of Top-K explanation features with respect to the set of features 
    modified in the generated counterfactuals.
    """
    
    def __init__(self):
        pass
        
    def compute(
        self, 
        feature_importance: np.ndarray, 
        feature_names: List[str], 
        original_instance: pd.DataFrame,
        cf_files: pd.DataFrame,
        k: int = 5
    ) -> Dict[str, float]:
        """
        Compute agreement between importance and CF changes.
        
        Args:
            feature_importance: Explanation weights.
            feature_names: List of feature names.
            original_instance: The original instance (as 1-row DataFrame).
            cf_files: The generated counterfactuals (DataFrame).
            k: Top-K features to check.
            
        Returns:
            Dictionary with 'cf_sensitivity_recall' and 'cf_sensitivity_precision'.
        """
        if cf_files is None or cf_files.empty:
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
        # Ignore target if present? usually last col or 'income'
        
        modified_features = set()
        
        # original array
        orig_vals = original_instance[common_cols].iloc[0].values
        
        # Check each CF
        for _, cf_row in cf_files.iterrows():
            cf_vals = cf_row[common_cols].values
            
            # Where do they differ?
            # Handle float comparison carefully, and categorical
            # For simplicity, string comparison for cats, isclose for floats
            
            # Simple inequality mask
            # If data is mixed types, element-wise comparison in numpy can be tricky if not cast
            # Let's iterate
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
            # CF is identical to original? (Did not flip?)
            return {
                'cf_sensitivity': 0.0,
                'cf_sensitivity_recall': 0.0, 
                'cf_sensitivity_precision': 0.0
            }

        # 2. Identify Top-K Explanation Features
        abs_weights = np.abs(feature_importance)
        top_k_indices = np.argsort(abs_weights)[-k:][::-1]
        top_k_features = [feature_names[i] for i in top_k_indices]
        
        # 3. Compute Overlap
        # Need to handle One-Hot-Encoding mapping if feature_names are OHE
        # but DiCE usually works on raw data (pre-transform).
        # THIS IS A TRICKY PART.
        # If 'feature_names' are from the MODEL input (OHE), and 'original_instance' is passed to DiCE (Raw),
        # we have a mismatch.
        # Assumption: EXP1 uses a pipeline where model input is OHE, but we likely have access to RAW data for DiCE.
        # BUT, the explainer explains the OHE features.
        # So we need to map OHE features -> Base features.
        
        def get_base_feature(f):
            if '_' in f: return f.split('_')[0]
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
