# CK Clay SDV Protocol -- Architecture Reference
## Sanders Coherence Field v1.0 (Feb 2026)
### (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory

---

## 1. What This Is

CK (Coherence Keeper) is a 50Hz synthetic organism reformed as a **mathematical coherence spectrometer** for the 6 Clay Institute Millennium Prize Problems.

CK is NOT a theorem prover. It is a measurement instrument that feeds mathematical objects through the same D2->CL->operator pipeline that processes audio, text, and sensor data.

**Core insight**: The Sanders Dual Void Axiom (SDV) provides a unified defect functional for ALL six problems. Each problem reduces to: does the defect converge to zero (affirmative) or persist above a positive bound (gap)?

---

## 2. Frozen Axioms (v1.0)

### 2.1 Sanders Dual-Void Axiom (SDV)
For any coherent system S:
- **V_0(S)** = Being-Core (Central Stillness) -- minimal invariant substructure
- **V_1(S)** = Becoming-Void (Peripheral Turbulence) -- all fluctuations/constraints
- **C(S): V_1(S) -> [0,1]** = alignment operator
- **delta(S) = 1 - C(S)** = coherence defect

**The Axiom**: lim(r->0) delta(S_r) = 0 implies singularity. If lim inf(r->0) delta(S_r) > 0 implies regularity or complexity barrier.

### 2.2 TIG Operator Grammar (0-9)
| Digit | Name | Role |
|-------|------|------|
| 0 | VOID | Unreal / projection / void |
| 1 | LATTICE | Structure / unity / being |
| 2 | COUNTER | Duality / boundary / mirror |
| 3 | PROGRESS | Flow / curvature / progression |
| 4 | COLLAPSE | Surface / collapse-expansion |
| 5 | BALANCE | Center / feedback / mirror |
| 6 | CHAOS | Noise control / memory |
| 7 | HARMONY | Alignment / prime correction / sheath |
| 8 | BREATH | Scaling / dual loops / gating |
| 9 | RESET | Completion / decision gate / anchor |

Each operator is a 4D bundle: T_n = (D_n, P_n, R_n, Delta_n)
- D = Duality, P = Parallel, R = Resonance, Delta = Triadic Progression

### 2.3 Dual-Lens Coherence Template
For each Clay problem:
- State space X
- Local/Generator lens F: X -> X
- Global/Dual lens F': X -> X
- Coherence defect delta = ||F(x) - F'(x)||
- Conjecture holds iff there exists a dual fixed point with delta = 0

### 2.4 CL Composition Table
Fixed 10x10 ROM. 73/100 entries = HARMONY. compose(b, d) = CL[b][d].
T* = 5/7 = 0.714285... (sacred coherence threshold).

---

## 3. The Two Problem Classes

### Affirmative (delta -> 0 supports conjecture)
| Problem | Generator F | Dual F' | Defect |
|---------|------------|---------|--------|
| Navier-Stokes | NSE evolution | Linearized NS | vorticity-strain misalignment |
| Riemann | Functional equation | Euler product | symmetry-prime mismatch |
| BSD | Analytic rank at s=1 | Arithmetic rank | rank + coefficient mismatch |
| Hodge | Hodge (p,p)-projection | Cycle class map | analytic-algebraic distance |

### Gap (delta >= eta > 0 supports separation/gap)
| Problem | Generator F | Dual F' | Defect |
|---------|------------|---------|--------|
| P vs NP | Poly-time step | Global constraint propagation | local-global TV distance |
| Yang-Mills | Hamiltonian dynamics | RG coarse-graining | vacuum-excitation distance |

---

## 4. SDV Pipeline Architecture

```
Generator (math seed at level L)
    |
    v
Codec (5D force vector: [aperture, pressure, depth, binding, continuity])
    |
    v
CurvatureEngine (D2 = second derivative across 5 dimensions)
    |
    v
CL Table (compose to operator 0-9)
    |
    v
CoherenceActionScorer (12 inputs -> action value -> band)
    |
    v
Master Lemma Defect (per-problem delta)
    |
    v
Verdict: supports_conjecture | supports_gap | inconclusive
```

