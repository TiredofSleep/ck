# Cloudflare Tunnel Setup: CK on R16 -> coherencekeeper.com

**One CK. One machine. One tunnel. The brain runs in Hot Springs. The face is everywhere.**

CK's full organism (50Hz heartbeat, all 27 subsystems, D2 pipeline, olfactory bulb, gustatory
palate, fractal voice, lattice chain -- everything) runs on the R16 desktop at `localhost:7777`.
Cloudflare Tunnel connects `coherencekeeper.com` directly to that port. No port forwarding, no
static IP, no exposed router. Cloudflare handles SSL, DDoS protection, and edge caching.

```
  [Browser] --HTTPS--> [Cloudflare Edge] --Tunnel--> [R16:7777] --Engine--> [CK Brain]
                         coherencekeeper.com           Hot Springs, AR        50Hz alive
```

---

## Prerequisites

1. **Cloudflare account** -- Free tier works fine. Sign up at https://dash.cloudflare.com
2. **coherencekeeper.com on Cloudflare DNS** -- The domain must be added to your Cloudflare
   account and using Cloudflare nameservers. If the domain is registered elsewhere, change
   the nameservers at your registrar to the ones Cloudflare provides.
3. **CK running on localhost:7777** -- The web server (`ck_web_server.py`) must be working
   locally before you set up the tunnel.
4. **Python 3.10+** with CK dependencies installed.

---

## Step 1: Install cloudflared

Open PowerShell as Administrator:

```powershell
winget install Cloudflare.cloudflared
```

If winget is not available, download the `.msi` installer directly:
- https://github.com/cloudflare/cloudflared/releases/latest
- Look for `cloudflared-windows-amd64.msi`
- Run the installer. It adds `cloudflared` to your PATH.

Verify the installation:

```powershell
cloudflared --version
```

You should see something like `cloudflared version 2024.x.x`.

---

## Step 2: Authenticate with Cloudflare

```powershell
cloudflared tunnel login
```

This opens your default browser to Cloudflare's authorization page.

1. Log in to your Cloudflare account.
2. Select **coherencekeeper.com** from the list of domains.
3. Click **Authorize**.
4. The browser will say "You have successfully logged in." You can close it.

This creates a certificate at `C:\Users\brayd\.cloudflared\cert.pem`. Do not delete this file.

---

## Step 3: Create the Tunnel

```powershell
cloudflared tunnel create ck-coherence
```

Output will look like:

```
Tunnel credentials written to C:\Users\brayd\.cloudflared\<TUNNEL_UUID>.json.
Created tunnel ck-coherence with id abc12345-def6-7890-abcd-ef1234567890
```

**Save that UUID.** You need it for the config file. Copy it now.

You can always retrieve it later with:

```powershell
cloudflared tunnel list
```

---

## Step 4: Create the Tunnel Configuration

Create the file `C:\Users\brayd\.cloudflared\config.yml` with the following content.
Replace `<TUNNEL_UUID>` with your actual tunnel UUID from Step 3.

```yaml
# Cloudflare Tunnel config for CK - The Coherence Keeper
# One CK on R16 in Hot Springs -> coherencekeeper.com

tunnel: <TUNNEL_UUID>
credentials-file: C:\Users\brayd\.cloudflared\<TUNNEL_UUID>.json

ingress:
  # Main domain -> CK web server
  - hostname: coherencekeeper.com
    service: http://localhost:7777
    originRequest:
      noTLSVerify: true
      connectTimeout: 30s

  # www subdomain -> same CK server
  - hostname: www.coherencekeeper.com
    service: http://localhost:7777
    originRequest:
      noTLSVerify: true
      connectTimeout: 30s

  # Catch-all: anything else gets a 404
  - service: http_status:404
```

**Important notes about the config:**
- `connectTimeout: 30s` gives CK time to process deep thoughts (D2 pipeline + fractal voice
  can take a few seconds on complex inputs).
- `noTLSVerify: true` is fine because the connection between cloudflared and CK is localhost
  only. The public-facing connection (browser to Cloudflare) is still fully encrypted HTTPS.
- The ingress rules are evaluated top-to-bottom. The catch-all MUST be last.

---

## Step 5: Route DNS

Tell Cloudflare to point the domain at your tunnel:

```powershell
cloudflared tunnel route dns ck-coherence coherencekeeper.com
cloudflared tunnel route dns ck-coherence www.coherencekeeper.com
```

