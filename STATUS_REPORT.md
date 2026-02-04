# STATUS REPORT (Monitoring Phase)

**Batch Experiments - Phase 2 (Resumed)**

*   **Status:** Active (Restarted after hang).
*   **Recent Issues:**
    *   `MLP` + `SHAP` experiments (specifically `n=200`) caused the batch runner to **HANG** for 3+ hours.
    *   Action: Killed the stuck process.
    *   Resolution: Added filter to **SKIP** all `mlp_shap` experiments to prevent further hangs.
*   **Current Configuration:**
    *   Skipped: `Anchors` (Broken), `DiCE` (Too Slow), `SVM SHAP` (Too Slow), `MLP SHAP` (Hangs/Slow).
    *   Running: Remaining `SHAP` and `LIME` experiments on lighter models (`LogReg`, `XGBoost`, `RandomForest`).
*   **Progress:**
    *   The runner is processing the remaining queue.
    *   Completion estimate is significantly reduced now that heavy endpoints are skipped.

**Next Validation:**
*   Check logs in ~10 minutes to ensure new experiments are starting and completing.
