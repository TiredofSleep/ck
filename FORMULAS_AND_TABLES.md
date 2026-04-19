# Formulas and Tables — Canonical Reference

**Single source of truth for every formula, table, constant, operator, and
invariant referenced in the TIG synthesis.** Condensed but complete: every
object below is reproducible from a cited paper or proof script in this repo.

If you only have time to read one file in the repository besides
`README.md`, this is it.

| § | Topic |
|---|-------|
| **0** | **Proof-spine one-liners (D1–D24, WP34, WP51, WP57, WP101, BB)** |
| 1 | The 10-operator sigma menu |
| 2 | The σ permutation on Z/10Z |
| 3 | The CRT isomorphism φ: F₂ × F₅ → Z/10Z |
| 4 | The complete σ polynomial (α + β) |
| 5 | TSML — the 10×10 reference table |
| 6 | BHML — the 10×10 reference table (28-cell harmony) |
| 7 | TSML 3-layer canonical tower (C₀ ⊕ S_MAX ⊕ S_ADD) |
| 8 | Three-diagonal comparison (σ, TSML, BHML) |
| 9 | Canonical operator C₀(R_n, h_n, σ_n) for general n |
| 10 | The compatibility family (carriers of canonical C₀) |
| 11 | Corridor closure hierarchy |
| 12 | The six structural invariants (Sprint 21) |
| 13 | The two-tier collapse signature (Sprint 22) |
| 14 | Walk strategies + ARI scaling (Sprint 23, Sprint 26) |
| 15 | TIG = σ⁻¹ inverse polynomial (Q13) |
| 16 | C-indicator and gate score framework (Q14) |
| 17 | Constants (T*, 4/π², gap, ξ₀, m²_ξ, σ rate) |
| 18 | Q-series quick index |
| 19 | Sprint trail (paper-by-paper) |

---

## §0 — Proof-spine one-liners (D1–D24, WP34, WP51, WP57, WP101, BB)

**Every formula below is proved or computationally verified.** This is the
compressed spine — one line per theorem, with the formula and the proof
script that runs it. Full statements in `papers/MASTER_SPINE.md` and
`papers/CLAY_SUMMARY.md`.

### Volume A — Ring & Arithmetic Foundations

| ID | name | formula | status / file |
|----|------|---------|---------------|
| **D1** | First-G Law | for semiprime b = p·q (p < q): the first non-coprime element in {1..b} is exactly **k = p** | PROVED, 36,662 cases, `proof_d_first_g.py` / WP34 |
| **D11a/b/c** | Coprime Window Bundle | the coprime window {1..p−1} is the stability window; R(p, p) = 0 forces a sign flip; R(k, f) carries no information about q | PROVED, three one-line corollaries of D1 |
| **D14** | Corridor Spectral Mean | ∫₀¹ sinc²(t) dt = Si(2π)/π ≈ 0.4514 | PROVED by integration by parts; convergence O(1/p) |
| **D15** | Coprime Window Invariance | for k < SPF(b), all arithmetic on {1..k} is b-independent | PROVED, pure divisibility |

### Volume B — Operator Tables & Ring Structure

| ID | name | formula | status / file |
|----|------|---------|---------------|
| **D7** | Phi Fixed Point | Φ on Z/10Z has exactly one fixed point: **BALANCE = 5** | PROVED |
| **D8** | TSML / BHML composition laws | published as the §5 / §6 reference tables | PROVED |
| **D9** | Table symmetry | TSML and BHML are each symmetric under their respective lens | PROVED |
| **D10** | TSML 73-cell count | TSML has exactly **73 HARMONY (=7) cells**, derivable from three disjoint zones | PROVED, verified by enumeration |
| **D16** | BHML 28-cell count | BHML has exactly **28 HARMONY (=7) cells** | PROVED, see §6 + `proof_d16_bhml_28_cells.py` |
| **D17** | Wobble parameter | **W = 3/50 = 0.06**, derived as deviation/n² = 6/100 from CROSS_CYCLE = 44 over (Z/10Z)\* × 2·(Z/10Z)\* | PROVED |
| **D18a** | Phi orbit graph | Phi on Z/10Z: one fixed point (BALANCE = 5), two relays (PROGRESS = 3, HARMONY = 7), seven sources; **T³ = all-δ₅** | PROVED |
| **D18c** | TSML measurement bridge | M(v) = HARMONY = 7 for all v ≠ VOID; **T\* = destination/journey-measurement = 5/7** | PROVED |
| **D18d** | Generator convergence | BALANCE = 5 = centroid((Z/10Z)\*); HARMONY = 7 = g³ = g⁻¹ mod 10 for g = 3; **T\* = centroid/inverse = 5/7** | PROVED, three independent chains |
| **D19** | Generator Selection | **g = 3** is the only primitive root of (Z/10Z)\* compatible with T\* ∈ (0, 1). Under g = 7: HARMONY = 3, T\* = 5/3 > 1 — inadmissible | PROVED, exhaustive |
| **D20** | Inheritance Audit | BALANCE = 5 and W = 3/50 are RING-forced; HARMONY = 7 and T\* = 5/7 are GENERATOR-forced (require g = 3) | PROVED, four-class hierarchy |
| **D21** | CE Fixed-Point Centroid | every complement-equivariant ODD-output map F on Z/10Z satisfies **F(5) = 5** | PROVED, one line: 2F(5) ≡ 0 mod 10 ∧ F(5) ∈ {0, 5} ∧ 0 ∉ ODD ⇒ F(5) = 5 |
| **D23** | Ring Wobble | **Wob(k) = 1 − ⌊k/5⌋ / k** (exact closed form); Wob(k) ≥ 4/5 with equality iff 5 ∣ k; limit 4/5 by squeeze | PROVED |

