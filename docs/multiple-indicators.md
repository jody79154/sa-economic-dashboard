# Multiple-indicator storage

## Verified inflation download
User-supplied server output: 66 rows, zero missing values, all years 1960–2025 available. Latest annual CPI inflation observations: 2021 4.618745%; 2022 7.039873%; 2023 6.075244%; 2024 4.361152%; 2025 3.205505%. Raw snapshot: data/raw/inflation/20261113T232446668534Z/. These values describe this retrieval and may be revised.

The rate declined from 2022 through 2025. This means consumer prices rose more slowly, not that the price level fell.

## Import
Run from repository root:

```bash
psql -h 127.0.0.1 -U analytics_user -d sa_economics -f sql/004_economic_indicators.sql
```

The transaction creates public.economic_observations with generic value and unit columns, copies existing unemployment observations, stages and upserts inflation, then grants the dashboard reader SELECT access. Composite keys prevent duplicates; retrieval timestamps prevent stale replacement. The legacy unemployment table remains unchanged, so the existing dashboard continues working.

Expected first-import summary: unemployment 66 total, 35 available, 31 missing; inflation 66 total, 66 available, zero missing. Both cover 1960–2025. Repeat execution should retain those counts.

The 0–100 constraint applies only to unemployment; valid inflation can be negative or above 100. Both series reject non-finite numeric values. A transaction failure rolls back uncommitted changes.

During this transition, refresh unemployment using the existing fetch and 001 import, then run 004 to synchronize the new table. Fetch inflation before 004 to refresh inflation. There is not yet one unified scheduled pipeline. Dashboard selector and database execution verification are pending.
