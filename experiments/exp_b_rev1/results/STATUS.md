# Cohort B2 run status

Generated 2026-11-07 10:14:43 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 10:14:43
Orchestrator: RUNNING (mode quality, workers 6/6, queue 180, admission: 6 workers running (max 6))
Host: CPU 66%  RAM free 8.9/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 389/575  rows 35591/57500  failed rows 1
timing  : cells 0/115
  pid  30040 connect4/svm/22/anchors                  inst 4564    153 s  RSS 1.10 GB (peak 2.11)
  pid  30684 adult/svm/22/shap                        inst 5744     12 s  RSS 0.30 GB (peak 0.31)
  pid  40636 breast_cancer/rf/33/dice                 inst 34    147 s  RSS 0.26 GB (peak 0.26)
  pid  22244 spambase/rf/33/anchors                   inst 833     12 s  RSS 0.62 GB (peak 0.69)
  pid  27812 adult/mlp/33/anchors                     inst 6474    552 s  RSS 1.22 GB (peak 3.39)
  pid  35184 german_credit/logreg/33/anchors          inst 43     43 s  RSS 0.84 GB (peak 1.01)
Sync: last push 15 min ago (90a04b26bb), last commit 15 min ago
```
