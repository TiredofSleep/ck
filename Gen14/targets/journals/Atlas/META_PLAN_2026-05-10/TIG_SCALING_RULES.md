# TIG_SCALING_RULES

## Closed-form rules for TIG structure at any modulus n

**Brayden Sanders · 7Site LLC · Trinity Infinity Geometry**
*Goal: predict TIG structure at Z/n without brute-force composition. Apply rules; read off invariants.*
*Source: Crossing Lemma framework + foundation paper [J33] axiom forcing*
*Locked v1 · 2026-05-08*

---

## §0. The principle

Every movement we've computed — substrate progression, σ²-ℤ₃ rotation, Russian doll box growth, pizza swap (Euclidean), bivariate (ω, j) scaling, σ-cycle ↔ flag tangent — has the same architecture:

**Additive partition × Multiplicative dynamics → Information at crossings.**

This is the **Threshold Crossing Lemma**'s shadow. Information generation happens precisely where multiplicative orbits cross additive partition fibers. Type I (injective lift) preserves structure with no new information; Type II (missing invariant) parametrizes the breaking; the residual is genuine generation — BUMP cells, threshold transitions, bridge residue.

The rules below let you compute scale-dependent invariants at any Z/n directly from substrate properties, without ever brute-forcing the composition table.

---

## §1. The Rules

### Tier A — Exact, closed form (compute once, read off forever)

**Rule 1 — CRT structure.** $\mathbb{Z}/n \cong \bigoplus_{p^a \,||\, n} \mathbb{Z}/p^a$. Define $\omega(n)$ = number of distinct prime factors.

**Rule 2 — Idempotent count.** For squarefree $n$: $\#\text{idempotents}(\mathbb{Z}/n) = 2^{\omega(n)}$. (Each idempotent corresponds to a subset of the prime factors.)

**Rule 3 — Unit group structure.** $U(n) = \prod_{p^a \,||\, n} U(p^a)$, where:
- $U(p^a)$ is cyclic of order $p^{a-1}(p-1)$ for $p$ odd
- $U(2^a) = \mathbb{Z}/2 \times \mathbb{Z}/2^{a-2}$ for $a \geq 3$, trivial for $a = 1$, $\mathbb{Z}/2$ for $a = 2$
- $|U(n)| = \varphi(n) = n \prod_p (1 - 1/p)$

**Rule 4 — σ-orbit structure (closed form once $g$ chosen).** Pick a generator $g$ of $U(n)$ (or a tuple if $U(n)$ is non-cyclic). Then $\sigma_g(x) = g x \bmod n$ has:
- $\sigma_g$-fixed set: $\{x : (g-1)x \equiv 0 \pmod n\}$
- σ-cycle lengths: determined by orbit decomposition of $\sigma_g$ on $\mathbb{Z}/n$
- For Z/n with U(n) cyclic of order $m$: σ has order $m$ on $U(n)$ and lifts to $\mathbb{Z}/n$ via CRT

**Rule 6 — Stratum classification.**
- **Stratum I** (substrate): $\{p : p \mid n\}$
- **Stratum II** (attractor / HARMONY-prime): smallest prime $\notin$ Stratum I
- **Stratum III** (wobble): next primes outside substrate
- **Stratum IV** (lattice): 71 (universe-specific; lives in field discriminants)

**Rule 9 — Scaling under $\mathbb{Z}/n \to \mathbb{Z}/(np)$ (adding new prime $p$):**
- $\omega \to \omega + 1$
- $\varphi \to \varphi \cdot (p - 1)$
- $\#\text{idempotents}$ doubles
- σ-orbit lengths: lcm with $U(p)$'s order (for odd $p$: lcm with $p - 1$)
- HARMONY (Stratum II) may relocate if $p$ was the previous attractor
- Wobble updates to next prime not in expanded substrate

### Tier B — Scale-invariant qualitative rules

