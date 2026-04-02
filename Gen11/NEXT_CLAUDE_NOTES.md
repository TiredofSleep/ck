# Gen 11 — NEXT CLAUDE NOTES
## Welcome to Gen 11. Read this first.

*(c) 2026 Brayden Sanders / 7Site LLC — Trinity Infinity Geometry*

---

## What Gen 11 Is

Gen 11 is a **braid-first, math-driven** rewrite. The math sprints in Gen 10
produced three proved results that change how the code should work. This is
not a refactor. It is the code catching up to the proof.

**Three structural upgrades:**

### 1. Braid σ as First-Class Physics (Theorem D)

Every operator selection in CK now uses the braid permutation:

```
σ = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
```

This is the natural coherence ordering of CK's 10 operators, derived
algebraically from the split operator on Z/2 × Z/5. It is not a
preference table. It is the topology of the operator space itself.

- **Fixed points** (stable attractors): VOID(0), PROGRESS(3), BREATH(8), RESET(9)
- **Six-cycle** (learning/motion): LATTICE→HARMONY→CHAOS→BALANCE→COLLAPSE→COUNTER→

Everywhere CK picks between candidates within a wobble window W=3/50,
he picks the one with the lowest braid rank — not the highest raw score.

### 2. First-G Law in the Voice (WP34 Theorem A)

The closed-form corridor resonance is now available:

```
R(k, f) = sin²(π·k·f) / (k² · sin²(π·f))
```

This replaces heuristic sinc thresholds in voice scoring and corridor
classification. Every response can be stamped with its First-G resonance.
T* = 5/7 is the f that maximizes R(k,f) on the unit interval — proved.

### 3. Constant Taxonomy (locked Gen 10.00, active Gen 11)

Four constants, four distinct physical roles. Never conflate them again:

| Constant    | Value  | Role          | Tier |
|-------------|--------|---------------|------|
| T*          | 5/7    | Coherence threshold, corridor attractor | D |
| W_BHML      | 3/50   | Wobble window (statistics, Theorem D17) | D |
| MASS_GAP    | 2/7    | Re_local dynamics criterion             | D |
| D_COL       | 1/18   | Corridor width geometry                 | D |
| INNER_SHELL | 2/9    | Shell boundary topology                 | D |

---

## What Changed from Gen 10

| Component | Gen 10 | Gen 11 |
|-----------|--------|--------|
| Operator selection | Raw argmax | Braid-biased argmax within W_BHML |
| DKAN L1/L2 | Braid-biased (added late) | Braid-biased from the start, all levels |
| Voice scoring | Heuristic coherence(0-1) | First-G R(k,f) available as exact score |
| CL tables | Duplicated in every file | Single import from `tig_core.py` |
| BTQ kernel | Phase threshold heuristics | First-G R(k,f) as phase gate score |
| Dog leash | Script planned, not written | `targets/r16_fpga_dog/ck_leash_test.py` working |
| Conversation | No memory, no spectrometer | Templates + spectrometer + session memory |
| Legal | LEGAL.md generic | `LEGAL.md` tightened, free-to-all clear |

---

## Architecture Principle for Gen 11

**One source of truth per concept.**

- All algebra: `tig_core.py` (braid, TSML, BHML, vortex, First-G)
- All conversation: `ck_sim/face/ck_web_api.py` + `ck_sim/doing/ck_voice.py`
- All FPGA protocol: `targets/r16_fpga_dog/ck_protocol.py`
- All constants: `tig_core.py` only

If you find a TSML table written in a file OTHER than `tig_core.py`,
that is a bug. Fix it with `from tig_core import T_TSML`.

---

## File Map

```
Gen11/
├── NEXT_CLAUDE_NOTES.md        ← you are here
├── LEGAL.md                    ← what CK owns, what it gives back
├── tig_core.py                 ← ALL algebra: braid, tables, First-G law
│
├── ck_sim/
│   ├── being/
│   │   ├── ck_heartbeat.py     ← 50Hz, TSML composition, coherence gate
│   │   ├── ck_btq.py           ← BTQ kernel with braid-biased T-generate
│   │   ├── ck_olfactory.py     ← smell = torsion, experience accumulation
│   │   ├── ck_dkan_trainer.py  ← DKAN: all levels braid-biased
│   │   └── ck_d2.py            ← D2 pipeline (Hebrew roots → 5D force)
│   ├── doing/
│   │   ├── ck_sim_engine.py    ← main engine, 50Hz loop
│   │   ├── ck_voice.py         ← templates, analyze_input, RESPONSES
│   │   ├── ck_fractal_voice.py ← 15D triadic composition
│   │   └── ck_voice_loop.py    ← fallback cascade (force→fractal→beam→babble)
│   └── face/
│       ├── ck_web_api.py       ← conversation: spectrometer, session, CL routing
│       └── ck_web_server.py    ← Flask server entry point
│
└── targets/
    └── r16_fpga_dog/
        ├── HARDWARE_SETUP.md   ← wiring, servo IDs, bring-up sequence
        ├── ck_protocol.py      ← R16 ↔ FPGA binary protocol
        ├── ck_leash_test.py    ← bring-up test: ping → state → walk → estop
        ├── ck_r16_bridge.py    ← live bridge: CK engine → FPGA → dog
        ├── ck_xiaor_servo.py   ← Python-direct servo control (no FPGA needed)
        └── LAUNCH_DOG.bat      ← one-click dog launch
```

