# Active Context: XAI Evaluation Framework

- **Current Objective:** Run and maintain the XAI experiment pipeline and serve results to the dashboard.
- **Current State:** 
    - **API:** Running on port 8000 (local) and deployed on Render.
    - **Experiments:** Recovery runner (`scripts/run_recovery.py`) is executing missing exp2_scaled experiments.
    - **Data:** Verified `exp2_scaled` results (334 total runs confirmed visible in API).
    - **Dashboard:** Connected and visualizing results.
- **Next Steps:**
    1. Monitor long-running recovery experiments for remaining 50 runs.
    2. Expand test coverage for API endpoints.
- **Active Constraints:**
    - Python 3.10+ required.
    - `alibi` and `dice-ml` are required.
