# Initial findings: South African unemployment

Source: World Bank indicator SL.UEM.TOTL.ZS, modeled ILO estimate, unemployment as a percentage of total labor force. Retrieved 7 November 2026. Results below are based on server query output provided by the project owner, not invented observations.

## Coverage
66 returned years (1960–2025), 35 available values (1991–2025), 31 missing values (1960–1990). Available years are consecutive. Missing values are NULL, not zeros.

## Findings
- Highest observed annual rate in this retrieved series: 34.007% in 2021.
- The five highest years are 2021, 2022, 2025, 2024 and 2023.
- Rates fell from 34.007% in 2021 to 32.098% in 2023, a decline of 1.909 percentage points.
- Rates then rose to 32.279% in 2024 and 32.391% in 2025.
- The 2025 increase was 0.112 percentage points. The 2025 rate remained 1.616 percentage points below 2021.

| Period represented | Available years | Mean annual unemployment rate |
|---|---:|---:|
| 1991–1999 | 9 | 22.934% |
| 2000–2009 | 10 | 22.623% |
| 2010–2019 | 10 | 25.759% |
| 2020–2025 | 6 | 32.210% |

These are unweighted averages of available annual rates, not unemployment rates calculated from pooled labor-force totals. The first and last periods are incomplete decades. Do not present the 2020–2025 average as a complete 2020s average.

## Limitations
These are modeled estimates, not necessarily identical to Stats SA national survey figures. Historical estimates may be revised. Descriptive trends do not establish their causes, predict future rates, or by themselves measure individual financial hardship.

## Reproduce
Run the ingestion and database import before analysis, from the project root:
```bash
python src/fetch_unemployment.py
psql -h 127.0.0.1 -U analytics_user -d sa_economics -f sql/001_unemployment.sql
psql -h 127.0.0.1 -U analytics_user -d sa_economics -f sql/002_analysis.sql
```
A later retrieval may produce revised results; retain its raw snapshot and timestamp.
