# Cohort B2 run status

Generated 2026-11-07 17:20:56 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 17:20:56
  !! Throttling suspected: the micro-benchmark is 1.16x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 5/6, queue 8, admission: RAM available 8.4 GB minus expected peak 4.9 GB < reserve 6.0 GB (smaller jobs go first))
Host: CPU 62%  RAM free 8.4/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 562/575  rows 51655/57500  failed rows 3
timing  : cells 0/115
  pid  24712 adult/svm/44/shap                        inst 7105    399 s  RSS 0.30 GB (peak 0.31)
  pid  14008 connect4/svm/33/anchors                  inst 12389    171 s  RSS 1.60 GB (peak 2.05)
  pid  48280 adult/svm/55/shap                        inst 1027     85 s  RSS 0.30 GB (peak 0.31)
  pid  41516 adult/svm/33/anchors                     inst 5853   2829 s  RSS 0.79 GB (peak 1.92)
  pid  11340 adult/svm/44/anchors                     inst 9162     49 s  RSS 1.01 GB (peak 1.44)
Sync: last push 15 min ago (0ef897451d), last commit 15 min ago
```
