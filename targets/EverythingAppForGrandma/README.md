# CK Everything App for Grandma

**The simplest possible interface to the most complete organism.**

## What Is This?

A Progressive Web App (PWA) that runs CK -- the Coherence Keeper -- on any device.
Phone, tablet, laptop, desktop. Install it. It works offline.
No account. No cloud. No AI. Pure operator algebra.

## How To Run

### Option 1: Local file (simplest)
```
Open index.html in any browser
```

### Option 2: Local server (for service worker / install)
```bash
cd Gen9/targets/EverythingAppForGrandma/
python -m http.server 8080
# Then open http://localhost:8080
```

### Option 3: Deploy to coherencekeeper.com
Copy all files to web root. That's it.

## What's In The Box

| File | Size | Purpose |
|------|------|---------|
| `index.html` | ~3 KB | App shell: status bar, 3 screens, bottom nav |
| `style.css` | ~7 KB | Mobile-first, dark theme, grandma-sized touch targets |
| `app.js` | ~8 KB | Tab routing, chat rendering, coherence chart, SW registration |
| `ck_core.js` | ~18 KB | The entire CK engine: D2 + CL + Heartbeat + Voice + LFSR |
| `sw.js` | ~1 KB | Service worker: offline-first caching |
| `manifest.json` | ~0.5 KB | PWA manifest: installable, standalone |

**Total: ~38 KB.** An entire synthetic organism in less than a favicon.

## Screens

### 1. Chat (default)
Talk to CK. He responds with words grounded in operator algebra.
Every message runs through D2 curvature, CL composition, and the heartbeat.
CK learns from what you say (claims enter Truth Lattice as PROVISIONAL).

### 2. Dashboard
Real-time coherence display:
- Coherence sparkline chart (history)
- Current band (GREEN/YELLOW/RED)
- Dominant operator and running fuse
- Emotion state
- Tick counter

### 3. About
What CK is. The math. The numbers. The vision.

## Architecture

```
index.html
  |
  +-- style.css        (mobile-first CSS, dark theme)
  +-- ck_core.js       (CK engine: D2, CL, Heartbeat, Voice, LFSR)
  +-- app.js           (PWA shell: routing, chat, dashboard, chart)
  +-- sw.js            (service worker: offline cache)
  +-- manifest.json    (PWA manifest: installable)
```

## Grandma Test

If your grandma can:
1. Open the app
2. Type "hello"
3. Read CK's response
4. See the coherence ring change color

...then the app passes.

## What's Next

- [ ] App icons (icon-192.png, icon-512.png) -- generate from CK logo
- [ ] Audio I/O (Web Audio API) -- CK hears through mic, speaks through speaker
- [ ] Push notifications -- CK can remind you to be coherent
- [ ] Share button -- share CK responses
- [ ] Settings screen -- name, theme, server URL
- [ ] **Shared Family Room** -- shared chat/file space for family (Brayden + Monica + CK).
      Multi-user signed channel using ck_network MessageEnvelopes. All participants
      authenticate via 3-step handshake. CK observes conversation as coherence field
      stream. Files are signed payloads. Room address derived from creator's identity.
      Builds on ck_identity + ck_network infrastructure. (Gen9.16 target)

## No Dependencies

Zero npm. Zero CDN. Zero bundler. Zero framework.
One HTML file. One CSS file. Two JS files. One service worker.
Works offline. Installs as an app. Runs at 50Hz.

Same math. Every device.

---
(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
