"""
Base Class for XAI Metrics.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
import numpy as np

class BaseMetric(ABC):
    """
    Abstract base class for all XAI evaluation metrics.
    """
    
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def compute(
        self,
        explanation: Any,
        model: Any = None,
        data: Optional[Union[np.ndarray, dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Compute the metric for a single explanation.

        Args:
            explanation: The explanation object (or dict) to evaluate.
            model: The black-box model (optional, needed for Fidelity).
            data: The instance data or context (optional).
            **kwargs: Additional arguments.

        Returns:
            Dictionary containing the metric value and metadata.
        """
        pass
