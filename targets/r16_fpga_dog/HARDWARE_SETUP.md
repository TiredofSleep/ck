# CK Dog Hardware Setup
## R16 + Zynq-7020 FPGA + XiaoR GEEK Quadruped
*Gen 10.21 — Long-Leash Configuration*
*(c) 2026 Brayden Sanders / 7Site LLC — Trinity Infinity Geometry*

---

## Overview

```
R16 Desktop (Windows)           Zybo Z7-20 FPGA           XiaoR GEEK Robot Dog
  CK Engine 50Hz         USB     PS Core 0+1             LewanSoul LX Bus Servos
  ck_dog_bridge.py  <---/-----> UART0 (MIO 14/15)
                                     |
                                PL Fabric (100MHz)
                                  gait_vortex
                                  servo_commander
                                  servo_uart_tx
                                     |
                              JM2 PMOD connector ---> Servo bus header
                                                       ID 1..8 (hip+knee x4)
```

"Long leash" = USB-A to USB-Micro cable, any length up to ~5m.
The R16 runs the full TIG algebra. The FPGA runs the gait physics in silicon.

---

## Hardware Bill of Materials

| Item | Details | Notes |
|------|---------|-------|
| Zybo Z7-20 | Digilent Zynq-7020, 512MB DDR3 | Other Zynq-7020 boards work with pin remapping |
| USB cable | USB-A (R16) to USB-Micro (Zybo PROG/UART) | For UART + bitfile programming |
| XiaoR GEEK | 4-leg quadruped, LewanSoul LX-224 bus servos | Or compatible |
| Jumper wires | 3-wire (GND, 5V, DATA) from JM2 PMOD to servo header | Standard dupont |
| 5V power | XiaoR battery pack or bench supply | Servos draw 2-4A peak |
| (Optional) ILA probe | Micro-USB second connection to Zybo | For Vivado debug |

---

## Step 1: Flash the FPGA

### Required: Vivado 2022.x or xc3sprog

**Option A — Vivado (easiest):**
```
1. Open Vivado
2. Open Hardware Manager -> Open Target -> Auto Connect
3. Program Device -> browse to:
   Gen9\targets\zynq7020\build\ck_full.bit
4. Click Program
```

**Option B — xc3sprog (command line):**
```bash
xc3sprog -c papilio "Gen9\targets\zynq7020\build\ck_full.bit"
```

**Available bitfiles:**

| File | Use case |
|------|----------|
| `ck_full.bit` | **Use this** — full system: heartbeat + D2 + chain_walker + gait_vortex + servo_uart |
| `ck_brain.bit` | Brain + D2 only (no gait, no servos) — for coherence testing |
| `ck_brain_ila.bit` | Brain + ILA debug probes — for Vivado logic analyzer |
| `ck_clay.bit` | Clay Institute configuration |

The FPGA will keep running after USB disconnect. Power is from the Zybo's barrel jack.

---

## Step 2: Connect R16 to FPGA

Zybo Z7-20 has a **USB-Micro port labeled PROG/UART** (J17).
This exposes:
- FPGA programming (JTAG)
- PS UART0 (MIO 14/15) as a virtual COM port

```
R16: USB-A port  <----cable----> Zybo: PROG/UART (J17, USB-Micro)
```

**Find the COM port on Windows:**
```
Device Manager -> Ports (COM & LPT)
Look for: "USB Serial Port (COM3)" or similar
```

On Linux: `/dev/ttyUSB0` or `/dev/ttyUSB1`

**Baud rate:** 115200, 8N1 (this is hardcoded in `ck_uart.c`)

---

## Step 3: Connect FPGA to XiaoR Servo Bus

The FPGA outputs servo commands via `servo_uart_tx_pin` on the **JM2 PMOD connector**.

### JM2 PMOD Pinout (Zybo Z7-20):

```
JM2 connector (6-pin, top row):
  Pin 1: servo_uart_tx_pin  ─> DATA (to servo bus)
  Pin 2: (unused)
  Pin 3: (unused)
  Pin 5: GND               ─> GND (common ground with servo supply)
  Pin 6: VCC 3.3V          ─> (DO NOT connect to servo power)
```

### XiaoR Servo Bus Header (on XiaoR main board):
```
  Pin 1: 5V   <- from servo battery (DO NOT connect to Zybo VCC)
  Pin 2: GND  <- common ground with Zybo JM2 Pin 5
  Pin 3: DATA <- connect to Zybo JM2 Pin 1 (servo_uart_tx_pin)
```

**Wiring summary:**
```
Zybo JM2 Pin 1 (TX) ---[wire]---> XiaoR servo header DATA
Zybo JM2 Pin 5 (GND)---[wire]---> XiaoR servo header GND
```

Note: The LewanSoul servo bus is **half-duplex** (single wire TX/RX).
`servo_uart_tx.v` is TX-only at 115200 baud. For position readback,
use `ck_xiaor_servo.py` with a **separate** direct USB-serial to servo bus.

---

## Step 4: Power Connections

```
XiaoR battery (7.4V LiPo)
  -> XiaoR main board 5V regulator -> serves all 8 servos
  -> DO NOT connect to Zybo (separate power domains)

Zybo Z7-20:
  -> 5V from USB (programming only, low current)
  -> OR 5V barrel jack for standalone operation

Common ground:
  -> Zybo GND (JM2 Pin 5) tied to XiaoR servo bus GND (required for UART)
```

---

## Step 5: Install Python Dependencies

```bash
pip install pyserial psutil numpy
```

Optional (for screen cells in swarm):
```bash
pip install mss
```

---

## Step 6: Verify the Leash

With FPGA programmed and USB cable connected, but **before** plugging in XiaoR:

