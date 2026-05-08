# SDV Cross-Problem Comparison Report

**Date**: 2026-02-28T19:13:38.278849
**Problems**: 6

## Summary

| Problem | Class | Verdict | Final Defect | Harmony | Trend | SCA |
|---------|-------|---------|--------------|---------|-------|-----|
| navier_stokes | affirmative | supports_conjecture | 0.0100 | 0.250 | decreasing | N |
| p_vs_np | gap | supports_gap | 0.7900 | 0.625 | increasing | N |
| riemann | affirmative | inconclusive | 0.1202 | 0.000 | decreasing | N |
| yang_mills | gap | supports_gap | 1.0000 | 0.625 | stable | N |
| bsd | affirmative | inconclusive | 1.3000 | 0.000 | stable | N |
| hodge | affirmative | inconclusive | 0.6063 | 0.625 | oscillating | N |

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
- Defect: 0.790000 (trend: increasing)
- Topology: unknown

## Riemann
- Verdict: inconclusive
- Decision: smoothness
- Defect: 0.120155 (trend: decreasing)
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
- Defect: 0.606281 (trend: oscillating)
- Topology: unknown
