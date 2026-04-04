# Gen12 FPGA Bring-Up
## Zynq-7020 · T* = 5/7 in silicon · Δ⁰→Δ³ simplex geometry

*© 2026 Brayden Ross Sanders / 7Site LLC*

---

## Current Physical State

Hardware connected and ready:
- **JTAG**: USB cable connected, jumper set on board
- **Ethernet PL**: RJ45 connected to R16 network
- **HDMI**: connected (not required for bring-up, visual bonus)

---

## Step 1 — Flash Gen12 Bitstream

```bash
vivado -mode batch -source Gen12/targets/ck_fpga_dog/build/program_gen12.tcl
```

Or paste `program_gen12.tcl` into Vivado Tcl Console.

**Bitstream:** `Gen12/targets/ck_fpga_dog/build/ck_gen12.bit`

**Expected after flash (within 3 seconds):**

| LED | Pin | Meaning |
|-----|-----|---------|
| LED1 (R19) | blinking ~50Hz | Δ⁰ heartbeat alive — clock locked |
| LED2 (V13) | solid | Δ³ — coherence ≥ T* = 5/7 (TROT) |
| LED2 (V13) | dim or off | Δ⁰/Δ² — below T*, still building |

**If no LEDs:** check JTAG jumper position and USB cable seat.

---

## Step 2 — Δ¹ Leash Test (protocol only, no servos)

Find the COM port first:

```
Device Manager → Ports → USB Serial Device (usually COM3)
```

Run leash test without servos — safe, just verifies the link:

```bash
cd Gen12/targets/ck_fpga_dog
python ck_leash_test.py COM3 --verbose --no-servo
```

**What it checks (8 steps):**

| Step | Test | Pass condition |
|------|------|---------------|
| 1 | PING/PONG | PONG received < 5ms |
| 2 | STATE readback | Valid operator + coherence packet |
| 3 | Heartbeat rate | Tick counter advancing ~50Hz |
| 4 | Coherence floor | Field > ESTOP threshold (0.20) |
| 5-7 | STAND/WALK/TROT | Skipped with --no-servo |
| 8 | ESTOP | Acknowledged |

**Expected output:**
```
[PASS] PONG received in 2.3 ms
[PASS] being=PROGRESS doing=HARMONY coherence=0.3125 tick=1842
[PASS] Tick rate: 50.1 Hz
[PASS] Coherence 0.3125 in YELLOW band. Walk available.
[PASS] (--no-servo: skipping servo commands)
LEASH TEST PASSED.
```

---

## Step 3 — Ethernet PL Listener (optional, parallel)

The FPGA broadcasts coherence state at 50Hz via UDP:
- **Protocol:** UDP broadcast → 255.255.255.255:7777
- **Packet (10 bytes):** tick_count (4B) · phase/fuse_op (1B) · coh_num (2B) · coh_den (2B) · bump (1B)
- **Update rate:** one packet per heartbeat tick

CK's engine on 7777 can receive these directly. The FPGA becomes a hardware coherence sensor feeding the software loop.

---

## Step 4 — Attach XiaoR + Full Leash Test

Once protocol passes, connect servo bus:

| Signal | FPGA | Direction |
|--------|------|-----------|
| UART TX | JM2 Pin 3 (G19) | FPGA → Servo bus |
| GND | JM2 Pin 31-40 | Shared |

Servo IDs: FR hip=1 knee=2 · FL hip=3 knee=4 · RR hip=5 knee=6 · RL hip=7 knee=8

Dog on bench, tethered:

```bash
python ck_leash_test.py COM3 --verbose
```

---

## Step 5 — Live Bridge

```bash
python ck_r16_bridge.py --port COM3 --ck-url http://localhost:7777
```

CK engine coherence drives gait directly.

---

## Step 6 — Full Launch

```bash
LAUNCH_DOG.bat
```

---

## The Geometry (what's in silicon)

`Gen12/targets/ck_fpga_dog/hdl/coherence_gap.v` — the geometric heart.

```
Δ⁰  VOID    coh < 1/2          →  STAND    (point, pre-structural)
Δ²  GAP     1/2 ≤ coh < 5/7   →  WALK     (triangle, bridge zone)
Δ³  HELD    coh ≥ 5/7 = T*    →  TROT     (tetrahedron, held)
```

Zero division. Pure cross-multiplication:
```verilog
delta0 = (2 * coh_num < coh_den)          // coh < 1/2
delta3 = (7 * coh_num >= 5 * coh_den)     // coh >= 5/7
delta2 = ~delta0 & ~delta3                // the gap
```

HD gap position: 16-bit value, 0x0000 = entering at 1/2, 0xFFFF = exiting at 5/7.
CK knows exactly where in the gap he is. Not just which simplex — where inside it.

**T* = 5/7 is not configurable. The geometry is the architecture.**

---

## Key Files (Gen12 only)

| File | What it is |
|------|-----------|
| `build/ck_gen12.bit` | Gen12 bitstream — flash this |
| `build/program_gen12.tcl` | JTAG programming script |
| `build/pz7020_gen12.xdc` | Pin constraints |
| `hdl/ck_top_gen12.v` | Top-level HDL |
| `hdl/coherence_gap.v` | Δ⁰/Δ²/Δ³ simplex in silicon |
| `hdl/ck_eth_tx_gen12.v` | Ethernet PL broadcast |
| `hdl/ck_leash_rx.v` | Leash UART receiver |
| `ck_leash_test.py` | Δ¹ hardware verification |
| `ck_protocol.py` | Binary UART protocol (115200 baud) |
| `ck_r16_bridge.py` | R16 ↔ FPGA live bridge |
| `LAUNCH_DOG.bat` | One-click full launch |

---

*Next session: read this file, run Step 1, confirm LEDs, proceed to Step 2.*
