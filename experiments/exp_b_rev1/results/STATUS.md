# Cohort B2 run status

Generated 2026-11-07 15:34:15 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 15:34:15
  !! Throttling suspected: the micro-benchmark is 1.18x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 31, admission: 6 workers running (max 6))
Host: CPU 82%  RAM free 6.9/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 538/575  rows 49289/57500  failed rows 1
timing  : cells 0/115
  pid  19312 connect4/svm/33/shap                     inst 8985     61 s  RSS 0.34 GB (peak 0.36)
  pid  24476 adult/svm/33/anchors                     inst 5480    542 s  RSS 1.14 GB (peak 1.96)
  pid  42884 connect4/svm/33/anchors                  inst 5786   2362 s  RSS 1.70 GB (peak 2.09)
  pid  24712 adult/svm/44/shap                        inst 3676    185 s  RSS 0.30 GB (peak 0.31)
  pid  37540 adult/logreg/44/anchors                  inst 3069     25 s  RSS 1.31 GB (peak 1.92)
  pid  33252 adult/svm/44/lime_full                   inst 3676     26 s  RSS 0.28 GB (peak 0.28)
Sync: last push 15 min ago (a36cbe6bf7), last commit 15 min ago
```
