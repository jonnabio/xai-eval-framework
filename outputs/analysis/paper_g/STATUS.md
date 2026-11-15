# Paper G — run status

Generated 2026-11-15 15:34 UTC by `scripts/paper_g_status.py`. Progress only: no metric value is shown before the run ends.

| Item | Value |
|---|---|
| State | running |
| Active stage | roar |
| Last heartbeat | 2026-11-15T15:34:20Z (0 min ago) |
| Jobs | 6 |
| Running shards | electricity/mlp/seed_42, adult/mlp/seed_42, bank_marketing/mlp/seed_42, magic_telescope/mlp/seed_123, electricity/rf/seed_123 |
| Free memory | 5.6 GiB |
| Host | jonnabio-Latitude-5450 (13th Gen Intel(R) Core(TM) i5-1335U, 14.8 GiB RAM) |
| Commit of the run | b3c6893b7248 |
| Free disk | 360.6 GiB at set-up |

## Stages

| Stage | Done | Failed | To do | Total | Estimated time left |
|---|---|---|---|---|---|
| pilot | 4 | 0 | 0 | 4 | 0.0 h |
| full | 160 | 0 | 0 | 160 | 0.0 h |
| roar | 42 | 0 | 118 | 160 | 0.0 h |
| synthetic | 0 | 0 | 20 | 20 | — |

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
| 42 | 29 | 0 | 32 |
| 123 | 13 | 0 | 32 |
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
