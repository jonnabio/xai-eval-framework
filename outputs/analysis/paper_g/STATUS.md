# Paper G — run status

Generated 2026-11-15 14:18 UTC by `scripts/paper_g_status.py`. Progress only: no metric value is shown before the run ends.

| Item | Value |
|---|---|
| State | running |
| Active stage | full |
| Last heartbeat | 2026-11-15T14:18:54Z (0 min ago) |
| Jobs | 6 |
| Running shards | adult/rf/seed_42, adult/mlp/seed_42, bank_marketing/mlp/seed_42, compas/rf/seed_42, compas/mlp/seed_42 |
| Free memory | 6.2 GiB |
| Host | jonnabio-Latitude-5450 (13th Gen Intel(R) Core(TM) i5-1335U, 14.8 GiB RAM) |
| Commit of the run | c2b4eb202653 |
| Free disk | 360.6 GiB at set-up |

## Stages

| Stage | Done | Failed | To do | Total | Estimated time left |
|---|---|---|---|---|---|
| pilot | 4 | 0 | 0 | 4 | 0.0 h |
| full | 27 | 0 | 133 | 160 | 0.1 h |
| roar | 0 | 0 | 160 | 160 | — |
| synthetic | 0 | 0 | 20 | 20 | — |

### full: shards done per seed

| Seed | Done | Failed | Total |
|---|---|---|---|
| 42 | 27 | 0 | 32 |
| 123 | 0 | 0 | 32 |
| 456 | 0 | 0 | 32 |
| 789 | 0 | 0 | 32 |
| 101112 | 0 | 0 | 32 |

## Failures

None.

## Pilot timing and memory

| Shard | Seconds | Peak memory (MiB) |
|---|---|---|
| adult/logreg/seed_42 | 2.5 | 473.4 |
| adult/rf/seed_42 | 7.5 | 619.8 |
| adult/xgb/seed_42 | 2.0 | 378.4 |
| adult/mlp/seed_42 | 27.9 | 486.6 |
