"""
Future Domain Stubs.

This module contains stub definitions for Vision and NLP models required by the Thesis.
They serve to validate that the BaseTrainer architecture is robust enough to handle
non-tabular data (Images, Text) and Deep Learning frameworks (Torch/TF) in future phases.
"""
from typing import Any, Dict
import numpy as np
from .base import BaseTrainer

class CNNTrainer(BaseTrainer):
    """
    Stub for Convolutional Neural Network (Vision).
    Target: MNIST / CIFAR-10 experiments.
    """
    def train(self, X_train: Any, y_train: Any, X_val: Any = None, y_val: Any = None):
        # In the future, this will handle 4D arrays (N, H, W, C)
        # and use PyTorch/TensorFlow DataLoaders.
        print("Mock: Training CNN on images...")
        self.model = "Trained_CNN_Model"
        return self

    def predict(self, X: Any) -> np.ndarray:
        return np.random.randint(0, 2, size=(len(X),))

    def predict_proba(self, X: Any) -> np.ndarray:
        return np.random.rand(len(X), 2)

class TransformerTrainer(BaseTrainer):
    """
    Stub for Transformer (NLP).
    Target: BERT/GPT for Text Classification (IMDb).
    """
    def train(self, X_train: Any, y_train: Any, X_val: Any = None, y_val: Any = None):
        # In the future, X_train will be List[str] or Token IDs.
        print("Mock: Training Transformer on text...")
        self.model = "Trained_BERT_Model"
        return self

    def predict(self, X: Any) -> np.ndarray:
        return np.random.randint(0, 2, size=(len(X),))
        
    def predict_proba(self, X: Any) -> np.ndarray:
        return np.random.rand(len(X), 2)
