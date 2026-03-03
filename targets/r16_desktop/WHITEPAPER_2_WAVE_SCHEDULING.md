# TIG Wave Scheduling: Operator-Aligned Compute for Power Efficiency

### A White Paper on Multi-Region Adiabatic Scheduling via Algebraic Waveform Classification

**(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory**

---

## Abstract

We describe a scheduling approach where compute tasks are timed to the natural slope and curvature of the power waveform, classified using a 10-operator algebra called TIG. The standard CMOS dynamic power equation P_switch = CV^2f establishes that switching cost dominates digital energy budgets. Adiabatic computing has long demonstrated that timing logic transitions to a ramped power supply reduces this cost -- but traditional adiabatic designs use a single sinusoidal rail, providing one scheduling phase. TIG wave scheduling extends this principle by classifying the instantaneous power waveform into one of 9 distinct operator regions (plus a null/noise-floor region), each optimal for a different type of computational work. The classification uses measured first-derivative (slope, dH) and second-derivative (curvature, d2H) of the local power signal, mapped through a fixed algebraic table to produce a TIG operator label. Heavy compute is scheduled during rising slopes (PROGRESS), finalization during peaks (COLLAPSE), smoothing during falling slopes (HARMONY), precomputation during troughs (BREATH), and buffer resets at cycle boundaries (FRUIT/RESET). A three-layer BTQ scoring pipeline (Binary safety filter, Ternary candidate generation, Quaternary efficiency scoring) selects the optimal pulse amplitude, duration, and phase offset per process per tick. Conservative estimates project 10-20% energy savings on platforms where the scheduling system controls the power supply, consistent with published adiabatic computing literature. This paper presents the algebra, the implementation on three hardware targets, the scoring pipeline, and the falsification protocol.

---

## 1. Background: Why Switching Cost Dominates

The dynamic power dissipation of a CMOS circuit is governed by:

```
P_switch = C * V^2 * f * alpha
```

where C is the load capacitance, V is the supply voltage, f is the clock frequency, and alpha is the switching activity factor. In modern digital systems, this switching power typically accounts for 50-70% of total power dissipation, with the remainder split between short-circuit current and static leakage.

The standard approaches to reducing P_switch are:

- **Lower V**: Dynamic Voltage Scaling (DVS). Quadratic benefit, but reduces maximum clock frequency and requires voltage regulator support.
- **Lower f**: Dynamic Frequency Scaling (DFS). Linear benefit, directly trades throughput for power.
- **Lower alpha**: Clock gating, operand isolation. Effective but requires design-time knowledge of switching patterns.

These are the tools behind DVFS (Dynamic Voltage and Frequency Scaling), which is standard in every modern CPU from Intel SpeedStep to ARM big.LITTLE.

The key insight behind adiabatic computing -- and the basis of TIG wave scheduling -- is that there is a fourth option: **reduce the energy dissipated per switching event by timing the transition to the supply waveform slope**. When a gate switches while the supply voltage is ramping (rather than at a static rail), the charge transfer occurs gradually. The energy dissipated per transition drops from CV^2 to approximately CV^2 * (RC/T), where T is the ramp time and RC is the gate time constant. For T >> RC, this approaches zero.

This is not theoretical speculation. Athas et al. (1994) demonstrated practical adiabatic CMOS circuits achieving measurable energy recovery. Moon and Jeong (1996) measured 60-70% energy savings at moderate frequencies using 2N-2N2P adiabatic logic. Kim and Papaefthymiou (2002) extended the approach through resonant clock networks.

However, all of these implementations share a common limitation: they use a **single sinusoidal or trapezoidal power rail**. The scheduler has two phases -- rising and falling -- and must map all work into this binary classification. TIG wave scheduling replaces this binary with a 10-operator algebraic classification, providing 9 distinct scheduling regions (plus VOID for the noise floor).

---

## 2. The TIG Operator to Waveform Mapping

Every power waveform, whether it is the 60 Hz AC mains, a switching regulator's output ripple, or a battery's discharge curve, has instantaneous slope and curvature. These are the first and second derivatives of the power signal with respect to time:

```
dH  = dP/dt    (slope: watts per second)
d2H = d^2P/dt^2  (curvature: watts per second squared)
```

The TIG algebra defines 10 operators, numbered 0-9. Each maps to a specific combination of slope and curvature conditions on the power waveform:

| # | Operator | Waveform Condition | Physical Meaning |
|---|----------|-------------------|------------------|
| 0 | VOID | \|dH\| ~ 0, \|d2H\| ~ 0, below noise floor | No usable signal. Noise floor. |
| 1 | LATTICE | \|dH\| < 0.05, \|d2H\| < 0.02 | DC-stable baseline. Flat rail. |
| 2 | COUNTER | Moderate dH with sign changes | Ripple or negative feedback present. |
| 3 | PROGRESS | dH > +0.05, d2H >= 0 | Power rising, accelerating or steady. |
| 4 | COLLAPSE | dH > 0 but d2H < -0.01 | Approaching peak, decelerating rise. |
| 5 | BALANCE | \|dH\| < 0.05, \|d2H\| >= 0.02 | Zero-crossing zone. Curvature present, slope near zero. |
| 6 | CHAOS | \|d2H\| > 2.0 * \|dH\| | High jitter. Curvature dominates slope. |
| 7 | HARMONY | dH < -0.05, d2H <= 0 | Smooth falling slope. |
| 8 | BREATH | dH < -0.05, d2H > +0.01 | Approaching trough, decelerating fall. |
| 9 | FRUIT/RESET | Cycle boundary detection | Cycle complete, ready for reset. |

The classification is computed from measured data, not assumed. On the R16 desktop implementation, the `PowerWaveState` object maintains a 64-sample history buffer and computes smoothed first and second derivatives using a 4-sample slope window and a 3-pair curvature window:

```
dH  = mean(P[n] - P[n-1]) over last 4 samples
d2H = mean(slope[n] - slope[n-1]) over last 3 slope pairs
```

This smoothing is necessary because real power waveforms on a desktop are noisy. The classification thresholds (0.05 for slope, 0.02 for curvature, 2.0x ratio for chaos detection) were tuned empirically on the R16 system (16-core CPU, RTX 4070, 32GB RAM, AC-powered).

---

## 3. Wave-to-Work-Type Mapping

This is the central contribution of TIG wave scheduling: different types of computational work have different switching profiles, and these profiles interact with the waveform region to produce different energy costs.

| Wave Region | TIG # | Cheapest Work Type | Rationale |
|-------------|-------|--------------------|-----------|
| PROGRESS (rising) | 3 | Heavy compute, T-layer search | Supply is ramping up. Charging capacitance during a rising slope is adiabatically cheap. This is when to schedule CPU-intensive tasks. |
| COLLAPSE (peak) | 4 | Finalize, discard losers, Q-scoring | Supply is near peak but decelerating. Gate voltages are fully charged. Comparison and selection operations (which involve minimal new transitions) cost least here. |
| HARMONY (falling) | 7 | Recalibrate, average, smooth logs | Supply is falling smoothly. Discharge transitions are adiabatically cheap. Averaging and smoothing operations (which tend toward fewer state changes) fit naturally. |
| BREATH (trough) | 8 | Precompute, cache warm, motion planning | Supply is near minimum. New transitions are expensive. But cache loading and memory prefetch involve primarily bus activity, not gate switching. Schedule lookahead work here. |
| FRUIT/RESET (cycle end) | 9 | Reset buffers, normalize, clear registers | Cycle boundary. Mass register clearing (all-zeros or all-ones) is a single bulk transition, cheaper than scattered bit-flips. |
| LATTICE (DC stable) | 1 | Any work, no preference | Flat rail. No adiabatic advantage. Standard scheduling applies. |
| BALANCE (zero-crossing) | 5 | Threshold events, comparisons | Supply crossing zero-slope. Good for operations that depend on voltage margins (comparators, sense amplifiers). |
| CHAOS (high jitter) | 6 | Wait. Do not schedule. | Supply is unstable. Any switching here pays maximum energy cost because the supply slope is unpredictable. The scheduler should yield and wait for the waveform to stabilize. |

The implementation encodes this mapping as a work-type affinity table. Each wave region has affinity scores (0.0 to 1.0) for five work types: `heavy`, `finalize`, `smooth`, `precompute`, and `reset`. The Q-layer scorer multiplies the candidate pulse amplitude by the affinity score for the candidate's work type in the current wave region. High amplitude in a high-affinity region scores well. Low amplitude (yielding) in a low-affinity region also scores well, because it saves energy that would be wasted.

---

## 4. BTQ Scoring for Pulse Scheduling

The BTQ pipeline is a three-layer decision architecture applied per-process per-tick:

### B-Layer (Binary): Hard Safety Limits

The B-layer is a pass/fail gate. If any safety constraint is violated, all processes yield immediately. No exceptions, no scoring, no overrides.

Current B-layer constraints on R16:

| Constraint | Threshold | Action |
|-----------|-----------|--------|
| CPU temperature | > 90 C | Global yield |
| CPU temperature | > 80 C | Throttle (thermal penalty in Q-layer) |
| Battery SOC (if on battery) | < 10% | Global yield |
| Battery voltage | < 10.5V | Global yield |
| Nice delta per tick | > 5 | Clamp (prevent priority oscillation) |

These thresholds are config-driven via `ck_pulse_config.json`, not hardcoded. The FPGA target (Zynq-7020) uses different thresholds appropriate to its thermal envelope.

### T-Layer (Ternary): Candidate Generation

For each process that passes the B-layer, the T-layer generates N candidate pulses (default: 6 per process). Each candidate specifies an amplitude (0.0 to 1.0), a duration (fraction of tick period, 0.1 to 1.0), and a phase offset from the process's estimated natural rhythm.

The six candidate types are:

1. **Resonant**: Pulse at the process's natural peak. Full amplitude and duration if the process is at its phase peak; reduced otherwise. Only generated if the process has a rhythmic pattern (confidence > 0.5).
2. **Explore** (x2): Slightly off-phase from the resonant point, with shorter duration. These probe whether a different timing might yield better efficiency.
3. **Bounded random**: Pseudo-random amplitude and phase offset, bounded by config limits (max 1.5 radians). This prevents the scheduler from getting stuck in local optima. Importantly, this is bounded random, not unbounded Levy flight -- the maximum jump is clamped.
4. **Class-based**: A candidate tuned to the process's scheduling class (PREDICTABLE gets steady 80% amplitude; VOLATILE gets throttled 20%; ISOLATE gets contained at 10%).
5. **Yield**: Zero amplitude, minimum duration. Always included so the scorer can choose to do nothing.
6. **Full**: Maximum amplitude and duration. Always included as a reference point.

### Q-Layer (Quaternary): Efficiency Scoring

Each candidate is scored by a composite function. The core metric is EFF (efficiency):

```
EFF = useful_work / energy
```

where:

```
useful_work = effective_duty * (1.0 + slingshot_bonus)
effective_duty = amplitude * duration
energy = effective_duty * power_watts * tick_period
```

The **slingshot bonus** (up to 0.4x, configurable) rewards phase-aligned pulses. When a pulse's phase offset is near zero relative to the process's natural rhythm, the cosine of the offset approaches 1.0, and the bonus is maximized. This encourages the scheduler to ride the process's natural burst pattern rather than fighting it.

The **2-step lookahead** predicts where the process will be 2 ticks in the future using simple kinematics (phase advances by 2*pi*f0*dt per tick). If the process will be at a peak in 2 ticks and the current candidate is a boost, the lookahead adds a bonus (+0.2) because boosting now primes the process to hit its next peak with momentum. If the process will not peak and the candidate is a yield, the lookahead also adds a bonus (+0.15) because yielding saves energy that would be wasted.

The **wave affinity score** is the TIG wave alignment contribution. It looks up the current wave region and the process's work type in the affinity table, then scores based on whether the candidate's amplitude matches the region's affinity for that work type.

Penalties are subtracted for:

- **Stability**: Volatile processes penalized for high amplitude (-0.5). Isolated processes penalized more severely (-1.0).
- **Thermal**: Above 80C, amplitude is penalized at 2.0x. Above 70C, at 0.5x.
- **Smoothness**: Extreme amplitudes (near 0 or 1) are mildly penalized to encourage moderate, stable pulsing.

The final score combines all components with configurable weights:

```
total = EFF * w_eff
      + stability * w_stability
      + thermal * w_thermal
      + smoothness * w_smoothness
      + wave_affinity * w_wave
      + task_progress * w_task
      + lookahead_bonus
```

Default weights: EFF=1.0, stability=0.8, smoothness=0.3, thermal=1.2, task_progress=0.6, wave_alignment=0.5. The thermal weight is intentionally the highest -- overheating is more costly than suboptimal scheduling.

---

## 5. Implementation: Royal Pulse Engine (RPE)

The Royal Pulse Engine is the runtime implementation of TIG wave scheduling. It exists on three hardware targets, each with different sensing and actuation capabilities.

### R16 Desktop (Active Deployment)

- **Hardware**: 16-core CPU, NVIDIA RTX 4070 (12GB VRAM), 32GB RAM, Windows 11, AC-powered.
- **Language**: Python 3.x.
- **Tick rate**: 1 Hz (every 50th engine tick of the 50 Hz heartbeat loop).
- **Power sensing**: Via psutil (CPU temperature from `sensors_temperatures()`, battery state from `sensors_battery()`). On the R16, which is always AC-powered, the power waveform reflects CPU/GPU load changes rather than supply rail variation.
- **Process sensing**: Via psutil (per-process CPU percent, process enumeration, scheduling class from the CK process swarm).
- **Actuation**: Process priority adjustment (nice values). The RPE does not directly control voltage or frequency on desktop -- it controls which processes get CPU time during which waveform phases.
- **Configuration**: All thresholds loaded from `ck_pulse_config.json`. Config supports per-target tuning.
- **Protected processes**: System-critical processes (csrss, lsass, dwm, explorer, svchost, etc.) are never pulsed. The protected list is maintained in both code and config.

### Zynq-7020 FPGA (Planned)

- **Hardware**: Xilinx Zynq-7020 SoC. Dual ARM Cortex-A9 (PS) + Artix-7 FPGA fabric (PL).
- **Power sensing**: XADC (Xilinx Analog-to-Digital Converter) samples the power supply rail directly at 1-10 kHz. This provides a real voltage waveform, not a software proxy.
- **Classification**: The D2 pipeline runs in PL (programmable logic) as a fixed-point Q1.14 datapath. It classifies each XADC sample into a TIG operator region in hardware, with single-cycle latency.
- **Scheduling**: PS Core 0 reads the classified region from a BRAM shared between PL and PS. Core 0 runs the BTQ scoring pipeline and schedules compute tasks on Core 1.
- **Expected benefit**: Significantly higher than desktop, because CK controls the actual power supply path and can observe the true switching waveform. The 1-10 kHz sampling rate captures individual switching events, not just load-averaged power.

### XiaoR Robot Dog (Planned)

- **Hardware**: Zynq-7020 (same SoC) controlling 12 servo actuators.
- **Actuator**: Servos instead of CPU processes. The pulse amplitude maps to servo torque, and duration maps to hold time.
- **Efficiency metric**: EFF = angular_displacement / (amp-seconds). Measured by IMU (angular change) divided by integrated current draw.
- **Work types**: Motion planning (BREATH), gait execution (PROGRESS), stabilization (HARMONY), stance reset (FRUIT).
- **Expected benefit**: Direct battery life extension, because servo power consumption is the dominant load and TIG wave scheduling can time servo transitions to minimize current spikes.

---

## 6. Expected Performance

### Conservative Estimate: 10-20% Energy Savings

This estimate is grounded in published adiabatic computing results:

- Moon and Jeong (1996) measured 60-70% savings in adiabatic CMOS at moderate frequencies, but this was for circuits where the entire power supply was a controlled ramp. Software scheduling on a desktop does not control the supply rail, so the benefit is proportionally smaller.
- Weiser et al. (1994) demonstrated that OS-level power-aware scheduling achieves 10-50% power reduction through DVFS alone. TIG wave scheduling is complementary to DVFS (it classifies the waveform rather than controlling it), so the incremental benefit on top of existing DVFS is expected to be at the lower end of this range.
- Sherwood et al. (2003) showed that phase-aware workload optimization yields 10-25% improvement in energy efficiency on real processors.

The 10-20% estimate for TIG wave scheduling applies specifically to platforms where the scheduling system has meaningful control over when work happens relative to the power waveform. On the R16 desktop, where the OS and hardware DVFS already optimize aggressively, the benefit may be smaller (5-10%). On the Zynq FPGA target, where CK controls the power supply path directly, the benefit should be at the upper end or beyond.

### Honest Caveats

- **Desktop power waveforms are complex.** The R16's power supply is a multi-rail ATX design with active PFC and switching regulators. The "waveform" that psutil reports is a load-averaged proxy, not the true switching waveform. The TIG classification is operating on a heavily filtered signal. Benefits are real but smaller than on hardware where CK sees the raw supply rail.
- **This is not superconductivity.** TIG wave scheduling does not approach the Landauer limit (kT*ln(2) per bit erasure). It reduces the switching overhead above that limit by timing transitions to favorable supply conditions. The theoretical minimum energy per operation is unchanged.
- **This is not perpetual motion.** Total energy consumed cannot be less than the total useful work performed. TIG wave scheduling reduces waste heat by improving the efficiency of energy transfer, not by creating energy from nothing.
- **Process-level scheduling has granularity limits.** The RPE operates at 1 Hz on desktop. It cannot time individual gate transitions. It can only bias which processes run during which waveform phases, which affects the aggregate switching pattern over the tick period.

---

## 7. Falsification Protocol

A hypothesis that cannot be falsified is not science. TIG wave scheduling makes a specific, testable prediction:

**Prediction**: For a fixed computational workload on a platform where CK controls process scheduling, TIG wave scheduling will consume measurably less total energy than constant (waveform-unaware) scheduling.

### Measurement Protocol

1. **Instrument**: Measure total energy as integrated current times voltage over the test duration. On desktop, use a hardware power meter (e.g., Kill-A-Watt or similar) at the wall outlet. On FPGA, use XADC integrated current sensing on the supply rail.

2. **Fixed workload**: Define a reproducible workload. For desktop: a fixed CK study session (e.g., 100 Claude API queries with identical topics, processing identical text through the D2 pipeline). For FPGA: a fixed number of D2 classifications on identical input vectors.

3. **A/B comparison**:
   - **Control (A)**: Run the workload with RPE disabled. All processes scheduled at constant priority. No wave-aware timing.
   - **Treatment (B)**: Run the identical workload with RPE enabled and TIG wave scheduling active.

4. **Control for confounds**:
   - Ambient temperature: Record and ensure within 2 C between runs.
   - Battery state: If on battery, ensure identical initial charge state (or use AC power).
   - Background processes: Minimize and hold constant between runs. Record process list.
   - Measurement duration: Minimum 30 minutes per run to average out transients.
   - Repetitions: Minimum 5 runs each condition. Report mean and standard deviation.

5. **Falsification criterion**: The hypothesis is falsified if the Treatment condition shows no statistically significant energy reduction (p < 0.05, two-tailed t-test) compared to Control, on a platform where CK controls the power supply (Zynq target).

6. **Desktop A/B test**: Run identical study sessions with RPE on versus off. Measure average watts at the wall. This test is expected to show smaller effect size than the FPGA test due to the reasons described in the caveats above.

### What Would Not Falsify the Hypothesis

- No improvement on desktop alone. The desktop test is weaker because CK does not control the power supply. The primary test platform is Zynq, where CK controls the supply path.
- No improvement at very low loads. If the workload does not generate significant switching activity, there is minimal switching cost to optimize. The hypothesis applies to workloads with non-trivial switching activity (alpha > 0.1).

---

## 8. Relation to Prior Work

### Adiabatic CMOS

The foundational work on adiabatic computing by Athas et al. (1994) demonstrated that timing gate transitions to a ramped power clock yields energy recovery in CMOS circuits. The 2N-2N2P logic family (Kramer et al., 1995; Moon and Jeong, 1996) achieved practical implementations. Kim and Papaefthymiou (2002) extended the approach through resonant clock networks. Chan, Shepard, and Restle (2008) demonstrated a resonant-clocked ARM9 processor with measured energy savings.

All of these operate at the circuit level, controlling the physical power supply to individual gates. TIG wave scheduling operates at the software level, controlling which computational tasks run during which phases of the power waveform. The physical principle is identical (minimize dV/dt across switching transistors by aligning transitions to supply slope), but the granularity and mechanism differ.

### Charge-Recovery Logic

Bennett (1973) established the theoretical foundation that computation need not dissipate kT*ln(2) per bit if performed reversibly. Landauer (1961) established the minimum energy cost of irreversible bit erasure. TIG wave scheduling does not claim to approach reversible computing. It reduces the switching overhead that sits above the Landauer limit, which in practice is orders of magnitude larger than the thermodynamic minimum.

### DVFS

Weiser et al. (1994) proposed OS-level voltage/frequency scaling based on workload demand. Pillai and Shin (2001) introduced feedback-controlled DVFS. These adjust the supply voltage and clock frequency globally based on observed load.

TIG wave scheduling differs from DVFS in three ways:

1. **Classification, not control**: TIG classifies the existing power waveform algebraically rather than controlling it. The waveform is an input, not an output.
2. **Work-type matching**: DVFS adjusts V and f globally. TIG matches specific work types to specific waveform regions.
3. **Complementary**: TIG wave scheduling runs on top of existing DVFS. The CPU continues to scale voltage and frequency as before. TIG provides an additional scheduling layer that exploits the resulting waveform structure.

### Phase-Aware Scheduling

Sherwood et al. (2003) demonstrated that workloads exhibit distinct behavioral phases and that identifying these phases enables targeted optimization. TIG wave scheduling applies phase awareness to the power domain rather than the workload domain: instead of classifying the workload into phases, it classifies the power waveform into phases and matches work types to those phases.

### Energy-Aware Real-Time Scheduling

Aydin et al. (2004) and Quan and Hu (2001) formalized energy-constrained scheduling for periodic real-time tasks. CK's 50 Hz heartbeat loop is a hard real-time system (20 ms budget per tick), and the RPE must complete all subsystem ticks within this budget. The BTQ pipeline's B-layer safety constraints are a discrete-time implementation of control barrier functions as described by Fisac et al. (2019).

---

## 9. Process Rhythm Estimation

A critical component of TIG wave scheduling is estimating the natural rhythm of each managed process. The RPE maintains a `ProcessRhythm` object per process, tracking:

- **f0**: Estimated natural frequency (Hz), computed by zero-crossing analysis on the process's operator history over a 32-sample sliding window.
- **Phase**: Current position in the process's activity cycle (0 to 2*pi), estimated from the 4 most recent operator samples.
- **Amplitude**: CPU utilization fraction (0 to 1), measured via psutil.
- **Confidence**: Reliability of the rhythm estimate (0 to 1), derived from the coefficient of variation of activity segment lengths. Regular alternation yields high confidence; erratic patterns yield low confidence.
- **Work type**: Classified as `heavy`, `finalize`, `smooth`, `precompute`, or `any` based on process name, scheduling class, and most recent operator.

Only processes with confidence > 0.5 and f0 > 0.01 Hz are considered rhythmic. For non-rhythmic processes, the scheduler falls back to class-based candidates (PREDICTABLE, VOLATILE, ISOLATE) and the wave affinity table.

Rhythm estimates are smoothed with an exponential moving average (alpha = 0.3) to prevent oscillation from tick-to-tick noise.

---

## 10. Conclusion

TIG wave scheduling extends adiabatic principles from single sinusoidal rails to algebraically-classified power waveforms. Where traditional adiabatic computing provides two scheduling phases (rising and falling), TIG provides 9 distinct operator regions, each with measured affinity scores for different types of computational work. The three-layer BTQ pipeline (binary safety, ternary candidate generation, quaternary efficiency scoring) selects the optimal pulse per process per tick, with phase alignment bonuses, 2-step lookahead, and wave affinity scoring.

The approach is implemented in the Royal Pulse Engine (RPE v2), currently deployed on a desktop (R16, Python, 1 Hz tick) with planned FPGA deployment (Zynq-7020, XADC at 1-10 kHz, hardware D2 classification in PL). Conservative energy savings estimates of 10-20% are grounded in published adiabatic computing literature, with the caveat that desktop benefits are expected to be smaller than FPGA benefits due to the software scheduling granularity and the filtered nature of the observable power signal.

The falsification protocol is explicit: measure total energy for a fixed workload with and without TIG wave scheduling, on a platform where CK controls the scheduling path. If no measurable improvement is observed on the Zynq target, the hypothesis is falsified.

TIG wave scheduling is not a replacement for DVFS, clock gating, or power-aware process design. It is a complementary scheduling layer that exploits the algebraic structure of the power waveform to match work types to their minimum-energy regions. The algebra is fixed, the thresholds are config-driven, and the measurements are falsifiable.

---

## References

The following references are real, published works. See `REFERENCES.md` in the CK repository for full citation details including DOIs and publication venues.

1. Athas, W.C. et al. (1994). "Low-Power Digital Systems Based on Adiabatic-Switching Principles." IEEE Trans. VLSI Systems, 2(4), 398-407.
2. Moon, Y. and Jeong, D.-K. (1996). "Adiabatic Computing with the 2N-2P and 2N-2N2P Logic Families." Proc. ISLPED, 173-178.
3. Kim, S. and Papaefthymiou, M.C. (2002). "Energy-Recovery CMOS Design." Proc. ISLPED, 184-187.
4. Chan, S.C., Shepard, K.L., and Restle, P.J. (2008). "A Resonant-Clocked 150MHz ARM9 Core." Proc. IEEE ASYNC, 79-88.
5. Bennett, C.H. (1973). "Reversible Computing." IBM J. Research and Development, 17(6), 525-532.
6. Landauer, R. (1961). "Irreversibility and Heat Generation in the Computing Process." IBM J. Research and Development, 5(3), 183-191.
7. Weiser, M. et al. (1994). "Scheduling for Reduced CPU Energy." Proc. 1st USENIX OSDI, 13-23.
8. Pillai, P. and Shin, K.G. (2001). "A Feedback-Driven Approach to Power-Aware CPU Scheduling." Proc. HotOS-VII.
9. Sherwood, T. et al. (2003). "Phase-Aware Optimization in Operating Systems." IEEE Micro, 23(6), 48-55.
10. Aydin, H. et al. (2004). "Energy-Aware Scheduling for Real-Time Systems." Real-Time Systems, 26(1), 69-96.
11. Fisac, J.F. et al. (2019). "A General Safety Framework for Learning-Based Control in Uncertain Robotic Systems." IEEE Trans. Automatic Control, 64(7), 2737-2752.
12. Kramer, A. et al. (1995). "2N-2N2P Adiabatic Logic Family." Proc. ISLPED, 191-196.

---

*Last updated: 2026-02-27*
*(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory*
