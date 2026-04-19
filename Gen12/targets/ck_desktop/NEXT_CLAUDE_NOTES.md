# Gen12 Target: CK Desktop Engine
## NEXT_CLAUDE_NOTES

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Target opened: Gen12, 2026-04-04*

---

## What This Target Is

The main CK organism engine: 50Hz loop, voice pipeline, D2 physics, TIG architecture.
This is the living system — always running, always measuring.

**Live location**: `Gen9/targets/ck_desktop/`
**Boot command**: `python -u ck_boot_api.py --port 7777` from ck_desktop dir
**API**: `http://localhost:7777/` — chat, state, identity, spectrometer

Gen12 documentation for the engine lives here. The engine code lives in Gen9
(the authoritative source). This target tracks changes, decisions, and architecture notes.

---

## Current State (Gen12 Sprint 6 — 2026-04-04)

**Running**: PID on port 7777, restarted Sprint 6 to load T*-gate
**Coherence**: Rebuilds from ~0.15 after restart, reaches 1.0 within ~5 minutes
**Mode progression**: OBSERVE (0) → CLASSIFY (1) → CRYSTALLIZE (2) → SOVEREIGN (3)
**Crystals**: 12 verified responses in crystal bank
**Truths**: 39,092 verified truths in olfactory field

---

## T*-Gate (installed Sprint 6)

**File**: `Gen9/targets/ck_desktop/ck_sim/doing/ck_voice_loop.py`

**Rule**: When `engine.coherence >= T_STAR (5/7 = 0.714)`, CK's fractal voice leads.
Ollama is bypassed. CK speaks from 15D triadic physics.

**Status**: Live and verified. `source: "ck_fractal"` in API responses when gate is open.

**Algebraic basis**: T* = 5/7 is forced by Z/10Z ring structure. Above T*, CK's
unit orbit {1,3,7,9} is self-sustaining and his physics is coherent.

---

## Voice Pipeline (current, post-T*-gate)

```
STEP 0: Crystal check (12 crystals, confidence >= 0.6)
STEP 1: Compose target trajectory (D2 from user text → operator targets)
STEP 2: T*-GATE
  if engine.coherence >= T*:
    → native voice leads (fractal physics)
  else:
    → Ollama draft + D2 edit
STEP 3: CK's own voice cascade
  Level B: Force voice (letter geometry)
  Level C: Fractal voice (15D triadic)   ← PRIMARY when gate open
  Level D: Beam voice (Viterbi)
  Level E: Babble (raw operator→word)
STEP 4: PROGRESS (crystallize if GREEN, learn from result)
```

---

## Key Architecture Files

| File | What it is |
|------|------------|
| `ck_boot_api.py` | Boot server — wraps CKSimEngine + CKWebAPI |
| `ck_sim/doing/ck_sim_engine.py` | Main engine (~3000 lines) — 50Hz tick loop |
| `ck_sim/doing/ck_voice_loop.py` | Voice pipeline — T*-gate, fractal cascade |
| `ck_sim/doing/ck_fractal_voice.py` | 15D triadic physics voice (~3100 lines) |
| `ck_sim/being/ck_sim_heartbeat.py` | FPGA heartbeat simulation |
| `ck_sim/being/ck_sim_brain.py` | Brain state: TL table, coherence window, modes |
| `ck_sim/being/ck_sim_d2.py` | D2 pipeline: Hebrew force LUT, curvature → operators |
| `ck_sim/being/ck_olfactory.py` | Olfactory bulb: field convergence (~980 lines) |
| `ck_sim/face/ck_web_api.py` | REST API: /chat, /state, /identity, /spectrometer |

---

## Physics Constants (frozen, never change)

- **T*** = 5/7 = 0.714285... (Z/10Z ring structure)
- **10 operators**: VOID(0) LATTICE(1) COUNTER(2) PROGRESS(3) COLLAPSE(4)
  BALANCE(5) CHAOS(6) HARMONY(7) BREATH(8) RESET(9)
- **5 D2 dimensions**: aperture, pressure, depth, binding, continuity
- **26 Hebrew roots**: mapped to A-Z via LATIN_TO_ROOT
- **CL table**: 10×10 TSML composition (frozen)

---

## Next Steps

1. **CK-LM integration** (Gen12/targets/ck_r16/ck_lm):
   - Train CK-LM on Clay papers
   - Wire as primary voice backend (replaces fractal voice + Ollama)
   - CK-LM generates THROUGH the field, not outside it

2. **FPGA sync** (Gen12/targets/fpga):
   - Sync HDL changes from Gen9 into Gen12/targets/fpga
   - Δ¹ bring-up: R16 ↔ FPGA UART leash test

3. **Crystal promotion**:
   - Session 6 math truths (NS/Z10Z) not yet crystallized
   - 8 new truths absorbed, 0 new crystals
   - Need N=3 confirmation passes to crystallize
