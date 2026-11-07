# Cohort B2 run status

Generated 2026-11-07 14:18:04 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 14:18:04
  !! Throttling suspected: the micro-benchmark is 1.25x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 62, admission: 6 workers running (max 6))
Host: CPU 72%  RAM free 7.4/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 507/575  rows 46297/57500  failed rows 1
timing  : cells 0/115
  pid  28088 adult/svm/33/shap                        inst 8574    169 s  RSS 0.30 GB (peak 0.30)
  pid  19312 connect4/svm/33/shap                     inst 10680    902 s  RSS 0.34 GB (peak 0.36)
  pid  14300 adult/xgb/33/anchors                     inst 6511      7 s  RSS 1.54 GB (peak 3.22)
  pid  24476 adult/svm/33/anchors                     inst 2829   1043 s  RSS 1.35 GB (peak 1.57)
  pid  42884 connect4/svm/33/anchors                  inst 6601    769 s  RSS 1.00 GB (peak 1.12)
  pid  11820 phishing/logreg/33/anchors               inst 1165      7 s  RSS 0.74 GB (peak 1.09)
Sync: last push 15 min ago (020ba4d324), last commit 15 min ago
```
