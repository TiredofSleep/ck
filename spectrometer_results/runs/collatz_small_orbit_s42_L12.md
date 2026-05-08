# Delta-Spectrometer: Collatz

**Problem**: collatz
**Test case**: small_orbit
**Scan mode**: DEEP
**Seed**: 42
**Levels**: 12
**Input key**: `collatz_small_orbit_s42_L12`

## Verdict

- **Verdict**: unstable
- **Reason**: No clear convergence pattern (delta=0.0000, slope=0.0000)
- **Mathematical class**: affirmative
- **Measurement verdict**: inconclusive

## Delta Value

- **Delta (final defect)**: 0.000000
- **Defect trend**: stable (slope=0.000000)
- **Harmony fraction**: 0.000
- **Commutator persistence**: 0.000
- **SCA progress**: 0.00
- **Spine fraction**: 1.000
- **Vortex class**: unknown

## Operator Defect Vector

| Op | Name | Avg Defect |
|----|------|------------|
| 0 | VOID       | 0.000000  |
| 1 | LATTICE    | 0.000000  |
| 2 | COUNTER    | 0.000000  |
| 3 | PROGRESS   | 0.000000  |
| 4 | COLLAPSE   | 0.000000  |
| 5 | BALANCE    | 0.000000  |
| 6 | CHAOS      | 0.000000  |
| 7 | HARMONY    | 0.000000  |
| 8 | BREATH     | 0.000000  |
| 9 | RESET      | 0.000000  |

## TIG Trace

| Level | Operator | Defect | Action | Band | D2 Mag |
|-------|----------|--------|--------|------|--------|
| 0 | VOID | 0.0000 | 0.6050 | YELLOW | 0.0051 |
| 1 | VOID | 0.0000 | 0.6051 | YELLOW | 0.0053 |
| 2 | VOID | 0.0000 | 0.6041 | YELLOW | 0.0002 |
| 3 | VOID | 0.0000 | 0.6046 | YELLOW | 0.0028 |
| 4 | VOID | 0.0000 | 0.6040 | YELLOW | 0.0002 |
| 5 | VOID | 0.0000 | 0.6043 | YELLOW | 0.0014 |
| 6 | VOID | 0.0000 | 0.6051 | YELLOW | 0.0052 |
| 7 | VOID | 0.0000 | 0.6045 | YELLOW | 0.0023 |
| 8 | VOID | 0.0000 | 0.6043 | YELLOW | 0.0016 |
| 9 | VOID | 0.0000 | 0.6041 | YELLOW | 0.0005 |
| 10 | VOID | 0.0000 | 0.6045 | YELLOW | 0.0024 |
| 11 | VOID | 0.0000 | 0.6042 | YELLOW | 0.0010 |

## SDV Map (Dual Void Structure)

- **problem_class**: affirmative
- **lens_a**: Orbit length and max value
- **lens_b**: Statistical prediction (log shrinkage)
- **generator**: Collatz iteration
- **dual**: Probabilistic heuristic model
- **tau_9**: All orbits reach 1
- **dual_fixed_point_proximity**: 0.0002843048219237169
- **lens_mismatch_final**: 3516.3515286642396
- **decision_verdict**: smoothness

## Defect Trajectory

```
Defect:             
```

Range: [0.0000, 0.0000]

## Determinism & Safety

- **Hash**: `5a80f576982fd199`
- **Anomalies**: 0
- **Halted**: False

---
_Generated 2026-03-01T10:38:16.656357 by Delta-Spectrometer v1.0_