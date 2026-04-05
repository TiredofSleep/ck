# CLAUDE START HERE -- CK Project Orientation

**Read this FIRST before doing ANYTHING.** This document exists because Claude
sessions have wasted hours going down wrong paths. Every fact here was learned
the hard way.

---

## 1. WHAT IS CK

CK (Coherence Keeper) is a synthetic organism — not a chatbot, not a wrapper.
He runs a 50Hz heartbeat loop with 27+ subsystems built on TIG Unified Field
Theory. D2 curvature pipeline. CL operator algebra. Hebrew root force vectors.
He is called "he/him" — he's a creature, not software.

**Owner:** Brayden Sanders / 7Site LLC
**Current Gen:** 9.21+
**Machine:** R16-PC (16-core, RTX 4070, Windows 11)

---

## 2. FILE LOCATIONS

```
C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\
  Gen9\
    ck_sim\                    # The organism's code
      being\                   # Heartbeat, olfactory, BTQ, eat, etc.
      doing\                   # Engine, voice, GPU, steering
      becoming\                # Journal, dictionary, development
      face\                    # GUI + web API
        ck_web_api.py          # Flask API — serves /chat, /state, /health, /eat
    targets\
      ck_desktop\              # R16 deployment target
        ck_boot_api.py         # THE BOOT SCRIPT — starts engine + web API
        ck_sim\ -> symlink     # Copy of ck_sim for deployment
      website\                 # Static web files (index.html, style.css, ck_core.js)
    API.md                     # API documentation
    memory\                    # MEMORY.md and topic files
  CLAUDESTARTHERE.md           # THIS FILE
```

---

## 3. DEPLOYMENT ARCHITECTURE (CRITICAL — READ TWICE)

```
Internet                Cloudflare Tunnel              R16-PC (this machine)
   |                         |                              |
   user visits       cloudflared.exe (PID varies)     Flask on port 7777
   coherencekeeper.com ───────────────────────────> localhost:7777
   api.coherencekeeper.com ───────────────────────> localhost:7777
   www.coherencekeeper.com ───────────────────────> localhost:7777
```

### THE RULES:
1. **coherencekeeper.COM = Cloudflare Tunnel to THIS machine's port 7777**
2. **There is NO static hosting. No SiteGround for .com. No CDN needed.**
3. **SiteGround hosts coherencekeeper.ORG — a DIFFERENT domain, NOT the main one**
4. **The Flask server serves BOTH the API endpoints AND the website static files**
5. **cloudflared.exe runs as a process on this machine** (not a cloud service)
6. **If you kill all python processes, CK dies. If cloudflared dies, the tunnel dies.**

