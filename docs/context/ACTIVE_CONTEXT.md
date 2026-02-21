# Active Context: XAI Evaluation Framework

- **Current Objective:** Run and maintain the XAI experiment pipeline and serve results to the dashboard.
- **Current State:** 
    - **API:** Running on Render (Oregon) and synchronized with the latest recovery data.
    - **Experiments:** Phase 1 Recovery is **82.4% complete**. All MLP experiments are finalized. Currently running the high-latency **SVM + Kernel SHAP** batch (6 workers optimized).
    - **Data:** 344 healthy runs confirmed live in production dashboard.
    - **Dashboard Assets:** Updated Radar plots, Trade-off scatter plots, and Pearson Heatmaps generated with the 82% dataset and pushed to `outputs/`.
- **Next Steps:**
    1. Complete the final 17.6% of recovery (SVM-only).
    2. Finalize Paper A/B drafts with full statistical significance.
    3. Monitor background workers for potential SVM budget timeouts.
- **Active Constraints:**
    - Python 3.10+ required.
    - `alibi` and `dice-ml` are required.
