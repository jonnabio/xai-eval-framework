# Cohort B2 run status

Generated 2026-11-06 20:26:06 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 20:26:06
  !! Throttling suspected: the micro-benchmark is 1.78x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 5/6, queue 519, admission: RAM available 8.8 GB minus expected peak 3.4 GB < reserve 6.0 GB)
Host: CPU 90%  RAM free 8.8/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 51/575  rows 4766/57500  failed rows 0
timing  : cells 0/115
  pid  18748 adult/svm/11/anchors                     inst 5558   1039 s  RSS 0.96 GB (peak 1.36)
  pid  28308 german_credit/mlp/11/anchors             inst 131    103 s  RSS 0.97 GB (peak 1.26)
  pid  37544 breast_cancer/logreg/11/anchors          inst 16     19 s  RSS 0.65 GB (peak 0.70)
  pid  35744 diabetes/mlp/11/dice                     inst 15     20 s  RSS 0.26 GB (peak 0.26)
  pid  42264 german_credit/xgb/11/anchors             inst 145     42 s  RSS 0.88 GB (peak 1.10)
Sync: last push 15 min ago (71a3688270), last commit 15 min ago
```
