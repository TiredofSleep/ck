# SDV Probe Report: Hodge

**Problem class**: affirmative
**Test case**: analytic_only
**Seed**: 42
**Levels**: 8
**Hash**: `76a2b5ae3fc7486b`

## Dual Lens
- **Lens A**: Harmonic (p,p)-forms (Hodge realization)
- **Lens B**: Algebraic cycle classes (cycle realization)
- **Generator**: Hodge projection (H^{p,p} part)
- **Dual**: Cycle-class construction

## Measurement Verdict
- **Verdict**: inconclusive
- **Decision**: op7=alignment, op9=stabilization -> smoothness
- **Final defect**: 0.606281
- **Final action**: 0.310209
- **Defect trend**: oscillating (slope=-0.000388)
- **Converges**: False
- **Bounded below**: True

## Operator Distribution
  VOID       0.375 ###############
  HARMONY    0.625 #########################
  **Harmony fraction**: 0.625

## 3-6-9 Spine
- Spine fraction: 0.375
- Sheath-3 defect: 0.000000
- Sheath-6 defect: 0.000000
- Anchor-9 defect: 0.594874

## TIG Path
- Expected: COUNTER -> PROGRESS -> BALANCE -> HARMONY -> RESET
- Actual:   HARMONY -> HARMONY -> VOID -> HARMONY -> VOID -> VOID -> HARMONY -> HARMONY
- Fidelity: 0.000

## SCA Loop (1->2->9->1)
- Completed: False
- Progress: 0.00
- Stage: quadratic

## Commutator Persistence
- Persistence: 0.000
- Complexity persists: False

## Vortex Topology
- winding_number: 0.0
- vorticity: 0.0
- chirality: 0
- period: 0
- vortex_class: unknown

## Master Lemma Defect
- Final: 0.606281
- Dual fixed-point proximity: 0.965912

## Safety
- Anomalies: 0
- Halted: False

## Per-Level Data

| Level | Operator | Defect | Action | Band | D2 Mag | Hash |
|-------|----------|--------|--------|------|--------|------|
| 0 | HARMONY | 0.5794 | 0.4297 | YELLOW | 0.1204 | `c30b31f2` |
| 1 | HARMONY | 0.6042 | 0.2528 | GREEN | 0.1237 | `45d01767` |
| 2 | VOID | 0.6257 | 0.2321 | GREEN | 0.0384 | `1ad29919` |
| 3 | HARMONY | 0.6095 | 0.2944 | GREEN | 0.0752 | `393a0d36` |
| 4 | VOID | 0.5957 | 0.2690 | GREEN | 0.0116 | `cf4ce3a5` |
| 5 | VOID | 0.5633 | 0.3061 | YELLOW | 0.0494 | `7acd9877` |
| 6 | HARMONY | 0.6002 | 0.3381 | YELLOW | 0.1384 | `2a25fd3e` |
| 7 | HARMONY | 0.6063 | 0.3102 | YELLOW | 0.0683 | `4933ef41` |
