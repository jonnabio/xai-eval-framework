# Model-Agnostic XAI Evaluation Framework

This repository implements a modular, model-agnostic framework designed to benchmark XAI methods (such as LIME, SHAP, Anchors, and counterfactuals). It provides tools to evaluate explanations using classical metrics (fidelity, stability, sparsity, cost/EEU) as well as LLM-based semantic scores (causal alignment, counterfactual sensitivity).

The project targets multiple experimental setups, starting with tabular data (Adult dataset MVP). It utilizes Python 3.11 and Conda for environment management.

This work is part of the PhD thesis: **"Arquitectura Agnóstica para la Interpretabilidad de Modelos de Inteligencia Artificial de Caja Negra"**.

## Branching model

The `main` branch is stable and corresponds to thesis/paper-ready code. Development for specific experiments happens in branches like `dev/exp1-adult-mvp`.

See [BRANCHING.md](BRANCHING.md) for details.
