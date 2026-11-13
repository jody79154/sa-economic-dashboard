# Learning log

## 7 November 2026 — Environment and repository
Completed, as reported by the project owner:
- Configured an Ubuntu Oracle VM and verified Docker with hello-world.
- Tested local models, measured slow CPU inference, then removed models and stopped Ollama.
- Created ~/projects/sa-economic-dashboard and a Python virtual environment.
- Installed requests and pandas.

Repository work:
- Added scope, milestones, environment guide, source plan and starter folders.
- Preserved the existing Python ignore rules and extended them for generated data and credentials.

Lessons:
- A cloud VM, Python environment and GitHub repository are separate components.
- Download speed is different from model inference speed.
- Trial credits and Always Free allowances must be distinguished.
- Report completed work separately from planned capabilities.

Next milestone:
Fetch one real unemployment series, inspect its metadata and missing values, save a raw snapshot and report validation counts. No analytical results exist yet.

For each future entry record: goal, commands/change, observed result, problem/fix, lesson and next step. Do not include credentials or personal account identifiers.

## 7 November 2026 — First real data ingestion

Server execution succeeded, based on terminal output supplied by the project owner:
- 66 annual observations received; 31 missing values and 35 non-missing values.
- Raw response snapshot retained at data/raw/20261107T200413142210Z/.
- Cleaned export saved at data/processed/za_unemployment.csv.
- Latest available modeled ILO estimates (% of total labor force): 2021: 34.007; 2022: 33.268; 2023: 32.098; 2024: 32.279; 2025: 32.391.
- Script completed without triggering its structural, numeric, duplicate or percentage-range validation errors.

These are historical modeled estimates from this retrieval, not live measurements or national survey estimates. Missing observations were preserved, not replaced with zeros.

Next: inspect year coverage and missing years, calculate year-over-year percentage-point changes, then add PostgreSQL storage. Do not infer why values are missing without checking source metadata.

## Coverage and first interpretation
User-supplied inspection output confirms:
- API year range: 1960–2025.
- Available observations: every year from 1991 through 2025 (35 values).
- Missing observations: 1960–1990 inclusive (31 years).
- There are no internal gaps in the available series, so consecutive differences for this retrieval represent annual percentage-point changes.
- Unemployment fell from 34.007% in 2021 to 32.098% in 2023, then rose to 32.391% in 2025.
- This descriptive finding does not establish causes. Missing earlier years remain missing; they are not zero unemployment.

## PostgreSQL import completed
User-supplied output confirms PostgreSQL 18.6 on Ubuntu 26.04/aarch64, successful access to sa_economics as analytics_user, COPY 66, INSERT 0 66 and COMMIT. SQL counts matched the CSV: 66 rows, 35 available values, 31 NULL values, 1960–2025. Repeat-import behavior has not yet been verified on the server. Next: execute sql/002_analysis.sql and interpret its five query results.
