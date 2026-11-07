# Cohort B2 run status

Generated 2026-11-07 04:10:09 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 04:10:09
  !! Throttling suspected: the micro-benchmark is 1.18x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 320, admission: 6 workers running (max 6))
Host: CPU 68%  RAM free 7.5/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 249/575  rows 22781/57500  failed rows 0
timing  : cells 0/115
  pid  22332 connect4/svm/11/anchors                  inst 1428    897 s  RSS 1.32 GB (peak 2.54)
  pid  14416 connect4/svm/22/shap                     inst 1486      7 s  RSS 0.34 GB (peak 0.34)
  pid  29420 adult/svm/22/anchors                     inst 9039    144 s  RSS 1.51 GB (peak 1.52)
  pid  21144 connect4/xgb/22/anchors                  inst 3370      5 s  RSS 1.77 GB (peak 2.35)
  pid  20960 adult/logreg/22/dice                     inst 5543     31 s  RSS 0.33 GB (peak 0.34)
  pid  29684 breast_cancer/svm/22/dice                inst 37      1 s  RSS 0.26 GB (peak 0.26)
Sync: last push 15 min ago (ef750b5258), last commit 15 min ago
```
