# SDV Probe Report: Yang Mills

**Problem class**: gap
**Test case**: bpst_instanton
**Seed**: 42
**Levels**: 12
**Hash**: `0e6e36891474a083`

## Dual Lens
- **Lens A**: Local gauge curvature F_mu_nu, action density
- **Lens B**: Global spectral invariants (mass spectrum)
- **Generator**: Time/gradient flow
- **Dual**: RG coarse-graining

## Measurement Verdict
- **Verdict**: supports_gap
- **Decision**: op7=misalignment, op9=stabilization -> smoothness
- **Final defect**: 0.142294
- **Final action**: 0.562755
- **Defect trend**: oscillating (slope=-0.000154)
- **Converges**: False
- **Bounded below**: True

## Operator Distribution
  VOID       0.750 ##############################
  BALANCE    0.083 ###
  HARMONY    0.083 ###
  BREATH     0.083 ###
  **Harmony fraction**: 0.083

## 3-6-9 Spine
- Spine fraction: 0.750
- Sheath-3 defect: 0.000000
- Sheath-6 defect: 0.000000
- Anchor-9 defect: 0.153410

## TIG Path
- Expected: VOID -> COUNTER -> COLLAPSE -> HARMONY -> BREATH -> RESET
- Actual:   VOID -> BALANCE -> BREATH -> HARMONY -> VOID -> VOID -> VOID -> VOID -> VOID -> VOID -> VOID -> VOID
- Fidelity: 0.167

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
- Final: 0.142294
- Dual fixed-point proximity: 0.389485

## Safety
- Anomalies: 0
- Halted: False

## Per-Level Data

| Level | Operator | Defect | Action | Band | D2 Mag | Hash |
|-------|----------|--------|--------|------|--------|------|
| 0 | VOID | 0.1604 | 0.5699 | YELLOW | 0.0364 | `ae51a47b` |
| 1 | BALANCE | 0.1479 | 0.6952 | YELLOW | 0.5065 | `388ef118` |
| 2 | BREATH | 0.1373 | 0.6570 | YELLOW | 0.3390 | `3da6edc5` |
| 3 | HARMONY | 0.1453 | 0.5993 | YELLOW | 0.0862 | `c8271e46` |
| 4 | VOID | 0.1522 | 0.5386 | YELLOW | 0.0347 | `3dd2fb11` |
| 5 | VOID | 0.1685 | 0.5449 | YELLOW | 0.0279 | `6f9630ee` |
| 6 | VOID | 0.1499 | 0.5563 | YELLOW | 0.0492 | `f0090ddf` |
| 7 | VOID | 0.1469 | 0.5563 | YELLOW | 0.0274 | `65c2dedd` |
| 8 | VOID | 0.1544 | 0.5556 | YELLOW | 0.0113 | `cdd3efb5` |
| 9 | VOID | 0.1588 | 0.5565 | YELLOW | 0.0054 | `eb2fc0bd` |
| 10 | VOID | 0.1472 | 0.5621 | YELLOW | 0.0190 | `4d8db591` |
| 11 | VOID | 0.1423 | 0.5628 | YELLOW | 0.0130 | `c4cfbd48` |
