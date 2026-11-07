# Cohort B2 run status

Generated 2026-11-06 22:51:12 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 22:51:12
  !! Throttling suspected: the micro-benchmark is 1.27x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 5/6, queue 446, admission: RAM available 8.6 GB minus expected peak 3.6 GB < reserve 6.0 GB)
Host: CPU 58%  RAM free 8.6/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 124/575  rows 11282/57500  failed rows 0
timing  : cells 0/115
  pid  18748 adult/svm/11/anchors                     inst 1964     12 s  RSS 1.24 GB (peak 1.87)
  pid  40356 connect4/svm/11/shap                     inst 10533    545 s  RSS 0.34 GB (peak 0.36)
  pid   9200 connect4/rf/11/anchors                   inst 2694     43 s  RSS 2.49 GB (peak 2.79)
  pid    960 breast_cancer/logreg/11/dice             inst 101    138 s  RSS 0.26 GB (peak 0.26)
  pid  19892 german_credit/svm/11/shap                inst 155      2 s  RSS 0.25 GB (peak 0.25)
Sync: last push 15 min ago (eb6f92337c), last commit 15 min ago
```
