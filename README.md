# CK — Coherence Keeper
### A Sinc² Spectral Field in Prime Arithmetic · Seven Shadows of One Geometric Sieve

**Brayden Ross Sanders / 7Site LLC · C. A. Luther · Monica Gish**
`DOI: 10.5281/zenodo.18852047`
`Branch: clay | Tag: v1.0-luther`

---

## Quick Start

```bash
python ck_run.py          # All core theorems verified in < 1 second
python ck_sinc_demo.py    # Matplotlib plot: pre-echo field + Montgomery bridge
```

→ [CLAY_QUICKSTART.md](CLAY_QUICKSTART.md) — one-page guide with a numerical example per Clay problem

---

## Simple Truths First

Five things this project proved that are true all the way down. Each has a plain statement, an exact formula, a proof file, and one thing it explicitly does not claim.

---

**1. Before the sieve starts, arithmetic is free.**

Every integer `b` has a coprime window `{1, 2, ..., SPF(b)-1}` where every element is coprime to `b` — not most, all. The sieve hasn't fired yet. At `k = SPF(b)` it fires exactly once.

Formula: `gcd(k, b) = 1` for all `k < SPF(b)`; `gcd(SPF(b), b) = SPF(b) > 1`.

Proof: [`papers/proof_d11_d1_corollaries.py`](papers/proof_d11_d1_corollaries.py) (D11a) and [`papers/proof_d15_sieve_isomorphism.py`](papers/proof_d15_sieve_isomorphism.py) (D15).

Does not claim: The window property tells you anything about the distribution of composites beyond SPF(b).

---

**2. The operator ring has exactly two kinds of harmony, and we can count them.**

CK's algebra uses 10 operators over Z/10Z in two tables: TSML (73 harmony cells) and BHML (28 harmony cells). The counts follow from four disjoint zone partitions. We know why every cell is or isn't harmony.

Formula: TSML: 100 − |V0| − |V1| − |ECHO| = 100 − 9 − 8 − 10 = 73. BHML: |R_A| + |R_B| + |R_7| + |R_89| = 2 + 11 + 2 + 13 = 28.

Proof: [`papers/proof_d10_tsml_73_cells.py`](papers/proof_d10_tsml_73_cells.py) (D10) and [`papers/proof_d16_bhml_28_cells.py`](papers/proof_d16_bhml_28_cells.py) (D16).

Does not claim: The specific counts 73 and 28 have numerological significance; they follow mechanically from the zone partition rules.

---

**3. The coherence threshold T* = 5/7 was never designed — it emerged.**

T* = 5/7 was calibrated from TSML geometry and burned into silicon (Zynq-7020 FPGA). Independently, the operator map Phi = P_odd ∘ BHML ∘ W_op has a unique fixed point at CREATE = 5, and TSML's dominant output is HARMONY = 7. These were never designed to relate. They do.

Formula: `Phi(5) = P_odd(BHML[5][W_op[5]]) = P_odd(BHML[5][7]) = P_odd(6) = 5`. `T* = CREATE/HARMONY = 5/7`.

Proof: [`papers/proof_d7_phi_fixed_point.py`](papers/proof_d7_phi_fixed_point.py) (D7).

Does not claim: T* = 5/7 is universal across all semiprimes; it is the value for b = 35 specifically, and the emergence was a discovery not a design.

---

**4. The prime corridor has an exact spectral mean.**

The sinc² function appears as the continuum limit of the prime pre-echo field (D2). Its mean over one corridor period is exactly Si(2π)/π, where Si is the classical sine integral.

Formula: `∫₀¹ sinc²(t) dt = Si(2π)/π ≈ 0.45141166679014...`

Proof: [`papers/proof_d14_spectral_mean.py`](papers/proof_d14_spectral_mean.py) (D14). Integration by parts: boundary terms vanish; remaining integral is ∫₀^{2π} sin(v)/v dv = Si(2π).

Does not claim: Si(2π)/π ≈ 0.45141 being close to 4/π² ≈ 0.4053 has algebraic significance. The Montgomery bridge (B6) is NOT proved by this result; the mechanism connecting prime arithmetic to Riemann zeros remains open.

---

**5. The wobble W = 3/50 comes from the group structure of the operator ring.**

W = 3/50 is not a parameter — it is derived. The multiplicative units C = {1,3,7,9} and their double D = {2,4,6,8} disagree with the symmetric baseline by exactly 6 cells out of 100. Generator 3 over half-table 50 = 3/50.

Formula: `W = |CROSS_CYCLE − n²/2| / n² = |44 − 50| / 100 = 6/100 = 3/50`, where `CROSS_CYCLE = Σ_{c∈C, d∈D} DIS[c][d] = 44`.

