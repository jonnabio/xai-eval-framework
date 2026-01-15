"""
Base Trainer Module.

This module defines the abstract base class for all model trainers in the framework.
It enforces a consistent interface for training, evaluation, and persistence, enabling
polymorphic usage by the ExperimentRunner.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
import json
import joblib
import time
import logging
import numpy as np
import pandas as pd
import sklearn.metrics as metrics

logger = logging.getLogger(__name__)

class BaseTrainer(ABC):
    """
    Abstract Base Class for Model Trainers.
    
    All model implementations (RF, XGB, SVM, MLP) must inherit from this class
    and implement the abstract methods. This ensures the ExperimentRunner can
    interact with any model type uniformly.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the trainer with configuration.
        
        Args:
            config: Dictionary containing model hyperparameters and settings.
        """
        self.config = config
        self.model = None
        self.metrics: Dict[str, Any] = {}
        self.feature_names: Optional[List[str]] = None
        
    @abstractmethod
    def train(self, X_train: Any, y_train: Any, X_val: Any = None, y_val: Any = None) -> 'BaseTrainer':
        """
        Train the model.
        
        Args:
            X_train: Training features.
            y_train: Training labels.
            X_val: Validation features (optional, for early stopping).
            y_val: Validation labels (optional).
            
        Returns:
            self: For method chaining.
        """
        pass

    @abstractmethod
    def predict(self, X: Any) -> np.ndarray:
        """
        Generate class predictions.
        
        Args:
            X: Input features.
            
        Returns:
            Array of predicted class labels.
        """
        pass

    @abstractmethod
    def predict_proba(self, X: Any) -> np.ndarray:
        """
        Generate class probabilities.
        
        Args:
            X: Input features.
            
        Returns:
            Array of shape (n_samples, n_classes) with probabilities.
        """
        pass

    def evaluate(self, X_test: Any, y_test: Any) -> Dict[str, float]:
        """
        Evaluate model performance on test dataset.
        
        This method is concrete because metrics are standardized across all
        classification models in this framework.
        
        Args:
            X_test: Test features.
            y_test: True test labels.
            
        Returns:
            Dictionary of metrics (accuracy, precision, recall, f1, roc_auc).
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
            
        logger.info("Evaluating model performance...")
        
        y_pred = self.predict(X_test)
        
        # Handle probability prediction for ROC AUC
        try:
            y_prob = self.predict_proba(X_test)[:, 1]
        except (AttributeError, IndexError):
            y_prob = None
            logger.warning("Model does not support predict_proba or binary classification. ROC AUC will be None.")
        
        # Calculate Metrics
        # Weighted average used due to potential class imbalance in Adult dataset
        self.metrics = {
            "accuracy": float(metrics.accuracy_score(y_test, y_pred)),
            "precision": float(metrics.precision_score(y_test, y_pred, average='weighted', zero_division=0)),
            "recall": float(metrics.recall_score(y_test, y_pred, average='weighted', zero_division=0)),
            "f1": float(metrics.f1_score(y_test, y_pred, average='weighted', zero_division=0)),
            "roc_auc": float(metrics.roc_auc_score(y_test, y_prob)) if y_prob is not None else None,
            "confusion_matrix": metrics.confusion_matrix(y_test, y_pred).tolist()
        }
        
        logger.debug(f"Evaluation Metrics: {json.dumps(self.metrics, indent=2)}")
        return self.metrics

    def save(self, path: Union[str, Path], filename: str = "model.pkl") -> Path:
        """
        Persist model and artifacts to disk.
        
        Args:
            path: Directory to save artifacts.
            filename: Name of the model file.
            
        Returns:
            Path to the saved model file.
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
            
        save_dir = Path(path)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # 1. Save Model object
            model_path = save_dir / filename
            joblib.dump(self.model, model_path)
            
            # 2. Save Metrics
            metrics_path = save_dir / "metrics.json"
            with open(metrics_path, 'w') as f:
                json.dump(self.metrics, f, indent=2)
                
            # 3. Save Metadata
            metadata = {
                "model_class": self.__class__.__name__,
                "training_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "config": self.config,
                "feature_names": self.feature_names
            }
            metadata_path = save_dir / "metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
            logger.info(f"Model artifacts saved to {save_dir}")
            return model_path
            
        except Exception as e:
            logger.error(f"Failed to save model artifacts: {e}")
            raise e

    @classmethod
    def load(cls, path: Union[str, Path], filename: str = "model.pkl") -> 'BaseTrainer':
        """
        Load a trained trainer from disk.
        
        Args:
            path: Directory containing saved artifacts.
            filename: Name of the model file.
            
        Returns:
            Initialized trainer instance with loaded model.
        """
        path = Path(path)
        model_path = path / filename
        metadata_path = path / "metadata.json"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
            
        # Load metadata
        config = {}
        feature_names = None
        metrics_data = {}
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                config = metadata.get('config', {})
                feature_names = metadata.get('feature_names')
        
        # Initialize
        trainer = cls(config)
        trainer.model = joblib.load(model_path)
        trainer.feature_names = feature_names
        
        # Try load metrics if exist
        metrics_path = path / "metrics.json"
        if metrics_path.exists():
            with open(metrics_path, 'r') as f:
                trainer.metrics = json.load(f)
                
        logger.info(f"Loaded {cls.__name__} from {path}")
        return trainer