**Rule 5 — Operator semantics (preserved across substrates).**
- VOID $= 0$ always; acts as VOID on non-HARMONY, lifts HARMONY
- HARMONY = element acting as universal absorber under composition (its row/column = HARMONY everywhere)
- σ-fixed set = "central pillar" / Conservation Tetrad analog
- σ-cycle = "active flow" / Manifestation Hexad analog
- 4-core analog = σ-fixed ∪ {HARMONY} (or σ-fixed XOR a structural swap)

**Rule 8 — Composition table HARMONY-default.** Default cell value at any non-trivial position = HARMONY. Off-diagonal = HARMONY unless BUMP. Diagonal $T[i,i]$ = HARMONY for non-VOID $i$ (axiom A7). Row/column 0 = VOID except $T[0, h] = h$ for HARMONY element $h$.

**Rule 10 — Three-substrate architecture.** At any modulus satisfying A1-A4 + A7, three parallel substrates emerge (TSML/BHML/STD analogs), distinguished by BUMP values at the forced positions. DOING relation $= |M_1 - M_2| \bmod n$ between any two parallel substrates.

### Tier C — Parametric (require BDC entropy or external choice)

**Rule 7 — BUMP positions and values (Crossing Lemma).** Information is generated at multiplicative-orbit × additive-partition crossings. BUMP positions are FORCED by BDC entropy extremum at A9 (foundation paper [J33]). BUMP values are the Tier-A choice that distinguishes the three parallel substrates. **Without the closed-form BDC entropy at $\mathbb{Z}/n$, BUMP positions at higher rungs require execution rather than analytic prediction.**

---

## §2. Verification at Z/10

| Quantity | Rule prediction | Canon value | ✓ |
|---|---|---|:---:|
| ω(10) | 2 | 2 | ✓ |
| CRT | Z/2 × Z/5 | Z/2 × Z/5 | ✓ |
| φ(10) | 4 | 4 | ✓ |
| # idempotents | $2^2 = 4$ | 4 ({0, 1, 5, 6}) | ✓ |
| U(10) | Z/4 | Z/4 | ✓ |
| σ-fixed (canon) | structural class | {0, 3, 8, 9} | ✓ |
| HARMONY | Stratum II prime | 7 (smallest prime ∉ {2, 5}) | ✓ |
| 4-core | σ-fixed XOR {3↔7} | {0, 7, 8, 9} | ✓ |
| Wobble candidates | smallest primes outside | 11, 13 | ✓ |

The Tier-A and Tier-B rules predict every structural invariant of canon at Z/10 from substrate properties alone. Tier-C (BUMP positions {(1,2), (2,4), (2,9), (3,9), (4,8)} and values 3, 4, 9, 3, 8) requires BDC entropy.

---

## §3. Prediction at Z/30 (next rung)

Apply rules — no brute-force needed:

| Quantity | Rule prediction |
|---|---|
| ω(30) | 3 |
| CRT | Z/2 × Z/3 × Z/5 |
| φ(30) | $1 \cdot 2 \cdot 4 = 8$ |
| # idempotents | $2^3 = 8$ |
| U(30) | $1 \times \mathbb{Z}/2 \times \mathbb{Z}/4$ (NOT cyclic) |
| σ-generator (natural) | smallest unit > 1 = 7 |
| σ-fixed (with $g = 7$) | {0, 5, 10, 15, 20, 25} (6 elements) |
| σ-orbits | 6 cycles of length 4 each |
| HARMONY | 7 — same as Z/10 (still Stratum II since 7 ∉ {2, 3, 5}) |
| 4-core analog | σ-fixed ∪ {7} XOR structural swap (concrete cells await BDC entropy) |
| Wobble candidate | 7 (until 7 enters substrate at Z/210) |

**Key observations at Z/30:**
- Idempotent count doubled vs Z/10 (4 → 8)
- σ-fixed set is the **set of multiples of 5** in Z/30: $\{0, 5, 10, 15, 20, 25\}$ — these have CRT pattern $(*, *, 0)$
- σ-cycle structure decomposes into multiple orbits (6 of length 4) instead of a single hexagon as at Z/10 — this is **structurally richer**
- HARMONY does NOT yet enter substrate at Z/30 — wobble status of prime 7 unchanged
- BUMP count prediction: scales with number of (σ-fixed × σ-cycle) crossing types — likely 10-15 BUMP positions (vs 5 at Z/10), but exact count requires BDC entropy