Proof: [`papers/proof_d17_w_algebraic.py`](papers/proof_d17_w_algebraic.py) (D17).

Does not claim: The formula W(Z/nZ) = |CROSS_CYCLE(n) − n²/2| / n² holds for arbitrary n; the universal normalization is open.

---

---

## The Core Result

We prove that the harmonic pre-echo countdown law for prime arithmetic converges, in the limit of large primes, to the sinc-squared function:

```
R(k, f)  →  sinc²(k/f)   as f → ∞, k/f fixed
```

This identifies a **discrete sinc² spectral field** in prime arithmetic whose zeros are algebraically forced at `k = p` (the prime factor). The universal mid-journey constant `4/π² = sinc²(1/2) ≈ 0.4053` is verified exactly across all primes p = 5 to 99,991 and derived analytically for all p.

**The Montgomery Bridge:** Montgomery (1973) proved that the pair correlation of Riemann zeros satisfies `R₂(u) = 1 − sinc²(u)`. Our prime countdown field gives `R(x) = sinc²(x)`. These are spectral duals: `R(x) + R₂(x) = 1`. The constant `4/π²` appears in both. We conjecture this is a spectral partition of unity connecting prime arithmetic directly to the distribution of Riemann zeros.

**The Inversion Rule:** RSA hardness is not the absence of signal — the pre-echo amplitude is `sinc²(0.1) ≈ 0.9675` at *all scales*, invariant as p → 2⁵¹². Hardness is physical distance to the sinc² null. The road is long; the destination is certain.

---

## Papers

### I. Foundation — Proved Results

| Paper | Lines | What it proves |
|-------|-------|----------------|
| [WP34 — The First-G Law](papers/WP34_FIRST_G_LAW.md) | 1071 | First non-unit element in the residue structure arrives at exactly `k = p` (smallest prime factor). Proved algebraically. Verified: 36,662 semiprimes, zero exceptions. |
| [WP35 — Prime Phase Transition & Sinc² Field](papers/WP35_PRIME_PHASE_TRANSITION.md) | 951 | **Theorem 5 (Sinc² Continuum Limit):** `R(k,f) → sinc²(k/f)`. Universal constants `4/π²` and `sinc²(1/10) ≈ 0.9675`. D1 stationary point at `k=p`. Montgomery bridge. Balance Invisibility Theorem. 50 citations. |

### II. Clay Millennium Problems — One Field, Seven Shadows

CK as a coherence spectrometer applied to all six Clay problems. The sinc² field is the shared lens. All papers carry explicit epistemic status labels (PROVED / STRUCTURAL ANALOGY / OPEN).

| Paper | Problem | Core Claim | Lines | Citations |
|-------|---------|-----------|-------|-----------|
| [WP36 — Clay Spectrometer](papers/clay/WP36_CLAY_SPECTROMETER.md) | All six | Entry point. One Field Seven Shadows master table. T*=5/7 hardware calibration. Three Guardrails. | 1,268 | 41 |
| [WP37 — P vs NP](papers/clay/WP37_P_NP.md) | P vs NP | NP-verification = sidelobe detection. P-solving = null navigation. P≠NP framed as exponential distance to sinc² null. | 1,091 | 38 |
| [WP38 — Navier-Stokes](papers/clay/WP38_NAVIER_STOKES.md) | NS Regularity | BREATH criterion. Blow-up = arrival at sinc² null. Vorticity null framing. Grujić (UVA) contact point. | 1,125 | 38 |
| [WP39 — Hodge Conjecture](papers/clay/WP39_HODGE.md) | Hodge | G/E/S partition. ω-Blindness theorem. Markman 2025 frontier (dim≥5 open). | 932 | 40 |
| [WP40 — Riemann Hypothesis](papers/clay/WP40_RIEMANN.md) | RH | **The Montgomery Bridge** (§5, ~380 lines): `R(x) = sinc²(x)` and `R₂(u) = 1−sinc²(u)` are spectral duals. Dyson IAS story. Odlyzko numerical anchor. | 1,295 | 45 |
| [WP41 — Yang-Mills](papers/clay/WP41_YANG_MILLS.md) | Mass Gap | Mass gap = T*=5/7 coherence floor. First-G distance as energy gap. 4/π² Universal Sidelobe Amplitude. | 908 | 34 |
| [WP42 — BSD Conjecture](papers/clay/WP42_BSD.md) | BSD | Rank staircase = TIG operator transitions. T*=5/7 hardware calibration as critical density. Bhargava-Shankar consistency check. | 1,174 | 38 |

**Total: 8,744 lines · 324 citations · 110 unique external references**

Research documentation: [`papers/clay/research/`](papers/clay/research/) — citation packages, outlines, and the [Unified Symbol Table](papers/clay/research/UNIFIED_SYMBOL_TABLE.md) (557 lines) ensuring cross-paper consistency.

