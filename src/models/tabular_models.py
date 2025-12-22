# User Story: EXP1-08
"""
Tabular Model Training and Evaluation for XAI Experiments.

This module provides the core functionality for training, evaluating, and managing
tabular machine learning models, specifically Random Forests, within the context
of Experiment 1 (Adult Dataset).

It handles the complete lifecycle of model creation:
1. Training with configurable hyperparameters.
2. Comprehensive evaluation (Accuracy, ROC-AUC, Confusion Matrix).
3. Feature importance extraction and ranking.
4. Model persistence with rich metadata (metrics, environment details).
5. Validation against performance thresholds.

Key Classes:
    AdultRandomForestTrainer: Class-based manager for the training pipeline.

Key Functions:
    train_random_forest_adult: Main driver for training and evaluation.
    calculate_classification_metrics: Computes detailed performance metrics.
    get_feature_importance: Extracts and ranks feature importance.
    save_model_with_metadata: Persists model and metadata safely.
    load_trained_model: Loading utility with verification.

Experiment Context:
    Experiment 1 focuses on establishing a baseline Random Forest model on the
    Adult Income dataset to serve as a target for subsequent XAI explanation
    methods (LIME, SHAP).

Examples:
    >>> from src.models.tabular_models import train_random_forest_adult
    >>> model, metrics = train_random_forest_adult(
    ...     config_path="experiments/exp1_adult/configs/models/rf_adult_config.json",
    ...     force_retrain=True
    ... )
    >>> print(metrics['test_accuracy'])
    0.8523

References:
    Experiment Documentation: experiments/exp1_adult/README.md
"""

import logging
import json
import yaml
import time
import os
import platform
import sys
from pathlib import Path
from typing import Dict, Tuple, Any, Optional

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)
import joblib

# Setup logging configuration at module level
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Import data loader
try:
    from src.data_loading.adult import load_adult
except ImportError:
    # Fallback for running as script from different location
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from src.data_loading.adult import load_adult

def calculate_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: Optional[np.ndarray] = None,
    prefix: str = ""
) -> Dict[str, Any]:
    """
    Calculate comprehensive classification metrics.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_proba: Predicted probabilities (optional)
        prefix: Prefix for metric keys (optional)
        
    Returns:
        Dictionary containing calculated metrics
    """
    if prefix and not prefix.endswith("_"):
        prefix = f"{prefix}_"
        
    metrics = {
        "timestamp": time.time()
    }
    

    # 1. Basic metrics
    # Rounding to 4 decimal places ensures consistent reporting without false precision.
    metrics[f"{prefix}accuracy"] = round(accuracy_score(y_true, y_pred), 4)
    
    # Use 'macro' average to treat all classes equally, important for imbalanced datasets like Adult.
    # zero_division=0 prevents warnings/errors when a class is not predicted at all.
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='macro', zero_division=0
    )
    metrics[f"{prefix}precision_macro"] = round(precision, 4)
    metrics[f"{prefix}recall_macro"] = round(recall, 4)
    metrics[f"{prefix}f1_macro"] = round(f1, 4)
    
    if y_proba is not None:
        try:
            # Handle binary vs multiclass
            # Check shape[1] because sometimes binary proba returns (n_samples, 2) and sometimes 1D in other libraries.
            if y_proba.ndim == 2 and y_proba.shape[1] == 2:
                # Binary case: explicit use of positive class (index 1) for ROC AUC
                auc = roc_auc_score(y_true, y_proba[:, 1])
            else:
                # Multiclass case or 1D: 'ovr' (One-vs-Rest) is standard for multiclass AUC.
                auc = roc_auc_score(y_true, y_proba, multi_class='ovr')
            metrics[f"{prefix}roc_auc"] = round(auc, 4)
        except Exception as e:
            logger.warning(f"Could not calculate ROC AUC: {e}")
            metrics[f"{prefix}roc_auc"] = None

    # 2. Confusion Matrix stats (Binary specific mainly, or flattened)
    cm = confusion_matrix(y_true, y_pred)
    # Only calculate detailed counts for binary to avoiding complexity in multiclass scenarios
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        total = np.sum(cm)
        metrics[f"{prefix}confusion_counts"] = {
            "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)
        }
        # Percentages helpful for quick intuition on error distribution
        metrics[f"{prefix}confusion_percentages"] = {
            "tn": round(tn/total, 4), "fp": round(fp/total, 4),
            "fn": round(fn/total, 4), "tp": round(tp/total, 4)
        }
    
    # 3. Class Distribution
    # Critical for detecting model collapse (predicting only one class)
    # Predicted
    unique, counts = np.unique(y_pred, return_counts=True)
    metrics[f"{prefix}pred_class_distribution"] = {
        str(k): int(v) for k, v in zip(unique, counts)
    }
    
    # True
    unique_true, counts_true = np.unique(y_true, return_counts=True)
    metrics[f"{prefix}true_class_distribution"] = {
        str(k): int(v) for k, v in zip(unique_true, counts_true)
    }
    
    # 4. Confidence statistics
    # Helps assess calibration. High accuracy but low confidence suggests "lucky" model or difficult boundary.
    if y_proba is not None:
        # Assuming last dimension is classes
        max_probs = np.max(y_proba, axis=1)
        metrics[f"{prefix}mean_confidence"] = round(float(np.mean(max_probs)), 4)
        metrics[f"{prefix}std_confidence"] = round(float(np.std(max_probs)), 4)
        
    return metrics

