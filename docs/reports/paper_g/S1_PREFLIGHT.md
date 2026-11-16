# Paper G — S1 full-run preflight record

Recorded 2026-11-16 14:39 UTC at `be0626a65` (main after PR #137) on jonnabio-Latitude-5450, Python 3.13.12 (run-host venv), before any full S1 output existed.

```
PASS 1 spec 12.3 frozen (unchanged since 664b71f22)
PASS 2 supplementary code revision
PASS 3 regression suite
PASS 4 semantic contract (S1 pairs admitted; frozen LIME refused undeclared)
PASS 5 deterministic shard bytes (phoneme/logreg/42 computed twice)
PASS 6 original outputs identical to PR #129 head
PASS 7 160 target blocks with stored LIME rows
PASS 8 pilot reproduces the committed pilot CSVs byte for byte
PASS 9 new paths cannot overwrite history (supplementary/s1 absent; outside raw/analysis/s3/pilot)
PASS 10 resource monitoring (MemAvailable, package temperature)
free GiB 5.0 temp C 66.0 | block time phoneme/logreg 5.4 s
ALL PASS
regression suite: ========= 134 passed, 121 deselected, 4 warnings in 139.60s (0:02:19) ==========
```

- Frozen specification: `ANALYSIS_PLAN.md` §12.3 at `664b71f22` (unchanged). S1 code: `scripts/paper_g_s1_lime.py` at `b24461a07` (merged `be0626a65`). Original data: frozen run `04c6dfd84`.
- Concurrency: **4 workers** instead of 6. Available memory at preflight was 5.0 GiB and ROAR-lite peaked at 1.1 GiB per job (6 × 1.1 > 5.0); one thread per worker and the 1.5 GiB admission guard unchanged. No scientific setting changed.
- Command: `.venv/bin/python scripts/paper_g_s1_lime.py --full --jobs 4 --authorized "Author approval, 2026-11-16, Paper G Task 19 (full S1)"`