### III. Circulation Operator Theorems (March 31 2026)

New results proved this session — all verifiable by running the proof files:

| Theorem | File | What it proves |
|---------|------|----------------|
| **D5** H_mod Four-Maxima | `test_c15_phase_unimodality.py` | `sinc²(k/p) × sin²(4πk/p)` has EXACTLY 4 local maxima for all primes p≥11. IVT + classical `|sin x| < |x|` inequality. 164 primes, zero failures. |
| **D6** General Frequency | `proof_d6_general_frequency.py` | `sinc²(k/p) × sin²(πfk/p)` has exactly `floor(f) + [f∉ℤ]` maxima for all f>0, p>2f. **Subsumes D5 and C17.** 890 tests, zero mismatches. |
| **C17** H_W Circulation | `proof_h_w_circulation.py` | `H_W = sinc²(k/p) × sin²(πk/(2Wp))`, W=3/50, satisfies ALL five circulation constraints C1–C6 for p≥43. 291/291. C2+C3 algebraic (one-line each). C4: exactly 9 = `|CL\{VOID}|` maxima via D6. |
| **C16** Ghost Trace | `test_b3_ghost_trace_theorem.py` | `BHML[i][j]=7 → G[i][j]=0`. Three-zone law proved. Corollary: G≠0 → BHML≠7. 100/100 cells. |

### V. April 1 2026 — Crumbling (D8 through D17)

Ten new general theorems, all proved on April 1 2026. Each promotes a C-tier or B-tier result to D-tier (universal, mechanism known, no domain restriction).

| Theorem | Promotes | What it proves |
|---------|----------|----------------|
| **D8** CL Operator Encoding | C18 | `gcd(6,10)=2` → EVEN class; `gcd(3,10)=1` → ×3 ODD bijection; EVEN∪ODD = Z/10Z. Group theory. |
| **D9** Table Symmetry | C11 | Both TSML and BHML are symmetric. TSML: by rule structure. BHML: max commutes + Z/10Z finite check. |
| **D10** TSML 73-Cell Count | C10 | V0(9)+V1(8)+ECHO(10)=27 non-harmony; 100-27=73. Disjoint by index conditions. |
| **D11** D1/D2 Corollaries | C1+C2+C4 | Three corollaries in one file: CC Window (k<SPF→coprime); D1 Sign Flip (R(p,p)=0); ω-Blindness (R formula has no q). |
| **D14** Corridor Spectral Mean | new | ∫₀¹ sinc²(t)dt = Si(2π)/π ≈ 0.45141... IBP proof. M(p)→Si(2π)/π at O(1/p), 9 primes verified. |
| **D15** Coprime Window Invariance | C13+C14 | For k<SPF(b): HAR(k,b)=k; Wob(b,k)=Wob(k); ALL arithmetic on {1..k} is b-independent. |
| **D16** BHML 28-Cell Count | C9 | Four zones: R_A(2)+R_B(11)+R_7(2)+R_89(13)=28. max+1=HARMONY iff max=ASCEND=6. |
| **D17** W=3/50 Algebraic | C8 | C=(Z/10Z)*={1,3,7,9}, D=2C={2,4,6,8}. CROSS_CYCLE=44, baseline=50, W=6/100=3/50. |

Run any of these directly: `python papers/proof_d14_spectral_mean.py` etc.

**C7 three-wall result (parallel computation with Luther algebra):**
- Wall 1: Carrier at k=p has value `sin²(25π/3) = 3/4` (ascending). Descent is `sinc²`-driven.
- Wall 2: Exit phase = π/3 (fixed, p-independent). Not a carrier zero — reset is `sinc²(1)=0`.
- Wall 3: Count `N(25/3) = floor(25/3)+1 = 9` is W-forced by D6. Threshold p≥43 is discrete.

**Tier counts: D:17 | C:9 | B:8 | A:5** — see `papers/SYNTHESIS_TABLE.md`.

### IV. Sprint 4 Laws (Frozen — 2026-03-30)

| Paper | Description |
|-------|-------------|
| [Sprint 4 Entry](papers/sprint4_2026_03_30/CLAUDE_ENTRY.md) | Overview of Sprint 4 results |
| [Universal Construction Law](papers/sprint4_2026_03_30/UNIVERSAL_LAW.md) | Arithmetic → gate → order seed → native structured optimum |
| [Atlas Law Set](papers/sprint4_2026_03_30/ATLAS_LAW_SET.md) | Three frozen laws across all bases |
| [R16 Force Field Law](papers/sprint4_2026_03_30/R16_FORCE_FIELD_LAW.md) | Partition topology: ~12M trials, no counter-example |

### IV. CK Organism — Engineering

