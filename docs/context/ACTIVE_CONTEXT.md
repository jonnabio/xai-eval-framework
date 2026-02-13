# Active Context: XAI Evaluation Framework

- **Current Objective:** Run and maintain the XAI experiment pipeline and serve results to the dashboard.
- **Current State:** 
    - **API:** Running on port 8000 (local) and deployed on Render.
    - **Experiments:** Recovery runner (`scripts/run_recovery.py`) is executing missing experiments (Anchors, DiCE, SVM/MLP SHAP).
    - **Data:** Verified `exp2_scaled` results (334 total runs confirmed visible in API).
    - **Dashboard Data:** Merged `aggregated_metrics` and `llm_evaluation` into `results.json` files for dashboard consumption.
    - **Dashboard:** Connected and visualizing results.
    - **Known Issues:** Feature mismatch (107 vs 108) in `MLPClassifier` resolved by loading correct preprocessor. Missing dependencies (`alibi`, `dice-ml`) installed. JSON corruption in `exp2_scaled` fixed.
- **Next Steps:**
    1. Monitor recovery experiments and verify dashboard integration.
    2. Expand test coverage for API endpoints.
    3. Finalize data aggregation for thesis report.
- **Active Constraints:**
    - Python 3.10+ required.
    - `alibi` and `dice-ml` are required.
