# Cohort B2 run status

Generated 2026-11-06 21:04:35 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 21:04:35
  !! Throttling suspected: the micro-benchmark is 1.82x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 490, admission: 6 workers running (max 6))
Host: CPU 75%  RAM free 9.0/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 79/575  rows 7339/57500  failed rows 0
timing  : cells 0/115
  pid  18748 adult/svm/11/anchors                     inst 3612     73 s  RSS 1.14 GB (peak 1.87)
  pid  17976 phishing/mlp/11/anchors                  inst 1691    104 s  RSS 1.07 GB (peak 2.10)
  pid  25896 connect4/svm/11/lime                     inst 6936     10 s  RSS 0.31 GB (peak 0.31)
  pid  36276 connect4/mlp/11/anchors                  inst 3969     79 s  RSS 0.93 GB (peak 1.14)
  pid  28056 diabetes/xgb/11/dice                     inst 43     11 s  RSS 0.37 GB (peak 0.37)
  pid  35348 adult/xgb/11/lime_full                   inst 4709      2 s  RSS 0.39 GB (peak 0.39)
Sync: last push 8 min ago (ec9cbedf5f), last commit 8 min ago
```