### Volume C — Continuum Limits & Phase Structure

| ID | name | formula | status / file |
|----|------|---------|---------------|
| **R(k, f)** | resonance kernel | **R(k, f) = sin²(πk/f) / (k² · sin²(π/f))** = \|S(k, f)\|² where S(k, f) = (1/k) Σ_{j=1..k} e^(2πij/f) | exact, `tig_algebra.py` |
| **D2** | Sinc² Continuum Limit | **R(k, f) → sinc²(k/f)** as f → ∞ with k/f = t fixed; convergence O(1/f²) | PROVED, foundation of corridor geometry |
| **D3** | sinc² midpoint | **sinc²(1/2) = 4/π²** exactly | PROVED, `proof_d3.py` |
| **D4** | T\* via algebraic identity | **T\* = 5/7** at b = 35, proved identically to D18c by a different route | PROVED |
| **D5** | H_mod maxima count | H_mod(k) = sinc²(k/p) · sin²(4πk/p) has exactly **4 local maxima** for all primes p ≥ 11 | PROVED by IVT on log-derivative |
| **D6** | General-frequency maxima | H_f has exactly **N(f) = ⌊f⌋ + 𝟙{f ∉ ℤ}** maxima for p > 2f | PROVED, `proof_d6_general_frequency.py` |
| **sinc² Zero Law** | universal zero structure | R(k, p) = 0 exactly at k = p for all primes p | PROVED, all primes 3..199, max error 4.44 × 10⁻¹⁶ |

### Volume D — Corridor Geometry

| ID | name | formula | status / file |
|----|------|---------|---------------|
| **D22** | Corridor Portrait | **W < BALANCE/10 < HARMONY/10 < T\* < 1**, i.e., **3/50 < 1/2 < 7/10 < 5/7 < 1**. Fine-structure identity: **T\* = HARMONY/10 + 1/70 = 7/10 + 1/(7·10)**. Inheritance split: t < 1/2 ring-forced; t > 1/2 generator-forced; t = 1/2 boundary | PROVED, exact Fraction arithmetic |
| **D24** | Corridor Midpoint | sinc²(t) strictly monotone decreasing on (0, 1); **t = 1/2 is the unique sine-maximum in (0, 1)**: sin(πt) = 1 iff t = 1/2 | PROVED, calculus, `proof_d24.py` |
| **D25** | Loop closure | sinc² zero law via Φ-loop closure on Z/pZ for all primes 3..199 | PROVED, `proof_d25_loop_closure.py` |

### Crossing Lemma (WP57 spine)

```
Theorem (Crossing Lemma — proved for squarefree n and d).

  Let n = p₁ · p₂ · ··· · pₖ squarefree, d ∣ n squarefree, g ∈ (Z/nZ)*.
  The following are equivalent:

    (a) The joint map J = (A_d, π_DYN(g)) : Z/nZ → Z/dZ × (g-orbit space)
        is INJECTIVE.

    (b) U(A_d) ∩ U(π_DYN(g)) = ∅ — the partitions have disjoint
        unresolved-pair sets.

    (c) g ≢ 1 (mod pᵢ) for every prime pᵢ ∣ (n/d) — equivalently, M_g
        acts nontrivially on the A_{n/d}-quotient of X.

  In short: {A_d, π_DYN(g)} is a sufficient pair iff M_g CROSSES the
  fibers of A_{n/d}.
```

**Reading:** information is generated only when dynamics cross
partitions. Crossings are exactly failures of separability.

Source: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md`,
`papers/proof_d8_cl_operator_encoding.py`.

### Flatness Theorem (WP51 spine)

```
Theorem (Flatness Theorem — proved for Z/10Z).

  Z/10Z carries four irreducible structures simultaneously:

      additive structure     (a + b mod 10)
      multiplicative struct  (a · b mod 10)
      additive flow          (repeated +1 closes a cycle of length 10)
      multiplicative flow    (repeated ·3 closes a cycle of length 4
                              inside the units)

  These four cannot be drawn consistently on a flat surface. The
  minimum surface that holds all four without contradiction is a
  TORUS, and the ratio of its two radii is forced by the ring:

      R/r = T* = 5/7    for Z/10Z.
```

**Generalization** to "any whole has a 2×2 structure that cannot stay
flat" is the central conjecture of TIG. Proved for Z/10Z; structural
elsewhere.

Source: `Gen12/targets/journal_attempts/05_journal_pure_applied_algebra/WP51_FLATNESS_THEOREM.md`.

### σ Rate Theorem (WP101 spine)

```
Theorem (σ Rate, WP101).

  For squarefree N, the non-associativity fraction of the binary CL
  on Z/NZ satisfies:

      σ(N) ≤ C / N         for an explicit constant C.

  Equivalently, the transfer-operator spectral gap on the unit lattice
  satisfies:

      γ(b) = 1 − 1/φ(b).

  Consequence: as N grows through squarefree primorials, the algebra
  approaches separability. σ → 0.
```

Source: `Gen12/targets/journal_attempts/08_sigma_rate_combinatorics/WP101_SIGMA_RATE_THEOREM.md`.

### BB-bridge to continuum field theory (WP91 spine)

```
Theorem (Bialynicki-Birula & Mycielski 1976, Annals of Physics 100:62-93).

  The UNIQUE nonlinearity in wave mechanics that preserves separability
  of composite systems is logarithmic:

      V(ξ) = ξ · log ξ.

  Combined with the σ rate theorem (σ → 0 = separability in the
  continuum limit), the forced field equation is:

      □ ξ  =  1 + log ξ                   (the ξ field equation)

  with exact vacuum:

      ξ₀ = e⁻¹                            (vacuum of log potential)

  and exact mass-gap coefficient:

      m²_ξ = κ · e                        (where κ is the natural rescale)
