
import joblib
import logging
from pathlib import Path
from functools import lru_cache
from typing import Any

logger = logging.getLogger(__name__)

@lru_cache(maxsize=4)
def load_model(model_path: str) -> Any:
    """
    Load a model from disk with caching.
    
    Args:
        model_path: Absolute or relative path to the model file.
        
    Returns:
        The loaded model object.
    """
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
        
    logger.info(f"Loading model from disk: {model_path}")
    try:
        model = joblib.load(path)
        return model
    except Exception as e:
        logger.error(f"Failed to load model {model_path}: {e}")
        raise e