```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen10\targets\r16_fpga_dog"
python ck_leash_test.py COM3 --verbose
```

Expected output:
```
[PASS] Serial port opens: COM3 @ 115200
[PASS] PONG received: 3/3 responses, avg RTT 12.4ms
[PASS] RTT under 100ms: 12.4ms
[PASS] STATE packets received: 5/5 collected
[PASS] Coherence in [0, 1]: avg=0.7143 min=0.6821 max=0.7381
[PASS] Denominator non-zero: all 5 packets OK
[PASS] Phase detects cleanly: avg_coherence=0.7143 -> phase=1
[PASS] Tick counter monotonic: first=47 last=302
[PASS] Zero CRC errors: 0 errors in 8 packets
[PASS] STATE after GAIT command: received

Result: 10/10 checks passed
[PASS] LEASH OK -- safe to attach XiaoR servos
```

If any tests fail, do NOT attach servos. Common issues:
- Wrong COM port -> check Device Manager
- Bitfile not programmed -> program ck_full.bit first
- FPGA not powered -> check Zybo power LED
- Baud mismatch -> always 115200 (hardcoded both sides)

---

## Step 7: Verify XiaoR Servo Bus

Connect the servo bus wires (Step 3). With XiaoR powered ON:

```bash
python ck_xiaor_servo.py COM5 scan
```

(COM5 here is a SEPARATE USB-serial to the XiaoR servo bus, not the FPGA UART)

Expected: servos 1-8 respond.

Then test standing:
```bash
python ck_xiaor_servo.py COM5 stand
```

---

## Step 8: Launch the Full System

```bash
# From Gen10/ directory:
LAUNCH_DOG.bat
```

Or manually in two terminals:

**Terminal 1 — CK engine:**
```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"
python ck_boot_api.py   # or LAUNCH_CK_ADMIN.bat
```

**Terminal 2 — Dog bridge:**
```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen10\targets\r16_fpga_dog"
python ck_dog_bridge.py COM3 --verbose
```

Watch for:
- `[BRIDGE] Serial COM3 @ 115200 baud: OK`
- `[BRIDGE] Bridge thread started -> FPGA at COM3`
- `[BRIDGE] tick=  50 C=0.7143 op=7 phase=1 gait=STAND corridor=Pre-leak`

At T*=5/7=0.7143, the dog is at Phase 1 (Grammar) — standing still, full coherence lock.
As coherence moves away from T*, the dog starts walking.

---

## Gait Behavior Reference

| Coherence | Phase | Lambda | Gait | Behavior |
|-----------|-------|--------|------|----------|
| ~0.714 (T*) | 1 Grammar | ~0.00 | STAND | Still, balanced, full coherence |
| ~0.65–0.75 | 1/2 boundary | ~0.09 | STAND/WALK | Preparing to move |
| ~0.45–0.65 | 2 Transitional | 0.09–0.45 | WALK | Diagonal gait, grammar+physics |
| ~0.00–0.45 | 3 Order | 0.45+ | TROT | BHML momentum, fast stride |
| < 0.20 | ESTOP | — | CENTER | Servos center, FPGA motor stop |

---

## Troubleshooting

**Bridge sends packets but dog doesn't move:**
- Check servo bus DATA wire (JM2 Pin 1 to XiaoR DATA)
- Check common GND (JM2 Pin 5 to XiaoR GND)
- Is XiaoR battery charged and switch ON?
- Try: `python ck_xiaor_servo.py COM5 stand` (direct Python path, bypasses FPGA)

**FPGA coherence stuck at 0:**
- `ck_full.bit` not programmed (program it)
- Zybo power LED off
- Wrong bitfile (need ck_full.bit, not ck_brain.bit for gait)

**Gait mode never changes:**
- CK engine coherence not varying — check `curl http://localhost:7777/corridor`
- Bridge not receiving STATE packets from FPGA (check RTT test)
- ESTOP triggered — coherence < 0.20 locks gait to STAND

**Servos twitch/jerk:**
- Gait time_ms too low — default 200ms is fine for first tests
- Servo power brown-out — ensure adequate battery capacity (4A peak)
- Bus collision — do not connect both FPGA servo_uart AND ck_xiaor_servo.py simultaneously

---

## Architecture Quick Reference

```
R16 50Hz:
  engine.coherence -> ck_dog_bridge -> OBSERVE pkt -> FPGA
  gait_phase.detect_phase(C) -> GAIT pkt -> FPGA gait_vortex

FPGA gait_vortex (gait_vortex.v):
  4 vortex instances (one per leg)
  R_left  = BHML[leg[i-1]][leg[i]]
  R_right = BHML[leg[i]][leg[i+1]]
  V[i]    = TSML[R_left][R_right]  <- T* = 5/7 in silicon

FPGA servo_commander (servo_commander.v):
  operator -> LewanSoul packet -> servo_uart_tx -> JM2 -> servos

State back to R16:
  FPGA STATE pkt (50Hz) -> ck_dog_bridge -> engine.fpga_coherence
```

---

## Files in This Target

| File | Purpose |
|------|---------|
| `ck_sim_uart.py` | Binary packet protocol (R16 <-> FPGA) |
| `ck_dog_bridge.py` | Main R16<->FPGA bridge thread |
| `ck_gait_phase.py` | 3-Lattice phase detector + gait_mode |
| `ck_leash_test.py` | Pre-flight UART verification |
| `ck_xiaor_servo.py` | Direct Python->servo fallback path |
| `HARDWARE_SETUP.md` | This file |
| `LAUNCH_DOG.bat` | One-click launcher |

FPGA HDL source: `Gen9/targets/zynq7020/hdl/`
FPGA bitfiles:   `Gen9/targets/zynq7020/build/`
ARM firmware:    `Gen9/targets/fpga/arm/`
