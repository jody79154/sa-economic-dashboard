# Public HTTPS deployment

Hostname: jaudaandeoraj-analytics.duckdns.org. User confirmed its IPv4 record was set to the existing VM address. DNS and public connectivity still require verification.

Caddy terminates HTTPS on port 443 and proxies to Streamlit on 127.0.0.1:8502. PostgreSQL remains local. No SSH tunnel is needed by public visitors.

## Prerequisites
- Healthy sa-dashboard service on 8502.
- DNS A record points to this VM; remove incorrect AAAA records if any.
- OCI subnet security list or attached NSG allows stateful inbound TCP 80 and 443 from 0.0.0.0/0, any source port.
- Host firewall permits TCP 80 and 443.
- Keep ports 5432 and 8502 closed to public ingress. Preserve existing SSH rules.

Inspect host firewall before changing it:
```bash
sudo ufw status
sudo iptables -S INPUT
```
Do not enable UFW blindly or flush firewall rules; Oracle images may have existing reject rules requiring specific changes and persistence.

## Install and configure
```bash
sudo apt update
sudo apt install -y caddy
cd ~/projects/sa-economic-dashboard
git pull --ff-only origin feature/first-dataset
sudo caddy validate --config deploy/Caddyfile --adapter caddyfile
sudo install -m 644 deploy/Caddyfile /etc/caddy/Caddyfile
sudo systemctl enable --now caddy
sudo systemctl reload caddy
```
Inspect an existing /etc/caddy/Caddyfile before replacing it if the server already hosts another website.

## Verify
```bash
getent ahostsv4 jaudaandeoraj-analytics.duckdns.org
curl --max-time 10 http://127.0.0.1:8502/_stcore/health
sudo systemctl status caddy --no-pager
sudo journalctl -u caddy -n 50 --no-pager
```
Then open https://jaudaandeoraj-analytics.duckdns.org from Windows or mobile data and test the slider, charts and CSV download. Certificate issuance requires working DNS and reachability. Do not claim public access before external verification.

This publishes the dashboard to anyone with the URL. Only public economic observations should be displayed. Passwords remain in ignored server secrets, not the repository or browser. The public app currently has no login and is intended as a small portfolio demonstration, not a high-traffic service. Refreshing the Streamlit cache does not trigger ingestion.

Caddy certificates renew automatically while requirements remain satisfied. If the VM's public IP changes, update DuckDNS. Service or DNS-provider availability is not guaranteed forever. Deployment does not add another Oracle VM or paid API.
