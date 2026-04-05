# SDV Probe Report: Riemann

**Problem class**: affirmative
**Test case**: known_zero
**Seed**: 42
**Levels**: 12
**Hash**: `c31d453147b5e163`

## Dual Lens
- **Lens A**: Euler product (local prime factors)
- **Lens B**: Functional equation (global symmetry)
- **Generator**: Analytic-symmetry flow (functional eq)
- **Dual**: Euler product (prime flow)

## Measurement Verdict
- **Verdict**: inconclusive
- **Decision**: op7=misalignment, op9=collapse -> smoothness
- **Final defect**: 0.000000
- **Final action**: 0.543591
- **Defect trend**: stable (slope=0.000000)
- **Converges**: True
- **Bounded below**: False

## Operator Distribution
  LATTICE    0.167 ######
  PROGRESS   0.083 ###
  COLLAPSE   0.167 ######
  BALANCE    0.083 ###
  CHAOS      0.167 ######
  HARMONY    0.083 ###
  BREATH     0.167 ######
  RESET      0.083 ###
  **Harmony fraction**: 0.083

## 3-6-9 Spine
- Spine fraction: 0.333
- Sheath-3 defect: 0.000000
- Sheath-6 defect: 0.000000
- Anchor-9 defect: 0.000000

## TIG Path
- Expected: VOID -> LATTICE -> COUNTER -> BALANCE -> HARMONY -> BREATH -> RESET
- Actual:   BREATH -> COLLAPSE -> CHAOS -> BREATH -> BALANCE -> LATTICE -> CHAOS -> RESET -> HARMONY -> LATTICE -> PROGRESS -> COLLAPSE
- Fidelity: 0.000

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
- Final: 0.000000
- Dual fixed-point proximity: 1.000000

## Safety
- Anomalies: 0
- Halted: False

## Per-Level Data

| Level | Operator | Defect | Action | Band | D2 Mag | Hash |
|-------|----------|--------|--------|------|--------|------|
| 0 | BREATH | 0.0000 | 0.5270 | YELLOW | 0.4344 | `7e86d1e9` |
| 1 | COLLAPSE | 0.0000 | 0.6067 | YELLOW | 1.7648 | `46d48e53` |
| 2 | CHAOS | 0.0000 | 0.5765 | YELLOW | 1.3057 | `8e1d2a5a` |
| 3 | BREATH | 0.0000 | 0.4931 | YELLOW | 0.3263 | `da8011ab` |
| 4 | BALANCE | 0.0000 | 0.5283 | YELLOW | 0.5001 | `a21f241b` |
| 5 | LATTICE | 0.0000 | 0.5412 | YELLOW | 0.8613 | `d66ce2b8` |
| 6 | CHAOS | 0.0000 | 0.5514 | YELLOW | 1.5022 | `a0789bcb` |
| 7 | RESET | 0.0000 | 0.5396 | YELLOW | 1.2784 | `b04f32e3` |
| 8 | HARMONY | 0.0000 | 0.4235 | YELLOW | 0.1580 | `9bec312c` |
| 9 | LATTICE | 0.0000 | 0.4710 | YELLOW | 0.5697 | `24c1e6a9` |
| 10 | PROGRESS | 0.0000 | 0.4963 | YELLOW | 1.0148 | `1c8e0dc4` |
| 11 | COLLAPSE | 0.0000 | 0.5436 | YELLOW | 2.0000 | `3f45f5fc` |
