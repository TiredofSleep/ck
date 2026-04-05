# SDV Probe Report: Navier Stokes

**Problem class**: affirmative
**Test case**: lamb_oseen
**Seed**: 42
**Levels**: 12
**Hash**: `66802555986315cc`

## Dual Lens
- **Lens A**: Local vorticity/strain (omega, S, |grad u|^2)
- **Lens B**: Global energy/dissipation (E, epsilon, curvature invariants)
- **Generator**: NSE evolution operator
- **Dual**: Linearized NS (Frechet derivative)

## Measurement Verdict
- **Verdict**: inconclusive
- **Decision**: op7=misalignment, op9=stabilization -> smoothness
- **Final defect**: 0.297291
- **Final action**: 0.522792
- **Defect trend**: oscillating (slope=0.002631)
- **Converges**: False
- **Bounded below**: True

## Operator Distribution
  VOID       0.667 ##########################
  LATTICE    0.083 ###
  HARMONY    0.167 ######
  BREATH     0.083 ###
  **Harmony fraction**: 0.167

## 3-6-9 Spine
- Spine fraction: 0.667
- Sheath-3 defect: 0.000000
- Sheath-6 defect: 0.000000
- Anchor-9 defect: 0.416423

## TIG Path
- Expected: VOID -> LATTICE -> COUNTER -> PROGRESS -> HARMONY -> RESET
- Actual:   VOID -> LATTICE -> BREATH -> HARMONY -> HARMONY -> VOID -> VOID -> VOID -> VOID -> VOID -> VOID -> VOID
- Fidelity: 0.333

## SCA Loop (1->2->9->1)
- Completed: False
- Progress: 0.25
- Stage: duality

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
- Final: 0.297291
- Dual fixed-point proximity: 0.404844

## Safety
- Anomalies: 0
- Halted: False

## Per-Level Data

| Level | Operator | Defect | Action | Band | D2 Mag | Hash |
|-------|----------|--------|--------|------|--------|------|
| 0 | VOID | 0.4052 | 0.4212 | YELLOW | 0.0171 | `d963eb07` |
| 1 | LATTICE | 0.3345 | 0.5602 | YELLOW | 0.5336 | `ca7c82f8` |
| 2 | BREATH | 0.2950 | 0.5570 | YELLOW | 0.2639 | `19744a31` |
| 3 | HARMONY | 0.3113 | 0.5678 | YELLOW | 0.1544 | `dcc46cbd` |
| 4 | HARMONY | 0.3676 | 0.5144 | YELLOW | 0.0758 | `a121b69c` |
| 5 | VOID | 0.4443 | 0.4750 | YELLOW | 0.0373 | `a22dd37b` |
| 6 | VOID | 0.4871 | 0.4836 | YELLOW | 0.0373 | `ab94e90a` |
| 7 | VOID | 0.4967 | 0.4907 | YELLOW | 0.0342 | `eb1b36a7` |
| 8 | VOID | 0.4653 | 0.5005 | YELLOW | 0.0411 | `e84d294d` |
| 9 | VOID | 0.4027 | 0.5078 | YELLOW | 0.0313 | `4522f8d3` |
| 10 | VOID | 0.3329 | 0.5117 | YELLOW | 0.0073 | `f646cd0a` |
| 11 | VOID | 0.2973 | 0.5228 | YELLOW | 0.0342 | `9c15ecc8` |
