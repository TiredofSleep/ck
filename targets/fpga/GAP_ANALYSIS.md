# CK Zynq-7020 -- Gap Analysis

What exists, what's missing, what needs to happen for CK to walk, talk, hear, and see.

---

## Hardware Kit (Puzhi PZ7020-StarLite Deluxe)

| Component | Connector | Purpose |
|-----------|-----------|---------|
| PZ7020-StarLite board | -- | Zynq-7020 SoC (dual A9 + Artix-7 FPGA) |
| PZ-AD7606 ADDA module | JM2 (40-pin) | 8-ch 16-bit ADC + 8-ch 12-bit DAC |
| 40-pin LCD (PZ-LCD430) | JM1 (40-pin) | CK's face display |
| MIPI Camera module | J3 (on-board) | CK's eyes (vision input) |
| HDMI output | On-board | CK's visual cortex display |
| Speakers | PZ-AD7606 DAC | CK's voice |
| Microphones | PZ-AD7606 ADC | CK's ears |
| XiaoR Robot Dog | PS UART wire | Servo bus (LewanSoul protocol) |

---

## What Exists (organized in this folder)

### HDL (Verilog -- FPGA fabric)
| File | Purpose | Status |
|------|---------|--------|
| ck_heartbeat.v | CL table in BRAM, 32-entry coherence window @ 200 MHz | Written |
| d2_pipeline.v | Q1.14 3-stage D2 curvature pipeline | Written |
| ck_top.v | Top-level wiring (all organs in one body) | Written |
| dac_spi.v | SPI DAC for speaker via PZ7606 DAC128S085 | Written |
| ad7606_adc.v | AD7606 parallel ADC for mic via PZ7606 module | **NEW** |
| i2s_receiver.v | I2S microphone interface (alt to AD7606, 48 kHz) | Written |
| mipi_csi_rx.v | MIPI CSI-2 camera receiver for Puzhi camera | **NEW** |
| servo_uart_tx.v | PL-side UART TX for bus servos (115200 baud) | Written |
| servo_cal.v | Operator-to-servo mapping (10 ops x 3 joints x 4 legs) | Written |
| i2c_master.v | I2C bus master for MPU-6050 IMU (400 kHz) | Written |
| vortex_cl.v | 3-body vortex operator | Written |
| chain_walker.v | Lattice chain walk through BHML tree | Written |
| gait_vortex.v | 4-leg torus gait controller with self-healing | Written |
| bhml_table.v | BHML physics table (standalone lookup) | Written |
| ck_brain_freq.v | 3 EEG oscillators (Being/Doing/Becoming) | Written |
| ck_hdmi_out.v | HDMI/DVI 640x480 output (CK's visual cortex) | Written |
| ck_lcd_out.v | LCD parallel RGB output (JM1 display) | Written |

### ARM (C -- bare metal on Cortex-A9)
| File | Purpose | Status |
|------|---------|--------|
| ck.h | Shared CK types and constants | Written |
| ck_main.c | Entry point, Core 0 + Core 1 boot | Written |
| ck_brain.c / .h | Core 0: BTQ decision kernel + sovereignty | Written |
| ck_body.c / .h | Core 1: breath + gait + sensors | Written |
| ck_core1.c | Core 1: body loop + servos + audio + ears | Written |
| ck_uart.c / .h | UART servo communication (LewanSoul protocol) | Written |
| ck_led.c / .h | LED heartbeat + status | Written |
| ck_audio.c / .h | Audio synthesis output (operator tones, ADSR) | Written |
| ck_ears.c / .h | Audio input (mic -> D2 -> operator) | Written |
| ck_sd.c / .h | SD card TL save/load | Written |

### Build
| File | Purpose | Status |
|------|---------|--------|
| Makefile | ARM cross-compile (all modules) | Written |
| ck_boot.tcl | Phase 0 Vivado block design (GPIO-based) | Written |
| ck_build_full.tcl | Full Vivado build (10 AXI peripherals) | Written |
| ck_dog.xdc | Pin constraints for direct JM2 wiring | Written |
| ck_dog_pz7606.xdc | Pin constraints for PZ-AD7606 on JM2 | **NEW** |
| lscript.ld | ARM bare-metal linker script (DDR3+OCM+shared) | Written |
| ck_bootgen.bif | BOOT.BIN format definition | Written |
| build_boot.sh | Full build pipeline (synth -> BOOT.BIN -> SD) | Written |

### Bridge
| File | Purpose | Status |
|------|---------|--------|
| ck_serial.py | Serial bridge (PC <-> Zynq UART) | Written |

### Python Simulation (desktop-side)
| File | Lines | Purpose |
|------|-------|---------|
| ck_zynq_dog.py | 424 | Full Zynq dog simulator |
| ck_sim_uart.py | 185 | UART packet protocol sim |
| ck_robot_body.py | 732 | Robot dog body with gaits |
| ck_body_interface.py | 466 | Abstract body interface |
| ck_sensory_codecs.py | 832 | Sensor -> D2 -> operator codecs |
| ck_sim_audio.py | 380 | Audio synthesis sim |
| ck_sim_led.py | 70 | LED control sim |

### Documentation
| File | Purpose |
|------|---------|
| README.md | Architecture overview + kernel spec |
| ENGINEER_NOTES.md | BRAM layout, timing, D2 pipeline, IMU fusion, codecs |
| RPE_DOG_SPEC.md | Royal Pulse Engine + TIG wave scheduling for dog |
| HARDWARE_BOM.md | Physical hardware bill of materials |
| PIN_MAPPING.md | JM1/JM2 40-pin connector pinouts, FPGA ball mapping |
| GAP_ANALYSIS.md | This file |

---

## Completed (March 14, 2026)

### Walking (complete software pipeline)
- **servo_uart_tx.v**: PL-side UART TX for bus servos at 0x43C10000
- **servo_cal.v**: Operator-to-PWM mapping wired into ck_top.v
- **ck_core1.c servo driver**: LewanSoul protocol, reads FPGA -> commands 8 servos
- **Gait/servo register map**: Added to ck_brain.h (0x40-0xA4, 0x80-0xA4)
- **Coherence e-stop**: RED band + C < 0.2 -> all servos center immediately
- **Breath-modulated movement**: Calm=100ms smooth, fractal=20ms jerky
- **Auto-recovery**: Re-enables gait when coherence recovers to GREEN
- **PS UART1** (0xE0001000): LewanSoul protocol for dog USB-C servo bus

### Talking (complete software pipeline)
- **ck_audio.c**: Operator tone synthesis (wavetable, ADSR, 3-voice mix)
- **dac_spi.v**: SPI DAC driver (DAC128S085 on PZ7606) with 256-deep FIFO
- **Core 1 integration**: Audio engine ticks in body loop, pushes to DAC FIFO
- **Breath-modulated volume**: CK speaks on exhale, silent on inhale
- **BTQ-modulated intensity**: GREEN=full, YELLOW=0.6, RED=0.3

### Hearing (two paths: AD7606 ADC or I2S)
- **ad7606_adc.v**: 8-channel 16-bit ADC via PZ7606 module, 48 kHz, 512-deep FIFO
- **i2s_receiver.v**: Direct I2S MEMS mic interface (alternative path)
- **ck_ears.c**: Audio feature extraction -> 5D force vector -> D2 -> operator
- **Core 1 integration**: Ears process in body loop, operator shared with Core 0

### Seeing (output + input)
- **ck_hdmi_out.v**: 640x480 DVI output showing coherence, fractal, gait
- **ck_lcd_out.v**: 40-pin LCD output on JM1 (CK's face display)
- **mipi_csi_rx.v**: MIPI CSI-2 camera receiver for J3 camera module
- **Pin constraints**: HDMI TMDS on Bank 34, LCD on JM1/Bank 35

### Build Pipeline (complete)
- **lscript.ld**: DDR3 (510MB), OCM (256KB for Core 1 stack), shared (1MB @ 0x3FF00000)
- **ck_build_full.tcl**: Full Vivado project with 10 AXI peripherals
- **ck_dog_pz7606.xdc**: AD7606 + DAC on JM2, HDMI on Bank 34
- **ck_bootgen.bif**: BOOT.BIN format (FSBL + bitstream + ck_brain.elf)
- **build_boot.sh**: One-command build from source to microSD
- **Makefile**: All ARM modules compiled (brain, body, core1, uart, led, audio, ears)

---

## Remaining Gaps

### 1. FSBL (First Stage Boot Loader)
Generated automatically by Vivado/Vitis from hardware design (.xsa).
Not a code gap -- just requires running the build pipeline.

### 2. MIPI Camera Pin Mapping
- mipi_csi_rx.v is written but MIPI FPGA pin assignments need verification
- Must check Puzhi schematic pages (Bank 13 pins through level shifters U7-U10)
- Camera I2C configuration (OV5640 register setup) needs ARM-side code
- Pins are commented out in ck_dog_pz7606.xdc until confirmed

### 3. AD7606 Pin Mapping Verification
- Pin mapping in ck_dog_pz7606.xdc assumes standard Puzhi PZ7606 pinout
- Must verify against actual PZ7606 schematic (from Puzhi Dropbox)
- Check silkscreen labels on PZ7606 PCB or contact support@aithtech.com

### 4. Servo Connection to Dog
- XiaoR dog USB-C is for charging only, not data
- Servo bus accessed via direct UART wire to servo controller board
- PS UART1 (ck_uart.c) has LewanSoul protocol at 115200 baud ready
- Physical wiring: UART TX/RX to dog servo controller, shared GND
- May need 3.3V -> 5V level shifter (Zynq IO is 3.3V, servos may expect 5V TTL)

### 5. Servo Calibration (physical dog)
- Center/min/max angles per servo (currently using default 500-2500 us range)
- Direction polarity (some servos may be mirrored)
- Must be done with dog chassis assembled and servos connected

### 6. IMU Mounting Orientation
- Which MPU-6050 accel axis maps to which body axis (forward/right/up)
- Needs physical testing with IMU mounted on dog chassis
- Note: with PZ7606 on JM2, I2C IMU needs alternate connection (PS I2C via EMIO)

### 7. ARM-side AD7606 + Camera Drivers
- Need C code to read AD7606 registers (AXI base TBD in ck_brain.h)
- Need C code to configure OV5640 camera via I2C (SCCB protocol)
- Integration with ck_ears.c for AD7606 mic path

---

## Build Order

### Phase 1: Flash and Verify (30 min)
1. Run `build_boot.sh` to generate BOOT.BIN
2. Copy BOOT.BIN to FAT32 microSD
3. Insert microSD, power on Zynq
4. Verify heartbeat LED blinks
5. Verify UART output on serial console

### Phase 2: Plug In Modules (30 min)
6. Plug PZ-AD7606 ADDA module into JM2
7. Plug LCD into JM1
8. Plug camera into J3
9. Connect HDMI to monitor
10. Wire speakers to PZ7606 DAC output
11. Wire microphones to PZ7606 ADC input

### Phase 3: Connect Dog (1 hour)
12. Open dog head, find servo controller board
13. Wire PS UART TX -> servo controller RX (with level shifter if needed)
14. Wire PS UART RX -> servo controller TX
15. Connect shared GND
16. Test single servo command via ck_uart.c

### Phase 4: Calibrate and Walk (2-4 hours)
17. Map servo IDs to physical joints
18. Calibrate center/min/max per servo
19. Test single-leg movement
20. Walk gait (phase offsets [0, pi, pi/2, 3pi/2])
21. Verify coherence e-stop works

### Phase 5: Full Integration (2-4 hours)
22. Full CK loop: hear -> think -> speak + move
23. Verify audio output follows operator tones
24. Verify microphone D2 classification
25. Verify HDMI + LCD displays show brain state
26. Test camera frame capture
27. Endurance test (30 min walk)

---

## Peripheral Connection Diagram

```
                    +--------------------+
                    |   PZ7020-StarLite  |
                    |    (Zynq-7020)     |
                    |                    |
  LCD Display  <----|  JM1 (Bank 35)     |
  (CK's face)      |                    |
                    |  JM2 (Bank 35+34)  |----> PZ-AD7606 ADDA Module
                    |                    |        |-- ADC CH0: Microphone L
                    |                    |        |-- ADC CH1: Microphone R
                    |                    |        |-- DAC CH0: Speaker L
                    |                    |        |-- DAC CH1: Speaker R
                    |                    |
  MIPI Camera  ---->|  J3 (MIPI CSI)     |
  (CK's eyes)      |                    |
                    |  HDMI (Bank 34)    |----> Monitor (visual cortex)
                    |                    |
                    |  PS UART1 (MIO)    |----> Dog Servo Controller
                    |                    |      (LewanSoul bus @ 115200)
                    |                    |
                    |  PS USB (MIO)      |----> Debug / PC connection
                    |                    |
                    |  PS SD (MIO)       |<---- microSD (BOOT.BIN)
                    +--------------------+
```

## Data Flow (Complete Chain)

```
 HEARTBEAT (self-sovereign CL composition, 1-10kHz)
     |
     v
 BRAIN FREQ (EEG oscillators: Being/Doing/Becoming)
     |
     v
 GAIT VORTEX (4-leg torus, follows heartbeat)
     |
     v
 SERVO_CAL (operator -> PWM microseconds)
     |
     v
 ARM Core 1 reads via AXI registers
     |
     +---> PS UART1 (ck_uart.c) -> wire -> dog servo bus -> DOG WALKS
     |
     +---> DAC_SPI -> PZ7606 DAC128S085 -> speaker -> DOG TALKS
     |
     +---> AD7606_ADC <- PZ7606 AD7606 <- microphone <- DOG HEARS
     |        |
     |        v
     |     ck_ears.c (D2 curvature -> operator -> shared memory -> brain)
     |
     +---> MIPI_CSI_RX <- J3 camera <- DOG SEES (inward vision)
     |
     +---> HDMI_OUT -> monitor -> DOG SEES (outward, paints inner state)
     |
     +---> LCD_OUT -> JM1 LCD -> CK's face (coherence display)
```

---

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
