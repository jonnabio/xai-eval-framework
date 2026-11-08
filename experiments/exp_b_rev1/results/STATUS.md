# Cohort B2 run status

Generated 2026-11-07 19:22:44 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 19:22:44
Orchestrator: RUNNING (mode quality, workers 5/6, queue 3, admission: RAM available 5.0 GB minus expected peak 3.9 GB < reserve 3.5 GB (smaller jobs go first))
Host: CPU 58%  RAM free 5.0/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 567/575  rows 52169/57500  failed rows 4
timing  : cells 0/115
  pid  26720 connect4/svm/33/anchors                  inst 674   2830 s  RSS 1.32 GB (peak 2.14)
  pid  28160 connect4/rf/33/anchors                   inst 3704     85 s  RSS 2.80 GB (peak 2.80)
  pid  46256 adult/mlp/44/anchors                     inst 8431     74 s  RSS 2.35 GB (peak 3.44)
  pid  19700 adult/svm/55/anchors                     inst 3541    152 s  RSS 1.18 GB (peak 1.44)
  pid  38764 adult/xgb/44/anchors                     inst 9730      9 s  RSS 1.48 GB (peak 2.36)
Sync: last push 15 min ago (64eaf0250c), last commit 15 min ago
```
