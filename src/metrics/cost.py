"""
Cost (Efficiency) Metric.
"""
import time
from typing import Any, Dict, Optional, Union
import numpy as np
from .base import BaseMetric

class CostMetric(BaseMetric):
    """
    Measures the computational cost of generating an explanation.
    captures wall-clock time and optionally estimates energy usage.
    """

    def __init__(self):
        super().__init__(name="Cost")
        self.start_time = None

    def __enter__(self):
        """Context manager start."""
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager end - not used directly for calculation."""
        pass

    def measure(self, generation_func, *args, **kwargs) -> Dict[str, float]:
        """
        Measure time taken to execute a function.

        Args:
            generation_func: The function to generate explanations.
            *args, **kwargs: Arguments for the function.

        Returns:
            Result of function and metrics dict.
        """
        start = time.perf_counter()
        result = generation_func(*args, **kwargs)
        end = time.perf_counter()
        
        duration_ms = (end - start) * 1000.0
        
        metrics = {
            "time_ms": duration_ms,
            "seconds": duration_ms / 1000.0
        }
        return result, metrics

    def compute(
        self,
        explanation: Any,
        model: Any = None,
        data: Optional[Union[np.ndarray, dict]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Compute cost from existing metadata if available.
        Expected metadata format: {'total_time_seconds': float}
        """
        if isinstance(explanation, dict) and 'metadata' in explanation:
            meta = explanation['metadata']
            if 'total_time_seconds' in meta:
                return {
                    "time_ms": meta['total_time_seconds'] * 1000.0,
                    "seconds": meta['total_time_seconds']
                }
        
        # If not in metadata, return -1 (unknown)
        return {"time_ms": -1.0, "seconds": -1.0}
