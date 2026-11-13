# Inflation: first ingestion milestone

Source: World Bank FP.CPI.TOTL.ZG, Inflation, consumer prices (annual %), South Africa (ZAF). Underlying source: IMF International Financial Statistics. Definition and attribution: https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=ZA and https://databank.worldbank.org/metadataglossary/world-development-indicators/series/FP.CPI.TOTL.ZG (CC BY 4.0).

This measures annual change in consumer prices, not the CPI index level and not a labor-force share. Lower positive inflation means prices are rising more slowly, not falling. Negative inflation is possible; rates above 100% are also mathematically valid. Do not reuse the unemployment 0–100 constraint for inflation.

Run from the repository root with the virtual environment active:

```bash
python src/fetch_inflation.py
```

The script saves timestamped original responses in data/raw/inflation/ and exports data/processed/za_inflation.csv. Missing values remain blank. Country, indicator, duplicate keys and finite numeric values are checked. A temporary output file replaces the CSV only after successful validation/export. Raw responses are retained for review. An old CSV can remain after a failed run: inspect the terminal result and retrieval timestamp.

Validation: Python syntax compilation passed. Server execution, live data counts and latest values are pending; no results have been invented. This milestone does not change the existing unemployment table or live dashboard. The next step is a generic indicator table with appropriate units and constraints, followed by an indicator selector. Future refactoring should share the common API pagination logic between ingestion scripts.
