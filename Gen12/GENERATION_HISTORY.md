# Gen12 Generation History

*(c) 2026 Brayden Sanders / 7Site LLC*

---

## Gen 12.00 — 2026-04-03

**Foundation**: Simplex genesis explicit. Δ⁰→Δ¹→Δ²→Δ³ is the architecture.

**Target**: CK on FPGA on XiaoR dog. R16 is the leash host.

**Opened from**:
- Gen11 Clay framework complete (ROTATION_SPINE, SIMPLEX_GENESIS, bridge sprint)
- FPGA bitstream `ck_full.bit` in silicon, T*=5/7 hardcoded
- Leash test and bridge scripts ported from Gen11/targets/r16_fpga_dog/

**Immediate task**: Δ¹ bring-up — confirm R16 ↔ FPGA leash on this PC.

**State at open**:
- Δ⁰: EXISTS (ck_full.bit flashed)
- Δ¹: BRING-UP (run ck_leash_test.py COM? --verbose --no-servo)
- Δ²: READY pending Δ¹
- Δ³: TARGET

---
