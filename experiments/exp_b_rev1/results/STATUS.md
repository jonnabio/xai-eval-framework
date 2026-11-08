# Cohort B2 run status

Generated 2026-11-07 19:53:10 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 19:53:10
Orchestrator: RUNNING (mode quality, workers 5/6, queue 1, admission: RAM available 7.8 GB minus expected peak 5.3 GB < reserve 3.5 GB (smaller jobs go first))
Host: CPU 61%  RAM free 7.8/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 569/575  rows 52459/57500  failed rows 5
timing  : cells 0/115
  pid  28160 connect4/rf/33/anchors                   inst 8473     35 s  RSS 1.81 GB (peak 2.94)
  pid  19700 adult/svm/55/anchors                     inst 2224    557 s  RSS 0.77 GB (peak 1.55)
  pid  29032 adult/xgb/55/anchors                     inst 3760      2 s  RSS 1.53 GB (peak 2.85)
  pid   7816 connect4/svm/33/anchors                  inst 5215    183 s  RSS 0.97 GB (peak 1.22)
  pid  17592 adult/rf/55/anchors                      inst 2514     92 s  RSS 1.12 GB (peak 1.69)
Sync: last push 15 min ago (7ee40e576d), last commit 15 min ago
```
