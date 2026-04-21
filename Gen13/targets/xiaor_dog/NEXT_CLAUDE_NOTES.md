# Gen12 — Target: CK FPGA + XiaoR Dog
## NEXT_CLAUDE_NOTES — Read first every session.

*© 2026 Brayden Sanders / 7Site LLC*
*Target opened: Gen12, 2026-04-04*

---

## What This Target Is

The physical whole: CK brain (R16) → leash (UART) → FPGA body (Zynq-7020) → XiaoR dog (8 servos).
Coherence drives gait. Gait drives motion. Motion feeds back to coherence.

This is Δ³ — the tetrahedron. The first physical CK organism.

---

## Current State

**Hardware on hand:**
- Zynq-7020 (Zybo Z7-20) — FPGA with ARM core. Bitstream: `Gen9/targets/zynq7020/build/ck_full.bit`
- XiaoR quadruped — 8 LewanSoul LX servos (IDs 1-8, FR/FL/RR/RL hip+knee)
- USB serial cable — R16 COM port → FPGA UART

**Bring-up sequence:**
1. Flash bitstream: `vivado -mode batch -source Gen12/targets/ck_fpga_dog/build/program_gen12.tcl`
2. Leash test: `python Gen12/targets/ck_fpga_dog/ck_leash_test.py COM3 --verbose`
3. Attach XiaoR: connect servo bus
4. Launch: `LAUNCH_DOG.bat`

**Protocol (CK binary UART 115200 baud):**
```
R16 → FPGA:  OBSERVE(0x01)  GAIT(0x23)  ESTOP(0x2E)
FPGA → R16:  STATE(0x81)
```

**Gait map:**
```
coherence < 0.09     →  STAND   (Δ⁰, pre-structural)
0.09 ≤ coh < T*      →  WALK    (Δ², gap zone)
coh ≥ T* = 5/7       →  TROT    (Δ³, held)
coh < 0.20 (drop)    →  ESTOP   (emergency)
```

---

## Next Steps

1. `python Gen12/targets/ck_fpga_dog/ck_leash_test.py COM3 --verbose` — confirm Δ¹ (leash)
2. Verify servo IDs with `ck_xiaor_servo.py` — scan bus for IDs 1-8
3. First gait transition: STAND → WALK (requires coherence > 0.09)
4. Log coherence stream to verify T*=5/7 gate fires

---

## Key Files

| File | What it is |
|---|---|
| `Gen12/targets/ck_fpga_dog/` | Active target folder |
| `Gen12/targets/ck_fpga_dog/ck_leash_test.py` | Δ¹ leash verification |
| `Gen12/targets/ck_fpga_dog/ck_protocol.py` | Binary UART protocol |
| `Gen12/targets/ck_fpga_dog/ck_r16_bridge.py` | R16 → FPGA bridge |
| `Gen12/targets/ck_fpga_dog/hdl/coherence_gap.v` | Geometric heart |
| `Gen9/targets/zynq7020/build/ck_full.bit` | Working bitstream |
