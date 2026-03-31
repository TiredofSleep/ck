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

### III. Sprint 4 Laws (Frozen — 2026-03-30)

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

`© 2026 Brayden Ross Sanders / 7Site LLC · DOI: 10.5281/zenodo.18852047`
