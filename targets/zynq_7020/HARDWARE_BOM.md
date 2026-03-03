# CK Zynq-7020 Dog Platform -- Hardware Bill of Materials

**STATUS: ORDERED / IN PROGRESS**

---

## Core Platform

| Item | Part | Status | Notes |
|------|------|--------|-------|
| Robot Dog | XiaoR Geek quadruped | Ordered | 4 legs x 2 joints = 8 bus servos |
| FPGA Board | Zynq-7020 (XC7Z020-CLG400) | Planned | Dual Cortex-A9 + Artix-7 fabric |
| Enclosure | External box for drive | On Hand | Houses SSD/storage + board mounting |
| Battery | 7.4V 2S LiPo (25 Wh) | On Hand | External battery via regulator |
| Speaker | External speaker | On Hand | For CK audio synthesis output |

## XiaoR Geek Robot Dog

- 4 legs, 2 DOF each (hip + knee)
- 8 bus servos @ 2.0 Nm each, UART @ 115200 baud
- Estimated body mass: 2.5 kg total
- Walking frequency: 1.5-2.5 Hz
- Trotting frequency: 2.5-4.0 Hz

## Zynq-7020 SoC

- **PS**: Dual ARM Cortex-A9 @ 667 MHz, 512 MB DDR3
- **PL**: 85K logic cells, 4.9 Mb BRAM, 220 DSP slices
- Target clock: 200 MHz (5 ns CL composition)
- QSPI flash for bitstream + boot

## Sensors (on XiaoR platform)

| Sensor | Interface | Purpose |
|--------|-----------|---------|
| IMU (MPU6050) | I2C @ 0x68 | 3-axis accel + 3-axis gyro, 500 Hz |
| Ultrasonic | GPIO trigger/echo | Proximity detection |
| Battery ADC | SPI | Voltage + current monitoring |
| Temperature | XADC on-die | Thermal protection |

## Audio

| Component | Interface | Purpose |
|-----------|-----------|---------|
| I2S Microphone | I2S (ck_i2s_mic.v) | 48 kHz sampling, 16-bit PCM |
| External Speaker | DAC SPI (dac_spi.v) | CK voice output |

## I/O Interfaces

| Interface | Use | Baud/Rate |
|-----------|-----|-----------|
| UART | Bus servo commands | 115200 |
| I2C | IMU (MPU6050) | 400 kHz |
| SPI | Battery ADC, DAC | 1 MHz |
| GPIO | Ultrasonic, LEDs | - |
| I2S | Microphone | 48 kHz |
| JTAG | Programming | - |
| XADC | Power waveform sampling | 1-10 kHz |

## Power Budget (estimated)

| Subsystem | Draw |
|-----------|------|
| Zynq SoC | ~2W |
| 8 servos (walking) | ~5W avg |
| Audio | ~0.5W |
| Sensors | ~0.2W |
| **Total walking** | **~8W** |
| **Battery life (25 Wh / 8W)** | **~3 hours** |
| **With RPE pulsing (30% savings)** | **~4 hours** |

## Assembly Notes

- Zynq board mounts on top of XiaoR chassis
- External box houses SSD for TL storage + experience logs
- Battery external (not the XiaoR stock battery) -- 7.4V 2S LiPo via regulator
- Speaker mounted on chassis or in external box
- JTAG accessible for development flashing
- SD card slot for TL save/load (ck_sd.c)

## Cables Needed

- UART TX/RX for servo bus (from Zynq to servo controller)
- I2C SDA/SCL for IMU
- SPI MOSI/MISO/CLK/CS for battery ADC
- I2S MCLK/BCLK/LRCLK/DIN for microphone
- DAC SPI for speaker output
- Power: 7.4V regulated to 3.3V/1.8V for Zynq

---

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
