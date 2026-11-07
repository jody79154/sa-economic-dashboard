# Run the dashboard as a background service

This unit is for the existing ubuntu user and project path. Streamlit binds to 127.0.0.1:8502. It reuses the existing local secrets file; no credentials are included in the unit.

## Install
First stop the foreground Streamlit on port 8502 with Ctrl+C in its terminal. Leave the Windows SSH tunnel alone.
In Ubuntu:
```bash
cd ~/projects/sa-economic-dashboard
git pull --ff-only origin feature/first-dataset
sudo systemd-analyze verify deploy/sa-dashboard.service
sudo install -m 644 deploy/sa-dashboard.service /etc/systemd/system/sa-dashboard.service
sudo systemctl daemon-reload
sudo systemctl enable --now sa-dashboard
systemctl is-active sa-dashboard
systemctl is-enabled sa-dashboard
curl --retry 5 --retry-delay 2 --retry-connrefused --max-time 10 http://127.0.0.1:8502/_stcore/health
```
Expected: active, enabled, ok. If verification fails, inspect the output before installing. The service must be active and healthy before claiming success. No reboot is required for installation.

## Troubleshooting
```bash
sudo journalctl -u sa-dashboard -n 60 --no-pager
sudo ss -ltnp 'sport = :8502'
```
Do not kill unrelated processes. A foreground app on port 8502 must exit before the service can bind. Startup is rate limited after repeated failures; fix the cause then use sudo systemctl reset-failed sa-dashboard and restart it.

## Operation
```bash
sudo systemctl restart sa-dashboard
sudo systemctl stop sa-dashboard
```
A stop leaves automatic startup enabled; to disable it use sudo systemctl disable --now sa-dashboard.
After updating code or dependencies, restart the service.

Closing an SSH session will not stop the service. Closing the Windows tunnel prevents access from Windows until the tunnel is recreated. Oracle must keep the VM running; this unit cannot prevent provider outages or free-tier reclamation. Data refreshes are not scheduled yet.

## Verification status
Service installation, health check, disconnect behavior and reboot startup require confirmation on the user's server. Enabled startup is not proof of a completed reboot test. Do not reboot until ready to interrupt other work.
