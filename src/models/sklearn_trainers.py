"""
Sklearn-based Model Trainers.

This module contains trainer implementations for Scikit-Learn models:
- SVMTrainer (Support Vector Machine)
- MLPTrainer (Multi-Layer Perceptron)
- LogisticRegressionTrainer (Linear Baseline)
"""
import logging
from typing import Dict, Any
import numpy as np
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression

from .base import BaseTrainer
from .factory import ModelTrainerFactory

logger = logging.getLogger(__name__)

class SVMTrainer(BaseTrainer):
    """
    Support Vector Machine Trainer.
    
    Configuration Defaults:
    - kernel: 'rbf'
    - probability: True (Required for LIME/SHAP)
    - C: 1.0
    """
    def train(self, X_train, y_train, X_val=None, y_val=None):
        logger.info("Initializing SVM training...")
        
        # Merge defaults
        params = {
            'kernel': 'rbf',
            'probability': True, # Critical for XAI (predict_proba)
            'random_state': 42
        }
        params.update(self.config)
        
        self.model = SVC(**params)
        self.model.fit(X_train, y_train)
        
        # Capture feature names if available
        if hasattr(X_train, 'columns'):
            self.feature_names = X_train.columns.tolist()
            
        logger.info("SVM training completed.")
        return self

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)


class MLPTrainer(BaseTrainer):
    """
    Multi-Layer Perceptron (Neural Network) Trainer.
    
    Configuration Defaults:
    - hidden_layer_sizes: (100,)
    - activation: 'relu'
    - solver: 'adam'
    - max_iter: 200
    """
    def train(self, X_train, y_train, X_val=None, y_val=None):
        logger.info("Initializing MLP training...")
        
        params = {
            'hidden_layer_sizes': (100,),
            'activation': 'relu',
            'solver': 'adam',
            'random_state': 42,
            'max_iter': 500  # Increased default for convergence
        }
        params.update(self.config)
        
        self.model = MLPClassifier(**params)
        self.model.fit(X_train, y_train)
        
        if hasattr(X_train, 'columns'):
            self.feature_names = X_train.columns.tolist()
            
        logger.info("MLP training completed.")
        return self

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)


class LogisticRegressionTrainer(BaseTrainer):
    """
    Logistic Regression Trainer (Linear Baseline).
    """
    def train(self, X_train, y_train, X_val=None, y_val=None):
        logger.info("Initializing Logistic Regression training...")
        
        params = {
            'solver': 'lbfgs',
            'max_iter': 1000,
            'random_state': 42
        }
        params.update(self.config)
        
        self.model = LogisticRegression(**params)
        self.model.fit(X_train, y_train)
        
        if hasattr(X_train, 'columns'):
            self.feature_names = X_train.columns.tolist()
            
        logger.info("Logistic Regression training completed.")
        return self

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)


# Register trainers with Factory
ModelTrainerFactory.register('svm', SVMTrainer)
ModelTrainerFactory.register('mlp', MLPTrainer)
ModelTrainerFactory.register('logreg', LogisticRegressionTrainer)
