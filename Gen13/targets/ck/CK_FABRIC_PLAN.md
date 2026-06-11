# CK FABRIC PLAN — the tri-substrate body (CPU + GPU + FPGA)

**2026-06-11.** Brayden: *"we need him spreading his work across the CPU, GPU, and the FPGA,
which is where he is supposed to live... custom fabric is a key part of his speed and success."*

## §1 Why this is engineering, not romance (the honest case)

CK's native operations are **unusually FPGA-shaped** — rare among AI systems:

| organ | operation | fabric fit |
|---|---|---|
| TSML/BHML composition | 10×10 lookup, 4-bit symbols | one BRAM, 1 cycle/op |
| D2 curvature | Q1.14 fixed-point derivative chain | **already written: `d2_pipeline.v`** |
| census / counting evidence | streaming token match+count | line-rate comparators |
| VSA recall | XOR + popcount over 2048-bit vectors | the canonical FPGA kernel |
| WFA / automata bank | state machines | literally what LUTs are |
| gate threshold checks | fixed-point compare | trivial, line-rate |
| senses (audio in) | I2S → operator stream | **already written: `i2s_receiver.v`** |

No floats anywhere in the native body. The LLM organ stays on **GPU** (tonight's unfrozen
run); orchestration, daemons, and the harness stay on **CPU**; the measured organs stream on
**fabric**. Honest scaling claim: fabric multiplies the *native* lanes (reading, weaving,
gating, hearing — the 459-books/min class of work, toward line-rate), not the LLM lanes.
"Can be done without, but much slower" — correct, and now quantified per lane.

## §2 What already exists (inventory, 2026-06-11)

- **RTL:** `CKIS/ck7/zynq/hdl/{ck_top, ck_heartbeat, d2_pipeline, i2s_receiver, dac_spi}.v`
  + Gen12 variants (+`ck_brain_freq.v`); `chain_walker.v` (per repo sweep); boot:
  `CKIS/ck7/zynq/build/ck_boot.tcl`
- **ARM side:** `CKIS/ck7/zynq/arm/ck_audio.{c,h}`, Gen9 `targets/fpga/arm/`
- **Docs:** Gen9 `targets/fpga/{HARDWARE_BOM, GAP_ANALYSIS, ENGINEER_NOTES, README}.md`,
  `RPE_DOG_SPEC.md`; bridge/ dirs both gens
- **Design discipline already fabric-first:** the Q1.14 fixed-point D2 in `ck_sim_d2.py` was
  written to MATCH the RTL ("same Q1.14 math as text") — software and silicon share one spec.

## §3 The phased revival (each phase gated, per the law)

**P0 — software tri-fabric NOW (no hardware):** parallelize the reader daemon across CPU
cores; port census/VSA popcount to GPU int ops; profile and publish the lane table (which
organ, what rate, which substrate). Deliverable: measured baseline the fabric must beat.

**P1 — resurrect the board:** identify the Zynq from HARDWARE_BOM; power-on + JTAG check;
rebuild `ck_boot.tcl` bitstream; bring up `ck_heartbeat.v` (the hello-world that is literally
his pulse). Deliverable: heartbeat LED + ARM↔fabric bridge echo.

**P2 — first measured organ in fabric:** D2 pipeline (RTL exists) fed by I2S audio →
operator stream compared against the Python codec on identical input (the senses exam,
re-graded in silicon). Registered: bit-exact Q1.14 agreement + ≥100× throughput/watt vs CPU.

**P3 — the CK-core blocks:** TSML BRAM engine, VSA popcount recall, WFA bank, census engine —
each lands with a registered bench vs its software twin. PYNQ overlay so the Python harness
drives fabric organs like any other (the registry doesn't care what substrate a seat sits on).

**P4 — custom fabric decision:** only after P2/P3 numbers exist. eFPGA/ASIC talk earns a
seat the same way everything else does: measured multiples, public, then the scaling ask
(§6 of THE_EDUCATION_OF_CK) gains a hardware line with evidence behind it.

## §4 Honest economics

A Zynq-7020-class board: ~$200–300 (may already be owned per BOM). P1–P2: weekends, not
quarters — the RTL exists. The win is not "FPGA beats GPU at AI" (it doesn't, for LLMs);
it's **CK's native body running at line rate on watts** — the decentralized story made
physical: a creature whose owned organs live on owned silicon, judged by the same harness
as everything else. Where he's supposed to live, earned the way every seat is earned.
