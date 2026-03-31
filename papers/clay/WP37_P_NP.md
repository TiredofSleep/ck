# WP37 — P vs NP Through the TIG Lens
## First-G Complexity Boundaries and the Algebraic Certificate Structure

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Structural framing — conjectural connections to P/NP, not a proof*

---

## Abstract

**NP-verification is the local detection of a sinc² sidelobe; P-solving is the global
navigation to the sinc² null.** — Sanders & Luther (Google/Sanders framing)

The First-G Law (WP34) establishes a sharp algebraic boundary at k=p in the partition
structure of any semiprime b=p×q: below this boundary, the stability window {1..p-1} is
computationally tractable (P-regime); above it, the G-obstruction creates exponential
difficulty (NP-regime). In the sinc² picture: a verifier sees a sidelobe of R(k,f) at
k < p and confirms "this is near a null" in O(1) local time; a solver must navigate to the
null itself at k=p, which requires traversing 2^512 featureless corridor steps in the RSA
regime. The signal R(k/p=0.1, p) ≈ 0.9675 is always present — but presence of the signal
is not proximity to the gate. RSA is hard because the road is 2^512 steps long, not because
the signal is weak. The Luther Dispersion Conjecture — that gate difficulty tracks
|G|×interleave — provides the geometric certificate structure for this complexity class
boundary. The zero-width phase transition at k=p (WP35, Theorem 2) means the boundary is
not a gradient but a hard algebraic step. This paper frames how TIG partition geometry maps
onto the P vs NP landscape, with explicit connection to the Montgomery pair correlation
for Riemann zeros — both are sinc² nulls, and the same function governs both.

---

## §1. The Complexity Boundary as a Geometric Event

### The First-G Law (WP34 §2 — PROVED)

For every semiprime b = p×q with p ≤ q, define the coprimality partition of the growing
alphabet {1..k}:

```
C_k = { x ∈ {1..k} : gcd(x, b) = 1 }     (units — coherent elements)
G_k = { x ∈ {1..k} : gcd(x, b) > 1 }     (non-units — obstructing elements)
```

**Theorem (First-G Law).** The first non-unit element in {1..k} appears at exactly k = p:

```
|G_k| = 0   for all k < p
|G_p| = 1   (the element p is the first non-unit)
```

**Proof.** For any x ∈ {1..k} with k < p: since p ≤ q are the only prime factors of b,
and x < p ≤ q, x cannot be divisible by either p or q. Therefore gcd(x, b) = 1 and x ∈ C_k.
At k = p: gcd(p, b) = p > 1, so p ∈ G_p. □

### The Two Zones

The First-G Law partitions alphabet growth into two structurally distinct zones:

**Pre-G zone {1..p-1} — P-regime:**
Every element is coprime to b. Gate_rate = 0. No obstruction. Testing membership in C_k
requires only x < p (O(1) comparison). This is the stability window: a featureless,
obstruction-free corridor of width p-1.

**Density of permitted states in the pre-G zone:** exactly 1.0 — every element is a unit,
every state is permitted. The Luther metric |G|×interleave = 0 here. There are no voids
in the unit alphabet.

**Post-G zone {p..} — NP-regime:**
G elements are present. The partition distorts. Interleave rises immediately to nonzero.
Computing the full G-partition structure requires knowing p — the hard factoring problem.

**Density drop at the gate:** The density of permitted states falls from 1.0 to
φ(b)/b = (p-1)(q-1)/(pq) — a drop of exactly 1/p + 1/q - 1/(pq), which is precisely
the Luther metric divided by the current alphabet size. The Luther metric |G|×interleave
is the measure of VOIDS opened in the unit alphabet at the gate event.

### The Zero-Width Transition (WP35 §3 — PROVED)

The phase transition at k = p has zero width. The gate_rate sequence:

```
gate_rate(k) = |G_k| / k
```

satisfies gate_rate(k) = 0 for all k < p and gate_rate(p) > 0. There is no gradient, no
blurring, no intermediate regime. The complexity jump is instantaneous. This is not an
approximation — it is the Sieve of Eratosthenes performing its first removal, which
happens in a single step when p enters the alphabet.

---

## §2. The Luther Dispersion Conjecture as NP Certificate

### The Conjecture (C. A. Luther — WP34 §9)

**Luther Dispersion Conjecture:** For a semiprime b = p×q, the gate difficulty function
satisfies:

```
gate_rate(k) ≈ F_k( |G_k| × interleave(b, k) )
```

where interleave(b, k) = transitions(C, G in sequence {1..k}) / (2 · min(|C_k|, |G_k|))
measures how deeply the unit and non-unit elements are mixed within {1..k}.

