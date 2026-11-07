# Cohort B2 run status

Generated 2026-11-06 23:51:52 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 23:51:52
  !! Throttling suspected: the micro-benchmark is 1.30x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 424, admission: 6 workers running (max 6))
Host: CPU 70%  RAM free 10.4/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 145/575  rows 13287/57500  failed rows 0
timing  : cells 0/115
  pid  40356 connect4/svm/11/shap                     inst 8975    820 s  RSS 0.34 GB (peak 0.36)
  pid  19772 spambase/svm/11/anchors                  inst 216     12 s  RSS 0.63 GB (peak 1.65)
  pid  22332 connect4/svm/11/anchors                  inst 9079    121 s  RSS 1.10 GB (peak 1.10)
  pid  48188 adult/svm/11/shap                        inst 5558    263 s  RSS 0.30 GB (peak 0.30)
  pid  24424 adult/svm/11/lime                        inst 7213     15 s  RSS 0.28 GB (peak 0.28)
  pid  33472 adult/logreg/11/anchors                  inst None      8 s  RSS 0.21 GB (peak 0.21)
Sync: last push 15 min ago (18dfdd9528), last commit 15 min ago
```
