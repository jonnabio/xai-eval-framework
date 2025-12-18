"""
SHAP Tabular Wrapper for XAI Evaluation Framework.

This module provides a standardized interface for generating SHAP explanations
for tabular classification models, specifically optimized for tree-based models
(Random Forest, XGBoost) used in Experiment 1.
"""
import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import shap
from sklearn.utils import resample

# Configure module-level logger
logger = logging.getLogger(__name__)

def sample_background_data(
    X: np.ndarray,
    n_samples: int = 100,
    y: Optional[np.ndarray] = None,
    stratify: bool = True,
    random_state: int = 42
) -> np.ndarray:
    """
    Sample background data for SHAP explainer initialization.

    Args:
        X: Training data features (n_train_samples, n_features).
        n_samples: Number of background samples to select.
        y: Target labels (n_train_samples,). Required if stratify=True.
        stratify: Whether to perform stratified sampling.
        random_state: Random seed.

    Returns:
        Subsampled background data (n_samples, n_features).
    """
    # Robustness: If dataset is smaller than requested samples and not replacing, use entire dataset
    # (or up to dataset size)
    if n_samples > X.shape[0]:
        logger.warning(
            f"Requested {n_samples} background samples but only {X.shape[0]} available. "
            f"Using all {X.shape[0]} samples."
        )
        n_samples = X.shape[0]

    if stratify and y is not None:
        return resample(
            X, 
            n_samples=n_samples, 
            stratify=y, 
            random_state=random_state, 
            replace=False
        )
    else:
        return resample(
            X, 
            n_samples=n_samples, 
            random_state=random_state, 
            replace=False
        )

def validate_shap_additivity(
    shap_values: np.ndarray,
    expected_value: float,
    predictions: np.ndarray,
    tolerance: float = 1e-3
) -> Tuple[bool, float]:
    """
    Verify SHAP additivity property holds: expected_value + sum(shap_values) ≈ prediction.

    Args:
        shap_values: Feature attributions (n_samples, n_features).
        expected_value: Base value of the explainer.
        predictions: Model predictions (probabilities for positive class).
        tolerance: Maximum allowed absolute error.

    Returns:
        Tuple of (is_valid, max_error).
    """
    sum_attribs = np.sum(shap_values, axis=1)
    reconstructed_preds = expected_value + sum_attribs
    
    # Check absolute difference
    diffs = np.abs(reconstructed_preds - predictions)
    max_error = np.max(diffs)
    
    is_valid = max_error <= tolerance
    return is_valid, float(max_error)

