# Data sources and provenance

Planned source: World Bank Indicators API v2.
Documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
Country page: https://data.worldbank.org/country/south-africa

First proposed series:
- Country: ZAF (South Africa)
- Indicator: SL.UEM.TOTL.ZS
- Definition: Unemployment, total (% of total labor force), modeled ILO estimate.
- Frequency: annual.
- Example request: https://api.worldbank.org/v2/country/ZAF/indicator/SL.UEM.TOTL.ZS?format=json&per_page=100

Proposed later indicators, to verify against API metadata before use:
- FP.CPI.TOTL.ZG: inflation, consumer prices (annual %).
- NY.GDP.MKTP.KD.ZG: GDP growth (annual %).

No data has been fetched yet. At ingestion, save the raw response, full request URL, UTC retrieval timestamp, indicator metadata, source update information when supplied, and validation counts. Handle pagination explicitly.

Validate HTTP status and API errors; confirm expected country and indicator; convert years and numeric values; reject duplicate country-indicator-year records; preserve missing values. Do not treat a missing value as zero.

Distinguish modeled ILO estimates from national unemployment estimates. Check coverage, units, methodology and licensing/attribution before publishing. Do not claim causation from chart correlations or present annual data as live measurements.
