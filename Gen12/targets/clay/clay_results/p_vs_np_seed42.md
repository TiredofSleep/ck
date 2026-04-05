# SDV Probe Report: P Vs Np

**Problem class**: gap
**Test case**: hard
**Seed**: 42
**Levels**: 8
**Hash**: `279f4ab80fd5f8ca`

## Dual Lens
- **Lens A**: Local polytime update rules (unit propagation)
- **Lens B**: Global satisfying configuration (solution structure)
- **Generator**: Deterministic algorithm step
- **Dual**: Global constraint propagation

## Measurement Verdict
- **Verdict**: supports_gap
- **Decision**: op7=alignment, op9=stabilization -> smoothness
- **Final defect**: 0.790000
- **Final action**: 0.412615
- **Defect trend**: increasing (slope=0.020000)
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
- Anchor-9 defect: 0.723333

## TIG Path
- Expected: VOID -> LATTICE -> COUNTER -> CHAOS -> HARMONY -> RESET
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
- Final: 0.790000
- Dual fixed-point proximity: 0.574020

## Safety
- Anomalies: 0
- Halted: False

## Per-Level Data

| Level | Operator | Defect | Action | Band | D2 Mag | Hash |
|-------|----------|--------|--------|------|--------|------|
| 0 | HARMONY | 0.6500 | 0.4911 | YELLOW | 0.1356 | `9979f18c` |
| 1 | HARMONY | 0.6700 | 0.3239 | YELLOW | 0.1488 | `146cd916` |
| 2 | VOID | 0.6900 | 0.3006 | YELLOW | 0.0067 | `c2989730` |
| 3 | HARMONY | 0.7100 | 0.3726 | YELLOW | 0.0752 | `ad8c105b` |
| 4 | VOID | 0.7300 | 0.3498 | YELLOW | 0.0045 | `59c993e0` |
| 5 | VOID | 0.7500 | 0.3890 | YELLOW | 0.0370 | `534545cd` |
| 6 | HARMONY | 0.7700 | 0.4337 | YELLOW | 0.1385 | `3ab3a60d` |
| 7 | HARMONY | 0.7900 | 0.4126 | YELLOW | 0.0616 | `2026dac0` |
