# CK v1.3 Deep Experiment Report
**Date**: 2026-03-01 00:07:05
**Total time**: 39.6s
**Depth**: L48  |  **Seeds**: 10000  |  **Base seed**: 1

---

## 1. Deep Probes (Partition Stability)

| Problem | Test Case | Depth | Final Delta | Partition | Class | Accel |
|---------|-----------|-------|-------------|-----------|-------|-------|
| bsd | large_sha_candidate | L48 | 0.016904 | FLIP | inconclusive | 0.0048 |
| bsd | rank2_explicit | L48 | 0.000006 | STABLE | inconclusive | -0.0000 |
| bsd | rank_mismatch | L48 | 1.300000 | STABLE | inconclusive | 0.0000 |
| hodge | analytic_only | L48 | 0.611620 | STABLE | inconclusive | -0.0008 |
| hodge | known_transcendental | L48 | 0.703585 | STABLE | inconclusive | -0.0003 |
| hodge | prime_sweep_deep | L48 | 0.017834 | STABLE | inconclusive | 0.0022 |
| navier_stokes | eigenvalue_crossing | L48 | 0.194190 | STABLE | inconclusive | 0.0046 |
| navier_stokes | high_strain | L48 | 0.010000 | FLIP | inconclusive | 0.0036 |
| navier_stokes | near_singular | L48 | 0.080060 | STABLE | inconclusive | 0.0007 |
| p_vs_np | adversarial_local | L48 | 0.050000 | STABLE | inconclusive | 0.0011 |
| p_vs_np | hard | L48 | 0.838380 | STABLE | supports_gap | -0.0076 |
| p_vs_np | scaling_sweep | L48 | 0.988380 | STABLE | supports_gap | -0.0231 |
| riemann | off_line | L48 | 0.167779 | STABLE | inconclusive | 0.0054 |
| riemann | off_line_dense | L48 | 0.423879 | STABLE | inconclusive | -0.0198 |
| riemann | quarter_gap | L48 | 0.074893 | STABLE | inconclusive | -0.0028 |
| yang_mills | excited | L48 | 1.000000 | STABLE | supports_gap | 0.0000 |
| yang_mills | scaling_lattice | L48 | 0.114444 | STABLE | inconclusive | 0.0098 |
| yang_mills | weak_coupling | L48 | 0.000058 | STABLE | inconclusive | 0.0256 |

**Partition stability**: 16/18 probes maintain same class from L12 to L48.

## 2. Counter-Example Hunt (Falsification Sweep)

| Problem | Class | Seeds | Falsifications | Mean Delta | Std | 99.9% CI Lower | Emp. Bound |
|---------|-------|-------|----------------|-----------|-----|----------------|------------|
| navier_stokes | affirmative | 10000 | 0 | 0.010000 | 0.000000 | 0.010000 | 0.010000 |
| p_vs_np | gap | 10000 | 0 | 0.848328 | 0.017343 | 0.847757 | 0.773475 |
| riemann | affirmative | 10000 | 0 | 0.309327 | 0.168729 | 0.303774 | 0.000043 |
| yang_mills | gap | 10000 | 0 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |
| bsd | affirmative | 10000 | 0 | 1.300000 | 0.000000 | 1.300000 | 1.300000 |
| hodge | affirmative | 10000 | 0 | 0.600007 | 0.020002 | 0.599349 | 0.528591 |

**Total falsifications across all problems**: 0
**60000 probes, 0 falsifications.** Two-class partition holds with p < 1.7e-05.

## 3. Scaling Laws (Convergence Exponents)

| Problem | Best Model | Convergence | Rate | R^2 | Half-Life | Asymptotic Delta |
|---------|-----------|-------------|------|-----|-----------|------------------|
| navier_stokes | power | algebraic | 0.5962 | 0.644 | 3.2 | 0.000000 |
| p_vs_np | power | none | 0.0686 | 0.742 | inf | 0.838380 |
| riemann | none | none | 0.0000 | 0.004 | inf | 0.167779 |
| yang_mills | exponential | none | -0.0000 | 1.000 | inf | 1.000000 |
| bsd | exponential | none | -0.0000 | 1.000 | inf | 1.300000 |
| hodge | none | none | 0.0000 | 0.009 | inf | 0.611620 |

## 4. Cross-Problem Correlation Matrix

- Within-affirmative mean r: **-0.117**
- Within-gap mean r: **0.000**
- Cross-class mean r: **-0.089**
- **Class separation: 0.011**

| | NS | RH | PNP | YM | BSD | HOD |
|---|---|---|---|---|---|---|
| **NS** | 1.000 | -0.831 | 0.032 | 0.000 | 0.000 | -0.070 |
| **PNP** | -0.831 | 1.000 | 0.266 | 0.000 | 0.000 | -0.150 |
| **RH** | 0.032 | 0.266 | 1.000 | 0.000 | 0.000 | -0.664 |
| **YM** | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| **BSD** | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| **HOD** | -0.070 | -0.150 | -0.664 | 0.000 | 0.000 | 1.000 |

## 5. Conclusions

### Partition Stability
- 16/18 probes partition-stable at L48

### Falsification Status
- 0 falsifications in 60000 probes

---
CK measures. CK does not prove.
(c) 2026 Brayden Sanders / 7Site LLC