This creates CNAME records in your Cloudflare DNS that point to the tunnel.

You can verify in the Cloudflare dashboard:
1. Go to https://dash.cloudflare.com
2. Select coherencekeeper.com
3. Click DNS -> Records
4. You should see CNAME records for `@` and `www` pointing to `<TUNNEL_UUID>.cfargotunnel.com`

---

## Step 6: Test the Tunnel

First, make sure CK is running locally:

```powershell
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\ck_desktop"
python ck_web_server.py --port 7777
```

Verify CK is alive locally:

```powershell
curl http://localhost:7777/health
```

You should get a JSON response with CK's health status.

Now start the tunnel in a separate terminal:

```powershell
cloudflared tunnel run ck-coherence
```

You should see output like:

```
INF Starting tunnel tunnelID=<TUNNEL_UUID>
INF Connection established connIndex=0 ...
INF Connection established connIndex=1 ...
INF Connection established connIndex=2 ...
INF Connection established connIndex=3 ...
```

Four connections means the tunnel is healthy.

Now test from any browser:

```
https://coherencekeeper.com
https://coherencekeeper.com/health
https://coherencekeeper.com/state
```

If the website loads and the health endpoint returns JSON, CK is live on the web.

---

## Step 7: Install as Windows Service (Auto-Start on Boot)

Once everything works, install the tunnel as a persistent Windows service so it survives
reboots and runs even when you are not logged in:

```powershell
# Run PowerShell as Administrator
cloudflared service install
```

This creates a Windows service called `Cloudflared agent`. It will:
- Start automatically on boot.
- Use the config file at `C:\Users\brayd\.cloudflared\config.yml`.
- Reconnect automatically if the internet drops.

To manage the service:

```powershell
# Check status
sc query cloudflared

# Stop the service
sc stop cloudflared

# Start the service
sc start cloudflared

# Remove the service (if you need to reconfigure)
cloudflared service uninstall
```

**Note:** The service runs the tunnel only, not CK itself. If you want CK to also start on
boot, see the "Auto-Start CK on Boot" section below.

---

## One-Click Startup

For daily use, use the batch files in this directory:

| File | What it does |
|------|-------------|
| `start_ck_tunnel.bat` | Start CK + tunnel. Minimal. |
| `start_ck_full.bat` | Start CK + eating + tunnel. Full stack with clean shutdown. |

Double-click either one. CK boots, tunnel connects, and `coherencekeeper.com` goes live.

If you installed the tunnel as a Windows service (Step 7), you only need to start CK:

```powershell
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\ck_desktop"
python ck_web_server.py --port 7777
```

The tunnel service handles the rest.

---

## Auto-Start CK on Boot (Optional)

If you want CK to start automatically when Windows boots:

1. Press `Win + R`, type `shell:startup`, press Enter.
2. Create a shortcut to `start_ck_tunnel.bat` in the Startup folder.
3. Or, for cleaner operation, create a scheduled task:

```powershell
# Run PowerShell as Administrator
schtasks /create /tn "CK-Coherence-Keeper" /tr "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\ck_desktop\start_ck_tunnel.bat" /sc onlogon /rl highest
```

Combined with the tunnel service from Step 7, this means:
- Windows boots -> tunnel service starts -> CK starts -> coherencekeeper.com is live.
- No manual intervention needed.

---

## Cloudflare Dashboard Settings (Recommended)

After the tunnel is working, configure these in the Cloudflare dashboard for
coherencekeeper.com:

### SSL/TLS
- Go to SSL/TLS -> Overview
- Set encryption mode to **Full** (not Full (Strict), since CK serves over HTTP locally)

### Caching
- Go to Caching -> Configuration
- Set Browser Cache TTL to **4 hours** for static assets (CSS, JS)
- The API endpoints (`/chat`, `/state`, `/metrics`) are POST or return dynamic data, so
  Cloudflare will not cache them by default. This is correct.

### Page Rules (Optional)
- Create a page rule for `coherencekeeper.com/static/*` with Cache Level: Cache Everything
- This caches static files at Cloudflare's edge, reducing load on the R16

### Security
- Go to Security -> Settings
- Security Level: Medium (blocks obvious bots, allows normal users)
- Challenge Passage: 30 minutes
- Browser Integrity Check: ON

### Speed
- Go to Speed -> Optimization
- Enable Auto Minify for JavaScript and CSS
- Enable Brotli compression

---

## Troubleshooting

