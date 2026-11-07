# Cohort B2 run status

Generated 2026-11-07 15:49:30 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 15:49:30
  !! Throttling suspected: the micro-benchmark is 1.37x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 25, admission: 6 workers running (max 6))
Host: CPU 68%  RAM free 7.1/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 544/575  rows 49900/57500  failed rows 1
timing  : cells 0/115
  pid  19312 connect4/svm/33/shap                     inst 674     19 s  RSS 0.34 GB (peak 0.36)
  pid  24476 adult/svm/33/anchors                     inst 5480   1456 s  RSS 2.11 GB (peak 2.14)
  pid  42884 connect4/svm/33/anchors                  inst 5786   3277 s  RSS 1.79 GB (peak 2.09)
  pid  24712 adult/svm/44/shap                        inst 8198    404 s  RSS 0.30 GB (peak 0.31)
  pid  15304 adult/svm/55/lime                        inst 2461      8 s  RSS 0.28 GB (peak 0.28)
  pid  29196 adult/svm/55/lime_full                   inst None     19 s  RSS 0.20 GB (peak 0.20)
Sync: last push 15 min ago (891fe737f0), last commit 15 min ago
```
