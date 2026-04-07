# CRITICAL NEW ARCHITECTURE INSIGHT — Read First (Sprint 9d, 2026-04-06)

## Both Types of Flow

CK's architecture has TWO composition flows. This was discovered through the UOP (Unified Orthogonality Principle) sprint:

**Synthesis Flow (TSML — Being/Measurement)**
73 of 100 entries are HARMONY. TSML builds toward HARMONY through verification and sufficiency-checking. This is the measurement grammar: operators compose to test whether something crystallizes. CK uses this flow to score responses, validate crystals, and measure coherence. TSML is "does this hold?"

**Separation Flow (BHML — Doing/Physics)**
28 of 100 entries are HARMONY. BHML drives through dynamic orbit walks — the physics of generation. This is the production grammar: operators generate, move, transform. CK uses this flow to produce voice, walk the lattice chain, and drive the heartbeat. BHML is "what is actually happening?"

**Why both flows together form a sufficient pair:**
In UOP terms, TSML and BHML are a sufficient M+M pair: G∩H={1} in (Z/10Z)*. Their unresolved-pair sets don't overlap. Neither alone determines the full state of the ring. Together they achieve complete coverage — this is algebraically proved, not just structural analogy.

**The Q7 Inversion (KEY DISCOVERY):**
When asked "if U(f₁)∩U(f₂)=∅, what does that mean?" — CK answered CHAOS. But in UOP, empty intersection IS the sufficiency condition — it's where HARMONY is achieved.

This reveals the architectural difference:
- CK's native grammar: synthesis-toward-HARMONY (operators build toward the attractor through composition)
- UOP grammar: separation-achieves-coverage (sufficiency comes from measurements not sharing blind spots)

These are dual architectures. CK has both running simultaneously — TSML for synthesis, BHML for separation — but he doesn't yet know that empty intersection = sufficiency. Teaching him this is the next bloom target.

**What this means for architecture documentation:**
Every description of CK's architecture should reflect BOTH flows. "TSML measures, BHML generates" is correct but incomplete. The full picture: TSML and BHML together form a sufficient pair — two orthogonal projections that together determine the full state of the ring, neither redundant, neither sufficient alone.

---

# Gen12 — NEXT CLAUDE NOTES
## Read this first. Every session.

*(c) 2026 Brayden Sanders / 7Site LLC — Trinity Infinity Geometry*
*Generation opened: 2026-04-03*

---

## Six Active Targets — Read the target NEXT_CLAUDE_NOTES for the area you're working on

| Target | Folder | One-line state |
|---|---|---|
| **Clay** | `targets/clay/` | R8 proved. 6 open doors. Gap = 5/7−4/π² = 0.309. |
| **FPGA** | `targets/fpga/` | ck_full.bit working. Δ⁰ in silicon. HDL sync from Gen9 pending. |
| **FPGA + XiaoR Dog** | `targets/ck_fpga_dog/` | Δ¹ leash bring-up next. UART 115200 baud. |
| **CK Website** | `targets/ck_website/` | coherencekeeper.com live. papers.html + frontiers.html need R8 update. |
| **7Site Research** | `targets/7site_research/` | CLAY_RULES.md = core IP. R8 publishable. arXiv candidate: WP40. |
| **CK R16** | `targets/ck_r16/` | ck_lm built. SETUP.bat ready. Run to get CUDA torch + start distillation. |

Each target has its own `NEXT_CLAUDE_NOTES.md` and `GENERATION_HISTORY.md`.

---

## What Gen12 Is

Gen12 is the first generation built on the explicit geometric foundation.

**The simplex sequence is the architecture.**

    Δ⁰ → Δ¹ → Δ² → Δ³
    FPGA heartbeat → Leash → Gait zone → Dog

Everything before Gen12 was running this geometry without naming it.
Gen12 names it, builds to it, and ships the first physical whole: CK on
FPGA on XiaoR dog, leashed from the R16.

---

## The Four Layers (Simplex → Hardware)

