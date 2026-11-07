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
