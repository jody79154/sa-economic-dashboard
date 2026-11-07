# South African Economic Dashboard

A learning and portfolio project: build a reproducible pipeline that collects real economic data, validates it, stores it in PostgreSQL and presents it in Streamlit.

## Questions
- How have South Africa's unemployment, inflation and GDP growth changed over time?
- How does South Africa compare with selected countries?
- Which observations are missing, revised or not directly comparable?

## Current status
Environment preparation only. No dataset has been downloaded, no analysis has been completed, and no dashboard has been deployed.

Reported completed on the Ubuntu server:
- Docker and Git installed.
- Python virtual environment created.
- requests and pandas installed.
- Earlier Ollama models removed and the Ollama container stopped.

Planned: API ingestion → raw snapshots → validation and cleaning → PostgreSQL → SQL analysis → Streamlit.
Weekly refreshes, logging and backups will follow after the manual pipeline works.

## Repository map
| Path | Purpose |
|---|---|
| src/ | Data ingestion and transformation code |
| sql/ | Schema and analytical queries |
| app/ | Streamlit application |
| data/ | Generated raw and processed data; excluded from Git |
| docs/setup.md | Environment setup and server connection |
| docs/data-sources.md | Source definitions and provenance rules |
| docs/learning-log.md | Progress, lessons and next steps |
| requirements.txt | Initial Python dependencies |

## Getting started
Follow [the setup guide](docs/setup.md). The initial dependencies prepare the environment; there is no application command yet.

## Data integrity
Use real World Bank observations. Keep missing values missing, retain raw responses and retrieval timestamps, document units and estimation methods, and never substitute invented numbers. Historical observations may be revised. Correlation alone does not establish causation.

## Costs and security
Use the existing Oracle VM and open-source software; no paid model APIs are required. Free eligibility depends on the account, region and current Oracle allowances; this project cannot guarantee permanent free hosting.
Do not commit passwords, SSH keys, tokens, database dumps or environment files. Keep database access private.

## Milestones
- [x] Prepare server and Python environment (user-reported)
- [x] Establish repository documentation
- [ ] Retrieve and validate one unemployment series
- [ ] Add inflation and GDP growth
- [ ] Create PostgreSQL schema and repeatable load
- [ ] Write five analytical SQL queries
- [ ] Build a dashboard with source notes and filters
- [ ] Schedule refreshes and verify backups
- [ ] Add findings, screenshots and a demonstration

No findings or performance claims will be presented until supported by actual runs.