def get_feature_importance(
    model: RandomForestClassifier,
    feature_names: list,
    top_k: int = 20,
    save_path: str = None
) -> pd.DataFrame:
    """
    Extract and rank feature importances.
    
    Args:
        model: Trained Random Forest model
        feature_names: List of feature names matching model input
        top_k: Number of top features to log/return check
        save_path: Optional path to save CSV
        
    Returns:
        DataFrame with feature importances
    """
    # Note: feature_importances_ in sklearn RF is "Gini Importance" (impurity-based).
    # It favors high-cardinality features. For Experiment 1 baseline, this is acceptable,
    # but permutation importance should be considered for deeper analysis.
    importances = model.feature_importances_
    
    # Create DataFrame
    df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    })
    
    # Sort and rank
    df = df.sort_values('importance', ascending=False).reset_index(drop=True)
    df['rank'] = df.index + 1
    # Global explanation often focuses on top % of total importance
    df['cumulative_importance'] = df['importance'].cumsum()
    
    # Log top features
    logger.info(f"Top {min(10, len(df))} Features:")
    for i, row in df.head(10).iterrows():
        logger.info(f"{int(row['rank'])}. {row['feature']}: {row['importance']:.4f}")
        
    # Save if path provided
    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
        logger.info(f"Feature importance saved to {path}")
        
    return df

def save_model_with_metadata(
    model: RandomForestClassifier,
    metrics: Dict[str, Any],
    config: Dict[str, Any],
    feature_names: list
) -> str:
    """
    Save model and metadata, return save path.
    
    Args:
        model: Trained Random Forest model
        metrics: Dictionary of calculated metrics
        config: Configuration dictionary used for training
        feature_names: List of feature names
        
    Returns:
        str: Full path to the saved model file
    """
    try:
        output_config = config['output']
        model_dir = Path(output_config['model_dir'])
        
        # 1. Create directory
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Save model
        model_filename = output_config.get('model_filename', 'rf_model.pkl')
        model_path = model_dir / model_filename
        joblib.dump(model, model_path)
        
        # 3. Create metadata
        metadata = {
            "model_type": "RandomForest",
            "training_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "model_params": config['model']['params'],
            "performance_metrics": {
                "accuracy": metrics.get("test_accuracy"),
                "roc_auc": metrics.get("test_roc_auc"),
                "f1_macro": metrics.get("test_f1_macro")
            },
            "feature_names": feature_names,
            "sklearn_version": sklearn.__version__,
            "python_version": platform.python_version()
        }
        
        # 4. Save metadata
        metadata_filename = model_path.stem + "_metadata.json"
        metadata_path = model_dir / metadata_filename
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        # 5. Verify files
        if not model_path.exists():
            raise FileNotFoundError(f"Failed to save model to {model_path}")
        if not metadata_path.exists():
            logger.warning(f"Failed to save metadata to {metadata_path}")
            
        return str(model_path)

    except Exception as e:
        logger.error(f"Error in save_model_with_metadata: {str(e)}")
        raise

