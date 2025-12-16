"""
Metrics implementation for Experiment 1 (Adult Dataset).
User Story: EXP1-02
"""

import time
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import kendalltau, spearmanr

def compute_fidelity(explanation_predictions, model_predictions):
    """
    Compute fidelity of the explanation.
    Measures how well the surrogate model approximates the black-box model.

    Args:
        explanation_predictions: predictions from the explanation model
        model_predictions: predictions from the black-box model

    Returns:
        dict: Local fidelity metrics (r2_score, mse)
    """
    return {
        'r2_score': r2_score(model_predictions, explanation_predictions),
        'mse': mean_squared_error(model_predictions, explanation_predictions)
    }

def compute_stability(explanation, perturbation_func, X_instance, n_perturbations=5, noise_level=0.01):
    """
    Compute stability of the explanation.
    Measures consistency of explanations under input perturbations.

    Args:
        explanation: The original explanation feature importances (array-like).
        perturbation_func: Function to generate perturbed instances and get new explanations.
                           Signature: func(X_instance, noise_level) -> new_explanation_importances
        X_instance: The instance being explained.
        n_perturbations: Number of perturbations to run.
        noise_level: Magnitude of noise.

    Returns:
        dict: Stability metrics (cosine, kendall, spearman) averaged over perturbations.
    """
    original_importances = np.array(explanation).reshape(1, -1)
    
    cosine_sims = []
    kendall_taus = []
    spearman_rhos = []

    for _ in range(n_perturbations):
        # Generate perturbed explanation
        # Note: perturbation_func handles the logic of perturbing X and re-explaining
        perturbed_importances = np.array(perturbation_func(X_instance, noise_level)).reshape(1, -1)

        # Cosine Similarity
        cosine_sims.append(cosine_similarity(original_importances, perturbed_importances)[0][0])
        
        # Rank Correlations
        # flatten for stats functions
        orig_flat = original_importances.flatten()
        pert_flat = perturbed_importances.flatten()
        
        kendall_taus.append(kendalltau(orig_flat, pert_flat)[0])
        spearman_rhos.append(spearmanr(orig_flat, pert_flat)[0])

    return {
        'cosine_similarity': np.nanmean(cosine_sims),
        'kendall_tau': np.nanmean(kendall_taus),
        'spearman_rho': np.nanmean(spearman_rhos)
    }

def compute_sparsity(explanation, threshold=0.01):
    """
    Compute sparsity of the explanation.
    Measures conciseness.

    Args:
        explanation: Feature importances.
        threshold: Threshold for considering a feature important.

    Returns:
        dict: Sparsity metrics (non_zero_ratio, top_k_mass, gini)
    """
    importances = np.abs(np.array(explanation))
    total_features = len(importances)
    total_mass = np.sum(importances) + 1e-10 # avoid div by zero

    # Non-zero ratio (features > threshold)
    non_zero_count = np.sum(importances > threshold)
    non_zero_ratio = non_zero_count / total_features

    # Top-k mass
    sorted_importances = np.sort(importances)[::-1]
    top_5_mass = np.sum(sorted_importances[:5]) / total_mass
    top_10_mass = np.sum(sorted_importances[:10]) / total_mass

    # Gini Coefficient
    # Mean absolute difference
    mad = np.abs(np.subtract.outer(importances, importances)).mean()
    # Relative mean absolute difference
    rmad = mad / np.mean(importances)
    gini = 0.5 * rmad

    return {
        'non_zero_ratio': non_zero_ratio,
        'top_5_mass': top_5_mass,
        'top_10_mass': top_10_mass,
        'gini_coefficient': gini
    }

def compute_cost(explanation_func, *args, **kwargs):
    """
    Compute cost (time) of generating explanations.
    
    Args:
        explanation_func: Function to generate explanation.
        *args, **kwargs: Arguments for the explanation function.

    Returns:
        dict: Cost metrics (wall_time_ms) and the result of the function
    """
    start_time = time.time()
    result = explanation_func(*args, **kwargs)
    end_time = time.time()

    wall_time_ms = (end_time - start_time) * 1000

    metrics = {
        'wall_time_ms': wall_time_ms
        # Memory and CPU time would require psutil and more complex tracking
    }
    
    return metrics, result