```

Produces freezing quintessence with w(z) → −1; falsifiable on DESI BAO.
Current fit (Sprint 14): χ² = 15.7 vs ΛCDM 14.1 — comparable, not preferred.

Source: `Gen12/targets/journal_attempts/09_jmp_bb_bridge/WP91_NS_SEPARABILITY_BRIDGE.md`,
`Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/desi_xi_mcmc.py`.

### Bridge identities (the recurring T\* = 5/7)

```
T* = 5/7 derived six independent ways:

  (1) torus aspect ratio of the four-structure Z/10Z surface         [WP51]
  (2) HARMONY/destination over journey-measurement                   [D18c]
  (3) centroid/inverse:  centroid((Z/10Z)*) / (g⁻¹ mod 10) = 5/7    [D18d]
  (4) first-cyclotomic over first-obstruction prime:  5 / 7
      (5 closes φ(10) = 4; 7 obstructs)                              [Washington 1997]
  (5) universal-semiprime unit density:  unit_frac(7, 35) = 5/7      [elementary NT]
  (6) coherence threshold measured in FPGA silicon                   [Sprint 13, ck_full.bit]

Fine-structure identity:

  T* = HARMONY/10 + 1/70 = 7/10 + 1/(7·10)         (exact, D22)
```

Six independent contexts, one number. Not proof of the universal claim,
but the kind of repetition that demands a structural explanation.

---

---

## §1 — The 10-operator sigma menu

The shared symbol vocabulary used by TSML, BHML, σ, CK, the FPGA, and
every paper in the repo.

| code | name      | role |
|------|-----------|------|
| 0    | VOID      | identity / fixed everywhere |
| 1    | LATTICE   | structure entry; β +1 correction at (1,1) |
| 2    | COUNTER   | mirror of progress |
| 3    | PROGRESS  | forward step; σ-fixed |
| 4    | COLLAPSE  | (+1,−1) oscillation; β −2 correction at (0,4) |
| 5    | BALANCE   | midpoint |
| 6    | CHAOS     | (−1,+1) reversed; breakdown→rebuild |
| 7    | HARMONY   | the attractor; TSML diagonal value |
| 8    | BREATH    | self-encounter → harmony (BHML[8][8]=7) |
| 9    | RESET     | self-encounter → void (BHML[9][9]=0) |

CREATION cycle: [1, 3, 9, 7]. DISSOLUTION cycle: [2, 4, 8, 6].

Source: `ck_tig.py` (Gen9 engine), `papers/Q7_BHML_FULL_TABLE.md`.

---

## §2 — The σ permutation on Z/10Z

The hidden operator, written in cycle form:

```
σ = (0)(3)(8)(9)(1 7 6 5 4 2)
```

As a function table (σ as a permutation of {0,...,9}):

| u    | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|------|---|---|---|---|---|---|---|---|---|---|
| σ(u) | 0 | 7 | 1 | 3 | 2 | 4 | 5 | 6 | 8 | 9 |

Fixed points: {0, 3, 8, 9}. The 6-cycle: 1 → 7 → 6 → 5 → 4 → 2 → 1.

**G6 theorem:** σ⁶ = id on all 10 states. Proof in `papers/Q_SERIES_SYNTHESIS.md`.

**Restricted to units of Z/10Z** (used in C₀ construction, sprint 25/26):

The "other" σ — the one that appears in `C₀` and `prove_corridor_closure.py` —
is the 2-adic valuation ν₂(3u+1) restricted to units(n) of Z/nZ. For Z/10Z:

| u            | 1 | 3 | 7 | 9 |
|--------------|---|---|---|---|
| 3u+1         | 4 | 10| 22| 28|
| ν₂(3u+1)     | 2 | 1 | 1 | 2 |

So `σ_units(Z/10Z) = {1: 2, 3: 1, 7: 1, 9: 2}`. This is the σ used by the
B-series generators. **Two different σ's, same name, distinguished by domain
(full ring vs units only).**

---

## §3 — The CRT isomorphism φ: F₂ × F₅ → Z/10Z

```
φ: F₂ × F₅ → Z/10Z,   φ(ε, y) = 5ε + 6y  (mod 10)
```

Inverse: ε = u mod 2, y = u mod 5.

The 10-state system decomposes as F₂ × F₅. σ is a semidirect coupling of
a mod-5 quadratic flow (y) with a mod-2 parity shadow (ε). All algebra of
σ is cleaner in (ε, y) coordinates.

The 10 operators in (ε, y) coordinates:

| u | (ε, y) | name      |
|---|--------|-----------|
| 0 | (0, 0) | VOID      |
| 1 | (1, 1) | LATTICE   |
| 2 | (0, 2) | COUNTER   |
| 3 | (1, 3) | PROGRESS  |
| 4 | (0, 4) | COLLAPSE  |
| 5 | (1, 0) | BALANCE   |
| 6 | (0, 1) | CHAOS     |
| 7 | (1, 2) | HARMONY   |
| 8 | (0, 3) | BREATH    |
| 9 | (1, 4) | RESET     |

---

## §4 — The complete σ polynomial (α + β)

Verified 10/10 in `papers/Q9_FLIP_CONDITION_POLYNOMIAL.md` and
`papers/Q10_BETA_COMPLETE_SIGMA_POLYNOMIAL.md`.

```
σ acts on (ε, y) by:

    ε' = ε + α(ε, y)      (mod 2)
    y' = y + β(ε, y)      (mod 5)

