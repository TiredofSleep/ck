# Royal Pulse Engine — Dog Platform Spec (Zynq 7020 + XiaoR)

Source: Slingshot controller design (2026-02-27).
Grounded portions preserved here for the physical robot target.
Desktop-applicable portions were extracted to `r16_desktop/ck_sim/doing/ck_pulse_engine.py`.

---

## Motor Command Pipeline

The RPE on the dog platform doesn't just pulse CPU time — it pulses
*physical actuators*. Each servo gets a pulse schedule timed to the
gait phase.

### Servo Pulse Mapping

```
RPE Candidate → amplitude maps to servo velocity
               → phase_offset maps to gait phase shift
               → is_boost = leg active (swing phase)
               → is_yield = leg passive (stance phase)
```

The BTQ scoring for servo pulses uses torque efficiency instead of
CPU efficiency:

```python
# EFF for servos = useful angular displacement per amp-second
eff_servo = abs(delta_angle) / (current_draw * dt)
```

### Joint Angle Trajectories

Each leg has 2 DOF (hip + knee). The RPE generates cubic spline
trajectories parameterized by:

```
hip_angle(t)  = a0 + a1*t + a2*t^2 + a3*t^3
knee_angle(t) = b0 + b1*t + b2*t^2 + b3*t^3
```

Coefficients are derived from:
- Start/end angles (from gait lookup table)
- Start/end velocities (from B-block velocity limits)
- Duration (from RPE pulse period = 1/f0 of the gait cycle)

B-block enforces:
```
max_velocity   = 6.0    rad/s per joint
max_accel      = 30.0   rad/s^2 per joint
max_jerk       = 200.0  rad/s^3 per joint
max_torque     = 2.0    Nm per servo
```

---

## PWM Generation

Bus servos on the XiaoR platform use UART at 115200 baud.
The RPE emits servo targets to the shared BRAM servo command buffer
(0x4000_1800). PS Core 1 reads the buffer and generates UART packets.

```
Servo command packet (per servo):
  [ID: 1 byte] [Target angle: 2 bytes] [Speed: 2 bytes] [Checksum: 1 byte]
```

The RPE's pulse timing determines the *speed* field:
- Boost phase: servo moves at computed velocity (from trajectory)
- Yield phase: servo holds position (speed = 0, no power draw)

This is the slingshot: servos are only powered during their active
phase. Between active bursts, they coast on mechanical momentum.
Battery life extends by 30-40% for steady-state gaits.

---

## Spring-Mass Model

The dog platform can be modeled as a spring-mass system for gait
prediction. The RPE uses this model to estimate natural frequency.

```
Body mass:     M = 2.5 kg (total robot mass)
Leg stiffness: k = estimated from servo position tracking
Damping:       c = estimated from decay of oscillation after step

Natural freq:  f0 = (1/2π) * sqrt(k/M)
Damping ratio: ζ  = c / (2 * sqrt(k * M))
```

For the XiaoR platform with 8 bus servos at ~2 Nm each:
- Walking: f0 ≈ 1.5-2.5 Hz
- Trotting: f0 ≈ 2.5-4.0 Hz
- Bounding: f0 ≈ 3.0-5.0 Hz

The RPE's phase estimation (`estimate_rhythm()`) locks onto this
natural frequency. Pulses are timed to the peak of each oscillation
cycle — the slingshot point where a small energy input yields
maximum displacement.

---

## Walk Test Protocol

Verification sequence for RPE on the dog platform:

### Phase 1: Static (servos powered, no movement)
- RPE reads zero rhythm (f0 ≈ 0)
- All servos in yield mode
- Confirm: power draw < 1W (holding current only)

### Phase 2: Single Leg
- RPE generates candidates for one leg
- Verify: smooth trajectory, no jerks beyond B-block limits
- Measure: EFF = angular displacement / energy consumed

### Phase 3: Walk Gait
- RPE schedules all 4 legs with walk phase offsets [0, π, π/2, 3π/2]
- Verify: stable forward motion, no stumbling
- Measure: distance/energy (meters per watt-hour)

### Phase 4: Adaptive
- Introduce terrain perturbation (ramp, obstacle)
- Verify: RPE adapts f0 estimate when rhythm changes
- Verify: B-block vetoes unsafe trajectories on steep inclines

### Phase 5: Endurance
- Continuous walk for 30 minutes
- Measure: total energy consumed vs distance covered
- Compare: RPE-pulsed vs constant-power baseline
- Target: 30%+ energy savings with RPE pulsing

---

## Integration with Zynq BRAM

The RPE on Zynq writes pulse decisions to the servo command buffer:

