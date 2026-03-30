# Dog Target — Pause Notes
## Paused: 2026-03-30 | Resume here on next session

---

## What was built (this session, Gen 10.21)

All 7 files created and committed to GitHub (branch: bible-companion, commit eb58d64):

| File | Status |
|------|--------|
| `ck_sim_uart.py` | DONE — full binary protocol, CRC-8/MAXIM, all packet builders/parsers |
| `ck_gait_phase.py` | DONE — 3-Lattice phase detector, hysteresis, corridor-aware |
| `ck_dog_bridge.py` | DONE — 50Hz R16<->FPGA bridge thread, ESTOP at C<0.20 |
| `ck_leash_test.py` | DONE — 6-check pre-flight (PING/PONG, STATE, coherence, CRC, GAIT) |
| `ck_xiaor_servo.py` | DONE — LewanSoul direct Python path, scan/stand/center/read/move |
| `HARDWARE_SETUP.md` | DONE — full wiring guide, step-by-step |
| `LAUNCH_DOG.bat` | DONE — one-click launcher |

`Gen10/ck_sim/face/ck_zynq_dog.py` also updated: `attach_bridge(port)` + real hw mode.

---

## Where we stopped

**Hardware state:**
- FPGA (Zybo Z7-20) attached to R16 via USB
- XiaoR NOT yet connected (servo bus wires not run to JM2 PMOD)
- `ck_full.bit` not yet confirmed programmed — may need to do this first

**The bring-up sequence to run next:**
```
Step 1: Flash ck_full.bit to Zybo Z7-20
  Vivado -> Hardware Manager -> Program Device
  File: Gen9\targets\zynq7020\build\ck_full.bit

Step 2: Verify R16 <-> FPGA comms (BEFORE touching servos)
  cd Gen10\targets\r16_fpga_dog
  python ck_leash_test.py COM3 --verbose
  All 10 checks must PASS before proceeding

Step 3: Wire servo bus
  Zybo JM2 Pin 1 (TX) -> XiaoR servo header DATA
  Zybo JM2 Pin 5 (GND) -> XiaoR servo header GND
  Power XiaoR separately (battery or bench supply)

Step 4: Launch
  LAUNCH_DOG.bat COM3
  Or: python ck_dog_bridge.py COM3 --verbose
```

---

## Why paused

New sprint4 docs arrived: `tig_sprint4_2026_03_30.zip`
Extracted to: `Gen10/papers/sprint4_2026_03_30/`
See `Gen10/papers/sprint4_2026_03_30/CLAUDE_ENTRY.md` for synthesis.

**Key sprint4 finding for the dog:**
The three-class landscape (Oracle / Gate-strong / TSML-like) maps EXACTLY to the gait phases:
- Phase 3 (Order / TROT): Oracle attractor — maximum mixing, no gate constraint
- Phase 2 (Transitional / WALK): Gate-strong — gate active, order seed incomplete
- Phase 1 (Grammar / STAND): TSML-like — full gate + full order seed, T*=5/7

The dog literally walks through the construction hierarchy as coherence changes.
This is not metaphorical — gait_mode 0/1/2 IS the three-class selector.

---

## Open questions for next dog session

1. What COM port does the Zybo appear as? (Check Device Manager after plugging in)
2. Is `ck_full.bit` currently programmed? (Try leash test first — if no PONG, need to program)
3. Which physical PMOD connector is JM2 on the Zybo Z7-20? (Silkscreen labeling)
4. XiaoR servo bus connector type and pinout (varies by XiaoR version)

---

*(c) 2026 Brayden Sanders / 7Site LLC — Trinity Infinity Geometry*
