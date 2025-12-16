# User Story: EXP1-08
"""
Handles model training for XAI experiments.
This module provides functionality to train and evaluate tabular machine learning models,
specifically focusing on Random Forest and other tree-based ensembles used in XAI evaluation.
"""

import logging
import json
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
    metrics[f"{prefix}accuracy"] = round(accuracy_score(y_true, y_pred), 4)
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='macro', zero_division=0
    )
    metrics[f"{prefix}precision_macro"] = round(precision, 4)
    metrics[f"{prefix}recall_macro"] = round(recall, 4)
    metrics[f"{prefix}f1_macro"] = round(f1, 4)
    
    if y_proba is not None:
        try:
            # Handle binary vs multiclass
            if y_proba.ndim == 2 and y_proba.shape[1] == 2:
                # Binary case: use probability of positive class
                auc = roc_auc_score(y_true, y_proba[:, 1])
            else:
                # Multiclass case or 1D
                auc = roc_auc_score(y_true, y_proba, multi_class='ovr')
            metrics[f"{prefix}roc_auc"] = round(auc, 4)
        except Exception as e:
            logger.warning(f"Could not calculate ROC AUC: {e}")
            metrics[f"{prefix}roc_auc"] = None

    # 2. Confusion Matrix stats (Binary specific mainly, or flattened)
    cm = confusion_matrix(y_true, y_pred)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        total = np.sum(cm)
        metrics[f"{prefix}confusion_counts"] = {
            "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)
        }
        metrics[f"{prefix}confusion_percentages"] = {
            "tn": round(tn/total, 4), "fp": round(fp/total, 4),
            "fn": round(fn/total, 4), "tp": round(tp/total, 4)
        }
    
    # 3. Class Distribution
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
    importances = model.feature_importances_
    
    # Create DataFrame
    df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    })
    
    # Sort and rank
    df = df.sort_values('importance', ascending=False).reset_index(drop=True)
    df['rank'] = df.index + 1
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

def train_random_forest_adult(
    config_path: str = "experiments/exp1_adult/configs/models/rf_adult_config.json",
    force_retrain: bool = False,
    verbose: bool = True
) -> Tuple[RandomForestClassifier, Dict[str, Any]]:
    """
    Train Random Forest on Adult dataset.
    
    Args:
        config_path: Path to the JSON configuration file.
        force_retrain: If True, retrain model even if it already exists.
        verbose: If True, print training progress.
        
    Returns:
        Tuple containing (trained_model, metrics_dict)
    """
    try:
        # 1. Load config
        if verbose:
            logger.info(f"Loading configuration from {config_path}")
            
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        model_params = config['model']['params']
        output_config = config['output']
        
        # 2. Create output directories
        model_dir = Path(output_config['model_dir'])
        model_dir.mkdir(parents=True, exist_ok=True)
        
        results_dir = Path(output_config['results_dir'])
        results_dir.mkdir(parents=True, exist_ok=True)
        
        model_path = model_dir / output_config['model_filename']
        
        # 3. Check if model exists
        if model_path.exists() and not force_retrain:
            if verbose:
                logger.info(f"Model already exists at {model_path}. Loading...")
            model = joblib.load(model_path)
            return model, {}
            
        # 4 & 5. Load data
        if verbose:
            logger.info("Loading Adult dataset...")
            
        data = load_adult() 
        X_train, X_test, y_train, y_test = data[0], data[1], data[2], data[3]
        
        # 6. Initialize model
        if verbose:
            logger.info(f"Initializing Random Forest with params: {model_params}")
            
        model = RandomForestClassifier(**model_params)
        
        # 7. Train with timing
        if verbose:
            logger.info("Starting training...")
            
        start_time = time.time()
        model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        if verbose:
            logger.info(f"Training completed in {training_time:.2f} seconds")
            
        # 8. Evaluation
        if verbose:
            logger.info("Evaluating model on test set...")
            
        y_pred = model.predict(X_test)
        
        # Get probabilities (handle binary case)
        if hasattr(model, "predict_proba"):
            y_proba_full = model.predict_proba(X_test)
        else:
            y_proba_full = None
            
        # Calculate metrics
        metrics = calculate_classification_metrics(y_test, y_pred, y_proba_full, prefix="test")
        
        # 9. Feature Importance
        if hasattr(model, "feature_importances_"):
            feature_names = data[4] if len(data) > 4 else []
            if isinstance(feature_names, np.ndarray):
                feature_names = feature_names.tolist()
            
            # Ensure feature names match input dim
            if len(feature_names) != X_train.shape[1]:
                logger.warning(f"Feature names count ({len(feature_names)}) != Input features ({X_train.shape[1]}). Generating generic names.")
                feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]
            
            fi_df = get_feature_importance(
                model, 
                feature_names, 
                save_path=str(results_dir / "rf_feature_importance.csv")
            )
            
            # Add top 10 to metrics
            metrics["top_10_features"] = fi_df.head(10)[['feature', 'importance']].to_dict('records')
        
        # 10. Add metadata
        feature_names = data[4] if len(data) > 4 else []
        if isinstance(feature_names, np.ndarray):
            feature_names = feature_names.tolist()
            
        metrics["training_metadata"] = {
            "training_time_seconds": round(training_time, 4),
            "model_params": model_params,
            "dataset_shape": X_train.shape,
            "n_features": X_train.shape[1],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # 11. Validation
        validation_config = config.get("validation", {})
        min_acc = validation_config.get("min_accuracy", 0.0)
        min_auc = validation_config.get("min_roc_auc", 0.0)
        
        current_acc = metrics.get("test_accuracy", 0.0)
        current_auc = metrics.get("test_roc_auc", 0.0)
        
        if current_acc < min_acc:
            logger.warning(f"Model accuracy {current_acc} below threshold {min_acc}")
        if current_auc is not None and current_auc < min_auc:
            logger.warning(f"Model ROC AUC {current_auc} below threshold {min_auc}")
            
        if verbose:
            logger.info(f"Test Accuracy: {current_acc}")
            logger.info(f"Test ROC AUC: {current_auc}")

        # Save model using helper
        save_path = save_model_with_metadata(
            model=model,
            metrics=metrics,
            config=config,
            feature_names=feature_names
        )
        
        if verbose:
            logger.info(f"Model and metadata saved to {save_path}")
            
        return model, metrics

    except Exception as e:
        logger.error(f"Error in train_random_forest_adult: {str(e)}")
        raise
