
import logging
import time
from pathlib import Path
from src.utils.model_loader import load_model, get_cache_stats, clear_model_cache
import joblib
import numpy as np

# Setup dummy model
class DummyModel:
    def predict(self, X):
        return np.zeros(len(X))

def create_dummy_model(path: Path):
    model = DummyModel()
    joblib.dump(model, path)
    return path

def verify_caching():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("VerifyCaching")
    
    dummy_path = Path("dummy_model.joblib")
    create_dummy_model(dummy_path)
    
    try:
        clear_model_cache()
        logger.info("Cache cleared.")
        
        # 1. First Load (Cold)
        start = time.perf_counter()
        m1 = load_model(str(dummy_path))
        t1 = (time.perf_counter() - start) * 1000
        logger.info(f"First load time: {t1:.2f}ms")
        
        # 2. Second Load (Warm)
        start = time.perf_counter()
        m2 = load_model(str(dummy_path))
        t2 = (time.perf_counter() - start) * 1000
        logger.info(f"Second load time: {t2:.2f}ms")
        
        assert m1 is m2, "Loaded objects should be identical (same reference)"
        assert t2 < 1.0, f"Warm load took too long: {t2:.2f}ms"
        
        stats = get_cache_stats()
        logger.info(f"Cache stats: {stats}")
        assert stats.hits >= 1, "Expected at least 1 cache hit"
        
        logger.info("✅ Basic Caching Verified Sucessfully")
        
    finally:
        if dummy_path.exists():
            dummy_path.unlink()

if __name__ == "__main__":
    verify_caching()
