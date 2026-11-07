# Cohort B2 run status

Generated 2026-11-06 22:20:50 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 22:20:50
  !! Throttling suspected: the micro-benchmark is 1.27x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 451, admission: 6 workers running (max 6))
Host: CPU 72%  RAM free 5.9/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 118/575  rows 10739/57500  failed rows 0
timing  : cells 0/115
  pid  18748 adult/svm/11/anchors                     inst 7050   1898 s  RSS 1.09 GB (peak 1.87)
  pid  36276 connect4/mlp/11/anchors                  inst 10077     18 s  RSS 2.68 GB (peak 3.05)
  pid  40356 connect4/svm/11/shap                     inst 141      6 s  RSS 0.34 GB (peak 0.36)
  pid  45688 adult/rf/11/anchors                      inst 8599     51 s  RSS 1.43 GB (peak 1.80)
  pid  13948 connect4/svm/11/dice                     inst 1670     14 s  RSS 0.37 GB (peak 0.37)
  pid   9200 connect4/rf/11/anchors                   inst 6923    280 s  RSS 1.41 GB (peak 1.89)
Sync: last push 15 min ago (8ce26d9e02), last commit 15 min ago
```
