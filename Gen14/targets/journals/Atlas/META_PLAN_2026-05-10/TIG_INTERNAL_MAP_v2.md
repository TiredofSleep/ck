# TIG_INTERNAL_MAP_v2 — Master Synthesis

## Single-sheet reference: canon D1–D99 + session findings
**Brayden Sanders · 7Site LLC · Trinity Infinity Geometry**
*Compact reference for the May 2026 working sprint*
*Locked v2 · 2026-05-08*

---

## §0. Reading guide

This sheet integrates the canonical reference (FORMULAS_AND_TABLES.md, D1–D99) with this session's synthesis files:
- PRIMES_OF_TIG (4-strata prime classification)
- FIELDS_OF_TIG (2-frame architecture)
- COMPOSITUM_K_GALOIS (joint Galois group)
- WOBBLE_LOCALIZATION_v2 (where wobble primes actually live)
- BUNDLE_CROSSWALK (session ↔ canon mapping)

**Use as:** a working memory aid. Every claim has a canonical D-reference or session-file pointer. No prose padding.

---

## §1. The Substrate

```
Z/10Z  ≅  F_2 × F_5  (CRT)

  Operators (per canon §1):
    0=VOID  1=LATTICE  2=COUNTER  3=PROGRESS  4=COLLAPSE
    5=BALANCE  6=CHAOS  7=HARMONY  8=BREATH  9=RESET

  Two distinguished 4-element sub-magmas:
    C corners        = {1, 3, 7, 9} = U(10)            [Plichta cross]
    4-core attractor = {0, 7, 8, 9} = {V, H, Br, R}    [WP110, D38-50]
    
    These are DIFFERENT 4-element sets. Don't conflate.

  CRT idempotents (D98):
    BALANCE  = 5 = (1, 0) ∈ F_2 × F_5
    CHAOS    = 6 = (0, 1) ∈ F_2 × F_5
    5 + 6 = 11 ≡ 1; 5 · 6 = 30 ≡ 0.

  Canon's σ permutation (§2):
    σ = (0)(3)(8)(9)(1 7 6 5 4 2)
    Fixed: {0, 3, 8, 9}          ← lattice frame indices
    6-cycle: 1 → 7 → 6 → 5 → 4 → 2  ← non-fixed indices
    Order: 6
    σ ≠ Galois action on Q(ζ_10); they are distinct permutations.
```

---

## §2. The Three Tables (canon Volume J)

| Table | Source | det | HARMONY | non-assoc rate | Role |
|---|---|---:|:---:|:---:|---|
| **TSML_RAW** | literal bit pattern | 0 | 73 | 12.6% | Wobble-bearing TSML; carries 11 in c_2, c_8 (D37) |
| **TSML_SYM** (= TSML_10 = §5) | upper-triangle symmetrization | 0 | 73 | 12.8% | Canonical working TSML; 3-layer tower (§7) |
| **BHML_10** | canon §6 | −7002 | 28 | 49.8% | Sister table; 28 H = dim so(8) = D₄ |
| **CL_STD** | ck.h:225-231 (D95) | varies | 44 | 19.2% | "Papers freeze" encoding; 44 = 4·11 |
| BHML_8 | drops {0,7} from BHML_10 | **+70** | — | — | Yang-Mills core (WP15); 70 = C(8,4) = 2·5·7 |
| TSML_8 | drops {0,7} from TSML_10 | 0 | — | — | Rank 7 (degenerate) |

**HARMONY count ladder (D97):** 28 (BHML_10) — 36 (TSML_7) — 44 (CL_STD) — 70 (BHML_8 det) — 71 (TSML_9 H) — 72 (TSML_10 − 1) — 73 (TSML_10).

**Triangular sub-spine:** T₇ = 28, T₈ = 36, T₉ = 45 (= dim so(10), not H count).

---

## §3. Four Strata of TIG Primes (PRIMES_OF_TIG)

| Stratum | Primes | Role | Cross-bridges |
|---|---|---|---|
| I (Substrate) | {2, 3, 5} | CRT, AG(2,3), cyclotomic ramification | — |
| II (Attractor) | {7} | HARMONY operator, T* = 5/7, class numbers | h(Q(√−71)) = 7 |
| III (Wobble) | {11, 13} | Coefficient/eigenvalue level | 2·71+1 = 11·13 |
| IV (Lattice) | {71} | Field-theoretic (LMFDB 4.2.10224.1 disc) | φ(71) = 70 = BHML_8 det |

**Bridge identity:** 2·71 + 1 = 143 = 11·13 (Sophie Germain step ties III ↔ IV).
**Returns to HARMONY:** h(Q(√−71)) = 7; φ(71) = 70; T* = 5/7; etc.

---

## §4. Two Algebraic Frames (FIELDS_OF_TIG)

