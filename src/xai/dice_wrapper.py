"""
DiCE Wrapper for Counterfactual Explanation Generation.

This module provides a standardized interface for generating counterfactual explanations
using the DiCE (Diverse Counterfactual Explanations) library.
"""
import logging
import pandas as pd
import numpy as np
import dice_ml
from typing import List, Dict, Any, Optional, Union

logger = logging.getLogger(__name__)

class DiCETabularWrapper:
    """
    Wrapper for DiCE tabular counterfactuals.
    """
    def __init__(
        self,
        model: Any,
        training_data: pd.DataFrame,
        target_column: str,
        continuous_features: List[str],
        categorical_features: List[str],
        backend: str = "sklearn",
        model_type: str = "classifier"
    ):
        """
        Initialize DiCE wrapper.

        Args:
            model: Trained model (sklearn-compatible).
            training_data: Training data including target column.
            target_column: Name of the target variable.
            continuous_features: List of continuous feature names.
            categorical_features: List of categorical feature names.
            backend: 'sklearn', 'TF1', 'TF2', 'PYT'. Defaults to 'sklearn'.
            model_type: 'classifier' or 'regressor'.
        """
        self.target_column = target_column
        
        # DiCE Data Object
        self.d = dice_ml.Data(
            dataframe=training_data,
            continuous_features=continuous_features,
            outcome_name=target_column
        )
        
        # DiCE Model Object
        self.m = dice_ml.Model(
            model=model,
            backend=backend,
            model_type=model_type
        )
        
        # DiCE Explainer
        # For sklearn backend, method typically needs to be 'random' or 'genetic' or 'kdtree'
        # 'random' is fastest for simple checks.
        self.exp = dice_ml.Dice(self.d, self.m, method="random")
        
    def generate_counterfactuals(
        self,
        query_instances: pd.DataFrame,
        total_CFs: int = 1,
        desired_class: Union[int, str] = "opposite"
    ) -> List[pd.DataFrame]:
        """
        Generate counterfactuals for query instances.

        Args:
            query_instances: DataFrame containing instances to explain (no target col).
            total_CFs: Number of counterfactuals to generate per instance.
            desired_class: Target class (or "opposite").

        Returns:
            List of DataFrames, each containing the CFs for the corresponding query instance.
        """
        # DiCE expects query_instances to be a DataFrame/dict
        # It handles one instance at a time or batch depending on backend.
        # Sklearn backend usually robust with single instances loop.
        
        cfs_list = []
        
        for idx, row in query_instances.iterrows():
            try:
                # Need to convert row to DF
                # DiCE expects the input to have feature names
                query_df = query_instances.loc[[idx]]
                
                # Generate
                dice_exp = self.exp.generate_counterfactuals(
                    query_df, 
                    total_CFs=total_CFs, 
                    desired_class=desired_class
                )
                
                # Get CFs as dataframe
                # visualize_as_dataframe returns None but prints, 
                # cf_examples.final_cfs_df is what we want.
                if dice_exp.cf_examples_list:
                    # Usually list of CFExample objects
                    cf_df = dice_exp.cf_examples_list[0].final_cfs_df
                    cfs_list.append(cf_df)
                else:
                    logger.warning(f"No CFs generated for instance {idx}")
                    cfs_list.append(pd.DataFrame())
                    
            except Exception as e:
                logger.error(f"Error generating CF for instance {idx}: {e}")
                cfs_list.append(pd.DataFrame())
                
        return cfs_list
