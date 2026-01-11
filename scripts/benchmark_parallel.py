
import logging
import time
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import patch
from src.experiment.runner import ExperimentRunner
from src.experiment.config import ExperimentConfig, ModelConfig, ExplainerConfig, MetricsConfig, SamplingConfig

# Mock classes to avoid full dependencies/data loading if possible, 
# or use existing ones if fast enough. 
# We'll rely on the real Runner but use a small config.

def dummy_load_adult(*args, **kwargs):
    """Return dummy data matching the benchmark model (20 features)."""
    n_samples = 100
    n_features = 20
    X = np.random.rand(n_samples, n_features)
    y = np.random.randint(0, 2, size=n_samples)
    feature_names = [f"feat_{i}" for i in range(n_features)]
    class_names = ["Class0", "Class1"]
    return X, X, y, y, feature_names, class_names

def run_benchmark():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Benchmark")
    
    # Needs a real model file for the runner to load
    # We can rely on the dummy model from verify_caching or create one
    import joblib
    dummy_path = Path("benchmark_model.joblib")
    # Always recreate to be safe
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification
    # Ensure 20 features to match our dummy loader
    X, y = make_classification(n_samples=100, n_features=20)
    model = RandomForestClassifier(n_estimators=10).fit(X, y)
    joblib.dump(model, dummy_path)
    
    # Config
    base_config = ExperimentConfig(
        name="benchmark_parallel",
        dataset="adult", 
        model=ModelConfig(name="rf", path=dummy_path),
        explainer=ExplainerConfig(method="lime", num_samples=10, params={}), # Fast
        sampling=SamplingConfig(samples_per_class=2), 
        metrics=MetricsConfig(fidelity=True, stability=False),
        output_dir=Path("outputs/benchmark")
    )
    
    # Patch the data loader
    with patch('src.experiment.runner.load_adult', side_effect=dummy_load_adult):
        
        # Cleanup any previous artifacts
        result_file = base_config.output_dir / "results.json"
        if result_file.exists():
            result_file.unlink()
            
        # 1. Sequential (max_workers=1)
        base_config.max_workers = 1
        runner_seq = ExperimentRunner(base_config)
        
        logger.info("Running Sequential Benchmark...")
        start_seq = time.perf_counter()
        try:
            res_seq = runner_seq.run()
        except Exception as e:
            logger.error(f"Sequential run failed: {e}", exc_info=True)
            return

        dur_seq = time.perf_counter() - start_seq
        logger.info(f"Sequential Time: {dur_seq:.2f}s")
        
        # Cleanup results from seq run
        result_file = base_config.output_dir / "results.json"
        if result_file.exists():
            result_file.unlink()
        
        # 2. Parallel (max_workers=2)
        base_config.max_workers = 2
        # Force reload of runner to reset state
        runner_par = ExperimentRunner(base_config)
        
        logger.info("Running Parallel Benchmark (2 workers)...")
        start_par = time.perf_counter()
        try:
            res_par = runner_par.run()
        except Exception as e:
            logger.error(f"Parallel run failed: {e}", exc_info=True)
            return

        dur_par = time.perf_counter() - start_par
        logger.info(f"Parallel Time (2 workers): {dur_par:.2f}s")
        
        speedup = dur_seq / dur_par if dur_par > 0 else 0
        logger.info(f"Speedup: {speedup:.2f}x")
        
        # Validate consistency (check number of results)
        count_seq = len(res_seq.get('instance_evaluations', []))
        count_par = len(res_par.get('instance_evaluations', []))
        
        logger.info(f"Evaluated Items: Seq={count_seq}, Par={count_par}")
        assert count_seq == count_par, "Result counts differ!"
        assert count_seq > 0, "No instances evaluated!"

    # Cleanup
    if dummy_path.exists():
        dummy_path.unlink()

if __name__ == "__main__":
    run_benchmark()
