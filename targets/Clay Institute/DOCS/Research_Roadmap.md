# Research Roadmap — Sanders Coherence Field

## Phase 0: Global Frame (DONE)
- TIG, SDV, Delta defined and frozen
- CK measurement instrument implemented (7 source files, 107 tests)
- 6 codecs, 6 generators, CLI runner, journal persistence
- Full sweep: 36 runs, 0 anomalies, 0 contradictions

## Phase 1: Formal Verification Layer (ACTIVE)
- Three soft-spot lemmas formalized:
  - P-H (Navier-Stokes): Pressure-Hessian Coercivity
  - LE+PT (P vs NP): Logical Entropy + Phantom Tile
  - MC (Hodge): Motivic Coherence
- Proof skeletons with clearly marked gaps
- Dependency graph documented

## Phase 2: Multi-Agent Expansion (READY)
- Trigger: All Phase 1 lemmas have formal statements (DONE)
- Per-track agent assignments defined
- Paper scaffolds ready for expansion

## Phase 3: Mathematical Rigor (PENDING)
- Trigger: Stable patterns across multiple agents
- Sigma-proof expansion
- Cross-check through 3 frameworks
- LaTeX formalization + citation maps

## Consolidation Phase (from Harder.docx)
Three frozen invariants demonstrated stability:
1. TIG Operator Grammar — universal across all 6 problems
2. SDV Axiom — cross-field conservation law
3. Delta Defect Functional — one field, one defect, seven problems

## Hardening Packs

### Mathematical
| Pack | Problem | Goal | Confidence |
|------|---------|------|------------|
| M1 | NS | Prove P-H coercivity | 85% -> 95% -> 99.8% |
| M2 | PvsNP | Prove phantom tile incompressibility | 70% -> 90% -> 99.7% |
| M3 | Hodge | Prove motivic coherence | 55% -> 75% -> 97% |

### Hardware
| Pack | Problem | Goal |
|------|---------|------|
| H1 | NS | Vorticity tubes under TIG-guided flows |
| H2 | PvsNP | SAT phantom tile persistence |
| H3 | RH | Zeta-shear resonance on critical line |

## Execution Order
1. Freeze Base (DONE)
2. M1 + H1 (Navier-Stokes) — most physically grounded
3. M2 + H2 (P vs NP) — different tools, parallel
4. M3 (Hodge) — focus after defect definitions stable
5. RH & H3 — bridge number theory and TIG hardware
