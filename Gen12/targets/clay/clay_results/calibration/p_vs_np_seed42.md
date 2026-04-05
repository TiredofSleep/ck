# SDV Probe Report: P Vs Np

**Problem class**: gap
**Test case**: easy
**Seed**: 42
**Levels**: 12
**Hash**: `f3acaf37c3978709`

## Dual Lens
- **Lens A**: Local polytime update rules (unit propagation)
- **Lens B**: Global satisfying configuration (solution structure)
- **Generator**: Deterministic algorithm step
- **Dual**: Global constraint propagation

## Measurement Verdict
- **Verdict**: supports_gap
- **Decision**: op7=misalignment, op9=stabilization -> smoothness
- **Final defect**: 0.750000
- **Final action**: 0.346262
- **Defect trend**: stable (slope=0.000000)
- **Converges**: False
- **Bounded below**: True

## Operator Distribution
  VOID       0.500 ####################
  HARMONY    0.500 ####################
  **Harmony fraction**: 0.500

## 3-6-9 Spine
- Spine fraction: 0.500
- Sheath-3 defect: 0.000000
- Sheath-6 defect: 0.000000
- Anchor-9 defect: 0.750000

## TIG Path
- Expected: VOID -> LATTICE -> COUNTER -> CHAOS -> HARMONY -> RESET
- Actual:   HARMONY -> HARMONY -> VOID -> HARMONY -> VOID -> VOID -> HARMONY -> HARMONY -> VOID -> VOID -> HARMONY -> VOID
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
- Final: 0.750000
- Dual fixed-point proximity: 0.746882

## Safety
- Anomalies: 0
- Halted: False

## Per-Level Data

| Level | Operator | Defect | Action | Band | D2 Mag | Hash |
|-------|----------|--------|--------|------|--------|------|
| 0 | HARMONY | 0.7500 | 0.5200 | YELLOW | 0.1356 | `97421563` |
| 1 | HARMONY | 0.7500 | 0.3397 | YELLOW | 0.1354 | `a5a9a945` |
| 2 | VOID | 0.7500 | 0.3086 | YELLOW | 0.0067 | `0205da4a` |
| 3 | HARMONY | 0.7500 | 0.3698 | YELLOW | 0.0752 | `db057fc2` |
| 4 | VOID | 0.7500 | 0.3361 | YELLOW | 0.0045 | `f5dbbcb2` |
| 5 | VOID | 0.7500 | 0.3643 | YELLOW | 0.0370 | `ac79026b` |
| 6 | HARMONY | 0.7500 | 0.3978 | YELLOW | 0.1385 | `08eae056` |
| 7 | HARMONY | 0.7500 | 0.3653 | YELLOW | 0.0616 | `f31170d6` |
| 8 | VOID | 0.7500 | 0.3476 | YELLOW | 0.0421 | `cd1a3902` |
| 9 | VOID | 0.7500 | 0.3496 | YELLOW | 0.0122 | `7feb0b28` |
| 10 | HARMONY | 0.7500 | 0.3657 | YELLOW | 0.0638 | `87268e4a` |
| 11 | VOID | 0.7500 | 0.3463 | YELLOW | 0.0262 | `2747f379` |
