# Tech Stack Context

**Scope**: XAI Evaluation Framework (`xai-eval-framework`)
**Status**: Active
**Last Updated**: 2026-01-12

## Core Frameworks
- **Runtime**: Python 3.11
- **Environment Manager**: Conda / Pip
- **Primary Libraries**:
    - `scikit-learn` == 1.5.2 (Modeling)
    - `pandas` (Data Manipulation)
    - `numpy` (Math)

## Machine Learning & XAI
- **Models**: RandomForest, XGBoost, LogisticRegression, Neural Networks (PyTorch/Keras optional)
- **XAI Libraries**:
    - `shap` (Shapley Values)
    - `lime` (Local Surrogate)
    - `dice-ml` (Counterfactuals)

## API & Service
- **Framework**: FastAPI
- **Server**: Uvicorn / Gunicorn
- **Validation**: Pydantic v2

## Testing & Quality
- **Testing**: Pytest
- **Linting**: Ruff / Flake8
- **Formatting**: Black / Isort

## Infrastructure
- **Deployment**: Render.com (Docker/Python Environment)
- **CI/CD**: GitHub Actions (planned)
