"""
Experiment orchestration and execution.

Coordinates model loading, explanation generation, metric evaluation,
and result persistence for XAI evaluation experiments.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import numpy as np
import pandas as pd
import joblib

from src.experiment.config import ExperimentConfig
from src.data_loading.adult import load_adult
from src.xai.shap_tabular import SHAPTabularWrapper
from src.xai.lime_tabular import LIMETabularWrapper
from src.evaluation.sampler import EvaluationSampler
from src.metrics import FidelityMetric, StabilityMetric, SparsityMetric, CostMetric

logger = logging.getLogger(__name__)

class ExperimentRunner:
    """
    Orchestrates end-to-end XAI evaluation experiments.
    """
    
    def __init__(self, config: ExperimentConfig):
        """
        Initialize experiment runner with configuration.
        """
        self.config = config
        self.dataset = None
        self.model = None
        self.explainer = None
        self.results = {
            "experiment_metadata": {},
            "model_info": {},
            "instance_evaluations": []
        }
        
        # Set random seed
        np.random.seed(config.random_seed)
        
        # Ensure output directory exists
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        
    def setup(self) -> None:
        """
        Load dataset, model, and initialize explainer.
        """
        logger.info("Setting up experiment environment...")
        
        # 1. Load Dataset
        logger.info(f"Loading dataset: {self.config.dataset}")
        if self.config.dataset == "adult":
            # Using existing loader
            # Point to 'data' dir relative to where this usually runs? 
            # Ideally config should specify data root or we infer.
            # Assuming project root structure.
            # Using defaults for now, assuming standard project layout.
            data_dir = str(Path("data").resolve()) 
            # If path mismatch, user needs to ensure data is there.
            
            # Unpack tuple from load_adult
            X_train, X_test, y_train, y_test, feature_names, _ = load_adult(
                cache_dir=data_dir, 
                random_state=self.config.random_seed
            )
            
            self.dataset = {
                'X_train': X_train,
                'X_test': X_test,
                'y_train': y_train,
                'y_test': y_test,
                'feature_names': feature_names
            }
        else:
            raise ValueError(f"Unsupported dataset: {self.config.dataset}")
        
        # 2. Load Model
        logger.info(f"Loading model from: {self.config.model.path}")
        if not self.config.model.path.exists():
             raise FileNotFoundError(f"Model not found at {self.config.model.path}")
        
        # Assuming joblib load works for both RF and XGB as implemented in EXP1-10
        self.model = joblib.load(self.config.model.path)
        
        # 3. Initialize Explainer
        logger.info(f"Initializing {self.config.explainer.method.upper()} explainer")
        
        if self.config.explainer.method == "shap":
            # Map 'tree'/'kernel' to wrapper 'model_type'
            model_type = self.config.explainer.explainer_type or "tree"
            
            self.explainer = SHAPTabularWrapper(
                model=self.model,
                training_data=self.dataset['X_train'],
                feature_names=self.dataset['feature_names'],
                model_type=model_type,
                n_background_samples=100, # Default or from params?
                **self.config.explainer.params
            )
        elif self.config.explainer.method == "lime":
            self.explainer = LIMETabularWrapper(
                training_data=self.dataset['X_train'],
                feature_names=self.dataset['feature_names'],
                class_names=self.dataset.get('class_names', ['<=50K', '>50K']),
                num_features=self.config.explainer.num_features or 10,
                num_samples=self.config.explainer.num_samples or 1000,
                random_state=self.config.random_seed
                # mode='classification' is default for wrapper
            )
        else:
            raise ValueError(f"Unsupported explainer: {self.config.explainer.method}")
        
        logger.info("Setup complete")
        
    def generate_instances(self) -> pd.DataFrame:
        """
        Generate evaluation instances using configured sampling strategy.
        """
        logger.info("Generating evaluation instances...")
        
        if self.config.sampling.strategy == "stratified":
            sampler = EvaluationSampler(
                model=self.model,
                X_test=self.dataset['X_test'],
                y_test=self.dataset['y_test'],
                random_state=self.config.sampling.random_seed
            )
            instances = sampler.sample_stratified_by_error(
                n_per_group=self.config.sampling.samples_per_class
            )
        else:
            raise ValueError(f"Unsupported sampling strategy: {self.config.sampling.strategy}")
        
        logger.info(f"Generated {len(instances)} evaluation instances")
        return instances
        
    def evaluate_instance(
        self,
        instance_row: pd.Series,
        idx: int,
        total: int
    ) -> Dict[str, Any]:
        """
        Evaluate a single instance.
        """
        if (idx + 1) % 10 == 0:
            logger.info(f"Processing instance {idx+1}/{total}...")
        
        # Prepare Data
        # Metadata cols from sampler output
        meta_cols = ['original_index', 'target', 'prediction', 'quadrant']
        # Extract features as numpy array
        instance_data = instance_row.drop(labels=meta_cols).values.astype(float)
        
        # Get feature names for explanation context
        feature_names = self.dataset['feature_names']
        
        # 1. Generate Explanation & Measure Cost
        # Wrapper .explain_instance returns (weights, metadata)
        # We need raw weights for metrics
        
        cost_metric = CostMetric()
        # Measure generation
        (weights, meta), time_metrics = cost_metric.measure(
            self.explainer.explain_instance,
            self.model,
            instance_data,
            return_full=True
        )
        
        metrics_results = {}
        
        # 2. Compute Metrics
        
        # COST
        if self.config.metrics.cost:
            metrics_results['cost'] = time_metrics['time_ms'] # ms
            
        # SPARSITY
        if self.config.metrics.sparsity:
            sparsity_m = SparsityMetric() # Default threshold
            res = sparsity_m.compute(weights)
            metrics_results['sparsity'] = res['nonzero_percentage']
            
        # FIDELITY
        if self.config.metrics.fidelity:
            fidelity_m = FidelityMetric() # Default params
            res = fidelity_m.compute(weights, model=self.model, data=instance_data)
            metrics_results['fidelity'] = res['r2_score']
            
        # STABILITY
        if self.config.metrics.stability:
             # Define helper for regeneration
             def explainer_func(m, d):
                 w_full = self.explainer.explain_instance(m, d[0], return_full=False)
                 return {'feature_importance': w_full}
             
             stability_m = StabilityMetric(
                 n_iterations=self.config.metrics.stability_perturbations,
                 perturbation_std=self.config.metrics.stability_noise_level
             )
             
             res = stability_m.compute(
                 None, 
                 model=self.model, 
                 data=instance_data,
                 explainer_func=explainer_func
             )
             metrics_results['stability'] = res['cosine_similarity_mean']
        
        # Construct Result
        return {
            "instance_id": int(instance_row['original_index']),
            "quadrant": instance_row['quadrant'],
            "true_label": int(instance_row['target']),
            "prediction": int(instance_row['prediction']),
            "prediction_correct": int(instance_row['target']) == int(instance_row['prediction']),
            "metrics": metrics_results,
            "metrics": metrics_results,
            "explanation": self._format_explanation(weights, feature_names)
        }
        
    def _format_explanation(self, weights: np.ndarray, feature_names: List[str], top_k: int = 10) -> Dict[str, Any]:
        """Format explanation for storage/LLM context."""
        # Pair weights with names
        exp_list = []
        for i, w in enumerate(weights):
            if i < len(feature_names):
                exp_list.append((feature_names[i], float(w)))
        
        # Sort by absolute magnitude
        exp_list.sort(key=lambda x: abs(x[1]), reverse=True)
        
        # Take top k
        top_features = exp_list[:top_k]
        
        return {
            "top_features": [f"{name}: {val:.4f}" for name, val in top_features],
            "raw_top": {name: val for name, val in top_features}
        }
        
    def run(self) -> Dict[str, Any]:
        """
        Execute complete experiment workflow.
        """
        start_time = datetime.now()
        logger.info(f"Starting experiment: {self.config.name}")
        
        try:
            self.setup()
            
            instances = self.generate_instances()
            
            # Metadata
            self.results["experiment_metadata"] = {
                "name": self.config.name,
                "dataset": self.config.dataset,
                "timestamp": start_time.isoformat(),
                "config_version": self.config.version,
                "random_seed": self.config.random_seed
            }
            
            self.results["model_info"] = {
                "name": self.config.model.name,
                "path": str(self.config.model.path),
                "explainer_method": self.config.explainer.method
            }
            
            # Loop
            total = len(instances)
            for idx, (_, row) in enumerate(instances.iterrows()):
                try:
                    res = self.evaluate_instance(row, idx, total)
                    self.results["instance_evaluations"].append(res)
                except Exception as e:
                    logger.error(f"Error evaluating instance {idx}: {e}")
                    # Continue loop
                    
            # Aggregate
            self.results["aggregated_metrics"] = self._compute_aggregates()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            self.results["experiment_metadata"]["duration_seconds"] = duration
            self.results["experiment_metadata"]["completed_at"] = end_time.isoformat()
            
            logger.info(f"Experiment completed in {duration:.2f}s")
            
            self.save_results()
            
            return self.results
            
        except Exception as e:
            logger.error(f"Experiment failed: {e}", exc_info=True)
            raise RuntimeError(f"Experiment execution failed: {e}") from e

    def _compute_aggregates(self) -> Dict[str, Any]:
        """Compute mean/std for each metric."""
        aggregates = {}
        evals = self.results['instance_evaluations']
        
        if not evals:
            return {}
            
        sample_metrics = evals[0]['metrics'].keys()
        
        for m in sample_metrics:
            values = [e['metrics'][m] for e in evals if m in e['metrics']]
            if values:
                aggregates[m] = {
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values)),
                    "count": len(values)
                }
        return aggregates
        
    def save_results(self) -> None:
        """Save results to JSON and CSV."""
        # JSON
        json_path = self.config.output_dir / "results.json"
        # Convert any numpy types to python native for json
        # (Already mostly done in evaluate_instance, but aggregation has floats)
        
        # Custom encoder just in case
        class NpEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer): return int(obj)
                if isinstance(obj, np.floating): return float(obj)
                if isinstance(obj, np.ndarray): return obj.tolist()
                return super(NpEncoder, self).default(obj)
                
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=2, cls=NpEncoder)
        logger.info(f"Saved JSON results to: {json_path}")
        
        # CSV
        csv_data = []
        for inst in self.results['instance_evaluations']:
            row = {
                'instance_id': inst['instance_id'],
                'quadrant': inst['quadrant'],
                'prediction_correct': inst['prediction_correct']
            }
            # Flatten metrics
            for k, v in inst['metrics'].items():
                row[f"metric_{k}"] = v
            csv_data.append(row)
            
        df = pd.DataFrame(csv_data)
        csv_path = self.config.output_dir / "metrics.csv"
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved CSV metrics to: {csv_path}")
