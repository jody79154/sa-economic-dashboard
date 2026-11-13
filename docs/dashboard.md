# Dashboard setup

The dashboard reads PostgreSQL using a dedicated SELECT-only role. It does not fetch from the World Bank automatically; ingestion and import remain separate steps.

## Setup on Ubuntu
From the project root, with the virtual environment active:
```bash
python -m pip install -r requirements.txt
sudo -u postgres createuser --pwprompt dashboard_reader
psql -h 127.0.0.1 -U analytics_user -d sa_economics -f sql/003_dashboard_access.sql
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
chmod 600 .streamlit/secrets.toml
nano .streamlit/secrets.toml
```
Create the role only once. Set its password at the prompt; enter that same password in the local secrets file. It is ignored by Git. Do not share it. The role created by createuser has no superuser, database-creation or role-creation privileges; grants allow reading only the observation table. Do not reuse the owner's password.

## Launch
Always run from the repository root:
```bash
python -m streamlit run app/dashboard.py
```
The server listens only on loopback. On Windows, open another PowerShell window and establish a tunnel:
```powershell
ssh -N -L 127.0.0.1:8501:127.0.0.1:8501 -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -i "PATH_TO_PRIVATE_KEY" ubuntu@SERVER_PUBLIC_IP
```
Keep both sessions open. Browse http://127.0.0.1:8501 on Windows. Do not open Oracle ingress ports 8501 or 5432. Closing the app terminal stops the app; background service deployment comes later.

## Verify
- Unfiltered latest year: 2025; rate: 32.391%; annual change: +0.112 pp, for the verified first snapshot.
- Highest rate: 34.007% in 2021.
- Coverage: 66 returned, 35 available, 31 missing.
- Year slider changes chart/table range; missing values stay missing.
- Downloaded selected CSV matches selected rows.
- Database reload button clears the five-minute data cache.
- Confirm git check-ignore .streamlit/secrets.toml reports the secret path.

Python syntax compilation passed in the preparation environment. Database integration and browser rendering must still be verified on the user's server.