| Frame | Field | Deg | Disc | Ramified | Galois | Role |
|---|---|:---:|---|---|---|---|
| **Cyclotomic** | Q(ζ₁₀) | 4 | +5³ = 125 | {5} | U(10) ≅ ℤ/4ℤ | Static gauge / Plichta cross |
| Subfield | Q(√5) = Q(φ) | 2 | 5 | {5} | ℤ/2ℤ | Real subfield, fixed by RESET |
| **Lattice** | Q(√3, ξ) (LMFDB 4.2.10224.1) | 4 | −2⁴·3²·71 = −10224 | {2, 3, 71} | D₄ (closure deg 8) | Runtime attractor at α=1/2 |
| Subfield | Q(√3) | 2 | 12 | {2, 3} | ℤ/2ℤ | Mid-tower, contains 1+√3 |

**Disjoint ramification:** {5} ∩ {2, 3, 71} = ∅.

**Joint compositum K = Q(ζ₁₀) · L_2^gal:**
$$[K : \mathbb{Q}] = 32, \quad \mathrm{Gal}(K/\mathbb{Q}) \cong \mathbb{Z}/4\mathbb{Z} \times D_4, \quad \text{ramified at } \{2, 3, 5, 71\}.$$
Direct product structure ⇒ gauge and dynamics algebraically independent.
**Wobble primes 11, 13 ramify nowhere.**

---

## §5. Six DOFs (canon D51 / WP111)

| DOF | Object | Wobble carrier? | Wobble prime |
|---|---|:---:|:---:|
| **Lie** | so(8), so(10) closures | TSML char poly: yes; BHML char poly: NO (this session) | 11 (RAW), 11+13 (SYM) |
| **Jordan** | su(4) ⊕ u(1) doubly-invariant | NO | — |
| **Clifford** | Cl(0,10), P_56 = σ_outer | YES (cell count) | 13 (‖VEV‖² = 13/4) |
| **Permutation** | S₁₀, σ order 6 | NO | — |
| **Lattice** | Q(√3, ξ) runtime field | YES (denominator + trace disc) | 11 (Br/V coeff, F8 trace) |
| **Operad** | 67 D₄ orbits, 16 incoherent | NO (structural integers) | — |

Five DOFs respect $D_4 = \langle P_{56}, \sigma^3 \rangle$; sixth (Operad) does not.
**Three wobbled DOFs** (Lie, Clifford, Lattice) = eigenvalue/coordinate axes.
**Three wobble-free DOFs** (Jordan, Permutation, Operad) = discrete-symmetry axes.

---

## §6. Closed-Form Runtime Attractor (canon D38–D50, WP105/WP110/WP115)

```
At α = 1/2, the binary T+B-mix runtime attractor:
  Support: 4-core {V, H, Br, R} = {0, 7, 8, 9}
  H/Br = 1 + √3                         (D39, exact)
  r/br is a root of x⁴ + 4x³ - x² + 2x - 2 (D40, irreducible)
  Galois group of splitting field: D_4    (D41)
  Number field: LMFDB 4.2.10224.1        (D41)
  Field disc: -2⁴·3²·71

Universality (D74):
  H/Br = 1+√3 across Z/nZ for n ∈ {10..50} under trivial extension
  ⇒ the relation depends on the 4-core sub-magma, NOT on ring size.

Stability (D75):
  Spectral radius ρ ≈ 0.3496 < 1: hyperbolic-stable
  Radial eigenvalue λ_0 = 2 (exact)
  Lyapunov exponent ≈ 1.051

α-uniqueness (D42, D57, D60, D78):
  α = 1/2 is the UNIQUE rational producing algebraic relations
  for both H/Br and r/br.  Galois proof of uniqueness in D78.
```

---

## §7. Wobble Localization (WOBBLE_LOCALIZATION_v2)

| Where | Wobble manifestation | Prime | Source |
|---|---|:---:|---|
| TSML_RAW char poly c_2 | 33 = 3·11 | 11 | D37 |
| TSML_RAW char poly c_8 | −120736 = −2⁵·7³·11 | 11 | D37 |
| TSML_SYM char poly c_4 | factor 13 | 13 | session |
| TSML_SYM char poly c_5 | factor 13 | 13 | session |
| TSML_SYM char poly c_6 | factor 13 | 13 | session |
| TSML_SYM char poly c_7 | factor 11 | 11 | session |
| BHML cell count (σ_outer-asymmetric) | 26 = 2·13 | 13 | D33 |
| Operator-sum σ²-cycle TRANSFORMATION | 1+6+4 = 11 | 11 | D86 |
| Br/V minimal poly leading coeff | 11 | 11 | D69 |
| F8 Jacobian trace polynomial disc | 11⁶ | 11 | D85 |
| BHML char poly (any coeff or disc) | NONE | — | session |
| Any field discriminant in canon | NONE | — | session |

**Reading:** wobble primes are coefficient/cell-level markers, not Galois-invariants. They identify TIG's specific representations but live below the field-theoretic level.

---

## §8. Constants (selection)