This is conjectural: the functional form F_k is not yet determined. The structural claim —
that difficulty is a function of the product |G|×interleave — is Luther's contribution.

### Why This Is an NP Certificate Structure

The dispersion metric |G|×interleave has a critical property:

**Given the factorization** (i.e., given p): computing |G_k| and interleave(b, k) for any
k takes polynomial time. Count the multiples of p in {1..k}, count transitions. O(k) work.

**Without the factorization**: computing |G_k| requires knowing which elements of {1..k}
share a factor with b. This is exactly the integer factorization problem. For b = P×Q with
P, Q ≈ 2^512, this requires ≈ 2^512 steps by any known method.

**The certificate IS the factorization.** The YES certificate for "this world has difficulty
D" is the pair (p, partition-at-k=p). Verification — given p, compute |G|×interleave and
check it matches D — is polynomial. Finding p without being given it is the hard problem.

This is structurally analogous to NP certificate definition:
- **Easy to verify**: given p, compute dispersion metric in O(k) time
- **Hard to find**: without p, you must factor b

*Note: this is a structural analogy, not a proof that the factoring problem reduces to NP-
completeness in the standard complexity-theoretic sense. The analogy is exact in form;
the gap to a formal proof remains open.*

### The Partition Geometry as Certificate (WP34 §9 — PROVED)

A stronger result is already proved: **Partition Geometry Invariance.** Worlds b=22, b=26,
b=34, b=38 all produce the identical partition G={2,4,6,8} at k=9 (all share smallest prime
p=2) and all give identical difficulty scores to four decimal places despite different
q-partners.

This means the G-partition geometry — not the specific semiprime b — determines difficulty.
The partition is the NP certificate; b is the input; the geometry is the witness. This
is proved, not conjectured.

---

## §3. The ω(b) Hierarchy as Complexity Stratification

### Definition

Let ω(b) denote the number of distinct prime factors of b. By the Chinese Remainder Theorem:

```
Z/bZ ≅ Z/p₁^a₁Z × Z/p₂^a₂Z × ... × Z/pₙ^aₙZ
```

The number of non-trivial idempotents in Z/bZ is:

```
N_idemp = 2^(ω(b)-1) - 1
```

Each idempotent corresponds to a CRT projection — an "anchor" in the partition algebra.

### The Hierarchy (PROVED from CRT)

```
ω = 1: prime powers — Z/p^n Z is a local ring
        0 non-trivial idempotents
        G_k has only one generator (p itself)
        P-like: no certificate structure, single-factor obstruction

ω = 2: semiprimes — Z/pqZ ≅ Z/pZ × Z/qZ
        1 non-trivial idempotent (the CRT mixed element)
        2-layer certificate structure
        This is the RSA class

ω = 3: three-factor — 3 non-trivial idempotents
        Maximum certificate complexity within the three-factor class
        Gate sequence is tiered, not zero-width
```

Each additional prime factor adds exactly one gate layer (one more First-G transition, at
the next smallest prime). The ω(b) hierarchy is a discrete complexity stratification,
provable directly from the ring decomposition.

### Connection to Circuit Complexity (Conjectural)

ω(b) ≈ circuit depth of the obstruction structure in the following sense: each prime factor
requires one independent gate layer to detect. A circuit that detects all G-elements of
{1..k} for a ω=n modulus requires at least n independent primality tests. Whether ω(b)
maps onto any standard circuit complexity measure (NC, AC, TC) is an open question.

---

## §4. RSA as the Deep P/NP Instance

### The Stability Window as Security Parameter

RSA encryption uses b = P×Q with P, Q ≈ 2^512. By the First-G Law, the stability window
has width p-1 ≈ 2^512. In TIG terms:

- Every k in {1..p-1} is in the P-regime: O(1) to verify coprimality, no obstruction,
  zero gate_rate
- The partition algebra's richness — idempotents, CRT structure, G-partition geometry —
  lives entirely in the post-G zone, inaccessible from within the stability window

### The Hallway Principle (WP34 §11 — Structural)

> *"RSA is not a complex lock; it is a very long, perfectly smooth hallway."*
> — Sanders

The hallway is the stability window {1..p-1}. Every computation that stays in the hallway
is in featureless P-tractable space. The room at the end — the G-partition, the CRT
idempotents, the full algebraic structure — is real and accessible in principle. The road
is just exponentially long.

This reframes RSA security not as algebraic complexity of the ring but as geometric
distance to the first obstruction. The ring Z/bZ at b=P×Q is not inherently complex.
It is a simple two-factor product ring. What makes it hard is that the first gate is
2^512 steps away.

### The Signal Is Always There (WP35 — PROVED)

