"""
LIME (Local Interpretable Model-agnostic Explanations) wrapper for tabular data.

This module provides a standardized interface for generating LIME explanations
for binary classification models on tabular datasets.
"""
# Standard library imports
from typing import Any, Dict, List, Optional, Tuple, Union
import time

# Third-party imports
import numpy as np
from lime.lime_tabular import LimeTabularExplainer

from .base import ExplainerWrapper

class LIMETabularWrapper(ExplainerWrapper):
    """
    Wrapper for LIME tabular explanations with standardized output format.

    Attributes:
        explainer (LimeTabularExplainer): Configured LIME explainer instance
        feature_names (List[str]): Names of input features
        num_features (int): Number of top features to include in explanations
        num_samples (int): Number of samples for local model training
    """

    def __init__(
        self,
        training_data: np.ndarray,
        feature_names: List[str],
        class_names: Optional[List[str]] = None,
        num_features: int = 10,
        num_samples: int = 5000,
        kernel_width: Optional[float] = None,
        discretize_continuous: bool = False,
        feature_selection: str = 'auto',
        random_state: int = 42,
        **kwargs
    ):
        """
        Initialize LIME wrapper with configuration.

        Args:
            training_data: Training data (n_samples, n_features) to initialize statistics.
            feature_names: List of feature names matching columns in training_data.
            class_names: Names of prediction classes. Defaults to ['0', '1'].
            num_features: Number of features to include in the explanation.
            num_samples: Number of perturbed samples for local surrogate training.
            kernel_width: Kernel width for the exponential kernel. None = auto.
            discretize_continuous: Whether to discretize continuous features.
            feature_selection: Feature selection method (auto, none, forward_selection, etc).
            random_state: Random seed for reproducibility.
            **kwargs: Additional LIME arguments.
        """
        super().__init__(training_data, feature_names, **kwargs)
        
        # Validate inputs
        if training_data.shape[1] != len(feature_names):
            raise ValueError(
                f"Mismatch: training_data has {training_data.shape[1]} columns but "
                f"feature_names has length {len(feature_names)}."
            )

        # Store configuration
        self.class_names = class_names if class_names else ['0', '1']
        self.num_features = num_features
        self.num_samples = num_samples
        self.kernel_width = kernel_width
        self.discretize_continuous = discretize_continuous
        self.feature_selection = feature_selection
        self.random_state = random_state

        # Initialize LIME Explainer
        self.explainer = LimeTabularExplainer(
            training_data=self.training_data,
            feature_names=self.feature_names,
            class_names=self.class_names,
            mode='classification',
            discretize_continuous=self.discretize_continuous,
            feature_selection=self.feature_selection,
            kernel_width=self.kernel_width,
            random_state=self.random_state,
            **self.kwargs
        )

    def generate_explanations(
        self,
        model: Any,
        X_samples: np.ndarray,
        predict_fn: Optional[callable] = None
    ) -> Dict[str, np.ndarray]:
        """
        Generate LIME explanations for multiple instances.

        Args:
            model: Trained model with predict_proba method.
            X_samples: Samples to explain (n_instances, n_features).
            predict_fn: Optional custom prediction function (default: model.predict_proba).

        Returns:
            Dictionary containing:
                - 'feature_importance': Array of shape (n_instances, n_features).
                - 'top_features': Array of shape (n_instances, num_features).
                - 'metadata': Dict with timing, LIME config, etc.
        """
        # Validate inputs
        if X_samples.ndim == 1:
            X_samples = X_samples.reshape(1, -1)

        if X_samples.shape[1] != len(self.feature_names):
            raise ValueError(
                f"X_samples has {X_samples.shape[1]} features, "
                f"but wrapper expects {len(self.feature_names)}"
            )

        n_instances = X_samples.shape[0]
        n_features = X_samples.shape[1]

        # Use model's predict_proba if custom function not provided
        if predict_fn is None:
            if not hasattr(model, 'predict_proba'):
                raise ValueError("Model must have predict_proba method or provide predict_fn")
            predict_fn = model.predict_proba

        # Initialize result arrays
        effective_num_features = min(self.num_features, n_features)
        feature_importance = np.zeros((n_instances, n_features))
        top_features = np.zeros((n_instances, effective_num_features), dtype=int)

        # Track timing
        start_time = time.time()
        instance_times = []

        # Generate explanation for each instance
        for i, instance in enumerate(X_samples):
            instance_start = time.time()

            imp_vector, _ = self.explain_instance(
                model=model,
                instance=instance,
                predict_fn=predict_fn,
                return_full=True
            )
            
            feature_importance[i] = imp_vector
            
            # Get top features by absolute importance
            abs_importance = np.abs(imp_vector)
            # argsort returns ascending, so we take last effective_num_features and reverse
            top_features[i] = np.argsort(abs_importance)[::-1][:effective_num_features]

            instance_times.append(time.time() - instance_start)

        total_time = time.time() - start_time

        # Compile metadata
        metadata = {
            'total_time_seconds': total_time,
            'avg_time_per_instance': total_time / n_instances if n_instances > 0 else 0,
            'instance_times': instance_times,
            'num_features_requested': self.num_features,
            'effective_num_features': effective_num_features,
            'num_samples': self.num_samples,
            'n_instances': n_instances,
            'n_features': n_features,
            'kernel_width': self.kernel_width,
            'random_state': self.random_state
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
        predict_fn: Optional[callable] = None,
        return_full: bool = False
    ) -> Union[np.ndarray, Tuple[np.ndarray, object]]:
        """
        Generate LIME explanation for a single instance.
        """
        # Validate input
        if instance.ndim != 1:
            raise ValueError(f"instance must be 1D array, got shape {instance.shape}")

        if instance.shape[0] != len(self.feature_names):
            raise ValueError(
                f"instance has {instance.shape[0]} features, "
                f"but wrapper expects {len(self.feature_names)}"
            )

        # Use model's predict_proba if custom function not provided
        if predict_fn is None:
            if not hasattr(model, 'predict_proba'):
                raise ValueError("Model must have predict_proba method or provide predict_fn")
            predict_fn = model.predict_proba

        # Generate LIME explanation
        exp = self.explainer.explain_instance(
            data_row=instance,
            predict_fn=predict_fn,
            num_features=self.num_features,
            num_samples=self.num_samples
        )

        # Convert to feature importance vector
        importance_vector = np.zeros(len(self.feature_names))

        # Get explanation as map (feature_idx -> importance)
        # Check available labels in map
        target_label = 1
        
        if target_label in exp.as_map():
            exp_map = exp.as_map()[target_label]
        else:
            exp_map = exp.as_map().get(1, [])

        for feat_idx, importance in exp_map:
            if feat_idx < len(importance_vector):
                importance_vector[feat_idx] = importance

        if return_full:
            return importance_vector, exp
        else:
            return importance_vector

    def get_config(self) -> Dict:
        """
        Get current LIME configuration.
        """
        return {
            'num_features': self.num_features,
            'num_samples': self.num_samples,
            'kernel_width': self.kernel_width,
            'discretize_continuous': self.discretize_continuous,
            'feature_selection': self.feature_selection,
            'random_state': self.random_state,
            'feature_names': self.feature_names,
            'class_names': self.class_names,
            'n_training_samples': self.training_data.shape[0],
            'n_features': len(self.feature_names)
        }

def generate_lime_explanations(
    model,
    X_samples: np.ndarray,
    training_data: np.ndarray,
    feature_names: List[str],
    num_features: int = 10,
    num_samples: int = 5000,
    random_state: int = 42,
    **lime_kwargs
) -> Dict[str, np.ndarray]:
    """
    Convenience function for generating LIME explanations without explicit wrapper instantiation.
    """
    # Create wrapper instance
    wrapper = LIMETabularWrapper(
        training_data=training_data,
        feature_names=feature_names,
        num_features=num_features,
        num_samples=num_samples,
        random_state=random_state,
        **lime_kwargs
    )

    # Generate and return explanations
    return wrapper.generate_explanations(model=model, X_samples=X_samples)

# Module-level configuration for default LIME parameters
DEFAULT_LIME_CONFIG = {
    'num_features': 10,
    'num_samples': 5000,
    'kernel_width': None,
    'discretize_continuous': False,
    'random_state': 42
}
