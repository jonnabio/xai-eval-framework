# Model-Agnostic XAI Evaluation Framework

> **PhD Thesis Project**: "Arquitectura Agnóstica para la Interpretabilidad de Modelos de Inteligencia Artificial de Caja Negra"
> [![Render Status](https://img.shields.io/badge/Render-Deployed-success)](https://xai-benchmark-frontend.onrender.com)

A modular, extensible framework for benchmarking Explainable AI (XAI) methods. This toolkit provides rigorous evaluation pipelines combining classical metrics (fidelity, stability) with novel LLM-based semantic evaluation for post-hoc explanations (LIME, SHAP).

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Startouf/xai-eval-framework.git
   cd xai-eval-framework
   ```

2. **Set up the environment**:
   This project uses `conda` for dependency management.
   ```bash
   conda env create -f environment.yml
   conda activate xai_eval
   ```

3. **Verify installation**:
   ```bash
   python -c "import src; print('Setup successful!')"
   ```

## ⚡ Quick Start: Experiment 1

Run the baseline Random Forest training pipeline on the Adult dataset:

```bash
# 1. Train the model
python experiments/exp1_adult/train_rf.py --verbose

# 2. Visualize results (ROC, Confusion Matrix)
python experiments/exp1_adult/visualize_rf_results.py
```

Outputs will be saved to `experiments/exp1_adult/results/`.

## 📂 Project Structure

```text
xai-eval-framework/
├── experiments/          # Experiment-specific logic
│   └── exp1_adult/       # EXP1: Adult Dataset Baseline
│       ├── configs/      # Model & metric configurations
│       ├── results/      # Generated plots & metrics
│       └── scripts/      # Experiment-specific utilities
├── src/                  # Core library code
│   ├── data_loading/     # Data loaders (Adult, etc.)
│   ├── models/           # Scikit-learn wrappers & training logic
│   └── metrics/          # XAI evaluation metrics (Fidelity, Stability)
├── docs/                 # Documentation & Design Docs
├── tests/                # Global unit & integration tests
├── environment.yml       # Conda environment definition
├── README.md             # This file
└── experiments/sample_data/ # Added for development/testing
```

## 🔬 Experiments

| Experiment | Description | Status |
| :--- | :--- | :--- |
| **[EXP1: Adult Baseline](experiments/exp1_adult/README.md)** | Establishes a robust Random Forest baseline on census data to serve as a target for LIME/SHAP benchmarking. | ✅ Complete |
| **EXP2: Semantic Eval** | (Planned) Evaluating natural language explanations using LLMs. | 📅 Pending |

## 🔗 Integration Status
Phase 1 integration is complete and under review:
- **Backend PR**: [Link to PR] (FastAPI REST API)
- **Frontend PR**: [Link to PR] (Next.js Dashboard)
- **Review Guide**: [PR_REVIEW_GUIDE.md](pr_evidence/PR_REVIEW_GUIDE.md)

## ♻️ Reproducibility

To ensure scientific rigor, this framework mandates:
- **Python Version**: 3.11
- **Random Seed**: Global seed `42` used for all splits and initializations.
- **Config-Driven**: All hyperparameters are defined in YAML files (e.g., [`rf_adult_config.yaml`](experiments/exp1_adult/configs/models/rf_adult_config.yaml)).

## 🚀 Deployment

The backend is configured for deployment on **Render.com** (Free Tier).

- **Infrastructure**: Defined in [`render.yaml`](render.yaml) (Infrastructure-as-Code).
- **Strategy**: [ADR-0020 Render Deployment Strategy](docs/decisions/0020-render-deployment-strategy.md).
- **Health Check**: `GET /health`.
- **Environment**: Requires `SENTRY_DSN` and `ENVIRONMENT=production` set in the Render Dashboard.

## 📚 Documentation

- [**Config Schema**](docs/config_schema.md): Detailed reference for configuration parameters.
- [**Branching Strategy**](BRANCHING.md): Guide to contribution workflow.

## 📝 Citation

*(Placeholder for Thesis/Paper Citation)*

```bibtex
@phdthesis{MyThesis2025,
  author = {Your Name},
  title = {Arquitectura Agnóstica para la Interpretabilidad de Modelos de IA},
  school = {University Name},
  year = {2025}
}
```

## 📧 Contact

**Author**: [Your Name]  
**Email**: [your.email@example.com]  
**Institution**: [University Name]
