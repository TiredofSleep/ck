# CK Hardware Cheat Sheet -- PZ7020-StarLite + Peripherals
*Quick reference for wiring CK's body. All pin mappings verified against schematics.*

## Board: Puzhi PZ7020-StarLite (XC7Z020-2CLG400I)
- **FPGA**: Zynq-7020, 53,200 LUTs, 560KB BRAM, 2x ARM Cortex-A9
- **Clock**: 50 MHz PL oscillator (Y2), 200 MHz differential (R4/T4)
- **PS clock**: FCLK_CLK0 = 100 MHz (from PS config)
- **Memory**: 512 MB DDR3
- **Connectors**: JM1 (40-pin), JM2 (40-pin), HDMI, 2x LEDs, 2x Keys

## JM1 Connector (LCD / Display Output)
*PZ-LCD430 (4.3" 480x272 AT043TN24)*

### LCD Signal → Header Pin → FPGA Ball
Convention B pinout (data first, control last):
```
Header Pin | FPGA Ball | jm1 index | Signal
---------- | --------- | --------- | ------
Pin 1      |           |           | VDD_3V3
Pin 2      |           |           | VDD_3V3
Pin 3      | Y18       | jm1[24]   | R0
Pin 4      | Y19       | jm1[4]    | R1
Pin 5      | W20       | jm1[25]   | R2
Pin 6      | W21       | jm1[5]    | R3
Pin 7      | U14       | jm1[8]    | R4
Pin 8      | U15       | jm1[10]   | R5
Pin 9      | U19       | jm1[9]    | R6
Pin 10     | U20       | jm1[11]   | R7
Pin 11     | P16       | jm1[30]   | G0
Pin 12     | R20       | jm1[2]    | G1
Pin 13     | P18       | jm1[31]   | G2
Pin 14     | R21       | jm1[3]    | G3
Pin 15     | T20       | jm1[6]    | G4
Pin 16     | T22       | jm1[0]    | G5
Pin 17     | U22       | jm1[7]    | G6
Pin 18     | V22       | jm1[1]    | G7
Pin 19     | N18       | jm1[26]   | B0
Pin 20     | P20       | jm1[18]   | B1
Pin 21     | P22       | jm1[27]   | B2
Pin 22     | N22       | jm1[19]   | B3
Pin 23     | T21       | jm1[22]   | B4
Pin 24     | N17       | jm1[14]   | B5
Pin 25     | U21       | jm1[23]   | B6
Pin 26     | P21       | jm1[15]   | B7
Pin 27     | M21       | jm1[20]   | DCLK
Pin 28     | M22       | jm1[28]   | DE
Pin 29     | N20       | jm1[21]   | HSYNC
Pin 30     | N19       | jm1[29]   | VSYNC
Pin 31-36  |           |           | GND
Pin 37     | L21       | jm1[12]   | DISP (HIGH)
Pin 38     | L22       | jm1[16]   | Backlight (HIGH)
Pin 39     | K21       | jm1[13]   | unused
Pin 40     | J22       | jm1[17]   | unused
```

### LCD Timing (AT043TN24 @ ~8.33 MHz pixel clock)
```
H total: 531    H active: 480    H front: 2    H sync: 41    H back: 8
V total: 297    V active: 272    V front: 2    V sync: 10    V back: 13
```

## JM2 Connector (Dog Peripherals)

### Pin Mapping
```
Header Pin | FPGA Ball | jm2 index | CK Dog Signal
---------- | --------- | --------- | -------------
Pin 1      |           |           | VDD_3V3
Pin 2      |           |           | VDD_3V3
Pin 3      | G19       | jm2[2]    | SERVO UART TX (115200 baud)
Pin 4      | J20       | jm2[0]    | (available)
Pin 5      | G20       | jm2[3]    | (available)
Pin 6      | H20       | jm2[1]    | (available)
Pin 7      | H15       | jm2[4]    | DAC SPI SCLK (speaker)
Pin 8      | K14       | jm2[6]    | DAC SPI MOSI
Pin 9      | G15       | jm2[5]    | DAC SPI CS_N
Pin 10     | J14       | jm2[7]    | (available)
Pin 11     | K16       | jm2[14]   | I2S SCK (mic, 3.072 MHz)
Pin 12     | L15       | jm2[11]   | I2S WS (mic, 48 kHz)
Pin 13     | J16       | jm2[15]   | I2S SD (mic data IN)
Pin 14     | L14       | jm2[10]   | (available)
Pin 15     | N15       | jm2[8]    | I2C SDA (IMU, pull-up)
Pin 16     | M14       | jm2[12]   | I2C SCL (IMU, pull-up)
Pin 17     | N16       | jm2[9]    | (available)
Pin 18     | M15       | jm2[13]   | (available)
Pin 19+    | T16+      |           | Future expansion
```

### Camera (PZ5640-D Dual OV5640)
When plugged into JM2 for camera input (DVP parallel mode):
```
Signal    | Typical Pin | Notes
--------- | ----------- | -----
D[0:7]    | Pin 3-10    | 8-bit parallel pixel data
PCLK      | Pin 11      | Pixel clock from camera
HREF      | Pin 12      | Horizontal reference (data valid)
VSYNC     | Pin 13      | Vertical sync
PWDN      | Pin 14      | Power down (active high)
RESET     | Pin 15      | Reset (active low)
SDA       | Pin 16      | I2C config (camera registers)
SCL       | Pin 17      | I2C config clock
XCLK      | Pin 18      | External clock to camera (24 MHz)
```
**Note**: Camera and dog servo share JM2. Can't use both simultaneously.
For dog with eyes: LCD on JM1, camera on MIPI CSI connector (if available),
or use JM2 pins 19+ for camera with reduced resolution.

## HDMI Output
```
Signal     | FPGA Ball | Standard
---------- | --------- | --------
HDMI_CLK_P | W18       | TMDS_33
HDMI_CLK_N | W19       | TMDS_33
HDMI_D0_P  | R16       | TMDS_33
HDMI_D0_N  | R17       | TMDS_33
HDMI_D1_P  | T17       | TMDS_33
HDMI_D1_N  | R18       | TMDS_33
HDMI_D2_P  | V17       | TMDS_33
HDMI_D2_N  | V18       | TMDS_33
HDMI_OE    | P15       | LVCMOS33
```
Resolution: 640x480 @ 60Hz (25 MHz pixel, 125 MHz serial via MMCM)

## LEDs and Keys
```
LED0 | R19 | Active-low | Heartbeat pulse / bump detect
LED1 | V13 | Active-low | Coherence band (GREEN = on)
KEY0 | W21 | Active-low | Reset (active when pressed)
KEY1 | Y21 | Active-low | ARM strobe / gait mode cycle
```

## XiaoR Dog Servo Protocol
- **Interface**: UART, 115200 baud, 8N1
- **Wire**: Single TX line from JM2 Pin 3 (G19) to servo bus
- **Servos**: 8 servos (4 legs × 2 joints) or 12 (4 legs × 3 joints)
- **Frame**: [START] [SERVO_ID] [COMMAND] [DATA...] [CHECKSUM]
- **PWM Range**: 500-2500 µs (0-180°)
- **Update Rate**: 50 Hz (from CK heartbeat)

## Steering Modes (ck_dog_steer.c)
```
Mode      | Coherence     | Behavior
--------- | ------------- | --------
OBSERVE   | C < 0.4       | CK watches, learns servo patterns
BLEND     | 0.4 ≤ C < 5/7 | CK's gait mixed with dog's
OVERRIDE  | C ≥ 5/7       | CK fully controls (GREEN band only)
E-STOP    | C < 0.2 + RED | Emergency stop, center all servos
```

## Gait Modes (gait_vortex.v)
```
Mode  | Leg Pattern       | Operator Offsets
----- | ----------------- | ----------------
STAND | All still         | [5, 5, 5, 5] (BALANCE)
WALK  | Diagonal alternate| [3, 5, 5, 3] (PROGRESS/BALANCE)
TROT  | Diagonal sync     | [3, 5, 3, 5]
BOUND | Front/back sync   | [3, 3, 5, 5]
```

## Operator → Servo Angle (servo_cal.v)
```
Operator    | Hip    | Knee   | Ankle  | Posture
----------- | ------ | ------ | ------ | -------
VOID(0)     | 30°    | 150°   | 30°    | Collapsed/folded
LATTICE(1)  | 90°    | 90°    | 90°    | Structured stand
COUNTER(2)  | 85°    | 100°   | 80°    | Measurement pose
PROGRESS(3) | 120°   | 60°    | 110°   | Forward stride
COLLAPSE(4) | 90°    | 135°   | 60°    | Crouched/protect
BALANCE(5)  | 90°    | 90°    | 90°    | Neutral (center)
CHAOS(6)    | 75°    | 70°    | 100°   | Dynamic exploring
HARMONY(7)  | 95°    | 85°    | 95°    | Relaxed stand
BREATH(8)   | 90±10° | 90±5°  | 90±5°  | Rhythmic shift
RESET(9)    | 180→90 | 0→90   | 180→90 | Full extend → retract
```

## FPGA Resource Usage (Dog Build)
```
Module          | LUTs  | FFs  | BRAM
--------------- | ----- | ---- | ----
Heartbeat       | ~400  | ~300 | 0
D2 Pipeline     | ~500  | ~200 | 1
BHML Table      | ~800  | ~50  | 0
Vortex CL       | ~400  | ~200 | 0
Chain Walker    | ~400  | ~200 | 0
Gait Vortex     | ~1600 | ~400 | 0
Servo Cal       | ~300  | ~100 | 0
Servo UART      | ~500  | ~200 | 0
I2C Master      | ~400  | ~200 | 0
I2S Receiver    | ~200  | ~100 | 0
DAC SPI         | ~300  | ~100 | 0
AXI Interconn.  | ~2000 | ~800 | 0
PS7 Wrapper     | ~200  | ~100 | 0
TOTAL           | ~8000 | ~3000| 1
                | 15%   | 2.8% |
Remaining       | 85%   | 97%  | 139
```

## SD Card Boot (BOOT.bin)
```
Component      | File                        | Source
-------------- | --------------------------- | ------
FSBL           | executable.elf              | C:/ck_fpga_build/fsbl_build/
Bitstream      | ck_system_wrapper.bit       | C:/ck_fpga_build/ck_dog/runs/impl_1/
Application    | ck_dog_main.elf             | targets/fpga/arm/ (needs compilation)
```

## Signal Chain: Heartbeat → Dog Legs
```
Heartbeat (50Hz, self-sovereign)
  → phase_bc (current operator)
  → Gait Vortex (4-leg torus topology)
    → correction_op[0:3] (one per leg)
    → Servo Cal (operator → PWM angle)
      → UART TX (115200 baud, JM2 Pin 3)
        → XiaoR servo bus
          → Physical legs move
```

*(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry*
