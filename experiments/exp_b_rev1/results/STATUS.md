# Cohort B2 run status

Generated 2026-11-06 22:05:41 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 22:05:41
  !! Throttling suspected: the micro-benchmark is 1.21x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 4/6, queue 456, admission: RAM available 7.8 GB minus expected peak 3.4 GB < reserve 6.0 GB)
Host: CPU 48%  RAM free 7.8/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 115/575  rows 10433/57500  failed rows 0
timing  : cells 0/115
  pid  18748 adult/svm/11/anchors                     inst 7050    989 s  RSS 1.18 GB (peak 1.87)
  pid  36276 connect4/mlp/11/anchors                  inst 9906    165 s  RSS 2.29 GB (peak 3.05)
  pid  40356 connect4/svm/11/shap                     inst 9994    681 s  RSS 0.34 GB (peak 0.36)
  pid  16236 adult/xgb/11/anchors                     inst 417     92 s  RSS 1.62 GB (peak 2.53)
Sync: last push 15 min ago (3aa0c25609), last commit 15 min ago
```
