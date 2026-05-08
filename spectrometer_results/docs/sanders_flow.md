# Sanders Flow: Lyapunov Verification Report

**Date**: 2026-03-01T02:44:04.224660
**Problems**: 6

## Summary

| Problem | Class | Strategy | Delta (start) | Delta (end) | Drop | Monotone | Lyapunov |
|---------|-------|----------|---------------|-------------|------|----------|----------|
| navier_stokes | affirmative | noise | 0.000000 | 0.010000 | -0.010000 | NO (3v) | NO |
| p_vs_np | gap | noise | 0.850836 | 0.850928 | -0.000092 | NO (19v) | NO |
| riemann | affirmative | noise | 0.162615 | 0.162700 | -0.000085 | NO (19v) | NO |
| yang_mills | gap | noise | 0.200153 | 1.000000 | -0.799847 | NO (9v) | NO |
| bsd | affirmative | noise | 1.300000 | 1.300000 | -0.000000 | YES | NO |
| hodge | affirmative | noise | 1.000000 | 0.599072 | 0.400928 | YES | NO |

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
| 14 | 0.0693 | 0.000000 | unstable |
| 15 | 0.0443 | 0.000000 | unstable |
| 16 | 0.0249 | 0.000000 | unstable |
| 17 | 0.0111 | 0.001845 | unstable |
| 18 | 0.0028 | 0.007961 | unstable |
| 19 | 0.0000 | 0.010000 | unstable |

### P Vs Np

- **Flow class**: gap
- **Problem class**: gap
- **Steps**: 20
- **Monotonicity score**: 0.0%
- **Violations at steps**: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

| Step | Sigma | Delta | Verdict |
|------|-------|-------|---------|
| 0 | 1.0000 | 0.850836 | stable |
| 1 | 0.8975 | 0.850846 | stable |
| 2 | 0.8006 | 0.850854 | stable |
| 3 | 0.7091 | 0.850863 | stable |
| 4 | 0.6233 | 0.850871 | stable |
| 5 | 0.5429 | 0.850878 | stable |
| 6 | 0.4681 | 0.850885 | stable |
| 7 | 0.3989 | 0.850891 | stable |
| 8 | 0.3352 | 0.850897 | stable |
| 9 | 0.2770 | 0.850902 | stable |
| 10 | 0.2244 | 0.850907 | stable |
| 11 | 0.1773 | 0.850912 | stable |
| 12 | 0.1357 | 0.850915 | stable |
| 13 | 0.0997 | 0.850919 | stable |
| 14 | 0.0693 | 0.850921 | stable |
| 15 | 0.0443 | 0.850924 | stable |
| 16 | 0.0249 | 0.850926 | stable |
| 17 | 0.0111 | 0.850927 | stable |
| 18 | 0.0028 | 0.850928 | stable |
| 19 | 0.0000 | 0.850928 | stable |

### Riemann

- **Flow class**: gap
- **Problem class**: affirmative
- **Steps**: 20
- **Monotonicity score**: 0.0%
- **Violations at steps**: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

| Step | Sigma | Delta | Verdict |
|------|-------|-------|---------|
| 0 | 1.0000 | 0.162615 | unstable |
| 1 | 0.8975 | 0.162624 | unstable |
| 2 | 0.8006 | 0.162632 | unstable |
| 3 | 0.7091 | 0.162640 | unstable |
| 4 | 0.6233 | 0.162647 | unstable |
| 5 | 0.5429 | 0.162654 | unstable |
| 6 | 0.4681 | 0.162660 | unstable |
| 7 | 0.3989 | 0.162666 | unstable |
| 8 | 0.3352 | 0.162671 | unstable |
| 9 | 0.2770 | 0.162676 | unstable |
| 10 | 0.2244 | 0.162681 | unstable |
| 11 | 0.1773 | 0.162685 | unstable |
| 12 | 0.1357 | 0.162688 | unstable |
| 13 | 0.0997 | 0.162691 | unstable |
| 14 | 0.0693 | 0.162694 | unstable |
| 15 | 0.0443 | 0.162696 | unstable |
| 16 | 0.0249 | 0.162698 | unstable |
| 17 | 0.0111 | 0.162699 | unstable |
| 18 | 0.0028 | 0.162699 | unstable |
| 19 | 0.0000 | 0.162700 | unstable |

### Yang Mills

- **Flow class**: gap
- **Problem class**: gap
- **Steps**: 20
- **Monotonicity score**: 52.6%
- **Violations at steps**: [4, 5, 6, 7, 8, 9, 10, 11, 12]

| Step | Sigma | Delta | Verdict |
|------|-------|-------|---------|
| 0 | 1.0000 | 0.200153 | stable |
| 1 | 0.8975 | 0.200137 | stable |
| 2 | 0.8006 | 0.200122 | stable |
| 3 | 0.7091 | 0.200108 | stable |
| 4 | 0.6233 | 0.286182 | stable |
| 5 | 0.5429 | 0.404202 | stable |
| 6 | 0.4681 | 0.514083 | stable |
| 7 | 0.3989 | 0.615825 | stable |
| 8 | 0.3352 | 0.709427 | stable |
| 9 | 0.2770 | 0.794890 | stable |
| 10 | 0.2244 | 0.872213 | stable |
| 11 | 0.1773 | 0.941397 | stable |
| 12 | 0.1357 | 1.000000 | stable |
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
| 5 | 0.5429 | 0.997112 | unstable |
| 6 | 0.4681 | 0.942280 | unstable |
| 7 | 0.3989 | 0.891509 | unstable |
| 8 | 0.3352 | 0.844801 | unstable |
| 9 | 0.2770 | 0.802154 | unstable |
| 10 | 0.2244 | 0.763568 | unstable |
| 11 | 0.1773 | 0.729044 | unstable |
| 12 | 0.1357 | 0.698582 | unstable |
| 13 | 0.0997 | 0.672182 | unstable |
| 14 | 0.0693 | 0.649843 | unstable |
| 15 | 0.0443 | 0.631565 | unstable |
| 16 | 0.0249 | 0.617350 | unstable |
| 17 | 0.0111 | 0.607195 | unstable |
| 18 | 0.0028 | 0.601103 | unstable |
| 19 | 0.0000 | 0.599072 | unstable |

---
_Generated 2026-03-01T02:44:04.224871 by Sanders Flow v1.0_