def load_trained_model(model_path: str) -> RandomForestClassifier:
    """
    Load a trained model from disk.
    
    Args:
        model_path: Path to the .pkl file
        
    Returns:
        Loaded RandomForestClassifier model
    """
    path = Path(model_path)
    if not path.exists():
        logger.error(f"Model file not found: {model_path}")
        raise FileNotFoundError(f"Model file not found: {model_path}")
        
    try:
        model = joblib.load(path)
        if not isinstance(model, RandomForestClassifier):
            logger.warning(f"Loaded model is not RandomForestClassifier, got {type(model)}")
        return model
    except Exception as e:
        logger.error(f"Error loading model from {model_path}: {e}")
        raise

def load_model_metadata(model_dir: str) -> Dict[str, Any]:
    """
    Load model metadata JSON.
    
    Args:
        model_dir: Directory containing the model and metadata
        
    Returns:
        Metadata dictionary, or empty dict if not found
    """
    dir_path = Path(model_dir)
    # Find metadata file (assuming *_metadata.json pattern)
    meta_files = list(dir_path.glob("*_metadata.json"))
    
    if not meta_files:
        logger.warning(f"No metadata file found in {model_dir}")
        return {}
        
    # Load the first one found (usually only one per specific model run/dir)
    meta_path = meta_files[0]
    try:
        with open(meta_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading metadata {meta_path}: {e}")
        return {}

def verify_model_performance(
    model: Any, 
    X_test: np.ndarray, 
    y_test: np.ndarray, 
    thresholds: Dict[str, float]
) -> bool:
    """
    Verify if model meets performance thresholds.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        thresholds: Dictionary of {metric_name: min_value}
        
    Returns:
        True if all thresholds met, False otherwise
    """
    y_pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)
    else:
        y_proba = None
        
    metrics = calculate_classification_metrics(y_test, y_pred, y_proba)
    
    passes = True
    for metric, min_val in thresholds.items():
        # Handle prefix mapping if needed, or assume thresholds match metric keys
        # The training function uses "test_accuracy", but calculate returns "accuracy" if no prefix
        # Let's try direct match first, then checks
        
        score = metrics.get(metric)
        if score is None:
             # Try checking with/without 'test_' prefix
             if metric.startswith('test_'):
                 score = metrics.get(metric.replace('test_', ''))
             else:
                 score = metrics.get(f"test_{metric}")
                 
        if score is None:
            logger.warning(f"Metric {metric} not found in calculated metrics")
            continue
            
        if score < min_val:
            logger.warning(f"Performance degradation: {metric} {score} < {min_val}")
            passes = False
        else:
            logger.info(f"Check passed: {metric} {score} >= {min_val}")
            
    return passes

