# SDV Probe Report: Navier Stokes

**Problem class**: affirmative
**Test case**: high_strain
**Seed**: 42
**Levels**: 8
**Hash**: `7dbd6ee726a49a3d`

## Dual Lens
- **Lens A**: Local vorticity/strain (omega, S, |grad u|^2)
- **Lens B**: Global energy/dissipation (E, epsilon, curvature invariants)
- **Generator**: NSE evolution operator
- **Dual**: Linearized NS (Frechet derivative)

## Measurement Verdict
- **Verdict**: supports_conjecture
- **Decision**: op7=misalignment, op9=stabilization -> smoothness
- **Final defect**: 0.010000
- **Final action**: 0.473501
- **Defect trend**: decreasing (slope=-0.021325)
- **Converges**: True
- **Bounded below**: False

## Operator Distribution
  VOID       0.625 #########################
  BALANCE    0.125 #####
  HARMONY    0.250 ##########
  **Harmony fraction**: 0.250

## 3-6-9 Spine
- Spine fraction: 0.625
- Sheath-3 defect: 0.000000
- Sheath-6 defect: 0.000000
- Anchor-9 defect: 0.046168

## TIG Path
- Expected: VOID -> LATTICE -> COUNTER -> PROGRESS -> HARMONY -> RESET
- Actual:   VOID -> BALANCE -> HARMONY -> HARMONY -> VOID -> VOID -> VOID -> VOID
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
- Final: 0.010000
- Dual fixed-point proximity: 0.634896

## Safety
- Anomalies: 0
- Halted: False

## Per-Level Data

| Level | Operator | Defect | Action | Band | D2 Mag | Hash |
|-------|----------|--------|--------|------|--------|------|
| 0 | VOID | 0.1603 | 0.4371 | YELLOW | 0.0339 | `5f7f8bae` |
| 1 | BALANCE | 0.1179 | 0.5583 | YELLOW | 0.5084 | `d92de8c1` |
| 2 | HARMONY | 0.0772 | 0.5400 | YELLOW | 0.2500 | `03cb05a5` |
| 3 | HARMONY | 0.0552 | 0.4733 | YELLOW | 0.1264 | `4f3fe114` |
| 4 | VOID | 0.0322 | 0.4425 | YELLOW | 0.0625 | `06d68f07` |
| 5 | VOID | 0.0184 | 0.4581 | YELLOW | 0.0326 | `50321c75` |
| 6 | VOID | 0.0100 | 0.4673 | YELLOW | 0.0165 | `ab27bfa5` |
| 7 | VOID | 0.0100 | 0.4735 | YELLOW | 0.0114 | `e3bb115e` |
