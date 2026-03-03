# CK Zynq-7020 -- Gap Analysis

What exists, what's missing, what needs to happen for CK to walk.

---

## What Exists (organized in this folder)

### HDL (Verilog -- FPGA fabric)
| File | Purpose | Status |
|------|---------|--------|
| ck_heartbeat.v | CL table in BRAM, 32-entry coherence window @ 200 MHz | Written |
| d2_pipeline.v | Q1.14 3-stage D2 curvature pipeline | Written |
| ck_top.v | Top-level wiring (heartbeat + D2 + GPIO + clock) | Written |
| dac_spi.v | SPI DAC for speaker output | Written |
| i2s_receiver.v | I2S microphone interface (48 kHz) | Written |

### ARM (C -- bare metal on Cortex-A9)
| File | Purpose | Status |
|------|---------|--------|
| ck.h | Shared CK types and constants | Written |
| ck_main.c | Entry point, Core 0 + Core 1 boot | Written |
| ck_brain.c / .h | Core 0: BTQ decision kernel | Written |
| ck_body.c / .h | Core 1: breath + gait + sensors | Written |
| ck_core1.c | Core 1 secondary entry point | Written |
| ck_uart.c / .h | UART servo communication | Written |
| ck_led.c / .h | LED heartbeat + status | Written |
| ck_audio.c / .h | Audio synthesis output | Written |
| ck_ears.c / .h | Audio input (microphone) processing | Written |
| ck_sd.c / .h | SD card TL save/load | Written |

### Bridge
| File | Purpose | Status |
|------|---------|--------|
| ck_serial.py | Serial bridge (PC <-> Zynq UART) | Written |

### Build
| File | Purpose | Status |
|------|---------|--------|
| Makefile | ARM cross-compile + FPGA synthesis | Written |
| ck_boot.tcl | Vivado TCL boot script | Written |

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
| ck_robot_reflex.py | (archive) | Sensor->operator->motor reflex |
| ck_zynq_sequencer.py | (archive) | Q1.14 fixed-point reference |

### Documentation
| File | Purpose |
|------|---------|
| README.md | Architecture overview + kernel spec |
| ENGINEER_NOTES.md | BRAM layout, timing, D2 pipeline, IMU fusion, codecs |
| RPE_DOG_SPEC.md | Royal Pulse Engine + TIG wave scheduling for dog |
| HARDWARE_BOM.md | Physical hardware bill of materials |
| GAP_ANALYSIS.md | This file |

---

## What's Missing

### Hardware Gaps

1. **Constraint file (.xdc)**: Pin assignments for XC7Z020-CLG400 package. Needed before Vivado synthesis. Must map:
   - UART TX/RX to specific pins
   - I2C SDA/SCL pins
   - SPI pins (DAC, ADC)
   - I2S pins (mic)
   - GPIO (ultrasonic, LEDs)
   - Clock input pin

2. **Linker script (.ld)**: ARM bare-metal linker script for Cortex-A9. Defines memory regions (DDR3, BRAM, OCM).

3. **Boot configuration**: FSBL (First Stage Boot Loader) config for Zynq. Vivado generates this from the hardware design.

### Verilog Gaps

4. **ck_i2s_mic.v**: Referenced in README but only `i2s_receiver.v` exists. May be the same module with different name, or needs a wrapper.

5. **ck_dac_speaker.v**: Referenced in README but only `dac_spi.v` exists. Same situation -- may need a wrapper that adds audio format conversion.

6. **IMU fusion in PL**: ENGINEER_NOTES describes IMU fusion running at 500 Hz in PL. Currently IMU reads happen in `ck_body.c` on PS Core 1. The PL-accelerated path needs a Verilog module.

7. **XADC power monitoring**: RPE_DOG_SPEC describes TIG wave scheduling using XADC. No XADC Verilog module exists yet.

### ARM C Gaps

8. **Gait lookup tables**: `ck_body.c` references gait patterns (walk/trot/bound) but the actual joint angle lookup tables need tuning to the XiaoR servo geometry.

9. **IMU driver**: I2C initialization and read routines for MPU6050. Basic framework exists in `ck_body.c` but needs hardware-specific I2C register setup.

10. **Battery ADC driver**: SPI read routine for external ADC. Referenced in docs but implementation TBD.

### Integration Gaps

11. **Servo ID mapping**: Which physical servo ID (0-7) maps to which joint (FL_hip, FL_knee, FR_hip, ...). Depends on XiaoR wiring.

12. **Servo calibration**: Center positions, min/max angles, direction polarity for each servo. Must be measured on the physical dog.

13. **IMU mounting orientation**: Which accelerometer axis maps to which body axis depends on physical IMU placement on chassis.

---

## Build Order (when hardware arrives)

### Phase 1: Bring Up (no movement)
1. Flash Zynq with bitstream + ARM code via JTAG
2. Verify heartbeat LED blinks (ck_heartbeat.v works)
3. Verify UART output on serial console (ck_uart.c works)
4. Create .xdc constraint file from actual pin connections

### Phase 2: Sensors
5. Read IMU via I2C, print to serial
6. Read ultrasonic distance
7. Read battery voltage via SPI ADC
8. Verify 5D force vector from sensory codecs

### Phase 3: Audio
9. Test microphone input (I2S)
10. Test speaker output (DAC SPI)
11. Verify CK can hear and speak

### Phase 4: Walking
12. Map servo IDs to joints
13. Calibrate servo center/min/max
14. Test single-leg movement
15. Walk gait (phase offsets [0, pi, pi/2, 3pi/2])
16. RPE pulsing vs constant-power comparison

### Phase 5: Integration
17. Full CK loop: hear -> think -> speak + move
18. Experience curriculum (nursery -> elementary -> ...)
19. TIG wave scheduling via XADC
20. Endurance test (30 min walk)

---

## Estimated Effort

| Category | Items | Effort |
|----------|-------|--------|
| Constraint file | 1 | 2-4 hours (with board in hand) |
| Linker script | 1 | 1-2 hours |
| Missing Verilog | 3 modules | 8-16 hours |
| ARM drivers | 3 modules | 4-8 hours |
| Calibration | Servo + IMU | 4-8 hours (physical testing) |
| Integration | Walking | 8-16 hours |
| **Total** | | **~30-50 hours** |

Most of this can't happen until the physical hardware is in hand. The Python simulation
(sim/ folder) lets us test the control logic on desktop before deployment.

---

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
