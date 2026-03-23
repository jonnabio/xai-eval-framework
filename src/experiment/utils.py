import os
import multiprocessing

def get_default_workers() -> int:
    """Return the default number of worker processes.

    The function reads the ``DEFAULT_WORKERS`` environment variable (default ``6``).
    If set and positive, it is used directly. Otherwise it falls back to the
    ``RESERVED_CORES`` logic (default ``6``) to compute ``max(1, cpu_count - reserved)``.
    """
    # Preferred explicit default
    default_workers = int(os.getenv("DEFAULT_WORKERS", "6"))
    if default_workers > 0:
        return default_workers
    try:
        total_cpus = multiprocessing.cpu_count()
    except NotImplementedError:
        total_cpus = 1
    reserved = int(os.getenv("RESERVED_CORES", "6"))
    if reserved < 0:
        reserved = 0
    if reserved >= total_cpus:
        return 1
    return max(1, total_cpus - reserved)
