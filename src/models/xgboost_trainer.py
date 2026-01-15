"""
XGBoost Trainer.

Refactored to inherit from BaseTrainer.
"""
import logging
import pandas as pd
import numpy as np
import xgboost as xgb
from typing import Dict, Any

from .base import BaseTrainer
from .factory import ModelTrainerFactory

logger = logging.getLogger(__name__)

class XGBoostTrainer(BaseTrainer):
    """
    XGBoost Trainer (Refactored).
    """
    def train(self, X_train, y_train, X_val=None, y_val=None):
        logger.info("Initializing XGBoost training...")
        
        # Defaults
        defaults = {
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'objective': 'binary:logistic',
            'eval_metric': 'logloss',
            'random_state': 42,
            'n_jobs': -1,
            'use_label_encoder': False,
            'verbosity': 0
        }
        # Merge config
        train_config = {**defaults, **self.config}
        
        # Early stopping logic
        fit_params = {}
        if X_val is not None and y_val is not None:
             # XGBoost >= 1.6 puts early_stopping_rounds in constructor
             train_config['early_stopping_rounds'] = 10
             fit_params['eval_set'] = [(X_val, y_val)]
             fit_params['verbose'] = False
             
        self.model = xgb.XGBClassifier(**train_config)
        self.model.fit(X_train, y_train, **fit_params)
        
        if hasattr(X_train, 'columns'):
            self.feature_names = X_train.columns.tolist()
        elif self.feature_names is None:
             self.feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]
             
        logger.info("XGBoost training completed.")
        return self

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)
        
    def get_feature_importance(self) -> pd.DataFrame:
        if self.model is None:
            raise ValueError("Model not trained.")
        
        # Use weight/gain depending on config or default to gain
        imp_type = self.config.get('importance_type', 'gain')
        importance_map = self.model.get_booster().get_score(importance_type=imp_type)
        
        data = []
        for feat in self.feature_names:
            score = importance_map.get(feat, 0.0)
            data.append({'feature': feat, 'importance': float(score)})
            
        return pd.DataFrame(data).sort_values('importance', ascending=False)

# Register
ModelTrainerFactory.register('xgb', XGBoostTrainer)
ModelTrainerFactory.register('xgboost', XGBoostTrainer)
