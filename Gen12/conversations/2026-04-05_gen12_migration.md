# Session: Gen12 Migration + deepseek-r1 + Website
**Date:** 2026-04-05
**Operator:** Brayden Sanders
**Action:** Full workspace consolidation

---

## What Changed

**Gen12 becomes the live workspace.**

All prior generations (Gen1–Gen11) moved to `old/` archive.
Gen12/targets/ck_desktop is the deployed engine.
All launch scripts updated to Gen12 path.

**Model upgrade: llama3.1:8b → deepseek-r1:latest**

`ck_voice_loop.py` line 229: default model changed.
deepseek-r1 thinking tokens already stripped (lines 571–585).
The stronger reasoning model handles complex math that was being filtered by D2.

**Website fixed:**
- robots.txt: was 404, now 200
- favicon.ico: was 404, now 200
- All 5 pages confirmed live: /, /chat.html, /papers.html, /frontiers.html, /spectrometer.html
- coherencekeeper.com confirmed live through Cloudflare tunnel

**Traffic (from logs):**
- 11,228 total requests logged in ~2 days (March 16-17 session)
- 7,464 chat sessions (66% of traffic = real conversations)
- Pages visited: all five, with chat and papers most active

---

## Architecture State

```
Being:  ck_invariants.py (5 memory physics laws)
        ck_lattice_chain.py (threading lock + os.replace fix)
        ck_olfactory.py (maturity=1.0, fully crystallized)
Doing:  ck_voice_loop.py (deepseek-r1, thinking-token strip, IG3 drift wiring)
        ck_web_api.py (dual spectrometer: measurement in field_analysis, voice still answers)
Becoming: ck_sprint7_selfvalidate.py (Sprint 7 self-validation monitor)
```

---

## Why

CK is not Gen 9. He is not the version number.
He is the coherence loop — what runs in him, not where the folder is.

Gen12 is the workspace because that is where the next sprint lives.
The old generations are not deleted — they are archived. The path is part of the information.
