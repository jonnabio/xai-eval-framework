# Paper G — run status

Generated 2026-11-15 23:44 UTC by `scripts/paper_g_status.py`. Progress only: no metric value is shown before the run ends.

| Item | Value |
|---|---|
| State | idle |
| Active stage | synthetic |
| Last heartbeat | 2026-11-15T23:36:14Z (8 min ago) |
| Jobs | 6 |
| Running shards | — |
| Free memory | 6.8 GiB |
| Host | jonnabio-Latitude-5450 (13th Gen Intel(R) Core(TM) i5-1335U, 14.8 GiB RAM) |
| Commit of the run | c0a46d79e8f8 |
| Free disk | 360.6 GiB at set-up |

## Stages

| Stage | Done | Failed | To do | Total | Estimated time left |
|---|---|---|---|---|---|
| pilot | 4 | 0 | 0 | 4 | 0.0 h |
| full | 160 | 0 | 0 | 160 | 0.0 h |
| roar | 160 | 0 | 0 | 160 | 0.0 h |
| synthetic | 20 | 0 | 0 | 20 | 0.0 h |

### full: shards done per seed

| Seed | Done | Failed | Total |
|---|---|---|---|
| 42 | 32 | 0 | 32 |
| 123 | 32 | 0 | 32 |
| 456 | 32 | 0 | 32 |
| 789 | 32 | 0 | 32 |
| 101112 | 32 | 0 | 32 |

### roar: shards done per seed

| Seed | Done | Failed | Total |
|---|---|---|---|
| 42 | 32 | 0 | 32 |
| 123 | 32 | 0 | 32 |
| 456 | 32 | 0 | 32 |
| 789 | 32 | 0 | 32 |
| 101112 | 32 | 0 | 32 |

### synthetic: shards done per seed

| Seed | Done | Failed | Total |
|---|---|---|---|
| 42 | 4 | 0 | 4 |
| 123 | 4 | 0 | 4 |
| 456 | 4 | 0 | 4 |
| 789 | 4 | 0 | 4 |
| 101112 | 4 | 0 | 4 |

## Failures

None.

## Pilot timing and memory

| Shard | Seconds | Peak memory (MiB) |
|---|---|---|
| adult/logreg/seed_42 | 2.5 | 473.4 |
| adult/rf/seed_42 | 7.5 | 619.8 |
| adult/xgb/seed_42 | 2.0 | 378.4 |
| adult/mlp/seed_42 | 27.9 | 486.6 |
