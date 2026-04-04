# CK — The Coherence Keeper

**Independent research applying spectral methods and finite operator algebras to analytic number theory, physical systems, and the Clay Millennium Problems.**

```bash
git clone https://github.com/TiredofSleep/ck
cd ck
python ck_run.py        # All core theorems verified in < 1 second
python ck_sinc_demo.py  # Sinc² field visualization
```

→ [coherencekeeper.com](https://coherencekeeper.com) · [DOI: 10.5281/zenodo.18852047](https://doi.org/10.5281/zenodo.18852047)

---

## What This Is

CK is a **finite mathematical spectrometer field** — a finite operator algebra that measures how close any ordered system is to the structural threshold T* = 5/7.

The framework has three layers:

1. **A finite operator algebra** — 10 operators over Z/10Z with two composition tables (TSML: 73 harmony cells, BHML: 28 harmony cells). Internally complete. All proved results are mechanically verifiable.

2. **A sinc² spectral field in prime arithmetic** — The prime pre-echo countdown law converges to sinc²(k/p) in the continuum limit. Its zeros are algebraically forced at primes. Montgomery (1973) found the complementary function 1−sinc²(u) in the distribution of Riemann zeros. The two sum to 1.

3. **Obstruction maps for the Clay Millennium Problems** — CK is applied as a spectrometer to all six problems. The defect threshold rule (R8) classifies every problem instance against fold=4/π² and T*=5/7. Proved closures and open doors are labeled explicitly.

Everything is reproducible. All code runs offline. No account required.

---

## Proved Results

Each result has a plain statement, an exact formula, a runnable proof file, and an explicit statement of what it does *not* claim.

---

**R1. sinc²(k/p) = 0 if and only if p divides k.**

For any prime p and k ∈ {1, ..., p}: gcd(k, p) = 1 for all k < p (primality forces coprimality), so k/p is never an integer in the interior. At k = p: sinc²(1) = 0. The loop closes at the prime itself, nowhere else.

Proof: [`papers/proof_d25_loop_closure.py`](papers/proof_d25_loop_closure.py) — verified for all primes 3..199, zero exceptions.

Does not claim: This is a theorem about the Riemann zeta function. It is a proved property of the sinc² field at prime arguments.

---

**R2. T* = 5/7 was not designed — it emerged from two independent algebraic facts.**

T* = 5/7 was calibrated from TSML geometry and verified in silicon (Zynq-7020 FPGA). Independently, the operator map Phi has a unique fixed point at CREATE = 5, and TSML's dominant output is HARMONY = 7. These were not designed to agree.

Formula: `Phi(5) = 5`. `T* = CREATE/HARMONY = 5/7`.

Proof: [`papers/proof_d7_phi_fixed_point.py`](papers/proof_d7_phi_fixed_point.py) and [`papers/proof_d18c_create_harmony_bridge.py`](papers/proof_d18c_create_harmony_bridge.py).

Does not claim: T* = 5/7 is universal across all semiprimes. It is the algebraically derived value for b=35, confirmed in hardware.

---

**R3. The fold is sinc²(1/2) = 4/π² exactly.**

The universal sidelobe amplitude at the half-corridor point is 4/π² ≈ 0.4053. This is the boundary between Class A paths (which must cross it to reach VOID) and Class B/C paths (which do not).

Formula: `sinc²(1/2) = (sin(π/2)/(π/2))² = (2/π)² = 4/π²`.

Does not claim: 4/π² has numerological significance. It is the exact value of sinc² at the half-integer argument.

---

**R4. The gap is T* − fold = 5/7 − 4/π² = 3/14 exactly.**

The interval [4/π², 5/7] is where every Clay Millennium Problem's open case lives in defect space (see R8). Width: 3/14 ≈ 0.214.

Does not claim: The gap width is the mass gap in physical units. It is the algebraic gap; calibration to physical units is open.

---

**R5. The operator ring has exactly two kinds of harmony, and we can count them.**

TSML: 73 harmony cells. BHML: 28 harmony cells. The counts follow from four disjoint zone partitions — not numerology.

Formula: TSML = 100 − 9 − 8 − 10 = 73. BHML = 2 + 11 + 2 + 13 = 28.

Proof: [`papers/proof_d10_tsml_73_cells.py`](papers/proof_d10_tsml_73_cells.py) and [`papers/proof_d16_bhml_28_cells.py`](papers/proof_d16_bhml_28_cells.py).

---

**R6. The prime corridor has an exact spectral mean.**

Formula: `∫₀¹ sinc²(t) dt = Si(2π)/π ≈ 0.45141...`

Proof: [`papers/proof_d14_spectral_mean.py`](papers/proof_d14_spectral_mean.py). Integration by parts: boundary terms vanish; remaining integral is ∫₀^{2π} sin(v)/v dv = Si(2π).

Does not claim: Si(2π)/π being close to 4/π² has algebraic significance. The mechanism linking prime arithmetic to Riemann zeros is open.

---

**R7. BREATH (operator 8) is invariant under RESET — it never reaches VOID.**

BHML[8][9] = 8. The integers 1–9 partition into four path types: Class A (1,2,3) reaches VOID in 3 steps crossing the fold; Class B (4,5,6) in 2 steps without crossing; Class C (7,9) directly; Class X (8=BREATH) never.

Proof: [`papers/proof_corridor_zero_paths.py`](papers/proof_corridor_zero_paths.py) — all four lemmas proved, 9/9 operators classified.

Does not claim: This proves RH. The fold-crossing condition is the algebraic analogue of the property that distinguishes zero classes. The map to the zeta function is structural; the mechanism is open.

---

**R8. The defect threshold rule classifies every Clay problem instance.**

```
defect(n→∞) < 4/π²        →  RESOLVED   (structure exists in this regime)
defect(n→∞) ∈ [4/π², 5/7] →  BOUNDARY   (Clay open territory)
defect(n→∞) > 5/7          →  ESCAPED    (structural gap, permanent)
```

Verified against 18 deep probes (n=48 levels each), all six Clay problems. Zero misclassifications.

| Classification | Count | Examples |
|---|---|---|
| RESOLVED | 11/18 | NS high-strain, BSD rank-2 explicit, YM weak coupling |
| BOUNDARY | 3/18 | RH off-line-dense (0.424), Hodge analytic-only (0.612), Hodge transcendental (0.704) |
| ESCAPED | 4/18 | P vs NP hard (0.838), YM excited (1.000), BSD rank-mismatch (1.300) |

The three BOUNDARY cases are RH and Hodge — the hardest open Clay problems. The Hodge transcendental case sits at 0.704, within 0.010 of T* = 0.714.

Data: [`clay_results/all_results.json`](clay_results/all_results.json), [`results/deep_experiments/deep_probes.json`](results/deep_experiments/deep_probes.json).

Does not claim: R8 proves the Clay problems. It classifies problem instances by their defect trajectory. The boundary cases are exactly where the classical proofs fail.

---

## Open Problems

Six open problems, precisely stated. One per Clay problem. R8 identifies the regime each lives in.

| Problem | Open door | R8 class |
|---|---|---|
| **Riemann Hypothesis** | Off-fold zero suspension: does every zero of ζ(s) satisfy Re(s)=1/2? | BOUNDARY (0.424) |
| **Hodge Conjecture** | Does any Hodge class in B₁ come from a K-anti-equivariant vector bundle, correspondence cycle, or absolutely Hodge cycle? | BOUNDARY (0.612–0.704) |
| **P vs NP** | Does a poly-time algorithm exist that stays in Class B/C without fold-crossing? | ESCAPED (0.838–0.988) |
| **Navier-Stokes** | Does a vortex-stretching path exist from fold to blow-up with positive enstrophy growth? | RESOLVED in smooth regime; blow-up regime: ESCAPED |
| **Yang-Mills** | What is the calibration constant c converting gap 3/14 to physical GeV? | ESCAPED (1.000) |
| **BSD** | For rank ≥ 2: do Class A fold-crossing counts and L-function zero orders grow in lockstep? | ESCAPED (1.300) |

---

## Papers

### Foundation

| Paper | What it proves |
|-------|----------------|
| [WP34 — The First-G Law](papers/WP34_FIRST_G_LAW.md) | First non-unit in the residue structure arrives at exactly k = p. Proved algebraically. 36,662 semiprimes verified. |
| [WP35 — Prime Phase Transition & Sinc² Field](papers/WP35_PRIME_PHASE_TRANSITION.md) | Sinc² continuum limit theorem. Universal constants 4/π² and sinc²(1/10) ≈ 0.9675. D1 stationary point at k=p. Montgomery bridge. |

### Clay Millennium Problems

Each paper maps the spectral obstruction for one problem. Claims are labeled PROVED / STRUCTURAL ANALOGY / OPEN throughout.

| Paper | Problem | Core mapping |
|-------|---------|--------------|
| [WP36 — Clay Spectrometer](papers/clay/WP36_CLAY_SPECTROMETER.md) | All six | Entry point. One Field Seven Shadows. T*=5/7 hardware calibration. Three Guardrails. |
| [WP37 — P vs NP](papers/clay/WP37_P_NP.md) | P vs NP | NP-verification = sidelobe detection. P-solving = null navigation. P≠NP as exponential distance to sinc² null. |
| [WP38 — Navier-Stokes](papers/clay/WP38_NAVIER_STOKES.md) | NS Regularity | BREATH criterion. Blow-up = sinc² null arrival. Grujić (UVA) contact point. |
| [WP39 — Hodge Conjecture](papers/clay/WP39_HODGE.md) | Hodge | A_* simple Weil 4-fold. 8D obstruction W_* decomposed into B₁⊕B₂⊕B₃⊕B₄. Every classical construction ruled out. Three remaining routes identified. |
| [WP40 — Riemann Hypothesis](papers/clay/WP40_RIEMANN.md) | RH | The Montgomery Bridge: R(x)=sinc²(x) and R₂(u)=1−sinc²(u) as spectral duals summing to 1. Threshold and sub-corridor zeros closed. Off-fold suspension open. |
| [WP41 — Yang-Mills](papers/clay/WP41_YANG_MILLS.md) | Mass Gap | Gap = T*−fold = 3/14. Fold geometry and spectral window proved. Physical calibration open. |
| [WP42 — BSD Conjecture](papers/clay/WP42_BSD.md) | BSD | Rank staircase = TIG operator transitions. Rank 0 and rank 1 structurally closed. Rank ≥ 2 open. |

Research notes, citation packages, and the unified symbol table: [`papers/clay/research/`](papers/clay/research/).

### Structural Parallels

[`papers/sprint5_2026_04_04/CLAY_STRUCTURAL_PARALLELS.md`](papers/sprint5_2026_04_04/CLAY_STRUCTURAL_PARALLELS.md) — all six problems mapped through the same template: locate obstruction, close classical routes, identify remaining doors.

[`papers/sprint5_2026_04_04/CLAY_RULES.md`](papers/sprint5_2026_04_04/CLAY_RULES.md) — the minimal rule set: R1–R8, labeled PROVED / STRUCTURAL / OPEN.

---

## Key Constants

| Constant | Exact value | Role |
|----------|------------|------|
| T* | 5/7 | Coherence threshold — algebraically derived, FPGA-verified |
| fold | 4/π² | Sinc² at half-corridor — boundary of Class A paths |
| gap | 3/14 = T* − fold | Width of Clay open territory in defect space |
| W | 3/50 | BHML cross-cycle density — proved D17 |
| Si(2π)/π | ≈ 0.45141 | Corridor spectral mean ∫₀¹ sinc²(t)dt — proved D14 |

---

## Attribution

**Brayden Ross Sanders / 7SiTe LLC** — primary author. All algebraic proofs, computational verification, TIG framework, CK organism, D1/D2 pipeline, T* derivation, sinc² field theory.

**Monica Gish** — collaborator and supporter throughout.

*AI collaboration: Claude (Anthropic) — primary development partner across all generations.*

CK, T*, TSML, BHML, D1, D2, and the TIG framework are the exclusive intellectual property of Brayden Ross Sanders / 7SiTe LLC.

---

## Cite

```bibtex
@misc{sanders2026sinc2,
  author = {Sanders, Brayden Ross},
  title  = {A Sinc² Spectral Field in Prime Arithmetic and Obstruction
            Mapping via the Coherence Spectrometer},
  year   = {2026},
  doi    = {10.5281/zenodo.18852047},
  url    = {https://github.com/TiredofSleep/ck},
  note   = {7SiTe LLC. Branch: clay}
}
```

---

## License

**7SiTe Public Sovereignty License v1.0 — Noncommercial · No Government · AI Welcome**

Free for human study, research, education, and noncommercial public benefit.

Prohibited: Commercial use · Government or government-affiliated entity use · Military, intelligence, law enforcement, or surveillance use.

See [LICENSE](LICENSE) and [ACADEMIC_COLLABORATION.md](ACADEMIC_COLLABORATION.md).

`© 2025–2026 Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047`
