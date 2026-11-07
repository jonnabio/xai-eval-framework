# Cohort B2 run status

Generated 2026-11-06 19:40:40 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 19:40:40
Orchestrator: RUNNING (mode quality, workers 5/6, queue 534, admission: RAM available 8.6 GB minus expected peak 3.1 GB < reserve 6.0 GB)
Host: CPU 59%  RAM free 8.6/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 36/575  rows 3428/57500  failed rows 0
timing  : cells 0/115
  pid  45268 german_credit/rf/11/anchors              inst 152      5 s  RSS 0.63 GB (peak 1.68)
  pid  31044 breast_cancer/rf/11/anchors              inst 3     55 s  RSS 0.63 GB (peak 0.70)
  pid  29392 phishing/svm/11/shap                     inst 196      8 s  RSS 0.26 GB (peak 0.26)
  pid  39372 connect4/xgb/11/anchors                  inst 12372     76 s  RSS 1.23 GB (peak 1.54)
  pid  42736 spambase/rf/11/dice                      inst 600    213 s  RSS 0.27 GB (peak 0.27)
Sync: last push 15 min ago (af9f841ac3), last commit 15 min ago
```
