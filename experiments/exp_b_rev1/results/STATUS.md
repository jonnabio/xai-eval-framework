# Cohort B2 run status

Generated 2026-11-07 13:02:03 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 13:02:03
  !! Throttling suspected: the micro-benchmark is 1.19x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 4/6, queue 83, admission: RAM available 8.2 GB minus expected peak 4.9 GB < reserve 6.0 GB)
Host: CPU 73%  RAM free 8.2/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 488/575  rows 44322/57500  failed rows 1
timing  : cells 0/115
  pid   2696 adult/svm/33/shap                        inst 5233    267 s  RSS 0.30 GB (peak 0.30)
  pid  36256 connect4/svm/33/shap                     inst 391    299 s  RSS 0.34 GB (peak 0.34)
  pid  27000 phishing/svm/33/anchors                  inst 264     11 s  RSS 0.74 GB (peak 1.06)
  pid   7300 german_credit/logreg/33/dice             inst 178     16 s  RSS 0.26 GB (peak 0.26)
Sync: last push 15 min ago (4dfa9a5d82), last commit 15 min ago
```
