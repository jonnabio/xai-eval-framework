# Cohort B2 run status

Generated 2026-11-06 15:38:33 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 15:38:33
  !! Throttling suspected: the micro-benchmark is 1.77x its first value (heat or power plan).
Orchestrator: RUNNING (mode pilot, workers 4/4, queue 4, admission: 4 workers running (max 4))
Host: CPU 48%  RAM free 9.6/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 167/175  rows 673/700  failed rows 0
quality : jobs 0/575  rows 0/57500  failed rows 0
timing  : cells 0/115
  pid   4152 connect4/svm/11/shap                     inst 9079    646 s  RSS 0.42 GB (peak 0.48)
  pid  10976 connect4/svm/11/anchors                  inst 12120    420 s  RSS 1.47 GB (peak 1.86)
  pid  35816 adult/svm/11/shap                        inst 5558   2085 s  RSS 0.38 GB (peak 0.38)
  pid  33388 phishing/rf/11/shap                      inst 1337      1 s  RSS 0.26 GB (peak 0.26)
Sync: last push 15 min ago (6f3f5fa7dc), last commit 15 min ago
```