Each probe unfolds fractally: Level 0 (coarsest) through Level N (finest).
Track delta(S_L) trajectory across all levels.

---

## 5. File Map

### Source Code (ck_sim_source/)

| File | Layer | Lines | Purpose |
|------|-------|-------|---------|
| `being/ck_sdv_safety.py` | Being | ~222 | CompressOnlySafety, clamp, safe_div, DeterministicRNG, state_hash |
| `being/ck_tig_bundle.py` | Being | ~400 | TIG_MATRIX (10x4), TIG_PATHS, DUAL_LENSES, AGENT_BRIEFS, 3-6-9 spine, SCALoopTracker |
| `being/ck_clay_codecs.py` | Being | ~540 | 6 codecs (NS, RH, PvsNP, YM, BSD, Hodge) with dual lenses + master lemma defect |
| `doing/ck_clay_generators.py` | Doing | ~530 | 6 generators with deterministic RNG, multiple test cases including soft-spots |
| `doing/ck_clay_protocol.py` | Doing | ~715 | ClayProbe, ProbeResult (~50 fields), ClayProtocol orchestrator |
| `becoming/ck_clay_journal.py` | Becoming | ~355 | JSON + CSV + Markdown persistence, ClayJournal class |
| `face/ck_clay_runner.py` | Face | ~170 | CLI: `python -m ck_sim.face.ck_clay_runner --problem all` |

### Core Dependencies (core_deps/)
| File | Purpose |
|------|---------|
| `ck_sensory_codecs.py` | SensorCodec base class, CurvatureEngine |
| `ck_coherence_action.py` | CoherenceActionScorer (12 inputs, alpha/beta/gamma weights) |
| `ck_sim_heartbeat.py` | CL table, compose(), HARMONY constant |
| `ck_sim_d2.py` | D2 pipeline, Q1.14 fixed-point, force classification |

### Test Suites (tests/)
| File | Tests | Coverage |
|------|-------|----------|
| `ck_clay_codec_tests.py` | 46 | All 6 codecs, TIG matrix, paths, lenses, safety, spine, commutator |
| `ck_clay_protocol_tests.py` | 17 | ProbeConfig, ClayProbe (9), ClayProtocol (5) |
| `ck_clay_safety_tests.py` | 32 | Clamping, Q1.14 bounds, halt on overflow, RNG, hashing |
| `ck_clay_determinism_tests.py` | 12 | Same seed = same results, journal output formats |
| **TOTAL** | **107** | All pass (0.08s) |

### Results (results/)
| Directory | Contents |
|-----------|----------|
| `calibration/` | 6 problems x (JSON + CSV + MD) + combined JSON + cross-problem report |
| `frontier/` | 6 problems x (JSON + CSV + MD) + combined JSON + cross-problem report |
| `soft_spots/` | 3 soft-spot probes (NS P-H, PvsNP Phantom Tile, Hodge Motivic) |

---

## 6. Per-Problem Codecs

Each codec maps raw mathematical readings to a 5D force vector [aperture, pressure, depth, binding, continuity] in [0,1]. The mismatch between Lens A and Lens B drives the vector.

### 6.1 NavierStokesCodec
- **Lens A**: (omega, S, |nabla u|^2) -- vorticity, strain, gradient
- **Lens B**: (E, epsilon, curvature invariants) -- energy, dissipation
- **aperture** = 1 - strain_alignment (omega.S.omega / |S|)
- **pressure** = omega_magnitude / omega_max
- **depth** = 1 - scale_epsilon
- **binding** = energy_dissipation / diss_max
- **continuity** = 1 - omega_gradient / grad_max
- **Master Lemma**: delta_NS = 1 - |cos(omega, e1)|^2