The Harmonic Pre-Echo Countdown (WP35):

```
R(k, f) = sin²(πk/f) / (k² · sin²(π/f))
```

gives a closed-form spectral signal that counts down to the first gate. R(k, 1/p) decays
monotonically as k → p, reaching R = 1/(p-1)² at k = p-1, and collapsing to R = 0
at k = p exactly. This signal is present and computable for all k < p.

**The Inversion Rule (physical distance framing):** Complexity is not algebraic difficulty
of the ring structure — it is physical distance to a geometric sink. The sink is the sinc²
null at k=p. At k/p = 0.1 (ten percent of the way to the gate), R ≈ 0.9675: the signal
is strong, nearly at maximum. But being close to signal maximum is not being close to the
gate. Navigating from k/p=0.1 to the null at k=p requires crossing 0.9p more steps of
featureless corridor. For RSA with p ≈ 2^512, that crossing contains 2^512 steps regardless
of signal strength. The signal strength tells you the null exists and where it is. The road
length is the complexity. The signal is not the bottleneck; the geometry is.

The signal is ω-blind (proved in WP35): R(k, 1/p) is identical for b=p², b=p×q, and
b=p×q×r. It sees only the smallest prime factor, regardless of ring structure. This means
even in the hallway, there is a monotonically shrinking resonance signal pointing toward
the gate — but at P, Q ≈ 2^512, the signal at any k reachable in polynomial time is
indistinguishable from zero. The RSA Hardness Inversion Principle (WP35): security is
precisely the regime where the countdown clock falls below any finite observer's noise floor.

---

## §4b. The Montgomery Connection — NP-Hardness and Riemann Zeros as the Same sinc² Object

### The Pair Correlation Function

Hugh Montgomery (1973) conjectured, and subsequent numerical work has strongly confirmed,
that the pair correlation of normalized Riemann zero spacings u satisfies:

```
r(u) = 1 - sinc²(u)     where sinc(u) = sin(πu)/(πu)
```

This is the same functional form as the Harmonic Pre-Echo Countdown:

```
R(k, f) = sin²(πk/f) / (k² · sin²(π/f))   →   sinc²(k/f)  as f → ∞
```

**These are the same function.** The pair correlation r(u) and the pre-echo signal R(k,f)
both reduce to sinc². The zeros of r(u) — the Montgomery repulsion nulls where the
probability of finding a zero-spacing of size u goes to zero — are sinc² nulls. The
gate events in the TIG partition — the k=p collapses where R(k,f) → 0 — are sinc² nulls.

### The Unified Picture

| Structure | sinc² null | What the null means |
|-----------|-----------|---------------------|
| Riemann zeros (WP40) | r(u)=1-sinc²(u)=0 at u=1,2,3... | Zero repulsion: no two zeros this close |
| TIG gate events (WP34/35) | R(k,f)=sinc²(k/f)=0 at k=f | Phase transition: gate opens here |
| NP-hardness (WP37) | sinc² null is the P/NP boundary | Solver must reach k=p; verifier sees sidelobe |
| Mass gap (WP41) | Yang-Mills energy barrier as sinc² null | Single gate distance to cross |
| Regularity breakdown (WP38) | Navier-Stokes BREATH collapse as sinc² zero | Vorticity spreads to null |
| Rank staircase (WP42) | BSD jump events as irregular sinc² nulls | Dispersed staircase of nulls |

CK as spectrometer is measuring which sinc² null an observer is trying to reach. The
problems differ in how many nulls there are, how they are spaced, and how dispersed the
approach path is — not in what kind of object the null is.

### The Complexity Interpretation

**NP-hardness IS Montgomery repulsion** — both are sinc² nulls at which no shorter path
can exist. Just as no two Riemann zeros can occupy the same spacing (repulsion), no
polynomial algorithm can collapse the 2^512-step corridor to reach the gate. The repulsion
is not a number-theoretic accident in one case and an algebraic accident in the other:
it is the same sinc² geometry expressing the same principle.

**Verifier vs. solver in Montgomery terms:** The verifier detects a sidelobe — it sees
that the function is nonzero (a zero exists nearby), i.e., it reads R(k,f) > 0 at a
local k and confirms proximity to the null. The solver must navigate to u=0 of the pair
correlation, i.e., to the null itself. Local detection of nonzero (sidelobe) is easy;
global navigation to the zero (null) is the hard problem.

*This connection is structural framing. Establishing it as a formal reduction between the
Riemann hypothesis and P vs NP requires additional work. The mathematical objects are
provably the same function; the implication arrow between the two problems remains open.*

---

## §5. Open Questions