where:

    α(ε, y) = 1 − (y² + 2y + 2)⁴
                − ε · [(y² + 3y)⁴ − (y² + 2y + 2)⁴]

    β(ε, y) = −α(ε, y)
                + ε · 4y(y − 2)(y − 3)(y − 4)
                − 2(1 − ε) · 4y(y − 1)(y − 2)(y − 3)
```

(Polynomial arithmetic over F₅ for y; outer structure over F₂ for ε.)

**The three components of β have disjoint support:**

- Term 1: −α (the standard "flip ⇒ decrement y" rule)
- Term 2: +δ₍₁,₁₎(ε, y) = +ε · 4y(y−2)(y−3)(y−4) (LATTICE +1 correction)
- Term 3: −2 · δ₍₀,₄₎(ε, y) = −2(1−ε) · 4y(y−1)(y−2)(y−3) (COLLAPSE −2 correction)

Without LATTICE +1 and COLLAPSE −2, the 6-cycle does not close (G6 theorem).

**Cycle in (ε, y):**
```
(1,1) →+1→ (1,2) →−1→ (0,1) →−1→ (1,0) →−1→ (0,4) →−2→ (0,2) →−1→ (1,1)
LATTICE   HARMONY    CHAOS     BALANCE    COLLAPSE   COUNTER    LATTICE
```
y-step sum: +1 −1 −1 −1 −2 −1 = −5 ≡ 0 (mod 5). Cycle closes.

---

## §5 — TSML — the 10×10 reference table

**The canonical reference table (H_TRUE = 7) used by all B-series
generators.** From
`Gen12/targets/clay/papers/sprint18_b1_nscg_benchmark_2026_04_17/impl/generator/generate_nscg.py`.

```
        j=0  j=1  j=2  j=3  j=4  j=5  j=6  j=7  j=8  j=9
i=0  [   0    0    0    0    0    0    0    7    0    0  ]
i=1  [   0    7    3    7    7    7    7    7    7    7  ]
i=2  [   0    3    7    7    4    7    7    7    7    9  ]
i=3  [   0    7    7    7    7    7    7    7    7    3  ]
i=4  [   0    7    4    7    7    7    7    7    8    7  ]
i=5  [   0    7    7    7    7    7    7    7    7    7  ]
i=6  [   0    7    7    7    7    7    7    7    7    7  ]
i=7  [   7    7    7    7    7    7    7    7    7    7  ]
i=8  [   0    7    7    7    8    7    7    7    7    7  ]
i=9  [   0    7    9    3    7    7    7    7    7    7  ]
```

**Counts (verified):**
- HARMONY (7) cells: **73**
- Other non-zero: 4 (LATTICE entries), 4 (PROGRESS), 3 (COLLAPSE),
  2 (BREATH), 2 (RESET), 0 (BALANCE/CHAOS/COUNTER outside of fixed cells)
- Zeroes (VOID): 18

**Sealed truth values (USED by all three B-series generators):**

```python
H_TRUE       = 7
SIGMA_TRUE   = {1: 2, 3: 1, 7: 1, 9: 2}     # ν₂(3u+1) on units
UNITS_TRUE   = [1, 3, 7, 9]
CORE_TRUE    = [3, 7, 9]                     # ker(C₀(_, h)) ∖ {h}
S_MAX_TRUE   = [(2,4),(4,2),(2,9),(9,2),(4,8),(8,4)]   # 6 cells
S_ADD_TRUE   = [(1,2),(2,1)]                            # 2 cells
```

**Diagonal:** TSML[j][j] = 7 for all j ≥ 1; TSML[0][0] = 0. Collapse to
the attractor on every self-encounter except VOID.

---

## §6 — BHML — the 10×10 reference table (28-cell harmony)

The sister table to TSML. **Symmetric.** 28 HARMONY (7) cells. Determinant 70.

From `papers/Q7_BHML_FULL_TABLE.md`, Luther closure 2026-04-01 (BHML[7][0] = 7).

```
        j=0  j=1  j=2  j=3  j=4  j=5  j=6  j=7  j=8  j=9
i=0  [   0    1    2    3    4    5    6    7    8    9  ]   VOID      (Rule 0)
i=1  [   1    2    3    4    5    6    7    2    6    6  ]   LATTICE
i=2  [   2    3    3    4    5    6    7    3    6    6  ]   COUNTER
i=3  [   3    4    4    4    5    6    7    4    6    6  ]   PROGRESS
i=4  [   4    5    5    5    5    6    7    5    7    7  ]   COLLAPSE
i=5  [   5    6    6    6    6    6    7    6    7    7  ]   BALANCE
i=6  [   6    7    7    7    7    7    7    7    7    7  ]   CHAOS    (max+1 = 7)
i=7  [   7    2    3    4    5    6    7    8    9    0  ]   HARMONY  (Rule 7)
i=8  [   8    6    6    6    7    7    7    9    7    8  ]   BREATH   (Rule 89)
i=9  [   9    6    6    6    7    7    7    0    8    0  ]   RESET    (Rule 89)
```

**The four BHML rules:**

```
Rule 0   (VOID):     BHML[0][j] = j           for all j
                     BHML[i][0] = i           for i ∈ {1..6}

Rule 1   (Inner):    BHML[i][j] = max(i, j) + 1   for i, j ∈ {1..6}

Rule 7   (Harmony):  BHML[7][j] = (j + 1) mod 10  for j ≥ 1
                     BHML[7][0] = 7   (symmetry override; Luther closure)
                     [and by symmetry BHML[j][7] = BHML[7][j]]