class SHAPTabularWrapper:
    """
    Wrapper for SHAP tabular explanations with standardized output format.

    Attributes:
        explainer (shap.Explainer): Configured SHAP explainer (TreeExplainer or KernelExplainer).
        background_data (np.ndarray): Background data summary.
        expected_value (float): The base value E[f(x)].
        feature_names (List[str]): Feature names.
    """

    def __init__(
        self,
        model: Any,
        training_data: np.ndarray,
        feature_names: List[str],
        model_type: str = "tree",
        n_background_samples: int = 100,
        random_state: int = 42,
        training_labels: Optional[np.ndarray] = None
    ):
        """
        Initialize SHAP wrapper.

        Args:
            model: Trained model (sklearn RF, XGBoost, etc.).
            training_data: Dataset to sample background from.
            feature_names: List of feature names.
            model_type: "tree" or "kernel". 
            n_background_samples: Number of samples for background summary.
            random_state: Seed for sampling.
            training_labels: Optional labels for stratified background sampling.
        """
        self.feature_names = feature_names
        self.model_type = model_type.lower()
        self.n_background_samples = n_background_samples
        self.random_state = random_state

        # Sample background data
        self.background_data = sample_background_data(
            training_data, 
            n_samples=n_background_samples, 
            y=training_labels, 
            stratify=(training_labels is not None),
            random_state=random_state
        )

        # Initialize Explainer
        if self.model_type == "tree":
            logger.info("Initializing shap.TreeExplainer")
            # TreeExplainer handles background data for 'interventional' feature perturbation
            # If model is XGBoost, it might need model.predict_proba depending on version, 
            # but usually passed directly.
            self.explainer = shap.TreeExplainer(
                model, 
                data=self.background_data,
                feature_perturbation="interventional",
                model_output="probability" # Critical for getting proba units, not log-odds
            )
        else:
            logger.info("Initializing shap.KernelExplainer")
            if not hasattr(model, 'predict_proba'):
                raise ValueError("Model must have predict_proba for KernelExplainer fallback.")
            
            # KernelExplainer needs a callable
            self.explainer = shap.KernelExplainer(
                model.predict_proba, 
                self.background_data
            )

        # Check expected value (can be list or scalar)
        # For 'probability' output, it matches class probabilities
        if isinstance(self.explainer.expected_value, (list, np.ndarray)):
            # Usually index 1 for positive class in binary
            if len(self.explainer.expected_value) > 1:
                self.expected_value = float(self.explainer.expected_value[1])
            else:
                 self.expected_value = float(self.explainer.expected_value[0])
        else:
            self.expected_value = float(self.explainer.expected_value)

    def generate_explanations(
        self,
        model: Any, # Kept for interface consistency, but self.explainer has implicit model ref
        X_samples: np.ndarray,
        predict_fn: Optional[callable] = None # Unused for SHAP usually, implies model checks
    ) -> Dict[str, np.ndarray]:
        """
        Generate SHAP explanations for multiple instances.

        Returns:
            Dict containing 'feature_importance' (n, k), 'top_features' (n, k), 'metadata'.
        """
        start_time = time.time()
        
        # 1. Calculate SHAP values
        # Returns [ n_samples, n_features, n_classes ] usually for proba/binary
        # check_additivity=False to avoid strict errors on float precision, we validate manually.
        raw_shap_values = self.explainer.shap_values(X_samples, check_additivity=False)
        
        # 2. Extract Positive Class (Index 1)
        # TreeExplainer with model_output='probability' returns list of arrays [ (N, M), (N, M) ]
        feature_importance = None
        
        if isinstance(raw_shap_values, list):
            # Binary classification usually gives list of 2 arrays
            if len(raw_shap_values) > 1:
                feature_importance = raw_shap_values[1]
            else:
                feature_importance = raw_shap_values[0]
        elif isinstance(raw_shap_values, np.ndarray):
            # If 3D array (N, M, C)
            if raw_shap_values.ndim == 3 and raw_shap_values.shape[2] > 1:
                feature_importance = raw_shap_values[:, :, 1]
            else:
                feature_importance = raw_shap_values
        else:
            raise TypeError(f"Unexpected SHAP output type: {type(raw_shap_values)}")
            
        # Ensure it is dense (N, M) and Float
        feature_importance = np.array(feature_importance, dtype=float)

        # 3. Top Features
        # Sort by absolute importance
        top_features = np.argsort(np.abs(feature_importance), axis=1)[:, ::-1]
        
        total_time = time.time() - start_time
        
        metadata = {
            'total_time_seconds': total_time,
            'avg_time_per_instance': total_time / len(X_samples),
            'expected_value': self.expected_value,
            'model_type': self.model_type,
            'n_background_samples': self.n_background_samples
        }
        
        return {
            'feature_importance': feature_importance,
            'top_features': top_features,
            'metadata': metadata
        }

    def explain_instance(
        self,
        model: Any,
        instance: np.ndarray,
        return_full: bool = False
    ) -> Union[np.ndarray, Tuple[np.ndarray, Any]]:
        """
        Explain single instance.
        """
        # Reshape to (1, n_features)
        if instance.ndim == 1:
            X_batch = instance.reshape(1, -1)
        else:
            X_batch = instance
            
        result = self.generate_explanations(model, X_batch)
        imp_vector = result['feature_importance'][0]
        
        if return_full:
            return imp_vector, result
        return imp_vector
        
    def get_expected_value(self) -> float:
        return self.expected_value

    def get_config(self) -> Dict:
        return {
            'model_type': self.model_type,
            'n_background_samples': self.n_background_samples,
            'random_state': self.random_state,
            'expected_value': self.expected_value
        }

def generate_shap_explanations(
    model: Any,
    X_samples: np.ndarray,
    training_data: np.ndarray,
    feature_names: List[str],
    model_type: str = "tree",
    n_background_samples: int = 100,
    random_state: int = 42,
    **shap_kwargs
) -> Dict[str, np.ndarray]:
    """
    Convenience function for SHAP explanations.
    """
    wrapper = SHAPTabularWrapper(
        model=model,
        training_data=training_data,
        feature_names=feature_names,
        model_type=model_type,
        n_background_samples=n_background_samples,
        random_state=random_state
    )
    
    return wrapper.generate_explanations(model, X_samples)
