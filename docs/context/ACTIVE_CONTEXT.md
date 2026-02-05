# Active Context: XAI Evaluation Framework

- **Current Objective:** Run and maintain the XAI experiment pipeline and serve results to the dashboard.
- **Current State:** 
    - **API:** Running on port 8000 (`src.api.main`) locally; deployed on Render.
    - **Experiments:** Recovery runner (`scripts/run_recovery.py`) is executing missing experiments (Anchors, DiCE, SVM/MLP SHAP).
    - **Dashboard Data:** Merged `aggregated_metrics` and `llm_evaluation` into `results.json` files for dashboard consumption.
    - **Dashboard:** Connected and visualizing results.
    - **Known Issues:** Feature mismatch (107 vs 108) in `MLPClassifier` resolved by loading correct preprocessor. Missing dependencies (`alibi`, `dice-ml`) installed.
- **Next Steps:**
    1. Monitor long-running recovery experiments.
    2. Expand test coverage for API endpoints.
- **Active Constraints:**
    - Python 3.10+ required.
    - Use `pip install -r requirements.txt` for deps.
    - `alibi` and `dice-ml` are required for full experiment suite.
