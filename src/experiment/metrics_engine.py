
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional

from src.metrics import (
    FaithfulnessMetric, 
    StabilityMetric, 
    SparsityMetric, 
    DomainAlignmentMetric, 
    CounterfactualSensitivityMetric
)
from src.experiment.config import ExperimentConfig

logger = logging.getLogger(__name__)

class MetricsEngine:
    """
    Handles computation of XAI metrics for experiment instances.
    """

    def __init__(self, config: ExperimentConfig, model: Any, dataset: Dict[str, Any], baseline_values: Optional[np.ndarray] = None):
        self.config = config
        self.model = model
        self.dataset = dataset
        self.baseline_values = baseline_values

    def compute_metrics(
        self,
        instance_data: np.ndarray,
        weights: np.ndarray,
        explainer_func: callable,
        dice_explainer: Any = None,
        time_metrics: Dict[str, float] = None
    ) -> Dict[str, Any]:
        """
        Compute all configured metrics for a single instance.
        """
        metrics_results = {}
        feature_names = self.dataset['feature_names']

        # 1. Cost (already measured upstream usually)
        if time_metrics and self.config.metrics.cost:
            metrics_results['cost'] = time_metrics.get('time_ms', 0.0)

        # 2. Sparsity
        if self.config.metrics.sparsity:
            sparsity_m = SparsityMetric()
            res = sparsity_m.compute(weights)
            metrics_results['sparsity'] = res['nonzero_percentage']

        # 3. Fidelity / Faithfulness
        if self.config.metrics.fidelity:
            faithfulness_m = FaithfulnessMetric(top_k=5)
            faithfulness_m.baseline_values = self.baseline_values
            res = faithfulness_m.compute(weights, model=self.model, data=instance_data)
            metrics_results['fidelity'] = res['faithfulness_score']
            metrics_results['faithfulness_gap'] = res['faithfulness_gap']

        # 4. Domain Alignment
        if hasattr(self.config.metrics, 'domain') and self.config.metrics.domain:
            domain_m = DomainAlignmentMetric()
            res = domain_m.compute(weights, feature_names, k=5)
            metrics_results.update(res)

        # 5. Counterfactual Sensitivity
        if hasattr(self.config.metrics, 'counterfactual') and self.config.metrics.counterfactual and dice_explainer:
            try:
                metrics_results.update(self._compute_cf_sensitivity(instance_data, weights, dice_explainer, feature_names))
            except Exception as e:
                logger.error(f"Error computing CF sensitivity: {e}")
                metrics_results['cf_sensitivity'] = 0.0

        # 6. Stability
        if self.config.metrics.stability:
             stability_m = StabilityMetric(
                 n_iterations=self.config.metrics.stability_perturbations,
                 perturbation_std=self.config.metrics.stability_noise_level
             )
             
             # wrap explainer func to match interface
             def wrapped_explainer_func(m, d):
                 w_full = explainer_func(m, d[0], return_full=False)
                 return {'feature_importance': w_full}

             res = stability_m.compute(
                 None, 
                 model=self.model, 
                 data=instance_data,
                 explainer_func=wrapped_explainer_func
             )
             metrics_results['stability'] = res['cosine_similarity_mean']

        return metrics_results

    def _compute_cf_sensitivity(self, instance_data: np.ndarray, weights: np.ndarray, dice_explainer: Any, feature_names: List[str]) -> Dict[str, Any]:
        query_df = pd.DataFrame(instance_data.reshape(1, -1), columns=feature_names)
        cfs_list = dice_explainer.generate_counterfactuals(query_df, total_CFs=1)
                
        if cfs_list and not cfs_list[0].empty:
            cf_df = cfs_list[0]
            cf_metric = CounterfactualSensitivityMetric()
            return cf_metric.compute(
                feature_importance=weights,
                feature_names=feature_names,
                original_instance=query_df,
                cf_files=cf_df,
                k=5
            )
        return {'cf_sensitivity': 0.0}