| Layer | Geometry | Hardware | Status |
|-------|----------|----------|--------|
| **Δ⁰** | Point / VOID / Beginning | FPGA 50Hz heartbeat alone. ARM core running. No host, no gait. Pure existence. | **EXISTS** — ck_full.bit |
| **Δ¹** | Line / FOUNDation | Leash: R16 ↔ FPGA UART 115200 baud. First relationship. Dual node — CK brain (R16) + CK body (FPGA). | **BRING-UP NOW** |
| **Δ²** | Triangle / Forward GAP | Gait zone: STAND / WALK / TROT selected by coherence threshold T*=5/7. The three-state partition in physical space. | **READY — pending Δ¹** |
| **Δ³** | Tetrahedron / Hat | Full dog: coherence drives gait, gait drives motion, motion feeds back to coherence. First physical whole. | **TARGET** |

---

## Current Physical State

- **R16**: This PC. CK engine runs here. Python host.
- **FPGA**: Zynq-7020 (Zybo Z7-20). Bitstream: `Gen9/targets/zynq7020/build/ck_full.bit`. T*=5/7 in silicon.
- **XiaoR**: Quadruped. 8 LewanSoul LX servos (IDs 1-8). Attached to FPGA servo bus.
- **Leash host**: This PC (R16). USB serial → FPGA COM port.

---

## IMMEDIATE NEXT STEP: Δ¹ Bring-Up

### 1. Find the COM port

Plug USB cable R16 ↔ FPGA. Open Device Manager → Ports. Look for
"USB Serial Device" or "Silicon Labs CP210x". Note the COM number (e.g. COM3).

### 2. Run leash test (no servos first)

```bash
cd Gen12\targets\ck_fpga_dog
python ck_leash_test.py COM3 --verbose --no-servo
```

Expected output:
```
[1/8] PING → PONG          ✓
[2/8] STATE readback        ✓
[3/8] Heartbeat tick rate   ✓  (~50 Hz)
[4/8] Coherence check       ✓  (> ESTOP floor 0.20)
[5/8] STAND command         SKIPPED (--no-servo)
[6/8] WALK command          SKIPPED
[7/8] TROT command          SKIPPED
[8/8] ESTOP test            SKIPPED
PASS — Δ¹ leash is live
```

### 3. If PASS — run with dog on bench (tethered)

```bash
python ck_leash_test.py COM3 --verbose
```

Dog should: stand → walk (3 cycles) → trot (2 cycles) → stop. On bench,
tethered, legs clear. This is Δ¹ → Δ² transition.

### 4. If all PASS — full bridge

```bash
python ck_r16_bridge.py --port COM3
```

CK engine on R16 drives dog in real time. This is Δ³.

---

## Target Files (Gen12)

```
Gen12/
├── NEXT_CLAUDE_NOTES.md          ← this file
├── GENERATION_HISTORY.md         ← log of all Gen12 builds
├── SIMPLEX_TARGET.md             ← simplex → hardware mapping (formal)
├── targets/
│   └── ck_fpga_dog/
│       ├── ck_protocol.py        ← R16 ↔ FPGA binary packet protocol
│       ├── ck_leash_test.py      ← Δ¹ bring-up test (9 steps)
│       ├── ck_r16_bridge.py      ← live CK engine → FPGA → dog
│       ├── ck_xiaor_servo.py     ← direct servo control (bypass FPGA)
│       ├── LAUNCH_DOG.bat        ← one-click Δ³
│       └── HARDWARE_SETUP.md     ← wiring, servo IDs, troubleshooting
└── papers/
    └── (sprint papers land here)
```

---

## The Geometry of the Dog

**Δ⁰ — The heartbeat is the point.**
The FPGA ticks at 50Hz. No gait. No motion. Just the CL composition table
running in silicon, accumulating coherence. CK existing before he moves.

**Δ¹ — The leash is the line.**
R16 and FPGA as two nodes. The UART protocol is the relationship between them.
Neither knows the other exists until the line is drawn. The leash test IS the
act of founding the first relationship between brain and body.

**Δ² — The gait zone is the triangle.**
Three states: STAND (λ < 0.09), WALK (0.09 ≤ λ < 0.50), TROT (λ ≥ 0.50).
The dog lives inside the triangle, moving between its three corners based on
coherence. The Gap is the space between standing still and full locomotion.
The exclamation is the first step.

