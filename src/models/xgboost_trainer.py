"""
XGBoost classifier training for XAI evaluation experiments.

This module provides the `XGBoostTrainer` class, designed to facilitate the training,
evaluation, and persistence of XGBoost models for Experiment 1 (Adult Dataset).
It serves as a high-performance, non-linear baseline to compare against Random Forest
interpretability.

The framework ensures reproducibility through fixed seeds and standardized metrics,
making it suitable for rigorous academic evaluation of XAI methods (LIME, SHAP).

Key Classes:
    XGBoostTrainer: Wrapper for XGBClassifier managing the full experiment lifecycle.

Examples:
    >>> from src.models.xgboost_trainer import XGBoostTrainer
    >>> from src.data_loading.adult import load_adult
    >>> 
    >>> # 1. Load Data
    >>> X_train, X_test, y_train, y_test = load_adult()
    >>>
    >>> # 2. Initialize Trainer
    >>> trainer = XGBoostTrainer(config={'n_estimators': 100, 'max_depth': 6})
    >>>
    >>> # 3. Train
    >>> trainer.train(X_train, y_train, X_val=X_test, y_val=y_test)
    >>>
    >>> # 4. Evaluate
    >>> metrics = trainer.evaluate(X_test, y_test)
    >>> print(metrics['accuracy'])
    >>>
    >>> # 5. Save
    >>> trainer.save(path="experiments/exp1_adult/models")

References:
    Experiment Documentation: experiments/exp1_adult/README.md
"""
from pathlib import Path
from typing import Dict, Any, Optional

import xgboost as xgb
import sklearn.metrics as metrics
import numpy as np
import pandas as pd
import json
import logging
import joblib

import time

logger = logging.getLogger(__name__)