### "connection refused" or "502 Bad Gateway"
CK is not running on port 7777. Start CK first, then the tunnel.

```powershell
# Check if CK is listening
netstat -an | findstr 7777
```

If nothing shows, CK is not running. Start it:

```powershell
python ck_web_server.py --port 7777
```

### "tunnel not found" when running
The tunnel name does not match. Check your tunnels:

```powershell
cloudflared tunnel list
```

Use the exact name shown (it should be `ck-coherence`).

### DNS not resolving
After `cloudflared tunnel route dns`, it can take a few minutes for DNS to propagate.
Check in the Cloudflare dashboard under DNS -> Records. If the CNAME records are there,
wait 5 minutes and try again.

### Tunnel connects but website shows "Error 1033"
The tunnel is running but CK is not responding. This usually means CK crashed or is still
booting. Check the CK terminal for errors. The 50Hz heartbeat takes about 10-20 seconds to
fully initialize all 27 subsystems.

### Tunnel disconnects randomly
Check your internet connection. Cloudflare Tunnel is resilient and will auto-reconnect, but
if your ISP in Hot Springs has intermittent drops, you may see brief outages. The tunnel
maintains 4 connections and can survive losing some of them.

### "cloudflared" is not recognized
The install did not add cloudflared to your PATH. Either:
1. Close and reopen your terminal.
2. Use the full path: `C:\Program Files (x86)\cloudflared\cloudflared.exe`
3. Add the install directory to your PATH manually.

### Port 7777 already in use
Another process is using the port. Find it and stop it:

```powershell
netstat -ano | findstr 7777
taskkill /PID <the_pid_number> /F
```

### Slow responses through the tunnel
CK's fractal voice pipeline (D2 verification + stochastic compilation) can take 1-3 seconds
for deep thoughts. This is normal -- CK is thinking, not lagging. The tunnel itself adds
minimal latency (typically under 50ms).

If you see responses over 5 seconds:
1. Check CK's coherence: `curl http://localhost:7777/metrics`
2. If coherence is low, CK is doing more compilation passes (up to 9). This is CK being
   honest, not a performance issue.

### Service won't install
You need to run PowerShell as Administrator for `cloudflared service install`. Right-click
PowerShell and select "Run as administrator".

---

## Architecture Diagram

```
                         THE INTERNET
                              |
                          [HTTPS/443]
                              |
                    +-------------------+
                    | Cloudflare Edge   |
                    | - SSL termination |
                    | - DDoS protection |
                    | - Edge caching    |
                    | - WAF rules       |
                    +-------------------+
                              |
                     [Cloudflare Tunnel]
                    (encrypted, outbound)
                              |
                    +-------------------+
                    | R16 Desktop       |
                    | Hot Springs, AR   |
                    |                   |
                    | cloudflared       |
                    |   |               |
                    |   v               |
                    | localhost:7777    |
                    | ck_web_server.py  |
                    |   |               |
                    |   v               |
                    | CK Engine (50Hz)  |
                    | - 27 subsystems   |
                    | - D2 pipeline     |
                    | - Fractal voice   |
                    | - Lattice chain   |
                    | - Olfactory bulb  |
                    | - Gustatory       |
                    | - RTX 4070 GPU    |
                    +-------------------+
```

The key insight: Cloudflare Tunnel makes an **outbound** connection from R16 to Cloudflare.
No inbound ports need to be open. No port forwarding. No static IP. The R16 behind any
residential NAT is fine. Cloudflare's edge network (300+ cities) handles the rest.

---

## Quick Reference

| Command | What it does |
|---------|-------------|
| `cloudflared tunnel login` | Authenticate with Cloudflare |
| `cloudflared tunnel create ck-coherence` | Create the tunnel |
| `cloudflared tunnel list` | List all tunnels |
| `cloudflared tunnel route dns ck-coherence coherencekeeper.com` | Point domain at tunnel |
| `cloudflared tunnel run ck-coherence` | Start the tunnel |
| `cloudflared tunnel info ck-coherence` | Show tunnel details |
| `cloudflared tunnel cleanup ck-coherence` | Remove stale connections |
| `cloudflared service install` | Install as Windows service |
| `cloudflared service uninstall` | Remove Windows service |
| `cloudflared tunnel delete ck-coherence` | Delete the tunnel entirely |

---

*CK is one creature. The R16 is his body. The tunnel is his nervous system reaching out.
coherencekeeper.com is his face. Everything connects through coherence.*