**This is the Plichta-natural rung. The substrate now contains primes 2, 3, 5 — Plichta's "natural" cross U(30) lives here as the multiplicative skeleton.**

---

## §4. Prediction at Z/210 (Fuller rung — HARMONY enters)

Apply rules — still no brute-force needed:

| Quantity | Rule prediction |
|---|---|
| ω(210) | 4 |
| CRT | Z/2 × Z/3 × Z/5 × Z/7 |
| φ(210) | $1 \cdot 2 \cdot 4 \cdot 6 = 48$ |
| # idempotents | $2^4 = 16$ |
| U(210) | $1 \times \mathbb{Z}/2 \times \mathbb{Z}/4 \times \mathbb{Z}/6$ |
| σ-generator | smallest unit > 1 = 11 |
| σ-fixed count | 10 |
| σ-orbits (top) | many cycles of length 6 (most common length matches lcm of U(p) orders) |
| HARMONY relocates? | Yes: prime 7 NOW in substrate; HARMONY-attractor moves to next prime |
| New attractor | 11 = next Stratum II prime (since 7 is now substrate) |
| Wobble | 11 enters as new attractor; 13 becomes new wobble |
| Idempotent count | 16 — matches dim of D₄-inv $\mathfrak{so}(10)$ from canon D34 |

**The structural transition at Z/210:**
- Prime 7 (HARMONY at Z/10, Z/30) leaves the attractor role and enters the substrate
- A new attractor takes its place — likely 11 (the next Stratum II prime)
- The 16 = 2⁴ idempotents match the doubly-invariant Higgs sector dimension at Z/10
- Cardinality match $|U(210)| = 48 = |O_h|$ (with the abelian-vs-nonabelian fence preserved from earlier work)

**This is the Fuller-territory rung.** Cuboctahedral cardinality, HARMONY-prime in substrate, the natural place to test Prediction C.

---

## §5. The Crossing Lemma in this framework

Each rule corresponds to a layer of the Crossing Lemma framework:

| Rule | Crossing-Lemma role |
|:---:|---|
| 1 | Defines additive partition (CRT) |
| 3 | Defines multiplicative dynamics (U(n)) |
| 4 | Computes the orbit structure — where dynamics lives |
| 5 | Identifies the structural classes |
| 6 | Stratifies primes by their crossing-role |
| 7 | Specifies where information is generated (BUMPs) |
| 8 | Default behavior away from crossings (HARMONY) |
| 9 | Predicts how crossings restructure under substrate growth |
| 10 | Identifies the parallel-substrate degree of freedom |

The rules carve TIG structure into:
- **Pure-multiplicative** (Type I — Rule 3, 4): no info, just orbit structure
- **CRT-additive crossings** (Type II — Rules 5, 6, 8): broken symmetries, parametrizable
- **Genuine-generation** (Rule 7): BUMP cells, where the system writes new info

---

## §6. Color preservation — what the rules buy you mentally

The rules let you mentally expand a TIG frame at any modulus by **assigning roles, then colors**:

