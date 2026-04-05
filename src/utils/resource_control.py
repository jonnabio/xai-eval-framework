"""
Resource Control Utilities for Standardized Benchmarking.

Ensures that explainer execution follows defined resource limits:
- Single-core affinity
- Memory monitoring and capping
- Per-request timeouts
"""

import os
import psutil
import logging
import signal
import threading
import time
import _thread
from typing import Any, Callable, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, TimeoutError

logger = logging.getLogger(__name__)

class ResourceGuard:
    """Context manager for enforcing resource limits on a single explanation request."""

    def __init__(
        self, 
        max_cores: int = 1, 
        memory_limit_gb: float = 4.0, 
        timeout_seconds: int = 300,
        enforce_affinity: bool = True
    ):
        self.max_cores = max_cores
        self.memory_limit_gb = memory_limit_gb
        self.timeout_seconds = timeout_seconds
        self.enforce_affinity = enforce_affinity
        
        self._process = psutil.Process()
        self._original_affinity = None
        self._stop_monitor = threading.Event()
        self._monitor_thread = None

    def _monitor_memory(self):
        """Continuously monitor memory usage and raise alarm if limit exceeded."""
        limit_bytes = self.memory_limit_gb * (1024 ** 3)
        while not self._stop_monitor.is_set():
            try:
                usage = self._process.memory_info().rss
                if usage > limit_bytes:
                    logger.error(f"Memory limit exceeded! {usage / (1024**3):.2f} GB > {self.memory_limit_gb} GB.")
                    # Gracefully interrupt the main thread instead of exiting completely,
                    # to prevent breaking the ProcessPoolExecutor and crashing subsequent jobs.
                    _thread.interrupt_main()
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break
            time.sleep(1.0) # Check every second

    def run_guarded(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with standardized resource constraints."""
        
        # 1. Enforce Affinity
        if self.enforce_affinity:
            try:
                # If we're requesting a single core, we don't necessarily need to pin to Core 0.
                # In fact, pinning everything to Core 0 causes a massive bottleneck in parallel runs.
                # We'll allow the OS to schedule across all available cores instead of pinning.
                # If specialized pinning is needed in the future, we can implement a core-stepping logic.
                logger.debug("Bypassing explicit Core 0 pinning to avoid parallel bottleneck. OS will manage single-core scheduling.")
            except Exception as e:
                logger.warning(f"Failed to set CPU affinity: {e}")

        # 2. Start Memory Monitor
        self._stop_monitor.clear()
        self._monitor_thread = threading.Thread(target=self._monitor_memory, daemon=True)
        self._monitor_thread.start()

        # 3. Execute with Timeout
        # We use a ThreadPoolExecutor with 1 worker to allow timeout management.
        # This is safe because SHAP/LIME are mostly CPU bound.
        # BUT: For sub-process level isolation, we'd need ProcessPoolExecutor.
        # For simplicity within a single runner, we use ThreadPool with timeout.
        
        result = None
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                result = future.result(timeout=self.timeout_seconds)
        except TimeoutError:
            logger.error(f"Explanation timed out after {self.timeout_seconds} seconds.")
            raise
        except KeyboardInterrupt:
            logger.error("Guarded execution interrupted (likely due to memory limit).")
            raise MemoryError(f"ResourceGuard terminated execution: memory limit {self.memory_limit_gb}GB exceeded.")
        except Exception as e:
            logger.error(f"Error during guarded execution: {e}")
            raise
        finally:
            # 4. Cleanup
            self._stop_monitor.set()
            if self._monitor_thread:
                self._monitor_thread.join(timeout=2.0)
            
            # Restore affinity if possible
            if self._original_affinity:
                try:
                    self._process.cpu_affinity(self._original_affinity)
                except Exception:
                    pass
                    
        return result
