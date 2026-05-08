# Sanders Attack Report

**Date**: 2026-03-01T07:42:55.554801
**Configurations**: 12

## Overview

- **Total configurations**: 12
- **Gate PASS**: 5 (investigated with Sanders Flow)
- **Gate SKIP**: 7 (expected patterns)
- **Candidate singularities**: 1

## Gate Results

| Problem | Regime | Skeleton | Gate | Investigated | Candidate |
|---------|--------|----------|------|--------------|-----------|
| bsd | calibration | frozen | SKIP | no | no |
| bsd | frontier | frozen | PASS | YES | no |
| hodge | calibration | stable | SKIP | no | no |
| hodge | frontier | bounded | SKIP | no | no |
| navier_stokes | calibration | oscillating | PASS | YES | no |
| navier_stokes | frontier | bounded | SKIP | no | no |
| p_vs_np | calibration | frozen | SKIP | no | no |
| p_vs_np | frontier | oscillating | PASS | YES | no |
| riemann | calibration | frozen | SKIP | no | no |
| riemann | frontier | wild | PASS | YES | YES |
| yang_mills | calibration | bounded | SKIP | no | no |
| yang_mills | frontier | frozen | PASS | YES | no |

## Investigated Configurations

### Bsd (frontier)

- **Gate reason**: Frontier shows saturated FROZEN at delta=1.3000 -- structural gap or phase saturation
- **Skeleton**: FROZEN (range=0.0000, entropy=0.000)
- **Flow**: delta 1.300000 -> 1.300000 (drop=0.000000)
- **Monotonicity**: 100.0% (0 violations)
- **Lyapunov confirmed**: YES
- **Flow class**: gap
- **Candidate singularity**: no
- **Summary**: CLEARED: Anomalous skeleton but flow is Lyapunov (mono=100.0%, delta=1.3000)

### Navier Stokes (calibration)

- **Gate reason**: Calibration case shows OSCILLATING skeleton (range=0.2065) -- unexpected turbulence
- **Skeleton**: OSCILLATING (range=0.2065, entropy=0.109)
- **Flow**: delta 0.295039 -> 0.297291 (drop=-0.002253)
- **Monotonicity**: 44.4% (5 violations)
- **Lyapunov confirmed**: YES
- **Flow class**: gap
- **Candidate singularity**: no
- **Summary**: CLEARED: Anomalous skeleton but flow is Lyapunov (mono=44.4%, delta=0.2973)

### P Vs Np (frontier)

- **Gate reason**: Frontier shows OSCILLATING skeleton with non-trivial entropy (0.017) -- scale-emergent structure
- **Skeleton**: OSCILLATING (range=0.1831, entropy=0.017)
- **Flow**: delta 0.690000 -> 0.834433 (drop=-0.144433)
- **Monotonicity**: 11.1% (8 violations)
- **Lyapunov confirmed**: YES
- **Flow class**: gap
- **Candidate singularity**: no
- **Summary**: CONFIRMED GAP: OSCILLATING skeleton + flow preserves gap (delta=0.8344)

### Riemann (frontier)

- **Gate reason**: Frontier shows WILD skeleton (range=0.4614, entropy=0.918) -- extreme disorder
- **Skeleton**: WILD (range=0.4614, entropy=0.918)
- **Flow**: delta 0.038752 -> 0.161055 (drop=-0.122303)
- **Monotonicity**: 33.3% (6 violations)
- **Lyapunov confirmed**: NO
- **Flow class**: gap
- **Candidate singularity**: YES
- **Summary**: CANDIDATE: WILD skeleton + flow NOT Lyapunov-confirmed (mono=33.3%, delta=0.1611)

### Yang Mills (frontier)

- **Gate reason**: Frontier shows saturated FROZEN at delta=1.0000 -- structural gap or phase saturation
- **Skeleton**: FROZEN (range=0.0000, entropy=0.000)
- **Flow**: delta 1.000000 -> 1.000000 (drop=0.000000)
- **Monotonicity**: 100.0% (0 violations)
- **Lyapunov confirmed**: YES
- **Flow class**: gap
- **Candidate singularity**: no
- **Summary**: CONFIRMED GAP: FROZEN skeleton + flow preserves gap (delta=1.0000)

## Candidate Singularities

- **riemann (frontier)**: CANDIDATE: WILD skeleton + flow NOT Lyapunov-confirmed (mono=33.3%, delta=0.1611)

---
_Generated 2026-03-01T07:42:55.554893 by Sanders Attack v1.0_