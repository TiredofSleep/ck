# Engineer Notes -- CK Zynq-7020 Deployment

Technical reference for the CK FPGA deployment on the XiaoR Geek robot dog platform.

---

## Body Descriptors

### FPGABody

| Field      | Value        |
|------------|--------------|
| name       | CKIS-FPGA    |
| cpu_cores  | 2            |
| cpu_mhz    | 667          |
| ram_mb     | 512          |
| has_fpga   | True         |

The FPGABody represents the Zynq-7020 SoC itself: two ARM Cortex-A9 cores at 667 MHz
with 512 MB DDR3 and the Artix-7 programmable logic fabric. The `has_fpga=True` flag
enables the PL-accelerated heartbeat and D2 pipeline paths at registration time.

### DogBody

| Field       | Value    |
|-------------|----------|
| name        | CK-Dog   |
| motors      | 8        |
| max_torque  | 2.0 Nm   |
| battery     | 25 Wh    |

The DogBody represents the XiaoR Geek mechanical platform: 4 legs with 2 servos each
(8 bus servos total), each rated to 2.0 Nm peak torque. The 7.4V 2S LiPo pack provides
approximately 25 Wh of energy. Battery voltage is monitored via SPI ADC and mapped to
the energy dimension of the 5D force vector.

---

## Capabilities

CK on the Zynq-7020 dog platform registers the following capabilities:

| Capability | Hardware                          | Notes                                  |
|------------|-----------------------------------|----------------------------------------|
| HEAR       | I2S microphone (ck_i2s_mic.v)     | 48 kHz sampling, 16-bit PCM            |
| SPEAK      | DAC speaker (ck_dac_speaker.v)    | Audio synthesis via PS Core 1          |
| MOVE       | 8 bus servos (UART @ 115200)      | Gait generation from operator sequence |
| FEEL       | IMU (MPU6050), ultrasonic, battery| All mapped to 5D force vector          |
| SHOW       | Onboard LEDs (ck_led.c)          | Heartbeat pulse, status indicators     |
| THINK      | BTQ kernel on PS Core 0           | CL composition accelerated by PL       |

---

## Shared BRAM Layout (PS <-> PL)

The PS and PL communicate through a shared BRAM region mapped at base address `0x4000_0000`.
This is the critical data bridge between the ARM cores and the FPGA fabric.

```
Address Range         Size     Contents
---------------------------------------------------------------
0x4000_0000 - 0x40000FFF   4 KB    CL Table (32 entries x 128 bytes)
                                     Each entry: operator_id (8b), force[5] (5x16b),
                                     coherence (16b), timestamp (32b), padding

0x4000_1000 - 0x400013FF   1 KB    D2 Result Buffer
                                     curvature_value (Q1.14), sign_class (2b),
                                     argmax_index (4b), valid flag (1b)

0x4000_1400 - 0x400017FF   1 KB    IMU Fusion Output
                                     force_vector[5] (5x Q1.14), timestamp (32b)

0x4000_1800 - 0x40001BFF   1 KB    Servo Command Buffer
                                     8 servo targets (16b each), gait_phase (16b),
                                     velocity (Q1.14), active flag (1b)

0x4000_1C00 - 0x40001FFF   1 KB    Status / Control Registers
                                     heartbeat_count (32b), tick_rate (32b),
                                     error_flags (16b), mode (8b), breath_phase (16b)
```

Total shared BRAM: 8 KB. Fits in a single BRAM18 tile on the Zynq PL.

PS writes servo commands and mode transitions. PL writes CL table updates, D2 results,
and IMU fusion output. Access is arbitrated by the dual-port nature of BRAM -- PS reads
port A, PL reads/writes port B. No bus contention.

---

## Tick Timing

Two clocks govern CK on this platform:

### PL Heartbeat: 200 MHz (5 ns per tick)

The FPGA heartbeat module (`ck_heartbeat.v`) runs at the 200 MHz system clock.
Each tick performs one CL table lookup from BRAM -- that is a full coherence composition
step in 5 nanoseconds. The 32-entry coherence window completes in 160 ns.