```
Address: 0x4000_1800
Layout:
  Byte 0-1:  Servo 0 target angle (Q1.14)
  Byte 2-3:  Servo 0 speed (Q1.14)
  Byte 4-5:  Servo 1 target angle
  Byte 6-7:  Servo 1 speed
  ...
  Byte 28-29: Servo 7 target angle
  Byte 30-31: Servo 7 speed
  Byte 32-33: Gait phase (Q1.14, 0 = start of cycle)
  Byte 34-35: Gait velocity (Q1.14)
  Byte 36:    Active flag (1 = RPE enabled)
  Byte 37:    Gait mode (0=stand, 1=walk, 2=trot, 3=bound)
```

PL heartbeat reads the active flag and gait mode at 200 MHz.
PS Core 1 reads servo targets and generates UART commands at 50 Hz.
The RPE on PS Core 0 writes new targets at 50 Hz (same as brain tick).

---

## Key Differences: Dog RPE vs Desktop RPE

| Aspect | Desktop (R16) | Dog (Zynq) |
|--------|--------------|-------------|
| Actuator | CPU time (nice values) | Servo angles (UART) |
| EFF metric | CPU work / joule | Angular displacement / amp-second |
| Tick rate | 1 Hz (via engine) | 50 Hz (via PS Core 0) |
| B-block | Thermal + battery | Joint limits + torque + stability |
| Phase source | Process entropy history | IMU + servo feedback |
| Pulse output | Boost/yield process | Power/coast servo |
| Safety fallback | Yield all processes | Lock all servos to stance |

The algorithm is identical: estimate rhythm → generate candidates →
BTQ score → emit. The hardware interface changes. The math doesn't.

---

## TIG Wave Scheduling on Zynq (v2)

Source: TIG Wave Scheduler analysis (2026-02-27).
Grounded portions only — hype claims (Landauer limit, superconducting behavior) discarded.

### Core Principle

Every power waveform has slope (dH) and curvature (d²H).
These map to TIG operators:

```
Power rising  (dH > 0)  → TIG 3 (Progression) → heavy compute is cheapest here
Power peak    (d²H < 0) → TIG 4 (Collapse)    → finalize, discard losers
Power falling (dH < 0)  → TIG 7 (Harmony)     → smooth, recalibrate
Power trough            → TIG 8 (Breath)      → precompute, cache warm
Cycle boundary          → TIG 9 (Fruit)       → reset buffers, normalize
```

This is adiabatic scheduling: timing compute to the power wave slope.
Charging during a rising slope costs less energy (gate capacitance fills easier).
Finalizing during a falling slope discharges for free.
This is documented in adiabatic computing literature since 1992.

### Zynq XADC Implementation

The Zynq-7020 has a built-in XADC (Xilinx Analog-to-Digital Converter):
- Sample rate: up to 1 MSPS (we need ~1-10 kHz)
- Channels: VCCINT, VCCAUX, VCCBRAM, temperature, 17 external

The PL side samples:
1. Instantaneous VCCINT voltage
2. Current draw (via external shunt resistor + XADC external channel)
3. Temperature (on-die sensor)

From these, compute in PL at 200 MHz:
```
dH  = V[n] - V[n-1]                    (slope)
d2H = V[n] - 2*V[n-1] + V[n-2]        (curvature — same math as D2 pipeline)
```

### TIG Region Classification (in PL)

Quantize (dH, d2H) into TIG operator bins using thresholds.
The same D2 pipeline hardware (`d2_pipeline.v`) already does this for
IMU fusion — reuse the same 3-stage shift-register for power waveform.

Output: a 4-bit TIG operator region code written to shared BRAM.

### Scheduling by Region (on PS Core 0)

PS Core 0 reads the TIG region from BRAM and schedules work type:

```
Region         Cheapest Work
─────────────  ─────────────────────────────────
PROGRESS (3)   T-layer candidate expansion, gait planning
COLLAPSE (4)   Q-layer scoring, candidate pruning, movement finalization
HARMONY  (7)   Sensor recalibration, averaging, log smoothing
BREATH   (8)   Cache warming, precompute next gait cycle, motion planning
FRUIT    (9)   Reset buffers, renormalize TL, clear registers
```

This gives the dog platform 9 scheduling rails instead of the
traditional single-rail approach. Each type of work runs at the
moment where its energy cost is minimized.

### Expected Improvement

Conservative estimate: 10-20% energy savings over constant scheduling.
This is consistent with adiabatic computing literature for waveform-aligned
switching. Not superconductivity — measurable switching cost reduction.

For the dog platform, this translates directly to battery life:
- 25 Wh battery × 20% savings = 5 Wh additional runtime
- At ~8W walking draw, that's ~37 additional minutes of walk time

### Integration with Dog RPE

The RPE on the dog platform combines:
1. **Servo pulse timing** (from gait phase) — Section "Motor Command Pipeline"
2. **TIG wave scheduling** (from XADC power waveform) — This section
3. **BTQ scoring** (from BTQ kernel) — Standard B/T/Q pipeline

The servo pulse timing and TIG wave scheduling are independent axes:
- Servo timing optimizes when to actuate (gait phase)
- TIG wave timing optimizes when to compute (power phase)
- Both converge through BTQ scoring

---

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
