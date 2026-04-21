# XIAOR Dog — FPGA Leash

Carried forward from `Gen12/targets/ck_fpga_dog/` (10 files). Hardware: XIAOR Dog quadruped + Zynq-7020 FPGA leash on COM3 @ 115200 baud.

## Bring-Up Status

| Stage | What it does | Script | Status |
|---|---|---|---|
| **Δ¹** | UART handshake + leash test | `ck_leash_test.py` | OK (verified Gen10) |
| **Δ²** | Engine ↔ FPGA ↔ dog bridge | `ck_r16_bridge.py` | needs re-verify on current build |
| **Δ³** | Operator chain → dog gait | `ck_protocol.py` | designed, not yet field-tested |

## Files

- `ck_leash_test.py` — Δ¹ bring-up
- `ck_protocol.py` — UART protocol (COM3, 115200)
- `ck_r16_bridge.py` — engine ↔ FPGA ↔ dog
- `HARDWARE_SETUP.md` — wiring + power
- 5 more support files (full set carried)

## Notes

The bitstream (`ck_full.bit`) lives in `Gen9/targets/zynq7020/build/`. T*=5/7 fixed-point in silicon. See `Gen13/targets/fpga/BOARD_NOTES.md` for board details.