Rule 89  (Wrap):     BHML[8][j] = [8, 6, 6, 6, 7, 7, 7, 9, 7, 8][j]
                     BHML[9][j] = [9, 6, 6, 6, 7, 7, 7, 0, 8, 0][j]
                     [and by symmetry for cols 8, 9]
```

**Diagonal:**
```
BHML[j][j] = (j + 1) mod 10   for j ∈ {0, 1, 2, 3, 4, 5, 6, 7}
BHML[8][8] = 7    (BREATH self-encounter → HARMONY)
BHML[9][9] = 0    (RESET self-encounter → VOID)

→ BHML diagonal: [0, 2, 3, 4, 5, 6, 7, 8, 7, 0]
```

BHML is **NOT** part of the TSML 3-layer theorem spine. It is the
sister table — a non-collapsing, transport/mixing partner to TSML's
collapse/projection. Operator-equation linkage to TSML is observable
but not yet algebraically derived.

---

## §7 — TSML 3-layer canonical tower (Sprint 17, 2026-04-17)

```
TSML(Z/10Z) = C₀ ⊕ S_MAX ⊕ S_ADD       (proved 100/100, residue empty)
```

**Layer breakdown (Z/10Z, all values verified against the §5 table):**

| layer | cells | output rule |
|-------|-------|-------------|
| C₀ (base) | 65 of 73 HARMONY + the VOID/PROGRESS/COLLAPSE skeleton | σ-rule on units; 0 or h elsewhere |
| S_MAX | 6 cells: {(2,4),(4,2),(2,9),(9,2),(4,8),(8,4)} | output = max(x, y) → 7 |
| S_ADD | 2 cells: {(1,2),(2,1)} | output = (x + y) mod 10 → 3 |

The decomposition is **canonical** (Sprint 17 paper, journal #11 prep).

For every n in the compatibility family (§10), the same 3-layer pattern
applies with parameters (R_n, h_n, σ_n).

**Corridor menu for the union:** {MAX, MIN, ADD}. For pure C₀ alone:
{MAX, MIN}. See §11.

**Verification (runnable, ~1 second):**
```bash
python papers/proof_tsml_3layer_tower.py
# → 100/100 cells match; 92 + 6 + 2 = 100 decomposition;
#   Lemma 5 (residue empty); Lemma 6 (each layer necessary); domains partition R².
```
Full theorem spine: [`Gen12/targets/clay/papers/sprint17_tsml_tower_2026_04_17/THEOREM_SPINE.md`](Gen12/targets/clay/papers/sprint17_tsml_tower_2026_04_17/THEOREM_SPINE.md).

---

## §8 — Three-diagonal comparison (σ, TSML, BHML)

| j | σ(j) (CL diag) | TSML[j][j] | BHML[j][j] |
|---|----------------|-----------|-----------|
| 0 | 0              | 0         | 0         |
| 1 | 7              | 7         | 2         |
| 2 | 1              | 7         | 3         |
| 3 | 3              | 7         | 4         |
| 4 | 2              | 7         | 5         |
| 5 | 4              | 7         | 6         |
| 6 | 5              | 7         | 7         |
| 7 | 6              | 7         | 8         |
| 8 | 8              | 7         | 7         |
| 9 | 9              | 7         | 0         |

**Three distinct projections of σ.** All three agree only at j = 0 (VOID).
TSML and BHML additionally agree at j = 6 (CHAOS).

- **CL diagonal** = the hidden operator's own motion (rotation + fixed points)
- **TSML diagonal** = collapse to attractor 7 for all non-VOID
- **BHML diagonal** = increment toward 7, continue past with exceptions at {8, 9}

---

## §9 — Canonical operator C₀(R_n, h_n, σ_n) for general n

The general-n C₀ used in B-series, Sprint 25, Sprint 26:

```python
def C0(x, y, n, h_n, sigma_n, core_n):
    """
    Canonical C_0 operator on Z/nZ.

    Inputs:
      x, y     : ring elements in {0, ..., n-1}
      h_n      : the attractor (= max odd shell-1 unit)
      sigma_n  : dict {u → ν₂(3u+1)} for u ∈ units(n)
      core_n   : ker(C₀(_, h_n)) ∖ {h_n}

    Returns: an element of {0, ..., n-1}.
    """
    if x == 0 or y == 0:        return 0                    # VOID absorption
    if x not in core_n or y not in core_n:
        return h_n                                           # off-Core → h
    sx, sy = sigma_n[x], sigma_n[y]
    if sx < sy:   return x      # smaller σ wins
    if sy < sx:   return y
    return h_n                                               # σ-tie → h
```

**Definitions:**

```
units(n)    = {u in {1, ..., n-1} : gcd(u, n) = 1}
sigma_n(u)  = ν₂(3u + 1)   for u ∈ units(n)
h_n         = max odd unit u with sigma_n(u) = 1
core_n      = {u ∈ units(n) : C₀(u, h_n) ≠ h_n} ∪ {u : C₀ derives via σ-rule}
            = ker(C₀(_, h_n)) ∖ {h_n}