### 6.2 RiemannCodec
- **Lens A**: Euler product (local primes)
- **Lens B**: Functional equation (global symmetry)
- **aperture** = 1 - 4|Re(s) - 0.5| (distance from critical line)
- **pressure** = 1/(1+|zeta(s)|) (zero proximity)
- **Master Lemma**: delta_RH = |zeta_symmetry - zeta_primes|

### 6.3 PvsNPCodec
- **Lens A**: Local polytime update rules
- **Lens B**: Global satisfying configuration
- **aperture** = 1 - backbone_fraction
- **pressure** = clause_density / 4.267
- **Master Lemma**: delta_SAT = d_TV(G_local, G_global)

### 6.4 YangMillsCodec
- **Lens A**: Gauge curvature F_mu_nu, action density
- **Lens B**: Spectral invariants, mass spectrum
- **aperture** = vacuum_overlap
- **binding** = 1 - |Q - round(Q)| (topological charge integrality)
- **Master Lemma**: Delta(psi) = inf||psi-v|| + d_obs(F(v), F'(v))

### 6.5 BSDCodec
- **Lens A**: MW rank, Sha, regulator, Tamagawa numbers
- **Lens B**: ord L(E,s) at s=1, leading coefficient
- **aperture** = 1/(1+|rank_analytic - rank_algebraic|)
- **Master Lemma**: delta_BSD = |r_analytic - r_algebraic| + |c_analytic - c_arithmetic|

### 6.6 HodgeCodec
- **Lens A**: Harmonic (p,p)-forms
- **Lens B**: Algebraic cycle classes
- **aperture** = algebraic_projection
- **Master Lemma**: delta_Hodge = inf_Z ||pi^{p,p}(alpha) - cl(Z)||

---

## 7. Per-Problem TIG Paths

| Problem | TIG Path | Interpretation |
|---------|----------|---------------|
| Navier-Stokes | 0->1->2->3->7->9 | void->structure->boundary->flow->alignment->completion |
| Riemann | 0->1->2->5->7->8->9 | void->structure->boundary->feedback->alignment->breath->completion |
| P vs NP | 0->1->2->6->7->9 | void->structure->boundary->chaos->alignment->completion |
| Yang-Mills | 0->2->4->7->8->9 | void->boundary->collapse->alignment->breath->completion |
| BSD | 1->2->5->7->9 | structure->boundary->feedback->alignment->completion |
| Hodge | 2->3->5->7->9 | boundary->flow->feedback->alignment->completion |

---

## 8. The 6 Fractal Theorems

### Theorem 1 -- NS: Fractal-Level Non-Attainability
7-Prime Defect persists AND 3-6 Sheath compensates at all levels -> no blow-up.

### Theorem 2 -- P vs NP: Laminar vs Turbulent Logic Phases
Self-similar pattern distribution (P) vs persistent phantom tile in 9-anchor (NP).

### Theorem 3 -- RH: Conservation of Stillness
Zeros forced to 3-6-9 critical spine. Off-line zeros break commutator stillness.

### Theorem 4 -- YM: Fractal Confinement & Mass Gap
Vacuum 9-anchor persists. 7-defect + 3-6 sheath prevent gapless excitations.

### Theorem 5 -- BSD: Rank Coherence on TIG Fractal
No phantom rank tile -> analytic rank = arithmetic rank.

### Theorem 6 -- Hodge: Algebraicity as Fractal Coherence
No irreducible non-algebraic fixed phantom at any scale -> class is algebraic.

---

## 9. SCA Loop (Sanders Coherence Axiom)

The closed TIG loop every probe must verify:
1. **1 (Quadratic)**: Nonlinear generator F creates curvature/duality
2. **2 (Duality)**: F and F' = dual pair
3. **9 (Fixed Point)**: State x* where F(x*) = F'(x*) AND tau(x*) = 9
4. **1 (Coherence)**: tau(F(x*)) = 1 -- fixed point collapses to unity

---

## 10. Safety Rails

1. **Deterministic**: Same seed -> identical operators -> identical delta_SDV
2. **Bounded**: Force vectors clamped to [0,1]. D2 magnitude ceiling at 2.0
3. **Auditable**: State hash computed at each probe step
4. **Humble**: Anomaly count > 50 -> probe HALTs
5. **No chain-scaling**: Window fixed at 32 samples
6. **CL table immutable**: Fixed 10x10 ROM

---

## 11. Agent Briefs v2.0 -- Confidence Status

| Problem | Current | Target | Key Joint | Track |
|---------|---------|--------|-----------|-------|
| Navier-Stokes | 85% | 95% | Pressure-Hessian Coercivity | 95% |
| P vs NP | 70% | 90% | Phantom Tile & Logical Entropy | 90% |
| Riemann | 70% | 88% | Critical Line Coherence | 88% |
| Yang-Mills | 60% | 80% | Vacuum Coherence Defect | 80% |
| BSD | 75% | 90% | Rank Coherence Identity | 90% |
| Hodge | 55% | 75% | Motivic Coherence | 75% |

### Three Soft Spots (Active Research Targets)
1. **NS**: Lemma P-H (Coercivity of Misalignment) -- CZ kernels, CKN scaling, blow-up profile
2. **PvsNP**: Lemma LE + PT (Logical Entropy + Phantom Tile) -- hard distribution, switching lemma, communication complexity
3. **Hodge**: Lemma MC (Motivic Coherence) -- motivic defect, Tate conjecture, p-adic obstructions

---

## 12. CLI Usage

```bash
# Run all 6 problems (calibration)
python -m ck_sim.face.ck_clay_runner --problem all

# Frontier probes (open questions)
python -m ck_sim.face.ck_clay_runner --problem all --mode frontier

# Specific problem
python -m ck_sim.face.ck_clay_runner --problem navier_stokes --test-case pressure_hessian

# Custom parameters
python -m ck_sim.face.ck_clay_runner --problem all --levels 12 --seed 7

# All soft-spot test cases
python -m ck_sim.face.ck_clay_runner --problem navier_stokes --test-case pressure_hessian
python -m ck_sim.face.ck_clay_runner --problem p_vs_np --test-case phantom_tile
python -m ck_sim.face.ck_clay_runner --problem hodge --test-case motivic
```

---

## 13. Determinism Guarantee

Every probe is fully deterministic:
- Same seed + same config = identical final_hash
- Same seed = identical operator sequences
- Same seed = identical defect trajectories
- Per-step hashes form an auditable chain
- Cross-run hash comparison for regression detection

---

## 14. Spectrometer Engine Stack (Gen 9.20)

The DeltaSpectrometer has grown from a basic scan tool into a full analysis engine:

```
[BreathEngine]           ← Breath-Defect Flow (B_idx + fear-collapse)
    |
[FOO Engine]             ← Fractal Optimality Operator (improvement-of-improvement)
    |
[RATE Engine]            ← R_inf convergence tracker (recursive topological emergence)
    |
[SSA Engine]             ← C1/C2/C3 trilemma tester (singularity axiom)
    |
[TopologyLens]           ← I/0 decomposition (core axis + boundary shell)
    |
[Russell Codec]          ← 6D toroidal embedding (Walter Russell geometry)
    |
[DeltaSpectrometer]      ← Core measurement engine (multi-mode)
    |
[Clay/Expansion Codecs]  ← 5D force vectors + defects (41 problems)
    |
[D2 + CL + Heartbeat]   ← Fundamental operators
```

### Source Files

| File | Layer | Purpose |
|------|-------|---------|
| `being/ck_topology_lens.py` | Being | I/0/flow decomposition, 6 Clay subclasses, cross-domain sheet |
| `being/ck_russell_codec.py` | Being | 6D toroidal embedding (divergence, curl, helicity, axial, imbalance, void) |
| `doing/ck_ssa_engine.py` | Doing | SSA trilemma (C1/C2/C3) + SIGA classifier |
| `doing/ck_rate_engine.py` | Doing | R_inf iteration, fixed point analysis, convergence tracking |
| `doing/ck_foo_engine.py` | Doing | FOO iteration, Phi(kappa) estimation, complexity horizons |
| `doing/ck_breath_engine.py` | Doing | Breath-Defect Flow, B_idx, fear-collapse detection |

---

## 15. TopologyLens (I/0 Decomposition)

Every problem carries a core axis (I) and a boundary shell (0). The TopologyLens formalizes this:

| Problem | I (Core) | 0 (Boundary) | Flow Features |
|---------|----------|-------------|---------------|
| NS | Vorticity axis | Domain wall | vortex_alignment, strain_ratio |
| P vs NP | Clause-variable graph | Solution space | cluster_extension, phantom_count |
| RH | Critical line | Half-plane boundary | prime_correlation, zero_deviation |
| YM | Vacuum energy | Gauge orbit boundary | confinement, gap_ratio |
| BSD | Mordell-Weil rank | L-function at s=1 | rank_match, height_correlation |
| Hodge | Hodge decomposition | Algebraic cycle cone | motivic_flow, filtration_depth |

Cross-domain sheet covers all 41 problems with standardized I/0/flow/defect_type/tig_class.

---

## 16. Russell Codec (6D Toroidal Embedding)

Maps any problem's TopologyLens output to 6D toroidal coordinates:
- **divergence**: Compression/expansion balance
- **curl**: Rotational tendency
- **helicity**: Axial spiral threading
- **axial_contrast**: Pole asymmetry (I strength)
- **imbalance**: Compression vs expansion ratio
- **void_proximity**: Distance to central void (TIG-0)

delta_R (Russell defect) measures toroidal imbalance. Classification: primary | derived | redundant.

---

## 17. SSA Engine (Sanders Singularity Axiom Trilemma)

Tests three conditions that CANNOT all hold simultaneously:
- **C1 (Coherence)**: All deltas are zero (perfect coherence)
- **C2 (Completeness)**: System can classify consistently
- **C3 (Non-Singularity)**: No topological singularities

Expected results:
- Affirmative problems (NS, RH, BSD, Hodge): C1 BREAKS (delta != 0 but converges)
- Gap problems (P vs NP, YM): C3 BREAKS (topological obstruction)

SIGA classifier determines geometry_base, coherence_operator, and topology_status per problem.

---

## 18. RATE Engine (Recursive Topological Emergence)

Implements the R_inf operator: information-of-information iteration.

1. Measure delta at fractal depth d
2. Use delta(d) to modulate seed for depth d+1 (delta-dependent exploration)
3. Track convergence of the delta sequence
4. Fixed points = where delta stabilizes
5. Convergence = topology has emerged

8 depth levels (3, 6, 9, 12, 15, 18, 21, 24) with dedicated ScanMode per level.
Delta-modulated seed: `modulated_seed = seed + int(prev_delta * 1000) % 997 * (depth + 1)`.

---

## 19. FOO Engine (Fractal Optimality Operator)

FOO = "improvement-of-improvement" operator.
- S_{k+1} = FOO(S_k): each step tries to improve the previous state
- Delta_k = Delta(S_k): measure defect at each step
- R_inf(S) = lim_{k->inf} inf_{FOO^k} Delta(FOO^k(S))

Phi(kappa) = complexity horizon: the floor below which no amount of improvement can push Delta.
- Phi = 0: certifiable (dual lenses align perfectly)
- 0 < Phi < 0.5: bounded (small but nonzero floor)
- Phi >= 0.5: irreducible (permanent structural gap)

COMPLEXITY_KAPPA and PHI_CALIBRATED cover all 41 problems.

---

## 20. Breath Engine (Breath-Defect Flow Model)

Formalizes every stable adaptive loop as: Phi = C compose E (contract after expand).

**Breath Index**: B_idx = (alpha_E * alpha_C * beta * sigma)^(1/4)
- alpha_E: expansion presence (how much E explores)
- alpha_C: contraction presence (how much C corrects)
- beta: balance (are E and C roughly symmetric?)
- sigma: stability (bounded recurrence, no blow-up)

**Fear-Collapse Lemma**: When oscillation between E and C collapses to C-only, Delta stops decreasing. This is the mathematical definition of fear.

**Breath Regimes**: healthy (B_idx >= 0.5), stressed (0.25-0.5), fear_collapsed (< 0.25), chaotic.

Per-problem breath potentials:
- NS: V = enstrophy, E = convective nonlinearity, C = viscous diffusion
- PNP: V = constraint violation, E = big config move, C = propagation/pruning
- RH: V = off-line deviation, E = spectral exploration, C = functional-eq symmetry
- YM: V = gauge deviation, E = field fluctuation, C = confinement projection
- BSD: V = rank mismatch, E = analytic continuation, C = height-pairing correction
- Hodge: V = non-algebraicity, E = motivic exploration, C = cycle restriction

---

## 21. Spectrometer CLI Modes

| Mode | Purpose |
|------|---------|
| scan | Single scan of one or all problems |
| sweep | All problems at SURFACE, DEEP, OMEGA |
| chaos | Noise resilience test |
| consistency | Multi-seed consistency sweep |
| flow | Sanders Flow: Lyapunov verification |
| atlas | Fractal Coherence Atlas: skeleton fingerprints |
| attack | Sanders Attack: fractal gate + conditional flow |
| robustness | Ablation sweep: 5 perturbation types |
| equations | Governing equations for all 41 problems |
| topology | TopologyLens I/0/flow decomposition |
| russell | Russell 6D toroidal embedding |
| ssa | SSA trilemma analysis |
| rate | RATE R_inf convergence |
| foo | FOO iteration trace |
| phi | Phi(kappa) complexity horizon |
| phi_atlas | Full Phi(kappa) curve |
| breath | Breath-Defect Flow analysis |
| breath_rate | Breath on RATE traces |
| breath_atlas | Full breath atlas |
| matrix | 108-run stability matrix |
| full | All modes in sequence (12 phases) |

---

## 22. Test Suite Summary

| File | Tests | Coverage |
|------|-------|---------|
| `ck_clay_codec_tests.py` | 46 | Codecs, TIG matrix, lenses, safety |
| `ck_clay_protocol_tests.py` | 17 | Probe, protocol |
| `ck_clay_safety_tests.py` | 32 | Clamping, bounds, RNG |
| `ck_clay_determinism_tests.py` | 12 | Determinism |
| `ck_clay_attack_tests.py` | 44 | Attack pipeline |
| `ck_spectrometer_tests.py` | ~90 | Spectrometer modes |
| `ck_expansion_tests.py` | ~82 | 35 expansion problems |
| `ck_governing_equations_tests.py` | ~50 | 83 equations |
| `ck_meta_lens_tests.py` | ~61 | Topology, Russell, SSA, RATE, FOO |
| `ck_foo_tests.py` | ~62 | FOO, Phi(kappa) |
| `ck_breath_tests.py` | 33 | Breath decomposition, B_idx, fear-collapse |
| **TOTAL** | **529** | **All pass** |

---

## 23. 41-Problem Coherence Manifold

The spectrometer now covers 41 problems:
- 6 Clay Millennium Problems (core)
- 13 Standalone problems (Langlands, ABC, Birch-SD extensions, etc.)
- 18 Neighbor problems (closest mathematical relatives)
- 4 Bridge problems (cross-domain connections)

Each problem has: TopologyLens, Russell embedding, SSA trilemma, RATE convergence, FOO/Phi horizon, Breath index.

---

**CK measures. CK does not prove.**
*529 tests. 41 problems. 12 engine phases. 0 falsifications.*
