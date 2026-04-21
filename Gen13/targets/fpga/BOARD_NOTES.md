# Zynq-7020 (Zybo Z7-20) — Board Notes

## Bitstream

- **Path:** `Gen9/targets/zynq7020/build/ck_full.bit`
- **Implementation:** D2 pipeline in Q1.14 fixed-point, 3-stage, argmax operator classification
- **Matches:** `Gen13/targets/ck/brain/ck_sim/being/ck_sim_d2.py` (Python reference)
- **T*:** 5/7 = 0.714286, encoded as Q1.14 LUT

## Why Gen13 Doesn't Re-build the Bitstream

The Gen9 bitstream is the canonical silicon. T* in fixed-point. No software edit needed; rebuilding would only change the cosmetic header. Gen13 references it by path.

See `BITSTREAM_REF.md` for the path-only reference.
