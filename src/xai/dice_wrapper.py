"""
DiCE Wrapper (Counterfactuals) for Tabular Data.

This module provides a standardized interface for generating counterfactual explanations
using the DiCE library, adapted to the ExplainerWrapper interface.
"""
import logging
import pandas as pd
import numpy as np
import time
from typing import List, Dict, Any, Optional, Union

from .base import ExplainerWrapper

logger = logging.getLogger(__name__)

class DiCETabularWrapper(ExplainerWrapper):
    """
    Wrapper for DiCE (Diverse Counterfactual Explanations).
    
    Adapts counterfactual generation to 'feature importance' by calculating
    the difference between the original instance and the generated counterfactual.
    Features that changed are considered 'important'.
    """

    def __init__(
        self, 
        training_data: np.ndarray, 
        feature_names: List[str], 
        categorical_features: List[str] = None,
        target_column: str = "target",
        **kwargs
    ):
        super().__init__(training_data, feature_names, **kwargs)
        self.categorical_features = categorical_features or []
        self.target_column = target_column
        self.dice_exp = None
        self.dice_m = None
        self.dice_d = None
        
    def _lazy_init(self, model):
        """Initialize DiCE lazily."""
        if self.dice_exp is not None:
            return

        try:
            import dice_ml
        except ImportError:
            raise ImportError("dice-ml is required. Install with `pip install dice-ml`.")
            
        logger.info("Initializing DiCE explainer...")
        
        # 1. Prepare Data
        # DiCE requires a dataframe with feature names + target
        # We need to reconstruct it from numpy training_data
        df_train = pd.DataFrame(self.training_data, columns=self.feature_names)
        # Add dummy target if not present (BaseTrainer usually splits X/y)
        # Here we assume training_data passed to init is just X.
        # DiCE needs knowledge of outcome range or class.
        # Workaround: Use model predictions on training data to verify?
        # Or Just assume binary classification 0/1 for now as per Adult/Thesis.
        df_train[self.target_column] = 0 # Dummy, DiCE just needs column existence for some operations
        
        self.dice_d = dice_ml.Data(
            dataframe=df_train,
            continuous_features=[f for f in self.feature_names if f not in self.categorical_features],
            outcome_name=self.target_column
        )
        
        # 2. Prepare Model
        self.dice_m = dice_ml.Model(
            model=model,
            backend="sklearn", # We forced sklearn backend for generic trainers
            model_type="classifier"
        )
        
        # 3. Explainer
        self.dice_exp = dice_ml.Dice(self.dice_d, self.dice_m, method="random") # 'random' is fast
        logger.info("DiCE initialized.")

    def generate_explanations(
        self, 
        model: Any, 
        X_samples: np.ndarray, 
        predict_fn: Optional[Any] = None
    ) -> Dict[str, np.ndarray]:
        """
        Generate Counterfactual-based importance.
        """
        self._lazy_init(model)
        
        n_samples = X_samples.shape[0]
        n_features = X_samples.shape[1]
        feature_importance = np.zeros((n_samples, n_features))
        
        start_time = time.time()
        
        # Convert to DF for DiCE
        query_df = pd.DataFrame(X_samples, columns=self.feature_names)
        
        for i in range(n_samples):
            try:
                # Generate CF
                # total_CFs=1, desired_class="opposite"
                dice_exp = self.dice_exp.generate_counterfactuals(
                    query_df.iloc[[i]], 
                    total_CFs=1, 
                    desired_class="opposite"
                )
                
                if dice_exp.cf_examples_list:
                    # Get CF DataFrame
                    cf_df = dice_exp.cf_examples_list[0].final_cfs_df
                    if not cf_df.empty:
                        # Extract CF vector (drop target)
                        # Ensure columns match order
                        cf_vector = cf_df[self.feature_names].iloc[0].values
                        original_vector = X_samples[i]
                        
                        # Importance = Absolute Difference between Original and CF
                        # (Normalized to [0,1] effectively if features are scaled, otherwise raw diff)
                        diff = np.abs(original_vector - cf_vector)
                        feature_importance[i] = diff
                        
            except Exception as e:
                logger.warning(f"DiCE failed for sample {i}: {e}")
                
        duration = time.time() - start_time
        
        # Top features are just argsort of differences
        top_features = np.argsort(-feature_importance, axis=1)[:, :5] # Top 5 changes

        return {
            'feature_importance': feature_importance,
            'top_features': top_features,
            'metadata': {
                'method': 'DiCE',
                'duration': duration,
                'count': n_samples
            }
        }

    def get_config(self) -> Dict[str, Any]:
        return {
            "method": "DiCE",
            "kwargs": self.kwargs
        }