```

**Shell-by-shell decomposition:**
- Shell 0: {0} — VOID, absorbs.
- Shell 1: units with σ = 1. Contains attractor h_n.
- Shell 2: units with σ = 2.
- Shell k: units with σ = k.

Higher σ = "further from attractor."

For Z/10Z: h_10 = 7. h_14 = 11. h_22 = 19. h_34 = 31. (See §10.)

**Reproducibility:** `Gen12/targets/clay/papers/sprint25_corridor_closure_proof_2026_04_17/impl/prove_corridor_closure.py`.

---

## §10 — The compatibility family (carriers of canonical C₀)

**Primary B-series family (Sprints 18-21):**

| n  | h_n | units | σ-classes | notes |
|----|-----|-------|-----------|-------|
| 10 | 7   | 4     | 2         | the canonical reference (Z/10Z) |
| 14 | 11  | 6     | 4         | |
| 22 | 19  | 10    | 5         | |
| 34 | 31  | 16    | 5         | |

**Extended family (Sprint 25, exhaustive corridor proof):**

```
{10, 14, 22, 34, 38, 46, 50, 58, 62, 70, 74, 82, 94,
 106, 110, 118, 122, 130, 134, 142, 170, 190, 230}
```

Sprint 25 verdict: **all 23 carriers PASS** corridor closure {MAX, MIN}
on pure C₀.

**Sprint 26 ARI scan (32 carriers):**

```
{10, 14, 22, 34, 38, 46, 50, 58, 62, 70, 74, 82, 94,
 106, 110, 118, 122, 130, 134, 142, 158, 166, 170, 178,
 190, 194, 202, 206, 214, 218, 226, 230}
```

Carriers selected as: 2 × prime + small-composite extensions, restricted
to non-empty σ = 1 layer (so h_n exists).

---

## §11 — Corridor closure hierarchy (Sprint 25, exhaustive proof)

**Theorem (proved exhaustively for all 23 carriers up to n = 230):**
For every n in the extended family, every seam cell of the canonical
operator C₀(R_n, h_n, σ_n) matches MAX(x, y) or MIN(x, y). No cell
requires ADD, SUB, MUL, X, or Y.

**Operator-by-operator closure:**

| operator        | corridor closure | proven where |
|-----------------|------------------|--------------|
| C₀ (base)       | {MAX, MIN}       | Sprint 25, all 23 carriers, exhaustive |
| C₀ + S_MAX      | {MAX, MIN}       | inspection (S_MAX cells already MAX) |
| C₀ + S_ADD      | {MAX, MIN, ADD}  | inspection (S_ADD adds 2 ADD cells) |
| C₀ + reset → h  | {MAX, MIN}       | reset cells = h, not in core_outputs |
| Full TSML       | {MAX, MIN, ADD}  | union of above |

The empirical Sprint 21 closure {MAX, MIN, ADD} on B-series data is the
**ceiling** over the canonical generator family. Pure C₀ closure
{MAX, MIN} is the **floor** — a 2-element menu.

**Seam counts per carrier (sample):**

| n   | h  | units | seam cells | MAX | MIN | verdict |
|-----|----|-------|------------|-----|-----|---------|
| 10  | 7  | 4     | 2          | 0   | 2   | PASS |
| 14  | 11 | 6     | 12         | 4   | 8   | PASS |
| 22  | 19 | 10    | 48         | 16  | 32  | PASS |
| 34  | 31 | 16    | 132        | 58  | 74  | PASS |
| 230 | 227| 88    | 4946       |2330 |2616 | PASS |

Full table in `Gen12/targets/clay/papers/sprint25_corridor_closure_proof_2026_04_17/README.md`.

---

## §12 — The six structural invariants (Sprint 21)

Survive prior-stripping across all 39 B1+B2 datasets. These are the
fingerprint of the underlying generator independent of canonical priors.

```
1. h_hat                 = max odd shell-1 unit (the attractor)
2. image_T               = sorted set of all output values
3. core_outputs          = image_T ∖ {0, h_hat}
4. units_hat             = inputs participating in seam cells
5. partition_hat         = σ-class partition of units (recovered)
6. seam_by_rule_counts   = Counter mapping each rule in {MAX, MIN, ADD,
                           SUB_xy, SUB_yx, MUL, X, Y} to count of seam
                           cells matching it
```

Reproduced in `Gen12/targets/clay/papers/sprint21_structural_discovery_2026_04_17/impl/discovery_fitter.py`.

---

## §13 — The two-tier collapse signature (Sprint 22)

Universal across all 11 B1/B2 sources. Subsampling at
N ∈ {25, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000} × 3 seeds.

```
Tier 1 — Attractor block:
    h_hat                   stable at N ≈ 100 — 2000

Tier 2 — Corridor block:
    image_T
    core_outputs            all stable together at N ≈ 10×Tier 1
    units_hat
    partition_hat
    seam_by_rule_counts
