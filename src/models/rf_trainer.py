"""
Random Forest Trainer.

This module contains the Random Forest implementation inheriting from BaseTrainer.
It mirrors the logic of the legacy AdultRandomForestTrainer but fits the new architecture.
"""
import logging
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from .base import BaseTrainer
from .factory import ModelTrainerFactory

logger = logging.getLogger(__name__)

class RandomForestTrainer(BaseTrainer):
    """
    Random Forest Trainer.
    
    Configuration Defaults:
    - n_estimators: 100
    - max_depth: None
    - criterion: 'gini'
    """
    def train(self, X_train, y_train, X_val=None, y_val=None):
        logger.info("Initializing Random Forest training...")
        
        # Merge defaults
        params = {
            'n_estimators': 100,
            'max_depth': None,
            'random_state': 42,
            'n_jobs': -1
        }
        params.update(self.config)
        
        self.model = RandomForestClassifier(**params)
        self.model.fit(X_train, y_train)
        
        # Capture feature names if available
        if hasattr(X_train, 'columns'):
            self.feature_names = X_train.columns.tolist()
        elif self.feature_names is None:
             self.feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]
            
        logger.info("Random Forest training completed.")
        return self

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)
        
    def get_feature_importance(self) -> pd.DataFrame:
        """Extract feature importance."""
        if self.model is None:
            raise ValueError("Model not trained.")
            
        importances = self.model.feature_importances_
        df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        return df

# Register
ModelTrainerFactory.register('rf', RandomForestTrainer)
ModelTrainerFactory.register('random_forest', RandomForestTrainer)
