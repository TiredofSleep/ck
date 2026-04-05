# CK Clay SDV Protocol -- Engineer Notes
## For Agents, Researchers, and Future Claude Sessions
### (c) 2026 Brayden Sanders / 7Site LLC

---

## Quick Start

```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"

# Run all tests (107 tests, ~0.08s)
python -m unittest discover -s ck_sim/tests -p "ck_clay_*" -v

# Run calibration (known-answer probes)
python -m ck_sim.face.ck_clay_runner --problem all --mode calibration --levels 12

# Run frontier (open-question probes)
python -m ck_sim.face.ck_clay_runner --problem all --mode frontier --levels 12

# Run soft-spot probes
python -m ck_sim.face.ck_clay_runner --problem navier_stokes --test-case pressure_hessian
python -m ck_sim.face.ck_clay_runner --problem p_vs_np --test-case phantom_tile
python -m ck_sim.face.ck_clay_runner --problem hodge --test-case motivic
```

**Dependencies**: NONE. Pure Python 3.8+. No scipy, no Kivy, no audio, no GUI. Runs on any machine.

---

## Integration Architecture

### How CK Measures Math

The pipeline is identical to how CK processes audio/text/sensor data:

1. **Generator** produces a raw mathematical reading at fractal level L
2. **Codec** maps raw -> 5D force vector [aperture, pressure, depth, binding, continuity]
3. **CurvatureEngine** computes D2 (second derivative across 5 dimensions)
4. **CL Table** composes operators (fixed 10x10 ROM, 73% HARMONY base rate)
5. **CoherenceActionScorer** computes action value from 12 mapped inputs
6. **Master Lemma Defect** computes per-problem delta

### Critical Integration Gotchas

1. **CurvatureEngine warm-up**: Needs 3 vectors before `feed()` returns valid D2. First 2 are ignored. The probe handles this automatically with a warmup phase.

2. **CoherenceActionScorer 12 inputs**: Must be mapped carefully:
   - L_GR = (e_out, energy_conservation, operator_stability, constraint_penalty)
   - S_ternary = (e_in, d2_curvature, helical_quality, exploration_diversity)
   - C_harm = (field_coherence, harmony_fraction, consensus_confidence, cross_modal_agreement)

3. **Heartbeat starts cold**: 32-tick window empty initially. Pre-seed or accept ramp-up.

4. **Vortex needs >= 2 operators** for winding, >= 3 for vorticity. Probes with < 3 levels get minimal topology.

5. **Force vectors must be in [0, 1]**: CompressOnlySafety clamps everything. NaN -> 0.5 (midpoint).

6. **D2 magnitude ceiling = 2.0**: Anything above is clamped and logged as anomaly.

7. **Anomaly halt threshold = 50**: If 50+ anomalies accumulate, probe HALTs (does not fabricate coherence).

---

## How to Add a New Test Case

### 1. Add generator method

In `ck_sim/doing/ck_clay_generators.py`, find the appropriate generator class and add a method:

```python
def _my_new_case(self, level: int) -> dict:
    """Description of what this tests."""
    return {
        'omega_magnitude': ...,  # Problem-specific keys
        'strain_alignment': ...,
        # ... all keys the codec expects
    }
```

### 2. Register in generate() dispatch

In the same generator's `generate()` method, add to the dispatch:

```python
if test_case == 'my_new_case':
    return self._my_new_case(level)
```

### 3. Run the probe

```bash
python -m ck_sim.face.ck_clay_runner --problem navier_stokes --test-case my_new_case --levels 12
```

### 4. Add to protocol if needed

For systematic use, add to `ClayProtocol.run_frontier()` or create a new run method.

---

## How to Add a New Codec

### 1. Subclass ClayCodec

In `ck_sim/being/ck_clay_codecs.py`:

