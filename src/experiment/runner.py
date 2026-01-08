"""
Experiment orchestration and execution.

Coordinates model loading, explanation generation, metric evaluation,
and result persistence for XAI evaluation experiments.
"""

import json
import logging
import sys
import argparse
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
# from src.xai.dice_wrapper import DiCETabularWrapper  <-- Moved to setup() to avoid hard dependency on dice_ml
from src.evaluation.sampler import EvaluationSampler
from src.metrics import CostMetric
from src.experiment.metrics_engine import MetricsEngine

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
        self.dice_explainer = None # DiCE wrapper
        self.baseline_values = None
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
            
            # Compute baseline for Faithfulness metric (mean of training data)
            self.baseline_values = np.mean(X_train, axis=0)
            

        else:
            raise ValueError(f"Unsupported dataset: {self.config.dataset}")
        
        # 2. Load Model
        logger.info(f"Loading model from: {self.config.model.path}")
        if not self.config.model.path.exists():
             raise FileNotFoundError(f"Model not found at {self.config.model.path}")
        
        # Assuming joblib load works for both RF and XGB as implemented in EXP1-10
        # Assuming joblib load works for both RF and XGB as implemented in EXP1-10
        self.model = joblib.load(self.config.model.path)
        
        # Setup DiCE if needed (AFTER MODEL LOAD)
        if hasattr(self.config.metrics, 'counterfactual') and self.config.metrics.counterfactual:
            logger.info("Initializing DiCE explainer...")
            # DiCE needs a dataframe with target
            # Reconstruct frame from dataset dict
            X_train = self.dataset['X_train']
            y_train = self.dataset['y_train']
            feature_names = self.dataset['feature_names']
            
            train_df = pd.DataFrame(X_train, columns=feature_names)
            
            if self.config.dataset == 'adult':
                target_col = 'income' # Known for adult
            else:
                target_col = 'target' 
                
            train_df[target_col] = y_train
            
            # Identify features
            # For processed data (OHE), everything is theoretically continuous or 0/1.
            cont_feats = feature_names
            cat_feats = []
            
            cat_feats = []
            
            from src.xai.dice_wrapper import DiCETabularWrapper
            self.dice_explainer = DiCETabularWrapper(
                model=self.model,
                training_data=train_df,
                target_column=target_col,
                continuous_features=cont_feats,
                categorical_features=cat_feats
            )

        
        # 3. Initialize Explainer
        logger.info(f"Initializing {self.config.explainer.method.upper()} explainer")
        
        if self.config.explainer.method == "shap":
            # Map 'tree'/'kernel' to wrapper 'model_type'
            model_type = self.config.explainer.explainer_type or "tree"
            
            # Extract n_background_samples if present, default to 100
            params = self.config.explainer.params.copy()
            n_bg = params.pop('n_background_samples', 100)
            
            self.explainer = SHAPTabularWrapper(
                model=self.model,
                training_data=self.dataset['X_train'],
                feature_names=self.dataset['feature_names'],
                model_type=model_type,
                n_background_samples=n_bg,
                **params
            )
        elif self.config.explainer.method == "lime":
            # Extract LIME specific params
            params = self.config.explainer.params or {}
            
            self.explainer = LIMETabularWrapper(
                training_data=self.dataset['X_train'],
                feature_names=self.dataset['feature_names'],
                class_names=self.dataset.get('class_names', ['<=50K', '>50K']),
                num_features=self.config.explainer.num_features or 10,
                num_samples=self.config.explainer.num_samples or 1000,
                random_state=self.config.random_seed,
                **params
            )
        else:
            raise ValueError(f"Unsupported explainer: {self.config.explainer.method}")
        
        # 4. Initialize Metrics Engine
        self.metrics_engine = MetricsEngine(
            config=self.config,
            model=self.model,
            dataset=self.dataset,
            baseline_values=self.baseline_values
        )

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
        
        # 2. Compute Metrics via Engine
        metrics_results = self.metrics_engine.compute_metrics(
            instance_data=instance_data,
            weights=weights,
            explainer_func=self.explainer.explain_instance,
            dice_explainer=self.dice_explainer,
            time_metrics=time_metrics
        )
        
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
            # Check if setup is already done (e.g. injected data)
            if self.dataset is None:
                self.setup()
            else:
                logger.info("Dataset already loaded, skipping setup()")

            # Check for existing results
            json_path = self.config.output_dir / "results.json"
            if json_path.exists():
                logger.info(f"Results already exist at {json_path}. Skipping experiment execution.")
                with open(json_path, 'r') as f:
                    self.results = json.load(f)
                return self.results
            
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

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description="Run single XAI experiment")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to experiment configuration YAML"
    )
    
    args = parser.parse_args()
    
    try:
        from src.experiment.config import load_config
        
        config_path = Path(args.config)
        config = load_config(config_path)
        
        runner = ExperimentRunner(config)
        runner.run()
        
    except Exception as e:
        logger.error(f"Failed to run experiment: {e}")
        sys.exit(1)