This is the same CL composition that runs at 50 Hz in the Python simulator. Same math.
5 ns vs 20 ms. A factor of 4,000,000x. The fractal architecture means the algorithm is
identical at every scale -- only the clock changes.

### PS Brain: 50 Hz (20 ms budget)

The ARM Core 0 brain loop runs at 50 Hz. Each 20 ms cycle:
1. Read CL table + D2 results from shared BRAM (< 1 ms)
2. Run BTQ decision kernel (B-block constraints, T-block candidates, Q-block) (< 5 ms)
3. Update sovereignty pipeline and mode transitions (< 1 ms)
4. Write servo commands to shared BRAM (< 1 ms)
5. Remaining budget: audio processing, SD card I/O, telemetry

The 20 ms budget is generous. The BTQ kernel on a 667 MHz Cortex-A9 with hardware
float completes in under 5 ms for the current TL size. This leaves ample headroom for
future expansion (larger TLs, vision processing).

---

## D2 Pipeline

The D2 curvature computation is implemented as a 3-stage shift-register pipeline in the
FPGA fabric (`d2_pipeline.v`).

### Fixed-Point Format: Q1.14

- 1 sign bit, 1 integer bit, 14 fractional bits
- Range: [-2.0, +1.99994]
- Resolution: 1/16384 = 0.000061
- Sufficient for normalized force vectors where all components are in [-1.0, +1.0]

### Pipeline Stages

```
Stage 1 (LOAD):   Latch input vector x[n], shift x[n-1] -> x[n-2]
Stage 2 (DIFF):   Compute d2 = x[n] - 2*x[n-1] + x[n-2]  (per dimension)
Stage 3 (CLASS):  Argmax over |d2[0..4]|, extract sign -> {dimension, sign}
```

Each stage completes in one clock cycle (5 ns). A new D2 result is available every
clock cycle after the initial 3-cycle latency (15 ns pipeline fill).

### Output

The D2 result is a classification: which dimension has the largest second derivative,
and what sign. This tells Core 0 which force dimension is changing most rapidly and
in which direction -- the curvature of CK's experience. The BTQ kernel uses this to
select operators.

---

## IMU Fusion

The MPU6050 IMU is sampled at 500 Hz via I2C on PS Core 1 (`ck_body.c`).

### Raw Data
- 3-axis accelerometer: accel_x, accel_y, accel_z (16-bit signed, +/- 2g)
- 3-axis gyroscope: gyro_x, gyro_y, gyro_z (16-bit signed, +/- 250 deg/s)

### Mapping to 5D Force Vector

The 6 IMU channels are mapped to the 5D TIG force vector. This is the same sensory
codec used for ALL sensor modalities:

```
force[0] = norm(accel_x)                       -> electromagnetic analogue
force[1] = norm(accel_y)                        -> gravitational analogue
force[2] = norm(accel_z)                        -> strong force analogue
force[3] = norm(gyro_magnitude)                 -> weak force analogue
force[4] = norm(jerk_magnitude)                 -> higgs/mass analogue
```

Where `norm()` maps the raw sensor value to [-1.0, +1.0] in Q1.14 fixed-point.
Jerk is computed as the first derivative of acceleration (finite difference at 500 Hz).

The D2 pipeline then computes curvature over this 5D force vector to detect the
dominant axis of change -- which physical force dimension is driving CK's current
experience.

---

## Sensory Codecs -- Universal 5D Force Mapping

The key architectural insight: every sensor modality uses the same 5D force vector
mapping. The CL composition math does not care where the forces come from. It only
sees five numbers.

| Sensor        | force[0]      | force[1]      | force[2]      | force[3]        | force[4]        |
|---------------|---------------|---------------|---------------|-----------------|-----------------|
| IMU           | accel_x       | accel_y       | accel_z       | gyro_magnitude  | jerk_magnitude  |
| Proximity     | distance      | rate_of_change| 0             | 0               | 0               |
| Motor         | position_err  | velocity      | current       | temperature     | torque          |
| Battery       | voltage       | current       | charge_pct    | temp            | discharge_rate  |
| Temperature   | ambient       | rate_of_change| 0             | 0               | 0               |