class XGBoostTrainer:
    """
    XGBoost classifier trainer for UCI Adult dataset.

    This class serves as the Gradient Boosting baseline for Experiment 1, contrasting with
    the Random Forest model (`AdultRandomForestTrainer`). It is designed to evaluate
    the fidelity of XAI methods (LIME, SHAP) on non-linear, high-performance models.

    The trainer handles hyperparameter management, training mechanics (including
    early stopping), comprehensive metric tracking, and artifact persistence.

    Attributes:
        model (xgb.XGBClassifier): The underlying XGBoost model instance.
        config (dict): Configuration dictionary including hyperparameters.
        metrics (dict): Performance metrics after evaluation (accuracy, AUC, etc.).
        feature_names (list): List of feature names corresponding to input columns.

    Methods:
        train: Fits the model with optional early stopping validation.
        evaluate: Computes classification metrics on a test set.
        get_feature_importance: Extracts feature importance (e.g., gain, weight).
        save: Persists model, metrics, and metadata to disk.
        load: Class method to restore a trained model from disk.
        predict: Generates class labels.
        predict_proba: Generates class probabilities.

    Examples:
        >>> trainer = XGBoostTrainer(config={'n_estimators': 100})
        >>> trainer.train(X_train, y_train, X_val=X_val, y_val=y_val)
        >>> metrics = trainer.evaluate(X_test, y_test)

    Notes:
        Early Stopping: If `X_val` and `y_val` are provided to `train()`, early stopping
        is enabled with rounds=10 to prevent overfitting, which is more critical for 
        boosting models than for bagging models like Random Forest.

    Related:
        src.models.tabular_models.AdultRandomForestTrainer
    """
    def __init__(self, config: dict = None):
        """
        Initialize the XGBoostTrainer with configuration.

        Args:
            config (dict, optional): Dictionary of hyperparameters to override defaults.
                Defaults merged with:
                - n_estimators: 100
                - max_depth: 6
                - learning_rate: 0.1
                - objective: 'binary:logistic'

        Example:
            >>> trainer = XGBoostTrainer({'n_estimators': 200, 'learning_rate': 0.05})

        Notes:
            Implements config merging strategy defined in EXP1-09.
        """
        # Default configuration (Baseline for Adult dataset)
        # See ADR-004 for hyperparameter justification
        self.defaults = {
            'n_estimators': 100,            # Match RF baseline
            'max_depth': 6,                 # XGB default (shallower than RF to avoid overfitting)
            'learning_rate': 0.1,           # Standard robust default
            'objective': 'binary:logistic', # Standard for binary classification
            'eval_metric': 'logloss',       # Optimal for probability calibration
            'random_state': 42,             # Reproducibility
            # Performance: Use all available cores. XGBoost parallelization is very efficient.
            # Expect ~2x faster training than sklearn RF for same n_estimators due to optimizations.
            'n_jobs': -1,                   # Use all cores
            'verbosity': 0,                 # Silence XGBoost internal logs
            'use_label_encoder': False      # Deprecated in newer XGBoost versions
        }
        
        # Merge defaults with user config
        if config is None:
            self.config = self.defaults.copy()
        else:
            self.config = {**self.defaults, **config}
            
        # Initialize attributes
        self.model = None
        self.metrics = {}
        self.feature_names = None
        
        logger.debug(f"Initialized XGBoostTrainer with config: {self.config}")

    def train(self, X_train, y_train, X_val=None, y_val=None) -> 'XGBoostTrainer':
        """
        Train the XGBoost model.

        Args:
            X_train (pd.DataFrame or np.ndarray): Training features.
            y_train (pd.Series or np.ndarray): Training labels.
            X_val (pd.DataFrame or np.ndarray, optional): Validation features for early stopping.
            y_val (pd.Series or np.ndarray, optional): Validation labels.

        Returns:
            XGBoostTrainer: Self instance for method chaining.

        Raises:
            Exception: If training fails (e.g., data mismatch).

        Example:
            >>> trainer.train(X_train, y_train, X_val=X_test, y_val=y_test)

        Notes:
            Enables early stopping (rounds=10) if validation data is provided.
            Captures feature names from DataFrame columns if available.
        """
        logger.info("Initializing XGBoost training...")
        
        # 1. Capture feature names
        if isinstance(X_train, pd.DataFrame):
            self.feature_names = X_train.columns.tolist()
        else:
            # Fallback for numpy arrays
            self.feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]
            
        # 2. Update config 'scale_pos_weight' if not explicit, could do it here,
        # but for now we rely on the config passed in init.
        
        # 3. Create Classifier
        # Prepare config with early checking (XGBoost >= 1.6 requires it in init)
        train_config = self.config.copy()
        if X_val is not None and y_val is not None:
            train_config['early_stopping_rounds'] = 10
            
        self.model = xgb.XGBClassifier(**train_config)
        
        # 4. Prepare fit arguments
        fit_params = {}
        if X_val is not None and y_val is not None:
            fit_params['eval_set'] = [(X_val, y_val)]
            fit_params['verbose'] = False # Keep logs clean unless requested
            
        # 5. Train
        try:
            # Memory: XGBoost uses a compressed histogram-based algorithm (DMatrix) internally.
            # For 48k rows (Adult), this is very memory efficient (<100MB RAM typically).
            self.model.fit(X_train, y_train, **fit_params)
            logger.info("XGBoost training completed successfully.")
        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise e
            
        return self

    def evaluate(self, X_test, y_test) -> dict:
        """
        Evaluate model performance on test dataset.

        Args:
            X_test (pd.DataFrame or np.ndarray): Test features.
            y_test (pd.Series or np.ndarray): True test labels.

        Returns:
            dict: Dictionary containing:
                - accuracy (float)
                - precision (float, weighted)
                - recall (float, weighted)
                - f1 (float, weighted)
                - roc_auc (float)
                - confusion_matrix (list[list])

        Raises:
            ValueError: If model is not trained.

        Example:
            >>> metrics = trainer.evaluate(X_test, y_test)
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
            
        logger.info("Evaluating model performance...")
        
        # Predictions
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate Metrics
        self.metrics = {
            "accuracy": float(metrics.accuracy_score(y_test, y_pred)),
            # Weighted average used due to potential imbalance, though 'binary' is standard.
            # Keeping consistent with RF trainer metrics.
            "precision": float(metrics.precision_score(y_test, y_pred, average='weighted', zero_division=0)),
            "recall": float(metrics.recall_score(y_test, y_pred, average='weighted', zero_division=0)),
            "f1": float(metrics.f1_score(y_test, y_pred, average='weighted', zero_division=0)),
            "roc_auc": float(metrics.roc_auc_score(y_test, y_prob)) if y_prob is not None else None,
            "confusion_matrix": metrics.confusion_matrix(y_test, y_pred).tolist()
        }
        
        logger.info(f"Evaluation Metrics: {json.dumps(self.metrics, indent=2)}")
        return self.metrics

    def get_feature_importance(self, importance_type='gain') -> pd.DataFrame:
        """
        Extract and rank feature importance.

        Args:
            importance_type (str): XGBoost importance type ('gain', 'weight', 'cover'). 
                Default 'gain'.

        Returns:
            pd.DataFrame: DataFrame with columns ['feature', 'importance', 'rank'],
                sorted by importance descending.

        Raises:
            ValueError: If model is not trained.

        Example:
            >>> df_imp = trainer.get_feature_importance('weight')
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
            
        # Extract importance from booster
        # importance_type options: 'weight', 'gain', 'cover', 'total_gain', 'total_cover'
        importance_map = self.model.get_booster().get_score(importance_type=importance_type)
        
        # Map to all features (ensure 0 for unused features)
        # We iterate over self.feature_names to ensure we include all features, 
        # even those with 0 importance (which XGBoost omits from the dict).
        data = []
        for feat in self.feature_names:
            score = importance_map.get(feat, 0.0)
            data.append({'feature': feat, 'importance': float(score)})
            
        df = pd.DataFrame(data)
        
        # Sort by importance descending
        df = df.sort_values(by='importance', ascending=False).reset_index(drop=True)
        
        # Add rank
        df['rank'] = df.index + 1
        
        return df

    def save(self, path: Path) -> None:
        """
        Persist model and artifacts to disk.

        Args:
            path (Path): Directory path to save artifacts.

        Artifacts:
            - xgb_model.pkl: Pickled model (joblib)
            - xgb_metrics.json: Metrics dictionary
            - xgb_feature_importance.csv: Importance data
            - xgb_model_metadata.json: Config and environment details

        Raises:
            ValueError: If model is not trained.
            Exception: If file I/O fails.

        Example:
            >>> trainer.save(Path("experiments/exp1/models"))
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
            
        save_dir = Path(path)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # 1. Save Model
            model_path = save_dir / "xgb_model.pkl"
            joblib.dump(self.model, model_path)
            
            # 2. Save Metrics
            metrics_path = save_dir / "xgb_metrics.json"
            with open(metrics_path, 'w') as f:
                json.dump(self.metrics, f, indent=2)
                
            # 3. Save Feature Importance
            importance_path = save_dir / "xgb_feature_importance.csv"
            imp_df = self.get_feature_importance()
            imp_df.to_csv(importance_path, index=False)
            
            # 4. Save Metadata
            metadata = {
                "model_type": "XGBClassifier",
                "training_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "config": self.config,
                "feature_names": self.feature_names,
                "xgb_version": xgb.__version__,
                "metrics": self.metrics
            }
            metadata_path = save_dir / "xgb_model_metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
            logger.info(f"Model artifacts saved to {save_dir}")
            logger.debug(f"Saved: {model_path.name}, {metrics_path.name}, {importance_path.name}, {metadata_path.name}")
            
        except Exception as e:
            logger.error(f"Failed to save model artifacts: {e}")
            raise e

    @classmethod
    def load(cls, path: Path) -> 'XGBoostTrainer':
        """
        Load a trained trainer from disk.

        Args:
            path (Path): Directory containing saved artifacts.

        Returns:
            XGBoostTrainer: Initialized trainer with loaded model and config.

        Raises:
            FileNotFoundError: If xgb_model.pkl is missing.

        Example:
            >>> trainer = XGBoostTrainer.load(Path("experiments/exp1/models"))
        """
        path = Path(path)
        model_path = path / "xgb_model.pkl"
        metadata_path = path / "xgb_model_metadata.json"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
            
        # Load metadata for config
        config = {}
        feature_names = None
        metrics = {}
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                config = metadata.get('config', {})
                feature_names = metadata.get('feature_names')
                metrics = metadata.get('metrics', {})
                
        # Initialize
        trainer = cls(config)
        trainer.model = joblib.load(model_path)
        trainer.feature_names = feature_names
        trainer.metrics = metrics
        
        logger.info(f"Loaded XGBoostTrainer from {path}")
        return trainer

    def predict(self, X) -> np.ndarray:
        """
        Generate class predictions.

        Args:
            X: Input features.

        Returns:
            np.ndarray: Predicted class labels (0/1).
            
        Raises:
            ValueError: If model is not trained.
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
        preds = self.model.predict(X)
        logger.debug(f"Generated {len(preds)} predictions.")
        return preds

    def predict_proba(self, X) -> np.ndarray:
        """
        Generate class probabilities.

        Args:
            X: Input features.

        Returns:
            np.ndarray: Probability estimates. Columns correspond to classes.
            
        Raises:
            ValueError: If model is not trained.
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
        probs = self.model.predict_proba(X)
        logger.debug(f"Generated {len(probs)} probability estimates.")
        return probs

