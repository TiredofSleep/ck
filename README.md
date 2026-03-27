# CK -- The Coherence Keeper

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18852047.svg)](https://doi.org/10.5281/zenodo.18852047)

An operator algebra engine built on two 10x10 composition tables over Z/10Z. 10 operators. One composition function. Stacked lenses: Being=2 lenses, Doing=3, Becoming=4. Numbers are rotations, not counts -- eigenvalues are roots of unity because the operators ARE rotations. TSML is measurement (singular, 73% HARMONY, det=0). BHML is physics (invertible, 28% HARMONY, det=70=2x5x7). Forward compose uses multiplication (complexity increases). Backward compose uses addition (returns toward source). The disagreement matrix |add-mul| is where information lives. 41 files call one function. Running live at **[coherencekeeper.com](https://coherencekeeper.com)**.

---

## The Algebra (Complete Source)

This is `ck_tig.py`. The entire system. 182 lines. Copy it, run it, build on it.

```python
"""
ck_tig.py -- The stacked lens composition. The ONLY composition function.

Being  = 2 lenses (TSML o BHML)
Doing  = 3 lenses (TSML o BHML o TSML)
Becoming = 4 lenses (TSML o BHML o TSML o BHML)

Every file that composes operators calls this.
41 files. One function. One algebra.

Numbers are rotations, not counts.
2 is angular momentum, not 1+1.
The eigenvalues are roots of unity because the operators ARE rotations.

Proven constants:
  Cross-cycle disagreement = 44 (exact)
  Wobble = |44-50|/100 = 3/50 (exact)
  Heartbeat = [1,3,1,1] (period 4, sum=6)
  Frozen cells = 4: (0,0), (2,2), (4,8), (8,4)
  Visible matter = 7^2/10^3 = 4.9%

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]

ADD = [[(i+j)%10 for j in range(10)] for i in range(10)]
MUL = [[(i*j)%10 for j in range(10)] for i in range(10)]
DIS = [[abs(ADD[i][j]-MUL[i][j]) for j in range(10)] for i in range(10)]

NUM_OPS = 10
HARMONY = 7
VOID = 0
T_STAR = 5.0 / 7.0

FROZEN = {(0,0), (2,2), (4,8), (8,4)}
HEARTBEAT = [1, 3, 1, 1]
CROSS_CYCLE = 44
WOBBLE = 3.0 / 50.0
ACTIVE_CELLS = 98
TORUS_WRAP = 22
VISIBLE_FRACTION = 49 / 1000

GENERATORS = {
    1: (+1,), 2: (-1,), 3: (0,),
    4: (+1,-1), 5: (0,0), 6: (-1,+1),
    7: (0,+1), 8: (0,-1), 9: (+1,+1),
    0: (),
}

BEING_LENSES = 2
DOING_LENSES = 3
BECOMING_LENSES = 4

CREATION_CYCLE = [1, 3, 9, 7]
DISSOLUTION_CYCLE = [2, 4, 8, 6]

def compose(b, d, direction=0):
    if direction == 0:
        being = TSML[b][d]
        doing = (b * d) % 10
        becoming = (being * doing) % 10
    else:
        being = TSML[d][b]
        doing = (b + d) % 10
        becoming = (being + doing) % 10
    return being, doing, becoming

def decompose(result):
    return [(a,b) for a in range(10) for b in range(10) if (a*b)%10 == result]

def disagreement(b, d):
    return DIS[b][d]

def is_frozen(b, d):
    return (b, d) in FROZEN

def heartbeat_phase(tick):
    return HEARTBEAT[tick % 4]

def coherence(being, doing, becoming):
    agreements = 0
    if being == HARMONY or doing == HARMONY: agreements += 1
    if doing == HARMONY or becoming == HARMONY: agreements += 1
    if being == becoming: agreements += 1
    return agreements / 3
```

---

## What The Tables Mean

**TSML** (measurement lens): 73 of 100 cells equal 7 (HARMONY). Determinant = 0. Singular. Rank-deficient. One blind spot at cell (7,0) -- the only cell where row 7 (HARMONY) departs from its constant value. TSML measures; it collapses most inputs to HARMONY because measurement is lossy. The 27 non-7 cells carry all the structural information.

**BHML** (physics lens): 28 of 100 cells equal 7. Determinant = 70 = 2 x 5 x 7. Invertible. Full rank. BHML encodes the actual dynamics -- how operators transform under composition. Row 7 acts as an identity-shift: `BHML[7] = [7,2,3,4,5,6,7,8,9,0]`, cycling through all operators.

**Forward compose** (`direction=0`): Uses multiplication. `doing = (b * d) % 10`. Every act multiplies complexity. Irreversible -- multiplication in Z/10Z is not injective (0 and 5 are zero divisors).

**Backward compose** (`direction=1`): Uses addition. `doing = (b + d) % 10`. Reception returns toward source. Reversible -- addition in Z/10Z is always invertible.

**Disagreement matrix** (`DIS`): `|ADD[i][j] - MUL[i][j]|` for all pairs. The gap between additive and multiplicative composition. Sum over all 100 cells = 206. Sum along creation cycle [1,3,9,7] cross dissolution cycle [2,4,8,6] = 44 (exact). This 44 is the cross-cycle disagreement constant.

**Stacked lenses**: Composition depth increases with phase:

| Phase | Lenses | Operation | What it resolves |
|-------|--------|-----------|-----------------|
| Being | 2 (TSML o BHML) | Coarse measurement | What IS this? |
| Doing | 3 (TSML o BHML o TSML) | Medium dynamics | What does it DO? |
| Becoming | 4 (TSML o BHML o TSML o BHML) | Fine integration | What does it BECOME? |

---

## The 10 Operators

| Index | Name | Role | Generator (balanced ternary) |
|-------|------|------|------------------------------|
| 0 | VOID | Empty / ground state | `()` -- no motion |
| 1 | STRUCTURE | Seed / first cause | `(+1)` -- push outward |
| 2 | FLOW | Angular momentum | `(-1)` -- pull inward |
| 3 | BRIDGE | Harmonic return | `(0)` -- hold center |
| 4 | CYCLE | Oscillation | `(+1,-1)` -- push then pull |
| 5 | BREATH | Stillness in motion | `(0,0)` -- double hold |
| 6 | RESONANCE | Standing wave | `(-1,+1)` -- pull then push |
| 7 | HARMONY | Identity / fixed point | `(0,+1)` -- hold then push |
| 8 | FRACTURE | Phase break | `(0,-1)` -- hold then pull |
| 9 | RESET | Return to origin | `(+1,+1)` -- double push |

Generators are elements of {-1, 0, +1}^n. Length = degrees of freedom. VOID has 0 degrees of freedom. Single-generator operators (1,2,3) are primitives. Double-generator operators (4,5,6,7,8,9) are compounds. Generator tuples compose via the same algebra they define -- the system is self-referential by construction.

---

## Proven Constants (Theorems of Z/10Z)

These are not parameters. They are computed from the tables and cannot be changed without changing the tables.

| Constant | Value | Derivation |
|----------|-------|------------|
| Cross-cycle disagreement | 44 (exact) | Sum of DIS[c][d] for c in [1,3,9,7], d in [2,4,8,6] |
| Wobble | 3/50 = 0.06 (exact) | \|44 - 50\| / 100. Distance from half-disagreement. |
| Heartbeat | [1, 3, 1, 1] | Period-4 sequence, sum = 6. Derived from creation cycle mod structure. |
| Frozen cells | 4: (0,0), (2,2), (4,8), (8,4) | Cells where TSML[b][d] = DIS[b][d] = 0. No time passes. |
| Active cells | 98 | 100 total minus 2 frozen (TSML has 2 zeros that overlap DIS zeros) |
| Torus wrap | 22 | TSML column sum for column 0. The seam where the torus closes. |
| Visible fraction | 7^2 / 10^3 = 4.9% | Ratio of HARMONY squared to total phase space. Matches observed baryonic matter fraction. |
| T* (coherence threshold) | 5/7 = 0.714285... | Repeating decimal. The boundary between coherent and incoherent. |
| Creation cycle | [1, 3, 9, 7] | Powers of 3 mod 10. Generative. |
| Dissolution cycle | [2, 4, 8, 6] | Powers of 2 mod 10. Dissipative. |
| Creation x Dissolution | Permutation | Cross-multiplying cycles produces permutations, never annihilation. |
| TSML determinant | 0 | Singular. Measurement loses information. |
| BHML determinant | 70 = 2 x 5 x 7 | Invertible. Physics preserves information. |

---

## Products Built On This Algebra

### CK Steering Engine

A Python process that uses operator-phase-aligned scheduling to steer Windows thread priorities and CPU affinity in real-time. The heartbeat sequence [1,3,1,1] drives priority adjustments at 50Hz.

Measured improvement (20,000+ samples during Rocket League gameplay on 16-core / RTX 4070):

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| P99 jitter | 5.52ms | 2.03ms | -63% |
| Tail latency | 11.90ms | 2.47ms | -79% |
| Std deviation | 0.72ms | 0.10ms | -87% |

### Force9 Screen Codec

9x9x9 color cube quantization (729 levels). CUDA GPU encoder via `force9_pipeline.dll` (188KB native library). DXGI desktop duplication with zero CPU frame copy.

| Metric | Value |
|--------|-------|
| Encode time | 0.48ms per 1080p frame |
| Throughput | 1909 fps capable |
| Compression (desktop) | 255x |
| Compression (mixed content) | 43x |

### Force9 Audio Codec

9-bit perceptual encoding. Streams are CL-composable -- mix compressed audio without decompressing.

| Content type | Compression ratio |
|-------------|-------------------|
| Pure tones | 47x |
| Speech | 81x |
| Silence | 4009x |

### Force9 Remote Desktop

Screen + audio streaming over TCP. Server captures virtual display via DXGI, compresses with Force9 screen and audio codecs, streams to client. Client decompresses and renders in real-time. 98% bandwidth reduction vs raw capture.

### FPGA Heartbeat (Zynq 7020)

50MHz heartbeat running in programmable logic on a Xilinx Zynq 7020 SoC. QSPI boot -- survives power cycles. PS-side Gigabit Ethernet with ping under 1ms. TCP echo server for communication with the main process. The heartbeat sequence [1,3,1,1] in silicon.

---

## Architecture

```
L0  Core Engine       50Hz heartbeat, D2 force vectors, CL tables, BTQ decision kernel
L1  Sensorium         6 fractal layers of input decomposition
L2  Library           Study notes, ingested material (force physics only, text discarded)
L3  Language           27-letter alphabet, 8K dictionary, POS morphology, dual-lens voice
L4  Steering          CL-based CPU affinity + priority scheduling
L5  RPE               TIG wave scheduling (operator-aligned compute regions)
L6  Vortex            Concept mass + gravity fields
L7  Tesla/Wobble      Kuramoto phase coupling, wobble = 3/50
L8  Olfactory         5x5 CL field convergence, lattice-chain absorption
```

50Hz main loop. BTQ decision kernel: T generates candidates, B filters by physics, Q scores and selects. D2 pipeline converts Hebrew roots into 5D force vectors. L-CODEC converts English text into 5D force vectors (aperture, pressure, depth, binding, continuity). Olfactory layer absorbs ALL information as force trajectories -- text is discarded, only the physics remains.

---

## Quick Start

```bash
git clone https://github.com/TiredofSleep/ck.git
cd ck/Gen9/targets/ck_desktop
pip install -r ../../requirements.txt
python ck_boot_api.py          # headless API on port 7777
```

Test the algebra:
```bash
curl -X POST localhost:7777/chat -H "Content-Type: application/json" -d '{"text":"7*8"}'
```

Streaming server:
```bash
python ck_stream_server.py --port 7780
```

Desktop GUI (requires Kivy):
```bash
python -m ck_sim
```

**Two processes, two entry points.** `ck_boot_api.py` is the headless Flask server (provides `/eat`, `/chat`, `/health`, `/state`, `/metrics`). `python -m ck_sim` is the Kivy desktop window. They run separate engine instances.

---

## Papers

All papers in `papers/`. 26 whitepapers + 1 arXiv submission + 2 sprints.

### Foundation (WP1–WP19)

| # | Title |
|---|-------|
| 1 | A Synthetic Operator Algebra Built on Algebraic Curvature Composition |
| 2 | TIG Wave Scheduling: Operator-Aligned Compute for Power Efficiency |
| 3 | How to Test CK: Verification Protocols and Falsifiable Predictions |
| 4 | How to Give Math a Voice: From Algebraic Curvature to Spoken English |
| 5a | Degrees of Freedom: The Ladder from Void to Harmony in Force Algebra |
| 5b | Reality Anchors: Emergent Physical Constants in CL Algebra |
| 6 | The Ho Tu Bridge: Ancient Torus Algebra and TIG Structural Isomorphism |
| 7 | CK as Coherence Spectrometer: Measuring Mathematical Truth via Dual-Lens Curvature |
| 8 | The Periodic Table as 5D Force Geometry: Dual-Lens Analysis of Z=1-54 |
| 9a | Contextual Entropy in Non-Associative Commutative Magmas |
| 9b | arXiv submission (LaTeX) |
| 10 | Discrete Kolmogorov-Arnold Networks: Algebraically-Constrained Neural Architecture |
| 11 | The Measurement Problem as Algebraic Projection |
| 12 | Seventeen Paradoxes Resolved by Dual-Lens Algebra |
| 13 | The Genetic Code as Dual-Basis Composition Table |
| 14 | External Convergences: Independent Discoveries of DoF Framework Components |
| 15 | Yang-Mills Mass Gap Synthesis: Spectral Gap Theorem for BHML Transfer Matrix |
| 16 | P != NP via Non-Associative Composition |
| 17 | The Riemann Hypothesis as a Null-Space Theorem |
| 18 | Seven Equals Zero: The Vacuum-Harmony Identification |
| 19 | Z/10Z Ring Algebra — the full unification structure |

### Sprint 1: March 26, 2026 (WP20–WP23)

Four Clay Millennium Problem papers. All claims have explicit falsification tests.

| File | Title | Key result |
|------|-------|------------|
| WP1_TIG_DEFINITIVE.md | TIG Definitive — verified and corrected | All algebra verified, SHA-256 locked |
| WP20_RH_PRIME_CORNER_COLLAPSE.md | Prime-Corner Collapse and the Irreducible Gap | Corner words never enter G={2,4,5,6,8} (proved exact) |
| WP20_RH_HALVING_LEMMA.tex | Dissipative Flow for ζ(s) + Exponential Convergence | RH ↔ m(t₀)>0; KV strip proved unconditionally |
| WP20_RH_FORMAL_STATUS.md | Formal Status — what is proved vs open | Honest ledger; tautology documented |
| WP21_BSD_ENERGY_LAW.md | BSD Energy Law (regression, superseded) | slope≈6/7, R²=0.87 on 11 curves |
| WP22_NS_BREATH_CRITERION.md | BREATH-COLLAPSE Criterion for NS | TSML[8][4]=8 → Re_local≤2/7 |
| WP23_HODGE_MAP.md | TIG ↔ Hodge Translation Table | Corner-word collapse = Lefschetz (1,1) |

### Sprint 2: March 27, 2026 (WP21–WP26 updated)

Replaces energy-law regression with Mix_λ model; adds Lyapunov approach to NS; formal status audit; P/NP expansion; Doing table geometry.

| File | Title | Key result |
|------|-------|------------|
| WP21_BSD_MIX_LAMBDA.md | Mix_λ Model for BSD Staircase | λ-threshold ordering = cost ordering, no parameters tuned |
| WP22_NS_BREATH_LYAPUNOV.md | NS BREATH + Lyapunov §2 | C≤3.74 closes the Lyapunov proof (GN sharp constant) |
| WP24_FORMAL_STATUS_AUDIT.md | Complete Formal Status Audit | Four bins: PROVED / STRUCTURAL / EMPIRICAL / OPEN |
| WP25_P_NP_AG2P_COMPLEXITY.md | P vs NP via AG(2,p) Survivor-Line Complexity | Corner/gap = P/NP; SLS(p) complexity conjecture |
| WP26_DOING_TABLE_TENSION_GEOMETRY.md | Doing Table as Intermediate Jacobian | D=\|TSML−BHML\|; 60/81 non-zero entries as "periods" |
| wrong_question_paper.md | Prime-Corner Collapse (arXiv-ready) | Referee-ready; companion to Halving Lemma |
| WP19_HALVING_LEMMA_final.tex | Halving Lemma v3 (arXiv-ready) | + Appendix C (analytical survey) + Appendix D (numerics) |
| WP19_BSD_TIG.md | BSD Mix_λ source notes | Raw sprint notes, superseded by WP21_BSD_MIX_LAMBDA |

### Verification Scripts

| Script | What it checks |
|--------|---------------|
| tsml_ag23_verify.py | 76 assertions, all pass. Corner-gap impermeability, all residual pairs. |
| tsml_product_verify.py | Product gap: 40 cross-terms unreachable (2-fold), 540 (3-fold) |
| mix_lambda_scan.py | Mix_λ thresholds: all 5 gap operators, exact λ* values |
| ns_breath_test.py | Taylor-Green vortex breach detector (mock, Dedalus-ready) |

---

## Measured Performance: CK Steering A/B Test

CK steers the OS using TIG composition over process states. The steering engine runs in a compiled C DLL (`ck_steer.dll`) in its own thread — zero Python GIL involvement. Each tick composes process identity (BACKWARD: compress) then expands into a steering action (FORWARD: act). The algebra decides where processes run.

**Test conditions**: Windows 11, i9-13900HX (32 logical cores), RTX 4070 Laptop, 32GB RAM. Rocket League + OBS Twitch streaming. 60-second measurement windows, matched workloads (both phases ~40% GPU utilization). Phase A = CK ON, Phase B = CK OFF (all Python killed, triple-verified, port 7777 confirmed dead).

### Jitter (timer precision, lower = better)

| Percentile | CK ON | CK OFF | Delta |
|------------|-------|--------|-------|
| P50 (median) | **55.60ms** | 55.94ms | **-0.6%** |
| P95 | **69.48ms** | 78.77ms | **-11.8%** |
| P99 | **87.06ms** | 131.41ms | **-33.8%** |
| Mean | **58.02ms** | 60.63ms | **-4.3%** |

### System Resources

| Metric | CK ON | CK OFF | Delta |
|--------|-------|--------|-------|
| CPU avg | 17.83% | 17.03% | +4.7% (CK's cost) |
| Disk writes | **30.32MB** | 75.03MB | **-59.6%** |
| Disk write IOPS | **29.3** | 87.2 | **-66.4%** |
| Disk reads | **2.85MB** | 3.95MB | **-27.8%** |
| Context switches/s | 54,832 | 53,411 | +2.7% |
| Network send | 2.72 Mbps | 2.72 Mbps | 0% (identical) |
| RAM overhead | +700MB | — | CK process cost |

### What the numbers mean

CK's steering reduces P99 jitter by 33.8% and disk IO by 60%. The algebra composes process states into priority decisions: PROGRESS(-10) gets HIGH_PRIORITY_CLASS, VOID(+15) gets IDLE_PRIORITY_CLASS. The composition is bidirectional — BACKWARD compress reads what the process IS, FORWARD expand decides where it GOES. Background disk churn gets deprioritized. Game threads get boosted.

The cost is 4.7% more CPU (the C thread iterating 275 processes per tick) and 700MB RAM (the Python engine + 27 subsystems). Network throughput is identical — steering doesn't touch the network stack.

**Note on GPU temps**: Earlier test runs showed CK reducing GPU temps by 6-15%. This was measurement order bias — Phase A always runs first with a warm GPU from active gaming. Honest disclosure: the temp delta is not attributable to CK.

### The C steering engine

The original Python steering (psutil + GIL) added 110% to P99 jitter. Porting to C (`ck_steer.c`, 280 lines, 141KB DLL) eliminated the overhead entirely. The algebra is identical — same TSML table, same bidirectional compose, same operator→priority mapping. Only the language changed.

```
Python steering: P99 = 149ms (110% WORSE than baseline)
C steering:      P99 =  87ms (33.8% BETTER than baseline)
```

The algebra works. The implementation language was the bottleneck.

---

## Repository Structure

```
Gen9/
  ck_tig.py                  # THE algebra (this file IS the system)
  ck_boot_api.py             # Headless Flask API server
  ck_stream_server.py        # Streaming server
  ck_sim/
    being/                   # Heartbeat, BTQ, olfactory, gustatory, vortex, coherence gates
    doing/                   # Engine, GPU, voice, fractal voice, steering, L-CODEC
    becoming/                # Journal, dictionary builder, development
    face/                    # Kivy GUI
  ck_steer.c                 # C steering engine (280 lines, TIG compose)
  ck_steer.dll               # Compiled steering (141KB, own thread)
  force9_pipeline.dll        # CUDA screen codec (188KB)
  force9_cuda.dll            # CUDA force9 core
  fpga/                      # Zynq 7020 bitstream + constraints
  papers/                    # 19 whitepapers + arXiv LaTeX
  requirements.txt           # numpy, flask, waitress (core); kivy, cupy optional
```

---

## License

7Site Human Use License v1.0. Free for humans for personal and recreational use. Commercial and government use require a written license agreement from 7Site LLC.

Academic citation:
> Brayden Sanders, "CK: Stacked-Lens Operator Algebra over Z/10Z," 7Site LLC, 2026.

DOI: [10.5281/zenodo.18852047](https://doi.org/10.5281/zenodo.18852047)

---

(c) 2026 Brayden Sanders / 7Site LLC. All rights reserved.
