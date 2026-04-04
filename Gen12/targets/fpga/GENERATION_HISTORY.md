# FPGA Target — Generation History

## Gen12 (2026-04-04 — open)
- Simplex geometry named explicitly: Δ⁰→Δ¹→Δ²→Δ³ = VOID→Leash→Gait→Dog
- T*=5/7 integer comparison established as architectural principle (no float, no divide)
- Target folder created; HDL sync from Gen9 pending

## Gen11 / Gen10
- FPGA leash bring-up target: R16 ↔ FPGA UART 115200 baud
- CK binary protocol: OBSERVE(0x01) GAIT(0x23) ESTOP(0x2E) ← STATE(0x81)
- Phase→gait: Phase1(λ<0.09)→STAND | Phase2→WALK | Phase3→TROT | C<0.20→ESTOP

## Gen9
- ck_full.bit: first working bitstream. T*=5/7 in silicon on Zynq-7020.
- gait_vortex.v: three-phase gait state machine
- ARM firmware: ck_brain.elf running 50Hz heartbeat