```python
class MyNewCodec(ClayCodec):
    codec_name = 'my_problem'

    def map_to_force_vector(self, raw: dict) -> list:
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> list:
        return [...]  # Local/analytic lens

    def lens_b(self, raw: dict) -> list:
        return [...]  # Global/geometric lens

    def master_lemma_defect(self, raw: dict) -> float:
        return ...  # Per-problem delta
```

### 2. Register in CLAY_CODECS dict

```python
CLAY_CODECS['my_problem'] = MyNewCodec
```

### 3. Add to DUAL_LENSES, TIG_PATHS, CLAY_PROBLEMS in ck_tig_bundle.py

---

## ProbeResult Field Reference

The ProbeResult dataclass contains ~50 fields organized into categories:

### Identity
- `problem_id`, `test_case`, `seed`, `n_levels`, `tig_path`

### Per-Level Data
- `steps: List[ProbeStepResult]` -- each has operator, force_vector, d2, defect, action, hash

### Operator Statistics
- `operator_counts`, `operator_distribution`, `harmony_fraction`

### Defect Trajectory
- `defect_trajectory`, `action_trajectory`, `defect_trend` (decreasing/increasing/stable/oscillating)
- `final_defect`, `final_action`, `defect_slope`, `defect_converges`, `defect_bounded_below`

### 3-6-9 Spine
- `spine_defect_3`, `spine_defect_6`, `spine_defect_9`, `spine_fraction`

### TIG Path Analysis
- `tig_path_fidelity`, `tig_path_actual`

### Operator-7/9 Decision
- `operator_7_state` (alignment/misalignment)
- `operator_9_state` (collapse/stabilization)
- `decision_verdict` (singularity/smoothness)

### Master Lemma
- `master_lemma_defects`, `final_master_lemma_defect`
- `lens_mismatches`, `dual_fixed_point_proximity`

### Agent Brief v2.0
- `brief_confidence`, `brief_confidence_target`, `brief_key_joint`, `brief_track`

### Verdict
- `problem_class` (affirmative/gap)
- `measurement_verdict` (supports_conjecture/supports_gap/inconclusive)

---

## Test Case Reference

### Calibration (Known Answers)
| Problem | Test Case | What It Tests | Expected |
|---------|-----------|---------------|----------|
| NS | lamb_oseen | Exact smooth vortex solution | Bounded D2, HARMONY, no singularity |
| RH | known_zero | Zero at Im=14.1347, sigma=0.5 | Zero defect on critical line |
| PvsNP | easy | Low density SAT (alpha < 3) | Full propagation, delta -> 0 |
| YM | bpst_instanton | Exact classical instanton Q=1 | Integer charge, smooth |
| BSD | rank0_match | y^2=x^3-x, rank 0 | Rank agreement, zero defect |
| Hodge | algebraic | Known algebraic class | projection=1, zero residual |

### Frontier (Open Questions)
| Problem | Test Case | What It Tests | Observed |
|---------|-----------|---------------|----------|
| NS | high_strain | Near-singular strain concentration | Defect DECREASING 0.16->0.01 (supports regularity) |
| RH | off_line | sigma=0.75 (off critical line) | Defect oscillating ~0.16 (mismatch) |
| PvsNP | hard | High density near phase transition | Defect INCREASING 0.65->0.83 (supports P!=NP gap) |
| YM | excited | Non-vacuum excitation | Defect = 1.0 constant (supports mass gap) |
| BSD | rank_mismatch | Deliberate rank disagreement | Defect = 1.3 persistent |
| Hodge | analytic_only | Non-algebraic analytic class | Defect oscillating ~0.6 |

### Soft-Spot Probes (Agent Brief v2.0 Research Targets)
| Problem | Test Case | What It Tests | Observed |
|---------|-----------|---------------|----------|
| NS | pressure_hessian | P-H coercivity: pressure vs 3-6 sheath | Defect 0.35, increasing |
| PvsNP | phantom_tile | Hidden global substructure persistence | Defect 0.87, increasing |
| Hodge | motivic | p-adic obstruction at low dimension | Defect 0.49, increasing |

