# Cohort B2 run status

Generated 2026-11-06 14:37:53 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 14:37:53
  !! Throttling suspected: the micro-benchmark is 1.44x its first value (heat or power plan).
Orchestrator: RUNNING (mode pilot, workers 4/4, queue 55, admission: 4 workers running (max 4))
Host: CPU 69%  RAM free 9.8/31.4 GB  disk free 360 GB  AC  3000.0 MHz
pilot   : jobs 116/175  rows 470/700  failed rows 0
quality : jobs 0/575  rows 0/57500  failed rows 0
timing  : cells 0/115
  pid   4152 connect4/svm/11/shap                     inst 5432    398 s  RSS 0.43 GB (peak 0.43)
  pid  35524 spambase/rf/11/anchors                   inst 244     79 s  RSS 0.49 GB (peak 0.59)
  pid   3232 adult/xgb/11/anchors                     inst 417     32 s  RSS 1.57 GB (peak 2.51)
  pid  46260 diabetes/mlp/11/anchors                  inst None     10 s  RSS 0.16 GB (peak 0.16)
Sync: last push 15 min ago (11e852c120), last commit 15 min ago
```
