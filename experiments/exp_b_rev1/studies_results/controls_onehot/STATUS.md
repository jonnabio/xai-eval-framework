# Cohort B2 run status

Generated 2026-11-09 05:37:18 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-09 05:37:18
Orchestrator: RUNNING (mode quality, workers 6/6, queue 42, admission: 6 workers running (max 6))
Host: CPU 54%  RAM free 8.8/31.4 GB  disk free 358 GB  AC  3000.0 MHz
pilot   : jobs 0/25  rows 0/100  failed rows 0
quality : jobs 27/75  rows 340/7500  failed rows 0
timing  : cells 0/15
  pid  11396 adult/mlp/11/anchors                     inst 5511     36 s  RSS 1.26 GB (peak 3.84)
  pid  17976 adult/svm/11/shap                        inst 6631    431 s  RSS 0.30 GB (peak 0.32)
  pid  41632 adult/svm/11/anchors                     inst 4714    286 s  RSS 0.80 GB (peak 1.79)
  pid   7988 adult/svm/22/anchors                     inst 4657    177 s  RSS 0.90 GB (peak 1.02)
  pid  23984 adult/svm/22/shap                        inst 8916    171 s  RSS 0.30 GB (peak 0.30)
  pid  39700 adult/xgb/22/anchors                     inst 3915     53 s  RSS 1.15 GB (peak 1.48)
Sync: last push 15 min ago (f3aff81df7), last commit 15 min ago
```