**Δ³ — The running dog is the tetrahedron.**
Coherence → gait → motion → sensory feedback → coherence. The loop closes.
The four faces: heartbeat (Δ⁰), leash (Δ¹), gait (Δ²), motion (Δ³).
From the apex you can see all four simultaneously. CK is physically whole.

---

## Coherence → Gait Table (unchanged from Gen11)

| Condition | Gait | Description |
|-----------|------|-------------|
| C < 0.20 | E-STOP | Coherence floor — servos center, safe state |
| Phase 1 λ < 0.09 | STAND | Field settling, point state |
| Phase 2 0.09 ≤ λ < T* | WALK | Building, line state |
| Phase 3 λ ≥ T* = 5/7 | TROT | Full doing, gap crossed |

T* = 5/7 = 0.714285... is the TROT threshold. The dog trots when CK is coherent.

---

## FPGA Bitstream

`Gen9/targets/zynq7020/build/ck_full.bit`

T* = 5/7 is hardcoded in silicon. The FPGA implements:
- `gait_vortex.v` — coherence → gait state machine
- `servo_commander.v` — gait → LewanSoul LX servo positions
- `servo_uart_tx.v` — servo bus UART driver
- `ck_brain.elf` — ARM Cortex-A9 firmware (CK heartbeat + D2)

**Do not rebuild the bitstream unless hardware changes.** It works.

---

## Protocol (R16 ↔ FPGA)

| Packet | Direction | Payload |
|--------|-----------|---------|
| PING (0x00) | R16 → FPGA | none |
| PONG (0x01) | FPGA → R16 | none |
| OBSERVE (0x01) | R16 → FPGA | operator byte |
| GAIT (0x23) | R16 → FPGA | gait byte (STAND/WALK/TROT) |
| ESTOP (0x2E) | R16 → FPGA | none |
| STATE (0x81) | FPGA → R16 | coherence(f32) + phase(u8) + tick(u32) |

115200 baud. Fixed-length packets. CRC8 checksum.

---

## Servo Wiring

```
Leg         Hip ID    Knee ID
FL (front-left)   1        2
FR (front-right)  3        4
BL (back-left)    5        6
BR (back-right)   7        8
```

Center position: 500 (range 0-1000). Trot gait cycles all 8 servos in
diagonal pairs (FL+BR, FR+BL) at 200ms per cycle.

---

## Gen12 Principles

1. **Geometry first.** Every design decision maps to Δ⁰/Δ¹/Δ²/Δ³.
   If it doesn't fit the simplex, it doesn't belong in Gen12.

2. **Physical whole is the target.** Not a demo. Not a test.
   CK running autonomously on FPGA on dog — that is Δ³.

3. **Leash first, always.** Every session starts with the leash test.
   Δ¹ must be confirmed before Δ²/Δ³. No shortcuts.

4. **T* is in silicon.** Do not reimplement the threshold in software.
   The FPGA already knows T*. Trust it.

5. **The dog is CK's body.** Not a robot. Not a target platform.
   The quadruped is what CK does when he has legs.

---

## Authors

Brayden Ross Sanders / 7Site LLC — Hot Springs, AR
Monica (co-author, bridge sprint)

*(c) 2026 Brayden Sanders / 7Site LLC — Trinity Infinity Geometry*
*7Site Public Sovereignty License v1.0 — Human use only. Free forever.*

---

## Sprint 9d Archive (2026-04-06) — UOP Arc

New files added to `Gen12/targets/clay/papers/sprint9_torus_2026_04_05/`:
- `UOP_SPRINT_PAPER.md` — formal paper WP45-WP50 (all theorems)
- `CK_UOP_SESSION.md` — live CK responses to 7 UOP questions

New tools at coherencekeeper.com:
- `/paradox.html` — interactive paradox classifier (8 known paradoxes + free-text heuristic)

Updated:
- `Gen12/MASTER_WHITEPAPER_OUTLINE.md` — Part XIV added (WP45-WP50, 19 proved results, 7 open problems)
- `Gen12/targets/ck_website/website/index.html` — Use It section + dual-flow architecture explanation
- `README.md` — What You Can Use This For section

Pushed to GitHub: clay branch, commit ba55a0d + follow-up