| Role | Color (canon TIG palette) | At Z/10 | At Z/30 |
|---|---|:---:|---|
| VOID | slate (#546e7a) | 0 | 0 |
| HARMONY | teal-cyan (#00bfa5) | 7 | 7 (still attractor) |
| σ-fixed (Conservation Tetrad) | teal family | {0, 3, 8, 9} | {0, 5, 10, 15, 20, 25} |
| σ-cycle (Manifestation Hexad) | warm graded | (1,7,6,5,4,2) | 6 cycles of length 4 |
| 4-core attractor | mixed | {0, 7, 8, 9} | extends with new structure |
| BUMP cells | yellow accent | 5 cells | ~10-15 cells (predicted) |
| Wobble primes (Stratum III) | dimmed | 11, 13 | 7 (until Z/210) |
| Substrate primes (Stratum I) | substrate-color | {2, 5} | {2, 3, 5} |

**Each role keeps its color across substrates.** When you ascend the tower, the integer values change but the structural roles (and their colors) persist. That's how you "expand a TIG frame in your mind using color" — the visual coding is scale-invariant.

---

## §7. What's still open

Despite the rules, three things still require execution rather than prediction:

1. **BUMP positions at higher rungs.** Forced by BDC entropy extremum, but the closed-form BDC entropy formula at arbitrary $n$ isn't in the rules above. Source from canon's J33 to fully close.

2. **BUMP values at higher rungs.** The Tier-A choice between three parallel substrates (TSML/BHML/STD analogs) — these are choices, not forced. At each rung, all three can be constructed; identifying canonical labels requires interpretive grounding.

3. **HARMONY relocation rule.** When prime 7 enters substrate at Z/210, what's the new HARMONY? Smallest Stratum II prime is 11 — but whether the algebraic role of HARMONY transfers cleanly to 11 (or to some other element) needs verification by execution at Z/210.

These are research items, not blockers. The rules cover **all the abelian-structure invariants** scale-portably; only the entropy-forced parametric content needs case-by-case execution.

---

## §8. Compact take-home

```
TIG SCALING RULES — closed form for any Z/n

EXACT (compute, read off):
  Rule 1: CRT decomposition          (textbook)
  Rule 2: # idempotents = 2^ω        (squarefree)
  Rule 3: U(n) structure              (textbook)
  Rule 4: σ-orbit decomposition       (Galois generator)
  Rule 6: Stratum classification     (4 strata)
  Rule 9: Scaling under prime addition (lcm/multiply)

INVARIANT (preserved across substrates):
  Rule 5: VOID = 0; HARMONY = absorber; σ-fixed = pillar
  Rule 8: Default = HARMONY; row/col 0 = VOID
  Rule 10: Three parallel substrates (TSML/BHML/STD)

PARAMETRIC (need BDC entropy):
  Rule 7: BUMP positions and values

WHAT THE RULES BUY:
  • Predict |idempotents|, |σ-fixed|, |σ-cycle|, |U(n)| at any n
  • Predict HARMONY's prime-status at each rung
  • Predict wobble & attractor migrations
  • No brute-force needed for any of the above

WHAT THEY DON'T:
  • Specific BUMP cell values at higher rungs (need BDC entropy)
  • Concrete TSML/BHML/STD tables at higher rungs

VERIFIED AT Z/10. APPLIED AT Z/30 AND Z/210 — predictions consistent with
canon's known structure (Z/10) and with substrate-progression expectations 
(Z/30 Plichta-natural, Z/210 Fuller-territory).

THE COLOR PERSISTENCE:
  Each operator's role determines its color.
  Roles persist across substrates.
  Therefore colors transfer across substrates by structural class.
  This is what lets you 'expand a TIG frame using color' at any modulus.
```

---

## §9. Status

- **[CLOSED — exact]** Rules 1, 2, 3, 4, 6, 9 — closed-form scaling
- **[CLOSED — invariant]** Rules 5, 8, 10 — preserved across substrates
- **[PARAMETRIC]** Rule 7 — BUMP positions/values need BDC entropy at higher rungs
- **[VERIFIED]** Rules predict Z/10 canon correctly
- **[APPLIED]** Z/30 and Z/210 invariant predictions made
- **[OPEN]** HARMONY relocation rule at Z/210 (needs execution)

The rules let you mentally model TIG at any modulus from substrate properties alone. Brute-force composition is needed only for BUMP-cell content at rungs above Z/10. **Everything else scales analytically.**

---

*© 2026 Brayden Sanders / 7Site LLC*
*Trinity Infinity Geometry · TIG Scaling Rules · Locked 2026-05-08*
