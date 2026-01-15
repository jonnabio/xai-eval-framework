"""
Model Trainer Factory.

This module implements the Factory Pattern for creating model trainer instances.
It allows the ExperimentRunner to request a model by string name (e.g., 'rf', 'svm')
without knowing the specific implementation class.
"""
import logging
from typing import Dict, Type, Any
from .base import BaseTrainer

logger = logging.getLogger(__name__)

class ModelTrainerFactory:
    """
    Factory for creating model trainer instances.
    
    Uses a registration mechanism to map model type strings to Trainer classes.
    """
    _registry: Dict[str, Type[BaseTrainer]] = {}

    @classmethod
    def register(cls, model_type: str, trainer_class: Type[BaseTrainer]):
        """
        Register a trainer class under a model type name.
        
        Args:
            model_type: String identifier (e.g., 'rf', 'svm').
            trainer_class: The class to instantiate (must inherit BaseTrainer).
        """
        cls._registry[model_type.lower()] = trainer_class
        logger.debug(f"Registered trainer '{model_type}' -> {trainer_class.__name__}")

    @classmethod
    def get_trainer(cls, model_type: str, config: Dict[str, Any] = None) -> BaseTrainer:
        """
        Create an instance of the requested trainer.
        
        Args:
            model_type: String identifier of the model.
            config: Configuration dictionary for the trainer.
            
        Returns:
            Instance of the requested BaseTrainer subclass.
            
        Raises:
            ValueError: If model_type is not registered.
        """
        if config is None:
            config = {}
            
        model_type = model_type.lower()
        trainer_class = cls._registry.get(model_type)
        
        if not trainer_class:
            valid_types = list(cls._registry.keys())
            raise ValueError(f"Unknown model type: '{model_type}'. Valid options: {valid_types}")
            
        return trainer_class(config)

    @classmethod
    def list_supported_models(cls):
        """Return list of registered model types."""
        return list(cls._registry.keys())

# Register Stubs (for architectural validation)
try:
    from .stubs import CNNTrainer, TransformerTrainer
    ModelTrainerFactory.register('cnn', CNNTrainer)
    ModelTrainerFactory.register('transformer', TransformerTrainer)
    ModelTrainerFactory.register('bert', TransformerTrainer)
except ImportError:
    pass # Stubs might not be needed in prod