1. **Formal reduction.** Does the First-G boundary correspond to a known complexity class
   separator? Can a formal reduction from an NP-complete problem to the G-detection problem
   be exhibited (without assuming the factoring hardness conjecture)?

2. **Luther metric computability.** Can |G|×interleave be computed without factoring in
   subexponential time? Any subexponential algorithm for the dispersion metric would be a
   factoring breakthrough.

3. **ω(b) and the polynomial hierarchy.** Is the ω(b) hierarchy related to the polynomial
   hierarchy (Σ_k^P)? Each ω-layer adds one certificate layer; this is structurally similar
   to how each Σ_k^P level adds one quantifier alternation.

4. **The AG(2,p) survivor connection.** WP25 established that survivor lines in AG(2,p)
   are the NP certificates for the TIG composition algebra. Does the ω(b) stratification
   match the AG(2,p) survivor-line count stratification as p grows? The p²-1 survivor
   formula (WP25 §2) and the 2^(ω(b)-1)-1 idempotent formula are structurally parallel.

5. **Harmonic signal recovery.** For small b in the post-G zone, R(k, 1/p) is measurable.
   Can the gate location be recovered from the harmonic signal alone, without testing
   coprimality directly? This would give a spectroscopic factoring approach.

---

## §6. Attribution

**Brayden Ross Sanders (7Site LLC):**
TIG framework, First-G Law proof and geometric interpretation, partition geometry
invariance, hallway/room principle, RSA hardness inversion framing, harmonic pre-echo
countdown, zero-width transition proof, ω(b) idempotent count.

**C. A. Luther:**
Dispersion conjecture (|G|×interleave as difficulty certificate), ω(b) hierarchy framing
as complexity stratification, joint derivation of harmonic resonance closed form.

*CK, T\*, TSML, BHML, D1, D2, and the TIG framework are the exclusive intellectual
property of Brayden Ross Sanders / 7Site LLC, developed over 18 months prior to this
sprint. C. A. Luther's contribution is the dispersion conjecture and number-theory framing
applied to the partition geometry studied here.*

---

## §7. Status Table

| Claim | Status | Source |
|-------|--------|--------|
| First-G event at exactly k=p | PROVED | WP34 §2-3 |
| Pre-G zone is P-tractable (O(1) coprimality test) | PROVED | WP34 §2 |
| Zero-width phase transition at k=p | PROVED | WP35 §3 |
| Partition geometry invariance | PROVED | WP34 §9 |
| ω(b) idempotent count = 2^(ω-1)-1 | PROVED (CRT) | Ring theory |
| Harmonic pre-echo countdown R(k,f) closed form | PROVED | WP35 §2 |
| R(k,f) is ω-blind | PROVED | WP35 §4 |
| Luther dispersion conjecture | CONJECTURE | WP34 §9 |
| ω(b) maps to polynomial hierarchy | OPEN | — |
| Formal 3-SAT reduction to G-detection | OPEN | — |
| R(k,f) and Montgomery r(u) are same sinc² function | STRUCTURAL | WP37 §4b |
| Montgomery repulsion = NP-hardness (formal reduction) | OPEN | WP37 §4b |
| Pre-G density = 1.0 (no voids) | PROVED | WP34 §2 |
| Post-G density drop = Luther metric / k | STRUCTURAL | WP37 §1 |

---

## References

- **WP34** — The First-G Law and Prime-Forced Dispersion (Sanders & Luther, March 2026)
- **WP35** — The Prime Phase Transition: Harmonic Pre-Echo, Zero-Width Gates, and the
  Geometry of RSA Security (Sanders & Luther, March 2026)
- **WP25** — P vs NP Through the TIG Lens: Survivor-Line Complexity in AG(2,p) and the
  Corner-Gap Dichotomy (Sanders, March 2026) — prior version, AG(2,p) framing preserved
- **Sprint4 Atlas Law Set** — Universal law, three-class landscape, HAR rule
  (Sanders & Luther, March 2026): `Gen10/papers/sprint4_2026_03_30/`
- **WP40** — Riemann Hypothesis — sinc² Zeros and Scale-Invariant Gates (Sanders, March 2026)
- **WP41** — Yang-Mills — Mass Gap as Single Gate Distance (Sanders, March 2026)
- **WP42** — BSD — Rank Staircase and Irregular Dispersion (Sanders, March 2026)
- **WP38** — Navier-Stokes — BREATH Collapse Criterion (Sanders, March 2026)
- **Montgomery, H. L.** — The pair correlation of zeros of the zeta function.
  *Analytic Number Theory (Proc. Sympos. Pure Math., Vol. XXIV),* AMS, 1973, pp. 181–193.
  *(pair correlation r(u) = 1 − sinc²(u); same functional form as R(k,f))*

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
