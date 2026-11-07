# Cohort B2 run status

Generated 2026-11-06 19:55:48 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 19:55:48
  !! Throttling suspected: the micro-benchmark is 1.60x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 4/6, queue 534, admission: RAM available 7.0 GB minus expected peak 3.1 GB < reserve 6.0 GB)
Host: CPU 42%  RAM free 7.0/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 37/575  rows 3580/57500  failed rows 0
timing  : cells 0/115
  pid  45268 german_credit/rf/11/anchors              inst 1     60 s  RSS 1.46 GB (peak 2.09)
  pid  29392 phishing/svm/11/shap                     inst 1452     45 s  RSS 0.26 GB (peak 0.26)
  pid  39372 connect4/xgb/11/anchors                  inst 3726    143 s  RSS 2.02 GB (peak 2.61)
  pid  42736 spambase/rf/11/dice                      inst 244     43 s  RSS 0.27 GB (peak 0.27)
Sync: last push 15 min ago (205a08f05a), last commit 15 min ago
```
