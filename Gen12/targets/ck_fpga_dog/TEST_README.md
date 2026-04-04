# Gen11 Bridge Test Suite — README

## What this is

Complete validation suite for all 5 Gen11 insertion points in `ck_r16_bridge_gen11.py`.
No hardware required. No imports beyond Python standard library.
Runnable anywhere: local Python, ChatGPT code interpreter, CI.

## Files

| File | Purpose |
|---|---|
| `test_gen11_bridge.py` | Full test suite + synthetic scenarios + metrics pipeline |
| `example_synthetic_log.csv` | Generated on first `--demo` run |

## How to run

```bash
# Standard run — all tests, pass/fail summary
python test_gen11_bridge.py

# Verbose — shows every PASS line
python test_gen11_bridge.py -v

# Demo mode — runs tests, then prints synthetic logs + A/B summary + writes CSV
python test_gen11_bridge.py --demo
```

## Expected console output (clean run)

```
GEN11 BRIDGE TEST SUITE
T* = 0.714286  MASS_GAP = 0.285714  W_BHML = 0.0600  ESTOP = 0.2

────────────────────────────────────────────────────────────
  3A — W_BHML Deadband (W=0.06)
────────────────────────────────────────────────────────────
────────────────────────────────────────────────────────────
  3B — RECOVER Band (0.20 ≤ C < 2/7)
────────────────────────────────────────────────────────────
...
════════════════════════════════════════════════════════════
  RESULTS: XX/XX passed  (0 failed)
════════════════════════════════════════════════════════════

  BENCH READINESS STATUS
  ...
  VERDICT: READY WITH CAVEATS
```

## What each section tests

### 3A — W_BHML Deadband
- Suppression when |ΔC| < 0.06 (W_BHML)
- Pass-through when |ΔC| > 0.06
- Max-hold override at 50 ticks (prevents freeze)
- Conservation: suppressed_count + actual_transitions ≈ total_would-be-transitions
- Instance isolation: two Gen11 layers don't share state

### 3B — RECOVER Band
- All 5 coherence band boundaries (exact values)
- RECOVER [0.20, 0.286) always maps to STAND gait
- RC-1 claim: no WALK or TROT during RECOVER band
- Ramp test: coherence 0→1 produces correct gait sequence

### 3C — Vortex Stumble Monitor
- Trigger fires at exactly tick 3 (not 1, not 2)
- Counter resets to 0 after trigger
- No false positives: 2+1+2 interleaved pattern never triggers
- High coherence + bad ops → watchdog overrides coherence-based gait
- Known algebraic values: vortex(7,7,7)=HARMONY, vortex(3,9,1)=HARMONY

### 3D — BHML Arbitration Gate
- Bad intermediates = {CHAOS(6), COLLAPSE(4)}
- WALK→TROT intermediate = COLLAPSE(4) → GATED (by algebra, not tuning)
- ESTOP never gated
- Gated transitions route to STAND

### 3E — First-G Stride Resonance
- R(1,f) = 1.0 for all f (algebraic identity)
- R(p-1, 1/p) = 1/(p-1)² for p=2,3,5,7 (harmonic countdown)
- Floor = 1/16 = 0.0625 (p=5 harmonic countdown)
- First-G = Fejér kernel / k identity verified
- Frequency cap at 0.99 prevents singularity

### Synthetic Scenarios
- SC-1: Quiet stable stance — 0 changes, 0 watchdog fires
- SC-2: Micro-jitter around T* — deadband activations counted
- SC-3: RECOVER band crossing — no WALK/TROT during RECOVER
- SC-4: Shove proxy (3 bad vortex ticks) — watchdog fires at tick 2
- SC-5: False positive challenge (2+1+2) — 0 watchdog fires
- SC-6: Confirmed watchdog trigger

### Metrics Pipeline
- Gait change rate (per minute)
- Deadband activation rate (per minute)
- Vortex harmony fraction
- Max consecutive non-harmony
- RECOVER entry count
- Control jitter variance
- Conservation check: B changes + B suppressed ≈ A changes ± 3

## Log schema

Every cycle produces a row with these fields:

| Field | Type | Range | Notes |
|---|---|---|---|
| tick | int | ≥ 0 | Integer tick counter |
| timestamp_ms | float | ≥ 0 | Wall clock ms |
| coherence | float | [0,1] | C from STATE packet |
| being_op | int | [0,9] | Operator from STATE |
| doing_op | int | [0,9] | Operator from STATE |
| becoming_op | int | [0,9] | Operator from STATE |
| gait_cmd | int | {0,1,2,3} | 0=STAND 1=WALK 2=TROT 3=ESTOP |
| coherence_band | str | {ESTOP,RECOVER,STAND,WALK,TROT} | 5-band classification |
| deadband_suppressed | int | {0,1} | 1 = transition suppressed by W_BHML |
| bhml_gated | int | {0,1} | 1 = transition blocked by BHML gate |
| r_stride | float | ≥ 0 | First-G R(k,f) value |
| r_stride_below_floor | int | {0,1} | 1 = R < 1/16 (floor) |
| vortex_is_harmony | int | {0,1} | 1 = vortex(being,doing,becoming) = HARMONY |
| consecutive_nonharmony | int | ≥ 0 | Ticks since last harmony vortex |
| watchdog_triggered | int | {0,1} | 1 = 3+ consecutive non-harmony, STAND forced |
| loop_interval_ms | float | > 0 | Actual bridge loop interval |
| scenario | str | any | Label for analysis grouping |

Synthetic and real-hardware runs use identical schema. A/B comparison is column-for-column.

## What is NOT tested here (hardware only)

- Serial packet timing jitter (OS-dependent)
- Engine coherence range (may not naturally enter RECOVER)
- Whether real disturbances produce bad being/doing/becoming operators
- Walking gait + step counter (3E stride scoring requires walking)
- Servo current logging (hardware channel only)

## Bench readiness

**READY WITH CAVEATS.** Software layer is deterministic and tested. Wire FPGA → dog, run leash test, then run bridge. The logs will confirm whether each insertion point activates under live conditions.
