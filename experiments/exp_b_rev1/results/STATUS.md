# Cohort B2 run status

Generated 2026-11-07 12:01:12 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 12:01:12
Orchestrator: RUNNING (mode quality, workers 6/6, queue 120, admission: 6 workers running (max 6))
Host: CPU 65%  RAM free 9.4/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 449/575  rows 40931/57500  failed rows 1
timing  : cells 0/115
  pid  36384 connect4/svm/33/dice                     inst 8174     87 s  RSS 0.30 GB (peak 0.37)
  pid  32316 connect4/logreg/33/anchors               inst 5363     10 s  RSS 1.31 GB (peak 2.15)
  pid  33456 german_credit/svm/33/anchors             inst 52     46 s  RSS 0.85 GB (peak 1.05)
  pid  49144 german_credit/rf/33/anchors              inst 131    203 s  RSS 1.06 GB (peak 1.51)
  pid   2996 adult/mlp/33/dice                        inst 6083     25 s  RSS 0.32 GB (peak 0.32)
  pid  48216 breast_cancer/svm/33/dice                inst 11     10 s  RSS 0.26 GB (peak 0.26)
Sync: last push 15 min ago (faac11f526), last commit 15 min ago
```
