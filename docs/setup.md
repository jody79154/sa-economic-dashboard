# Setup

## Existing Oracle environment
The user reports Ubuntu, Docker, Git, a virtual environment, requests and pandas installed. Screenshots confirmed an A1 Flex instance with 2 OCPUs, 12 GB RAM and a 150 GB boot volume. Other resources, storage performance settings and home-region eligibility have not been fully audited. Ollama was stopped and its models removed.

## Connect the existing project folder
Run on Ubuntu in ~/projects/sa-economic-dashboard. Inspect files before merging remote content:

```bash
cd ~/projects/sa-economic-dashboard
ls -la
git init -b main
git remote add origin https://github.com/jody79154/sa-economic-dashboard.git
git fetch origin
git status
```

Only if there are no existing tracked project files or conflicting local README/configuration files:
```bash
git checkout -b setup/first-dataset origin/main
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python -c "import requests, pandas; print('Dependencies import successfully')"
```

If Git reports an existing repository, remote or conflicting files, stop and inspect instead of forcing checkout or deleting anything.

The repository is private. HTTPS operations require GitHub authentication, not the GitHub account password. Use GitHub CLI browser authentication or a repository-specific SSH key. The Oracle login key and GitHub authentication are separate. Never paste tokens into commands, remote URLs or chat.

## Fresh checkout
```bash
git clone https://github.com/jody79154/sa-economic-dashboard.git
cd sa-economic-dashboard
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
```

Initial dependency ranges are not a tested lockfile. Record exact validated versions once ingestion is implemented.

## Development workflow
Use a feature branch, review git diff and git status, commit named source files, push the branch and open a pull request. Exclude generated data and secrets. Never run git clean or force a checkout to solve a merge problem without inspecting the files.

PostgreSQL, Streamlit, scheduled jobs and public hosting are not configured yet.
