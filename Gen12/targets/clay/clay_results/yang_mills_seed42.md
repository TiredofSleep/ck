# SDV Probe Report: Yang Mills

**Problem class**: gap
**Test case**: excited
**Seed**: 42
**Levels**: 8
**Hash**: `640331c4619dd1b4`

## Dual Lens
- **Lens A**: Local gauge curvature F_mu_nu, action density
- **Lens B**: Global spectral invariants (mass spectrum)
- **Generator**: Time/gradient flow
- **Dual**: RG coarse-graining

## Measurement Verdict
- **Verdict**: supports_gap
- **Decision**: op7=alignment, op9=stabilization -> smoothness
- **Final defect**: 1.000000
- **Final action**: 0.310311
- **Defect trend**: stable (slope=0.000000)
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
- Anchor-9 defect: 1.000000

## TIG Path
- Expected: VOID -> COUNTER -> COLLAPSE -> HARMONY -> BREATH -> RESET
- Actual:   HARMONY -> HARMONY -> VOID -> HARMONY -> VOID -> VOID -> HARMONY -> HARMONY
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
- Final: 1.000000
- Dual fixed-point proximity: 0.830812

## Safety
- Anomalies: 0
- Halted: False

## Per-Level Data

| Level | Operator | Defect | Action | Band | D2 Mag | Hash |
|-------|----------|--------|--------|------|--------|------|
| 0 | HARMONY | 1.0000 | 0.3874 | YELLOW | 0.0775 | `1e12ec77` |
| 1 | HARMONY | 1.0000 | 0.2187 | GREEN | 0.0980 | `24882683` |
| 2 | VOID | 1.0000 | 0.2127 | GREEN | 0.0538 | `9be969e2` |
| 3 | HARMONY | 1.0000 | 0.2702 | GREEN | 0.0652 | `8ef1d073` |
| 4 | VOID | 1.0000 | 0.2498 | GREEN | 0.0156 | `f7fe77f5` |
| 5 | VOID | 1.0000 | 0.2898 | GREEN | 0.0563 | `3dd1427b` |
| 6 | HARMONY | 1.0000 | 0.3262 | YELLOW | 0.1196 | `e2caf311` |
| 7 | HARMONY | 1.0000 | 0.3103 | YELLOW | 0.0677 | `fa0abb05` |