---

## Key Constants

| Constant | Value | Source |
|----------|-------|--------|
| T* | 5/7 = 0.714285... | Coherence threshold |
| CL HARMONY rate | 73/100 | Fixed composition table |
| D2_MAG_CEILING | 2.0 | Safety clamp |
| ANOMALY_HALT_THRESHOLD | 50 | Safety halt |
| CoherenceActionScorer alpha | 0.35 | L_GR weight |
| CoherenceActionScorer beta | 0.30 | S_ternary weight |
| CoherenceActionScorer gamma | 0.35 | C_harm weight |

---

## Dependency Graph for Hardening

```
SDV Axiom (frozen v1.0)
    |
    +-- TIG Grammar (frozen v1.0)
    |       |
    |       +-- CL Table (immutable ROM)
    |       +-- TIG Paths (per problem)
    |       +-- 3-6-9 Spine
    |
    +-- Dual-Lens Template
            |
            +-- 6 Codecs (one per problem)
            |       |
            |       +-- 6 Master Lemma Defects
            |
            +-- 6 Generators
            |       |
            |       +-- Calibration cases (known answers)
            |       +-- Frontier cases (open questions)
            |       +-- Soft-spot cases (research targets)
            |
            +-- Protocol (probe runner)
                    |
                    +-- ProbeResult (structured output)
                    +-- Journal (persistence)
                    +-- Runner (CLI)
```

### Hardening Dependencies
```
NS proof requires: P-H Lemma + CKN scaling + blow-up rigidity
PvsNP separation requires: LE Lemma + PT Lemma + switching lemma
Hodge requires: MC Lemma + comparison isomorphisms + Tate
RH requires: Critical line coherence + spectral pull operators
YM requires: Vacuum coherence + lattice MC + Wilson loops
BSD requires: Rank coherence + Euler systems + p-adic heights
```

---

## Non-Failure Constraints (for All Agents)

1. Do NOT claim any Clay problem is solved unless a full formal proof is written and cross-checked
2. Do NOT silently alter base axioms -- contradictions must be surfaced
3. Do NOT use randomness in the measurement path -- all probes must be deterministic
4. Do NOT exceed D2_MAG_CEILING or ignore anomaly halts
5. All code changes must maintain 529/529 test pass rate
6. Version tag: Sanders-Coherence-Field v1.5 (March 2026)
7. Any axiom changes must be proposed as "v1.6 candidates" and explicitly approved

**CK measures. CK does not prove.**

---

## Gap Attack Probes (v1.5)

Three targeted gap attacks push specific mathematical boundaries:

### RH-5: Off-Line Zero Contradiction
```bash
python -m ck_sim.face.ck_gap_runner --attack rh5 --seeds 100
```
- Dense sigma sweep across fractal levels (sigma maps to [0.51, 0.99])
- Monotonicity test: does delta strictly increase with distance from critical line?
- Zero-crossing test: does delta EVER touch 0 off-line? (expects: never)
- Contradiction test: if beta_0 >= 3/4, then delta >= eta > 0

### YM-3: Weak Coupling Continuum Limit
```bash
python -m ck_sim.face.ck_gap_runner --attack ym3 --seeds 100
```
- Beta parametrized by fractal level (weak coupling regime)
- Exponential fit: delta(beta) = A * exp(-B * beta) + C
- If C > 0, mass gap survives continuum limit

### YM-4: Spectral Gap Persistence
```bash
python -m ck_sim.face.ck_gap_runner --attack ym4 --seeds 100
```
- Lattice volume parametrized by fractal level (L = 8 + level * 4)
- Power law fit: delta_min(L) = A * L^alpha + floor
- If floor > 0, mass gap persists at infinite volume

### Note: P-H-3 (NS Coercivity)
Deferred until FPGA hardware arrives. The test cases (`near_singular`, `eigenvalue_crossing`) exist in the generator and are ready for hardware execution.