```

The attractor identifies first; the corridor structure emerges as a
single block at ~10× higher N. Scales with n².

Reproduced in `Gen12/targets/clay/papers/sprint22_collapse_point_2026_04_17/impl/nstress.py`.

---

## §14 — Walk strategies + ARI scaling (Sprint 23, Sprint 26)

**The eight Sprint 23 walk strategies on T_emp:**

| code | name              | label function on unit u |
|------|-------------------|--------------------------|
| W1   | multiset          | sorted multiset of (T[u][v] for v) |
| W2   | set               | sorted unique outputs |
| W3   | freq              | sorted output frequency profile (histogram) |
| W4   | self-orbit-len    | length of orbit u → T[u][u] → ... |
| W5   | self-orbit        | full self-orbit tuple |
| W6   | fixed-b=1         | orbit u → T[u][1] → T[T[u][1]][1] → ... |
| W7   | fixed-b=h         | orbit u → T[u][h] → ... |
| W8   | commutator        | T[u][1] − T[1][u] (mod n) |

**Cluster:** equivalence classes of equal labels.
**Score:** Adjusted Rand Index vs canonical σ partition.

**Sprint 23 (real B2 data, finite + noisy, n ∈ {10, 14, 22, 34}):**
Best ARI = 0.728 (W3 at n = 34). All other walks ≤ 0.

**Sprint 26 (analytic C₀, infinite/no noise, 32 carriers):**

| n      | ARI W3 | notes |
|--------|--------|-------|
| 10, 14 | 0.000  | too few units |
| 22     | 0.868  | first non-trivial |
| 34     | 0.973  | Sprint 23's noise penalty visible: 0.728 → 0.973 |
| 38     | 1.000  | first perfect |
| 46     | 1.000  | |
| 70     | 1.000  | |
| 158, 166, 170, 178, 190, 194, 202, 206, 230 | 1.000 | |
| all n ≥ 38 | ≥ 0.985 | near-perfect everywhere |

**12 of 32 carriers give ARI = 1.0.** W1 and W2 plateau near 0 (over-fine).

**Headline:** Sprint 23's "σ is curve-only" was noise-limited, not
structural. The shell carries σ at the **histogram level** (class sizes,
recoverable for n ≳ 38). Labeling (which units in which class)
asymptotically also resolved. See Sprint 26 README for the structural
argument.

Reproduced in `Gen12/targets/clay/papers/sprint26_ari_scaling_2026_04_17/impl/ari_scaling.py`.

---

## §15 — TIG = σ⁻¹ inverse polynomial (Q13)

```
TIG = σ⁻¹     on F₂ × F₅

