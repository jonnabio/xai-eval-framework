# Cohort B2 run status

Generated 2026-11-07 18:37:05 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 18:37:05
  !! Throttling suspected: the micro-benchmark is 1.69x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 5, admission: ok)
Host: CPU 65%  RAM free 6.2/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 564/575  rows 51870/57500  failed rows 4
timing  : cells 0/115
  pid  26720 connect4/svm/33/anchors                  inst 674     90 s  RSS 0.63 GB (peak 0.63)
  pid  28268 adult/svm/55/shap                        inst 1966    102 s  RSS 0.30 GB (peak 0.30)
  pid  28632 adult/svm/44/anchors                     inst None     12 s  RSS 0.20 GB (peak 0.20)
  pid  28160 connect4/rf/33/anchors                   inst None      6 s  RSS 0.14 GB (peak 0.14)
  pid  35988 adult/rf/44/anchors                      inst None      4 s  RSS 0.07 GB (peak 0.07)
  pid  46256 adult/mlp/44/anchors                     inst None      2 s  RSS 0.00 GB (peak 0.00)
Sync: last push 15 min ago (7c4c12e691), last commit 15 min ago
```
