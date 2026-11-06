# Cohort B2 run status

Generated 2026-11-06 14:07:36 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 14:07:36
  !! Throttling suspected: the micro-benchmark is 1.18x its first value (heat or power plan).
Orchestrator: RUNNING (mode pilot, workers 4/4, queue 115, admission: 4 workers running (max 4))
Host: CPU 53%  RAM free 10.6/31.4 GB  disk free 360 GB  AC  3000.0 MHz
pilot   : jobs 56/175  rows 230/700  failed rows 0
quality : jobs 0/575  rows 0/57500  failed rows 0
timing  : cells 0/115
  pid  33716 phishing/svm/11/shap                     inst 168    324 s  RSS 0.30 GB (peak 0.33)
  pid  16784 adult/svm/11/anchors                     inst 5558    493 s  RSS 0.92 GB (peak 1.46)
  pid  23972 german_credit/xgb/11/dice                inst 46     34 s  RSS 0.38 GB (peak 0.38)
  pid  36732 german_credit/logreg/11/dice             inst 164      3 s  RSS 0.26 GB (peak 0.26)
Sync: last push 15 min ago (9c5b5b94e7), last commit 15 min ago
```
