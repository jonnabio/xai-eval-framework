# Cohort B2 run status

Generated 2026-11-07 14:33:18 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 14:33:18
  !! Throttling suspected: the micro-benchmark is 1.21x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 54, admission: 6 workers running (max 6))
Host: CPU 66%  RAM free 9.2/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 515/575  rows 47064/57500  failed rows 1
timing  : cells 0/115
  pid  28088 adult/svm/33/shap                        inst 3148    480 s  RSS 0.30 GB (peak 0.30)
  pid  19312 connect4/svm/33/shap                     inst 4066     38 s  RSS 0.34 GB (peak 0.36)
  pid  24476 adult/svm/33/anchors                     inst 8675     50 s  RSS 1.32 GB (peak 1.70)
  pid  42884 connect4/svm/33/anchors                  inst 3589    693 s  RSS 0.90 GB (peak 1.16)
  pid  47676 connect4/svm/33/lime                     inst 5215     14 s  RSS 0.31 GB (peak 0.31)
  pid   9528 german_credit/rf/33/dice                 inst 188    106 s  RSS 0.27 GB (peak 0.27)
Sync: last push 15 min ago (18fde56666), last commit 15 min ago
```