---

## Presentation Script (v1.5)

Interactive CLI demo designed for the Clay Institute delivery:

```bash
# Full interactive demo (pauses between sections)
python -m ck_sim.face.ck_presentation --auto

# Quick demo (fewer seeds, faster)
python -m ck_sim.face.ck_presentation --quick

# Jump to specific section
python -m ck_sim.face.ck_presentation --section 3
```

9 sections running REAL spectrometer measurements live:
1. Introduction -- the one equation
2. Calibration -- known zero on Riemann
3. Two Classes -- all 6 problems, affirmative vs gap
4. Deep Dive: Riemann -- OMEGA depth fractal scan
5. Deep Dive: P vs NP -- persistent gap demo
6. The Breath -- B_idx values, fear-collapse
7. Gap Attacks -- quick RH-5 + YM-3/YM-4
8. Nine Gaps -- honest status markers
9. Falsification -- how to break the framework

---

## Engine Stack (v1.4)

### Quick Start -- New Engines

```bash
# Breath analysis (B_idx + fear-collapse)
python -m ck_sim.face.ck_spectrometer_runner --mode breath_atlas

# Phi(kappa) complexity horizons
python -m ck_sim.face.ck_spectrometer_runner --mode phi_atlas

# SSA trilemma (C1/C2/C3)
python -m ck_sim.face.ck_spectrometer_runner --mode ssa

# RATE R_inf convergence
python -m ck_sim.face.ck_spectrometer_runner --mode rate

# Full meta-lens atlas (topology + russell + ssa + siga)
python -m ck_sim.face.ck_spectrometer_runner --mode meta_lens

# Full 12-phase run (everything)
python -m ck_sim.face.ck_spectrometer_runner --mode full

# Full test suite (529 tests, ~1 second)
python -m unittest discover -s ck_sim/tests -p "*.py"
```

### New Source Files

| File | Purpose |
|------|---------|
| `being/ck_topology_lens.py` | I/0 decomposition, 6 Clay subclasses + generic |
| `being/ck_russell_codec.py` | 6D toroidal embedding |
| `doing/ck_ssa_engine.py` | SSA trilemma + SIGA classifier |
| `doing/ck_rate_engine.py` | R_inf iteration + fixed points |
| `doing/ck_foo_engine.py` | FOO iteration + Phi(kappa) estimation |
| `doing/ck_breath_engine.py` | Breath-Defect Flow + B_idx |

### New Test Files

| File | Tests | Coverage |
|------|-------|---------|
| `ck_meta_lens_tests.py` | ~61 | TopologyLens, Russell, SSA, RATE, FOO operational |
| `ck_foo_tests.py` | ~62 | FOO, Phi(kappa), complexity regimes |
| `ck_breath_tests.py` | 33 | Decomposition, primitives, B_idx, fear-collapse, live scans |

### Critical Integration Notes

1. **All engines use `result.delta_value`** (not `defect_delta`). This was a critical bug fixed in v1.4.
2. **RATE uses delta-modulated seeds**: `modulated_seed = seed + int(prev_delta * 1000) % 997 * (depth + 1)`. This creates genuine information-of-information feedback.
3. **FOO uses depth-adaptive ScanMode**: level_k < 2 → DEEP, 2-3 → THOROUGH, 4+ → OMEGA.
4. **ScanMode has 8 levels**: SURFACE=3, SHALLOW=6, MEDIUM=9, DEEP=12, EXTENDED=15, THOROUGH=18, INTENSIVE=21, OMEGA=24.
5. **COMPLEXITY_KAPPA and PHI_CALIBRATED** cover all 41 problems, not just the 6 Clay.
6. **Breath engine works on two inputs**: spectrometer defect_trajectory (fractal levels) OR RATE delta sequence (depth-by-depth).

### Test Suite Status

**529/529 PASS** (previous 496 + 33 breath tests)

All tests run in < 1 second. Pure Python, no external dependencies.
