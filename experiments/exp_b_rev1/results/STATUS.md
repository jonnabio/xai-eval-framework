# Cohort B2 run status

Generated 2026-11-07 15:19:02 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 15:19:02
  !! Throttling suspected: the micro-benchmark is 1.26x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 34, admission: 6 workers running (max 6))
Host: CPU 70%  RAM free 8.4/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 536/575  rows 48999/57500  failed rows 1
timing  : cells 0/115
  pid  19312 connect4/svm/33/shap                     inst 8174    490 s  RSS 0.34 GB (peak 0.36)
  pid  24476 adult/svm/33/anchors                     inst 7747   1001 s  RSS 1.27 GB (peak 1.70)
  pid  42884 connect4/svm/33/anchors                  inst 5786   1448 s  RSS 1.31 GB (peak 2.09)
  pid  24712 adult/svm/44/shap                        inst 2194     21 s  RSS 0.30 GB (peak 0.31)
  pid  19496 adult/rf/44/dice                         inst 4241     95 s  RSS 0.33 GB (peak 0.33)
  pid  23216 adult/xgb/44/lime_full                   inst None     24 s  RSS 0.39 GB (peak 0.39)
Sync: last push 15 min ago (50556f61e1), last commit 15 min ago
```
