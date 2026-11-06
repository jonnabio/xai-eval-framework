# Cohort B2 run status

Generated 2026-11-06 14:53:04 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 14:53:04
  !! Throttling suspected: the micro-benchmark is 1.24x its first value (heat or power plan).
Orchestrator: RUNNING (mode pilot, workers 4/4, queue 45, admission: 4 workers running (max 4))
Host: CPU 50%  RAM free 8.9/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 126/175  rows 510/700  failed rows 0
quality : jobs 0/575  rows 0/57500  failed rows 0
timing  : cells 0/115
  pid   4152 connect4/svm/11/shap                     inst 5432   1309 s  RSS 0.42 GB (peak 0.43)
  pid  40264 connect4/rf/11/anchors                   inst 1716    239 s  RSS 2.03 GB (peak 2.73)
  pid  39256 german_credit/svm/11/shap                inst 168     46 s  RSS 0.29 GB (peak 0.29)
  pid   4668 phishing/rf/11/anchors                   inst 1850     58 s  RSS 0.77 GB (peak 1.11)
Sync: last push 15 min ago (4a7dffe9be), last commit 15 min ago
```
