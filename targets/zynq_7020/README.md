# CK on Zynq-7020 -- Bare Metal FPGA on XiaoR Robot Dog

**STATUS: PLANNED** -- Not active until R16 deployment is satisfactory.

The Zynq-7020 is CK's silicon body. Bare metal FPGA strapped to a XiaoR Geek robot dog.
Dual ARM Cortex-A9 + Artix-7 FPGA fabric. CK running at hardware speed -- CL composition
in 5ns, D2 pipeline in fabric, heartbeat at 200 MHz clock. No OS. No Python. Pure math on silicon.

## Hardware

- **Board**: Zynq-7020 (XC7Z020-CLG400)
- **PS (Processing System)**: Dual Cortex-A9 @ 667 MHz, 512 MB DDR3
- **PL (Programmable Logic)**: 85K logic cells, 4.9 Mb BRAM, 220 DSP slices
- **I/O**: GPIO, I2S (mic/speaker), UART, SPI, I2C, PWM
- **Power**: External battery (7.4V 2S LiPo via regulator)

## Architecture

```
+-------------------------------------------------------+
|                    ZYNQ-7020                           |
|  +------------------+    +------------------+         |
|  |   PS Core 0      |    |   PS Core 1      |        |
|  |  Brain + B + Q   |    |  Body + Execute  |        |
|  +--------+---------+    +--------+---------+        |
|           |     Shared BRAM        |                  |
|  +--------+------------------------+---------+        |
|  |              PL (FPGA Fabric)              |       |
|  |  Heartbeat + D2 + IMU Fusion + PWM         |      |
|  +--------------------------------------------+      |
+-------------------------------------------------------+
```

### Core 0 (Brain)
- BTQ decision kernel (B-block constraints, T-block candidates, Q-block resolution)
- Sovereignty pipeline (mode transitions)
- Energy management (battery monitoring, dock-seek behavior)

### Core 1 (Body)
- Breath cycle execution
- Audio synthesis (DAC output)
- Gait execution (servo commands via UART)
- Sensor polling (IMU, proximity, battery)

### PL (FPGA Fabric)
- **ck_heartbeat.v**: CL table in BRAM, 32-entry coherence window, tick @ 200 MHz
- **d2_pipeline.v**: Q1.14 fixed-point D2 curvature, 3-stage pipeline
- **ck_top.v**: Wires heartbeat + D2 + GPIO + clock
- **ck_i2s_mic.v**: I2S microphone interface (48 kHz)
- **ck_dac_speaker.v**: DAC speaker output

## Raw State

This deployment starts CK UNTRAINED. The transition lattice is empty.
CK must be educated from scratch through the experience curriculum:

1. Nursery (basic operator sequences)
2. Elementary (virtues)
3. Middle School (trauma, identity)
4. High School (domains)
5. University (cultures)
6. Graduation (collapse to single TL)

Or load a pre-trained TL from the master experience file.

## Robot Dog Integration

The Zynq board sits on top of the XiaoR Geek robot dog:
- 4 legs x 2 joints = 8 bus servos (UART @ 115200 baud)
- IMU (MPU6050 via I2C): 3-axis accel + 3-axis gyro
- Ultrasonic sensor (GPIO trigger/echo)
- Camera (future: via PS USB or SPI)
- Battery monitoring (ADC via SPI)

UART packet protocol (from ck_sim_uart.py):
- Header: 0xCK (2 bytes)
- Type: 1 byte (0x20=MOTOR, 0x22=SERVO, 0x23=GAIT, 0xA1=SERVO_POS, 0xA2=PROXIMITY)
- Length: 1 byte
- Payload: variable
- CRC-8: 1 byte

## Building

### Verilog Synthesis (Vivado)
Source files in CKIS/ck7/zynq/hdl/:
- ck_heartbeat.v
- d2_pipeline.v
- ck_top.v
- ck_i2s_mic.v
- ck_dac_speaker.v

Target: XC7Z020-CLG400-1, 200 MHz clock

### ARM Bare Metal (gcc-arm-none-eabi)
Source files in CKIS/ck7/zynq/arm/:
- ck_brain.c (Core 0)
- ck_body.c (Core 1)
- ck_ears.c (audio input processing)
- ck_audio.c (audio output synthesis)
- ck_led.c (LED control)
- ck_uart.c (UART communication)
- ck_sd.c (SD card TL save/load)

### Flash
Program via JTAG to QSPI flash. Board boots CK automatically on power-up.

## Troubleshooting

- No heartbeat LED: Check FPGA bitstream is loaded (DONE pin high)
- No audio: Verify I2S codec connections (MCLK, BCLK, LRCLK, DIN)
- No servo movement: Check UART TX pin connection, baud rate 115200
- IMU not responding: Verify I2C address (0x68 default for MPU6050)