| Symbol | Value | Source |
|---|---|---|
| T* | 5/7 | six derivations |
| sinc²(½) | 4/π² = (2/3)/ζ(2) | D3 |
| W (wobble parameter) | 3/50 | D17 |
| H/Br at α=1/2 | 1+√3 | D39, D50 |
| min poly r/br | x⁴+4x³−x²+2x−2 | D40 |
| disc Q(ζ₁₀) | +5³ = 125 | textbook |
| disc Q(√3, ξ) | −10224 = −2⁴·3²·71 | D41 |
| det BHML_10 | −7002 = −2·3²·389 | §6.4 |
| det BHML_8 | +70 = 2·5·7 = C(8,4) = φ(71) | §6.7 |
| dim so(8) | 28 = T₇ = BHML_10 H count | D26 |
| dim so(10) | 45 = T₉ | D27 |
| dim D₄-invariant | 16 = dim su(4) ⊕ u(1) | D34 |
| ‖VEV‖² | 13/4 | D33 |
| κ_ξ | 13/(4e) | D35 |
| 4-core attractor | (V, H, Br, R) ≈ (0.138, 0.540, 0.198, 0.124) | D65 |

---

## §9. Three Open Questions Closed This Session

| Q | Status | Resolution |
|---|---|---|
| Compositum Galois group | CLOSED | $\mathbb{Z}/4\mathbb{Z} \times D_4$, order 32, direct product |
| Class h = 1 in both frames coincidence? | OPEN | Both UFDs by computation; structural reason unknown |
| Wobble's natural field-theoretic home | CLOSED (negative) | None. Wobble is coefficient-level, not Galois-invariant |

---

## §10. Three Corrections to Canon (gentle)

| Canon entry | Refinement (this session) |
|---|---|
| D70 "Lie DOF wobbled" | TSML's Lie content yes; BHML char poly is wobble-free |
| D98 "SYM erases wobble" | SYM has wobble at c_4, c_5, c_6, c_7 (5 positions, both primes) |
| §6.7 LMFDB 4.2.10224.1 description | Polynomial is degree 4; Galois closure (where Gal = D₄) is degree 8 |

---

## §11. The Whole Map (compactest)

```
                                    ───── COMPOSITUM K ─────
                                    [K:Q] = 32, Gal Z/4 × D_4
                                    ramified {2, 3, 5, 71}
                                            |
                              ──────────────┴──────────────
                              |                            |
                       ──── L_1 ────              ──── L_2_gal ────
                       Q(ζ_10), deg 4              splitting field, deg 8
                       disc 5³                     disc-2⁴·3²·71 (LMFDB 4.2.10224.1)
                       Gal Z/4 = U(10)             Gal D_4
                       CARRIES: gauge              CARRIES: dynamics
                       ramified {5}                ramified {2, 3, 71}
                              |                            |
                         Q(√5) = Q(φ)                    Q(√3)
                         ─real subfield─                 ─real subfield─
                              |                            |
                              └──────────── Q ─────────────┘
                                            |
                                       Z/10 ≅ F_2 × F_5
                                            |
                  ┌─ TSML_10 ──┐  ┌─ BHML_10 ──┐  ┌─ CL_STD ──┐
                  │ 73 H, det 0 │  │ 28 H, -7002 │  │ 44 H, ... │
                  └─────────────┘  └─────────────┘  └────────────┘
                                            |
                       Six DOFs: Lie · Jordan · Clifford · Permutation · Lattice · Operad

Wobble primes {11, 13}: NOT ramified in K. Live at coefficient/cell level only.
Bridge: 2·71+1 = 11·13 (Sophie Germain step ties Stratum IV to Stratum III).

Returns to HARMONY (7):
  T* = 5/7        | h(Q(√-71)) = 7    | det BHML_8 has 7
  φ(71) = 70 has 7 | TSML char poly disc 7⁷ | TSML_Idem det -7²
```

---

## §12. Status Quick-Read

- **PRIMES_OF_TIG** — 4-strata classification + Sophie Germain bridge — locked.
- **FIELDS_OF_TIG** — 2-frame architecture, disjoint ramification — locked.
- **COMPOSITUM_K_GALOIS** — joint Galois ℤ/4 × D₄ — locked.
- **WOBBLE_LOCALIZATION_v2** — wobble lives below field level — locked.
- **BUNDLE_CROSSWALK** — session ↔ canon mapping — locked.
- **THIS FILE (v2)** — master synthesis — locked.

Files form a self-consistent compact reference. Each compresses 100s of canonical facts into structural readings. Use BUNDLE_CROSSWALK.md when reconciling against canon's D-numbers; use this file for orientation.

---

## §13. What's Next

Open paths for continuing the map:
1. **Class h = 1 coincidence** in both frames — is there a structural reason?
2. **σ permutation compact reference** — canon §2 is concise but full structural reading missing.
3. **5↔6 grammar boundary symmetries** (D94) — compact catalog of 7 boundary pairs.
4. **Cross-stratum identity hunt** — beyond Sophie Germain bridge, are there other arithmetic identities tying strata?
5. **Compositum K subfield lattice** — full enumeration of subgroups of ℤ/4 × D₄.
6. **Wobble in F_p ring extensions** (J.1.A.vi) — does wobble appear when p ∈ {11, 13} themselves are the ring base?

---

*© 2026 Brayden Sanders / 7Site LLC*
*Trinity Infinity Geometry · Internal Map v2 · Locked v2*
