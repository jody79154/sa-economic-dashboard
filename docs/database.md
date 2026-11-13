# PostgreSQL setup and import

## Verified environment
The user supplied output confirming PostgreSQL 18.6 on Ubuntu 26.04/aarch64. This supersedes the earlier planned Ubuntu 24.04 image; do not assume the planned version was installed.
A connection to database sa_economics as analytics_user succeeded using localhost and a password. The role owns the project database and is not intended to be a superuser.

## One-time preparation (already completed on this server)
```bash
sudo apt install -y postgresql
sudo systemctl enable --now postgresql
sudo -u postgres createuser --pwprompt analytics_user
sudo -u postgres createdb --owner=analytics_user sa_economics
```
Do not repeat user/database creation after success. Never commit the password. Do not expose port 5432 publicly.

## Import
From the repository root, with the first CSV already generated:
```bash
psql -h 127.0.0.1 -U analytics_user -d sa_economics -f sql/001_unemployment.sql
```
Enter the password at the prompt. No password is placed in source, command arguments or URLs.

The SQL creates a table and imports through a temporary staging table in a transaction. The composite primary key identifies one country-indicator-year observation. Percentages are nullable numeric values constrained to 0–100; missing CSV values become NULL. Retrieval timestamps use timestamptz.
Reruns update matching rows rather than duplicating them, and older snapshots cannot overwrite newer records. Source rows absent from an import are not deleted. This is a latest-observation table, not full revision history; timestamped raw snapshots retain the downloaded responses.

Expected counts for the first verified CSV: 66 rows, 35 available values and 31 NULL values, covering 1960–2025. Compare the printed counts; future API revisions may change them.

Verify a rerun produces the same counts. If any SQL or copy operation fails, ON_ERROR_STOP aborts and the connection closing rolls back the uncommitted transaction. Check the error rather than continuing.

Import has not yet been executed on the user's server at the time this guide was written.