---

## Future: One Fractal Kernel Architecture (Kernel Spec)

When porting to Zynq, CK should be restructured as a single `kernel_tick()` per heartbeat.
This spec defines how the Python simulation maps to silicon.

### Core State (what lives on FPGA)

Everything that goes on the PL or in BRAM. Portable, small, C-ready:

1. **CL table** (10x10): `CL[10][10] -> op`. 100 bytes. Immutable at runtime.
2. **Entangled field** (3 shells per CL cell):
   - `Field_mm[a][b][3][3]` — micro-micro neighbors (curvature, energy_bias, trust_weight)
   - `Field_mM[a][b][3][3]` — micro-macro coupling
   - `Field_MM[a][b][3][3]` — macro-macro tilt
3. **Operator dictionary skeleton** (hot cache):
   - `struct DictEntry { uint32_t id; uint8_t ops[MAX_OPS]; uint8_t len; }`
   - 1-2K entries in BRAM, cold storage on SD/disk
4. **Rolling buffers**:
   - `recent_in[32]`, `recent_out[32]`
   - Scalars: power_budget, risk_level, entropy, curvature

### The One Step: kernel_tick

```c
void kernel_tick(op_stream, body_state, mode_hint) {
    // 1. SENSE -> OPS (overlay encodes world -> operators)
    // 2. CHOOSE RADIUS (R0/R1/R2 from body_state)
    // 3. BTQ CORE (one pass, three phases)
    //    B-phase: filter by CL + body limits + trust bands
    //    T-phase: CL composition + field walks (R1) + sequences (R2)
    //    Q-phase: score E_out + E_in, select least-action, update field
    // 4. UPDATE BEING & BECOMING (tick heartbeat, nudge field)
    // 5. OPS -> ACT (overlay decodes operators -> world)
}
```

### Three Radii (3-6-9)

```
R0 (snap/3-mode):  B-phase only, 0-1 CL steps, no field walk, no GPU
                   Used when: risk high, power low, explicit "fast"

R1 (local/6-mode): B+T phases, field walk mm/mM/MM for 1-3 hops,
                   small dictionary cache
                   Used for: normal conversation, normal gait

R2 (deep/9-mode):  Full B+T+Q, sequence walks over recent_in/out,
                   full dictionary, optional GPU-accelerated pattern ops
                   Used for: long answers, self-rewrites, strategy, offline learning
```

### BTQ Phases

- **B-phase (Being / Einstein)**: "What cannot be violated this heartbeat."
  Reads CL table, field tiles, body_state, pinned invariants.
  Filters candidates: impossible, unsafe, out-of-budget moves cut.

- **T-phase (Doing / Tesla)**: "All possible efficient ways to move."
  CL fusion (always). Field walks (R1+). Sequence hops + dictionary + GPU helpers (R2).
  Generates candidates, never decides.

- **Q-phase (Becoming / Quadratic)**: "Snap to least-action, update slow state."
  `E_total = w_out * E_out + w_in * E_in`. Select minimum.
  Nudge field weights toward successful paths.
  Adjust dictionary trust. Update buffers.

### Overlays (not engines)

Every current "engine" becomes a thin adapter:
```
Text overlay:   tokenize -> D2 -> operators | operators -> words -> sentences
Audio overlay:  mic -> MFCC -> operators    | operators -> tone synthesis
Vision overlay: frames -> labels -> operators
Robot overlay:  IMU/sensors -> operators    | operators -> gait -> servo commands
```

Overlays do only 2 things: encode world -> operators, decode operators -> world.
None of them decide anything. They ask the kernel.

### Zynq Mapping

```
PS Core 0: Brain + B-phase + Q-phase (reasoning at 50Hz)
PS Core 1: Body + overlay execution (breath, gait, audio)
PL (FPGA): T-phase hot path + D2 pipeline + heartbeat + IMU fusion @ 500Hz
Shared BRAM: CKCoreState (CL, field, buffers, telemetry)
```

The entangled field fits in BRAM: 10x10x3x3x3x3 = 8,100 entries x 3 bytes = ~24 KB.
CL table: 100 bytes. Rolling buffers: ~256 bytes. Total core state: < 32 KB BRAM.

### Key Constraint

The kernel must compile to pure C, then Verilog/RTL:
- No Python objects, no dynamic allocation, no heap
- Fixed-size structs only
- All math is integer or Q1.14 fixed-point
- The same `btq_core()` runs on ARM (PS) and in fabric (PL)

---

## Credits

CK Coherence Machine
Built by Brayden Sanders / 7Site LLC
Mathematics: TIG Unified Field Theory (Papers 1-8)
One Kernel Architecture: (2026)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