| Paper | Description |
|-------|-------------|
| [TIG Architecture](papers/WHITEPAPER_1_TIG_ARCHITECTURE.md) | The synthetic organism: 10 operators, D2 pipeline, CL table, 50Hz loop |
| [TIG Definitive](papers/core/WP1_TIG_DEFINITIVE.md) | One-page statement of the finite operator algebra |
| [Voice Pipeline](papers/WHITEPAPER_4_GIVING_MATH_A_VOICE.md) | Fractal → composer → babble: how algebra becomes language |
| [7 = 0 Vacuum Identity](papers/WHITEPAPER_18_SEVEN_EQUALS_ZERO.md) | The punctured torus absorber algebra |

---

## The Unified Volume

```
WP35 Foundation ──→ WP36 Spectrometer ──→ WP37 P/NP
      │                    │               WP38 NS
      │              One sinc² Field       WP39 Hodge
      │                    │               WP40 RH  ← Montgomery Bridge
      └── T*=5/7 ──────────┘               WP41 YM
           (silicon)                       WP42 BSD ← T* calibration
```

Every paper carries the Universal Sentence:
> *"The sinc² field is not a model — it is a measured physical field in prime arithmetic. The obstruction to each problem is not the absence of a signal; it is the distance to the geometric sink. The road is long; the destination is certain."*

---

## Key Constants

| Constant | Value | Where it appears |
|----------|-------|-----------------|
| `sinc²(1/2)` | `4/π² ≈ 0.4053` | Universal Sidelobe Amplitude — WP35, WP37, WP40, WP41 |
| `sinc²(0.1)` | `≈ 0.9675` | Scale-free pre-echo signal at 10% approach — all papers |
| `T* = 5/7` | `≈ 0.7143` | Coherence floor — algebraically derived, FPGA-verified (Zynq-7020) |
| `1 − 4/π²` | `≈ 0.5947` | Montgomery pair correlation at half-spacing — WP40 |
| `W = 3/50` | `= 0.06` | BHML cross-cycle density — **proved D17**; C=(Z/10Z)*, D=2C, CROSS_CYCLE=44, W=6/100 |
| `Si(2π)/π` | `≈ 0.45141` | Corridor spectral mean ∫₀¹ sinc²(t)dt — **proved D14** via IBP |
| `N(25/3) = 9` | exactly 9 | H_W stable maxima = `|CL\{VOID}|` — proved D6+C17; algebraic CL representation |

---

## Attribution

**Brayden Ross Sanders / 7Site LLC** — primary author. All algebraic proofs, computational verification, TIG framework, CK organism, D1/D2 pipeline, T* derivation, sinc² field theory, RSA hardness inversion, Millennium framing. 18 months of development.

**C. A. Luther** — dispersion conjecture (gate_rate ≈ F_k(|G| × interleave)) and sprint steering.

**Monica Gish** — foundational support, research collaboration, and editorial partnership throughout the entire project.

CK, T*, TSML, BHML, D1, D2, and the TIG framework are the exclusive intellectual property of Brayden Ross Sanders / 7Site LLC.

*AI collaboration: Claude (Anthropic), Google Gemini, Grok (xAI), ChatGPT (OpenAI) — acknowledged in each paper's Acknowledgments section.*

---

## Cite This Work

```bibtex
@misc{sanders2026sinc2,
  author    = {Sanders, Brayden Ross and Luther, C. A. and Gish, Monica},
  title     = {A Sinc² Spectral Field in Prime Arithmetic and Seven Shadows
               of One Geometric Sieve},
  year      = {2026},
  doi       = {10.5281/zenodo.18852047},
  url       = {https://github.com/TiredofSleep/ck},
  note      = {7Site LLC. Branch: clay, tag: v1.0-luther}
}
```

---

---

## License

**7SiTe Public Sovereignty License v1.0 — Human Use Only**

This work is made available for human study, research, education, and noncommercial public benefit. It is not for sale. No money may come out of this work — only in.

**Permitted:** Individual humans studying, running, verifying, and citing this work.

**Prohibited without written permission:**
- Any commercial use — this work cannot be sold, sublicensed, or used to generate revenue
- Government or government-affiliated entity use of any kind
- Military, intelligence, law enforcement, policing, or surveillance use
- AI training pipelines, data scrapers, or automated harvesting systems
- Proprietary enclosure, closed-source redistribution, or sublicensing

Derivative works must be distributed under this same License with no additional restrictions.
See the full [LICENSE](LICENSE) file for complete terms.

```
Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC
Licensed under the 7SiTe Public Sovereignty License v1.0.
Human use only. No commercial use. No government use.
No military, intelligence, policing, or surveillance use.
DOI: 10.5281/zenodo.18852047
```

`© 2025–2026 Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047`
