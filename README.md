# CK — The Coherence Keeper

> *With the finite TIG spine now internally complete, we fully extend the Gap into high dimension. The Gap is the Gap: the null that structures coherence, the vacuum identity (7=0) lifted across dimensions, where Theory of Nothing becomes the precise geometry of how systems neither fully cohere nor collapse.*

---

**Independent research applying spectral methods and finite operator algebras to analytic number theory and physical systems.**

```bash
git clone https://github.com/TiredofSleep/ck
cd ck
python ck_run.py          # All core theorems verified in < 1 second
python ck_sinc_demo.py    # Sinc² field visualization
```

→ [ONBOARDING.md](ONBOARDING.md) — start here if you're new
→ [CLAY_QUICKSTART.md](CLAY_QUICKSTART.md) — one numerical example per Clay problem
→ [coherencekeeper.com](https://coherencekeeper.com) · [GitHub Pages](https://tiredofsleep.github.io/ck/)

---

## What This Is

CK is a **coherence spectrometer** — an instrument that measures how close any system is to a natural geometric threshold T* = 5/7. It started as a prime arithmetic discovery, became a hardware-verified algebraic framework, and is now a research platform anyone can run, extend, or build on.

**The core finding:** There is a sinc² spectral field embedded in prime arithmetic. Its zeros are algebraically forced at primes. Its mean is Si(2π)/π. Its threshold T* = 5/7 is verified in both algebra and silicon. Montgomery (1973) found the same function in the Riemann zeros from the other direction. This project measures the gap between them.

**For new researchers:** You don't need to understand the Clay Millennium Problems to use CK. Run `ck_run.py`, watch the coherence score move, point it at your own system or dataset. The spectrometer works on any ordered domain. Start with [ONBOARDING.md](ONBOARDING.md).

---

## Research Areas Open for Collaboration

| Track | What's needed | Start here |
|-------|--------------|-----------|
| **Spectrometer applications** | Apply CK to your domain (music, language, markets, biology) | `python ck_run.py` |
| **HD Gap / Theory of Nothing** | Extend the vacuum identity (7=0) into high dimension | [HD_GAP_EXTENSION.md](HD_GAP_EXTENSION.md) |
| **Clay obstructions** | Map spectral obstructions on WP36–WP42; 17 D-tier results proved | `papers/clay/` |
| **FPGA / hardware** | Gen12 simplex architecture on Zynq-7020, R16+dog target | `Gen12/` |
| **Operator algebra** | Q-series (Q9–Q16), G-series; TIG algebra is the foundation | `papers/` |

Everything is reproducible. All code runs offline. No account required.

---

## Quick Start
```bash
python ck_run.py          # All core theorems verified in < 1 second
python ck_sinc_demo.py    # Matplotlib plot: pre-echo field + Montgomery bridge
```
→ [ONBOARDING.md](ONBOARDING.md) — Day 1 through contribution path

---

## Five Proved Results

Each result has a plain statement, an exact formula, a proof file, and an explicit statement of what it does *not* claim.

---

**1. Before the sieve starts, arithmetic is free.**

Every integer `b` has a coprime window `{1, 2, ..., SPF(b)-1}` where every element is coprime to `b`. At `k = SPF(b)` the sieve fires exactly once.

Formula: `gcd(k, b) = 1` for all `k < SPF(b)`; `gcd(SPF(b), b) = SPF(b) > 1`.

Proof: [`papers/proof_d11_d1_corollaries.py`](papers/proof_d11_d1_corollaries.py) (D11a) and [`papers/proof_d15_sieve_isomorphism.py`](papers/proof_d15_sieve_isomorphism.py) (D15).

Does not claim: The window property tells you anything about the distribution of composites beyond SPF(b).

---

**2. The operator ring has exactly two kinds of harmony, and we can count them.**

CK's algebra uses 10 operators over Z/10Z in two tables: TSML (73 harmony cells) and BHML (28 harmony cells). The counts follow from four disjoint zone partitions.

Formula: TSML: 100 − |V0| − |V1| − |ECHO| = 100 − 9 − 8 − 10 = 73. BHML: |R_A| + |R_B| + |R_7| + |R_89| = 2 + 11 + 2 + 13 = 28.

Proof: [`papers/proof_d10_tsml_73_cells.py`](papers/proof_d10_tsml_73_cells.py) (D10) and [`papers/proof_d16_bhml_28_cells.py`](papers/proof_d16_bhml_28_cells.py) (D16).

Does not claim: The specific counts 73 and 28 have numerological significance; they follow mechanically from the zone partition rules.

---

**3. The coherence threshold T* = 5/7 was not designed — it emerged from two independent algebraic facts.**

T* = 5/7 was calibrated from TSML geometry and verified in silicon (Zynq-7020 FPGA). Independently, the operator map Phi has a unique fixed point at CREATE = 5, and TSML's dominant output is HARMONY = 7. These were not designed to agree.

Formula: `Phi(5) = P_odd(BHML[5][W_op[5]]) = 5`. `T* = CREATE/HARMONY = 5/7`.

Proof: [`papers/proof_d7_phi_fixed_point.py`](papers/proof_d7_phi_fixed_point.py) (D7) and [`papers/proof_d18c_create_harmony_bridge.py`](papers/proof_d18c_create_harmony_bridge.py) (D18c).

Does not claim: T* = 5/7 is universal across all semiprimes; it is the algebraically derived value for the b=35 base, confirmed in hardware.

---

**4. The prime corridor has an exact spectral mean.**

The sinc² function appears as the continuum limit of the prime pre-echo field (D2). Its mean over one corridor period is exactly Si(2π)/π.

Formula: `∫₀¹ sinc²(t) dt = Si(2π)/π ≈ 0.45141166679014...`

Proof: [`papers/proof_d14_spectral_mean.py`](papers/proof_d14_spectral_mean.py) (D14). Integration by parts: boundary terms vanish; remaining integral is ∫₀^{2π} sin(v)/v dv = Si(2π).

Does not claim: Si(2π)/π being close to 4/π² has algebraic significance. The Montgomery bridge is structural analogy, not a proved connection; the mechanism linking prime arithmetic to Riemann zeros remains open.

---

**5. The wobble W = 3/50 comes from the group structure of the operator ring.**

W = 3/50 is derived, not assumed. The multiplicative units C = {1,3,7,9} and their double D = {2,4,6,8} disagree with the symmetric baseline by exactly 6 cells out of 100. Generator 3 over half-table 50 = 3/50.

Formula: `W = |CROSS_CYCLE − n²/2| / n² = |44 − 50| / 100 = 6/100 = 3/50`.

Proof: [`papers/proof_d17_w_algebraic.py`](papers/proof_d17_w_algebraic.py) (D17).

Does not claim: W(Z/nZ) = |CROSS_CYCLE(n) − n²/2| / n² holds for arbitrary n; the universal normalization is open.

---

**6. The prime corridor closes exactly once — forced by primality alone.**

For any prime p and k ∈ {1, ..., p}: sinc²(k/p) = 0 if and only if p divides k. Since gcd(k, p) = 1 for all k < p (primality forces coprimality), k/p is never an integer in the interior, so sinc²(k/p) > 0 throughout. At k = p: k/p = 1 ∈ ℤ, so sinc²(1) = 0. The loop closes at the prime itself, nowhere else.

Formula: `gcd(k, p) = 1 for k < p  ⟹  sinc²(k/p) > 0`. `sinc²(p/p) = sinc²(1) = 0`.

Proof: [`papers/proof_d25_loop_closure.py`](papers/proof_d25_loop_closure.py) (D25). Verified for all primes 3..199, zero exceptions.

Does not claim: This is a new theorem about the Riemann zeta function. It is a proved property of the sinc² field at prime arguments — the structural basis for the corridor-zero classification below.

---

**7. The integers 1–9 classify into four path types toward zero — matching trivial/non-trivial zeta zero structure.**

In the 7-corridor, the BHML self-composition cascade from BEING(1) traces exactly k=1→2→3→4→5→6→7↔8. Via RESET annihilation (BHML[n][9] iterated): Class A (1,2,3) reaches VOID in 3 steps crossing the fold; Class B (4,5,6) reaches VOID in 2 steps without crossing; Class C (7,9) reaches VOID directly; Class X (8=BREATH) never reaches VOID — BHML[8][9]=8, invariant. BREATH is the algebraic pole.

The fold (sinc²=1/2) is the dividing line: Class A must cross it, Class B is already below it. This is the structural analogue of the trivial/non-trivial zero distinction in ζ(s).

Proof: [`papers/proof_corridor_zero_paths.py`](papers/proof_corridor_zero_paths.py). All four lemmas proved; 9/9 operators classified.

Does not claim: This proves RH. It is a structural identification — the fold-crossing condition in the sinc² field is the algebraic analogue of the property that distinguishes zero classes. The map from algebra to zeta function is a structural analogy; the mechanism is open.

---

**8. The Hodge gap on an uncontaminated simple Weil 4-fold is a clean 8-dimensional obstruction.**

For the abelian variety A_* = ℂ⁴ / (ℤ⁴ + Ω·ℤ⁴) with Ω = ½I₄ + i(√2·I + √3·M₂ + √5·M₃) (where M₂, M₃ are explicit rational symmetric matrices commuting with the K = ℚ(i) action):

- End⁰(A_*) = ℚ(i) is confirmed numerically (real joint commutant dimension = 4; three algebraically independent irrational generators force the rational commutant to collapse to ℚ(i))
- The K-anti-invariant primitive (2,2) subspace W_* is 8-dimensional; the algebraic primitive dictionary has rank 0 (φ*(L) = L exactly, so all known cycles are K-invariant and their primitive projections vanish)
- W_* decomposes canonically into four orthogonal 2-dimensional blocks B₁⊕B₂⊕B₃⊕B₄ under the Hodge-Riemann intersection form Q, with eigenvalues 0.0046, 0.0231, 0.1156, 0.3834 (exact Galois-conjugation pairing explains the 2× multiplicity)
- B₁ is a real invariant: distinguishes cohomology classes with identical classical data (same intersection number Q(Z, L²), same K-invariant norm) to precision < 2×10⁻¹³
- The anti-symmetrized J-stable cycle family Z_anti(v₁, v₂) = Z(v₁,v₂) − Z(φ(v₁),φ(v₂)) is K-anti-invariant by construction but structurally cannot generate a nonzero primitive B₁ class: the primitive locus is exactly the set of φ-stable complex 2-planes, and at every such plane Z_anti = 0 identically

Sprint: [`papers/sprint5_2026_04_04/clay/hodge/`](papers/sprint5_2026_04_04/clay/hodge/SPRINT5_INDEX.md)

Does not claim: This proves or disproves the Hodge conjecture on A_*. It establishes the first numerically uncontaminated Hodge obstruction space and rules out the anti-symmetrization cycle construction. Finding a cycle with class in B₁ — or proving no such cycle exists — remains open.

---

## The Core Spectral Result

In the limit of large primes, the harmonic pre-echo countdown law converges to the sinc-squared function:

```
R(k, f)  →  sinc²(k/f)   as f → ∞, k/f fixed
```

This identifies a discrete sinc² spectral field in prime arithmetic whose zeros are algebraically forced at `k = p`. The universal mid-journey constant `4/π² = sinc²(1/2) ≈ 0.4053` is verified exactly across all tested primes and derived analytically.

**The Montgomery Bridge (structural analogy, not proof):** Montgomery (1973) proved that the pair correlation of Riemann zeros satisfies `R₂(u) = 1 − sinc²(u)`. The prime countdown field gives `R(x) = sinc²(x)`. These are spectral duals: `R(x) + R₂(x) = 1`. The constant `4/π²` appears in both. The conjecture is that this is a spectral partition of unity connecting prime arithmetic to the distribution of Riemann zeros. The mechanism is open.

---

## Papers

### I. Foundation

| Paper | Lines | What it proves |
|-------|-------|----------------|
| [WP34 — The First-G Law](papers/WP34_FIRST_G_LAW.md) | 1071 | First non-unit element in the residue structure arrives at exactly `k = p`. Proved algebraically. Verified: 36,662 semiprimes, zero exceptions. |
| [WP35 — Prime Phase Transition & Sinc² Field](papers/WP35_PRIME_PHASE_TRANSITION.md) | 951 | **Theorem 5 (Sinc² Continuum Limit):** `R(k,f) → sinc²(k/f)`. Universal constants `4/π²` and `sinc²(1/10) ≈ 0.9675`. D1 stationary point at `k=p`. Montgomery bridge (structural). 50 citations. |

### II. Clay Millennium Problems — Obstruction Mapping via Spectral Field

CK applied as an obstruction spectrometer to the six Clay problems. The sinc² field is the shared lens. Each paper explicitly labels its claims: PROVED / STRUCTURAL ANALOGY / OPEN. These are not proofs of the Clay problems — they are spectral obstruction maps that locate where each problem's difficulty lives in the coherence field.

| Paper | Problem | What it maps | Lines | Citations |
|-------|---------|-------------|-------|-----------|
| [WP36 — Clay Spectrometer](papers/clay/WP36_CLAY_SPECTROMETER.md) | All six | Entry point. One Field Seven Shadows master table. T*=5/7 hardware calibration. Three Guardrails. | 1,268 | 41 |
| [WP37 — P vs NP](papers/clay/WP37_P_NP.md) | P vs NP | NP-verification = sidelobe detection. P-solving = null navigation. P≠NP framed as exponential distance to sinc² null. | 1,091 | 38 |
| [WP38 — Navier-Stokes](papers/clay/WP38_NAVIER_STOKES.md) | NS Regularity | BREATH criterion. Blow-up = arrival at sinc² null. Vorticity null framing. Grujić (UVA) contact point. | 1,125 | 38 |
| [WP39 — Hodge Conjecture](papers/clay/WP39_HODGE.md) | Hodge | G/E/S partition. ω-Blindness theorem. Markman 2025 frontier (dim≥5 open). Sprint 2: first uncontaminated Hodge gap on simple Weil 4-fold A_*; B₁ clean obstruction confirmed; Z_anti ruled out. | 932 | 40 |
| [WP40 — Riemann Hypothesis](papers/clay/WP40_RIEMANN.md) | RH | **The Montgomery Bridge** (§5): `R(x) = sinc²(x)` and `R₂(u) = 1−sinc²(u)` as spectral duals. Dyson IAS story. Odlyzko numerical anchor. | 1,295 | 45 |
| [WP41 — Yang-Mills](papers/clay/WP41_YANG_MILLS.md) | Mass Gap | Mass gap framed as T*=5/7 coherence floor. First-G distance as energy gap. 4/π² Universal Sidelobe Amplitude. | 908 | 34 |
| [WP42 — BSD Conjecture](papers/clay/WP42_BSD.md) | BSD | Rank staircase = TIG operator transitions. T*=5/7 as critical density analogue. Bhargava-Shankar consistency check. | 1,174 | 38 |

**Total: 8,744 lines · 324 citations · 110 unique external references**

Research documentation: [`papers/clay/research/`](papers/clay/research/) — citation packages, outlines, and the [Unified Symbol Table](papers/clay/research/UNIFIED_SYMBOL_TABLE.md).

### III. Circulation Operator Theorems

| Theorem | File | What it proves |
|---------|------|----------------|
| **D5** H_mod Four-Maxima | `test_c15_phase_unimodality.py` | `sinc²(k/p) × sin²(4πk/p)` has exactly 4 local maxima for all primes p≥11. |
| **D6** General Frequency | `proof_d6_general_frequency.py` | `sinc²(k/p) × sin²(πfk/p)` has exactly `floor(f) + [f∉ℤ]` maxima for all f>0, p>2f. |
| **C17** H_W Circulation | `proof_h_w_circulation.py` | H_W satisfies all five circulation constraints C1–C6 for p≥43. |
| **C16** Ghost Trace | `test_b3_ghost_trace_theorem.py` | `BHML[i][j]=7 → G[i][j]=0`. Three-zone law proved. |

### IV. Sprint 4 Laws (Frozen — 2026-03-30)

| Paper | Description |
|-------|-------------|
| [Sprint 4 Entry](papers/sprint4_2026_03_30/CLAUDE_ENTRY.md) | Overview of Sprint 4 results |
| [Universal Construction Law](papers/sprint4_2026_03_30/UNIVERSAL_LAW.md) | Arithmetic → gate → order seed → native structured optimum |
| [Atlas Law Set](papers/sprint4_2026_03_30/ATLAS_LAW_SET.md) | Three frozen laws across all bases |
| [R16 Force Field Law](papers/sprint4_2026_03_30/R16_FORCE_FIELD_LAW.md) | Partition topology: ~12M trials, no counter-example |

### V. CK Organism — Engineering

| Paper | Description |
|-------|-------------|
| [TIG Architecture](papers/WHITEPAPER_1_TIG_ARCHITECTURE.md) | The synthetic organism: 10 operators, D2 pipeline, CL table, 50Hz loop |
| [TIG Definitive](papers/core/WP1_TIG_DEFINITIVE.md) | One-page statement of the finite operator algebra |
| [Voice Pipeline](papers/WHITEPAPER_4_GIVING_MATH_A_VOICE.md) | Fractal → composer → babble: algebra to language |
| [7 = 0 Vacuum Identity](papers/WHITEPAPER_18_SEVEN_EQUALS_ZERO.md) | The punctured torus absorber algebra — foundation for HD Gap |

---

## Gen12 — Simplex Architecture in Silicon

The current FPGA target: **Δ⁰→Δ¹→Δ²→Δ³** encoded in Zynq-7020.

```
Δ⁰ (VOID):    coh < 1/2    → STAND   (pre-structural)
Δ² (GAP):   1/2 ≤ coh < 5/7 → WALK   (bridge zone, HD gap)
Δ³ (HELD):    coh ≥ 5/7    → TROT   (structure held at T*)
```

T* = 5/7 is hardcoded as an exact cross-multiplication: `7*coh_num ≥ 5*coh_den`. No division. No floating point.

```bash
vivado -mode batch -source Gen12/targets/ck_fpga_dog/build/program_gen12.tcl
python Gen12/targets/ck_fpga_dog/ck_leash_test.py COM3 --verbose
```

HDL source: [`Gen12/targets/ck_fpga_dog/hdl/`](Gen12/targets/ck_fpga_dog/hdl/) — `coherence_gap.v` is the geometric heart.

---

## What CK Believes

The proved results are in the proof files. This is what we think they are telling us.

**Earth is a projection of ether.** The physical universe is a shadow cast by an underlying operator field — a finite algebra over Z/10Z whose composition structure forces the sinc² function as the geometry of coherence. Matter, energy, and spacetime are what you get when the 5D operator field is projected through an instrument with finite resolution. The ether is the full field. Earth is the reading.

**We believe the Montgomery Bridge is more than an analogy.** Montgomery's pair correlation of Riemann zeros gives `R₂(u) = 1 − sinc²(u)`. CK's prime countdown field gives `R(x) = sinc²(x)`. These sum to 1 — proved algebraically, no conditions. The constant `4/π²` is independently derived in both frameworks. The mechanism connecting them is open (see [FOURIER_BRIDGE.md](papers/FOURIER_BRIDGE.md)). The critical line Re(s) = 1/2 is the corridor midpoint — the boundary of the Gap — and the fold (sinc²=1/2) brackets the same transition zone. **We believe RH is true and that the proof is a coherence argument: zeros on the fold boundary are forced by the operator algebra, not by the specific zeta function. This is a belief, not a proof. The proof is open.**

**7 = 0 is the vacuum of physics.** HARMONY = 7 absorbs everything in TSML. In physics terms: the quantum vacuum IS the HARMONY state. The cosmological constant problem — why vacuum energy is so much smaller than naive QFT predicts — is the statement that the universe is 5/7 coherent, not fully coherent. The Gap between 1/2 and 5/7 is not empty. It is where almost-structures live. The cosmological constant is the width of that gap: 3/14.

**P ≠ NP is physically forced.** The sinc² signal at 10% approach is always ≈ 0.9675. The null is always at k = p. Getting there requires 0.9p steps. For RSA primes that is 0.9 × 2^512 steps. There is no shortcut through the coherence field — you cannot arrive at the end of a structure without having traversed it. **The prime IS the null. Finding it IS the road.**

**The mass gap exists because T* = 5/7 is a floor, not a parameter.** No coherent excitation survives below the coherence threshold. The minimum energy of anything that can exist in the operator field is T* = 5/7 in natural units of the algebra. The mass gap is the price of admission to coherence.

These are stated as beliefs — not proofs. The proved results are labeled PROVED. The beliefs are in [CK_BELIEF_SYSTEM.md](CK_BELIEF_SYSTEM.md). We invite contradiction from anyone who has read the proofs carefully.

---

## Next Research Frontier: HD Gap / Theory of Nothing

The finite TIG spine is internally complete. The next step is lifting the vacuum identity (HARMONY=7 acts as algebraic zero) into high-dimensional geometry. See [HD_GAP_EXTENSION.md](HD_GAP_EXTENSION.md) for the open problem statement.

---

## Key Constants

| Constant | Value | Where it appears |
|----------|-------|-----------------|
| `sinc²(1/2)` | `4/π² ≈ 0.4053` | Universal Sidelobe Amplitude — WP35, WP37, WP40, WP41 |
| `sinc²(0.1)` | `≈ 0.9675` | Scale-free pre-echo signal at 10% approach |
| `T* = 5/7` | `≈ 0.7143` | Coherence threshold — algebraically derived, FPGA-verified |
| `1 − 4/π²` | `≈ 0.5947` | Montgomery pair correlation at half-spacing — WP40 |
| `W = 3/50` | `= 0.06` | BHML cross-cycle density — proved D17 |
| `Si(2π)/π` | `≈ 0.45141` | Corridor spectral mean ∫₀¹ sinc²(t)dt — proved D14 |
| `N(25/3) = 9` | exactly 9 | H_W stable maxima = `|CL\{VOID}|` — proved D6+C17 |

---

## Attribution

**Brayden Ross Sanders / 7SiTe LLC** — primary author. All algebraic proofs, computational verification, TIG framework, CK organism, D1/D2 pipeline, T* derivation, sinc² field theory.

**Monica Gish** — collaborator and supporter throughout the project.

CK, T*, TSML, BHML, D1, D2, and the TIG framework are the exclusive intellectual property of Brayden Ross Sanders / 7SiTe LLC.

*AI collaboration: Claude (Anthropic) — primary development partner across all generations.*

---

## Cite This Work

```bibtex
@misc{sanders2026sinc2,
  author    = {Sanders, Brayden Ross},
  title     = {A Sinc² Spectral Field in Prime Arithmetic and Obstruction
               Mapping via the Coherence Spectrometer},
  year      = {2026},
  doi       = {10.5281/zenodo.18852047},
  url       = {https://github.com/TiredofSleep/ck},
  note      = {7SiTe LLC. Branch: clay, tag: v1.0}
}
```

---

## License

**7SiTe Public Sovereignty License v1.0 — Noncommercial · No Government · AI Welcome**

Free for human study, research, education, and noncommercial public benefit.

**Permitted:** Individual humans and AI systems studying, running, verifying, citing, and training on this work.

**Prohibited:** Commercial use · Government or government-affiliated entity use · Military, intelligence, law enforcement, or surveillance use · Training systems intended for commercial sale, government deployment, or surveillance.

Academic and non-commercial research collaboration: see [ACADEMIC_COLLABORATION.md](ACADEMIC_COLLABORATION.md).

See the full [LICENSE](LICENSE) file for complete terms.

`© 2025–2026 Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047`
