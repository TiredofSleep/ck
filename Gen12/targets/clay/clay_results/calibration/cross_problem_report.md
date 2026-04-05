# SDV Cross-Problem Comparison Report

**Date**: 2026-02-28T19:14:03.013474
**Problems**: 6

## Summary

| Problem | Class | Verdict | Final Defect | Harmony | Trend | SCA |
|---------|-------|---------|--------------|---------|-------|-----|
| navier_stokes | affirmative | inconclusive | 0.2973 | 0.167 | oscillating | N |
| p_vs_np | gap | supports_gap | 0.7500 | 0.500 | stable | N |
| riemann | affirmative | inconclusive | 0.0000 | 0.083 | stable | N |
| yang_mills | gap | supports_gap | 0.1423 | 0.083 | oscillating | N |
| bsd | affirmative | inconclusive | 0.0000 | 0.000 | stable | N |
| hodge | affirmative | inconclusive | 0.0208 | 0.083 | stable | N |

## Problem Classification
- **Affirmative** (delta->0 supports conjecture): ['navier_stokes', 'riemann', 'bsd', 'hodge']
- **Gap** (delta>=eta supports gap): ['p_vs_np', 'yang_mills']
- **Converging**: ['riemann', 'bsd', 'hodge']
- **Persistent defect**: ['navier_stokes', 'p_vs_np', 'yang_mills']

## Navier Stokes
- Verdict: inconclusive
- Decision: smoothness
- Defect: 0.297291 (trend: oscillating)
- Topology: unknown

## P Vs Np
- Verdict: supports_gap
- Decision: smoothness
- Defect: 0.750000 (trend: stable)
- Topology: unknown

## Riemann
- Verdict: inconclusive
- Decision: smoothness
- Defect: 0.000000 (trend: stable)
- Topology: unknown

## Yang Mills
- Verdict: supports_gap
- Decision: smoothness
- Defect: 0.142294 (trend: oscillating)
- Topology: unknown

## Bsd
- Verdict: inconclusive
- Decision: smoothness
- Defect: 0.000000 (trend: stable)
- Topology: unknown

## Hodge
- Verdict: inconclusive
- Decision: smoothness
- Defect: 0.020778 (trend: stable)
- Topology: unknown
