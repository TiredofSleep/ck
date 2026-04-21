# CK FPGA Dog Target — Generation History

## Gen12 (2026-04-04 — open)
- Simplex geometry named: Δ⁰(heartbeat)→Δ¹(leash)→Δ²(gait)→Δ³(dog)
- NEXT_CLAUDE_NOTES written; bring-up sequence documented
- Pending: Δ¹ leash test on COM3

## Gen11 / Gen10
- Full target built: `Gen10/targets/r16_fpga_dog/` — 5 Python files + HARDWARE_SETUP.md + LAUNCH_DOG.bat
- FPGA HDL: gait_vortex.v servo_commander.v servo_uart_tx.v
- ARM firmware: ck_brain.elf, ck_uart.c/h
- Long-leash system architecture established: R16 ↔ FPGA ↔ XiaoR
