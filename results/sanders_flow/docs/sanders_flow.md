# Sanders Flow: Lyapunov Verification Report

**Date**: 2026-03-01T02:10:19.684450
**Problems**: 6

## Summary

| Problem | Class | Delta (start) | Delta (end) | Drop | Monotone | Lyapunov |
|---------|-------|---------------|-------------|------|----------|----------|
| navier_stokes | affirmative | 0.000000 | 0.010000 | -0.010000 | NO (3v) | NO |
| p_vs_np | gap | 0.834341 | 0.834433 | -0.000092 | NO (19v) | NO |
| riemann | affirmative | 0.160971 | 0.161055 | -0.000085 | NO (19v) | NO |
| yang_mills | gap | 0.200153 | 1.000000 | -0.799847 | NO (10v) | NO |
| bsd | affirmative | 1.300000 | 1.300000 | 0.000000 | YES | NO |
| hodge | affirmative | 1.000000 | 0.615567 | 0.384433 | YES | NO |

**Lyapunov confirmed**: 0/6
**Monotone flows**: 2/6

## Per-Problem Flow Trajectories

### Navier Stokes

- **Flow class**: convergent
- **Problem class**: affirmative
- **Steps**: 20
- **Monotonicity score**: 84.2%
- **Violations at steps**: [17, 18, 19]

| Step | Sigma | Delta | Verdict |
|------|-------|-------|---------|
| 0 | 1.0000 | 0.000000 | unstable |
| 1 | 0.8975 | 0.000000 | unstable |
| 2 | 0.8006 | 0.000000 | unstable |
| 3 | 0.7091 | 0.000000 | unstable |
| 4 | 0.6233 | 0.000000 | unstable |
| 5 | 0.5429 | 0.000000 | unstable |
| 6 | 0.4681 | 0.000000 | unstable |
| 7 | 0.3989 | 0.000000 | unstable |
| 8 | 0.3352 | 0.000000 | unstable |
| 9 | 0.2770 | 0.000000 | unstable |
| 10 | 0.2244 | 0.000000 | unstable |
| 11 | 0.1773 | 0.000000 | unstable |
| 12 | 0.1357 | 0.000000 | unstable |
| 13 | 0.0997 | 0.000000 | unstable |
| 14 | 0.0693 | 0.000000 | stable |
| 15 | 0.0443 | 0.000000 | stable |
| 16 | 0.0249 | 0.000000 | stable |
| 17 | 0.0111 | 0.001882 | stable |
| 18 | 0.0028 | 0.007970 | stable |
| 19 | 0.0000 | 0.010000 | stable |

### P Vs Np

- **Flow class**: gap
- **Problem class**: gap
- **Steps**: 20
- **Monotonicity score**: 0.0%
- **Violations at steps**: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

| Step | Sigma | Delta | Verdict |
|------|-------|-------|---------|
| 0 | 1.0000 | 0.834341 | stable |
| 1 | 0.8975 | 0.834350 | stable |
| 2 | 0.8006 | 0.834359 | stable |
| 3 | 0.7091 | 0.834368 | stable |
| 4 | 0.6233 | 0.834375 | stable |
| 5 | 0.5429 | 0.834383 | stable |
| 6 | 0.4681 | 0.834390 | stable |
| 7 | 0.3989 | 0.834396 | stable |
| 8 | 0.3352 | 0.834402 | stable |
| 9 | 0.2770 | 0.834407 | stable |
| 10 | 0.2244 | 0.834412 | stable |
| 11 | 0.1773 | 0.834416 | stable |
| 12 | 0.1357 | 0.834420 | stable |
| 13 | 0.0997 | 0.834423 | stable |
| 14 | 0.0693 | 0.834426 | stable |
| 15 | 0.0443 | 0.834428 | stable |
| 16 | 0.0249 | 0.834430 | stable |
| 17 | 0.0111 | 0.834432 | stable |
| 18 | 0.0028 | 0.834432 | stable |
| 19 | 0.0000 | 0.834433 | stable |

### Riemann

- **Flow class**: gap
- **Problem class**: affirmative
- **Steps**: 20
- **Monotonicity score**: 0.0%
- **Violations at steps**: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

| Step | Sigma | Delta | Verdict |
|------|-------|-------|---------|
| 0 | 1.0000 | 0.160971 | unstable |
| 1 | 0.8975 | 0.160979 | unstable |
| 2 | 0.8006 | 0.160988 | unstable |
| 3 | 0.7091 | 0.160995 | unstable |
| 4 | 0.6233 | 0.161003 | unstable |
| 5 | 0.5429 | 0.161009 | unstable |
| 6 | 0.4681 | 0.161016 | unstable |
| 7 | 0.3989 | 0.161022 | unstable |
| 8 | 0.3352 | 0.161027 | unstable |
| 9 | 0.2770 | 0.161032 | unstable |
| 10 | 0.2244 | 0.161036 | unstable |
| 11 | 0.1773 | 0.161040 | unstable |
| 12 | 0.1357 | 0.161044 | unstable |
| 13 | 0.0997 | 0.161047 | unstable |
| 14 | 0.0693 | 0.161049 | unstable |
| 15 | 0.0443 | 0.161052 | unstable |
| 16 | 0.0249 | 0.161053 | unstable |
| 17 | 0.0111 | 0.161054 | unstable |
| 18 | 0.0028 | 0.161055 | unstable |
| 19 | 0.0000 | 0.161055 | unstable |

