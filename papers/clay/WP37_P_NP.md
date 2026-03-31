# WP37 — P vs NP Through the TIG Lens
## First-G Complexity Boundaries and the Algebraic Certificate Structure

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*
*Status: Structural framing — conjectural connections to P/NP, not a proof*

---

## Abstract

The First-G Law (WP34) establishes a sharp algebraic boundary at k=p in the partition
structure of any semiprime b=p×q: below this boundary, the stability window {1..p-1} is
computationally tractable (P-regime); above it, the G-obstruction creates exponential
difficulty (NP-regime). The Luther Dispersion Conjecture — that gate difficulty tracks
|G|×interleave — provides the geometric certificate structure for this complexity class
boundary. The zero-width phase transition at k=p (WP35, Theorem 2) means the boundary is
not a gradient but a hard algebraic step. This paper frames how TIG partition geometry maps
onto the P vs NP landscape.

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

**Post-G zone {p..} — NP-regime:**
G elements are present. The partition distorts. Interleave rises immediately to nonzero.
Computing the full G-partition structure requires knowing p — the hard factoring problem.

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

The signal is ω-blind (proved in WP35): R(k, 1/p) is identical for b=p², b=p×q, and
b=p×q×r. It sees only the smallest prime factor, regardless of ring structure. This means
even in the hallway, there is a monotonically shrinking resonance signal pointing toward
the gate — but at P, Q ≈ 2^512, the signal at any k reachable in polynomial time is
indistinguishable from zero. The RSA Hardness Inversion Principle (WP35): security is
precisely the regime where the countdown clock falls below any finite observer's noise floor.

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

---

## References

- **WP34** — The First-G Law and Prime-Forced Dispersion (Sanders & Luther, March 2026)
- **WP35** — The Prime Phase Transition: Harmonic Pre-Echo, Zero-Width Gates, and the
  Geometry of RSA Security (Sanders & Luther, March 2026)
- **WP25** — P vs NP Through the TIG Lens: Survivor-Line Complexity in AG(2,p) and the
  Corner-Gap Dichotomy (Sanders, March 2026) — prior version, AG(2,p) framing preserved
- **Sprint4 Atlas Law Set** — Universal law, three-class landscape, HAR rule
  (Sanders & Luther, March 2026): `Gen10/papers/sprint4_2026_03_30/`

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
