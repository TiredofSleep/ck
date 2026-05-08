# SDV Cross-Problem Comparison Report

**Date**: 2026-02-28T19:14:06.882469
**Problems**: 6

## Summary

| Problem | Class | Verdict | Final Defect | Harmony | Trend | SCA |
|---------|-------|---------|--------------|---------|-------|-----|
| navier_stokes | affirmative | supports_conjecture | 0.0100 | 0.167 | decreasing | N |
| p_vs_np | gap | supports_gap | 0.8344 | 0.500 | increasing | N |
| riemann | affirmative | inconclusive | 0.1611 | 0.000 | oscillating | N |
| yang_mills | gap | supports_gap | 1.0000 | 0.417 | stable | N |
| bsd | affirmative | inconclusive | 1.3000 | 0.000 | stable | N |
| hodge | affirmative | inconclusive | 0.6156 | 0.500 | oscillating | N |

## Problem Classification
- **Affirmative** (delta->0 supports conjecture): ['navier_stokes', 'riemann', 'bsd', 'hodge']
- **Gap** (delta>=eta supports gap): ['p_vs_np', 'yang_mills']
- **Converging**: ['navier_stokes']
- **Persistent defect**: ['p_vs_np', 'yang_mills', 'bsd', 'hodge']

## Navier Stokes
- Verdict: supports_conjecture
- Decision: smoothness
- Defect: 0.010000 (trend: decreasing)
- Topology: unknown

## P Vs Np
- Verdict: supports_gap
- Decision: smoothness
- Defect: 0.834433 (trend: increasing)
- Topology: unknown

## Riemann
- Verdict: inconclusive
- Decision: smoothness
- Defect: 0.161055 (trend: oscillating)
- Topology: unknown

## Yang Mills
- Verdict: supports_gap
- Decision: smoothness
- Defect: 1.000000 (trend: stable)
- Topology: unknown

## Bsd
- Verdict: inconclusive
- Decision: smoothness
- Defect: 1.300000 (trend: stable)
- Topology: unknown

## Hodge
- Verdict: inconclusive
- Decision: smoothness
- Defect: 0.615567 (trend: oscillating)
- Topology: unknown