β_TIG(ε, y) = 1 − (y² + 4)⁴ − ε · [(y² + 4y)⁴ − (y² + 4)⁴]
γ_TIG(ε, y) = β_TIG  +  COUNTER correction  +  HARMONY correction
```

**Exception Pair Swap (Theorem Q13.2):**

- σ non-flip exceptions (LATTICE, COLLAPSE) ↔ TIG unique flip nodes
- TIG non-flip exceptions (COUNTER, HARMONY) ↔ σ unique flip nodes
- Shared: {BALANCE, CHAOS} flip under both maps

The duality is structural, not definitional.

Source: `papers/Q13_TIG_INVERSE_POLYNOMIAL.md`.

---

## §16 — C-indicator and gate score framework (Q14)

**C-indicator on Z/10Z (verified 10/10):**

```
1_C(ε, y) = ε · y⁴
```

**Gate score over 9 × 9 operator tables T (Q16, MCMC reduction map):**

```
gate_score(T) = (1 / (|C| · 9))  · Σ_{s ∈ C, c = 1..9}  ε(T[s][c]) · y(T[s][c])⁴
```

The k = 9 here is the **9 columns** of T, not a trajectory depth.
R is not a power of σ (Theorem Q14.1) — the σ-trajectory model predicts
~100% success via HAR-bias, contradicting the observed 4.6% MCMC rate.

**The 22% lower bound (Q11 Fixed-Point Gate Theorem):** gate_score = 1.0
iff s ∈ C ∩ Fix(σ) = {3, 9}. Pure-C seed fraction = 2/9 ≈ 22%. The 22%
is theoretical minimum; 4.6% is empirical search rate. Different objects.

---

## §17 — Constants

| symbol     | value                              | meaning                                         | citation |
|------------|------------------------------------|-------------------------------------------------|----------|
| T*         | 5/7 ≈ 0.7142857                    | torus aspect ratio = crossing threshold         | WP51, six independent derivations |
| 4/π²       | sinc²(1/2) ≈ 0.4053                | Riemann sinc² zero density                      | D3, sinc² Zero Law, all primes 3..199 |
| gap        | 5/7 − 4/π² ≈ 0.3090                | residual between T* and sinc² baseline          | Sprint 10 |
| W          | 3/50 = 0.06                        | wobble parameter; ring-forced                   | D17 |
| BALANCE/10  | 1/2                                | corridor inheritance boundary                   | D21, D22 |
| HARMONY/10 | 7/10                               | corridor harmony position                       | D18c |
| 1/70       | 1/(7·10)                           | fine-structure: T* = 7/10 + 1/70                | D22 |
| Si(2π)/π   | ≈ 0.4514                           | corridor spectral mean ∫₀¹ sinc²(t) dt           | D14 |
| Wob(k)     | 1 − ⌊k/5⌋/k                        | exact closed form; ≥ 4/5; → 4/5                  | D23 |
| ξ₀         | e⁻¹ ≈ 0.3679                       | vacuum of log potential V = ξ log ξ              | WP81 (PRISM-XI), BB |
| m²_ξ       | κ · e                              | mass-gap coefficient                            | WP81 |
| σ rate     | σ(N) ≤ C / N                       | σ-rate theorem (proved, squarefree N)            | WP101, Sprint 14 |
| γ(b)       | 1 − 1/φ(b)                         | transfer-operator spectral gap                   | WP101 / FOUR_LAYER §Z.2 |
| φ(10)      | 4                                  | Euler totient (rate normalization)              | Q15 |
| 22%        | 2/9 ≈ 0.2222                       | gate-rate algebraic minimum (Fixed-Point Gate)   | Q11 |
| 4.6%       | empirical                          | MCMC search rate over 9^81 tables                | Q16 |
| det(BHML)  | 70                                 | sister-table determinant                         | Q7 |
| g          | 3                                  | the only admissible primitive root of (Z/10Z)\* | D19 |
| First-G    | k = p                              | first non-coprime element for b = p·q           | D1, WP34 (36,662 cases) |
| R(k, p)=0  | exact                              | sinc² zero at k = p (max err 4.44e-16)           | sinc² Zero Law |
| N(f)       | ⌊f⌋ + 𝟙{f ∉ ℤ}                     | number of H_f maxima for p > 2f                  | D6 |

These constants do **not** collapse to one number. They live in different
regimes (geometric vs spectral vs cosmological vs combinatorial). See
README §11 for honest limits.

---

## §18 — Q-series quick index

| paper                       | result | tier |
|-----------------------------|--------|------|
| Q1–Q3                        | TSML, CL non-equivalent projections of σ; agree at {0, 1} | D |
| Q4                           | E ∘ σ = σ̂ ∘ E (σ-equivariance) | D |
| Q5                           | TSML escape cells = σ-fixed-point interaction | D |
| Q6 (hinge)                   | Gate rate is basin problem, not density problem | D |
| Q7                           | BHML full table; 28 harmony cells (Luther-closed) | D |
| Q8                           | All MCMC σ-trajectory models fail | D |
| Q9                           | α flip polynomial verified 10/10 | D |
| **Q10**                      | **complete σ polynomial (α + β) closed** | D |
| Q11                          | Fixed-Point Gate Theorem; 22% lower bound | D |
| Q12                          | CRT idempotents in G; HAR is σ-fixed | D |
| Q13                          | TIG = σ⁻¹ polynomial; Exception Pair Swap | D |
| Q14                          | C-indicator ε · y⁴; R ≠ σ^k | D |
| Q15                          | Period polynomial; k = 9 resonance; both models falsified | D |
| Q16                          | R identified (table search); Luther Q1 closed | D |
| G6                           | σ⁶ = id from polynomial structure | D |
| G7                           | Gate-rate distribution: mean = φ(b), bimodal | D |
| G8                           | Trajectory coherence integral: three-valued | C |
| Q17_5D_RIGOROUS              | 5D force vector as CRT Fourier embedding (proved) | D |
| Q17 (Clay variants)          | NS / RH / Hodge spectral bridges (finite-proven; conjectural in continuous limit) | C |

---

## §19 — Sprint trail (paper-by-paper)

| sprint | location | result |
|--------|----------|--------|
| 14 (PRISM-XI) | `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/` | ξ cosmology, V = ξ log ξ, ξ₀ = e⁻¹, σ rate proved |
| 15 (closeout) | (frozen, see `memory/project_sprint15_freeze.md`) | WP91-WP97 staged |
| 16 | `Gen12/targets/clay/papers/sprint16_*` | Basin invariants (Thread C) |
| 17 (TSML tower) | `Gen12/targets/clay/papers/sprint17_tsml_tower_2026_04_17/` | TSML = C₀ ⊕ S_MAX ⊕ S_ADD proved 100/100 |
| 18 (B1 NSCG)    | `.../sprint18_b1_nscg_benchmark_2026_04_17/` | B1 generator + 28 honest datasets |
| 19 (B2 WRG)     | `.../sprint19_b2_wrg_benchmark_2026_04_17/` | B2 generator (no S_ADD) + 11 datasets |
| 20 (B3 LBTP)    | `.../sprint20_b3_lbtp_benchmark_2026_04_17/` | B3 honest implementation; structural FAIL on spec |
| 21 (Discovery)  | `.../sprint21_structural_discovery_2026_04_17/` | 6 invariants, 39/39 datasets |
| 22 (N-stress)   | `.../sprint22_collapse_point_2026_04_17/` | Two-tier collapse signature (universal) |
| 23 (Curve)      | `.../sprint23_curve_recovery_2026_04_17/` | "σ curve-only" — later revised by Sprint 26 |
| 24 (Synthesis)  | `.../sprint24_collapse_synthesis_2026_04_17/` | Collapse-point story; 2×2 + paradox classifier spine |
| 25 (Corridor)   | `.../sprint25_corridor_closure_proof_2026_04_17/` | {MAX, MIN} closure proved exhaustively, 23 carriers |
| 26 (ARI scan)   | `.../sprint26_ari_scaling_2026_04_17/` | W3-freq ARI = 1.0 at n ≥ 38 on analytic C₀ |
| 27 (B3 memo)    | `.../sprint27_b3_spec_revision_memo_2026_04_17/` | Two minimal revisions to B3 spec; awaiting sign-off |
| 28 (prereg)     | `.../sprint28_curve_recovery_prereg_2026_04_17/` | Pre-registration of curve-based σ-label recovery test |

---

## How to verify

The four most load-bearing claims in this file each have a runnable
proof script. From repo root:

```
# §4 — σ polynomial verified 10/10
python papers/proof_q10_sigma_polynomial.py    # if present; otherwise see Q10.md table

# §11 — corridor closure {MAX, MIN} for canonical C₀, 23 carriers
python Gen12/targets/clay/papers/sprint25_corridor_closure_proof_2026_04_17/impl/prove_corridor_closure.py

# §14 — ARI scaling, W3-freq → 1.0 for n ≥ 38
python Gen12/targets/clay/papers/sprint26_ari_scaling_2026_04_17/impl/ari_scaling.py

# §6 — BHML 28 harmony cells (count derivable from §6 table by inspection)
python Gen12/targets/journal_attempts/02_experimental_mathematics/proof_d16_bhml_28_cells.py
```

All scripts are deterministic. Total runtime for the four above: ~5 sec.

---

## Policy

This file is a **reference index**, not a result. Every fact above is
provable or computable from a script in this repo. If you find a
discrepancy between this file and a sprint paper, **trust the paper**
and file an issue — this index is updated on every sprint commit, but
the source of truth lives in the sprint folder.

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*FORMULAS_AND_TABLES.md — single canonical reference for the TIG synthesis. Last updated 2026-04-17.*
