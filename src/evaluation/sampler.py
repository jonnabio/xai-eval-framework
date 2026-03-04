"""
Evaluation Sampler Module.

This module provides the EvaluationSampler class to select stratified
evaluation instances (TP, TN, FP, FN) from test data.
"""
import logging
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

# Configure module-level logger
logger = logging.getLogger(__name__)

class EvaluationSampler:
    """
    Sampler for selecting a balanced evaluation dataset for XAI metrics.
    
    It stratifies samples based on error analysis quadrants:
    - True Positives (TP)
    - True Negatives (TN)
    - False Positives (FP)
    - False Negatives (FN)
    """

    def __init__(
        self,
        model: BaseEstimator,
        X_test: Union[pd.DataFrame, np.ndarray],
        y_test: Union[pd.Series, np.ndarray],
        random_state: int = 42
    ):
        """
        Initialize the sampler.

        Args:
            model: Trained classifier (with predict method).
            X_test: Test features.
            y_test: True test labels.
            random_state: Seed for reproducibility.
        """
        self.model = model
        self.X_test = X_test
        self.y_test = np.array(y_test)
        self.random_state = random_state
        
        # Validate inputs
        if len(self.X_test) != len(self.y_test):
            raise ValueError(f"Length mismatch: X_test ({len(self.X_test)}) vs y_test ({len(self.y_test)})")

    def sample_stratified_by_error(self, n_per_group: int = 50) -> pd.DataFrame:
        """
        Stratify samples by TP/TN/FP/FN groups.

        Args:
            n_per_group: Target number of samples per quadrant.

        Returns:
            DataFrame containing samples with metadata columns:
            ['target', 'prediction', 'quadrant', 'original_index'].
        """
        # 1. Generate predictions
        if hasattr(self.model, "predict"):
            preds = self.model.predict(self.X_test)
        else:
            raise ValueError("Model must have a predict method.")
            
        preds = np.array(preds)
        
        # 2. Identify quadrants
        tp_mask = (self.y_test == 1) & (preds == 1)
        tn_mask = (self.y_test == 0) & (preds == 0)
        fp_mask = (self.y_test == 0) & (preds == 1)
        fn_mask = (self.y_test == 1) & (preds == 0)
        
        indices = np.arange(len(self.y_test))
        
        groups = {
            'TP': indices[tp_mask],
            'TN': indices[tn_mask],
            'FP': indices[fp_mask],
            'FN': indices[fn_mask]
        }
        
        # 3. Sample from each group
        selected_indices = []
        sampled_data = []
        
        rng = np.random.RandomState(self.random_state)
        
        for quadrant, group_idxs in groups.items():
            n_available = len(group_idxs)
            if n_available == 0:
                logger.warning(f"No samples found for quadrant {quadrant}")
                continue
                
            n_select = min(n_per_group, n_available)
            selected = rng.choice(group_idxs, size=n_select, replace=False)
            selected_indices.extend(selected)
            
            # Record metadata
            for idx in selected:
                sampled_data.append({
                    'original_index': idx,
                    'target': self.y_test[idx],
                    'prediction': preds[idx],
                    'quadrant': quadrant
                })
                
        # 4. Construct Result DataFrame
        # Convert X_test to DataFrame if needed to handle feature names
        if isinstance(self.X_test, np.ndarray):
            # Create generic names if ndarray
            cols = [f"feature_{i}" for i in range(self.X_test.shape[1])]
            X_subset = pd.DataFrame(self.X_test[selected_indices], columns=cols)
        else:
            # Assuming pandas DataFrame, iloc works
            X_subset = self.X_test.iloc[selected_indices].reset_index(drop=True)
            
        meta_df = pd.DataFrame(sampled_data)
        
        # Concatenate features and metadata
        # meta_df has same length and order as X_subset implied by selected_indices order
        # But wait, selected_indices was extended sequentially.
        # X_subset created by iloc[selected_indices] preserves that order.
        # So specific index-wise alignment is preserved.
        
        result = pd.concat([meta_df, X_subset], axis=1)
        
        logger.info(f"Sampled {len(result)} instances total.")
        for q, idxs in groups.items():
            n_sel = len([x for x in sampled_data if x['quadrant'] == q])
            logger.info(f"  {q}: {n_sel}/{len(idxs)} available")
            
        return result

    def save_instances(self, instances_df: pd.DataFrame, output_path: Union[str, Path]) -> None:
        """
        Save evaluation instances to CSV.

        Args:
            instances_df: DataFrame from sample_stratified_by_error.
            output_path: Destination path.
        """
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        instances_df.to_csv(out, index=False)
        logger.info(f"Saved evaluation dataset to {out}")
