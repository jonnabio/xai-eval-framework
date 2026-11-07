# Cohort B2 run status

Generated 2026-11-07 16:50:28 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 16:50:28
  !! Throttling suspected: the micro-benchmark is 1.27x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 11, admission: 6 workers running (max 6))
Host: CPU 68%  RAM free 7.1/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 558/575  rows 51303/57500  failed rows 3
timing  : cells 0/115
  pid  19312 connect4/svm/33/shap                     inst 6349     38 s  RSS 0.21 GB (peak 0.36)
  pid  24712 adult/svm/44/shap                        inst 9612      2 s  RSS 0.30 GB (peak 0.31)
  pid  14008 connect4/svm/33/anchors                  inst 4382     88 s  RSS 1.47 GB (peak 1.85)
  pid  48280 adult/svm/55/shap                        inst 4833      3 s  RSS 0.30 GB (peak 0.30)
  pid  41516 adult/svm/33/anchors                     inst 5853   1001 s  RSS 1.65 GB (peak 1.82)
  pid  11340 adult/svm/44/anchors                     inst 5207    491 s  RSS 1.34 GB (peak 1.34)
Sync: last push 15 min ago (10e6dec76a), last commit 15 min ago
```
