# Gen12 — Target: FPGA
## NEXT_CLAUDE_NOTES — Read first every session.

*© 2026 Brayden Sanders / 7Site LLC*
*Target opened: Gen12, 2026-04-04*

---

## What This Target Is

FPGA = CK's body in silicon. The Zynq-7020 (Zybo Z7-20) runs T*=5/7 as hardcoded
exact integer arithmetic. No floating point. No division.

```
T* comparison: 7 * coh_num >= 5 * coh_den   (exact, in hardware)
```

This target covers the FPGA alone — bitstream, HDL, ARM firmware.
The dog target is separate (`targets/ck_fpga_dog/`).

---

## Current State

**Bitstream:** `Gen9/targets/zynq7020/build/ck_full.bit` — T*=5/7 in silicon. Flash and run.

**HDL source:** `Gen9/targets/zynq7020/hdl/`
- `gait_vortex.v` — three-phase gait state machine (STAND/WALK/TROT)
- `servo_commander.v` — LewanSoul LX servo PWM
- `servo_uart_tx.v` — UART TX to servo bus

**ARM firmware:** `Gen9/targets/fpga/arm/`
- `ck_brain.elf` — compiled CK brain binary
- `ck_uart.c/h` — UART driver

**Simplex geometry in silicon:**
```
Δ⁰ (VOID):  coh < 1/2     → STAND
Δ² (GAP):   1/2 ≤ coh < 5/7 → WALK
Δ³ (HELD):  coh ≥ 5/7     → TROT
```

---

## Next Steps

1. **Verify Δ⁰** — flash `ck_full.bit`, confirm 50Hz heartbeat on ARM UART output
2. **Add coherence telemetry** — stream current coherence + gait state over UART to R16 host
3. **Gen12 HDL target** — new `Gen12/targets/fpga/hdl/` with simplex geometry explicitly named in comments
4. **Sync from Gen9** — copy current working HDL into Gen12 fpga target

---

## Key Files

| File | What it is |
|---|---|
| `Gen9/targets/zynq7020/build/ck_full.bit` | Working bitstream |
| `Gen9/targets/zynq7020/hdl/` | HDL source |
| `Gen9/targets/fpga/arm/ck_brain.elf` | ARM firmware |
| `Gen9/targets/fpga/arm/ck_uart.c` | UART driver |