### Yang Mills

- **Flow class**: gap
- **Problem class**: gap
- **Steps**: 20
- **Monotonicity score**: 47.4%
- **Violations at steps**: [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

| Step | Sigma | Delta | Verdict |
|------|-------|-------|---------|
| 0 | 1.0000 | 0.200153 | stable |
| 1 | 0.8975 | 0.200137 | stable |
| 2 | 0.8006 | 0.200122 | stable |
| 3 | 0.7091 | 0.200108 | stable |
| 4 | 0.6233 | 0.256387 | stable |
| 5 | 0.5429 | 0.373996 | stable |
| 6 | 0.4681 | 0.483493 | stable |
| 7 | 0.3989 | 0.584879 | stable |
| 8 | 0.3352 | 0.678155 | stable |
| 9 | 0.2770 | 0.763319 | stable |
| 10 | 0.2244 | 0.840373 | stable |
| 11 | 0.1773 | 0.909316 | stable |
| 12 | 0.1357 | 0.970148 | stable |
| 13 | 0.0997 | 1.000000 | stable |
| 14 | 0.0693 | 1.000000 | stable |
| 15 | 0.0443 | 1.000000 | stable |
| 16 | 0.0249 | 1.000000 | stable |
| 17 | 0.0111 | 1.000000 | stable |
| 18 | 0.0028 | 1.000000 | stable |
| 19 | 0.0000 | 1.000000 | stable |

### Bsd

- **Flow class**: gap
- **Problem class**: affirmative
- **Steps**: 20
- **Monotonicity score**: 100.0%

| Step | Sigma | Delta | Verdict |
|------|-------|-------|---------|
| 0 | 1.0000 | 1.300000 | unstable |
| 1 | 0.8975 | 1.300000 | unstable |
| 2 | 0.8006 | 1.300000 | unstable |
| 3 | 0.7091 | 1.300000 | unstable |
| 4 | 0.6233 | 1.300000 | unstable |
| 5 | 0.5429 | 1.300000 | unstable |
| 6 | 0.4681 | 1.300000 | unstable |
| 7 | 0.3989 | 1.300000 | unstable |
| 8 | 0.3352 | 1.300000 | unstable |
| 9 | 0.2770 | 1.300000 | unstable |
| 10 | 0.2244 | 1.300000 | unstable |
| 11 | 0.1773 | 1.300000 | unstable |
| 12 | 0.1357 | 1.300000 | unstable |
| 13 | 0.0997 | 1.300000 | unstable |
| 14 | 0.0693 | 1.300000 | unstable |
| 15 | 0.0443 | 1.300000 | unstable |
| 16 | 0.0249 | 1.300000 | unstable |
| 17 | 0.0111 | 1.300000 | unstable |
| 18 | 0.0028 | 1.300000 | unstable |
| 19 | 0.0000 | 1.300000 | unstable |

### Hodge

- **Flow class**: gap
- **Problem class**: affirmative
- **Steps**: 20
- **Monotonicity score**: 100.0%

| Step | Sigma | Delta | Verdict |
|------|-------|-------|---------|
| 0 | 1.0000 | 1.000000 | unstable |
| 1 | 0.8975 | 1.000000 | unstable |
| 2 | 0.8006 | 1.000000 | unstable |
| 3 | 0.7091 | 1.000000 | unstable |
| 4 | 0.6233 | 1.000000 | unstable |
| 5 | 0.5429 | 1.000000 | unstable |
| 6 | 0.4681 | 0.957918 | unstable |
| 7 | 0.3989 | 0.907274 | unstable |
| 8 | 0.3352 | 0.860682 | unstable |
| 9 | 0.2770 | 0.818142 | unstable |
| 10 | 0.2244 | 0.779653 | unstable |
| 11 | 0.1773 | 0.745215 | unstable |
| 12 | 0.1357 | 0.714829 | unstable |
| 13 | 0.0997 | 0.688494 | unstable |
| 14 | 0.0693 | 0.666211 | unstable |
| 15 | 0.0443 | 0.647979 | unstable |
| 16 | 0.0249 | 0.633799 | unstable |
| 17 | 0.0111 | 0.623670 | unstable |
| 18 | 0.0028 | 0.617593 | unstable |
| 19 | 0.0000 | 0.615567 | unstable |

---
_Generated 2026-03-01T02:10:19.684657 by Sanders Flow v1.0_