"""
Generate SCALED experiment configuration files for Phase I (Experiment 2: Comparative Evaluation).

Enhanced Matrix for PhD Thesis Statistical Robustness:
- Models (5): RF, XGB, SVM, MLP, LogReg
- Explainers (4): SHAP, LIME, Anchors, DiCE
- Seeds (5): 42, 123, 456, 789, 999 - for statistical robustness
- Sample sizes (3): 50, 100, 200 - configurable volume

Total configs: 5 × 4 × 5 × 3 = 300 experiment configurations

Usage:
    python scripts/generate_exp2_scaled_configs.py
    python scripts/generate_exp2_scaled_configs.py --seeds 42 123 456 --samples 100 200
    python scripts/generate_exp2_scaled_configs.py --quick  # Just 5 seeds, 1 sample size = 100 configs
"""
import yaml
import argparse
from pathlib import Path
from itertools import product

# Default Constants
DEFAULT_MODELS = ['rf', 'xgb', 'svm', 'mlp', 'logreg']
DEFAULT_EXPLAINERS = ['shap', 'lime', 'anchors', 'dice']
DEFAULT_SEEDS = [42, 123, 456, 789, 999]
DEFAULT_SAMPLES = [50, 100, 200]

OUTPUT_DIR = Path("configs/experiments/exp2_scaled")
MODEL_DIR = Path("experiments/exp1_adult/models")


def generate_configs(
    models: list = None,
    explainers: list = None,
    seeds: list = None,
    sample_sizes: list = None,
    stability_perturbations: int = 15,
    output_dir: Path = None
):
    """
    Generate experiment configuration files for all combinations.

    Args:
        models: List of model types (default: all 5)
        explainers: List of XAI methods (default: all 4)
        seeds: List of random seeds (default: 5 seeds)
        sample_sizes: List of samples_per_class values (default: [50, 100, 200])
        stability_perturbations: Number of perturbations for stability metric
        output_dir: Output directory for configs
    """
    models = models or DEFAULT_MODELS
    explainers = explainers or DEFAULT_EXPLAINERS
    seeds = seeds or DEFAULT_SEEDS
    sample_sizes = sample_sizes or DEFAULT_SAMPLES
    output_dir = output_dir or OUTPUT_DIR

    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    combinations = list(product(models, explainers, seeds, sample_sizes))

    print(f"Generating {len(combinations)} experiment configurations...")
    print(f"  Models: {models}")
    print(f"  Explainers: {explainers}")
    print(f"  Seeds: {seeds}")
    print(f"  Sample sizes: {sample_sizes}")
    print(f"  Output: {output_dir}")
    print()

    for model, explainer, seed, samples in combinations:

        config = {
            "name": f"exp2_{model}_{explainer}_s{seed}_n{samples}",
            "version": "2.0",
            "dataset": "adult",
            "random_seed": seed,

            "model": {
                "name": f"adult_{model}",
                "path": str(MODEL_DIR / f"{model}.joblib"),
                "type": model
            },

            "explainer": {
                "method": explainer,
                "params": {}
            },

            "sampling": {
                "strategy": "stratified",
                "samples_per_class": samples,
                "random_seed": seed
            },

            "metrics": {
                "fidelity": True,
                "stability": True,
                "sparsity": True,
                "cost": True,
                "domain": False,
                "counterfactual": False,
                "stability_perturbations": stability_perturbations
            },

            "output_dir": f"experiments/exp2_scaled/results/{model}_{explainer}/seed_{seed}/n_{samples}"
        }

        # Special Explainer Params
        if explainer == "shap":
            config['explainer']['params'] = {
                "n_background_samples": 50
            }
            if model in ['rf', 'xgb']:
                config['explainer']['explainer_type'] = "tree"
            else:
                config['explainer']['explainer_type'] = "kernel"

        elif explainer == "lime":
            config['explainer']['params'] = {
                "kernel_width": 3.0,
                "num_samples": 1000
            }

        elif explainer == "anchors":
            config['explainer']['params'] = {
                "threshold": 0.95
            }

        elif explainer == "dice":
            config['metrics']['counterfactual'] = True
            config['explainer']['params'] = {
                "num_counterfactuals": 5
            }

        # Write to file
        filename = output_dir / f"{model}_{explainer}_s{seed}_n{samples}.yaml"
        with open(filename, 'w') as f:
            yaml.dump(config, f, sort_keys=False)

        count += 1

    # Generate manifest
    manifest = {
        "experiment_set": "exp2_scaled",
        "total_configs": count,
        "dimensions": {
            "models": models,
            "explainers": explainers,
            "seeds": seeds,
            "sample_sizes": sample_sizes
        },
        "estimated_instances": count * sample_sizes[0] * 4,  # Conservative estimate
        "stability_perturbations": stability_perturbations
    }

    manifest_file = output_dir / "manifest.yaml"
    with open(manifest_file, 'w') as f:
        yaml.dump(manifest, f, sort_keys=False)

    print(f"Generated {count} configuration files in {output_dir}")
    print(f"Manifest saved to {manifest_file}")

    # Summary statistics
    min_instances = count * min(sample_sizes) * 4
    max_instances = count * max(sample_sizes) * 4
    print(f"\nEstimated total evaluation instances: {min_instances:,} - {max_instances:,}")

    return count


def main():
    parser = argparse.ArgumentParser(
        description="Generate scaled experiment configurations for XAI Benchmark"
    )
    parser.add_argument(
        "--models", nargs="+", default=DEFAULT_MODELS,
        help=f"Models to include (default: {DEFAULT_MODELS})"
    )
    parser.add_argument(
        "--explainers", nargs="+", default=DEFAULT_EXPLAINERS,
        help=f"Explainers to include (default: {DEFAULT_EXPLAINERS})"
    )
    parser.add_argument(
        "--seeds", nargs="+", type=int, default=DEFAULT_SEEDS,
        help=f"Random seeds (default: {DEFAULT_SEEDS})"
    )
    parser.add_argument(
        "--samples", nargs="+", type=int, default=DEFAULT_SAMPLES,
        help=f"Samples per class (default: {DEFAULT_SAMPLES})"
    )
    parser.add_argument(
        "--stability-perturbations", type=int, default=15,
        help="Number of stability perturbations (default: 15)"
    )
    parser.add_argument(
        "--output-dir", type=Path, default=OUTPUT_DIR,
        help=f"Output directory (default: {OUTPUT_DIR})"
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="Quick mode: 5 seeds × 1 sample size (100) = 100 configs"
    )
    parser.add_argument(
        "--medium", action="store_true",
        help="Medium mode: 5 seeds × 2 sample sizes = 200 configs"
    )

    args = parser.parse_args()

    # Preset modes
    if args.quick:
        args.samples = [100]
        print("Quick mode: Using single sample size (100)")
    elif args.medium:
        args.samples = [50, 100]
        print("Medium mode: Using 2 sample sizes (50, 100)")

    generate_configs(
        models=args.models,
        explainers=args.explainers,
        seeds=args.seeds,
        sample_sizes=args.samples,
        stability_perturbations=args.stability_perturbations,
        output_dir=args.output_dir
    )


if __name__ == "__main__":
    main()