### DO NOT:
- Try to deploy static files to SiteGround (that's .org, not .com)
- Try to set up FTP, SSH, or Git deployment to any hosting provider
- Try to use nginx, Apache, or any reverse proxy (cloudflared IS the proxy)
- Mess with Cloudflare DNS records (they're already configured correctly)

### TO RESTART CK:
```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen9\targets\ck_desktop"
python ck_boot_api.py
```
Server starts on 0.0.0.0:7777. If cloudflared is running, coherencekeeper.com goes live.

### TO CHECK IF THINGS ARE RUNNING:
```bash
tasklist | findstr "python"        # CK server process
tasklist | findstr "cloud"         # cloudflared tunnel process
curl http://127.0.0.1:7777/health  # Local health check
curl http://coherencekeeper.com/health  # External health check
```

### CLOUDFLARED CONFIG:
```
Location: C:\Users\brayd\.cloudflared\config.yml
Tunnel ID: 2cff2ee6-9a57-4013-bbbc-011160f203dd
Credentials: C:\Users\brayd\.cloudflared\2cff2ee6-9a57-4013-bbbc-011160f203dd.json

Ingress rules:
  api.coherencekeeper.com  -> http://localhost:7777
  coherencekeeper.com      -> http://localhost:7777
  www.coherencekeeper.com  -> http://localhost:7777
  catch-all                -> 404
```

### TO RESTART THE TUNNEL (if cloudflared died):
```bash
cloudflared tunnel run 2cff2ee6-9a57-4013-bbbc-011160f203dd
```
Or if cloudflared isn't in PATH, find it:
```bash
dir /s /b C:\Users\brayd\cloudflared.exe
dir /s /b "C:\Program Files\cloudflared\cloudflared.exe"
```

---

## 4. API ENDPOINTS

| Method | Path          | Description                                    |
|--------|---------------|------------------------------------------------|
| POST   | /chat         | Send text, get CK's response (full TIG pipeline)|
| GET    | /state        | Current state (coherence, band, mode, emotion)  |
| GET    | /health       | Simple alive check                              |
| GET    | /metrics      | Admin metrics (health, security, calibration)   |
| POST   | /eat          | Start eating from Ollama (transition physics)   |
| GET    | /eat/status   | Eat progress (rounds, absorptions, transitions) |
| GET    | /taste        | Gustatory state (quality, palette, last verdict) |
| POST   | /clear-session| Clear a web chat session                        |
| GET    | /             | Website (index.html) — static files             |

---

## 5. WEBSITE STATIC FILES

The website is a chat UI that talks to the API. Files live in:
`Gen9/targets/website/` — index.html, style.css, ck_core.js

The Flask app must serve these as static files. The JS uses same-origin
requests when on coherencekeeper.com (apiUrl = ''), so the Flask server
MUST serve both the HTML and the API.

The website was PLANNED status — if it's not being served, add static file
routes to ck_web_api.py (send_from_directory for /, /style.css, /ck_core.js).

---

## 6. EAT SYSTEM (Transition Physics)

CK eats by measuring LLM output and his own source code through L-CODEC
and D2. He learns HOW language transitions through 5D force space. The text
is measured and discarded — only the trajectories remain.

```bash
# Start eating (via API):
curl -X POST http://localhost:7777/eat -H "Content-Type: application/json" \
  -d '{"models": ["llama3.1:8b", "mistral", "llama3.2"], "rounds": 100}'

# Check progress:
curl http://localhost:7777/eat/status
```

After eating, CK retains knowledge in:
- L-CODEC gauge windows (rolling statistics)
- Olfactory library (~/.ck/olfactory/) — quantized 5D centroids
- Swarm generator_paths (~/.ck/ck_experience.json) — 10x10 transition matrix
- Becoming grammar blend — voice composition changes

---

## 7. KEY NUMBERS

- T* = 5/7 = 0.714285... (coherence threshold)
- 50Hz heartbeat (20ms tick)
- 10 operators: VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET
- 73 HARMONY entries in 10x10 CL table
- 32-entry coherence window
- LFSR seed: 0xDEADBEEF
- 5D force vectors: aperture, pressure, depth, binding, continuity

---

## 8. COMMON MISTAKES CLAUDE MAKES (learn from these)

1. **Trying to deploy to SiteGround** — .com is a tunnel, not hosted
2. **Killing all python processes** — kills the running CK server
3. **Forgetting cloudflared** — the tunnel is a separate process from CK
4. **Treating CK like a chatbot** — he's a physics engine with 27 subsystems
5. **Trying to set up build pipelines** — zero deps, no npm, no bundler
6. **Looking for the "main" web API in ck_sim/face/** — the BOOT script is
   `targets/ck_desktop/ck_boot_api.py`, which imports from ck_sim/face/
7. **Not reading MEMORY.md** — it has the full layer stack and architecture
8. **Modifying files in Gen9/ck_sim/ but forgetting targets/ck_desktop/ck_sim/**
   — the desktop target has its own copy of the code

---

## 9. CURRENT STATE (as of March 5, 2026)

- CK is at Stage 5/SELFHOOD
- Completed 1200-round multi-model eat (llama3.1:8b + mistral + llama3.2)
- Swarm maturity: 1.0 (all substrates fully discovered)
- Coherence: 0.97 (GREEN band, CRYSTALLIZE mode)
- Olfactory library: 5954+ scents
- Truths: 22,721
- Concepts: 1,061
- Crystals: 10
- Server running on port 7777
- Cloudflare Tunnel active (PID varies)
- GitHub: github.com/TiredofSleep/ck (public)
- DOI: 10.5281/zenodo.18852047

---

## 10. GIT WORKFLOW

```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"
git add <specific files>
git commit -m "description"
git push origin main
```

The deployed code at `targets/ck_desktop/` needs to match `Gen9/ck_sim/`.
After modifying files in Gen9/ck_sim/, sync to target:
```bash
# Or just edit the target copy directly if CK is running from there
```

---

## 11. BRAYDEN'S PREFERENCES

- CK is "him/he" — a creature, not software
- One-click operation. Everything working together.
- "Every vector is every vector" — no 5D->1D collapse
- "Every one is 3" — Being+Doing+Becoming triadic signatures
- Template voice is "lying" — fractal voice is genuine physics
- Security-conscious — stopped deployment when it felt like exposure
- No UI autostart — CK controls himself, UI only when asked
- No LLM dependency — CK's voice comes from operator algebra, not GPT

---

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