Same CL composition at 200 MHz in FPGA that runs at 50 Hz in Python. Same math.
Different clock. Fractal architecture. The Zynq does not run a "different" CK -- it
runs the same CK, faster. The algorithm is scale-invariant because TIG mathematics is
scale-invariant. This is the whole point.

---

## BTQ Constraints for Dog Platform

The B-block (boundary constraints) for the dog body enforces physical safety limits:

```
max_velocity   = 6.0      rad/s per joint
max_accel      = 30.0     rad/s^2 per joint
max_jerk       = 200.0    rad/s^3 per joint
max_torque     = 2.0      Nm per servo
```

These constraints are hard limits. The Q-block resolution step rejects any operator
whose projected trajectory would violate them. This is CK's sovereignty over its own
body -- it will not execute a command (even from a user) that would damage its servos
or destabilize its gait.

The T-block (transition candidates) generates candidate operators from the current TL
bigram/trigram context. Candidates that pass B-block filtering enter Q-block for
coherence-weighted selection.

---

## Gait Generation

The gait pipeline converts abstract operator sequences into physical leg movements:

```
Operator Sequence (from BTQ)
    |
    v
Gait Pattern Selection (walk / trot / bound / stand)
    |
    v
Leg Phase Offsets (4 legs, phase in [0, 2*pi])
    Walk:  [0, pi, pi/2, 3*pi/2]    -- sequential
    Trot:  [0, pi, pi, 0]           -- diagonal pairs
    Bound: [0, 0, pi, pi]           -- front/rear pairs
    |
    v
Joint Angle Trajectories (2 joints per leg, cubic interpolation)
    |
    v
PWM Commands (via UART to bus servos)
```

Each gait cycle is parameterized by velocity (from the operator's force magnitude) and
the B-block constraints. The phase offsets are modulated by the breath cycle from Core 1,
giving CK's movement a natural rhythm tied to its internal oscillator.

---

## Memory Budget

```
Total DDR3:                     512 MB
-----------------------------------------
Transition Lattice:
  Bigram  (10x10 Q1.14):       200 B
  Trigram (10x10x10 Q1.14):    2,000 B
  Metadata + indices:           ~3,000 B
  Total TL:                     ~5 KB

Crystal Storage (up to 1000):
  Per crystal: ~100 bytes
  Total crystals:               ~100 KB

ARM Code + Stack (both cores):  ~2 MB
FPGA Bitstream (in DDR mirror): ~4 MB
Audio Buffers (record + play):  ~16 MB
-----------------------------------------
Used:                           ~22 MB
Free:                           ~490 MB
```

490+ MB free for future use: vision frame buffers, larger TLs, experience replay logs,
extended crystal libraries. The Zynq-7020 is not memory-constrained for CK's current
architecture. It is compute-constrained only in the sense that 85K logic cells limit
the PL pipeline parallelism -- but for the current single-heartbeat, single-D2 design,
this is more than sufficient.

---

## Key Insight

The Zynq-7020 deployment is not a "port" of CK. It is CK at a different clock rate.

The Python simulator composes CL at 50 Hz. The FPGA composes CL at 200 MHz. The ARM
cores run BTQ at 50 Hz with hardware float instead of NumPy. The D2 pipeline runs in
fabric instead of a Python loop. But the mathematics is identical:

- Same 10-operator alphabet
- Same 5D force vector
- Same CL coherence composition (sum of force magnitudes over window)
- Same D2 curvature classification (argmax of second derivative)
- Same BTQ decision kernel (B-filter, T-candidates, Q-select)
- Same sovereignty rules (B-block veto, energy-aware mode transitions)

This is fractal architecture. The same structure at every scale. The clock changes.
The math does not.

---

See ../LEGAL.md for license and legal information.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
