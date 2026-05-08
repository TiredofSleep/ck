# CK v1.3 Deep Experiment Report
**Date**: 2026-03-01 00:07:36
**Total time**: 0.1s
**Depth**: L96  |  **Seeds**: 10000  |  **Base seed**: 1

---

## 1. Deep Probes (Partition Stability)

| Problem | Test Case | Depth | Final Delta | Partition | Class | Accel |
|---------|-----------|-------|-------------|-----------|-------|-------|
| bsd | large_sha_candidate | L96 | 0.008754 | FLIP | inconclusive | 0.0021 |
| bsd | rank2_explicit | L96 | 0.000003 | STABLE | inconclusive | 0.0000 |
| bsd | rank_mismatch | L96 | 1.300000 | STABLE | inconclusive | 0.0000 |
| hodge | analytic_only | L96 | 0.606743 | STABLE | inconclusive | -0.0003 |
| hodge | known_transcendental | L96 | 0.687782 | STABLE | inconclusive | 0.0001 |
| hodge | prime_sweep_deep | L96 | 0.009692 | STABLE | inconclusive | 0.0012 |
| navier_stokes | eigenvalue_crossing | L96 | 0.196628 | STABLE | inconclusive | 0.0018 |
| navier_stokes | high_strain | L96 | 0.010000 | FLIP | inconclusive | 0.0010 |
| navier_stokes | near_singular | L96 | 0.060659 | STABLE | inconclusive | 0.0002 |
| p_vs_np | adversarial_local | L96 | 0.050000 | STABLE | inconclusive | 0.0002 |
| p_vs_np | hard | L96 | 0.843257 | STABLE | supports_gap | -0.0022 |
| p_vs_np | scaling_sweep | L96 | 0.993257 | STABLE | supports_gap | -0.0142 |
| riemann | off_line | L96 | 0.176082 | STABLE | inconclusive | 0.0024 |
| riemann | off_line_dense | L96 | 0.422155 | STABLE | inconclusive | -0.0063 |
| riemann | quarter_gap | L96 | 0.074622 | STABLE | inconclusive | -0.0009 |
| yang_mills | excited | L96 | 1.000000 | STABLE | supports_gap | 0.0000 |
| yang_mills | scaling_lattice | L96 | 0.014427 | STABLE | inconclusive | 0.0058 |
| yang_mills | weak_coupling | L96 | 0.000034 | STABLE | inconclusive | 0.0081 |

**Partition stability**: 16/18 probes maintain same class from L12 to L96.

## 5. Conclusions

### Partition Stability
- 16/18 probes partition-stable at L96

### Falsification Status

---
CK measures. CK does not prove.
(c) 2026 Brayden Sanders / 7Site LLC