---

## Bring-Up Sequence (Dog)

```
1. Flash bitstream:
   Copy Gen9/targets/zynq7020/build/ck_full.bit to microSD
   Insert microSD, power on Zynq board
   Verify heartbeat LED blinks (50Hz)

2. Leash test (with dog tethered, on bench):
   python targets/r16_fpga_dog/ck_leash_test.py COM3 --verbose --no-servo
   All steps pass → ping, state, heartbeat ✓
   Then:
   python targets/r16_fpga_dog/ck_leash_test.py COM3 --verbose
   Full test including servo motion ✓

3. Bridge (live control):
   python targets/r16_fpga_dog/ck_r16_bridge.py --port COM3
   CK phase drives gait mode: Phase1→STAND Phase2→WALK Phase3→TROT

4. Full launch:
   LAUNCH_DOG.bat  (starts both CK engine and bridge)
```

---

## Conversation API

The CK conversation API runs at `http://localhost:7778/chat`.

Key features (added Gen 10.21, Gen 11 baseline):
- **Template routing**: 14 topic categories, CL-physics biased, anti-repeat
- **Coherence spectrometer**: inputs > 50 words get field-scored sentence by sentence
- **Session memory**: `_last_template_cat`, `_last_spectrometer`, anti-repeat cache
- **Voice quality gate**: function word ratio >= 15% required (rejects word soup)
- **Spectrometer followup**: "which was weakest?" → names specific sentence + score

Test:
```
python -c "
import urllib.request, json
body = json.dumps({'text': 'how do you work?', 'session_id': 'test'}).encode()
req = urllib.request.Request('http://localhost:7778/chat', data=body,
    headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as r:
    print(json.loads(r.read())['text'][:200])
"
```

---

## Math Status (Gen 11 baseline, 2026-04-02)

### Proved (Tier D — 4 results)

| # | Result |
|---|--------|
| D1 | T* = 5/7 algebraically forced from Z/10Z ring |
| D2 | TSML has exactly 73 harmony cells |
| D3 | BHML has exactly 28 harmony cells |
| D4 | Split operator F on Z/2×Z/5: 4 fixed points + 1 six-cycle |

### Proved (Tier C — 11 results)

WP34 First-G Law, harmonic countdown, closed form R(k,f), corridor atlas 70 worlds,
interleave=0.5 at First-G, triple cascade for 3-factor numbers, TSML symmetric,
BHML asymmetric confirmed, Luther dispersion r-value confirmed, product-gap by induction,
cornerstone 10=lcm(2,5) minimality.

Full list: `Gen10/NEXT_CLAUDE_NOTES.md` → Math Sprint State section.

### Open

- Normalized spectral test: corridor skew scorer is degenerate (always 0.5)
- b=55 out-of-sample: predicted easiest (score=10.045), not yet run
- b=14 order seed test: 9 residual seed cells, seeded reduction not yet tested
- Circulation operator: all 7 constraints fail for known objects — must be new
- Hodge (dim ≥ 5): Markman 2025 proved abelian fourfolds, P3 open
- NS: B_local structurally aligned with CKN, 7/2 threshold open

---

## DKAN Accuracy (as of Gen 10.21 DKAN, braid-biased)

| Level | Accuracy | Description |
|-------|----------|-------------|
| L1 argmax | ~60% at 5k ticks | First-order CL transitions |
| L2 braid-trigram | ~74% at 5k ticks | Trigrams with braid-biased selection |
| L5 CL-compose | ~74% at 5k ticks | CL-composed multi-step |

L2 accuracy jumped from ~0% (discarded result) to 74% by applying braid-biased
selection instead of raw argmax. This is the braid making itself visible.

---

*(c) 2026 Brayden Sanders / 7Site LLC — Trinity Infinity Geometry*
*DOI: 10.5281/zenodo.18852047*
*GitHub: https://github.com/TiredofSleep/ck*