class AdultRandomForestTrainer:
    """
    Manages the training, evaluation, and persistence of the Random Forest model for the Adult dataset.
    
    This class encapsulates the end-to-end pipeline for Experiment 1 model training. It includes
    data loading (handled internally via `load_adult`), model initialization, training execution,
    comprehensive metric calculation, feature importance extraction, and artifact persistence.
    
    Attributes:
        config (Dict[str, Any]): The full configuration dictionary.
        model_params (Dict[str, Any]): Model hyperparameters extracted from config.
        model (Optional[RandomForestClassifier]): The trained model instance.
        metrics (Dict[str, Any]): Dictionary of evaluation metrics.
        feature_names (List[str]): List of feature names matching the training data.
        
    Methods:
        train(force_retrain=False): Executes the training pipeline.
        evaluate(X_test, y_test): Performs model evaluation on new data.
        save(): Persists the trained model and metadata to disk.
        
    Example:
        >>> trainer = AdultRandomForestTrainer(config_path="config.json")
        >>> model, metrics = trainer.train()
        >>> trainer.save()
        
    Notes:
        - Relies on `src.data_loading.adult.load_adult` for data provision.
        - Caches models to `output_config['model_dir']` unless `force_retrain` is True.
        - Implements logic for EXP1-08.
    """
    def __init__(self, config_or_path: Any, verbose: bool = True):
        self.config_path = config_or_path if isinstance(config_or_path, (str, Path)) else None
        self.verbose = verbose
        self.model = None
        self.metrics = {}
        self.feature_names = []
        self.config = {}
        self.model_params = {}
        
        if isinstance(config_or_path, dict):
            self.config = config_or_path
            if 'model' in self.config and 'params' in self.config['model']:
                self.model_params = self.config['model']['params']
        else:
            self._load_config()
        
    def _load_config(self):
        """Load configuration from JSON or YAML file."""
        if not self.config_path:
             # Should not happen if logic in init is correct
             return

        if self.verbose:
            logger.info(f"Loading configuration from {self.config_path}")
            
        with open(self.config_path, 'r') as f:
            if str(self.config_path).endswith('.yaml') or str(self.config_path).endswith('.yml'):
                self.config = yaml.safe_load(f)
            else:
                self.config = json.load(f)
        self.model_params = self.config['model']['params']

    def train(self, X_train=None, y_train=None, X_test=None, y_test=None, force_retrain: bool = False) -> Tuple[RandomForestClassifier, Dict[str, Any]]:
        """
        Execute the full training pipeline.
        
        Args:
            X_train, y_train: Training data (optional).
            X_test, y_test: Testing data (optional).
            force_retrain (bool): Ignore existing models and force retraining.
            
        Returns:
            Tuple[RandomForestClassifier, Dict[str, Any]]: Trained model and metrics.
        """
        output_config = self.config['output']
        model_dir = Path(output_config['model_dir'])
        model_dir.mkdir(parents=True, exist_ok=True)
        results_dir = Path(output_config['results_dir'])
        results_dir.mkdir(parents=True, exist_ok=True)
        
        model_path = model_dir / output_config['model_filename']
        
        # Check for existing model
        if model_path.exists() and not force_retrain:
            if self.verbose:
                logger.info(f"Model already exists at {model_path}. Loading...")
            self.model = joblib.load(model_path)
            # Try to load existing metrics/feature names if possible, but simplest is empty dict return
            # The original function returned empty dict, so we maintain behavior
            return self.model, {}
            
        # Load Data if not provided
        if X_train is None or y_train is None:
            if self.verbose:
                logger.info("Loading Adult dataset...")
            data = load_adult(verbose=self.verbose)
            X_train, X_test, y_train, y_test = data[0], data[1], data[2], data[3]
            
            # Extract feature names
            f_names = data[4] if len(data) > 4 else []
            if isinstance(f_names, np.ndarray):
                f_names = f_names.tolist()
            self.feature_names = f_names
        elif self.feature_names == [] and isinstance(X_train, pd.DataFrame):
            # Try to capture feature names from dataframe if provided
            self.feature_names = X_train.columns.tolist()
        elif self.feature_names == []:
             # Fallback generic names
             self.feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]
        
        # Initialize
        if self.verbose:
            logger.info(f"Initializing Random Forest with params: {self.model_params}")
        self.model = RandomForestClassifier(**self.model_params)
        
        # Train
        if self.verbose:
            logger.info("Starting training...")
        start_time = time.time()
        self.model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        if self.verbose:
            logger.info(f"Training completed in {training_time:.2f} seconds")
            
        # Evaluate (Internal) - only if test data provided
        if X_test is not None and y_test is not None:
             self._evaluate_internal(X_test, y_test, X_train.shape, training_time, results_dir)
        
        # Save
        self.save()

        # Save Metrics to Results Dir
        metrics_filename = output_config.get('metrics_filename', 'rf_metrics.json')
        metrics_path = results_dir / metrics_filename
        with open(metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        if self.verbose:
            logger.info(f"Metrics saved to {metrics_path}")
        
        return self.model, self.metrics
        
    def _evaluate_internal(self, X_test, y_test, train_shape, training_time, results_dir):
        """Internal evaluation helper."""
        if self.verbose:
            logger.info("Evaluating model on test set...")
            
        y_pred = self.model.predict(X_test)
        
        if hasattr(self.model, "predict_proba"):
            y_proba_full = self.model.predict_proba(X_test)
        else:
            y_proba_full = None
            
        self.metrics = calculate_classification_metrics(y_test, y_pred, y_proba_full, prefix="test")
        
        # Feature Importance
        if hasattr(self.model, "feature_importances_"):
            # Validation of feature names length
            if len(self.feature_names) != train_shape[1]:
                logger.warning(f"Feature names count ({len(self.feature_names)}) != Input features ({train_shape[1]}). Generating generic names.")
                self.feature_names = [f"feature_{i}" for i in range(train_shape[1])]
            
            fi_df = get_feature_importance(
                self.model, 
                self.feature_names, 
                save_path=str(results_dir / "rf_feature_importance.csv")
            )
            self.metrics["top_10_features"] = fi_df.head(10)[['feature', 'importance']].to_dict('records')
            
        # Metadata
        self.metrics["training_metadata"] = {
            "training_time_seconds": round(training_time, 4),
            "model_params": self.model_params,
            "dataset_shape": train_shape,
            "n_features": train_shape[1],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Threshold Validation
        validation_config = self.config.get("validation", {})
        min_acc = validation_config.get("min_accuracy", 0.0)
        min_auc = validation_config.get("min_roc_auc", 0.0)
        
        current_acc = self.metrics.get("test_accuracy", 0.0)
        current_auc = self.metrics.get("test_roc_auc", 0.0)
        
        if current_acc < min_acc:
            logger.warning(f"Model accuracy {current_acc} below threshold {min_acc}")
        if current_auc is not None and current_auc < min_auc:
            logger.warning(f"Model ROC AUC {current_auc} below threshold {min_auc}")
            
        if self.verbose:
            logger.info(f"Test Accuracy: {current_acc}")
            logger.info(f"Test ROC AUC: {current_auc}")
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """External evaluation wrapper."""
        if self.model is None:
            raise RuntimeError("Model not trained yet.")
        y_pred = self.model.predict(X_test)
        # Update metrics state so it can be saved in metadata
        self.metrics = calculate_classification_metrics(y_test, y_pred)
        return self.metrics
        
    def save(self) -> str:
        """Persist model and metadata."""
        if self.model is None:
            raise RuntimeError("Nothing to save, model is None.")
            
        save_path = save_model_with_metadata(
            model=self.model,
            metrics=self.metrics,
            config=self.config,
            feature_names=self.feature_names
        )
        if self.verbose:
            logger.info(f"Model and metadata saved to {save_path}")
        return save_path

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Generate class predictions.
        
        Args:
            X: Input features.
            
        Returns:
            np.ndarray: Predicted class labels.
        """
        if self.model is None:
            raise RuntimeError("Model not trained yet.")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Generate class probabilities.
        
        Args:
            X: Input features.
            
        Returns:
            np.ndarray: Probability estimates.
        """
        if self.model is None:
            raise RuntimeError("Model not trained yet.")
        return self.model.predict_proba(X)

    def get_feature_importance(self) -> pd.DataFrame:
        """
        Extract feature importance.
        
        Returns:
            pd.DataFrame: DataFrame with feature importance.
        """
        if self.model is None:
            raise RuntimeError("Model not trained yet.")
        
        return get_feature_importance(self.model, self.feature_names)

def train_random_forest_adult(
    config_path: str = "experiments/exp1_adult/configs/models/rf_adult_config.yaml",
    force_retrain: bool = False,
    verbose: bool = True
) -> Tuple[RandomForestClassifier, Dict[str, Any]]:
    """
    Train Random Forest on Adult dataset.

    Args:
        config_path (str): Path to the JSON configuration file containing model
            hyperparameters and output paths. Defaults to standard experiment config.
        force_retrain (bool): If True, ignores existing saved models and forces
            a fresh training run. Defaults to False.
        verbose (bool): If True, logs detailed progress information to console/logger.
            Defaults to True.

    Returns:
        Tuple[RandomForestClassifier, Dict[str, Any]]:
            - trained_model: The fitted sklearn RandomForestClassifier.
            - metrics: Dictionary containing:
                - Performance scores (accuracy, roc_auc, etc.)
                - Confusion matrix stats
                - Training metadata (time, params, data shape)
                - Top 10 feature importances

    Raises:
        FileNotFoundError: If `config_path` does not exist or if dataset cannot be loaded.
        ValueError: If configuration is invalid or missing required keys.
        RuntimeError: If model training fails due to memory or data issues.

    Example:
        >>> from src.models.tabular_models import train_random_forest_adult
        >>> model, metrics = train_random_forest_adult(
        ...     config_path="config.json",
        ...     force_retrain=True
        ... )
        >>> # Typical Adult dataset shape after preprocessing:
        >>> # X_train shape: (32561, 108), X_test shape: (16281, 108)
        >>> print(metrics['training_metadata']['dataset_shape'])
        [32561, 108]

    Notes:
        - Uses caching: Checks for existing model at `output_config['model_path']`
          unless `force_retrain=True`.
        - Execution time: ~2-5 seconds for standard Adult dataset on modern CPU.
        - Implements EXP1-08 (RF Training Pipeline).
    """
    try:
        trainer = AdultRandomForestTrainer(config_path, verbose=verbose)
        return trainer.train(force_retrain=force_retrain)
    except Exception as e:
        logger.error(f"Error in train_random_forest_adult: {str(e)}")
        raise
